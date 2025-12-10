import polars as pl
from dataclasses import dataclass
from typing import Generator
import time

INPUT = "input/day-9.txt"


@dataclass(frozen=True, slots=True)
class Node:
    x: int
    y: int

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return self.__str__()

    def in_polygon(self, polygon: list["Edge"]) -> bool:
        ray_cast_collisions = 0
        for segment in polygon:
            if segment.contains(self):
                break
            ray_cast_collisions += self.ray_cast(segment)
        else:
            return ray_cast_collisions % 2 != 0
        return True

    def ray_cast(self, segment: "Edge") -> bool:
        if segment.is_horizontal:
            return False
        if segment.p0.x < self.x:
            return False
        upper_y = max(segment.p0.y, segment.p1.y)
        lower_y = min(segment.p0.y, segment.p1.y)
        return lower_y < self.y <= upper_y


@dataclass(frozen=True, slots=True)
class Edge:
    p0: Node
    p1: Node

    def __str__(self):
        return f"{self.p0}-{self.p1}"

    def __repr__(self):
        return self.__str__()

    @property
    def is_horizontal(self) -> bool:
        return self.p0.y == self.p1.y

    @property
    def points(self) -> Generator[Node, None, None]:
        if self.is_horizontal:
            x_upper = max(self.p0.x, self.p1.x)
            x_lower = min(self.p0.x, self.p1.x)
            return (Node(x, self.p0.y) for x in range(x_lower, x_upper))
        else:
            y_upper = max(self.p0.y, self.p1.y)
            y_lower = min(self.p0.y, self.p1.y)
            return (Node(self.p0.x, y) for y in range(y_lower, y_upper))

    def contains(self, point: Node) -> bool:
        if self.is_horizontal:
            x_upper = max(self.p0.x, self.p1.x)
            x_lower = min(self.p0.x, self.p1.x)
            return point.y == self.p0.y and x_lower <= point.x <= x_upper
        else:
            y_upper = max(self.p0.y, self.p1.y)
            y_lower = min(self.p0.y, self.p1.y)
            return point.x == self.p0.x and y_lower <= point.y <= y_upper


@dataclass(frozen=True, slots=True)
class Rectangle:
    a: Edge
    b: Edge
    c: Edge
    d: Edge
    area: int

    def __str__(self):
        return f"<{self.a.p0}..{self.area}..{self.c.p0}>"

    def __repr__(self):
        return self.__str__()

    def contained_in_polygon(self, polygon: list[Edge]) -> bool:
        return all(
            point.in_polygon(polygon)
            for edge in (self.a, self.b, self.c, self.d)
            for point in edge.points
        )


def main():
    input_lf = pl.scan_csv(
        INPUT, has_header=False, schema={"x": pl.Int64, "y": pl.Int64}
    ).with_row_index("node_id")

    rectangles = get_rectangles(input_lf)
    polygon = get_polygon(input_lf)

    start = time.monotonic()
    for i, rectangle in enumerate(rectangles):
        now = time.monotonic()
        elapsed = now - start
        remaining = (len(rectangles) - i) * elapsed / (i + 1)
        print(f" {i}/{len(rectangles)} | {100 * i / len(rectangles):.2f}% | {int(elapsed//60):02d}:{int(elapsed%60):02d} elapsed | {int(remaining//60):02d}:{int(remaining%60):02d} remaining", end="\r")

        if rectangle.contained_in_polygon(polygon):
            break

    print(f"Largest rectangle fully inside the polygon: {rectangle}")


def get_rectangles(input_lf: pl.LazyFrame) -> list[Rectangle]:
    rectangles_lf = (
        input_lf.join(input_lf, how="cross", suffix="_1")
        .filter(pl.col("node_id") < pl.col("node_id_1"))
        .select(
            pl.col("x").alias("x_0"),
            pl.col("y").alias("y_0"),
            pl.col("x_1"),
            pl.col("y_1"),
        )
        .with_columns(
            area=((pl.col("x_1") - pl.col("x_0")).abs() + 1)
            * ((pl.col("y_1") - pl.col("y_0")).abs() + 1)
        )
        .sort(pl.col("area"), descending=True)
    )
    rectangles_df = rectangles_lf.collect()

    rectangles = [None] * rectangles_df.height
    for i, r in enumerate(rectangles_df.iter_rows(named=True)):
        rectangles[i] = Rectangle(
            Edge(
                Node(r["x_0"], r["y_0"]),
                Node(r["x_0"], r["y_1"]),
            ),
            Edge(
                Node(r["x_0"], r["y_1"]),
                Node(r["x_1"], r["y_1"]),
            ),
            Edge(
                Node(r["x_1"], r["y_1"]),
                Node(r["x_1"], r["y_0"]),
            ),
            Edge(
                Node(r["x_1"], r["y_0"]),
                Node(r["x_0"], r["y_0"]),
            ),
            r["area"],
        )

    return rectangles


def get_polygon(input_lf: pl.LazyFrame) -> list[Edge]:
    polygon_lf = (
        input_lf.select(pl.col("x").alias("x_0"), pl.col("y").alias("y_0"))
        .with_columns(
            x_1=pl.col("x_0").shift(-1),
            y_1=pl.col("y_0").shift(-1),
        )
        .with_columns(
            x_1=pl.when(pl.col("x_1").is_null())
            .then(pl.col("x_0").first())
            .otherwise(pl.col("x_1")),
            y_1=pl.when(pl.col("y_1").is_null())
            .then(pl.col("y_0").first())
            .otherwise(pl.col("y_1")),
        )
    )
    polygon_df = polygon_lf.collect()

    poly_segments = [None] * polygon_df.height
    for i, p in enumerate(polygon_df.iter_rows(named=True)):
        poly_segments[i] = Edge(
            Node(p["x_0"], p["y_0"]),
            Node(p["x_1"], p["y_1"]),
        )

    return poly_segments


if __name__ == "__main__":
    main()
