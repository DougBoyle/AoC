import re

class Bag:
    def __init__(self, name):
        self.name = name
        self.possible = False
        self.containsGold = False
        self.contains = {}
        self.totalContained = None

# check which bags are possible to create first
# from that work out which can contain shiny gold bags
# Both steps done bottom-up iteratively

COLOR = "\w+ \w+"
#BAG_LIST = "(?:(\d+) ({0}) bags?, )*(\d+) ({1}) bags?.".format(COLOR, COLOR)
BAG_LIST = "((\d+) ({0}) bags?, )*(\d+) ({1}) bags?.".format(COLOR, COLOR)
#SENTENCE = "({0}) bags contain (?:no other bags.|{1})".format(COLOR, BAG_LIST)
SENTENCE = "({0}) bags contain (no other bags.|{1})".format(COLOR, BAG_LIST)

COLOR_BAG = "(\d+) ({0})".format(COLOR)
ColorBagPattern = re.compile(COLOR_BAG)

rules = {}

def matchLine(line):
    global rules
    m = re.match(SENTENCE, line)

    bag = Bag(m.group(1))
    
    rest = m.group(2)
    contains = ColorBagPattern.findall(rest)
    rules[bag.name] = bag
    for coloredBag in contains:
        count = int(coloredBag[0])
        name = coloredBag[1]
        bag.contains[name] = count
    
with open("day7.txt", "r") as f:
    for line in f.readlines():
        matchLine(line.strip())

# determine which possible
changing = True
while changing:
    changing = False
    for rule in rules:
        bag = rules[rule]
        if bag.possible:
            continue
        childrenPossible = True
        for child in bag.contains:
            if not rules[child].possible:
                childrenPossible = False
                break
        if childrenPossible:
            bag.possible = True
            changing = True

changing = True
while changing:
    changing = False
    for rule in rules:
        bag = rules[rule]
        if not bag.possible or bag.containsGold:
            continue
        doesContainGold = False
        for child in bag.contains:
            if rules[child].containsGold or rules[child].name == "shiny gold":
                doesContainGold = True
                break
        if doesContainGold:
            bag.containsGold = True
            changing = True

tot = 0
for  rule in rules:
    if rules[rule].containsGold:
        tot += 1
print(tot)

# Part 2
changing = True
while changing:
    changing = False
    for rule in rules:
        bag = rules[rule]
        if bag.totalContained is not None:
            continue
        totalContained = 0
        for child in bag.contains:
            childBag = rules[child]
            if childBag.totalContained is None:
                totalContained = None
                break
            totalContained += (childBag.totalContained + 1) * bag.contains[child]
        if totalContained is not None:
            bag.totalContained = totalContained
            changing = True

print(rules["shiny gold"].totalContained)
