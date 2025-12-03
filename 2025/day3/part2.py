def read_input():
    lines = []
    with open("input.txt") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return  lines

# lines = ["234234234234278", "811111111111119", "987654321111111", "818181911112111"]

lines = read_input()

total_sum = 0

# 1. Från vänster, hitta den största vid j där j > i så att det finns 12 - len(hittade) kvar till höger om j

for line in lines:
    bank = [int(c) for c in line]
    chosen = []
    i = 0
    while i < len(bank):
        candidate = bank[i]
        for j in range(i+1, len(bank)):
            # print(f"{i} {j}: {bank[j]}  {len(bank) - j} {12 - len(chosen)}")
            if bank[j] > candidate and (len(bank) - j) >= (12 - len(chosen)):
                candidate = bank[j]
                i = j
        # print("Appending", candidate, "from", i)
        chosen.append(candidate)
        if len(chosen) == 12:
            break
        if candidate == bank[i]:
            i += 1
    print(chosen)
    total_sum += int("".join([str(v) for v in chosen]))
print("Total sum: ", total_sum)
