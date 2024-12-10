from collections import deque


def read_file(filename):
    with open(filename) as f:
        return f.readline().strip() 

disk_map = read_file("input")
# disk_map = "2333133121414131402"

q = deque()

ptr = 0
file_id = 0
while ptr < len(disk_map):
    block_count = int(disk_map[ptr])
    ptr += 1
    empty_count = int(disk_map[ptr]) if ptr < len(disk_map) else 0
    
    for i in range(block_count):
        q.append(file_id)
        
    for i in range(empty_count):
        q.append(".")

    ptr += 1
    file_id += 1

ok_disk_map = []
while True:
    try:
        vl = q.popleft()
        if vl != ".":
            # print("popping left and appending", vl)
            ok_disk_map.append(vl)
        else:
            vr = q.pop()
            while vr == ".":
                # print("popping . from right")
                vr = q.pop()
            # print("popping right and appending", vr)
            ok_disk_map.append(vr)
    except Exception:
        break
print()
print(ok_disk_map)
result = 0
for i, v in enumerate(ok_disk_map):
    print(i, v, i*v)
    result += i * v
print("result", result)