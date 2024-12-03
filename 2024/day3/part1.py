import re

def read_lines(filename):
    with open(filename) as f:
        return f.readlines()
    
lines = read_lines("input.txt")
s = ""
for line in lines:
    s += line
# print(s)

muls = re.findall(r"mul\(\d+,\d+\)", s)
print(muls)
sum = 0
for mul in muls:
    p = 1
    for d in re.findall(r"\d+", mul):
        p *= int(d)
    sum += p
print("sum", sum)