INPUT = "input/day-7.txt"

SOURCE = "S"
SPLITTER = "^"


def main():
    with open(INPUT, "r") as f:
        input = f.read()
    lines = [[char for char in line] for line in input.strip().splitlines()]

    previous = lines.pop(0)
    previous = [1 if char == SOURCE else char for char in previous]

    while lines:
        current = lines.pop(0)

        for i in range(len(current)):
            if isinstance(previous[i], int):
                if current[i] == SPLITTER:
                    current[i - 1] = (
                        current[i - 1] + previous[i]
                        if isinstance(current[i - 1], int)
                        else previous[i]
                    )
                    current[i + 1] = (
                        current[i + 1] + previous[i]
                        if isinstance(current[i + 1], int)
                        else previous[i]
                    )
                else:
                    current[i] = (
                        current[i] + previous[i]
                        if isinstance(current[i], int)
                        else previous[i]
                    )

        print("".join(str(i)[-1:] for i in current))

        previous = current

    print(
        "Sum of possibilities: ",
        sum((char if isinstance(char, int) else 0 for char in previous)),
    )


if __name__ == "__main__":
    main()
