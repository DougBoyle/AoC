import re
from enum import Enum

COMMAND = "([NESWLRF])(\d+)"

class Direction(Enum):
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    
    def turnRight(self, angle):
        if angle % 90 != 0:
            raise "Expect turns to be multiples of 90 degrees"
        return Direction.directions[int(
            (Direction.directions.index(self) + angle/90) % 4
        )]
    def turnLeft(self, angle):
        return self.turnRight(-angle)
    def move(self, position, steps):
        return (position[0] + self.value[0]*steps, position[1] + self.value[1]*steps)

Direction.directions = [
    Direction.NORTH,
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST
]

def part1():
    position = (0, 0)
    direction = Direction.EAST

    with open("day12.txt", "r") as f:
        for line in f.readlines():
            m = re.match(COMMAND, line.strip())
            value = int(m.group(2))
            match m.group(1):
                case "N":
                    position = Direction.NORTH.move(position, value)
                case "E":
                    position = Direction.EAST.move(position, value)
                case "S":
                    position = Direction.SOUTH.move(position, value)
                case "W":
                    position = Direction.WEST.move(position, value)
                case "L":
                    direction = direction.turnLeft(value)
                case "R":
                    direction = direction.turnRight(value)
                case "F":
                    position = direction.move(position, value)

    print(abs(position[0]) + abs(position[1]))

### part 2

def rotateClockwise(position, angle):
    if angle % 90 != 0:
        raise "Expect turns to be multiples of 90 degrees"
    clockwiseTurns = int((angle/90) % 4)
    newPosition = position
    while clockwiseTurns > 0:
        newPosition = (newPosition[1], -newPosition[0])
        clockwiseTurns -= 1
    return newPosition

def part2():
    position = (0, 0)
    waypoint = (10, 1)
    with open("day12.txt", "r") as f:
        for line in f.readlines():
            m = re.match(COMMAND, line.strip())
            value = int(m.group(2))
            match m.group(1):
                case "N":
                    waypoint = Direction.NORTH.move(waypoint, value)
                case "E":
                    waypoint = Direction.EAST.move(waypoint, value)
                case "S":
                    waypoint = Direction.SOUTH.move(waypoint, value)
                case "W":
                    waypoint = Direction.WEST.move(waypoint, value)
                case "L":
                    waypoint = rotateClockwise(waypoint, -value)
                case "R":
                    waypoint = rotateClockwise(waypoint, value)
                case "F":
                    position = (
                            position[0] + waypoint[0]*value,
                            position[1] + waypoint[1]*value
                        )
    print(abs(position[0]) + abs(position[1]))
part2() # too big




