with open("day1.txt", "r") as f:
    data = f.readlines()
data = [int(x.strip()) for x in data]


data.sort()

def findTwo(start, end, target):
    start = 0
    end = len(data) - 1
    while end > start:
        v1 = data[start]
        v2 = data[end]
        total = v1 + v2
        if total == target:
            return v1 * v2
        elif total > target:
            end -= 1
        else:
            start += 1

def solveTwo():
    print(findTwo(0, len(data)-1, 2020))

def findThree():
    for i in range(0, len(data) - 2):
        v = data[i]
        product = findTwo(i+1, len(data)-1, 2020 - v)
        if product is not None:
            print(v * product)
            return

findThree()
