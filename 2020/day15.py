numbers = [2,20,0,4,1,17]

lastSaid = {}
gap = {}

for turn in range(1, 30000001):
    if turn <= len(numbers):
        number = numbers[turn - 1]
    else:
        number = gap[number]

    if number not in lastSaid:
        gap[number] = 0
    else:
        gap[number] = turn - lastSaid[number]
    lastSaid[number] = turn
    if turn % 1000000 == 0:
        print("turn {0} = {1}".format(turn, number))
    
print(number)
