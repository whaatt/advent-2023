# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0,
}

total = 0
for line in lines:
    item = ""
    i = 0
    while i < len(line):
        char = line[i]
        try:
            item += str(int(char))
            break
        except:
            pass
        found = False
        for number in numbers:
            if line[i : i + len(number)] == number:
                item += str(numbers[number])
                i += len(number)
                found = True
                break
        if not found:
            i += 1
        else:
            break
    i = 0
    while i < len(line[::-1]):
        char = line[::-1][i]
        try:
            item += str(int(char))
            break
        except:
            pass
        found = False
        for number in numbers:
            if line[::-1][i : i + len(number)] == number[::-1]:
                item += str(numbers[number])
                i += len(number)
                found = True
                break
        if not found:
            i += 1
        else:
            break
    total += int(item)

print(total)
