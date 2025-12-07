INPUT = 4842
GRID_SIZE = 300
MIN_SQR = 2
MAX_SQR = 300


def create_grid(input):
    grid = []
    for i in range(GRID_SIZE):
        x = i + 1
        grid.append([])
        for j in range(GRID_SIZE):
            y = j + 1
            rack_id = x + 10
            power_level = rack_id * y
            power_level += INPUT
            power_level *= rack_id
            hundreds_digit = int(power_level / 100) % 10
            power_level = hundreds_digit - 5
            grid[i].append(power_level)
    return grid


def find_max_square(grid):
    max_sqr_sum = -1
    max_sqr_size = None
    max_sqr_x = None
    max_sqr_y = None
    sums = {}
    sums[1] = grid[:]

    for step in range(MIN_SQR, MAX_SQR + 1):
        print("step", step)
        sums[step] = []
        for i in range(0, GRID_SIZE - step):
            sums[step].append([])
            for j in range(0, GRID_SIZE - step):
                sum = sums[step - 1][i][j]

                # if i == 32 and j == 44:
                #     print("step", step, "prev sum", sum)

                # add last row
                for ii in range(i, i + step):
                    # if i == 32 and j == 44:
                    #     print(
                    #         "ii",
                    #         ii,
                    #         "j + step - 1",
                    #         j + step - 1,
                    #         grid[ii][j + step - 1],
                    #     )
                    sum += grid[ii][j + step - 1]

                # add last col (minus last elem)
                for jj in range(j, j + step - 1):
                    # if i == 32 and j == 44:
                    #     print(
                    #         "jj",
                    #         jj,
                    #         "i + step - 1",
                    #         i + step - 1,
                    #         grid[i + step - 1][jj],
                    #     )
                    sum += grid[i + step - 1][jj]

                # if i == 32 and j == 44:
                #     print("step", step, "sum", sum)

                sums[step][i].append(sum)
                # print("sum:", sum)
                if sum > max_sqr_sum:
                    max_sqr_sum = sum
                    max_sqr_x = i + 1
                    max_sqr_y = j + 1
                    max_sqr_size = step
                    print(
                        "(TMP) x:",
                        max_sqr_x,
                        "y:",
                        max_sqr_y,
                        "sum:",
                        max_sqr_sum,
                        "size:",
                        max_sqr_size,
                    )
    return (max_sqr_x, max_sqr_y, max_sqr_sum, max_sqr_size)


grid = create_grid(input)
(max_sqr_x, max_sqr_y, max_sqr_sum, max_sqr_size) = find_max_square(grid)
print("x:", max_sqr_x, "y:", max_sqr_y, "sum:", max_sqr_sum, "size:", max_sqr_size)
