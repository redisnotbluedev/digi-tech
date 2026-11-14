"""
### Travel Cost Calculator

A calculator. For travel cost... Yeah.
"""

import csv
import datetime
import json
import math
import pathlib
import random
import sys
import time

import fast_flights
from fast_flights.model import Flights
import requests

TEXT_OPTIONS = {
	"messages": {
		"download": ["Downloading data..."],
		"hi": ["Welcome to the Travel Cost Calculator! Would you like to plan your trip?"],
		"bye": ["Goodbye.", "See you.", "Farewell!", "Have a nice day.", "Maybe next time."],
		"flight": {
			"people": {
				"opener": ["Let's start with the people going on your trip."],
				"adults": ["How many adults?"],
				"children": ["How many children?"],
				"infants_in_seat": ["How many infants (in-seat)?"],
				"infants_on_lap": ["How many infants (in-lap)?"]
			},
			"seat": ["Which cabin class would you like to fly in?"],
			"bags": ["How many carry-on bags?"],
			"checked": ["How many checked-in bags?"]
		},
		"destination": {
			"opener": ["Now, the destination."],
			"plane": ["Do you plan on taking a plane to your destination?"],
			"location": ["Where would you like to travel to? The more specific, the better."],
		},
		"leave": ["What is your departure date?"],
		"return": ["What is your return date?"],
		"confirm": ["Did you mean {}?"],
		"airports": ["Closest airports:\n{}\nWhich airport would you like to choose?"],
		"origin": ["Where are you leaving from?"]
	},
	"errors": {
		"download": ["Sorry, an error occured while downloading data."],
		"geocode": ["Sorry, something went wrong understanding your location, please try again."],
		"people": ["Sorry, only booking for up to ten passengers is supported."],
		"infants": ["There must be at least as many adults as infants on laps."],
		"flights": ["Sorry, we couldn't find any flights for your constraints. Please try again later."]
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

def geocode(location: str, retries: int = 0) -> list[dict]:
	"""
	Find an OpenStreetMap object based on a location string, based on the free Nominatim service.
	"""
	global last_nominatim

	elapsed = time.monotonic() - last_nominatim
	buffer = 1.1 + (2**retries if retries > 0 else 0)
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

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
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

def choose_airport(lat: float, lon: float) -> dict:
	"""
	Locate the three closest medium or large airports and prompt the user to make a decision
	out of the three, presenting necessary data to aid the user's decision in the process.
	"""
	options = sorted(
		[
			a | {"distance": haversine_distance(lat, lon, float(a["latitude_deg"]), float(a["longitude_deg"]))}
			for a in airports if a.get("type") in ("medium_airport", "large_airport") and a.get("scheduled_service") == "yes" and a.get("name") and a.get("iata_code")
		],
		key=lambda a: a["distance"]
	)[:3]
	if options[0]["distance"] <= 1: # ty: ignore[unsupported-operator]
		return options[0]
	return options[int(ask_user(random_traverse("messages.airports").format("\n".join([
		f" {options.index(a) + 1}. {a["name"]} ({a["iata_code"]} - {a["type"].replace("_", " ").title()})" # ty: ignore[unresolved-attribute]
		for a in options
	])), [str(n) for n in range(1, 4)])) - 1]

def parse_date(date: str) -> str | None:
	"""Robustly parse a date and convert it into YYYY-MM-DD format."""
	sep = ["/", ".", "-", " "]
	dt = None
	for s in sep:
		try:
			dt = datetime.datetime.strptime(date, f"%Y{s}%m{s}%d")
			break
		except ValueError:
			pass

	if dt:
		return datetime.datetime.strftime(dt, "%Y-%m-%d")
	return None

def serialise_flight(flight: Flights):
	"""Convert a Flights object into a string."""
	t = lambda x: f"{x.time[0]}:{x.time[1]:02d}"
	data = []
	data.append(f"${flight.price} USD • {flight.carbon.emission // 1000}kg carbon emission • {sum([s.duration for s in flight.flights]) / len(flight.flights):.2f} mins average flight")
	for f in flight.flights:
		single = []
		single.append("/".join([str(n) for n in f.departure.date]))
		single.append(t(f.departure))
		single.append(f"{f.from_airport.code} → {f.to_airport.code}")
		single.append("/".join([str(n) for n in f.arrival.date]))
		single.append(t(f.arrival))
		data.append("    " + " ".join(single))
	return "\n".join(data)

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

print(random_traverse("messages.flight.people.opener"))
while True:
	people = {}
	total = 0
	for n in ["adults", "infants_in_seat", "infants_on_lap", "children"]:
		while True:
			try:
				people[n] = int(ask_user(random_traverse(f"messages.flight.people.{n}")))
				if people[n] < 0:
					raise ValueError
				total += people[n]
				break
			except ValueError:
				pass

	if sum(people.values()) > 9:
		print(random_traverse("errors.people"))
		continue

	if people["infants_in_seat"] > people["adults"]:
		print(random_traverse("errors.infants"))
		continue

	break

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

		locations = geocode(ask_user(random_traverse("messages.origin")))

	location = locations[0]
	origin = choose_airport(float(location["lat"]), float(location["lon"]))

	while True:
		go = parse_date(ask_user(random_traverse("messages.leave")))
		if go is not None:
			break

	while True:
		back = parse_date(ask_user(random_traverse("messages.return")))
		if back is not None:
			break

	while True:
		try:
			bags = int(ask_user(random_traverse("messages.flight.bags")))
			break
		except ValueError:
			pass

	while True:
		try:
			checked = int(ask_user(random_traverse("messages.flight.checked")))
			break
		except ValueError:
			pass

	seat = ask_user(random_traverse("messages.flight.seat"), ["economy", "premium", "business"]).replace("premium", "premium-economy")
	query = fast_flights.create_query(
		flights=[
			fast_flights.FlightQuery(
				date=go,
				from_airport=origin["iata_code"],
				to_airport=destination["iata_code"]
			),
			fast_flights.FlightQuery(
				date=back,
				from_airport=destination["iata_code"],
				to_airport=origin["iata_code"]
			)
		],
		seat=seat, # ty: ignore[invalid-argument-type]
		trip="round-trip",
		passengers=fast_flights.Passengers(**people),
		carry_on_bags=bags,
		checked_bags=checked
	)

	for n in range(1, 3):
		try:
			data = fast_flights.get_flights(query)
			break
		except Exception:
			time.sleep(2**n)
	else:
		print(random_traverse("errors.flights"))
		sys.exit()

	flights = []
	for f in data:
		id = "|".join([str(f.price), str(f.carbon.emission), str(sum([s.duration for s in f.flights]) / len(f.flights))])
		if id not in flights:
			print(serialise_flight(f))
			flights.append(id)
