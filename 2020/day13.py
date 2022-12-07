import math

def part1():
    with open("day13.txt", "r") as f:
        startTime = int(f.readline().strip())
        frequencies = [int(s) for s in filter(
            lambda s: s != "x",
            f.readline().strip().split(",")
        )]

    firstAvailable = [
      math.ceil(startTime/n)*n for n in frequencies  
    ]

    earliest = min(firstAvailable)
    earliestId = frequencies[firstAvailable.index(earliest)]

    print((earliest - startTime) * earliestId)

### Part 2 ###
## t = solution
## frequencies f0 ... fn
## multiplies m0 ... mn
## # can just treat x's as 1/ignore
##
## t = m0 * f0 = m1 * f1 - 1 = m2 * f2 - 2
## m1 * f1 - m0 * f0 = 1 # can be efficiently solved by extended gcd(f1, f0)
## # That gives earliest time for those 2, can then find how often it repeats
## t = r1 + m1 * q1 = m2 * f2 - 2 = ...
## # Can arrange the same again:
## m2 * f2 - m1 * q1 = 2 - r1
## RHS must always be a multiple of left, only challenge is ensuring it is least

# At any point, from egcd(a, b, 1, 0, 0, 1):
# a = a0*m + a1*n, b = b0*m + b1*n
# e.g. egcd(26, 15) = (1, -4.0, 7.0) --> 15 * 7 - 26 * 4 = 1
def egcdHelp(m, n, a0, a1, b0, b1):
    if m < n:
        m, n = n, m
        a0, a1, b0, b1 = b0, b1, a0, a1
    while n != 0:
        r = m % n
        q = (m - r) // n
        m, n = n, r
        # m' = n
        # n' = r = m - q*n
        a0, a1, b0, b1 = b0, b1, a0 - q*b0, a1 - q*b1
    return (m, a0, a1)

def egcd(m, n):
    return egcdHelp(m, n, 1, 0, 0, 1)

def lcm(m, n):
    return (m * n) // egcd(m, n)[0]

with open("day13.txt", "r") as f:
    f.readline()
    buses = f.readline().strip().split(",")
 #   buses = testInput.strip().split(",")
sequence = []
index = 0
for frequency in buses:
    if frequency != "x":
        sequence.append((index, int(frequency)))
    index += 1

print(sequence)

while len(sequence) > 1:
    # t + d0 = m0 * f0, t + d1 = m1 * f1
    # d1 - d0 = (-m0) * f0 + m1 * f1
    d0, f0 = sequence.pop()
    d1, f1 = sequence.pop()
    g, m0, m1 = egcd(f0, f1)
    stepSize = lcm(f0, f1)
    multiplier = (d1 - d0)//g
    t = -m0 * multiplier * f0 - d0
    print(t)
    # looks awful but ensures always integer arithmetic
    if t < 0:
        t += (-t//stepSize)*stepSize
    while t < 0:
        t += stepSize
    sequence.append((-t, stepSize))
  
print(-sequence[0][0])

