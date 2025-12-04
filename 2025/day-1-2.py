import re

INPUT = "input/day-1-1.txt"

position = 50
dial_size = 100
zero_hits = 0

with open(INPUT, "r") as f:
    input = f.read()

translator = str.maketrans(
    {
        "R": "",  # +
        "L": "-",
    }
)

input = input.translate(translator)
input = re.sub(r"\n\s*\n", "\n", input).strip()

for line in input.splitlines():
    move = int(line)
    click = -1 if move < 0 else 1
    for _ in range(abs(move)):
        position = (position + click) % dial_size
        zero_hits += position == 0

print(f"Number of times dial hit zero: {zero_hits}")

