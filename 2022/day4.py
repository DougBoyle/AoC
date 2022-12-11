import numpy as np
from enum import Enum
import re
import time

def part1():
    redundant = 0

    with open("day4.txt") as f:
        for line in f.readlines():
            line = line.strip()
            segments = line.split(",")
            start1, end1 = (int(x) for x in segments[0].split("-"))
            start2, end2 = (int(x) for x in segments[1].split("-"))
            if (start1 <= start2 and end1 >= end2
                or start2 <= start1 and end2 >= end1):
                redundant += 1

    print(redundant)

def part2():
    overlap = 0

    with open("day4.txt") as f:
        for line in f.readlines():
            line = line.strip()
            segments = line.split(",")
            start1, end1 = (int(x) for x in segments[0].split("-"))
            start2, end2 = (int(x) for x in segments[1].split("-"))
            if (start1 <= start2 and start2 <= end1
                or start2 <= start1 and start1 <= end2):
                overlap += 1

    print(overlap)
