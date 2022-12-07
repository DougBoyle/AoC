group = set()
groupCount = 0
total = 0

with open("day6.txt", "r") as f:
    line = f.readline()
    while len(line) > 0:
        line = line.strip()
        if len(line) == 0:
            total += len(group)
            group = set()
            groupCount = 0
        elif groupCount == 0:
            group = set(line)
            groupCount += 1
        else:
       #     group.update(set(line))
           group = group.intersection(set(line))
        line = f.readline()
    if len(group) > 0:
        total += len(group)

print(total)
