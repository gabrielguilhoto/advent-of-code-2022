import functools


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, rucksacks: list[str]) -> int:
        return sum(
            self.get_type_priority(self.find_common_type_in_compartments(rucksack))
            for rucksack in rucksacks
        )

    def solve_part_2(self, rucksacks: list[str]) -> int:
        return sum(
            self.get_type_priority(self.find_common_type(rucksacks[i : i + 3]))
            for i in range(0, len(rucksacks), 3)
        )

    def find_common_type_in_compartments(self, rucksack: str) -> str:
        first_compartment = rucksack[: len(rucksack) // 2]
        second_compartment = rucksack[len(rucksack) // 2 :]

        return self.find_common_type([first_compartment, second_compartment])

    def find_common_type(self, items: list[str]) -> str:
        items_as_sets = [set(item) for item in items]
        intersection = functools.reduce(lambda x, y: x & y, items_as_sets)
        return next(iter(intersection))

    def get_type_priority(self, item_type: str):
        if item_type.islower():
            return ord(item_type) - ord("a") + 1

        return ord(item_type) - ord("A") + 27
