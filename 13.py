# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
patterns = input_value.split("\n\n")
patterns = [pattern.split("\n") for pattern in patterns]


def get_row_summary(row):
    total = 0
    for i in range(len(row)):
        number = 0
        if row[i] == "#":
            number = 1
        total += 2**i * number
    return total


def get_slice_smudge_equality(x, y):
    total_bits = 0
    for i in range(len(x)):
        total_bits += (x[i] ^ y[i]).bit_count()
    # Use 0 for Part 1.
    return total_bits == 1


def solve_pattern(pattern):
    rows = [get_row_summary(row) for row in pattern]
    columns_raw = [
        "".join(pattern[i][j] for i in range(len(pattern)))
        for j in range(len(pattern[0]))
    ]
    columns = [get_row_summary(column) for column in columns_raw]

    note = 0
    slices = len(pattern)
    for i in range(slices):
        remain = slices - i
        if i <= remain:
            if get_slice_smudge_equality(rows[:i], rows[i : 2 * i][::-1]):
                note += 100 * i
        else:
            if get_slice_smudge_equality(rows[i - remain : i], rows[i:][::-1]):
                note += 100 * i

    slices = len(pattern[0])
    for j in range(slices):
        remain = slices - j
        if j <= remain:
            if get_slice_smudge_equality(columns[:j], columns[j : 2 * j][::-1]):
                note += j
        else:
            if get_slice_smudge_equality(columns[j - remain : j], columns[j:][::-1]):
                note += j

    return note


print(sum(solve_pattern(pattern) for pattern in patterns))
