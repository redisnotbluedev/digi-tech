"""
### Travel Cost Calculator

A calculator. For travel cost... Yeah.
"""

def ask_user(prompt, options):
	response = input(prompt)
	while response not in options:
		print("Invalid input, please try again.")
		response = input(prompt)
	return response
