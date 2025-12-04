INPUT = "input/day-2.txt"

sum = 0

with open(INPUT, "r") as f:
    input = f.read()

ranges = [[int(num) for num in range.split("-")] for range in input.strip().split(",")]

for start, end in ranges:
    for num in range(start, end + 1):
        strnum = str(num)
        length = len(strnum)
        number_of_patterns = 2
        while number_of_patterns <= length:
            if length % number_of_patterns == 0:
                pattern_length = length // number_of_patterns
                if all(
                    strnum[i * pattern_length : (i + 1) * pattern_length] == strnum[0 : pattern_length]
                    for i in range(number_of_patterns)
                ):
                    sum += num
                    break
            number_of_patterns += 1

print(f"Sum of all matching numbers: {sum}")
