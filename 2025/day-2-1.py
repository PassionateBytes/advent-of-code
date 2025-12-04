INPUT = "input/day-2.txt"

sum = 0

with open(INPUT, "r") as f:
    input = f.read()

ranges = [[int(num) for num in range.split("-")] for range in input.strip().split(",")]

for start, end in ranges:
    for num in range(start, end + 1):
        strnum = str(num)
        length = len(strnum)
        if length % 2 == 0:
            if strnum[: length // 2] == strnum[length // 2 :]:
                sum += num
                print(f"Matching number found: {num}")

print(f"Sum of all matching numbers: {sum}")