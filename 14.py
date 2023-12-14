# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
grid = [[char for char in row] for row in input_value.split("\n")]


def get_load(grid):
    total_load = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "O":
                total_load += len(grid) - i
    return total_load


def roll_grid(grid):
    for column in range(len(grid[0])):
        current_tail = []
        for row in range(len(grid) - 1, -1, -1):
            if grid[row][column] == "#":
                for i in range(len(current_tail) - 1, -1, -1):
                    offset = len(current_tail) - 1 - i
                    tail_row = current_tail[i]
                    grid[tail_row][column] = "."
                    grid[row + 1 + offset][column] = "O"
                current_tail = []
            elif grid[row][column] == "O":
                current_tail.append(row)

        # Handle rocks at the top.
        for i in range(len(current_tail) - 1, -1, -1):
            offset = len(current_tail) - 1 - i
            tail_row = current_tail[i]
            grid[tail_row][column] = "."
            grid[offset][column] = "O"

    return grid


def grid_to_string(grid):
    return "\n".join("".join(row) for row in grid)


def rotate_right(grid):
    new_grid = [["." for i in range(len(grid))] for j in range(len(grid[0]))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            new_grid[j][len(grid) - i - 1] = grid[i][j]
    return new_grid


def cycle_grid(grid):
    grid = roll_grid(grid)
    grid = roll_grid(rotate_right(grid))
    grid = roll_grid(rotate_right(grid))
    grid = roll_grid(rotate_right(grid))
    return rotate_right(grid)


i = 0
seen = {}
while True:
    grid_string = grid_to_string(grid)
    if grid_string in seen:
        break
    seen[grid_string] = i
    grid = cycle_grid(grid)
    i += 1

difference = i - seen[grid_string]
cycles = (1000000000 - i) % difference
for _ in range(cycles):
    grid = cycle_grid(grid)

print(get_load(grid))
