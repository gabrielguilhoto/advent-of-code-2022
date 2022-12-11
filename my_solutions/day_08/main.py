import typing

Map = list[list[int]]
VisibilitySet = typing.Set[tuple[int, int]]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        map = self.get_map(raw_input)
        visibility_set: VisibilitySet = set()

        for row_index in range(len(map)):
            self.find_visible_trees_in_row(map, visibility_set, row_index, "forward")
            self.find_visible_trees_in_row(map, visibility_set, row_index, "backward")

        for col_index in range(len(map[0])):
            self.find_visible_trees_in_column(map, visibility_set, col_index, "forward")
            self.find_visible_trees_in_column(
                map, visibility_set, col_index, "backward"
            )

        return len(visibility_set)

    def solve_part_2(self, raw_input: list[str]):
        return self.find_highest_scenic_score(self.get_map(raw_input))

    def get_map(self, raw_input: list[str]) -> Map:
        return [[int(digit) for digit in row] for row in raw_input]

    def find_visible_trees_in_row(
        self,
        map: Map,
        visibility_set: VisibilitySet,
        row_index: int,
        direction: typing.Literal["forward", "backward"],
    ):
        highest_seen_height = -1
        C = len(map[row_index])
        col_indexes = range(C) if direction == "forward" else range(C - 1, -1, -1)
        for col_index in col_indexes:
            height = map[row_index][col_index]
            if height > highest_seen_height:
                highest_seen_height = height
                visibility_set.add((row_index, col_index))

    def find_visible_trees_in_column(
        self,
        map: Map,
        visibility_set: VisibilitySet,
        col_index: int,
        direction: typing.Literal["forward", "backward"],
    ):
        highest_seen_height = -1
        R = len(map)
        row_indexes = range(R) if direction == "forward" else range(R - 1, -1, -1)
        for row_index in row_indexes:
            height = map[row_index][col_index]
            if height > highest_seen_height:
                highest_seen_height = height
                visibility_set.add((row_index, col_index))

    def find_highest_scenic_score(self, map: Map) -> int:
        return max(
            self.find_scenic_score(map, row_index, col_index)
            for row_index in range(len(map))
            for col_index in range(len(map[row_index]))
        )

    def find_scenic_score(self, map: Map, row_index: int, col_index: int) -> int:
        trees_seen_left = 0
        for i in range(col_index - 1, -1, -1):
            trees_seen_left += 1
            if map[row_index][i] >= map[row_index][col_index]:
                break

        trees_seen_right = 0
        for i in range(col_index + 1, len(map[row_index])):
            trees_seen_right += 1
            if map[row_index][i] >= map[row_index][col_index]:
                break

        trees_seen_up = 0
        for i in range(row_index - 1, -1, -1):
            trees_seen_up += 1
            if map[i][col_index] >= map[row_index][col_index]:
                break

        trees_seen_down = 0
        for i in range(row_index + 1, len(map)):
            trees_seen_down += 1
            if map[i][col_index] >= map[row_index][col_index]:
                break

        return trees_seen_left * trees_seen_right * trees_seen_up * trees_seen_down
