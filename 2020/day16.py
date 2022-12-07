import math
import re
from enum import Enum

class Region(Enum):
    FIELDS = 0
    MY_TICKET = 1
    OTHER_TICKETS = 2

def rangePair(match):
    return match.group(1), [
        (int(match.group(2)), int(match.group(3))),
        (int(match.group(4)), int(match.group(5)))
    ]

fieldPattern = "([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)"
fields = {}
region = Region.FIELDS

otherTickets = []

with open("day16.txt", "r") as f:
    line = f.readline()
    while len(line) > 0:
        line = line.strip()
        if line == "your ticket:":
            region = Region.MY_TICKET
        elif line == "nearby tickets:":
            region = Region.OTHER_TICKETS
        elif len(line) > 0:
            match region:
                case Region.FIELDS:
                    m = re.match(fieldPattern, line)
                    if m is not None:
                        field, ranges = rangePair(m)
                        fields[field] = ranges
                case Region.MY_TICKET:
                    myTicket = [int(x) for x in line.split(",")]
                case Region.OTHER_TICKETS:
                    otherTickets.append([int(x) for x in line.split(",")])
        line = f.readline()

def validForField(field, value):
    (a, b), (c, d) = field
    return value >= a and value <= b or value >= c and value <= d

def couldBeValid(value):
    for field in fields.values():
        if validForField(field, value):
            return True
    return False

def fieldValidForPosition(field, i):
    for ticket in validTickets:
        if not validForField(fields[field], ticket[i]):
            return False
    return True  

def ticketScanErrorRate():
    return sum([x if not couldBeValid(x) else 0
                for ticket in otherTickets
                for x in ticket])

validTickets = list(filter(lambda ticket: all([couldBeValid(x) for x in ticket]), otherTickets))

possibleFields = [list(fields.keys()) for _ in range(len(myTicket))]
actualFields = [None for _ in range(len(myTicket))]

# filter out fields for each position where some valid ticket doesn't match that field's range
for i in range(len(myTicket)):
    possibleFields[i] = list(filter(lambda field: fieldValidForPosition(field, i), possibleFields[i]))

changing = True
while changing:
    changing = False
    for i in range(len(myTicket)):
        # Only case, remove from all others and record as actual.
        # Technically a special case, could also look for two positions with same pair etc.
        if len(possibleFields[i]) == 1:
            changing = True
            actualFields[i] = possibleFields[i][0]
            for j in range(len(myTicket)):
                possibleFields[j] = list(filter(lambda field: field != actualFields[i], possibleFields[j]))


# print(ticketScanErrorRate())

product = 1
count = 0
for i in range(len(myTicket)):
    if actualFields[i].startswith("departure"):
        count += 1
        product *= myTicket[i]
print(count, product)

