# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from z3 import Int, Solver

minimum = 200000000000000
maximum = 400000000000000  # Inclusive.

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

hailstones = []
for line in lines:
    line = line.split(" @ ")
    position = tuple(int(coordinate) for coordinate in line[0].split(", "))
    velocity = tuple(int(coordinate) for coordinate in line[1].split(", "))
    hailstones.append((position, velocity))


def get_mb(p, v):
    m = v[1] / v[0]
    b = p[1] - m * p[0]
    return (m, b)


# m1x + b1 = m2x + b2
# (m1x - m2x) = b2 - b1

# x = (b2 - b1) / (m1 - m2)
# y = m1*x + b1


def get_intersection_xy(p1, v1, p2, v2):
    m1, b1 = get_mb(p1, v1)
    m2, b2 = get_mb(p2, v2)
    if (m1 - m2) == 0:
        return None
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    # Ugly as hell...
    if v1[0] < 0 and x > p1[0]:
        return None
    if v1[0] > 0 and x < p1[0]:
        return None
    if v2[0] < 0 and x > p2[0]:
        return None
    if v2[0] > 0 and x < p2[0]:
        return None
    return (x, y)


# total = 0
# for i in range(len(hailstones)):
#     for j in range(i + 1, len(hailstones)):
#         intersection = get_intersection_xy(
#             hailstones[i][0], hailstones[i][1], hailstones[j][0], hailstones[j][1]
#         )
#         if intersection is None:
#             continue
#         (x, y) = intersection
#         if minimum <= x <= maximum and minimum <= y <= maximum:
#             total += 1

# print(total)

p = [Int(f"p${i}") for i in range(3)]
v = [Int(f"v${i}") for i in range(3)]

constraints = []
for i in range(len(hailstones[:3])):
    t = Int(f"t{i}")
    pi = hailstones[i][0]
    vi = hailstones[i][1]
    constraints.append(t > 0)
    constraints.append(p[0] + v[0] * t == pi[0] + vi[0] * t)
    constraints.append(p[1] + v[1] * t == pi[1] + vi[1] * t)
    constraints.append(p[2] + v[2] * t == pi[2] + vi[2] * t)

# N hailstones; N * 3 equations; N + 6 unknowns
# 2, 6, 8
# 3, 9, 9
# 4, 12, 10

s = Solver()
s.add(*constraints)
s.check()
print(sum(s.model()[p[i]].as_long() for i in range(3)))

# A bunch of random scratch work that didn't go anywhere:
# 19 - 2t = x + vt
# (19 - x) = (v + 2)t
# x = 18, t = 1 -> v = -1
# x = 17, t = 1 -> v = -4
# x = 17, t = 2 -> v = -1
# x = 16, t = 1 -> v = 1
# x = 16, t = 2 -> N/A
# x = 16, t = 3 -> v = -1

# 19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3

# x < 19 and vx > -2 OR x > 19 and vx < -2
# x < 18 and vx > -1 OR x > 18 and vx < -1
# x < 20 and vx > -2 OR x > 20 and vx < -2
# x < 12 and vx > -1 OR x > 12 and vx < -1
# x < 20 and vx > 1

# p + vt0 = p0 + v0t0
# p + vt1 = p0 + v0t1
# (p - p0) = 0 (mod (v0 - v))
# (p - p1) = v1t1 - vt1

# p - 19 = 0 mod (-2 - v)
# p - 18 = 0 mod (-1 - v)
# -1 = 0 (mod (-2 - v) * (-1 - v))
# -1 = 0 (mod 2 + 3v + v^2)
# -1 = (v^2 + 3v + 2) * k

# 19 - 2t1 = p + vt1
# 18 - t2 = p + vt2
