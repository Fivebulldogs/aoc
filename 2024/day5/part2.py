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

def is_update_correct(update):
    for i in range(len(update) - 1):
        curr = update[i]
        next = update[i+1]
        if next not in ordering_rules[curr]:
            print(f"{curr} NOT before {next}: err")
            return (False, i)
    return (True, -1)

incorrect_updates = []
for update in updates:
    (correct, _) = is_update_correct(update)
    if not correct:
        incorrect_updates.append(update)

sum = 0
for update in incorrect_updates:
    while True:
        (correct, pos) = is_update_correct(update)
        if not correct:
            print("update", update, "incorrect at", pos)
            tmp = update[pos]
            update[pos] = update[pos+1]
            update[pos+1] = tmp
            print("updated to", update)
        else:
            sum += update[int(len(update)/2)]
            break

print("sum", sum)
