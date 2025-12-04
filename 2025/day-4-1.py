from typing import Literal

INPUT = "input/day-4.txt"

ITEM = "@"
FREE = "."
type Element = Literal["@", "."]


def main():
    with open(INPUT, "r") as f:
        input = f.read()

    accessible_items = 0

    grid: list[list[Element]] = [
        [col for col in row.strip()] for row in input.strip().split("\n")
    ]
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        for x in range(width):
            element = grid[y][x]
            if element == ITEM:
                neighboring_items = count_neighboring_items(grid, x, y)
                accessible_items += neighboring_items < 4
                print(neighboring_items, end="")
            else:
                print(FREE, end="")
        print()

    print(f"\nAccessible items: {accessible_items}")


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
