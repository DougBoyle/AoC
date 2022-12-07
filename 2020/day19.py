import numpy as np
from enum import Enum
import re

def readDigit(line, start):
    index = start + 1
    while index < len(line) and line[index].isdigit():
        index += 1
    return int(line[start:index]), index

class RuleKind(Enum):
    SEQUENCE = 1
    OR = 2
    CHAR = 3
    NUMBER = 4

# stack of (rule, stringPos, rulePos, then)
# initialised as (0, 0, 0), bottom element only solved if position end of string when popped
# while solving, return position of sub-part, or -1 if no match, rather than True/False
### ISSUE! OR needs to re-order stack to remember what to come back to on later failure?
### Stack represents call stack, still need to pass around 'then'? So stack really just for OR cases?
stack = []

def solve(rule, message):
    global stack
    stack = [(rule, 0, 0, None)]
    return matchMessage(message)

# A general regex solver.
# Maintains a stack of ORs followed by the current thing actually being considered for a match.
# Each point additionally keeps a mutated sequence of things to do 'next', effectively joining different branches of the tree
# Means that seq(A, ...) -> A then ..., which means OR nodes have the context of what to test after (a|b)cde etc.
# The stack of just ORs means that all options gradually get exhausted.
# Guarentees about recursion for the question ensure recursive attempts look for strictly longer matches, so eventually terminate
def matchMessage(s):
    global stack
    # artificial stack limit for testing
    if len(stack) > 2000:
        raise Exception("Stack exceeded 2000 frames")
    while len(stack) > 0:
        rule, position, ruleIndex, then = stack.pop()
        match rule.kind:
            case RuleKind.CHAR:
                if position >= len(s) or s[position] != rule.subrules:
                    pass
                elif then is not None:
                    stack.append((then, position + 1, 0, None))
                else: # only a match if nothing left
                    if position + 1 == len(s):
                        return True
                    # else will fall back down stack, and try something else
            case RuleKind.SEQUENCE:
                if len(rule.subrules) > 0:
                    remaining = Rule(RuleKind.SEQUENCE, rule.subrules[1:])
                    if then is not None:
                        remaining.subrules.append(then)
                    stack.append((rule.subrules[0], position, 0, remaining))
                elif then is not None:
                    stack.append((then, position, 0, None))
                elif position == len(s):
                    return True
            case RuleKind.NUMBER:
                stack.append((rules[rule.subrules], position, 0, then))
            case RuleKind.OR:
                if ruleIndex < len(rule.subrules):
                    stack.append((rule, position, ruleIndex + 1, then))
                    stack.append((rule.subrules[ruleIndex], position, 0, then))
    return False
    

class Rule:
    # kind = char: subrules is the character to match
    # kind = sequence: subrules are sequence to match, each (Token, String/Rule)
    # kind = or: subrules are options, any of which can match, each a Rule
    def __init__(self, kind, subrules):
        self.subrules = subrules
        self.kind = kind
    # TODO: a 'match' method taking string + dictionary of all rules

    def match(self, s, position, then):
        match self.kind:
            case RuleKind.CHAR:
                if position >= len(s) or s[position] != self.subrules:
                    return False
                elif then is None:
                    return position + 1 == len(s)
                else:
                    return then.match(s, position + 1, None)
            case RuleKind.SEQUENCE:
                if len(self.subrules) > 0:
                    remaining = Rule(RuleKind.SEQUENCE, self.subrules[1:])
                    if then is not None:
                        remaining.subrules.append(then)
                    return self.subrules[0].match(s, position, remaining)
                elif then is None:
                    return position == len(s)
                else:
                    return then.match(s, position, None)
            case RuleKind.NUMBER:
                return rules[self.subrules].match(s, position, then)
            case RuleKind.OR:
                for case in self.subrules:
                    if case.match(s, position, then):
                        return True
                return False

    def findMatch(self, s, position, then):
        match self.kind:
            case RuleKind.CHAR:
                if position >= len(s) or s[position] != self.subrules:
                    return -1
                elif then is None:
                    return position + 1
                else:
                    return then.findMatch(s, position + 1, None)
            case RuleKind.SEQUENCE:
                if len(self.subrules) > 0:
                    remaining = Rule(RuleKind.SEQUENCE, self.subrules[1:])
                    if then is not None:
                        remaining.subrules.append(then)
                    return self.subrules[0].findMatch(s, position, remaining)
                elif then is None:
                    return position
                else:
                    return then.findMatch(s, position, None)
            case RuleKind.NUMBER:
                return rules[self.subrules].findMatch(s, position, then)
            case RuleKind.OR:
                for case in self.subrules:
                    n = case.findMatch(s, position, then)
                    if n >= 0:
                        return n
                return -1

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        match self.kind:
            case RuleKind.SEQUENCE:
                return " ".join(str(rule) for rule in self.subrules)
            case RuleKind.OR:
                return "(" + " | ".join([str(rule) for rule in self.subrules]) + ")"
            case RuleKind.CHAR:
                return self.subrules
            case RuleKind.NUMBER:
                # No longer possible in part 2, now rules recursive
                #return str(rules[self.subrules])
                return " " + str(self.subrules) + " "

    def strRec(self):
        match self.kind:
            case RuleKind.SEQUENCE:
                return " ".join(rule.strRec() for rule in self.subrules)
            case RuleKind.OR:
                return "(" + " | ".join([rule.strRec() for rule in self.subrules]) + ")"
            case RuleKind.CHAR:
                return self.subrules
            case RuleKind.NUMBER:
                # No longer possible in part 2, now rules recursive
                return rules[self.subrules].strRec()

