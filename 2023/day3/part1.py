import re


def read_input():
    with open("input.txt") as f:
        lines = []
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
        return lines


input = read_input()

# input = [
#     "467..114..",
#     "...*......",
#     "..35..633.",
#     "......#...",
#     "617*......",
#     ".....+.58.",
#     "..592.....",
#     "......755.",
#     "...$.*....",
#     ".664.598..",
# ]


# print(input)


def is_symbol_in_row(row, start_col, end_col, width, input):
    for col in range(max(start_col - 1, 0), min(end_col + 1, width)):
        val = input[row][col]
        if not (val.isdigit() or val == "."):
            print(f"symbol at {row}, {col}")
            return True
    return False


def is_symbol_in_col(col, row, input):
    val = input[row][col]
    if not (val.isdigit() or val == "."):
        print(f"symbol at {row}, {col}")
        return True
    return False


def is_part_number(start, end, line_number, width, height, input):
    # above
    if line_number > 0:
        if is_symbol_in_row(line_number - 1, start, end, width, input):
            print("symbol is above")
            return True
    # below
    if line_number < height - 1:
        if is_symbol_in_row(line_number + 1, start, end, width, input):
            print("symbol is below")
            return True
    # left
    if start > 0:
        if is_symbol_in_col(start - 1, line_number, input):
            print("symbol is left")
            return True
    # right
    if end < width:
        if is_symbol_in_col(end, line_number, input):
            print("symbol is right")
            return True


width = len(input[0])
height = len(input)

part_numbers = []
for line_number, line in enumerate(input):
    c = re.compile("\d+")
    for match in c.finditer(line):
        if is_part_number(
            match.start(), match.end(), line_number, width, height, input
        ):
            print(f"{match} IS a part number")
            part_number = int(match.group(0))
            part_numbers.append(part_number)
        else:
            print(f"{match} is NOT a part number")
print(sum(part_numbers))
