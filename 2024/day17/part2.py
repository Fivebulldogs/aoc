def read_file(filename):
    registers = {}
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            split_line = line.split(":")
            registers[split_line[0][-1]] =  int(split_line[1].strip())
            line = f.readline().strip()
        line = f.readline()
        program = [int(c.strip()) for c in line.split(":")[1].split(",")]
    return (registers, program)

def combo_operand(operand, registers):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return registers['A']
        case 5:
            return registers['B']
        case 6:
            return registers['C']
        case _:
            assert(False)


def run_program(program, registers):
    output = []
    output_idx  = 0
    ip = 0
    while True:
        instruction = program[ip]
        ip += 1
        operand = program[ip]
        
        match instruction:
            case 0:
                # adv
                registers['A'] = int(registers['A'] / pow(2, combo_operand(operand, registers)))
                ip += 1
            case 1:
                # bxl
                registers['B'] = registers['B'] ^ operand
                ip += 1
            case 2:
                # bst
                registers['B'] = combo_operand(operand, registers) % 8
                ip += 1
            case 3:
                # jnz
                if registers['A'] != 0:
                    ip = operand
            case 4:
                # bxc
                registers['B'] = registers['B'] ^ registers['C']
                ip += 1
            case 5:
                # out
                val = combo_operand(operand, registers) % 8
                if val != program[output_idx]:
                    # print(val, program[:output_idx+1])
                    return (-1, None)
                output.append(str(val))
                output_idx += 1
                ip += 1
            case 6:
                # bdv
                registers['B'] = int(registers['A'] / pow(2, combo_operand(operand, registers)))
                ip += 1
            case 7:
                # cdv
                registers['C'] = int(registers['A'] / pow(2, combo_operand(operand, registers)))
                ip += 1

        if ip >= len(program) - 1:
            return (0, output)

(registers, program) = read_file("input")

i = 1
program_str = ",".join([str(c) for c in program])
while True:
    registers['A'] = i
    (ok, output) = run_program(program, registers)
    if ok < 0:
        i += 2
        continue
    output_str = ",".join(output)
    if output_str[:5] == program_str[:5]:
        print("program_str", program_str)
        print("output_str", output_str)
        print(i)
    if output_str == program_str:
        print("found", i)
        break
    i += 2