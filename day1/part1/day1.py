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
 "1abc2",
 "pqr3stu8vwx",
 "a1b2c3d4e5f",
 "treb7uchet"]

input = read_input()
# print(input)

_sum = 0
for line in input:
    first_digit = re.search(r"\d", line)
    last_digit = re.search(r"\d", line[::-1])
    number = int(first_digit.group()) * 10 + int(last_digit.group())
    _sum += number
print(_sum)