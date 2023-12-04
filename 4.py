# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

dupes = defaultdict(lambda: 1)
processed = 0
for i in range(len(lines)):
    processed += dupes[i]
    line = lines[i]
    line = line.split(": ")[1]
    line = line.split(" | ")
    winning = {x for x in line[0].split(" ") if x != ""}
    yours = {x for x in line[1].split(" ") if x != ""}
    wins = 0
    for number in yours:
        if number in winning:
            wins += 1
    if wins > 0:
        for j in range(i + 1, i + 1 + wins):
            dupes[j] += dupes[i]

print(processed)
