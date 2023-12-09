# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

lines = [[int(x) for x in line.split()] for line in lines]


def next_value(line):
    line_diffs = [line]
    while not all(x == 0 for x in line_diffs[-1]):
        last = line_diffs[-1]
        line_diff = [last[i + 1] - last[i] for i in range(len(last) - 1)]
        line_diffs.append(line_diff)
    # line_diffs[-1].append(0)
    # for i in range(len(line_diffs) - 2, -1, -1):
    #     next_value_here = line_diffs[i][-1] + line_diffs[i + 1][-1]
    #     line_diffs[i].append(next_value_here)
    line_diffs[-1].insert(0, 0)
    for i in range(len(line_diffs) - 2, -1, -1):
        next_value_here = line_diffs[i][0] - line_diffs[i + 1][0]
        line_diffs[i].insert(0, next_value_here)
    return next_value_here


total = 0
for line in lines:
    total += next_value(line)

print(total)
