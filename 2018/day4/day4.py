def read_file(filename):
    lines = []
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return lines


def parse_lines(lines):
    result = []
    for line in lines:
        timestamp_info = line.split("] ")
        date_minute = timestamp_info[0][1:].split(" ")
        result.append(
            {
                "id": timestamp_info[1].split("#")[1].split(" ")[0]
                if "#" in timestamp_info[1]
                else "",
                "date": date_minute[0],
                "minute": date_minute[1],
                "info": timestamp_info[1],
            }
        )
    return sorted(result, key=lambda x: (x["date"], x["minute"]))


lines = read_file("input.txt")
entries = parse_lines(lines)
guard_sleep_times = {}
guard_id = None
asleep_minute = None
for entry in entries:
    if entry["id"]:
        guard_id = entry["id"]
        # print("guard", guard)
    elif entry["info"] == "falls asleep":
        asleep_minute = int(entry["minute"].split(":")[1])
        # print("asleep_minute", asleep_minute)
    elif entry["info"] == "wakes up":
        guard_sleep_time = guard_sleep_times.get(guard_id)
        if not guard_sleep_time:
            guard_sleep_times[guard_id] = {"total": 0, "minute_count": {}}
        wake_minute = int(entry["minute"].split(":")[1])
        # print("wake_minute", wake_minute)
        guard_sleep_times[guard_id]["total"] += wake_minute - asleep_minute
        for minute in range(asleep_minute, wake_minute):
            if guard_sleep_times[guard_id]["minute_count"].get(minute) is None:
                guard_sleep_times[guard_id]["minute_count"][minute] = 1
            else:
                guard_sleep_times[guard_id]["minute_count"][minute] += 1
    # guard_sleep_times
    # print(entry)
guard_with_most_sleep_time = sorted(
    guard_sleep_times.items(), key=lambda v: -v[1]["total"]
)[0]
print(guard_with_most_sleep_time)
guards_asleep_minutes = sorted(
    guard_with_most_sleep_time[1]["minute_count"].items(), key=lambda v: -v[1]
)
# print(guards_asleep_minutes)
guards_most_asleep_minute = guards_asleep_minutes[0][0]
print("guards_most_asleep_minute:", guards_most_asleep_minute)
print("result:", int(guard_with_most_sleep_time[0]) * guards_most_asleep_minute)
# 1823 too low
