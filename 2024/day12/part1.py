from collections import defaultdict, deque
from dataclasses import dataclass

def read_file(filename):
    lines = []
    with open(filename) as f:
        line = f.readline().strip() 
        while line:
            lines.append(line)
            line = f.readline().strip() 
    return lines

@dataclass
class Region:
    id: int = 0
    val: str = ""
    plot_count: int = 0
    perimeter: int = 0

    def __hash__(self):
        return hash(id)

lines = read_file("input")
region_id = 0
pos_to_region = {}
all_visited = set()

for i, line in enumerate(lines):
    for j, val in enumerate(line):           
        if (i, j) in all_visited:
            # print("loop node", i, j, val, "in all_visited, skipping")
            continue

        region: Region = pos_to_region.get((i, j))
        if not region:
            region = Region(region_id, val, 0)
            pos_to_region[(i, j)] = region
            region_id += 1

        # print()
        # print("Region id/val", region.id, region.val)

        q = deque()
        q.append((i, j))
        # print("Pushing 'loop' node", (i, j))
        visited = set()

        while True:
            try:
                (row, col) = q.pop()
                # print()
                # print("Popped ", row, col, ":", val)
                if (row, col) in visited:
                    # print(row, col, "in visited")
                    continue

                region.plot_count += 1
                # print("Region", region.val, " plot count", region.plot_count)
                
                visited.add((row, col))
                all_visited.add((row, col))
                # print(visited)

                if row > 0:
                    if lines[row-1][col] == val:
                        if (row-1, col) not in visited:
                            # print("Pushed", row-1, col)
                            q.append((row-1, col))
                            pos_to_region[(row-1, col)] = region
                    else:
                        # print("Adding perimeter above, ", lines[row-1][col])
                        region.perimeter += 1
                else:
                    # print("Adding perimeter above, outside")
                    region.perimeter += 1

                if row < len(lines) - 1:
                    if (row+1, col) not in visited:
                        # check plot below
                        if lines[row+1][col] == val:
                            # print("Pushed", row+1, col)
                            q.append((row+1, col))
                            pos_to_region[(row+1, col)] = region
                        else:
                            # print("Adding perimeter below,", lines[row+1][col])
                            region.perimeter += 1
                else:
                    # print("Adding perimeter below, outside")
                    region.perimeter += 1
                if col > 0:
                    if (row, col-1) not in visited:
                        # check to the left
                        if lines[row][col-1] == val:
                            # print("Pushed", row, col-1)
                            q.append((row, col-1))
                            pos_to_region[(row, col-1)] = region
                        else:
                            # print("Adding perimeter left,", lines[row][col-1])
                            region.perimeter += 1
                else:
                    # print("Adding perimeter left, outside")
                    region.perimeter += 1

                if col < len(line) - 1:
                    if (row, col+1) not in visited:
                        # check plot below
                        if lines[row][col+1] == val:
                            # print("Pushed", row, col+1)
                            q.append((row, col+1))
                            pos_to_region[(row, col+1)] = region
                        else:
                            # print("Adding perimeter right,", lines[row][col+1])
                            region.perimeter += 1
                else:
                    # print("Adding perimeter right, outside")
                    region.perimeter += 1
            except IndexError:
                break

price = 0
print()
for region in set(pos_to_region.values()):
    # print("Region", region.val, region.plot_count, region.perimeter)
    price += region.plot_count * region.perimeter
print("price", price)