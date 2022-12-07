with open("day10.txt", "r") as f:
    data = [int(line.strip()) for line in f.readlines()]

data.append(0) # the outlet

data.sort()

gap1count = 0
gap2count = 0
gap3count = 0

deltas = [data[i] - data[i-1] for i in range(1, len(data))]
gap1count = deltas.count(1)
gap2count = deltas.count(2)
gap3count= deltas.count(3)

if gap1count + gap2count + gap3count != len(data) - 1:
    print("Error, full chain not possible")

gap3count += 1 # the device itself
print(gap1count * gap3count)

### Part 2 ###
combinations = {0:1}
for n in data[1:]:
    tot = 0
    if n-3 in combinations:
        tot += combinations[n-3]
    if n-2 in combinations:
        tot += combinations[n-2]
    if n-1 in combinations:
        tot += combinations[n-1]
    combinations[n] = tot

# number of ways of making largest adapter = ways of connecting to final device
# (which is largest adapter + 3)
print(combinations[data[-1]])
