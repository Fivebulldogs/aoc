from collections import defaultdict
from dataclasses import dataclass

@dataclass
class Line:
    test_val: int
    vals: list

def read_lines(filename):
    lines =  []
    with open(filename) as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
        return lines

def parse_lines(lines):
    data = []
    for line in lines:
        split_line = line.split(":")
        vals = split_line[1].split(" ")
        line_vals = []
        for val in vals:
            if val != "":
                line_vals.append(int(val.strip()))
        data.append(Line(test_val=int(split_line[0]), vals=line_vals))
    return data

def concat(val1, val2):    
    return int(f"{val1}{val2}")

def build_tree(vals, test_val, partial_result):
    if len(vals) == 0:
        if partial_result == test_val:
            return True
        else:
            return False
        
    return (build_tree(vals[1:], test_val, partial_result + vals[0]) or
            build_tree(vals[1:], test_val, partial_result * vals[0]) or 
            build_tree(vals[1:], test_val, concat(partial_result, vals[0])))

lines = read_lines("input")
data = parse_lines(lines)

result = 0
for line in data:
    if build_tree(line.vals[1:], line.test_val, line.vals[0]):
        result += line.test_val
print(result)
