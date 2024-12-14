from collections import deque
from dataclasses import dataclass, field
from operator import itemgetter


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
    vertical_sides: list[set] = field(default_factory=list)
    horizontal_sides: list[set] = field(default_factory=list)

    def add_vertical_side_pos(self, new_pos):
        neighbor_sides = []
        other_sides = []
        for side in self.vertical_sides:
            for pos in side:
                # direction and col is same and rows are next to each other
                is_neighbor_side = False
                if (
                    new_pos[2] == pos[2]
                    and new_pos[1] == pos[1]
                    and abs(new_pos[0] - pos[0]) == 1
                ):
                    neighbor_sides.append(side)
                    is_neighbor_side = True
                    break
            if not is_neighbor_side:
                other_sides.append(side)

        vertical_sides = other_sides
        if len(neighbor_sides) > 0:
            merged_neighbor_sides = set()
            for side in neighbor_sides:
                merged_neighbor_sides = merged_neighbor_sides.union(side)
            merged_neighbor_sides.add(new_pos)
            vertical_sides.append(merged_neighbor_sides)
        else:
            new_side = set()
            new_side.add(new_pos)
            vertical_sides.append(new_side)

        self.vertical_sides = vertical_sides

    def add_horizontal_side_pos(self, new_pos):
        neighbor_sides = []
        other_sides = []
        for side in self.horizontal_sides:
            for pos in side:
                # direction and row is same and cols are next to each other
                is_neighbor_side = False
                if (
                    new_pos[2] == pos[2]
                    and new_pos[0] == pos[0]
                    and abs(new_pos[1] - pos[1]) == 1
                ):
                    neighbor_sides.append(side)
                    # print(side, "is neighbor to new pos", new_pos)
                    is_neighbor_side = True
                    break
            if not is_neighbor_side:
                # print("Region", self.val, "other side", side)
                other_sides.append(side)

        horizontal_sides = other_sides
        if len(neighbor_sides) > 0:
            merged_neighbor_sides = set()
            for side in neighbor_sides:
                merged_neighbor_sides = merged_neighbor_sides.union(side)
            merged_neighbor_sides.add(new_pos)
            horizontal_sides.append(merged_neighbor_sides)
        else:
            new_side = set()
            new_side.add(new_pos)
            horizontal_sides.append(new_side)

        self.horizontal_sides = horizontal_sides

    def __hash__(self):
        return hash(id)


lines = read_file("input")
region_id = 0
pos_to_region = {}
all_visited = set()

for i, line in enumerate(lines):
    for j, val in enumerate(line):
        if (i, j) in all_visited:
            continue

        region: Region = pos_to_region.get((i, j))
        if not region:
            region = Region(region_id, val, 0)
            pos_to_region[(i, j)] = region
            region_id += 1

        q = deque()
        q.append((i, j))
        visited = set()

        while True:
            try:
                (row, col) = q.pop()
                if (row, col) in visited:
                    continue

                region.plot_count += 1

                visited.add((row, col))
                all_visited.add((row, col))

                if row > 0:
                    if lines[row - 1][col] == val:
                        if (row - 1, col) not in visited:
                            q.append((row - 1, col))
                            pos_to_region[(row - 1, col)] = region
                    else:
                        region.add_horizontal_side_pos((row - 1, col, "U"))
                else:
                    region.add_horizontal_side_pos((row - 1, col, "U"))

                if row < len(lines) - 1:
                    if (row + 1, col) not in visited:
                        # check plot below
                        if lines[row + 1][col] == val:
                            q.append((row + 1, col))
                            pos_to_region[(row + 1, col)] = region
                        else:
                            region.add_horizontal_side_pos((row + 1, col, "D"))
                else:
                    region.add_horizontal_side_pos((row + 1, col, "D"))
                if col > 0:
                    if (row, col - 1) not in visited:
                        # check to the left
                        if lines[row][col - 1] == val:
                            q.append((row, col - 1))
                            pos_to_region[(row, col - 1)] = region
                        else:
                            region.add_vertical_side_pos((row, col - 1, "L"))
                else:
                    region.add_vertical_side_pos((row, col - 1, "L"))

                if col < len(line) - 1:
                    if (row, col + 1) not in visited:
                        # check plot below
                        if lines[row][col + 1] == val:
                            q.append((row, col + 1))
                            pos_to_region[(row, col + 1)] = region
                        else:
                            region.add_vertical_side_pos((row, col + 1, "R"))
                else:
                    region.add_vertical_side_pos((row, col + 1, "R"))
            except IndexError:
                break

price = 0
for region in set(pos_to_region.values()):
    # sort by rows, cols
    side_count = len(region.vertical_sides) + len(region.horizontal_sides)
    price += region.plot_count * side_count

print("price", price)
