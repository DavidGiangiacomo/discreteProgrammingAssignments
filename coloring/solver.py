#!/usr/bin/python
# -*- coding: utf-8 -*-

from constraints import *

class DomainStore:
    def __init__(self, nb, lowerBound):
        self.variables = [[j for j in range(0, lowerBound)] for i in range (0, nb)]

    def getValues(self, x):
        return self.variables[x]
        
    def setValues(self, x,  values):
        self.variables[x] = values
        
    def __str__( self ):
        return str(self.variables)

class ConstraintStore:
    def __init__(self, nb, lowerBound):
        self.domainStore = DomainStore(nb, lowerBound)
        self.constraints = []

    def addConstraint(self, constraint):
        self.constraints.append(constraint)

    def propagate(self):
        change = True
        while change:
            change = False
            for constraint in self.constraints:
                if constraint.isFeasible(self.domainStore):
                    change = change or constraint.prune(self.domainStore)
                else:
                    return False
#            print self
        return True
        
    def getNbSolutions(self):
        total = 1
        for domainValue in self.domainStore.variables:
            total *= len(domainValue)
        return total
        
    def isFeasible(self):
        for constraint in self.constraints:
            if not constraint.isFeasible(self.domainStore):
                return False
        return True
        
    def __str__( self ):
        return str(self.domainStore)
    
def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    nodeDegrees = [(i,  0) for i in range(0,  int(firstLine[0]))]
    edgeCount = int(firstLine[1])

    cs = ConstraintStore(nodeCount, min(17, nodeCount))
    
    for i in range(0,  nodeCount):
        cs.addConstraint(InferiorConstantConstraint(i, i + 1))

    edges = []
    for i in range(1, edgeCount+1):
        line = lines[i]
        parts = line.split()
        nodeDegrees[int(parts[0])] = (int(parts[0]), nodeDegrees[int(parts[0])][1] + 1)
        nodeDegrees[int(parts[1])] = (int(parts[1]), nodeDegrees[int(parts[1])][1] + 1)
        edges.append((int(parts[0]), int(parts[1])))
        cs.addConstraint(NotEqConstraint(int(parts[0]), int(parts[1])))

    nodeDegrees.sort(key=lambda tup: tup[1],  reverse=True)
    if not cs.isFeasible():
        return False
    while cs.getNbSolutions() > 1:
        for node in nodeDegrees:
            domainV = cs.domainStore.getValues(node[0])
            if len(domainV) > 1:
                cs.addConstraint(EqualConstantConstraint(node[0],  domainV[0]))
                if not cs.propagate():
                    return False
                continue
                    
    
    solution = [-1 for i in range(0, nodeCount)]
    result = 0
    for index,  variable in enumerate(cs.domainStore.variables):
        if not variable[0] in solution:
            result += 1
        solution[index] = variable[0]

    # prepare the solution in the specified output format
    outputData = str(result) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution))

    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

