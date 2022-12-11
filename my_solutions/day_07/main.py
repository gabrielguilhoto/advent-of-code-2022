import re
import typing


class Node:
    name: str
    size: int
    total_size: int
    children: list["Node"]
    parent: typing.Union["Node", None]

    def __init__(self, name: str, parent: typing.Union["Node", None]):
        self.size = 0
        self.total_size = 0
        self.children = []
        self.name = name
        self.parent = parent

    def add_children(self, child: "Node"):
        self.children.append(child)

    def set_size(self, size: int):
        self.size = size

    def set_total_size(self, total_size: int):
        self.total_size = total_size


class DirectoryTree:
    root: Node

    def set_root(self, root: Node):
        self.root = root


class CdCommand(typing.TypedDict):
    type: typing.Literal["cd"]
    directory: str


class LsCommand(typing.TypedDict):
    type: typing.Literal["ls"]
    file_sizes: list[int]


SMALL_DIRECTORY_SIZE = 100000
AVAILABLE_SPACE = 70000000
SPACE_NEEDED_FOR_UPDATE = 30000000


Command = typing.Union[CdCommand, LsCommand]


class DayPuzzleSolver:
    def __init__(self):
        self.delimiter = "\n"

    def solve_part_1(self, raw_input: list[str]) -> int:
        commands = self.get_commands_from_input(raw_input)
        tree = self.build_directory_tree(commands)
        self.calculate_total_size(tree)
        return self.calculate_size_of_small_directories(tree.root)

    def solve_part_2(self, raw_input: list[str]) -> int:
        commands = self.get_commands_from_input(raw_input)
        tree = self.build_directory_tree(commands)
        self.calculate_total_size(tree)
        return self.find_directory_size_to_delete(tree)

    def get_commands_from_input(self, raw_input: list[str]) -> list[Command]:
        i = 0
        commands: list[Command] = []

        while i < len(raw_input):
            if raw_input[i].startswith("$ cd"):
                directory = re.search(r"\$ cd (.+)", raw_input[i]).groups()[0]
                commands.append({"type": "cd", "directory": directory})
                i += 1

            if raw_input[i].startswith("$ ls"):
                i += 1
                file_sizes_in_directory: list[int] = []
                while i < len(raw_input) and not raw_input[i].startswith("$"):
                    if raw_input[i].startswith("dir"):
                        i += 1
                        continue
                    size = int(re.search(r"(\d+) .+", raw_input[i]).groups()[0])
                    file_sizes_in_directory.append(size)
                    i += 1

                commands.append({"type": "ls", "file_sizes": file_sizes_in_directory})

        return commands

    def build_directory_tree(self, commands: list[Command]) -> DirectoryTree:
        size_tree = DirectoryTree()
        root = Node("/", None)
        size_tree.set_root(root)
        current_node = root
        for command in commands:
            if command["type"] == "cd":
                if command["directory"] == "/":
                    current_node = root
                elif command["directory"] == "..":
                    current_node = typing.cast(Node, current_node.parent)
                else:
                    current_children_names = [n.name for n in current_node.children]
                    if command["directory"] not in current_children_names:
                        new_node = Node(command["directory"], current_node)
                        current_node.add_children(new_node)
                        current_node = new_node
                    else:
                        current_node = next(
                            c
                            for c in current_node.children
                            if c.name == command["directory"]
                        )
            elif command["type"] == "ls":
                current_node.set_size(sum(command["file_sizes"]))

        return size_tree

    def calculate_total_size(self, tree: DirectoryTree):
        (tree.root).set_total_size(self.calculate_total_size_on_node(tree.root))

    def calculate_total_size_on_node(self, node: Node) -> int:
        total_size = (
            sum(self.calculate_total_size_on_node(child) for child in node.children)
            + node.size
        )
        node.set_total_size(total_size)
        return total_size

    def calculate_size_of_small_directories(self, node: Node) -> int:
        size_of_small_subdirectories = sum(
            self.calculate_size_of_small_directories(c) for c in node.children
        )

        is_directory_small = node.total_size <= SMALL_DIRECTORY_SIZE
        return size_of_small_subdirectories + (
            node.total_size if is_directory_small else 0
        )

    def find_directory_size_to_delete(self, tree: DirectoryTree) -> int:
        unused_space = AVAILABLE_SPACE - tree.root.total_size
        space_to_free = SPACE_NEEDED_FOR_UPDATE - unused_space

        all_total_sizes: list[int] = []
        self.find_all_total_sizes(tree.root, all_total_sizes)

        size_to_delete = AVAILABLE_SPACE
        for total_size in all_total_sizes:
            if total_size > space_to_free and total_size < size_to_delete:
                size_to_delete = total_size

        return size_to_delete

    def find_all_total_sizes(self, node: Node, all_total_sizes: list[int]):
        all_total_sizes.append(node.total_size)
        for child in node.children:
            self.find_all_total_sizes(child, all_total_sizes)
