import re

def read_lines(filename):
    with open(filename) as f:
        return f.readlines()
    
lines = read_lines("input.txt")
s = ""
for line in lines:
    s += line
# print(s)

hits = re.findall(r"don\'t|do|mul\(\d+,\d+\)", s)
# print(hits)
sum = 0
enabled = True
for hit in hits:
    if hit == "do":
        enabled = True
    elif hit == "don't":
        enabled = False
    elif enabled:
        p = 1
        for d in re.findall(r"\d+", hit):
            p *= int(d)
        sum += p
print("sum", sum)
