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

def count_xmas(lines):
    matches = {"MS": defaultdict(list), "SM": defaultdict(list), "MM": defaultdict(list), "SS": defaultdict(list), "A": defaultdict(list)}
    for i, line in enumerate(lines):
        for match in re.finditer(r"(?=(M.{1}S))", line):
            matches["MS"][i].append(match)
        for match in re.finditer(r"(?=(S.{1}M))", line):
            matches["SM"][i].append(match)
        for match in re.finditer(r"A", line):
            matches["A"][i].append(match)

    cnt = 0
    for i, _ in enumerate(lines):
        for a_match in matches["A"][i]:
            for key in ["MS", "SM"]:
                if i > 0 and i < len(matches[key]) - 1:
                    for match_1 in matches[key][i - 1]:
                        for match_2 in matches[key][i + 1]:
                            if a_match.span()[0] == match_1.span()[0] + 1 and match_1.span() == match_2.span():
                                cnt += 1
    return cnt

def print_matrix(lines):
    print("   ", end="")
    for j in range(len(lines[0])):
        print(j, end=" ")
    print()

    for i, line in enumerate(lines):
        print(i, " ", end="")
        for c in line:
            print(c, end=" ")
        print()


lines = read_lines("input.txt")
cnt = 0
cnt = count_xmas(lines)

cnt += count_xmas(transpose(lines))
print("cnt", cnt)
