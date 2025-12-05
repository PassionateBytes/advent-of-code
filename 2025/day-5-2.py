"""
- each range is inclusive (i.e. range 4-8 includes #4 and #8)
- ranges may partly or fully overlap with one another
- count the number space that the ranges cover (overlaps are not to be counted multiple times!)
"""

from typing import Generator, Iterable
from dataclasses import dataclass

INPUT = "input/day-5.txt"


@dataclass(unsafe_hash=True)
class Range:
    start: int
    end: int

    def cut(self, cuts: list[int]) -> Iterable["Range"]:
        cuts = set(cuts)
        if self.end > self.start:
            cuts.remove(self.start)
        cuts = sorted(cuts)

        last_cut = None
        for cut in cuts:
            if self.start <= cut <= self.end:
                r = Range(start=last_cut or self.start, end=cut)
                yield r
                last_cut = cut
            elif last_cut is not None:
                break


def load_ranges(
    ingredient_ranges: str,
) -> Generator[Range, None, None]:
    for ingredient_range in ingredient_ranges.strip().splitlines():
        start, end = ingredient_range.strip().split("-")
        yield Range(int(start), int(end))


def main():
    with open(INPUT, "r") as f:
        input = f.read()

    ranges_str, _ = input.strip().split("\n" * 2)
    ranges_gen = load_ranges(ranges_str)
    ranges = sorted(ranges_gen, key=lambda r: r.start)

    merged_ranges = [ranges[0]]
    for r in ranges:
        prev = merged_ranges[-1]
        if r.start <= prev.end + 1:
            prev.end = max(r.end, prev.end)
        else:
            merged_ranges.append(r)

    print(sum(r.end - r.start + 1 for r in merged_ranges))


if __name__ == "__main__":
    main()
