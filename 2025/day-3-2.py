INPUT = "input/day-3.txt"


def list_get(a, x, default=-1):
    try:
        return a[x]
    except IndexError:
        return default


class DigitFound(Exception):
    pass


sum = 0

with open(INPUT, "r") as f:
    input = f.read()

for bank in input.strip().split("\n"):
    digits = list()
    digit_indexes = list()

    for digit_no in range(12, 0, -1):
        try:
            for search in range(9, 0, -1):
                start_idx = list_get(digit_indexes, -1, -1) + 1
                stop_idx = len(bank) - digit_no + 1
                for idx, digit in enumerate(bank[start_idx:stop_idx], start=start_idx):
                    if int(digit) == search:
                        raise DigitFound
        except DigitFound:
            digits.append(int(digit))
            digit_indexes.append(idx)
            print(bank[start_idx:idx], end="")
            print(f"\033[92m{digit}\033[0m", end="")

    print(bank[list_get(digit_indexes, -1, -1) + 1 :], end="")

    number = int("".join([str(digit) for digit in digits]))
    print(f" -> {number}")

    sum += number

print(f"Sum of all matching numbers: {sum}")
