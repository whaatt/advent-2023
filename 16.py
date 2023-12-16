# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
grid = input_value.split("\n")


def modify_by_direction(row, column, direction):
    if direction == "R":
        return (row, column + 1, direction)
    if direction == "L":
        return (row, column - 1, direction)
    if direction == "U":
        return (row - 1, column, direction)
    if direction == "D":
        return (row + 1, column, direction)
    return None


def get_energy(start_row, start_column, start_direction):
    seen_positions = set()
    stack = [(start_row, start_column, start_direction)]
    seen_stack = set()

    while stack:
        (row, column, direction) = stack.pop()
        if row < 0 and direction != "D":
            continue
        if row >= len(grid) and direction != "U":
            continue
        if column < 0 and direction != "R":
            continue
        if column >= len(grid[0]) and direction != "L":
            continue

        if (row, column, direction) in seen_stack:
            continue
        seen_stack.add((row, column, direction))
        seen_positions.add((row, column))

        if grid[row][column] == ".":
            stack.append(modify_by_direction(row, column, direction))
        elif grid[row][column] == "|":
            if direction in "UD":
                stack.append(modify_by_direction(row, column, direction))
            else:
                stack.append(modify_by_direction(row, column, "U"))
                stack.append(modify_by_direction(row, column, "D"))
        elif grid[row][column] == "-":
            if direction in "RL":
                stack.append(modify_by_direction(row, column, direction))
            else:
                stack.append(modify_by_direction(row, column, "R"))
                stack.append(modify_by_direction(row, column, "L"))
        elif grid[row][column] == "/":
            if direction == "R":
                stack.append(modify_by_direction(row, column, "U"))
            elif direction == "D":
                stack.append(modify_by_direction(row, column, "L"))
            elif direction == "U":
                stack.append(modify_by_direction(row, column, "R"))
            elif direction == "L":
                stack.append(modify_by_direction(row, column, "D"))
        elif grid[row][column] == "\\":
            if direction == "R":
                stack.append(modify_by_direction(row, column, "D"))
            elif direction == "D":
                stack.append(modify_by_direction(row, column, "R"))
            elif direction == "U":
                stack.append(modify_by_direction(row, column, "L"))
            elif direction == "L":
                stack.append(modify_by_direction(row, column, "U"))

    return len(seen_positions)


# Part 1:
# print(get_energy(0, 0, "R"))

starts = []
for i in range(len(grid)):
    starts.append((i, 0, "R"))
    starts.append((i, len(grid[0]) - 1, "L"))
    if i == 0:
        starts.append((i, 0, "D"))
        starts.append((i, len(grid[0]) - 1, "D"))
    if i == len(grid) - 1:
        starts.append((i, 0, "U"))
        starts.append((i, len(grid[0]) - 1, "U"))

for j in range(1, len(grid[0]) - 1):
    starts.append((0, j, "D"))
    starts.append((len(grid) - 1, j, "U"))

# Part 2:
print(max(get_energy(*start) for start in starts))
