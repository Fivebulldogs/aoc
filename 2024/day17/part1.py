def read_file(filename):
    registers = {}
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            split_line = line.split(":")
            registers[split_line[0][-1]] = int(split_line[1].strip())
            line = f.readline().strip()
        line = f.readline()
        program = [int(c.strip()) for c in line.split(":")[1].split(",")]
    return (registers, program)


def combo_operand(operand, registers):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case _:
            assert False


def run_program(program, registers):
    output = []
    ip = 0
    while True:
        instruction = program[ip]
        ip += 1
        operand = program[ip]

        match instruction:
            case 0:
                # adv
                registers["A"] = int(
                    registers["A"] / pow(2, combo_operand(operand, registers))
                )
                ip += 1
            case 1:
                # bxl
                registers["B"] = registers["B"] ^ operand
                ip += 1
            case 2:
                # bst
                registers["B"] = combo_operand(operand, registers) % 8
                ip += 1
            case 3:
                # jnz
                if registers["A"] != 0:
                    ip = operand
            case 4:
                # bxc
                registers["B"] = registers["B"] ^ registers["C"]
                ip += 1
            case 5:
                # out
                output.append(str(combo_operand(operand, registers) % 8))
                ip += 1
            case 6:
                # bdv
                registers["B"] = int(
                    registers["A"] / pow(2, combo_operand(operand, registers))
                )
                ip += 1
            case 7:
                # cdv
                registers["C"] = int(
                    registers["A"] / pow(2, combo_operand(operand, registers))
                )
                ip += 1

        if ip >= len(program) - 1:
            return output


(registers, program) = read_file("input")
# registers = {'C': 9}
# program = [2, 6]
output = run_program(program, registers)
print(",".join(output))
