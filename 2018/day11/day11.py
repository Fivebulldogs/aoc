input = 4842


def create_grid(input):
    grid = []
    for i in range(300):
        x = i + 1
        grid.append([])
        for j in range(300):
            y = j + 1
            rack_id = x + 10
            power_level = rack_id * y
            power_level += input
            power_level *= rack_id
            hundreds_digit = int(power_level / 100) % 10
            power_level = hundreds_digit - 5
            grid[i].append(power_level)
    return grid


def find_square(grid):
    max_sqr_sum = -1
    max_sqr_x = None
    max_sqr_y = None
    for i in range(0, 298):
        for j in range(0, 298):
            sum = 0
            # print(i, j)
            for a in range(i, i + 3):
                for b in range(j, j + 3):
                    sum += grid[a][b]
                    # print(a, b, grid[a][b], sum)
            # print(sum)
            if sum > max_sqr_sum:
                max_sqr_sum = sum
                max_sqr_x = i + 1
                max_sqr_y = j + 1
    return (max_sqr_x, max_sqr_y, max_sqr_sum)


grid = create_grid(input)
(max_sqr_x, max_sqr_y, max_sqr_sum) = find_square(grid)
print("x:", max_sqr_x, "y:", max_sqr_y, "sum:", max_sqr_sum)
