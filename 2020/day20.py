import numpy as np
from enum import Enum
import re

tiles = {}

tileId = 0
tile = []

TILE_ID_PATTERN = "Tile (\d+):"

# 0 = ., 1 = #
with open("day20.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            tiles[tileId] = np.array(tile)
            tile = []
            continue
        m = re.match(TILE_ID_PATTERN, line)
        if m is not None:
            tileId = int(m.group(1))
        else:
            tile.append([0 if c == '.' else 1 for c in line])
if len(tile) > 0:
    tiles[tileId] = np.array(tile)

# np.rot90(m) - anti-clockwise
# np.flip(m, axis=0) - flip vertically (None axis = all -> 180 rotation)


def rotate(tile, n):
    "n=0-3 for number of anti-clockwise turns of the original"
    return np.rot90(tile, k=n)

def flip(tile):
    return np.flip(tile, axis=0)

# permutations:
# tileId -> array
# 0 = original, 1-3 = rotated 1-3 times
# 4 = flipped, 5-7 = flipped + rotated 1-3 times
def getPermutations(tile):
    return [rotate(flippedTile, n) for flippedTile in [tile, flip(tile)]
            for n in range(4)]

permutations = {}
for tile in tiles:
    permutations[tile] = getPermutations(tiles[tile])

# Need to then be able to describe which tile-permutations pairs match,
# and fix one non-symmetric tile to get a unique solution.
# -- if none was individually unique, could just enforce each time one added
#    to the 'first' tile until it became unique.

# possible ways of matching:
# for a tile-orientation: 0 = on its right, 1 = above, 2 = left, 3 = below

# Orientation of edges always correct way round
# i.e. top/bottom read left to right, left/right read top to bottom.

# optimsation: precompute edges
#  144 tiles * 8 permutations * 4 sides = only about 5k to store
edgesRTLB = { tileId : { perm : np.array([tile[:,-1], tile[0], tile[:,0], tile[-1]])
                         for perm, tile in enumerate(perms) }
              for tileId, perms in permutations.items() }

edgesLBRT = { tileId : { perm : edges[[2,3,0,1]]
                         for perm, edges in perms.items() }
              for tileId, perms in edgesRTLB.items() }

def getMatches(tile, tilePerm, neighbour, neighbourPerm):
    # returns a tuple, one element per axis (for coordinates in each axis). Only one axis hence [0]
    return (edgesRTLB[tile][tilePerm] == edgesLBRT[neighbour][neighbourPerm]).all(axis=1).nonzero()[0]



# 144 tiles x 8 orientations = 1,152. So quadratic approach only ~1M to check
# encode a tile and orientations as {tile}-{0..7} using ordering above
# Each entry in matching list is (tile, orientation, [sides])
matches = { tile: [(i, []) for i in range(8)]
            for tile in permutations }

import time
start_time = time.time()

print("Computing pairwise matches")

# First pass, find possible joins (rather than adding literally all pairs)
# 10 cell edge = 1k possibilities = expect only 1 match per edge
for tileId in matches:
    tilePermutationMatches = matches[tileId]
    for idx, permMatches in tilePermutationMatches:
        for neighbourId in matches:
            if neighbourId == tileId:
                continue # can't match with itself!
            neighbourPermutationMatches = matches[neighbourId]
            for neighbourIdx, _ in neighbourPermutationMatches:
                pairMatches = getMatches(
                    tileId, idx,
                    neighbourId, neighbourIdx
                    )
                # actually worth recording
                if len(pairMatches) > 0:
                    permMatches.append(
                        (neighbourId, neighbourIdx, pairMatches)
                        )
                    
# 18s, down to 4s by pre-generating numpy arrays for edges and equating them
# Down further to 3.3s by being able to reasonably remove print on each iteration
print("--- %s seconds ---" % (time.time() - start_time)) 

# Conditions to fix a match (remember if Y matches to X then X also matches to Y):
# If an orientation has <2 different tiles it could match, not possible so remove it.
# If a tile has <= 2 different tiles it could match, for each orientation, it is corner.
# Once 4 corners found, that conditions to rule out options becomes 3 not 2.

def maxUniqueTiles(permutationMatches):
    maxMatches = 0
    for perm, matches in permutationMatches:
        distinctTiles = set()
        for match in matches:
            distinctTiles.add(match[0])
        maxMatches = max(maxMatches, len(distinctTiles))
    return maxMatches


# After first pass, a few with 3 matches and all others with 4
# Need some trial and error to start building clusters/find corners?

# Alternatively, if a tile has 2 edges that don't match anywhere else, is corner.

# From problem description, guaranteed no matches around outer border:
# "Tiles at the edge of the image also have this border,
#  but the outermost edges won't line up with any other tiles."


matchCount = {}
for tile, tileMatches in matches.items():
    n = maxUniqueTiles(tileMatches)
    if n not in matchCount:
        matchCount[n] = 0
    matchCount[n] += 1

# {4: 100, 2: 4, 3: 40} -- so corners/edges/inner pieces obvious from the start

# For each tile, for each permutation, <=1 candidate per edge
def isTrivial():
    for tile, tileMatches in matches.items():
        for orientation, orientationMatches in tileMatches:
                occupied = set()
                for match in orientationMatches:
                    for side in match[2]:
                        if side in occupied:
                            return False
                        occupied.add(side)
    return True

print("Trivial: " + str(isTrivial())) # True!

# As it is a trivial solution, can just fix orientation of one tile
# and solve by eliminating no longer possible configurations
# (removing X from Y symmetrically removes Y from X)

firstTile = list(tiles.keys())[0]

fixedOrientations = {firstTile: 0} # as edges paired up, more things locked to one orientation

# If tile has 1 permutation and max 1 option for each edge, must match exactly those,
# so can insert pairs of tile -> {tile -> (firstOrientation, secondOrientation), ...}
# May not even need, enough to just also record that the other must have fixed orientation too
pairedEdges = {} 


def getMatchesSize(matches):
    count = 0
    for tileId in matches:
        tilePermutationMatches = matches[tileId]
        for permutation, permMatches in tilePermutationMatches:
            for neighbour, neighbourPerm, sides in permMatches:
                count += len(sides)
    return count

print("Initial size: " + str(getMatchesSize(matches)))

def updateMatches(matches):
    # iterate, refining possible matches
    # puerly going off of forcing orientations, not actually considering which sides used at all
    for tileId in matches:
        newTileMatches = []
        # (permutation, [(tile, permutation, [sides, ...]), ...]), ...
        tilePermutationMatches = matches[tileId]

        for permutation, permMatches in tilePermutationMatches:
            newPermMatches = []
            # if orientation of this tile has been fixed, remove others
            if tileId in fixedOrientations and permutation != fixedOrientations[tileId]:
                continue
            
            for neighbour, neighbourPerm, sides in permMatches:
                # if neighbour's orientation fixed, remove that as a possible match
                if neighbour in fixedOrientations and neighbourPerm != fixedOrientations[neighbour]:
                    continue
                newPermMatches.append((neighbour, neighbourPerm, sides))
            if len(newPermMatches) > 0:
                newTileMatches.append((permutation, newPermMatches))

        matches[tileId] = newTileMatches

        # now, if there is only 1 possibility, record that (relying on fact that corner/edge/inner obvious)
        if len(newTileMatches) == 1:
            perm, permMatches = newTileMatches[0]
            fixedOrientations[tileId] = perm
            unique = True
            sides = set()
            for match in permMatches:
                if len(match[2]) > 1:   # could match on more than one side
                    unique = False
                else:
                    side = match[2][0]
                    if side in sides:   # nothing else matches to this side
                        unique = False
                    else:
                        sides.add(side)
            if unique:
                if tileId not in pairedEdges:
                    pairedEdges[tileId] = {}
                for match in permMatches:
                    # don't even need to track which side now
                    neighbour, neighbourPerm = match[0], match[1]
                    if neighbour not in pairedEdges:
                        pairedEdges[neighbour] = {}
                    pairedEdges[tileId][neighbour] = (perm, neighbourPerm)
                    pairedEdges[neighbour][tileId] = (neighbourPerm, perm)
                    
                    fixedOrientations[neighbour] = neighbourPerm

while len(fixedOrientations) < len(tiles):
    updateMatches(matches)
    print("Updated size: " + str(getMatchesSize(matches)))


# Finally, build the actual solution
# For matching edges have 0 = right, 1 = above, 2 = left, 3 = below
# Build [tileId -> (x, y)] and 12x12 array of (tileId, permutation) -- where row 0 is top
# Start in top left i.e. tile with no matces on sides 1 or 2

tilePositions = {}
# TODO: No longer 12x12 in pt 2, probably much slower to process?
squareTiles = [[None for x in range(12)] for y in range(12)]
squareOrientations = [[None for x in range(12)] for y in range(12)]

def getCoords(x, y, direction):
    if direction == 0:
        return x+1, y
    elif direction == 1:
        return x, y-1 # inverted y axis, top left is 0,0
    elif direction == 2:
        return x-1, y
    elif direction == 3:
        return x, y+1

for tileId in matches:
    perm, neighbours = matches[tileId][0] # unique at this point
    isTopLeft = True
    for neighbour in neighbours:
        side = neighbour[2][0] # side is unique
        if side == 1 or side == 2:
            isTopLeft = False
            break
    if isTopLeft:
        tilePositions[tileId] = (0, 0)
        squareTiles[0][0] = tileId
        squareOrientations[0][0] = perm
        break

lastLocated = 0
located = len(tilePositions)
print("located: " + str(lastLocated))
while located < len(tiles) and lastLocated != located:
    lastLocated  = located
    for tileId in matches:
        if tileId not in tilePositions:
            continue
        x, y = tilePositions[tileId]
        perm, neighbours = matches[tileId][0]
        for neighbour in neighbours:
            neighbourId, neighbourPerm, side = neighbour[0], neighbour[1], neighbour[2][0]
            if neighbourId in tilePositions:
                continue
            newX, newY = getCoords(x, y, side)
            tilePositions[neighbourId] = (newX, newY)
            squareTiles[newY][newX] = neighbourId
            squareOrientations[newY][newX] = neighbourPerm
    located = len(tilePositions)
    print("located: " + str(located))


# 17712468069479
print("Corner product: " +
      str(squareTiles[0][0] *
      squareTiles[11][0] *
      squareTiles[0][11] *
      squareTiles[11][11])
      )

# TODO: Build complete grid i.e. replace each of 12x12 grid with inner 8x8
tileWidth = len(tiles[firstTile][0])
tileHeight = len(tiles[firstTile])



completeGrid = []
for rowIdx in range(len(squareTiles)):
    cellRow = squareTiles[rowIdx]
    for y in range(1, tileHeight - 1):
        row = []
        for colIdx in range(len(cellRow)):
            tile = permutations[cellRow[colIdx]][squareOrientations[rowIdx][colIdx]]
            for x in range(1, tileWidth - 1):
                row.append(tile[y][x])
        completeGrid.append(row)

            
        

# width 20, height 3
# |                  # 
# |#    ##    ##    ###
# | #  #  #  #  #  #   

seaMonster = [[1 if x == '#' else 0 for x in "                  # "],
              [1 if x == '#' else 0 for x in "#    ##    ##    ###"],
              [1 if x == '#' else 0 for x in " #  #  #  #  #  #   "]]

def isSeaMonster(grid, cornerX, cornerY):
    width = len(grid[0])
    height = len(grid)
    if cornerX + 20 >  width or cornerY + 3 > height:
        return False
    for x in range(20):
        for y in range(3):
            if seaMonster[y][x] == 1 and grid[cornerY + y][cornerX + x] != 1:
                return False
    return True

def clearSeaMonster(grid, cornerX, cornerY):
    for x in range(20):
        for y in range(3):
            if seaMonster[y][x] == 1:
                grid[cornerY + y][cornerX + x] = 0


def hasSeaMonster(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if isSeaMonster(grid, x, y):
                return True
    return False

def removeAllSeaMonsters(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if isSeaMonster(grid, x, y):
                clearSeaMonster(grid, x, y)

def getCorrectOrientation(original):
    for grid in getPermutations(original):
        if hasSeaMonster(grid):
            return grid

# Debugging: Check 120x120 grid with gaps between looks sensible too
resultString = ""
for yCell in range(12):
    for y in range(10):
        for xCell in range(12):
            for x in range(10):
                tileId = squareTiles[yCell][xCell]
                orientation = squareOrientations[yCell][xCell]
                tile = permutations[tileId][orientation]
                resultString += '#' if tile[y][x] == 1 else '.'
            resultString += " "
        resultString += "\n"
    resultString += "\n"
                
grid = getCorrectOrientation(completeGrid)

print("Initial count: " + str(np.sum(grid)))
removeAllSeaMonsters(grid)
print("Final count: " + str(np.sum(grid)))





