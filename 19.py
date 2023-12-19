# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
pieces = input_value.split("\n\n")

workflows = pieces[0].split("\n")
workflow_map = {}
for i in range(len(workflows)):
    workflow = workflows[i]
    [name, steps] = workflow.split("{")
    steps = steps[:-1]
    steps = steps.split(",")
    for j in range(len(steps)):
        step = steps[j]
        if ":" in step:
            step = step.split(":")
            step = (step[0], step[1])
        else:
            step = ("True", step)
        steps[j] = step
    workflow_map[name] = steps

total = 0
parts_entries = pieces[1].split("\n")
for parts in parts_entries:
    parts = parts[1:-1].split(",")
    for part in parts:
        exec(part)
    current = "in"
    while current not in {"A", "R"}:
        workflow = workflow_map[current]
        for step in workflow:
            if eval(step[0]):
                current = step[1]
                break
    if current == "A":
        total += eval("x + m + a + s")

# Part 1:
# print(total)

ranges_initial = tuple(((1, 4000),) for _ in "xmas")
stack = [("in", ranges_initial)]


def split_ranges(ranges, condition, invert):
    if condition == "True":
        return ranges

    char = condition[0]
    char_index = "xmas".index(char)
    value = int(condition[2:])

    new_range = []
    for start, end in ranges[char_index]:
        if invert:
            if condition[1] == ">":  # <=
                if start > value:
                    continue
                if end > value:
                    new_range.append((start, value))
                    continue
                new_range.append((start, end))
            else:  # >=
                if end < value:
                    continue
                if start < value:
                    new_range.append((value, end))
                    continue
                new_range.append((start, end))
        else:
            if condition[1] == ">":
                if end <= value:
                    continue
                if start <= value:
                    new_range.append((value + 1, end))
                    continue
                new_range.append((start, end))
            else:  # <
                if start >= value:
                    continue
                if end >= value:
                    new_range.append((start, value - 1))
                    continue
                new_range.append((start, end))

    ranges = list(ranges)
    ranges[char_index] = tuple(new_range)
    return tuple(ranges)


ranges_solutions = []
while stack:
    (name, ranges) = stack.pop()
    if name == "A":
        ranges_solutions.append(ranges)
        continue
    if name == "R":
        continue

    for step in workflow_map[name]:
        stack.append((step[1], split_ranges(ranges, step[0], False)))
        ranges = split_ranges(ranges, step[0], True)


def score_solution(ranges):
    product = 1
    for range in ranges:
        total_interval = 0
        for start, end in range:
            if start > end:
                continue
            total_interval += end - start + 1
        product *= total_interval
    return product


print(sum(score_solution(ranges) for ranges in ranges_solutions))
