from collections import defaultdict


input = None
with open("input.txt") as f:
    input = f.readlines()

# input = [
#     "seeds: 79 14 55 13",
#     "",
#     "seed-to-soil map:",
#     "50 98 2",
#     "52 50 48",
#     "",
#     "soil-to-fertilizer map:",
#     "0 15 37",
#     "37 52 2",
#     "39 0 15",
#     "",
#     "fertilizer-to-water map:",
#     "49 53 8",
#     "0 11 42",
#     "42 0 7",
#     "57 7 4",
#     "",
#     "water-to-light map:",
#     "88 18 7",
#     "18 25 70",
#     "",
#     "light-to-temperature map:",
#     "45 77 23",
#     "81 45 19",
#     "68 64 13",
#     "",
#     "temperature-to-humidity map:",
#     "0 69 1",
#     "1 0 69",
#     "",
#     "humidity-to-location map:",
#     "60 56 37",
#     "56 93 4",
# ]

seeds = list(map(lambda x: int(x), input[0].split(": ")[1].split(" ")))
# print(seeds)

maps = defaultdict(list)
map_name = ""
for line in input[1:]:
    if len(line) == 0:
        continue
    if not line[0].isdigit():
        map_name = line.strip()[:-5]
    else:
        maps[map_name].append(list(map(lambda x: int(x), line.split(" "))))


def lookup(maps, map_name, sources):
    destinations = {}
    for source in sources:
        destination = None
        for dest_start, source_start, range in maps[map_name]:
            if source == 7535297:
                print(dest_start, source_start, range, "|", source + range)
            if source >= source_start and source <= source_start + range:
                destination = dest_start + (source - source_start)
                destinations[source] = destination
                break
        if destination is None:
            destinations[source] = source
    return destinations


# print(maps)

seed_to_soils = lookup(maps, "seed-to-soil", seeds)
# print("seed_to_soils", seed_to_soils)

soil_to_fertilizer = lookup(maps, "soil-to-fertilizer", seed_to_soils.values())
print("soil_to_fertilizer", soil_to_fertilizer)

fertilizer_to_water = lookup(maps, "fertilizer-to-water", soil_to_fertilizer.values())
# print("fertilizer_to_water", fertilizer_to_water)

water_to_light = lookup(maps, "water-to-light", fertilizer_to_water.values())
# print("water_to_light", water_to_light)

light_to_temperature = lookup(maps, "light-to-temperature", water_to_light.values())
# print("light_to_temperature", light_to_temperature)

temperature_to_humidity = lookup(
    maps, "temperature-to-humidity", light_to_temperature.values()
)
# print("temperature_to_humidity", temperature_to_humidity)

humidity_to_location = lookup(
    maps, "humidity-to-location", temperature_to_humidity.values()
)
# print("humidity_to_location", humidity_to_location)

print(min(humidity_to_location.values()))

# 7535297 too high
