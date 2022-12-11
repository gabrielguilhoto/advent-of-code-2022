import collections
import typing


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = ""

    def solve_part_1(self, buffer: str) -> int:
        return self.find_end_of_first_k_distinct_chars(buffer, 4)

    def solve_part_2(self, buffer: str) -> int:
        return self.find_end_of_first_k_distinct_chars(buffer, 14)

    def find_end_of_first_k_distinct_chars(self, buffer: str, k: int) -> int:
        last_k_chars_queue: typing.Deque[str] = collections.deque()
        char_counts: dict[str, int] = collections.defaultdict(int)

        for i, char in enumerate(buffer):
            if len(last_k_chars_queue) < k:
                last_k_chars_queue.append(char)
                char_counts[char] += 1

            if len(last_k_chars_queue) == k:
                if len(char_counts) == k:
                    return i + 1
                else:
                    char_to_remove = last_k_chars_queue.popleft()
                    char_counts[char_to_remove] -= 1
                    if char_counts[char_to_remove] == 0:
                        del char_counts[char_to_remove]

        return -1
