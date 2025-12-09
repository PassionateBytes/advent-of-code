import polars as pl

INPUT = "input/day-9.txt"


def main():
    # load data and add node_id
    input_lf = pl.scan_csv(
        INPUT, has_header=False, schema={"x": pl.Int64, "y": pl.Int64}
    ).with_row_index("node_id")

    # cross-combine uniquely
    combinations_lf = input_lf.join(input_lf, how="cross", suffix="_2").filter(
        pl.col("node_id") < pl.col("node_id_2")
    )

    # validate expected length
    input_count = input_lf.select(pl.len()).collect().item()
    combinations_count = combinations_lf.select(pl.len()).collect().item()
    assert combinations_count == input_count * (input_count - 1) / 2

    # calculate areas
    area_lf = combinations_lf.with_columns(
        area=((pl.col("x_2") - pl.col("x")).abs() + 1)
        * ((pl.col("y_2") - pl.col("y")).abs() + 1)
    )

    # find largest area
    result = (
        area_lf.sort(pl.col("area"), descending=True)
        .limit(1)
        .select(pl.col("area"))
        .collect()
        .item()
    )
    print(result)


if __name__ == "__main__":
    main()
