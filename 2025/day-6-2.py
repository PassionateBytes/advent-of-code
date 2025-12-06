import re
import functools


INPUT = "input/day-6.txt"


def main():
    with open(INPUT, "r") as f:
        input = f.read()

    # read data
    data = []
    for line in input.splitlines():
        data.append(line)

    # rotate table 90 degrees CCW
    data = list(zip(*data))[::-1]

    results = []
    section_numbers = []
    for row in data:
        cleaned_row = "".join(row).replace(" ", "")
        match = re.match(r"(\d+)(.)?", cleaned_row)
        if match is None:
            continue
        number, operator = match.groups()

        section_numbers.append(int(number))

        if operator:
            if operator == "+":
                result = sum(section_numbers)
            elif operator == "*":
                result = functools.reduce(lambda agg, x: agg * x, section_numbers, 1)
            results.append(result)
            section_numbers.clear()

    print(sum(results))


if __name__ == "__main__":
    main()
