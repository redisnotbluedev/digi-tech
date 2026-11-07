"""
### Travel Cost Calculator

A calculator. For travel cost... Yeah.
"""

import csv
import json
import pathlib
import random
import sys
import time

import fast_flights
import requests

TEXT_OPTIONS = {
	"messages": {
		"hi": ["Welcome to the Travel Cost Calculator! Would you like to plan your trip?"],
		"bye": ["Goodbye.", "See you.", "Farewell!", "Have a nice day.", "Maybe next time."],
		"destination": {
			"opener": ["Let's start with destination."],
			"plane": ["Do you plan on taking a plane to your destination?"],
			"location": ["Where would you like to travel to? The more specific, the better."]
		},
		"confirm": ["Did you mean {}?"]
	}
}
AIRPORTS = pathlib.Path(__file__).parent / "airports.csv"
USER_AGENT = "TravelCostCalculator/1.0"
last_nominatim = -1

def ask_user(prompt: str, options: list = [], show_options: bool = True) -> str:
	if show_options and options != []:
		if not prompt.endswith(" "):
			prompt += " "
		prompt += f"[{"/".join(options)}]"

	if not prompt.endswith(" "):
		prompt += " "

	response = input(prompt)
	while response.lower() not in [o.lower() for o in options] and options != []:
		print("Invalid input, please try again.")
		response = input(prompt)
	return response

def random_traverse(key: str):
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
	global last_nominatim

	elapsed = time.monotonic() - last_nominatim
	buffer = 1.1 + (2 ** retries if retries > 0 else 0)
	if elapsed < buffer:
		time.sleep(buffer - elapsed)
	last_nominatim = time.monotonic()

	try:
		resp = requests.get(
			"https://nominatim.openstreetmap.org/search",
			params={"q": location, "format": "json"},
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

print("=" * 49)
print(" " * 11 + "TRAVEL COST CALCULATOR!!!!!")
print("=" * 49)
print()

if not AIRPORTS.exists():
	print("Downloading data...")

	with requests.get("https://raw.githubusercontent.com/davidmegginson/ourairports-data/refs/heads/main/airports.csv", stream=True) as r:
		r.raise_for_status()
		with open(AIRPORTS, "wb") as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)

	print()

with open(AIRPORTS, newline="", encoding="utf-8") as f:
	airports = list(csv.DictReader(f))

if ask_user(random_traverse("messages.hi"), ["y", "n"]).lower() == "n":
	print(random_traverse("messages.bye"))
	sys.exit()

print(random_traverse("messages.destination.opener"))
if ask_user(random_traverse("messages.destination.plane"), ["y", "n"]).lower() == "y":
	locations = geocode(ask_user(random_traverse("messages.destination.location")))
	while True:
		if locations:
			if ask_user(random_traverse("messages.confirm").format(locations[0]["display_name"]), ["y", "n"]) == "y":
				break

		locations = geocode(ask_user(random_traverse("messages.destination.location")))
	location = locations[0]
