#!/usr/bin/python
# -*- coding: utf-8 -*-

currentMax = 0
finalResult = []

class Item:
    def __init__(self, index, value, weight, unitValue):
        self.index = index
        self.value = value
        self.weight = weight
        self.unitValue = unitValue

    def __repr__(self):
        return repr((self.index, self.value, self.weight, self.unitValue))

def estimate(items, capacity):
    result = 0
    i = 0
    room = capacity
    while room > 0 and i < len(items):
        if (items[i].weight <= room):
            result += items[i].value
            room -= items[i].weight
        else:
            result += items[i].unitValue * room
            room = 0
        i=i+1
    return result

def bab(capacity, items):
    items.sort(key=lambda item: item.unitValue, reverse=True)
    taken = [0 for i in range (0, len(items))]

    recurse(taken, items, capacity, 0)

    # prepare the solution in the specified output format
    outputData = str(currentMax) + ' ' + str(1) + '\n'
    outputData += ' '.join(map(str, finalResult))
    return outputData

def recurse(result, items, room, currentValue):
    global currentMax, finalResult
    if len(items) == 0:
        return currentValue

    if items[0].weight > room:
        return recurse(result, items[1:len(items)], room, currentValue)

    estimation = currentValue + estimate(items, room)
    if estimation <= currentMax:
        return 0

    result[items[0].index] = 1
    leftResult = recurse(result, items[1:len(items)], room - items[0].weight, currentValue + items[0].value)

    if leftResult > currentMax:
        currentMax = leftResult
        finalResult = result[0:len(result)]
    result[items[0].index] = 0

    if leftResult < estimation:
        result[items[0].index] = 0
        rightResult = recurse(result, items[1:len(items)], room, currentValue)
    else:
        return leftResult

    if rightResult > currentMax:
        currentMax = rightResult
        finalResult = result[0:len(result)]
        return currentMax
    else:
        return 0

def dynamic(capacity, items):
    value = 0
    weight = 0

    valuesByCapacities = [[0 for j in range (0, capacity + 1)] for i in range (0, len(items) + 1)]
    taken = [0 for i in range (0, len(items))]

    for i in range(1, len(items) + 1):
        value = items[i - 1].value
        weight = items[i - 1].weight
        for j in range(0, capacity + 1):
            if (weight <= j):
                valuesByCapacities[i][j] = max(valuesByCapacities[i - 1][j], valuesByCapacities[i - 1][j - weight] + value)
            else:
                valuesByCapacities[i][j] = valuesByCapacities[i - 1][j]

    result = valuesByCapacities[len(items)][capacity]

    for i in range (1, len(items) + 1):
        if (valuesByCapacities[len(items) - i][capacity] < valuesByCapacities[len(items) - i + 1][capacity]):
            taken[items[len(items) - i].index] = 1
            capacity -= items[len(items) - i].weight

    # prepare the solution in the specified output format
    outputData = str(result) + ' ' + str(1) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData

def solveIt(inputData):
    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nbItems = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    average = 0.0

    for i in range(0, nbItems):
        line = lines[i + 1]
        parts = line.split()

        v = int(parts[0])
        w = int(parts[1])

        items.append(Item(i, v, w, float(v) / float(w)))



#    outputData = dynamic(capacity, items)
    outputData = bab(capacity, items)
    return outputData


import sys

if __name__ == '__main__':
    sys.setrecursionlimit(10005)
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

