# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import deque

input_value = open("input.txt", "r").read()
grid = input_value.split("\n")

add_rows = set()
for row in range(len(grid)):
    if all(x == "." for x in grid[row]):
        add_rows.add(row)

add_columns = set()
for column in range(len(grid[0])):
    values = [grid[row][column] for row in range(len(grid))]
    if all(x == "." for x in values):
        add_columns.add(column)

total = 0
for row in range(len(grid)):
    for column in range(len(grid[row])):
        if grid[row][column] == ".":
            continue

        seen = set()
        queue = deque([(row, column, 0)])
        while queue:
            (x, y, distance) = queue.popleft()
            if (x, y) in seen:
                continue
            seen.add((x, y))

            if grid[x][y] == "#" and (x != row or y != column):
                total += distance

            for m, n in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
                if m < 0 or m >= len(grid) or n < 0 or n >= len(grid[0]):
                    continue
                if m not in add_rows and x in add_rows:
                    new_distance = distance + 1000000
                elif n not in add_columns and y in add_columns:
                    new_distance = distance + 1000000
                else:
                    new_distance = distance + 1
                queue.append((m, n, new_distance))

print(int(total / 2))
