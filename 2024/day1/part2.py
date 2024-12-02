def read_input(filename):
    with open(filename) as f:
        lines = f.readlines()
        left_list = []
        right_list = []
        for line in lines:
            line_split = line.split("   ")
            left_list.append(int(line_split[0]))
            right_list.append(int(line_split[1]))
        return (left_list, right_list, len(left_list))


(left_list, right_list, list_len) = read_input("input.txt")
print(left_list)
print(right_list)
sum = 0
for vl in left_list:
    vl_sum = 0
    for vr in right_list:
        if vl == vr:
            vl_sum += 1
    print(vl, vl_sum)
    sum += vl * vl_sum
print(sum)
