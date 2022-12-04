import heapq


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        elves = self.process_raw_input(raw_input)
        return max(sum(elf_calories) for elf_calories in elves)

    def solve_part_2(self, raw_input: list[str]) -> int:
        elves = self.process_raw_input(raw_input)
        max_calories_heap = [0, 0, 0]

        for elf_calories in elves:
            total_calories = sum(elf_calories)
            if total_calories > max_calories_heap[0]:
                heapq.heapreplace(max_calories_heap, total_calories)

        return sum(max_calories_heap)

    #    ['1000\n2000\n3000', '4000', '5000\n6000', '7000\n8000\n9000', '10000']
    # -> [[1000, 2000, 3000], [4000], [5000, 6000], [7000, 8000, 9000], [10000]]
    def process_raw_input(self, raw_input: list[str]) -> list[list[int]]:
        return [
            [int(s) for s in concatenated_numbers.split("\n")]
            for concatenated_numbers in raw_input
        ]
