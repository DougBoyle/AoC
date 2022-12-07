with open("day5.txt", "r") as f:
    data = f.readlines()


def getID(seat):
    tot = 0
    for char in seat:
        tot *= 2
        if char == "B" or char == "R":
            tot += 1
    return tot

seats = sorted([getID(line.strip()) for line in data])

for i in range(len(seats)):
    if seats[i+1] - seats[i] != 1:
        print(seats[i] + 1)
        break
