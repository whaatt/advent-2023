# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict
from functools import cache


input_value = open("input.txt", "r").read()
grid = input_value.split("\n")

start = None
for column in range(len(grid[0])):
    if grid[0][column] == ".":
        start = (0, column)

end = None
for column in range(len(grid[len(grid) - 1])):
    if grid[len(grid) - 1][column] == ".":
        end = (len(grid) - 1, column)


def get_neighbors(grid, position):
    (row, column) = position
    # current_value = grid[row][column]
    result = set()
    for new_row, new_column in {
        (row - 1, column),
        (row, column - 1),
        (row + 1, column),
        (row, column + 1),
    }:
        # Check bounds.
        if new_row < 0 or new_row >= len(grid):
            continue
        if new_column < 0 or new_column >= len(grid[0]):
            continue
        # P1:
        # Check slides from.
        # if current_value == ">" and new_column <= column:
        #     continue
        # if current_value == "<" and new_column >= column:
        #     continue
        # if current_value == "v" and new_row <= row:
        #     continue
        # if current_value == "^" and new_row >= row:
        #     continue
        new_value = grid[new_row][new_column]
        # Check forest.
        if new_value == "#":
            continue
        # P1:
        # Check slides to.
        # if new_value == ">" and new_column < column:
        #     continue
        # if new_value == "<" and new_column > column:
        #     continue
        # if new_value == "v" and new_row < row:
        #     continue
        # if new_value == "^" and new_row > row:
        #     continue
        result.add((new_row, new_column))
    return result


lengths = {}
successors = defaultdict(set)
for row in range(len(grid)):
    for column in range(len(grid[row])):
        vertex = (row, column)
        if grid[row][column] == "#":
            continue
        # P1:
        # if vertex != start and grid[row][column] not in "<>^v":
        #     continue
        if vertex != start and len(get_neighbors(grid, vertex)) < 3:
            continue
        seen = set()
        stack = [(vertex, 0)]
        while stack:
            (position, steps) = stack.pop()
            if position in seen:
                continue
            seen.add(position)
            # P2:
            # Case: Vertex end.
            if position != vertex and (
                len(get_neighbors(grid, position)) >= 3 or position == end
            ):
                successors[vertex].add(position)
                lengths[vertex, position] = steps
                continue
            # Case: Continue finding neighbors.
            neighbors = get_neighbors(grid, position)
            for neighbor in neighbors:
                # P1:
                # if grid[neighbor[0]][neighbor[1]] in "<>^v" or neighbor == end:
                #     successors[vertex].add((neighbor, steps + 1))
                #     continue
                stack.append((neighbor, steps + 1))

# longest = defaultdict(lambda: float("-inf"))
# longest[start] = 0
# got_changes = True
# while got_changes:
#     got_changes = False
#     for position in successors:
#         for successor, steps in successors[position]:
#             if longest[successor] < longest[position] + steps:
#                 longest[successor] = longest[position] + steps

# print(longest[end])


def get_longest(vertex, previous):
    if vertex in previous:
        return float("-inf")
    if vertex == end:
        return 0

    previous.add(vertex)
    longest_here = max(
        lengths[vertex, successor] + get_longest(successor, previous)
        for successor in successors[vertex]
    )
    previous.remove(vertex)
    return longest_here


print(get_longest(start, set()))
