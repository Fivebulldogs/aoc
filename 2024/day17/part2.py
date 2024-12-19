from collections import deque

program = [2, 4, 1, 2, 7, 5, 0, 3, 1, 7, 4, 1, 5, 5, 3, 0]
program_str = ",".join(str(v) for v in program)
regB = 0
regC = 0


# regA = 27334280
def run_program(suggestion):
    output_vals = []
    regA = suggestion
    while regA != 0:
        # bst regA (2,4)
        # regB = regA % 8
        regB = regA & 7
        # bxl 2    (1,2)
        regB = regB ^ 2  # xor of regB with 2 => flip bit 2
        # cdv regB (7,5)
        # regC = int(regA / pow(2, regB))  # C = shift A regB bits right
        regC = regA >> regB
        # adv 3    (0,3)
        # regA = int(regA / pow(2, 3))  # A = shift A three bits right
        regA >>= 3
        # bxl 7    (1,7)
        # regB = regB ^ 7  # flip rightmost three bits
        regB ^= 7
        # bxc 1    (4,1)
        # regB = regB ^ regC
        regB ^= regC
        # output regB  (5,5)
        # output_val = regB % 8  # => output 3 rightmost bits
        output_val = regB & 7
        output_vals.append(output_val)
    return output_vals


def test_output(output_vals, program):
    if len(output_vals) > 0:
        for k, output_val in enumerate(reversed(output_vals)):
            # print(" ", output_val, program[15 - k])
            if output_val != program[15 - k]:
                return (False, None, 0)
        return (True, output_vals, len(output_vals))
    return (False, None, 0)


q = deque()
q.append("")
output_cnt = 0
min_reg_a = 1e50
while True:
    try:
        input_bin_str = q.pop()
        for j in range(
            pow(2, 6)
        ):  # we seem to need to test two ternary numbers at a time
            suggestion = f"{input_bin_str}{j:03b}"
            regA = int(suggestion, 2)
            output_vals = run_program(regA)
            (output_correct, output_vals, output_cnt) = test_output(
                output_vals, program
            )
            if output_correct:
                if output_cnt == 16:
                    if regA < min_reg_a:
                        min_reg_a = regA
                else:
                    q.appendleft(f"{suggestion}")
    except IndexError:
        break


print("result: ", min_reg_a)
