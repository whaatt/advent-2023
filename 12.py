# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

problems = []
for line in lines:
    line = line.split(" ")
    springs = line[0]
    counts = tuple(int(x) for x in line[1].split(","))
    # Part 2 change:
    springs = "?".join([springs] * 5)
    # Part 2 change:
    counts *= 5
    problems.append((springs, counts))


def print_table(table):
    i_max = max(pair[0] for pair in table)
    j_max = max(pair[1] for pair in table)
    for i in range(i_max + 1):
        for j in range(j_max + 1):
            print(table[i, j], end="")
        print()


def solve_problem(springs, counts):
    table = defaultdict(int)
    for j in range(len(counts)):
        table[len(springs), j] = 0
    table[len(springs), len(counts)] = 1

    for i in range(len(springs) - 1, -1, -1):
        for j in range(len(counts), -1, -1):
            # print_table(table)
            # print(i, j)
            springs_here = springs[i:]
            counts_here = counts[j:]

            # Case: Chomp (possibly) operational spring.
            if springs_here[0] in ".?":
                table[i, j] += table[i + 1, j]

            # Continue if counts is zero (chomping is all we can do).
            if len(counts_here) == 0:
                continue

            # Case: Count immediately satisfiable.
            if (
                counts_here[0] <= len(springs_here)
                and all(x in "?#" for x in springs_here[: counts_here[0]])
                and springs_here[counts_here[0] : counts_here[0] + 1] in "?."
            ):
                # Case: Have to skip one since we're not at the end.
                if counts_here[0] < len(springs_here):
                    table[i, j] += table[i + counts_here[0] + 1, j + 1]
                # Case: No skipping necessary.
                else:
                    table[i, j] += table[i + counts_here[0], j + 1]

    # print_table(table)
    return table[0, 0]


print(sum(solve_problem(*problem) for problem in problems))
