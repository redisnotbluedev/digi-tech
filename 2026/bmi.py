def calculate_bmi(weight, height):
	if height <= 0 or weight <= 0:
		raise ValueError("Height and weight must be greater than zero.")

	bmi = weight / (height ** 2)
	bmi = round(bmi, 2)

	if bmi < 18.5:
		category = "Underweight"
	elif 18.5 <= bmi < 25.0:
		category = "Normal weight"
	elif 25.0 <= bmi < 30.0:
		category = "Overweight"
	else:
		category = "Obese"

	return bmi, category
