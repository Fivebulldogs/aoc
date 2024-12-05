from collections import defaultdict
import re

def read_lines(filename):
    with open(filename) as f:
        lines = []
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
        return lines


lines = read_lines("input.txt")

def forwards_and_backwards(lines):
    xmas_fwd_cnt = 0
    xmas_bwd_cnt = 0
    for line in lines:
        # print(line)
        # rows, forward
        for hit in re.findall("XMAS", line):
            if len(hit) > 0:
                xmas_fwd_cnt += 1
        # print("rows, forward", re.findall("XMAS", line))

        # rows, backwards'
        reversed_line = list(line)
        reversed_line.reverse()
        reversed_line = "".join(reversed_line)
        for hit in re.findall("XMAS", reversed_line):
            if len(hit) > 0:
                xmas_bwd_cnt += 1
    return xmas_fwd_cnt + xmas_bwd_cnt

def transpose(lines):
    cols = defaultdict(lambda: defaultdict(list))
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "":
                break
            cols[j][i] = c

    cols_as_lines = []
    for _, col in cols.items():
        line_str = ""
        for _, c in col.items():
            line_str += c
        cols_as_lines.append(line_str)
    return cols_as_lines

def get_diagonals(lines):
    xmas_cnt = 0
    # right half
    for i in range(len(lines[0])):
        x = i
        y = 0
        s = ""
        while x >= 0 and x < len(lines[0]) and y >= 0 and y < len(lines):
            s += lines[y][x]
            x += 1
            y += 1
        for hit in re.findall("XMAS", s):
            if len(hit) > 0:
                xmas_cnt += 1
    # left half
    for i in range(1, len(lines)):
        x = 0
        y = i
        s = ""
        while x >= 0 and x < len(lines[0]) and y >= 0 and y < len(lines):
            s += lines[y][x]
            x += 1
            y += 1
        for hit in re.findall("XMAS", s):
            if len(hit) > 0:
                xmas_cnt += 1

    return xmas_cnt

print("   ", end="")
for j in range(len(lines[0])):
    print(j, end=" ")
print()

for i, line in enumerate(lines):
    print(i, " ", end="")
    for c in line:
        print(c, end=" ")
    print()

xmas_cnt = 0
# forwards and backwards
xmas_cnt += forwards_and_backwards(lines)

# up and down
print("upwards and downwards")
cols_as_lines = transpose(lines)
xmas_cnt += forwards_and_backwards(cols_as_lines)

# diagonal downwards, forwards
xmas_cnt +=  get_diagonals(lines)

xmas_cnt +=  get_diagonals(lines[::-1])

reversed_lines = [line[::-1] for line in lines]
xmas_cnt += get_diagonals(reversed_lines)

reversed_reversed_lines = [line[::-1] for line in lines[::-1]]
xmas_cnt += get_diagonals(reversed_reversed_lines)

print("total", xmas_cnt)
