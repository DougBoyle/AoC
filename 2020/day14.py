import math
import re
from enum import Enum

class Command(Enum):
    MASK = 0
    MEM = 1

    def __init__(self, value, address=None):
        self.number = value
        self.address = address

maskPattern = "mask = ([X01]{36})"
memPattern = "mem\[(\d+)\] = (\d+)"

mask = "X"*36
memory = {}

def asBin36(value):
    s = bin(value)[2:] # 0b...
    if len(s) < 36:
        s = (36 - len(s))*"0" + s
    elif len(s) > 36:
        s = s[len(s)-36:]
    return s

def applyMask(mask, value):
    s = asBin36(value)
    result = 0
    for i in range(36):
        result *= 2
        match mask[i]:
            case "X":
                result += int(s[i])
            case "0":
                pass
            case "1":
                result += 1
    return result

def part1():
    with open("day14.txt", "r") as f:
        line = f.readline()
        while len(line) > 0:
            line = line.strip()
            m = re.match(maskPattern, line)
            if m is not None:
                mask = m.group(1)
                line = f.readline()
                continue
            
            m = re.match(memPattern, line)
            if m is not None:
                updateMemory(mask, int(m.group(1)), int(m.group(2)))
                line = f.readline()
                continue

            raise Exception("Command not recognised " + line)


def updateMemory(mask, address, value):
    s = asBin36(address)
    # apply all 1s, leave Xs as 0
    address2 = 0
    for i in range(36):
        address2 *= 2
        match mask[i]:
            case "X":
                pass
            case "0":
                address2 += int(s[i])
            case "1":
                address2 += 1
    # now recursively find all addresses to update
    # if no Xs anywhere, only this initial address written to
    memory[address2] = value
    updateAllAddresses(mask, address2, value, 0)

def updateAllAddresses(mask, address, value, i):
    if i == 36:
        return
    elif mask[i] != "X":
        return updateAllAddresses(mask, address, value, i+1)
    else:
        updateAllAddresses(mask, address, value, i + 1)
        # 1 inserted, write to new address and check for any other chanegs
        address |= 1 << (35 - i)
        memory[address] = value
        updateAllAddresses(mask, address, value, i + 1)

def part2():
    with open("day14.txt", "r") as f:
        line = f.readline()
        while len(line) > 0:
            line = line.strip()
            m = re.match(maskPattern, line)
            if m is not None:
                mask = m.group(1)
                line = f.readline()
                continue
            
            m = re.match(memPattern, line)
            if m is not None:
                updateMemory(mask, int(m.group(1)), int(m.group(2)))
                line = f.readline()
                continue

            raise Exception("Command not recognised " + line)

part2()

total = 0
for address in memory:
    total += memory[address]
print(total)

