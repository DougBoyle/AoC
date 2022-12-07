with open("day3.txt", "r") as f:
    data = f.readlines()
maxLen = len(data[0].strip())

def checkSlope(steps, down = 1):
    x = 0
    count = 0
    for line in data[down::down]:
        x = (x + steps) % maxLen
        if line[x] == "#":
            count += 1
    return count

print(checkSlope(1) * checkSlope(3) * checkSlope(5) * checkSlope(7)
      * checkSlope(1,2))
        
