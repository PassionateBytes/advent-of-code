import re
import polars as pl
import tempfile

INPUT = "input/day-6.txt"

tmp_file = tempfile.NamedTemporaryFile()


def main():
    with open(INPUT, "r") as f:
        input = f.read()
    input = re.sub(r"[^\S\n]+", " ", input)
    input = re.sub(r"\s*\n\s*", "\n", input)
    input = input.strip()
    with open(tmp_file.name, "w") as f:
        f.write(input)

    df = pl.read_csv(tmp_file.name, has_header=False, separator=" ")
    df = df.transpose()

    operator_col = df.columns[-1]
    value_cols = df.columns[:-1]

    df = df.with_columns([pl.col(col).cast(pl.Int64) for col in value_cols])

    query = df.with_columns(
        pl.when(pl.col(operator_col) == "+")
        .then(pl.fold(pl.lit(0), lambda acc, x: acc + x, exprs=pl.col(value_cols)))
        .otherwise(
            pl.fold(
                pl.lit(1).cast(pl.Int64),
                lambda acc, x: acc * x,
                exprs=pl.col(value_cols),
            )
        )
        .cast(pl.Int64)
        .alias("result")
    )

    print(query["result"].sum())


if __name__ == "__main__":
    main()
