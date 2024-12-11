input = "1750884 193 866395 7 1158 31 35216 0"
# input = "125 17"

pebbles = [v for v in input.split(" ")]

for i in range(25):
    new_pebbles = []
    for pebble in pebbles:
        if pebble == "0":
            new_pebbles.append("1")
        elif len(pebble) % 2 == 0:
            half_len = int(len(pebble)/2)

            left = pebble[:half_len]
            new_pebbles.append(left.lstrip("0"))

            right = pebble[half_len:]
            stripped_right = right.lstrip("0")
            new_pebbles.append(stripped_right if len(stripped_right) > 0 else "0")
        else:
            new_pebbles.append(str(int(pebble) * 2024))

        pebbles = new_pebbles
print("result", len(pebbles))