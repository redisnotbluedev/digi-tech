"""
Scenario 4: Birthday Gift Predictor
User input:
-> A category chosen by the user (e.g., “sporty”, “artistic”, “tech”, “relaxing”)
Program output:
-> A random gift suggestion that matches the category

Category
Possible Gifts

sporty
-> basketball, water bottle, sports bag, gym gloves
artistic
-> sketchbook, markers, paint kit, calligraphy pens
tech
-> headphone,Switch, Bluetooth speaker, mouse
relaxing
-> candle set, plush toy, puzzle book, tea bags
"""
import random

hobby = input("What's their hobby?").lower()
match hobby:
	case "sporty":
		options
