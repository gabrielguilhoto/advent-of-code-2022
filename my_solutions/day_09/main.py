import typing

Direction = typing.Literal["U", "D", "L", "R"]
Position = tuple[int, int]


class Movement(typing.TypedDict):
    direction: Direction
    steps: int


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        return self.count_tail_positions_for_part_1(self.get_movements(raw_input))

    def solve_part_2(self, raw_input: list[str]) -> int:
        return self.count_tail_positions_for_part_2(self.get_movements(raw_input))

    def get_movements(self, raw_input: list[str]) -> list[Movement]:
        movements: list[Movement] = []
        for line in raw_input:
            splitted_line = line.split(" ")
            movements.append(
                {
                    "direction": typing.cast(Direction, splitted_line[0]),
                    "steps": int(splitted_line[1]),
                }
            )
        return movements

    def count_tail_positions_for_part_1(self, movements: list[Movement]) -> int:
        head_position = (0, 0)
        tail_position = (0, 0)
        positions_tail_visited: set[Position] = set([tail_position])

        for movement in movements:
            for _ in range(movement["steps"]):
                head_position = self.move_head(head_position, movement["direction"])
                tail_position = self.move_tail(head_position, tail_position)
                positions_tail_visited.add(tail_position)

        return len(positions_tail_visited)

    def count_tail_positions_for_part_2(self, movements: list[Movement]) -> int:
        knot_positions: list[Position] = [(0, 0) for _ in range(10)]
        positions_tail_visited: set[Position] = set([knot_positions[-1]])

        for movement in movements:
            for _ in range(movement["steps"]):
                knot_positions[0] = self.move_head(
                    knot_positions[0], movement["direction"]
                )
                for i in range(1, len(knot_positions)):
                    knot_positions[i] = self.move_tail(
                        knot_positions[i - 1], knot_positions[i]
                    )
                positions_tail_visited.add(knot_positions[-1])

        return len(positions_tail_visited)

    def move_head(self, head_position: Position, direction: Direction):
        (x, y) = head_position

        if direction == "U":
            return (x, y + 1)

        if direction == "D":
            return (x, y - 1)

        if direction == "L":
            return (x - 1, y)

        if direction == "R":
            return (x + 1, y)

    def move_tail(self, head_position: Position, tail_position: Position) -> Position:
        if self.are_head_and_tail_touching(head_position, tail_position):
            return tail_position

        two_step_movement = self.move_tail_if_two_steps_from_head(
            head_position, tail_position
        )
        if two_step_movement:
            return two_step_movement

        return self.move_tail_diagonally(head_position, tail_position)

    def are_head_and_tail_touching(
        self, head_position: Position, tail_position: Position
    ) -> bool:
        x_distance = abs(head_position[0] - tail_position[0])
        y_distance = abs(head_position[1] - tail_position[1])

        return x_distance + y_distance <= 1 or (x_distance == 1 and y_distance == 1)

    def move_tail_if_two_steps_from_head(
        self, head_position: Position, tail_position: Position
    ) -> typing.Union[Position, None]:
        (x_h, y_h) = head_position
        (x_t, y_t) = tail_position

        if x_h == x_t and y_h == y_t + 2:
            return (x_t, y_t + 1)

        if x_h == x_t and y_h == y_t - 2:
            return (x_t, y_t - 1)

        if x_h == x_t + 2 and y_h == y_t:
            return (x_t + 1, y_t)

        if x_h == x_t - 2 and y_h == y_t:
            return (x_t - 1, y_t)

        return None

    def move_tail_diagonally(
        self, head_position: Position, tail_position: Position
    ) -> Position:
        def get_sign(num: int) -> int:
            return 1 if num > 0 else -1

        (x_h, y_h) = head_position
        (x_t, y_t) = tail_position

        return (x_t + get_sign(x_h - x_t), y_t + get_sign(y_h - y_t))
