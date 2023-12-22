# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa


from collections import defaultdict
import copy


input_value = open("input.txt", "r").read()
lines = input_value.split("\n")
x, y, z = "x", "y", "z"


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return str((self.x, self.y, self.z))


bricks = []
for line in lines:
    [start, end] = line.split("~")
    start = eval("(" + start + ")")
    end = eval("(" + end + ")")
    start = Point(*start)
    end = Point(*end)
    if start.z > end.z:
        start, end = end, start
    bricks.append((start, end))

bricks.sort(key=lambda point: point[0].z)

xy_occlusion = defaultdict(lambda: (0, -1))
supports_for = defaultdict(set)

for i in range(len(bricks)):
    (start, end) = bricks[i]

    max_occlusion = 0
    max_bricks = {}
    for x in range(start.x, end.x + 1):
        for y in range(start.y, end.y + 1):
            (occlusion, brick) = xy_occlusion[x, y]
            if occlusion > max_occlusion:
                max_occlusion = occlusion
                max_bricks = {(x, y): brick}
            elif occlusion == max_occlusion:
                if brick != -1:
                    max_bricks[x, y] = brick

    for x in range(start.x, end.x + 1):
        for y in range(start.y, end.y + 1):
            xy_occlusion[x, y] = (max_occlusion + (end.z - start.z + 1), i)
            if (x, y) in max_bricks:
                supports_for[i].add(max_bricks[x, y])

unsafe_set = set()
for supports in supports_for.values():
    if len(supports) == 1:
        unsafe_set |= supports

# print(len(bricks) - len(unsafe_set))


def test_brick(supports_for, brick):
    supports_here = copy.deepcopy(supports_for)
    bricks_removing = {brick}
    bricks_fallen = 0
    got_change = True
    while got_change:
        got_change = False
        new_bricks_removing = set()
        current_bricks = set(supports_here.keys())
        for brick in current_bricks:
            pre_count = len(supports_here[brick])
            supports_here[brick] -= bricks_removing
            post_count = len(supports_here[brick])
            if post_count < pre_count:
                got_change = True
            if post_count == 0:
                new_bricks_removing.add(brick)
                del supports_here[brick]
                bricks_fallen += 1
        bricks_removing = new_bricks_removing
    return bricks_fallen


print(sum(test_brick(supports_for, i) for i in range(len(bricks))))
