# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

# from collections import defaultdict

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

# position = (0, 0)
# grid = set()

# for line in lines:
#     [_, _, color] = line.split(" ")
#     color = color[2:-1]
#     steps = int(color[:5], 16)
#     direction = {0: "R", 1: "D", 2: "L", 3: "U"}[int(color[5], 16)]

#     for _ in range(steps):
#         if direction == "R":
#             position = (position[0], position[1] + 1)
#         if direction == "L":
#             position = (position[0], position[1] - 1)
#         if direction == "U":
#             position = (position[0] - 1, position[1])
#         if direction == "D":
#             position = (position[0] + 1, position[1])
#         grid.add(position)
#         colors[position] = color

# min_row = min(position[0] for position in grid)
# max_row = max(position[0] for position in grid)
# min_column = min(position[1] for position in grid)
# max_column = max(position[1] for position in grid)

# not_grid = set()
# for start_row in range(min_row, max_row + 1):
#     print(start_row)
#     for start_column in range(min_column, max_column + 1):
#         if (start_row, start_column) in grid:
#             continue
#         if (start_row, start_column) in not_grid:
#             continue

#         seen = set()
#         got_exterior = False
#         stack = [(start_row, start_column)]
#         while stack:
#             (row, column) = stack.pop()
#             if (
#                 row < min_row
#                 or row > max_row
#                 or column < min_column
#                 or column > max_column
#             ):
#                 got_exterior = True
#                 break
#             if (row, column) in grid:
#                 continue
#             if (row, column) in seen:
#                 continue
#             seen.add((row, column))
#             for new_row, new_column in {
#                 (row - 1, column),
#                 (row, column - 1),
#                 (row + 1, column),
#                 (row, column + 1),
#             }:
#                 stack.append((new_row, new_column))

#         if got_exterior:
#             not_grid |= seen
#         else:
#             grid |= seen

# print(len(grid))


position = (0, 0)
positions = [(0, 0)]
total_steps = 0
last_direction = None
for line in lines:
    # [direction, steps, _] = line.split(" ")
    # steps = int(steps)
    [_, _, color] = line.split(" ")
    color = color[2:-1]
    steps = int(color[:5], 16)
    direction = {0: "R", 1: "D", 2: "L", 3: "U"}[int(color[5], 16)]
    total_steps += steps

    if direction == "R":
        position = (position[0], position[1] + steps)
    if direction == "L":
        position = (position[0], position[1] - steps)
    if direction == "U":
        position = (position[0] - steps, position[1])
    if direction == "D":
        position = (position[0] + steps, position[1])
    last_direction = direction
    positions.append(position)
positions.append(positions[1])

min_row = min(position[0] for position in positions) - 5
# Use max bounds here...
max_row = max(position[0] for position in positions) + 5
min_column = min(position[1] for position in positions) - 5
max_column = max(position[1] for position in positions) + 5

total = 0
for i in range(len(positions) - 2):
    current = positions[i]
    new = positions[i + 1]

    if current[1] == new[1]:
        height = abs(new[0] - current[0]) - 1
        next_direction = "R" if new[1] < positions[i + 2][1] else "L"
        if (last_direction == "R") != (current[0] < new[0]):
            height += 1
        if (next_direction == "L") != (current[0] < new[0]):
            height += 1
        # Down
        if current[0] < new[0]:
            border = current[1]
            include = (border - min_column) * height
            exclude = (max_column - border) * height
            last_direction = "D"
        # Up
        else:
            border = current[1] + 1
            include = (max_column - border) * height
            exclude = (border - min_column) * height
            last_direction = "U"
    else:
        next_direction = "D" if new[0] < positions[i + 2][0] else "U"
        width = abs(new[1] - current[1]) - 1
        if (last_direction == "U") != (current[1] < new[1]):
            width += 1
        if (next_direction == "D") != (current[1] < new[1]):
            width += 1
        # Right
        if current[1] < new[1]:
            border = current[0] + 1
            include = (max_row - border) * width
            exclude = (border - min_row) * width
            last_direction = "R"
        # Left
        else:
            border = current[0]
            include = (border - min_row) * width
            exclude = (max_row - border) * width
            last_direction = "L"

    total += include - exclude

print(total // 4 + total_steps)
