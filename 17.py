# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

import heapq


input_value = open("input.txt", "r").read()
grid = [[int(x) for x in line] for line in input_value.split("\n")]

# seen = set()
# heap = []
# heapq.heappush(heap, (0, (0, 0, 0, 0, 0, 0)))

# while heap:
#     (loss, (row, column, up, down, left, right)) = heapq.heappop(heap)
#     if (row, column, up, down, left, right) in seen:
#         continue
#     seen.add((row, column, up, down, left, right))
#     if row == len(grid) - 1 and column == len(grid[row]) - 1:
#         print(loss)
#         break

#     if up < 3 and down == 0 and row - 1 >= 0:
#         heapq.heappush(
#             heap, (loss + grid[row - 1][column], (row - 1, column, up + 1, 0, 0, 0))
#         )
#     if down < 3 and up == 0 and row + 1 < len(grid):
#         heapq.heappush(
#             heap, (loss + grid[row + 1][column], (row + 1, column, 0, down + 1, 0, 0))
#         )
#     if left < 3 and right == 0 and column - 1 >= 0:
#         heapq.heappush(
#             heap, (loss + grid[row][column - 1], (row, column - 1, 0, 0, left + 1, 0))
#         )
#     if right < 3 and left == 0 and column + 1 < len(grid[row]):
#         heapq.heappush(
#             heap, (loss + grid[row][column + 1], (row, column + 1, 0, 0, 0, right + 1))
#         )

seen = set()
heap = []
heapq.heappush(heap, (0, (0, 0, 0, "D")))
heapq.heappush(heap, (0, (0, 0, 0, "R")))

while heap:
    (loss, (row, column, steps, direction)) = heapq.heappop(heap)
    if (row, column, steps, direction) in seen:
        continue
    seen.add((row, column, steps, direction))
    if row == len(grid) - 1 and column == len(grid[row]) - 1 and steps >= 4:
        print(loss)
        break

    if steps < 10:
        if direction == "U" and row - 1 >= 0:
            heapq.heappush(
                heap,
                (loss + grid[row - 1][column], (row - 1, column, steps + 1, direction)),
            )
        if direction == "D" and row + 1 < len(grid):
            heapq.heappush(
                heap,
                (loss + grid[row + 1][column], (row + 1, column, steps + 1, direction)),
            )
        if direction == "L" and column - 1 >= 0:
            heapq.heappush(
                heap,
                (loss + grid[row][column - 1], (row, column - 1, steps + 1, direction)),
            )
        if direction == "R" and column + 1 < len(grid[row]):
            heapq.heappush(
                heap,
                (loss + grid[row][column + 1], (row, column + 1, steps + 1, direction)),
            )

    if steps >= 4:
        directions = "LR" if direction in "UD" else "UD"
        for new_direction in directions:
            if new_direction == "U" and row - 1 >= 0:
                heapq.heappush(
                    heap,
                    (loss + grid[row - 1][column], (row - 1, column, 1, new_direction)),
                )
            if new_direction == "D" and row + 1 < len(grid):
                heapq.heappush(
                    heap,
                    (loss + grid[row + 1][column], (row + 1, column, 1, new_direction)),
                )
            if new_direction == "L" and column - 1 >= 0:
                heapq.heappush(
                    heap,
                    (loss + grid[row][column - 1], (row, column - 1, 1, new_direction)),
                )
            if new_direction == "R" and column + 1 < len(grid[row]):
                heapq.heappush(
                    heap,
                    (loss + grid[row][column + 1], (row, column + 1, 1, new_direction)),
                )
