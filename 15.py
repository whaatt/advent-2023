# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")
items = lines[0].split(",")


def hash_item(item):
    value_here = 0
    for char in item:
        value_here += ord(char)
        value_here *= 17
        value_here %= 256
    return value_here


total_value = 0
for item in items:
    total_value += hash_item(item)

# print(total_value)

boxes = [[] for _ in range(256)]
for item in items:
    if "=" in item:
        [label, length] = item.split("=")
        length = int(length)
        box = hash_item(label)
        swapped = False
        for slot, (some_label, _) in enumerate(boxes[box]):
            if some_label == label:
                boxes[box][slot] = (label, length)
                swapped = True
                break
        if swapped:
            continue
        boxes[box].append((label, length))
    else:
        label = item[:-1]
        box = hash_item(label)
        for slot, (some_label, _) in enumerate(boxes[box]):
            if some_label == label:
                boxes[box].pop(slot)

total_power = 0
for box in range(len(boxes)):
    for slot, (_, length) in enumerate(boxes[box]):
        power = (box + 1) * (slot + 1) * length
        total_power += power

print(total_power)
