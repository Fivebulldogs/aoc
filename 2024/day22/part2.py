from collections import defaultdict, deque


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


initial_secret_numbers = read_file("input")
price_changes_to_bananas = defaultdict(dict)

for i, initial_secret_number in enumerate(initial_secret_numbers):
    secret_numbers = []
    prev_price = None
    q = deque()
    secret_number = initial_secret_number
    for j in range(2000):
        price = secret_number % 10
        if prev_price is not None:
            price_change = price - prev_price
            q.append(price_change)

        if j > 4:
            q.popleft()
            key = hash("".join([str(v) for v in tuple(q)]))
            price_change_sequence_dict = price_changes_to_bananas.get(key)
            if (
                price_change_sequence_dict is None
                or price_change_sequence_dict.get(i) is None
            ):
                price_changes_to_bananas[key][i] = price

        secret_number = get_next_secret_number(secret_number)
        prev_price = price

max_sum = -1
for v in price_changes_to_bananas.values():
    s = 0
    for i, banana_count in v.items():
        s += banana_count
    if s > max_sum:
        max_sum = s
print(max_sum)
