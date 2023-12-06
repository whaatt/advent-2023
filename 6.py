# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

# times = [x for x in lines[0].split(": ")[1].split(" ") if x != ""]
# distances = [x for x in lines[1].split(": ")[1].split(" ") if x != ""]

# product = 1
# for i in range(len(times)):
#     ways = 0
#     max_time = times[i]
#     max_distance = distances[i]
#     for hold_time in range(max_time + 1):
#         current = hold_time * (max_time - hold_time)
#         if current > max_distance:
#             ways += 1
#     product *= ways

# print(product)

max_time = int("".join(x for x in lines[0].split(": ")[1].split(" ") if x != ""))
max_distance = int("".join(x for x in lines[1].split(": ")[1].split(" ") if x != ""))

ways = 0
# I guess you could do this in O(log(N))?
for hold_time in range(max_time + 1):
    current = hold_time * (max_time - hold_time)
    if current > max_distance:
        ways += 1

print(ways)
