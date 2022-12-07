import re
from enum import Enum

class Operation(Enum):
    ACC = 1
    JMP = 2
    NOP = 3

    @staticmethod
    def parse(s):
        match s:
            case "acc":
                return Operation.ACC
            case "jmp":
                return Operation.JMP
            case "nop":
                return Operation.NOP
            case _:
                raise "Operation " + s + " not recognised"

COMMAND = "acc|jmp|nop"
INSTRUCTION = "({0}) ([-+]\d+)".format(COMMAND)

class Instruction:
    def __init__(self, line):
        m = re.match(INSTRUCTION, line)
        self.op = Operation.parse(m.group(1))
        self.value = int(m.group(2))
        self.executed = False
        self.terminates = False

class Machine:
    def __init__(self, program):
        self.program = program
        self.pc = 0
        self.acc = 0
    def getNextInstruction(self):
        if self.pc == len(self.program):
            return None # End of program
        return self.program[self.pc]
    def step(self):
        instruction = self.getNextInstruction()
        if instruction is None:
            return
        instruction.executed = True
        match instruction.op:
            case Operation.ACC:
                self.acc += instruction.value
                self.pc += 1
            case Operation.NOP:
                self.pc += 1
            case Operation.JMP:
                self.pc += instruction.value
        

with open("day8.txt", "r") as f:
    machine = Machine([Instruction(line.strip()) for line in f.readlines()])

### Part 1:
##while not machine.getNextInstruction().executed:
##    machine.step()
##print(machine.acc)

# Program should terminate by reaching just after last instruction,
# having changed exactly 1 nop -> jmp or jmp -> nop.
# 1. Looping program includes a nop that would go to end - change that.

    

# From end, build list of instructions that would reach the end if executed:
#   An acc/nop just before an instruction that reaches the end,
#   or a jump +x at distance -x from an instruction that reaches the end.
def findTerminatingPaths(program):
    changing = True
    while changing:
        changing = False
        for i in range(len(program)):
            instr = program[i]
            if instr.terminates:
                continue
            match instr.op:
                case Operation.ACC | Operation.NOP:
                    if i + 1 == len(program) or program[i+1].terminates:
                        changing = True
                        instr.terminates = True
                case Operation.JMP:
                    if i + instr.value == len(program) or program[i + instr.value].terminates:
                        changing = True
                        instr.terminates = True

# Then, for running regular program, swap first nop -> jmp or jmp -> if it
# would then hit one of these instructions

findTerminatingPaths(machine.program)

# find point in program to change instruction
while True:
    pc = machine.pc
    instr = machine.program[pc]
    match instr.op:
        case Operation.NOP:
            target = pc + instr.value
            if (target == len(machine.program)
                or target < len(machine.program)
                    and machine.program[target].terminates):
                instr.op = Operation.JMP
                break
        case Operation.JMP:
            target = pc + 1
            if (target == len(machine.program)
                or machine.program[target].terminates):
                instr.op = Operation.NOP
                break
    machine.step()

# continue till end
while machine.getNextInstruction() is not None:
    machine.step()
print(machine.acc)
