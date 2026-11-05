type = input("What kind of pizza do you want to order? ")
size = input("What size of pizza do you want to order? ")
topping = input("Choose one add-on topping: Ham, Cheese, Bacon, Pineapple or None: ")

if size.lower() == "small":
	price = 8.5
elif size.lower() == "medium":
	price = 12.0
else:
	price = 15.5

if topping.lower() == "ham":
	price = price + 2.5
elif topping.lower() == "cheese":
	price = price + 1.5
elif topping.lower() == "bacon":
	price = price + 2.5
elif topping.lower() == "pineapple":
	price = price + 1

print(f"You bought a {size} {type} pizza, with {topping.lower()} topping, it costs ${price}")
