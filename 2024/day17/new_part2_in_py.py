max_output_idx  = 0
max_output_idx = 0

regB = 0
regC = 0

program = [2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]
program_str = ",".join(str(v) for v in program)
#print("regA", regA)
#print("program", program_str)

output_list = []
output_idx  = 0

for i in range(len(program)): # 16
    for j in range(2):
    # while regA != 0 and output_idx < len(program): # last op: (3,0)
        # bst regA (2,4)
        # regB = regA % 8
        regB = regA & 7
        # bxl 2    (1,2)
        regB = regB ^ 2  # xor of regB with 2 => flip bit 2
        # cdv regB (7,5)
        # regC = int(regA / pow(2, regB))  # C = shift A regB bits right
        regC = regA >> regB # correct?
        # adv 3    (0,3)
        # regA = int(regA / pow(2, 3))  # A = shift A three bits right
        regA >>= 3 # correct? 
        # bxl 7    (1,7)
        # regB = regB ^ 7  # flip rightmost three bits
        regB ^= 7
        # bxc 1    (4,1)
        # regB = regB ^ regC
        regB ^= regC
        # output regB  (5,5)
        # output_val = regB % 8  # => output 3 rightmost bits
        output_val = regB & 7

        if output_val != program[output_idx]:
            continue
        output_list.append(output_val)
        if output_idx > max_output_idx:
            print("max_output_idx", max_output_idx)
            print(",".join([str(c) for c in program[:output_idx + 1]]))
            max_output_idx = output_idx
        output_idx += 1
        
        
