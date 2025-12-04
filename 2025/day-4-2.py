from typing import Literal

INPUT = "input/day-4.txt"

ITEM = "@"
FREE = "."
REMOVED = "x"
type Element = Literal["@", ".", "x"]


def main() -> None:
    with open(INPUT, "r") as f:
        input = f.read()

    total_removed = 0

    grid: list[list[Element]] = [
        [col for col in row.strip()] for row in input.strip().split("\n")
    ]
    height = len(grid)
    width = len(grid[0])

    batch_removed: int | None = None
    while batch_removed is None or batch_removed > 0:
        batch_removed = 0

        for y in range(height):
            for x in range(width):
                element = grid[y][x]

                if element == ITEM:
                    neighboring_items = count_neighboring_items(grid, x, y)
                    if neighboring_items < 4:
                        grid[y][x] = REMOVED
                        batch_removed += 1
                        print(REMOVED, end="")
                    else:
                        print(ITEM, end="")
                else:
                    print(FREE, end="")
            print()

        total_removed += batch_removed
        print(f"\nBatch Removed: {batch_removed}\n\n{'=' * width}\n")

    print(f"\nTotal Removed: {total_removed}")


def count_neighboring_items(grid: list[list[Element]], x, y) -> int:
    count = 0
    height = len(grid)
    width = len(grid[0])

    for y_offset in (-1, 0, 1):
        for x_offset in (-1, 0, 1):
            if x_offset == 0 and y_offset == 0:
                continue
            if not 0 <= x + x_offset < width:
                continue
            if not 0 <= y + y_offset < height:
                continue
            element = grid[y + y_offset][x + x_offset]
            count += element == ITEM

    return count


if __name__ == "__main__":
    main()
