q1_ans = input("What is the capital of Australia? ").capitalize()
while q1_ans != "Canberra":
	print(f"{q1_ans} is not the capital of Australia.")
	q1_ans = input("What is the capital of Australia? ").capitalize()
print("Yes, the capital of Australia is Canberra.")
