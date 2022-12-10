import numpy as np
from enum import Enum
import re
import time

def priority(c):
    if c >= 'a' and c <= 'z':
        return 1 + ord(c) - ord('a')
    else:
        return 27 + ord(c) - ord('A')

def part1():
    total = 0
    with open("day3.txt") as f:
        for line in f.readlines():
            line = line.strip()
            size = len(line)//2
            pt1 = line[:size]
            pt2 = line[size:]
            for char in pt1:
                if char in pt2:
                    total += priority(char)
                    break
    print(total)

def part2():
    total = 0
    with open("day3.txt") as f:
        i = 0
        for line in f.readlines():
            line = line.strip()
            i = (i+1)%3
            if i == 1:
                elf1 = line
            elif i == 2:
                elf2 = line
            else:
                for char in line:
                    if char in elf1 and char in elf2:
                        total += priority(char)
                        break
    print(total)


