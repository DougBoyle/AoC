import numpy as np
from enum import Enum
import re

class Op(Enum):
    PLUS = 1,
    TIMES = 2

def readDigit(line, start):
    index = start + 1
    while index < len(line) and line[index].isdigit():
        index += 1
    return int(line[start:index]), index

def processNum(n, stack):
    if stack[-1] is None:
        stack[-1] = n
    else: # apply to previous number/operator
        m, op = stack.pop()
        match op:
            case Op.PLUS:
                n = m + n
            case Op.TIMES:
                n = m * n
        stack.append(n)

def evaluate(line):
    stack = [None]
    position = 0
    while position < len(line):
        if line[position] == " ":
            position += 1
        elif line[position].isdigit():
            n, position = readDigit(line, position)
            processNum(n, stack)
        elif line[position] == "+":
            n = stack.pop()
            stack.append((n, Op.PLUS))
            position += 1
        elif line[position] == "*":
            n = stack.pop()
            stack.append((n, Op.TIMES))
            position += 1
        elif line[position] == "(":
            stack.append(None)
            position += 1
        elif line[position] == ")":
            n = stack.pop()
            processNum(n, stack)
            position += 1
        else:
            raise Exception("Unexpected symbol " + line[position])
    if len(stack) != 1:
        raise Exception("Incomplete expression")
    return stack[0]

#### Part 2 ####

class Token(Enum):
    PLUS = 1,
    TIMES = 2,
    OPEN = 3,
    CLOSE = 4,
    NUM = 5,
    END = 6

    def __str__(self):
        match self:
            case Token.PLUS:
                return "+"
            case Token.TIMES:
                return "*"
            case Token.OPEN:
                return "("
            case Token.CLOSE:
                return ")"
            case Token.NUM:
                return ""
            case Token.END:
                return "."

# Need some record of state (i.e. compilers state machine)
# Stack IS the state, when * seen, and [..., (n, op), m] on stack, compress.
# Done whenever next op is * or END
def squashMultiplies(stack):
    while len(stack) >= 2 and stack[-1][1] is None and stack[-2][1] is Token.TIMES:
        n, _ = stack.pop()
        m, _ = stack.pop()
        stack.append((n*m, None))


def processNum2(n, stack):
    if len(stack) == 0 or stack[-1][1] == Token.OPEN:
        stack.append((n, None))
    else: # apply to previous number/operator
        m, op = stack[-1]
        match op:
            case Token.PLUS: # evaluate immediately
                stack[-1] = (m + n, None)
            case Token.TIMES:
                stack.append((n, None)) # will get squashed later

def nextToken(line, position):
    while position < len(line):
        if line[position] == " ":
            position += 1
        elif line[position].isdigit():
            n, position = readDigit(line, position)
            return Token.NUM, position, n
        elif line[position] == "+":
            return Token.PLUS, position + 1, None
        elif line[position] == "*":
            return Token.TIMES, position + 1, None
        elif line[position] == "(":
            return Token.OPEN, position + 1, None
        elif line[position] == ")":
            return Token.CLOSE, position + 1, None
        else:
            raise Exception("Unexpected symbol " + line[position])
    return Token.END, position, None

def evaluate2(line):
    stack = []
    token, position, value = nextToken(line, 0)
    while token != Token.END:
        match token:
            case Token.PLUS:
                n, _ = stack.pop()
                stack.append((n, Token.PLUS))
            case Token.TIMES:
                squashMultiplies(stack)
                n, _ = stack.pop()
                stack.append((n, Token.TIMES))
            case Token.OPEN:
                stack.append((None, Token.OPEN))
            case Token.CLOSE:
                squashMultiplies(stack)
                n, _ = stack.pop()
                stack.pop() # remove the OPEN
                processNum2(n, stack)
            case Token.NUM:
                processNum2(value, stack)
        token, position, value = nextToken(line, position)
    squashMultiplies(stack)
    if len(stack) != 1:
        raise Exception("Incomplete expression")
    return stack[0][0]

with open("day18.txt", "r") as f:
    total = 0
    for line in f.readlines():
        total += evaluate2(line.strip())
print(total)


