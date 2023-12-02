# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

games = []
for line in lines:
    line = line.split(": ")[1]
    line = line.split("; ")
    line = [game.split(", ") for game in line]
    for i in range(len(line)):
        game = line[i]
        line[i] = {}
        for color in game:
            [count, color] = color.split(" ")
            count = int(count)
            line[i][color] = count
    games.append(line)

maxes = {"green": 13, "red": 12, "blue": 14}

# Part 1:
# total = 0
# for i in range(len(games)):
#     number = i + 1
#     game = games[i]
#     bad = False
#     for draw in game:
#         for color in maxes:
#             if color not in draw:
#                 continue
#             if draw[color] > maxes[color]:
#                 bad = True
#                 break
#         if bad:
#             break
#     if not bad:
#         total += number

# Part 2:
total = 0
for i in range(len(games)):
    number = i + 1
    game = games[i]
    bad = False
    mins = {color: 0 for color in maxes}
    for draw in game:
        for color in draw:
            mins[color] = max(mins[color], draw[color])
    # Definitely a less hard-coded way to do this...
    power = mins["green"] * mins["red"] * mins["blue"]
    total += power

print(total)
