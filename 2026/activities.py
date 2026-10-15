activities = input("Do you prefer creative activities or practical activities? ").lower()
if activities == "creative":
	working = input("Do you enjoy working with others or working alone? ").lower()
	if working == "working with others":
		print("You should join Musical Theatre Club!")
	elif working == "working alone":
		print("You should join Creative Writing Club!")
elif activities == "practical":
	problems = input("Do you like solving problems or building things? ").lower()
	if problems == "solving problems":
		print("You should join Robotics Club!")
	elif problems == "building things":
		print("You should join Woodworking Club!")
