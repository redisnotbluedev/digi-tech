def get_rabbit_food(day):
	day = day.strip().lower()
	if day in ["saturday", "sunday"]:
		return "25 grams of pellets (plus a handful of fresh leafy greens)"
	return "30 grams of pellets"


def get_goldfish_food(day):
	day = day.strip().lower()
	if day == "sunday":
		return "0 pellets (Fasting day to keep their digestive system healthy)"
	return "3 pellets"


def get_dog_food(day):
	day = day.strip().lower()
	if day in ["saturday", "sunday"]:
		return "400 grams of kibble"
	return "350 grams of kibble"


def check_feeding_amount(pet_type, day):
	pet_type = pet_type.strip().lower()
	day = day.strip().lower()

	valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
	if day not in valid_days:
		return f"Error: \"{day}\" is not a valid day of the week."

	if pet_type == "rabbit":
		amount = get_rabbit_food(day)
	elif pet_type == "goldfish":
		amount = get_goldfish_food(day)
	elif pet_type == "dog":
		amount = get_dog_food(day)
	else:
		return f"Error: \"{pet_type}\" is not a pet in this household. Choose rabbit, goldfish, or dog."

	return f"On {day.capitalize()}, give your {pet_type} {amount}."
