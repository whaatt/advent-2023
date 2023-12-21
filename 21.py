# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa


input_value = open("input.txt", "r").read()
grid = input_value.split("\n")

# for i in range(len(grid)):
#     grid[i] = grid[i] * 5
# grid = grid * 5

print(len(grid), len(grid[0]))
# start = None
# for row in range(len(grid)):
#     for column in range(len(grid)):
#         if grid[row][column] == "S":
#             start = (row, column)

# total_corner = 0
for start_set in [
    # {(0, 65)},  # U
    # {(65, 0)},  # L
    # {(130, 65)},  # D
    # {(65, 130)},  # R
    # {(0, 65), (65, 0)},  # UL
    # {(65, 0), (0, 65)},  # LD
    # {(130, 65), (65, 130)},  # DR
    # {(65, 130), (0, 65)},  # RU
    {(0, 0)},
    {(130, 0)},
    {(0, 130)},
    {(130, 130)},
    # {(327, 327)},
    # {(65, 65)}
]:
    # for start in {(0, 0), (130, 0), (0, 130), (130, 130)}:
    # total_edge = 0
    # U, L, R, D
    # # for start in {(0, 65), (65, 0), (65, 130), (130, 65)}:
    # for start in {(65, 65)}:
    active_set = set()
    active_set |= start_set
    last_size, last_last_size = 0, 0
    steps = 0
    for _ in range(64):
        # print(steps)
        steps += 1
        new_active_set = set()
        for row, column in active_set:
            for new_row, new_column in {
                (row - 1, column),
                (row, column - 1),
                (row + 1, column),
                (row, column + 1),
            }:
                if new_row < 0 or new_row >= len(grid):
                    continue
                if new_column < 0 or new_column >= len(grid[0]):
                    continue
                if grid[new_row][new_column] not in ".S":
                    continue
                new_active_set.add((new_row, new_column))
        active_set = new_active_set
        # if len(active_set) == last_last_size:
        #     print(steps, len(active_set), last_size)
        #     break
        # last_last_size = last_size
        # last_size = len(active_set)
    print(len(active_set))
#     total_corner += len(active_set)

# print(total_corner)
# Steps: 131
# Reached: 7407 (odd number of steps)
# 26501365 // 131 = 202300
# 26501365 % 131 = 65

# 1 (1 filled, 4)
# 2 (1+4 filled, 9 edge, 8 corner)
#   zyz
#  zyxyz
#  yxxxy
#  zyxyz
#   zyz

# 0 Msteps: 0 filled, 0 edge, 0 corner
# 1 Msteps: 1 filled, 4 partial, 4 corner
# 2 Msteps: (1 + 4) filled, 8 partial, 8 corner
# 3 Msteps: (1 + 4 + 8) filled, 12 partial, 12 corner
#
#     y
# R  yxy   D
#   yxxxy
#  yxxxxxy
#   yxxxy
# R  yxy  L
#     y

#   zyz
#  zyxyz
#  yxxxy
#  zyxyz
#   zyz

# 202299th term of
# 4 + 8 + 12
# +1
# = 81850175401 * 7407 (total_center)
# 202300 * 4 partial (202300 * BAD (total_edge))
# 202300 * 4 corner (202300 * 3792 (total_corner))

# Corner terms
# 958
# 953
# 939
# 942
# 3792

# print(81850175401 * 7407 + 202300 * 22832 + 202300 * 3929)

# U 5693 I
# L 5704 I
# R 5723 I
# D 5712 I
# 6597
# 6581
# 6586
# 6600

# 22832 + 202299 * 26364
# 202299 remaining partial 4sets

# print(sum([6484, 6500, 6479, 6500]))
# print(
#     sum(
#         [
#             953,
#             939,
#             958,
#             942,
#         ]
#     )
# )

# 0 Msteps: 0 filled, 0 edge, 0 corner
# 1 Msteps: 1 filled, 4 partial, 4 corner
# 2 Msteps: (1 + 4) filled, 8 partial, 8 corner
# 3 Msteps: (1 + 4 + 8) filled, 12 partial, 12 corner
# 4 Msteps: (1 + 4 + 8 + 12) filled, 16 partial, 16 corner

# 4 MSteps:
# 1 + (0 + 8) of parity 0
# (4 + 12) of parity 1

# 5 MSteps:
# (1 + 8 + 16) of parity 0
# (4 + 12) of parity 1

# 6 MSteps:
# (1 + 8 + 16) of parity 0
# (4 + 12 + 20) of parity 1

# 202300 MSteps
# zero: 1 + ((N / 2) - 1)th term of 8 + 16 + etc,
# one: 4 * (N / 2) + ((N / 2) - 1)th term of 8 + 16 + etc..
# zero: 1 + 40924885400 = 40924885401
# one: 404600 + 40924885400 = 40925290000

# 101149th term of 8 + 16
# = (101149th term of 1 + 2) * 8
# = 5115610675 * 8
# = 40924885400

# 1
# 8 + 16 + 24 (plus 1)
# 4 + 12 + 20

# N = 2 MSteps
# (1 + (N - 1) * N / 2 * 4) = 5 for filled in MSquares
# Latest layer has N * 4 partials = 8
# 4 are simple edges (divided evenly between types)
# (N - 1) * 4 are complex edges (divided evenly between types)
#   - Even division 4X is baked into the sum 22298 (use multiplier 1)
#   - Even division 4X is baked into the sum 25963 (use multiplier N - 1)
# Latest layer has N * 4 corners = 8 (divided evenly between corner types)
#   - Even division 4X is baked into the sum 3792 (use multiplier N)
# 7407 + 4 * 7474 + 22298 + 1 * 25963 + 2 * 3792
# = 92880

# 93148 ??

# 59923 is target


# 131 - 15081 [good: 7407 + 1932/1906/1926/1910]
# 196 - 33564 [7407 + ]
# 262 - 59923


# 7407 odd; 7474 even

# 40924885401 * 7407 +
# 40925290000 * 7474 +
# 1 * 22298 + 202299 * 25963 + 202300 * 3792
# = 609012263058042
