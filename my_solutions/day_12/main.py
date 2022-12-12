import collections

Position = tuple[int, int]
Map = dict[Position, int]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        return self.find_distance(*self.process_raw_input(raw_input, {"S"}))

    def solve_part_2(self, raw_input: list[str]) -> int:
        return self.find_distance(*self.process_raw_input(raw_input, {"S", "a"}))

    def process_raw_input(
        self, raw_input: list[str], starting_values: set[str]
    ) -> tuple[Map, list[Position], Position]:
        starting_positions: list[Position] = []
        end: Position = (-1, -1)
        map: Map = {}

        for i, line in enumerate(raw_input):
            for j, value in enumerate(line):
                if value in starting_values:
                    starting_positions.append((i, j))

                if value == "S":
                    value = "a"

                if value == "E":
                    value = "z"
                    end = (i, j)

                map[(i, j)] = ord(value)

        return map, starting_positions, end

    def find_distance(
        self, map: Map, starting_points: list[Position], end: Position
    ) -> int:
        queue = collections.deque(starting_points)
        distances = {position: 0 for position in starting_points}

        while len(queue):
            (i, j) = queue.popleft()
            for neighbor in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                if neighbor not in map or map[neighbor] - map[(i, j)] > 1:
                    continue

                distance = distances[(i, j)] + 1
                if neighbor == end:
                    return distance

                if neighbor not in distances:
                    distances[neighbor] = distance
                    queue.append(neighbor)

        return -1
