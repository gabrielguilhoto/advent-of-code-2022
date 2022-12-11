import collections
import re
import typing


class Movement(typing.TypedDict):
    count: int
    origin: int
    destination: int


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> str:
        crate_stacks, movements = self.process_input(raw_input)

        for movement in movements:
            for _ in range(movement["count"]):
                crate_to_move = crate_stacks[movement["origin"]].pop()
                crate_stacks[movement["destination"]].append(crate_to_move)

        crates_on_top = ""
        for i in range(len(crate_stacks)):
            crates_on_top += crate_stacks[i][-1]

        return crates_on_top

    def solve_part_2(self, raw_input: list[str]):
        crate_stacks, movements = self.process_input(raw_input)

        for movement in movements:
            crates_to_move = reversed(
                [
                    crate_stacks[movement["origin"]].pop()
                    for _ in range(movement["count"])
                ]
            )
            crate_stacks[movement["destination"]].extend(crates_to_move)

        crates_on_top = ""
        for i in range(len(crate_stacks)):
            crates_on_top += crate_stacks[i][-1]

        return crates_on_top

    def process_input(
        self, raw_input: list[str]
    ) -> tuple[dict[int, list[str]], list[Movement]]:
        crate_stacks: typing.DefaultDict[int, list[str]] = collections.defaultdict(list)
        movements: list[Movement] = []

        row_index = 0
        while not re.search(r"^\s\d", raw_input[row_index]):
            for column_index, char in enumerate(raw_input[row_index]):
                if char.isalpha():
                    stack_index = column_index // 4
                    crate_stacks[stack_index].append(char)
            row_index += 1

        for stack in crate_stacks.values():
            stack.reverse()

        row_index += 2
        while row_index < len(raw_input):
            match = re.search(r"move (\d+) from (\d+) to (\d+)", raw_input[row_index])
            if match:
                match_groups = match.groups()
                movements.append(
                    {
                        "count": int(match_groups[0]),
                        "origin": int(match_groups[1]) - 1,
                        "destination": int(match_groups[2]) - 1,
                    }
                )
            row_index += 1

        return crate_stacks, movements
