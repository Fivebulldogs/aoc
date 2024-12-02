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
sum = 0
left_list = sorted(left_list)
right_list = sorted(right_list)
print(left_list)
print(right_list)
for i in range(list_len):
    dist = abs(int(left_list[i]) - int(right_list[i]))
    sum += dist
    
print(sum)