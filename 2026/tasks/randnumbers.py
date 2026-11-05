import random

n = random.randint(1, 10) + random.randint(11, 20)
guess = int(input("What is the sum of the two numbers? "))
if guess != n:
	print("you're wrong hahahahahhAHAHHAHAHAHHAHA")
	guess = int(input("What is the sum of the two numbers? "))
print("Youre right yayayayyayayy")
