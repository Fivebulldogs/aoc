from collections import defaultdict
from functools import reduce
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


def find_symbol_in_row(row, start_col, end_col, width, input):
    symbols = []
    for col in range(max(start_col - 1, 0), min(end_col + 1, width)):
        val = input[row][col]
        if not (val.isdigit() or val == "."):
            symbols.append((row, col))
            # print(f"symbol at {row}, {col}")
    return symbols


def find_symbol_in_col(col, row, input):
    val = input[row][col]
    if not (val.isdigit() or val == "."):
        # print(f"symbol at {row}, {col}")
        return (row, col)
    return None


def find_adjacent_symbols(start, end, line_number, width, height, input):
    adjacent_symbols = []

    # above
    if line_number > 0:
        symbols = find_symbol_in_row(line_number - 1, start, end, width, input)
        adjacent_symbols.extend(symbols)

    # below
    if line_number < height - 1:
        symbols = find_symbol_in_row(line_number + 1, start, end, width, input)
        adjacent_symbols.extend(symbols)

    # left
    if start > 0:
        symbol = find_symbol_in_col(start - 1, line_number, input)
        if symbol is not None:
            adjacent_symbols.append(symbol)

    # right
    if end < width:
        symbol = find_symbol_in_col(end, line_number, input)
        if symbol is not None:
            adjacent_symbols.append(symbol)
    return adjacent_symbols


width = len(input[0])
height = len(input)

part_numbers = []
symbol_to_parts = defaultdict(list)

for line_number, line in enumerate(input):
    c = re.compile("\d+")
    for match in c.finditer(line):
        adjacent_symbols = find_adjacent_symbols(
            match.start(), match.end(), line_number, width, height, input
        )

        if len(adjacent_symbols) > 0:
            part_number = int(match.group(0))
            for symbol in adjacent_symbols:
                symbol_to_parts[symbol].append(part_number)

gear_ratios = []
for symbol, parts in symbol_to_parts.items():
    if len(parts) > 1:
        gear_ratios.append(reduce(lambda x, y: x * y, parts))
print(sum(gear_ratios))
