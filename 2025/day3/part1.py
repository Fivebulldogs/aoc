def read_input():
    lines = []
    with open("input.txt") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return  lines

# lines = ["987654321111111", "811111111111119", "234234234234278", "818181911112111"]

lines = read_input()

total_sum = 0
banks = []
for line in lines:
    # print(line)
    bank = [int(c) for c in line]
    bank_sum = 0
    for i, v1 in enumerate(bank):
        for v2 in bank[i+1:]:
            curr_sum = 10 * v1 + v2
            if curr_sum > bank_sum:
                # print(f"{v1}{v2}: {curr_sum}")
                bank_sum = curr_sum
    total_sum += bank_sum
print(f"sum: {total_sum}")
