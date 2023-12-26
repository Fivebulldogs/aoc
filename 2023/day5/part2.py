from collections import defaultdict
from itertools import pairwise

input = [
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]

input = None
with open("input.txt") as f:
    input = f.readlines()


def get_seed_ranges():
    initial_seeds = list(map(lambda x: int(x), input[0].split(": ")[1].split(" ")))
    seed_ranges = []
    for i in range(0, len(initial_seeds) - 1, 2):
        seed_start = initial_seeds[i]
        range_len = initial_seeds[i + 1]
        print(seed_start, range_len)
        seed_ranges.append((seed_start, seed_start + range_len - 1))
    seed_ranges.sort(key=lambda range: range[0])
    return seed_ranges


def create_maps(input):
    maps = defaultdict(list)
    map_name = ""
    for line in input[1:]:
        if len(line) == 0:
            continue
        if not line[0].isdigit():
            map_name = line.strip()[:-5]
        else:
            maps[map_name].append(list(map(lambda x: int(x), line.split(" "))))

    # sort maps on source
    for map_name, ranges in maps.items():
        # sort on the source start
        ranges.sort(key=lambda range: range[1])

    # insert zero offset ranges into maps and transform maps into something more readable
    # (source_start, source_end, destination_offset)
    new_maps = {}
    for map_name, ranges in maps.items():
        new_ranges = []
        for i, (destination_offset, source_start, range_len) in enumerate(ranges):
            if i == 0:
                # add initial zero offset range?
                if source_start > 0:
                    new_ranges.append((0, source_start - 1, 0))

            new_ranges.append(
                (source_start, source_start + range_len - 1, destination_offset)
            )
            if i < len(ranges) - 1:
                if source_start + range_len < ranges[i + 1][1]:
                    # insert 0 offset range
                    new_ranges.append(
                        (
                            source_start + range_len,
                            ranges[i + 1][1] - 1,
                            source_start + range_len,
                        )
                    )
            elif i == len(ranges) - 1:
                # add last zero offset range that ends very far away
                new_ranges.append(
                    (source_start + range_len, 1e10, source_start + range_len)
                )

        new_maps[map_name] = new_ranges
    return new_maps


maps = create_maps(input)

seed_ranges = get_seed_ranges()
print("seed_ranges", seed_ranges)
print()


def get_destination_ranges(source_ranges, mapped_ranges):
    destination_ranges = []
    for source_range_start, source_range_end in source_ranges:
        new_destination_ranges = []
        for mapped_range_start, mapped_range_end, dest_offset in mapped_ranges:
            offset = dest_offset - mapped_range_start
            print(
                f"source range, ({source_range_start}, {source_range_end}) | mapped range ({mapped_range_start}, {mapped_range_end}, {offset})"
            )

            if source_range_start >= mapped_range_start:
                if source_range_end <= mapped_range_end:
                    new_dest = (
                        offset + source_range_start,
                        offset + source_range_end,
                    )
                    print(f"entire source range is within map range => {new_dest}")
                    new_destination_ranges.append(new_dest)
                    break  # no need to keep looking in more mapped ranges
                elif source_range_start <= mapped_range_end:
                    new_dest = (
                        offset + source_range_start,
                        offset + mapped_range_end,
                    )
                    print(
                        f"start of source range is within map range, end of source range is outside map range (to the right) => {new_dest}"
                    )
                    new_destination_ranges.append(new_dest)
                else:
                    print("entire source range is after map range => None")
            elif source_range_end >= mapped_range_start:
                if source_range_end <= mapped_range_end:
                    new_dest = (
                        offset + mapped_range_start,
                        offset + source_range_end,
                    )
                    print(
                        f"start of source range is outside map range (to the left), end of source range is within map range => {new_dest}"
                    )
                    new_destination_ranges.append(new_dest)
                else:
                    new_dest = (
                        offset + mapped_range_start,
                        offset + mapped_range_start,
                    )
                    print(
                        f"start of source range is outside map range (to the left), end of source range is outside map range (to the right) => {new_dest}"
                    )
                    new_destination_ranges.append(new_dest)
        print("new destination ranges", new_destination_ranges)
        destination_ranges.extend(new_destination_ranges)
        print()
    return destination_ranges


print("seed-to-soil", maps["seed-to-soil"])
print()

soil_ranges = get_destination_ranges(seed_ranges, maps["seed-to-soil"])
print("soil_ranges", soil_ranges)
print()

print("soil-to-fertilizer", maps["soil-to-fertilizer"])
fertilizer_ranges = get_destination_ranges(soil_ranges, maps["soil-to-fertilizer"])
print("fertilizer_ranges", fertilizer_ranges)
print()

print("fertilizer-to-water", maps["fertilizer-to-water"])
water_ranges = get_destination_ranges(fertilizer_ranges, maps["fertilizer-to-water"])
print("water_ranges", water_ranges)
print()

print("water-to-light", maps["water-to-light"])
light_ranges = get_destination_ranges(water_ranges, maps["water-to-light"])
print("light_ranges", light_ranges)
print()

print("light-to-temperature", maps["light-to-temperature"])
temperature_ranges = get_destination_ranges(light_ranges, maps["light-to-temperature"])
print("temperature_ranges", temperature_ranges)
print()

print("temperature-to-humidity", maps["temperature-to-humidity"])
humidity_ranges = get_destination_ranges(
    temperature_ranges, maps["temperature-to-humidity"]
)
print("humidity_ranges", humidity_ranges)
print()

print("humidity-to-location", maps["humidity-to-location"])
location_ranges = get_destination_ranges(humidity_ranges, maps["humidity-to-location"])
print("location_ranges", location_ranges)
print()

min_val = 1e10
for location_range in location_ranges:
    if location_range[0] < min_val:
        min_val = location_range[0]
print(min_val)
