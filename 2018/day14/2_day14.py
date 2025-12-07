import sys
from collections import deque

recipes = [3, 7]
elf_indices = [0, 1]
input = sys.argv[1]
input_len = len(input)
done = False

cnt = 0
while not done:
    new_recipe_sum = sum(recipes[idx] for idx in elf_indices)
    # print("new_recipe_sum:", new_recipe_sum)
    q = deque()
    digit = new_recipe_sum % 10
    q.append(digit)
    new_recipe_sum = int(new_recipe_sum / 10)
    while new_recipe_sum > 0:
        # print("digit:", digit)
        digit = new_recipe_sum % 10
        q.append(digit)
        new_recipe_sum = int(new_recipe_sum / 10)

    while True:
        try:
            digit = q.pop()
            recipes.append(digit)

            left_slice = recipes[-input_len:]
            done = "".join([str(v) for v in left_slice]) == input
            if done:
                print(len(recipes[: -len(left_slice)]))
                break

        except IndexError:
            break

    if done:
        break

    for j in range(2):
        elf_indices[j] = (elf_indices[j] + recipes[elf_indices[j]] + 1) % len(recipes)


# 53274238 too high!
