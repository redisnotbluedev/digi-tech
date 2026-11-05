password = "2314"
guess = input("What is the four digi passowrd? ")
attempts = 1

while attempts < 3:
	if guess == password:
		print("access granted!!!!!")
		attempts = 0
	else:
		print("password is incorrect")

	guess = input("What is the four digi passowrd? ")
	attempts += 1
else:
	print("access denied.")
