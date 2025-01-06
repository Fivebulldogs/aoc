def read_file(filename):
    with open(filename) as f:
        return (int(l.strip()) for l in f.readlines())


def get_next_secret_number(secret_number):
    mul_secret_number = secret_number * 64
    secret_number = mul_secret_number ^ secret_number
    pruned_secret_number = secret_number % 16777216

    div_secret_number = int(pruned_secret_number / 32)
    secret_number ^= div_secret_number
    pruned_secret_number = secret_number % 16777216

    mul_secret_number = secret_number * 2048
    secret_number = pruned_secret_number ^ mul_secret_number
    secret_number %= 16777216
    return secret_number


secret_numbers = read_file("input")

for i in range(2000):
    next_secret_numbers = []
    for secret_number in secret_numbers:
        next_secret_number = get_next_secret_number(secret_number)
        next_secret_numbers.append(next_secret_number)
    secret_numbers = next_secret_numbers[:]

print(sum(secret_numbers))
