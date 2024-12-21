max_output_idx  = 0
for i in range(100000000):
    regA = i
    regB = 0
    regC = 0

    program = [2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]
    program_str = ",".join(str(v) for v in program)
    #print("regA", regA)
    #print("program", program_str)
    
    output_list = []
    output_idx  = 0
    
    while regA != 0 and output_idx < len(program): # last op: (3,0)
        # bst regA (2,4)
        regB = regA % 8  # B will be between 0 and 7
        # bxl 2    (1,2)
        regB = regB ^ 2  # B will be between 1 and 7^2 = 49
        # cdv regB (7,5)
        regC = int(regA / pow(2, regB))  # C will be 
        # adv 3    (0,3)
        regA = int(regA / 8)
        # bxl 7    (1,7)
        regB = regB ^ 7
        # bxc 1    (4,1)
        regB = regB ^ regC
        # output regB  (5,5)
        output_val = regB % 8
        if output_val != program[output_idx]:
            continue
        output_list.append(output_val)
        if output_idx > max_output_idx:
            print("max_output_idx", max_output_idx)
            max_output_idx = output_idx
        output_idx += 1
        # print(regB % 8, end=",")
    # print()

    # if len(output_list) > 0 and ",".join([str(v) for v in output_list]) == program_str:
        # print(output_list)
        # print("result", i)
        # break

    if i % 1000000 == 0:
        print(i)