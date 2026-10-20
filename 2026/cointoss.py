import random

flips = int(input("How many times do you want to flip the coina??????? "))
results = []

for _ in range(flips):
	results.append(random.choice((0, 1)))

print(f"total: {len(results)}, heads: {len([f for f in results if f == 0])}, tails: {len([f for f in results if f == 1])}")
