import hashlib

def isnumber(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def process_answer(answer):
	factor = float(answer) if isnumber(answer) else len(answer)
	md5 = hashlib.md5(answer.encode("utf-8")).hexdigest()
	sha1 = hashlib.sha1(answer.encode("utf-8")).hexdigest()
	capitals = str(len([l for l in answer if l in "QWERTYUIOPASDFGHJKLZXCVBNM"]))
	numbers = str(sum([int(l) for l in answer if l.isnumeric()]))
	return int(hashlib.sha256(f"{md5}|{sha1}|{capitals}|{numbers}".encode("utf-8")).hexdigest(), 16) / (1 if factor == 0 else factor)

def pick_number(factors):
	numbers = []
	for f in factors:
		numbers.append(str(process_answer(input(f"What's your {f.lower()}? "))))
	return int(hashlib.sha256(str("|".join(numbers)).encode("utf-8")).hexdigest(), 16) % 1000

print(pick_number([
	"name",
	"favourite colour",
	"favourite number",
	"birth month",
	"birth year",
	"mother's maiden name",
	"weight",
	"height",
	"last 4 digits on your credit card",
	"least favourite turkey species",
	"age",
	"hours since last sleep",
	"relation to george farnsworth",
	"bank account number",
	"favourite animal"
]))