# TODO: This should itself return a 'Rule'?
# Need to distinguish ones with/without index
def parseOption(s):
    if '"' in s: # single character
        return Rule(RuleKind.CHAR, s[s.index('"') + 1])
    else:
        return Rule(RuleKind.SEQUENCE,
                    [Rule(RuleKind.NUMBER, int(n)) for n in s.strip().split(" ")]
                )
    
def parseRule(s):
    parts = s.split(":")
    ruleNum = int(parts[0])
    options = parts[1].split("|")
    if len(options) == 1:
        return ruleNum, parseOption(options[0])
    else:
        return ruleNum, Rule(RuleKind.OR, [parseOption(option) for option in options])

rules = {}
messages = []

parsingRules = True
with open("day19.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            parsingRules = False
        elif parsingRules:
            n, rule = parseRule(line)
            rules[n] = rule
        else:
            messages.append(line)

### Part 2 ###
# Replace rule 8: 42 -> 8: 42 | 42 8
#   Or slightly more efficiently, Seq( Num(42), Or( Seq([]), Num(8)))   - Seq([]) matches empty string
# Replace rule 11: 42 31 -> 11: 42 31 | 42 11 31
#   Again, can write as Seq( 42, Or ( Seq [], 11 ), 31 )
# Importantly, always tries most simple case before more complex one
newRule8 = Rule(RuleKind.SEQUENCE, [
        Rule(RuleKind.NUMBER, 42),
        Rule(RuleKind.OR, [
              Rule(RuleKind.SEQUENCE, []),
              Rule(RuleKind.NUMBER, 8)
        ])
    ])
newRule11 = Rule(RuleKind.SEQUENCE, [
        Rule(RuleKind.NUMBER, 42),
        Rule(RuleKind.OR, [
              Rule(RuleKind.SEQUENCE, []),
              Rule(RuleKind.NUMBER, 11)
        ]),
        Rule(RuleKind.NUMBER, 31)
    ])
rules[8] = newRule8
rules[11] = newRule11

# Neither 42 or 31 are recursive with these changes, so still shouldn't infinite loop

total = 0
processed = 0
for message in messages:
    if solve(rules[0], message):
        total += 1
    processed += 1
print(total)

# 0: 8 11 - needs to match both recursive ones
# (42) (42 31) or (42 42) (42 31) or (42 42 42) (42 31) ...
# or (42) (42 42 31 31) ...
# i.e. matches 31 one or more times, and 42 at least once more than 31
# As a cheat, could just manually process in loop i.e. 'matches 42?' until doesn't, then see if matches 31
# Issue comes from overlap between 42 and 31, but could work back once number of matches known

# Additionally, ONLY rules 8 and 11 mention 31 or 42.

# Getting stuck on message 31? (0 indexed) - aaababaababbbbabaababababbaabbaabbabbabbbaaaabababbabaaabbbbaaababbabaaa

# Depth issue just due to messy recursive calls rather than a proper stack for Sequences?
# i.e. keep a stack of (rule, position, indexInRule) where indexInRule is part of Seq/Or on for those rules?
# Sequence/Or can then modify stack in place by pop/pushing, rather than deep recursion?











