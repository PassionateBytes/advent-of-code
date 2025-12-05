from typing import Generator, Literal
import polars as pl

INPUT = "input/day-5.txt"


def main():
    with open(INPUT, "r") as f:
        input = f.read()

    fresh_ingredient_ranges_s, ingredient_inventory_s = input.strip().split("\n" * 2)
    fresh_ingredients = load_fresh_ingredients(fresh_ingredient_ranges_s)
    ingredient_inventory = load_ingredient_inventory(ingredient_inventory_s)

    lf_inventory = pl.DataFrame(
        ingredient_inventory,
        schema={"ingredient": pl.Int128},
    ).lazy()
    lf_fresh = pl.DataFrame(
        fresh_ingredients,
        schema={"start": pl.Int128, "end": pl.Int128},
    ).lazy()

    query = lf_inventory.join_where(
        lf_fresh,
        pl.col("ingredient") >= pl.col("start"),
        pl.col("ingredient") <= pl.col("end")
    ).select(pl.n_unique("ingredient"))

    result = query.collect().item()
    print("Number of fresh ingredients:", result)


def load_fresh_ingredients(
    ingredient_ranges: str,
) -> Generator[dict[Literal["start", "end"], int], None, None]:
    for ingredient_range in ingredient_ranges.strip().splitlines():
        start, end = ingredient_range.strip().split("-")
        yield {"start": start, "end": end}


def load_ingredient_inventory(
    ingredients: str,
) -> Generator[dict[Literal["ingredient"], int], None, None]:
    for ingredient in ingredients.strip().splitlines():
        yield {"ingredient": int(ingredient)}


if __name__ == "__main__":
    main()
