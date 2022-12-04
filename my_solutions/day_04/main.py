class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        assignment_pairs = self.process_raw_input(raw_input)
        assignment_fully_containing_pairs = 0

        for pair in assignment_pairs:
            intersection_size = self.find_range_intersection_size(*pair)
            smallest_range_size = min(range[1] - range[0] + 1 for range in pair)

            if intersection_size == smallest_range_size:
                assignment_fully_containing_pairs += 1

        return assignment_fully_containing_pairs

    def solve_part_2(self, raw_input: list[str]) -> int:
        assignment_pairs = self.process_raw_input(raw_input)

        return len(
            [
                pair
                for pair in assignment_pairs
                if self.find_range_intersection_size(*pair) > 0
            ]
        )

    def process_raw_input(self, raw_input: list[str]) -> list[list[list[int]]]:
        return [
            [
                [int(section) for section in elf_sections.split("-")]
                for elf_sections in raw_string.split(",")
            ]
            for raw_string in raw_input
        ]

    # a non-positive return value denotes no intersection
    def find_range_intersection_size(self, range1: list[int], range2: list[int]) -> int:
        intersection_start = max(range1[0], range2[0])
        intersection_end = min(range1[1], range2[1])

        return intersection_end - intersection_start + 1
