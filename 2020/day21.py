import numpy as np
from enum import Enum
import re

ALERGEN_LIST = "(\w+(?:, \w+)*)"
ALERGEN_PATTERN = "(?:$| \(contains " + ALERGEN_LIST + "\))"
INGREDIENTS_PATTERN = "(\w+(?: \w+)*)"
LINE_PATTERN = INGREDIENTS_PATTERN + ALERGEN_PATTERN

print(LINE_PATTERN)


allIngredients = set()
allAllergens = set()
# allergens -> ingredients. Entries my be ommitted, so empty allergen list tells us nothing
entries = []
ingredientCounts = {}

# 0 = ., 1 = #
with open("day21.txt", "r") as f:
    for line in f.readlines():
        m = re.match(LINE_PATTERN, line)
        if m is not None:
            ingredients = m.group(1).split(" ")
            for ingredient in ingredients:
                if ingredient not in ingredientCounts:
                    ingredientCounts[ingredient] = 0
                ingredientCounts[ingredient] += 1
            allIngredients.update(ingredients)
            allergens = m.group(2)
            if allergens is not None:
                allergens = allergens.split(", ")
                allAllergens.update(allergens)
                entries.append((allergens, ingredients))
                
# incomplete information, so initially any allergen could map to any ingredient
possibleIngredients = {allergen : allIngredients.copy() for allergen in allAllergens}

# If we know X, Y, Z contains A, B - can remove all except X,Y,Z from what A and B could be
# Once we know A is X, can remove X from consideration everywhere else

knownMappings = {}
knownIngredients = set()

size = sum(len(s) for s in possibleIngredients.values())
print(size)
lastSize = size * 2
while size < lastSize:
    lastSize = size
    for allergens, ingredients in entries:
        for allergen in allergens:
            possibleIngredients[allergen] = set(filter(
                lambda ingredient: ingredient in ingredients and ingredient not in knownIngredients,
                possibleIngredients[allergen]
            ))

    # remove known ones
    for allergen, possible in possibleIngredients.items():
        if len(possible) == 1:
            ingredient = next(iter(possible))
            knownMappings[allergen] = ingredient
            knownIngredients.add(ingredient)
    
    size = sum(len(s) for s in possibleIngredients.values())
    print(size)

print("Solved: " + str(len(knownMappings) == len(allAllergens)))


ingredintsWithoutAllergens = allIngredients.difference(knownIngredients)
count = 0
for ingredient in ingredintsWithoutAllergens:
    count += ingredientCounts[ingredient]
print(count)

orderedAllergens = sorted(allAllergens)
orderedIngredients = ",".join(knownMappings[alergen] for alergen in orderedAllergens)
print(orderedIngredients)
