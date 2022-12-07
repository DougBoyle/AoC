import re

with open("day2.txt", "r") as f:
    data = f.readlines()
data = [x.strip() for x in data]

def testLine(line):
    result = re.search(r"(\d+)-(\d+) ([a-z]): ([a-z]+)", line)
    minim = int(result.group(1))
    maxim = int(result.group(2))
    char = result.group(3)
    pswd = result.group(4)
    count = pswd.count(char)
    return count >= minim and count <= maxim

# print(sum([testLine(line) for line in data]))


def testLine2(line):
    result = re.search(r"(\d+)-(\d+) ([a-z]): ([a-z]+)", line)
    first = int(result.group(1))
    second = int(result.group(2))
    char = result.group(3)
    pswd = result.group(4)
    count = 0
    if pswd[first - 1] == char:
        count += 1
    if pswd[second - 1] == char:
        count += 1
    return count == 1

print(sum([testLine2(line) for line in data]))
