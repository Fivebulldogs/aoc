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
    elif entry["info"] == "falls asleep":
        asleep_minute = int(entry["minute"].split(":")[1])
    elif entry["info"] == "wakes up":
        guard_sleep_time = guard_sleep_times.get(guard_id)
        if not guard_sleep_time:
            guard_sleep_times[guard_id] = {"total": 0, "minute_count": {}}
        wake_minute = int(entry["minute"].split(":")[1])
        guard_sleep_times[guard_id]["total"] += wake_minute - asleep_minute
        for minute in range(asleep_minute, wake_minute):
            if guard_sleep_times[guard_id]["minute_count"].get(minute) is None:
                guard_sleep_times[guard_id]["minute_count"][minute] = 1
            else:
                guard_sleep_times[guard_id]["minute_count"][minute] += 1

for g in guard_sleep_times.items():
    g[1]["minute_count"] = sorted(g[1]["minute_count"].items(), key=lambda v: -v[1])


guards_sorted_on_minute_freq = sorted(
    guard_sleep_times.items(), key=lambda v: -v[1]["minute_count"][0][1]
)
print(
    "result:",
    int(guards_sorted_on_minute_freq[0][0])
    * guards_sorted_on_minute_freq[0][1]["minute_count"][0][0],
)
