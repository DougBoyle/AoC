import numpy as np
from enum import Enum
import re
import time

# directory
class Tree():
    def __init__(self, name):
        self.name = name
        self.children = []
        self.size = None
        self.parent = None
    def __repr__(self):
        return self.name
    def add(self, child):
        self.children.append(child)
    def getSize(self):
        if self.size is None:
            self.size = sum(child.getSize() for child in self.children)
        return self.size
    def hasSize(self):
        return self.size is not None
    def getOrCreateDir(self, name):
        for child in self.children:
            # Allow for a directory to contain both a file/directory of the same name
            if isinstance(child, Tree) and child.name == name:
                return child
        newChild = Tree(name)
        self.add(newChild)
        newChild.parent = self
        return newChild
    def mayCreateFile(self, file):
        for child in self.children:
            if isinstance(child, File) and child.name == file.name: # simple way to avoid duplicates
                return
        self.add(file)
        file.parent = self
            
class File():
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.parent = None
    def __repr__(self):
        return self.name
    def getSize(self):
        return self.size
    def hasSize(self):
        return True

root = None
current = None

PATTERN_CD = "\$ cd (.+)"
PATTERN_DIR = "dir (.+)"
PATTERN_FILE = "(\d+) (.+)" # not just \w, file names often include '.'

with open("day7.txt") as f:
    for line in f.readlines():
        line = line.strip()
        m = re.match(PATTERN_CD, line)
        if m is not None:
            name = m.group(1)
            if name == "/": # only occurs once, at start
                root = Tree(name)
                current = root
            elif name == "..":
                current = current.parent
            else:
                current = current.getOrCreateDir(name)
            continue
        m = re.match(PATTERN_DIR, line)
        if m is not None:
            name = m.group(1)
            current.getOrCreateDir(name)
            continue
        m = re.match(PATTERN_FILE, line)
        if m is not None:
            name = m.group(2)
            size = int(m.group(1))
            file = File(name, size)
            current.mayCreateFile(file)
            continue

# once all nodes found, recursively compute overall sizes,
# using manual stack to avoid stack overflow
stack = [root]
while len(stack) > 0:
    node = stack.pop()
    if node.hasSize():
        continue
    if all(child.hasSize() for child in node.children):
        node.getSize()
        continue
    stack.append(node) # come back later once children sizes populated
    stack += node.children

def DFSDirs(root, apply):
    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        if not isinstance(node, Tree):
            continue
        stack += node.children
        apply(node)

# Part 1
# DFS to sum directory sizes
total = 0
limit = 100000
def addIfUnderLimit(node):
    global total
    if node.getSize() <= limit:
        total += node.getSize()
DFSDirs(root, addIfUnderLimit)
print(total) # 1444896

# Part 2
totalAvailable = 70000000
required =       30000000
inUse = root.getSize()
target = inUse + required - totalAvailable
print(target)

smallest = totalAvailable
def updateSmallest(node):
    global smallest
    if node.getSize() < smallest and node.getSize() >= target:
        smallest = node.getSize()

DFSDirs(root, updateSmallest)
print(smallest)








