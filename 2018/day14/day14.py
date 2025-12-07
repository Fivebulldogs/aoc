import sys
from collections import deque

recipes = [3, 7]
elf_indices = [0, 1]
recipe_target_count = int(sys.argv[1])

while len(recipes) < recipe_target_count + 10:
    # print("elf_indices:", elf_indices)
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
        except IndexError:
            break
    # print(recipes)

    for j in range(2):
        elf_indices[j] = (elf_indices[j] + recipes[elf_indices[j]] + 1) % len(recipes)

print(
    "".join([str(v) for v in recipes[recipe_target_count : recipe_target_count + 10]])
)
