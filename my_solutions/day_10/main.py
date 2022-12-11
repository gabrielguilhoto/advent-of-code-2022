import typing


class AddxInstruction(typing.TypedDict):
    type: typing.Literal["addx"]
    value: int


class NoopInstruction(typing.TypedDict):
    type: typing.Literal["noop"]


Instruction = typing.Union[AddxInstruction, NoopInstruction]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        return self.find_signal_strengths_sum(self.get_instructions(raw_input))

    def solve_part_2(self, raw_input: list[str]) -> None:
        self.draw_on_crt(self.get_instructions(raw_input))

    def get_instructions(self, raw_input: list[str]) -> list[Instruction]:
        instructions: list[Instruction] = []

        for line in raw_input:
            splitted_line = line.split(" ")
            type = splitted_line[0]

            if type == "addx":
                value = int(splitted_line[1])
                instructions.append({"type": type, "value": value})

            if type == "noop":
                instructions.append({"type": type})

        return instructions

    def find_signal_strengths_sum(self, instructions: list[Instruction]) -> int:
        x = 1
        cycle_count: int = 0
        signal_strengths: list[int] = []

        def end_cycle(times: int):
            nonlocal cycle_count
            for _ in range(times):
                cycle_count += 1
                if cycle_count % 40 == 20:
                    signal_strengths.append(cycle_count * x)

        for instruction in instructions:
            if instruction["type"] == "noop":
                end_cycle(1)

            if instruction["type"] == "addx":
                end_cycle(2)
                x += instruction["value"]

        return sum(signal_strengths)

    def draw_on_crt(self, instructions: list[Instruction]) -> None:
        sprite_position = 1
        cycle_count: int = 0
        crt_pixels: list[str] = []
        PIXELS_PER_LINE = 40

        def end_cycle(times: int):
            nonlocal cycle_count
            for _ in range(times):
                is_pixel_lit = (
                    abs((cycle_count % PIXELS_PER_LINE) - sprite_position) <= 1
                )
                crt_pixels.append("#" if is_pixel_lit else ".")
                cycle_count += 1

        for instruction in instructions:
            if instruction["type"] == "noop":
                end_cycle(1)

            if instruction["type"] == "addx":
                end_cycle(2)
                sprite_position += instruction["value"]

        for i in range(0, len(crt_pixels), PIXELS_PER_LINE):
            print("".join(crt_pixels[i : i + PIXELS_PER_LINE]))
