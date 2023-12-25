# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict, deque
from copy import deepcopy


input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

neighbors = defaultdict(set)
edges = []
for line in lines:
    [start, ends] = line.split(": ")
    ends = ends.split(" ")
    for end in ends:
        edges.append(tuple(sorted((start, end))))
        neighbors[start].add(end)
        neighbors[end].add(start)


def cut_and_test(neighbors, wires):
    for start, end in wires:
        neighbors[start].discard(end)
        neighbors[end].discard(start)

    sets = []
    seen = set()
    for vertex in neighbors:
        if vertex in seen:
            continue
        sets.append(set())
        stack = [vertex]
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            sets[-1].add(current)
            for neighbor in neighbors[current]:
                stack.append(neighbor)

    for start, end in wires:
        neighbors[start].add(end)
        neighbors[end].add(start)
    return sets


def union(iterable):
    initial = set()
    for item_set in iterable:
        initial |= item_set
    return item_set


depths = []
for start, end in edges:
    queue = deque((vertex, 1) for vertex in neighbors[start] - {end})
    seen = set()
    seen.add(start)
    # print(queue)
    while queue:
        (current, depth) = queue.popleft()
        if current == end:
            depths.append((depth, (start, end)))
            break
        if current in seen:
            continue
        seen.add(current)
        queue.extend((neighbor, depth + 1) for neighbor in neighbors[current])

lengths = [
    len(item)
    for item in cut_and_test(
        neighbors, [x[1] for x in sorted(depths, reverse=True)[:3]]
    )
]
print(lengths[0] * lengths[1])
