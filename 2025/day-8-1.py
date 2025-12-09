import polars as pl
from collections import defaultdict, deque

INPUT = "input/day-8.txt"


def main():
    # load data and add node_id
    input_lf = pl.scan_csv(
        INPUT, has_header=False, schema={"x": pl.Int64, "y": pl.Int64, "z": pl.Int64}
    ).with_row_index("node_id")

    # cross-combine uniquely
    combinations_lf = input_lf.join(input_lf, how="cross", suffix="_2").filter(
        pl.col("node_id") < pl.col("node_id_2")
    )

    # validate expected length
    input_count = input_lf.select(pl.len()).collect().item()
    combinations_count = combinations_lf.select(pl.len()).collect().item()
    assert combinations_count == input_count * (input_count - 1) / 2

    # calculate distances, then sort and limit
    distances_lf = (
        combinations_lf.with_columns(
            distance=(
                (pl.col("x_2") - pl.col("x")).pow(2)
                + (pl.col("y_2") - pl.col("y")).pow(2)
                + (pl.col("z_2") - pl.col("z")).pow(2)
            ).sqrt()
        )
        .sort(pl.col("distance"))
        .limit(1000)
    )

    results = distances_lf.collect()

    # create graph of adjacent nodes
    graph: dict[list[int]] = defaultdict(list)
    for row in results.iter_rows(named=True):
        node_a = row["node_id"]
        node_b = row["node_id_2"]
        graph[node_a].append(node_b)
        graph[node_b].append(node_a)

    # collect circuits
    visited_nodes = set()
    circuits: list[set[int]] = []

    for root_node in graph:
        if root_node in visited_nodes:
            continue

        circuit = set()
        queue = deque([root_node])

        while queue:
            node = queue.popleft()
            circuit.add(node)
            visited_nodes.add(node)

            for neighbor in graph[node]:
                if neighbor in visited_nodes:
                    continue
                queue.append(neighbor)

        circuits.append(circuit)

    # sort largest circuit first
    circuits.sort(key=lambda x: len(x), reverse=True)

    # puzzle solution
    print(len(circuits[0]) * len(circuits[1]) * len(circuits[2]))


if __name__ == "__main__":
    main()
