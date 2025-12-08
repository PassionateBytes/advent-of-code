INPUT = "input/day-7.txt"

SOURCE = "S"
BEAM = "|"
SPLITTER = "^"


def main():
    with open(INPUT, "r") as f:
        input = f.read()

    split_count = 0

    lines = input.splitlines()
    previous = lines.pop(0)
    while lines:
        beam_idxs = set(
            (i for i, char in enumerate(previous) if char in {BEAM, SOURCE})
        )
        current = lines.pop(0)
        splitter_idxss = set((i for i, char in enumerate(current) if char == SPLITTER))

        split_count += len(beam_idxs & splitter_idxss)

        beam_idxs = beam_idxs - splitter_idxss
        beam_idxs.update({s - 1 for s in splitter_idxss if s - 1 >= 0})
        beam_idxs.update({s + 1 for s in splitter_idxss if s + 1 < len(current)})

        current = "".join(
            BEAM if i in beam_idxs else char for i, char in enumerate(current)
        )
        print(current)

        previous = current

    print(f"Split count: {split_count}")


if __name__ == "__main__":
    main()
