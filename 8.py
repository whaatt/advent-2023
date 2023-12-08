# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

import math

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

directions = lines[0]

nodes = {}
for line in lines[2:]:
    line = line.split(" = ")
    now = line[0]
    [left, right] = line[1][1:-1].split(", ")
    nodes[now] = (left, right)

currents = set(key for key in nodes if key[-1] == "A")
z_distances = []

for current in currents:
    steps = 0
    z_count = 0
    z_last = 0
    while current[-1] != "Z":
        direction = directions[steps % len(directions)]
        steps += 1
        (left, right) = nodes[current]
        if direction == "L":
            current = left
        else:
            current = right
    z_distances.append(steps)

print(math.lcm(*z_distances))
