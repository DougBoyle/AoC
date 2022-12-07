from collections import deque
# In this case, technically two linked lists through the
# same elements may be most efficient, where one is by
# insertion order and the other by sorted order.
buffer = deque()

def findPair(n):
    for i in range(25):
        for j in range(i + 1, 25):
            if buffer[i] + buffer[j] == n:
                return True
    return False

with open("day9.txt", "r") as f:
    data = [int(line.strip()) for line in f.readlines()]

# preamble
for i in range(25):
    buffer.append(int(data[i]))
# find the invalid value
invalid = None
for n in data[25:]:
    if not findPair(n):
        invalid = n
        break
    buffer.append(n)
    buffer.popleft()

print(invalid)

# find the sequence of numbers (at least 2) that sum to invalid
start = 0
end = 1
total = data[start] + data[end]
while total != invalid:
    # must progress end if no other numbers between them
    if start + 1 == end or total < invalid: 
        end += 1
        total += data[end]
    elif total > invalid:
        total -= data[start]
        start += 1

# guessed 15538721 - too low

print(min(data[start:end+1]) + max(data[start:end+1]))


