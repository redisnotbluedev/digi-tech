"""
### Travel Cost Calculator

A calculator. For travel cost... Yeah.
"""

import random, sys

TEXT_OPTIONS = {
	"messages": {
		"hi": ["Welcome to the Travel Cost Calculator! Would you like to plan your trip?"],
		"bye": ["Goodbye.", "See you.", "Farewell!", "Have a nice day.", "Maybe next time."],
		"destination": {
			"opener": ["Let's start with destination."],
			"interstate": ["Would you like to go overseas?"]
		}
	}
}

def ask_user(prompt, options):
	options = options.lower()
	ask = lambda: input(prompt + f" [{"/".join(options)}]{"" if prompt.endswith("?") or prompt.endswith(":") else ":"} ")
	response = ask()
	while response.lower() not in options and options != []:
		print("Invalid input, please try again.")
		response = ask()
	return response

def random_traverse(key):
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

print("=" * 49)
print(" " * 11 + "TRAVEL COST CALCULATOR!!!!!")
print("=" * 49)
print()
if ask_user(random_traverse("messages.hi"), ["y", "n"]) == "n":
	print(random_traverse("messages.bye"))
	sys.exit()

print(random_traverse("messages.destination.opener"))
