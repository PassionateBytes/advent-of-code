INPUT = "input/day-3.txt"


class DigitFound(Exception):
    pass


sum = 0

with open(INPUT, "r") as f:
    input = f.read()

for bank in input.strip().split("\n"):
    digits = []

    # find first digit...
    try:
        for search in range(9, 0, -1):
            for idx_1, digit_1 in enumerate(bank[:-1]):
                if int(digit_1) == search:
                    digits.append(int(digit_1))
                    print(bank[:idx_1], end="")
                    print(f"\033[92m{digit_1}\033[0m", end="")
                    raise DigitFound
    except DigitFound:
        pass

    # find second digit...
    try:
        for search in range(9, 0, -1):
            for idx_2, digit_2 in enumerate(bank[idx_1 + 1 :], start=idx_1 + 1):
                if int(digit_2) == search:
                    digits.append(int(digit_2))
                    print(bank[idx_1 + 1 : idx_2], end="")
                    print(f"\033[92m{digit_2}\033[0m", end="")
                    raise DigitFound
    except DigitFound:
        pass

    print(bank[idx_2 + 1 :], end="")

    number = int("".join([str(digit) for digit in digits]))
    print(f" -> {number}")

    sum += number

print(f"Sum of all matching numbers: {sum}")
