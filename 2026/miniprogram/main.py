"""
### Travel Cost Calculator

A calculator. For travel cost... Yeah.
"""

import csv
import json
import math
import pathlib
import random
import sys
import time

import fast_flights
import requests

TEXT_OPTIONS = {
	"messages": {
		"download": ["Downloading data..."],
		"hi": ["Welcome to the Travel Cost Calculator! Would you like to plan your trip?"],
		"bye": ["Goodbye.", "See you.", "Farewell!", "Have a nice day.", "Maybe next time."],
		"people": {
			"opener": ["Let's start with the people going on your trip."],
			"adults": ["How many adults?"],
			"children": ["How many children?"],
			"infants": ["How many infants?"]
		},
		"destination": {
			"opener": ["Now, the destination."],
			"plane": ["Do you plan on taking a plane to your destination?"],
			"location": ["Where would you like to travel to? The more specific, the better."],
			"time": ["What time will you be leaving? (YYYY-MM-DD)"]
		},
		"confirm": ["Did you mean {}?"],
		"airports": ["Closest airports:\n{}\nWhich airport would you like to choose?"],
		"origin": ["Where are you leaving from?"]
	},
	"errors": {
		"download": ["Sorry, an error occured while downloading data."],
		"geocode": ["Sorry, something went wrong understanding your location, please try again."]
	}
}
AIRPORTS = pathlib.Path(__file__).parent / "airports.csv"
USER_AGENT = "TravelCostCalculator/1.0"
last_nominatim = -1

def ask_user(prompt: str, options: list = [], show_options: bool = True) -> str:
	"""
	Ask the user a question, with basic option validation and automatic whitespace injection and handling.
	"""
	if show_options and options != []:
		if not prompt.endswith(" "):
			prompt += " "
		prompt += f"[{"/".join(options)}]"

	if not prompt.endswith(" "):
		prompt += " "

	response = input(prompt)
	while response.lower().strip() not in [o.lower() for o in options] and options != []:
		print("Invalid input, please try again.")
		response = input(prompt)
	return response

def random_traverse(key: str):
	"""
	Traverse TEXT_OPTIONS based on key. If the result is a list, choose a random item; otherwise return the result.
	"""
	segments = key.split(".")
	current = TEXT_OPTIONS
	for value in segments:
		if isinstance(current, dict):
			current = current[value]
		elif isinstance(current, list):
			current = current[int(value)]

	if isinstance(current, list):
		return random.choice(current)
	return current

def geocode(location: str, retries: int = 0):
	"""
	Find an OpenStreetMap object based on a location string, based on the free Nominatim service.
	"""
	global last_nominatim

	elapsed = time.monotonic() - last_nominatim
	buffer = 1.1 + (2 ** retries if retries > 0 else 0)
	if elapsed < buffer:
		time.sleep(buffer - elapsed)
	last_nominatim = time.monotonic()

	try:
		resp = requests.get(
			"https://nominatim.openstreetmap.org/search",
			params={"q": location, "format": "json", "accept-language": "en"},
			headers={"User-Agent": USER_AGENT}
		)
		resp.raise_for_status()
		return resp.json()

	except requests.HTTPError as e:
		if e.response.status_code == 429 and retries < 5: # ty: ignore[unresolved-attribute]
			return geocode(location, retries=retries + 1)

	except json.JSONDecodeError:
		pass

	return []

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float):
	"""
	Calculates the true great-circle distance between two points on Earth in kilometres.
	Remains accurate to approximately 0.5km, due to difference between polar and equatorial radius of the Earth.
	"""
	EARTH_RADIUS = 6371
	lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

	dlat = lat2 - lat1
	dlon = lon2 - lon1
	a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
	c = 2 * math.asin(math.sqrt(a))

	return EARTH_RADIUS * c

def choose_airport(lat: float, lon: float):
	"""
	Locate the three closest medium or large airports and prompt the user to make a decision
	out of the three, presenting necessary data to aid the user's decision in the process.
	"""
	options = sorted(
		[a for a in airports if a.get("type") in ("medium_airport", "large_airport") and a.get("scheduled_service") == "yes" and a.get("name")],
		key=lambda n: haversine_distance(lat, lon, float(n["latitude_deg"]), float(n["longitude_deg"]))
	)[:3]
	return options[int(ask_user(random_traverse("messages.airports").format("\n".join([
		f" {options.index(a) + 1}. {a["name"]} ({a["type"].replace("_", " ").title()})"
		for a in options
	])), [str(n) for n in range(1, 4)])) - 1]

print("=" * 49)
print(" " * 11 + "TRAVEL COST CALCULATOR!!!!!")
print("=" * 49)
print()

if not AIRPORTS.exists():
	print(random_traverse("messages.download"))

	try:
		with requests.get("https://raw.githubusercontent.com/davidmegginson/ourairports-data/refs/heads/main/airports.csv", stream=True) as r:
			r.raise_for_status()
			with open(AIRPORTS, "wb") as f:
				for chunk in r.iter_content(chunk_size=8192):
					f.write(chunk)
	except:
		print(random_traverse("errors.download"))

	print()

with open(AIRPORTS, newline="", encoding="utf-8") as f:
	airports = list(csv.DictReader(f))

if ask_user(random_traverse("messages.hi"), ["y", "n"]).lower() == "n":
	print(random_traverse("messages.bye"))
	sys.exit()

print(random_traverse("messages.people.opener"))
people = {}
for n in ["adults", "infants", "children"]:
	while True:
		try:
			people[n] = int(ask_user(random_traverse(f"messages.people.{n}")))
			if people[n] < 0:
				raise ValueError
			break
		except ValueError:
			pass

print(random_traverse("messages.destination.opener"))
if ask_user(random_traverse("messages.destination.plane"), ["y", "n"]).lower() == "y":
	locations = geocode(ask_user(random_traverse("messages.destination.location")))
	while True:
		if locations:
			if ask_user(random_traverse("messages.confirm").format(locations[0]["display_name"]), ["y", "n"]) == "y":
				break
		else:
			print(random_traverse("errors.geocode"))

		locations = geocode(ask_user(random_traverse("messages.destination.location")))

	location = locations[0]
	destination = choose_airport(float(location["lat"]), float(location["lon"]))

	locations = geocode(ask_user(random_traverse("messages.origin")))
	while True:
		if locations:
			if ask_user(random_traverse("messages.confirm").format(locations[0]["display_name"]), ["y", "n"]) == "y":
				break
		else:
			print(random_traverse("errors.geocode"))

		locations = geocode(ask_user(random_traverse("messages.destination.location")))

	location = locations[0]
	origin = choose_airport(float(location["lat"]), float(location["lon"]))

	date = ask_user(random_traverse("messages.destination.time"))

	# fast_flights.create_query(
	# 	flights=[fast_flights.FlightQuery(
	# 		date=date,
	# 		from_airport=departure,
	# 		to_airport=destination
	# 	)]
	# )
