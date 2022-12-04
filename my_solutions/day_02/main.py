import typing

FirstColumnLetter = typing.Literal["A", "B", "C"]
SecondColumnLetter = typing.Literal["X", "Y", "Z"]
ColumnLetter = typing.Union[FirstColumnLetter, SecondColumnLetter]
LetterTuple = tuple[FirstColumnLetter, SecondColumnLetter]

HandShape = typing.Literal["rock", "paper", "scissors"]
HandShapeTuple = tuple[HandShape, HandShape]

Outcome = typing.Literal["lose", "draw", "win"]

SHAPE_CORRESPONDECE: dict[ColumnLetter, HandShape] = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}
OUTCOME_CORRESPONDENCE: dict[SecondColumnLetter, Outcome] = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}

LOSER_TO: dict[HandShape, HandShape] = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}
WINNER_TO: dict[HandShape, HandShape] = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock",
}


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        strategy_guide = self.process_raw_input_for_part_1(raw_input)
        return sum(
            self.get_shape_score(entry) + self.get_outcome_score(entry)
            for entry in strategy_guide
        )

    def process_raw_input_for_part_1(
        self, raw_input: list[str]
    ) -> list[HandShapeTuple]:
        return self.normalize_letters_for_part_1(
            self.convert_raw_input_to_letter_tuple_list(raw_input)
        )

    def convert_raw_input_to_letter_tuple_list(
        self, raw_input: list[str]
    ) -> list[LetterTuple]:
        return [typing.cast(LetterTuple, tuple(entry.split())) for entry in raw_input]

    def normalize_letters_for_part_1(
        self, processed_input: list[LetterTuple]
    ) -> list[HandShapeTuple]:
        return [
            (SHAPE_CORRESPONDECE[entry[0]], SHAPE_CORRESPONDECE[entry[1]])
            for entry in processed_input
        ]

    def get_shape_score(self, entry: HandShapeTuple) -> int:
        [_opponent_shape, my_shape] = entry
        return {"rock": 1, "paper": 2, "scissors": 3}[my_shape]

    def get_outcome_score(self, entry: HandShapeTuple) -> int:
        [opponent_shape, my_shape] = entry

        if my_shape == opponent_shape:
            return 3

        if LOSER_TO[my_shape] == opponent_shape:
            return 6

        return 0

    def solve_part_2(self, raw_input: list[str]) -> int:
        strategy_guide = self.process_raw_input_for_part_2(raw_input)
        return sum(
            self.get_shape_score(entry) + self.get_outcome_score(entry)
            for entry in strategy_guide
        )

    def process_raw_input_for_part_2(
        self, raw_input: list[str]
    ) -> list[HandShapeTuple]:
        return self.normalize_letters_for_part_2(
            self.convert_raw_input_to_letter_tuple_list(raw_input)
        )

    def normalize_letters_for_part_2(
        self, processed_input: list[LetterTuple]
    ) -> list[HandShapeTuple]:
        return [
            (SHAPE_CORRESPONDECE[entry[0]], self.convert_outcome_to_my_shape(entry))
            for entry in processed_input
        ]

    def convert_outcome_to_my_shape(self, entry: LetterTuple) -> HandShape:
        opponent_shape = SHAPE_CORRESPONDECE[entry[0]]
        desired_outcome = OUTCOME_CORRESPONDENCE[entry[1]]

        if desired_outcome == "lose":
            return LOSER_TO[opponent_shape]

        if desired_outcome == "win":
            return WINNER_TO[opponent_shape]

        return opponent_shape
