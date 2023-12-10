# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict, deque


input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

grid = defaultdict(lambda: ".")
for i in range(len(lines)):
    for j in range(len(lines[i])):
        grid[i, j] = lines[i][j]

start = [key for key in grid if grid[key] == "S"][0]


max_distance = 0
queue = deque([(start, 0)])
neighbors = set()
seen = set()
while queue:
    ((i, j), distance) = queue.popleft()
    if (i, j) in seen:
        continue
    seen.add((i, j))
    if distance > max_distance:
        max_distance = distance

    letter = grid[i, j]
    if letter == "|":
        neighbors.add(((i, j), (i - 1, j)))
        queue.append(((i - 1, j), distance + 1))
        neighbors.add(((i, j), (i + 1, j)))
        queue.append(((i + 1, j), distance + 1))
    elif letter == "-":
        queue.append(((i, j - 1), distance + 1))
        queue.append(((i, j + 1), distance + 1))
    elif letter == "L":
        queue.append(((i - 1, j), distance + 1))
        queue.append(((i, j + 1), distance + 1))
    elif letter == "J":
        queue.append(((i - 1, j), distance + 1))
        queue.append(((i, j - 1), distance + 1))
    elif letter == "7":
        queue.append(((i + 1, j), distance + 1))
        queue.append(((i, j - 1), distance + 1))
    elif letter == "F":
        queue.append(((i + 1, j), distance + 1))
        queue.append(((i, j + 1), distance + 1))
    elif letter == "S":
        up = False
        left = False
        right = False
        down = False
        if grid[i - 1, j] in "|F7":
            up = True
            queue.append(((i - 1, j), distance + 1))
        if grid[i, j - 1] in "-LF":
            left = True
            queue.append(((i, j - 1), distance + 1))
        if grid[i + 1, j] in "|LJ":
            down = True
            queue.append(((i + 1, j), distance + 1))
        if grid[i, j + 1] in "-J7":
            right = True
            queue.append(((i, j + 1), distance + 1))
        if up and left:
            grid[i, j] = "J"
        elif up and right:
            grid[i, j] = "L"
        elif down and left:
            grid[i, j] = "7"
        elif down and right:
            grid[i, j] = "F"
        elif up and down:
            grid[i, j] = "|"
        else:
            grid[i, j] = "-"

known_loop = seen
# print(max_distance)


def get_parity(i, j):
    parity = 0
    source = None
    for n in range(j - 1, -1, -1):
        if (i, n) in known_loop:
            if grid[i, n] == "|":
                # Defensive.
                source = None
                parity += 1
            elif grid[i, n] == "-":
                # Propagate.
                pass
            elif source is None:
                source = grid[i, n]
            else:
                if grid[i, n] == "L" and source == "7":
                    parity += 1
                elif grid[i, n] == "F" and source == "J":
                    parity += 1
                source = None
        else:
            if source is not None:
                parity += 1
            source = None
    return parity


def print_grid():
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            print(grid[i, j], end="")
        print()


# Find odd parity items.
known_in = set()
for i, j in grid:
    if (i, j) in known_loop:
        continue
    parity = get_parity(i, j)
    if parity % 2 == 1:
        known_in.add((i, j))
        grid[i, j] = "I"
    else:
        grid[i, j] = "O"

# print_grid()
# print(sorted(known_in))
print(len(known_in))
