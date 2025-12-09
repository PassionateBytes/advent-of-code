import polars as pl

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
    distances_lf = combinations_lf.with_columns(
        distance=(
            (pl.col("x_2") - pl.col("x")).pow(2)
            + (pl.col("y_2") - pl.col("y")).pow(2)
            + (pl.col("z_2") - pl.col("z")).pow(2)
        ).sqrt()
    ).sort(pl.col("distance"))

    results = distances_lf.collect()

    # initialize union-find data structure
    uf = UnionFind(input_count)

    # process pairs one by one
    for row in results.iter_rows(named=True):
        node_a = row["node_id"]
        node_b = row["node_id_2"]

        if uf.find(node_a) == uf.find(node_b):
            continue

        uf.union(node_a, node_b)

        if uf.num_components == 1:
            answer = row["x"] * row["x_2"]
            break
    
    print(answer)

class UnionFind:
    def __init__(self, n: int) -> None:
        """
        Args:
            n: Number of nodes
        """
        self.parent = list(range(n))  # Each node is its own parent initially
        self.rank = [0] * n  # Track tree depth for union by rank
        self.num_components = n  # Start with n separate components

    def find(self, x: int) -> int:
        """
        Find the root of the component containing x.

        Uses path compression to flatten the tree structure.

        Args:
            x: Node to find root for

        Returns:
            Root node of the component containing x
        """
        if self.parent[x] != x:
            # Path compression: make x point directly to root
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Unite the components containing x and y.

        Uses union by rank to keep trees shallow.

        Args:
            x: First node
            y: Second node

        Returns:
            True if x and y were in different components (union happened),
            False if they were already in the same component
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same component

        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.num_components -= 1
        return True


if __name__ == "__main__":
    main()
