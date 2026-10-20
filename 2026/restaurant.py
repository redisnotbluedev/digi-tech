import random

fullness = 0
while fullness < 100:
	fullness += random.randint(10, 20)
	order = input("What would you like to order? ")
	print(f"You ordered: {order}. You're {fullness} full.")
print("You're full.")
