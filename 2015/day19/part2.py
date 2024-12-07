import re

def read_lines(filename):
    m = {}
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            if len(line) == 0:
                break
            line_split = line.split(" => ")
            m[line_split[1]] = line_split[0]
            line = f.readline().strip()
        molecule = f.readline().strip()
                
    return (m, molecule)

(m, molecule) = read_lines("input")
sorted_m = {k: v for k, v in sorted(m.items(), key=lambda item: len(item[0]), reverse=True)}

curr_molecule = molecule
prev_molecule = molecule
print(curr_molecule, len(curr_molecule))
replace_cnt = 0
while curr_molecule != "e":
    for k, v in sorted_m.items():
        curr_molecule = re.sub(k, v, curr_molecule, 1)
        if curr_molecule != prev_molecule:
            print(f"replaced {k} -> {v}")
            replace_cnt += 1
            print(curr_molecule, len(curr_molecule))
            prev_molecule = curr_molecule
print("replace_cnt", replace_cnt)
