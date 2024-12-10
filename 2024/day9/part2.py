from collections import deque
from dataclasses import dataclass


def read_file(filename):
    with open(filename) as f:
        return f.readline().strip() 

disk_map = read_file("input")
# disk_map = "2333133121414131402"

q = deque()

@dataclass
class Node:
    id: int
    count: int

ptr = 0
file_id = 0
while ptr < len(disk_map):
    block_count = int(disk_map[ptr])
    ptr += 1
    empty_count = int(disk_map[ptr]) if ptr < len(disk_map) else 0
    
    q.append(Node(id=file_id, count=block_count))
    if empty_count > 0:
        q.append(Node(id=-1, count=empty_count))

    ptr += 1
    file_id += 1

curr_id = file_id - 1
while curr_id >= 0:
    lq = deque()
    rq = deque()
    try:
        try:
            vr = q.pop()
            while vr.id != curr_id:
                rq.appendleft(vr)
                vr = q.pop()
        except Exception:
            print("why")
        
        try:
            vl = q.popleft()
            while vl.id >= 0 or vl.count < vr.count:
                lq.append(vl)
                vl = q.popleft()
        except Exception:
            # no empty space found, join queues into one
            print("no empty space found for", curr_id)
            rq.appendleft(vr)
            lq.extend(q)
            lq.extend(rq)
            q = lq.copy()
            curr_id -= 1
            continue

        # we found an empty space vl to fit vr!
        lq.append(vr)
        if vl.count > vr.count:
            # append any remaining empty space
            lq.append(Node(id=-1, count=vl.count - vr.count))
        # fill the hole after moving vr            
        rq.appendleft(Node(id=-1, count=vr.count))

        # join lq and rq
        lq.extend(q)
        lq.extend(rq)
        q = lq.copy()

        curr_id -= 1
    except Exception:
        print("Exception for curr_id", curr_id)
        break

# print("curr_id", curr_id)
# while True:
#     print(q.popleft())

result = 0
i = 0
while True:
    try:
        v = q.popleft()
        if v.id < 0:
            i += v.count
            continue
        for j in range(v.count):
            print(i, v.id)
            result += i * v.id
            i += 1
    except IndexError:
        print("oh", i)
        break
print("result", result)