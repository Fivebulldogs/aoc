import re


def read_input():
    with open("input.txt") as f:
        lines = []
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
        return lines
    

input = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen"
]

input = read_input()

number_table = {
    "one" : 1,
    "two" : 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

_sum = 0
for line in input:
    first_digit = None
    first_digit_pos = 1e6
    last_digit = None
    last_digit_pos = -1
    for (k, v) in number_table.items():
        c = re.compile(rf"{k}")
        for m in c.finditer(line):
            digit_pos = m.start()
            digit = m.group()
            if digit_pos < first_digit_pos:
                first_digit = number_table[digit]
                first_digit_pos = digit_pos
            if digit_pos > last_digit_pos:
                last_digit = number_table[digit]
                last_digit_pos = digit_pos

    for v in range(1, 10):
        c = re.compile(rf"\d")
        for m in c.finditer(line):
            digit_pos = m.start()
            digit = m.group()
            if digit_pos < first_digit_pos:
                first_digit = int(digit)
                first_digit_pos = digit_pos
            if digit_pos > last_digit_pos:
                last_digit = int(digit)
                last_digit_pos = digit_pos

    # print(first_digit, last_digit)
    number = first_digit * 10 + last_digit
    print(first_digit, last_digit, number)
    _sum += number
print(_sum)
