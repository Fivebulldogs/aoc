from collections import defaultdict


def read_lines(filename):
    ordering_rules = defaultdict(list)
    updates =  []
    with open(filename) as f:
        lines = f.readlines()    
        read_ordering_rules = True    
        for line in lines:
            if line.strip() == "":
                read_ordering_rules = False
                continue
            if read_ordering_rules:
                rules = line.strip().split("|")
                ordering_rules[int(rules[0])].append(int(rules[1]))
            else:
                update = []
                for v in line.strip().split(","):
                    update.append(int(v))
                updates.append(update)

    return (ordering_rules, updates)

(ordering_rules, updates) = read_lines("input.txt")
# print(ordering_rules)
# print(updates)

sum = 0
for update in updates:
    print("update", update)
    update_ok = True
    for i in range(len(update) - 1):
        curr = update[i]
        next = update[i+1]
        if next in ordering_rules[curr]:
            print(f"{curr} before {next}: ok")
        else:
            print(f"{curr} NOT before {next}: err")
            update_ok = False
            break
    if update_ok:
        sum += update[int(len(update)/2)]

print("sum", sum)