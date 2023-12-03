# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("input.txt", "r").read()
grid = input_value.split("\n")

ratio_items = defaultdict(set)
for i in range(len(grid)):
    j = 0
    while j < len(grid[i]):
        start = j
        end = j
        adjacencies = []
        while end < len(grid[i]) and grid[i][end] in "0123456789":
            for m in range(-1, 2):
                for n in range(-1, 2):
                    if 0 <= i + m < len(grid) and 0 <= end + n < len(grid[i + m]):
                        if grid[i + m][end + n] == "*":
                            adjacencies.append((i + m, end + n))
            end += 1
        for adjacency in adjacencies:
            ratio_items[adjacency].add((i, start, end, int(grid[i][start:end])))
        if start == end:
            j = end + 1
        else:
            j = end

total = 0
for key in ratio_items:
    item = ratio_items[key]
    if len(item) == 2:
        ratio = 1
        for i, start, end, value in item:
            ratio *= value
        total += ratio

print(total)
