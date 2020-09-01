"""
RandomWalksGenerator.py

Randomwalks-based Synthetic Data Generator

The synthetic data represents active components over time steps [0, t]. Synthetic data is generated as follows:
    1) Create connected components through a number of random-walks on graph G.
       Do not visit the same node per random-walk.

    2) Start at a node picked uniformly at random, for each iteration, there is probability 'alpha' of choosing a neighbor
       and a probability 'beta = 1 - alpha' of stopping

    3) End up with a random-walk which represents an active connected component.

    4) Repeat for a fixed number numOfRandomWalks

    5) Each random-walk will be assigned a time duration [t, t'], where t' can be adjusted with param k.

    6) Now each time step: 0, 1, 2..etc. will have a list of random-walks (i.e. active paths).
       e.g. t1: {[A,B,C], [CDE]}, t2: {[A,B,C], [D,F]}

    7) An input file is then generated based on the paths. The input file is a matrix of 0's and 1's.
       node 'i' at timestep 'j' is active if it has value 1 (e.g. inputMatrix[i][j] == 1)

@author Sami Tarazi
"""
import datetime
import os
import sys
import random
import itertools

from random import choice

import networkx as nx

import numpy as np

# Number of time steps
TS = 100

# Number of RandomWalks.
numOfRandomWalks = TS + 100

# Random Walk probability
alpha = 0.95

# Get graph path from input
graphPath = str(sys.argv[1])

tStamp = datetime.datetime.now().strftime('%m-%d--%H-%M-%S').format()


def main():

    tStamp = timeStamp()
    print(tStamp)
    # Load graph into memory
    graphFile = open(graphPath + "/Graph.txt", 'rb')
    G = nx.read_adjlist(graphFile)

    # generate random-walks. Do not visit nodes twice
    randomWalks = generateRandomWalks(G)

    # Assign a time step DURATION to each Random Walk.
    # Walk starts at a random t and ends at t + k
    # return walksMap[0] = [t, t + k] and walksMap[1] = [PATH]
    # e.g. randomWalk_1: {[1,3], [A,B,C]}
    walksMap = assignTimeSteps(randomWalks, k=2)

    # Break each time step duration into a single time step.
    # Return a list of random-walks for each single time step
    timeMap = listByTime(walksMap)
    print(timeMap)

    # Aggregate random walks for each time step. This converts walks into connected components.
    aggregateTimeMap = aggregateRandomWalks(timeMap, G)

    # Save random-walks and save time steps
    saveRandomWalks(walksMap, graphPath)
    saveTimeMap(aggregateTimeMap, walksMap, graphPath)

    # Generate node data based on active paths. Active node = 1, otherwise = 0
    inputFilePath, inputFileName = genInputFile(graphPath,aggregateTimeMap)


# Generate random-walks on graph G
# Store all walks in a list
# Return list of random-walks
def generateRandomWalks(G):
    # List to store random-walks
    randomWalks = []
    i = 1

    # Create a fixed number of random-walks. The number is denoted by variable 'numOfRandomWalks'
    while i <= numOfRandomWalks:
        # Get random-walk
        walk = randomWalk(G)

        # Add random-walk to list of walks
        randomWalks.append(walk)
        i = i + 1

    return randomWalks


# Random-walk on graph G with probability Alpha:
#   1) Choose a node uniformly at random
#   2) Visit one of its neighbours with probability Alpha, or stop with probability 1 - Alpha
#   3) Repeat step 2 until stopping
# Note: Do not visit the same node twice
# Return list of nodes to represent the random-walk
def randomWalk(G):
    allNodes = G.nodes()
    visitedNodes = {}
    stack = [] # Stack is needed if we consider re-visiting nodes
    result_randomWalk = []     # final random-walk to be returned

    # Choose node uniformly at random from the original graph G
    currentRandomNode = choice(list(allNodes))

    # push node into stack and mark as visited
    stack.append(currentRandomNode)
    visitedNodes[currentRandomNode] = True
    result_randomWalk.append(currentRandomNode) # Add node to result

    x = 0

    # Keep visiting neighbours based on Alpha probability
    while len(stack) > 0 and generateProbability():

        print("Current Node: " + str(currentRandomNode))
        print("Stack: " + str(stack))
        print("Visited Nodes: " + str(visitedNodes))

        # Get neighbours of current node
        neighbors = list(G.neighbors(currentRandomNode))

        print("Number of Neighbors: " + str(len(neighbors)))

        # if node has neighbours
        if len(neighbors) > 0:
            # Choose a neighbor uniformly at random
            randomNeighbor = choice(neighbors)

            # Check if neighbor is visited. If yes:
            # remove it from the list of neighbours. Then pick another neighbour.
            while randomNeighbor in visitedNodes:
                print("Neighbour Exists! now removing: " + str(randomNeighbor))
                neighbors.remove(randomNeighbor)
                if len(neighbors) > 0:
                    randomNeighbor = choice(neighbors)
                else:
                    break

            if len(neighbors) > 0: # if there exists an unvisited neighbor then add it
                # print neighbor
                print ("Neighbour Found: " + str(randomNeighbor))

                # Add random neighbor to stack, mark as visited, and add to final path
                stack.append(randomNeighbor)
                visitedNodes[randomNeighbor] = True
                result_randomWalk.append(randomNeighbor)
                currentRandomNode = randomNeighbor
            else: # if all neighbors are visited, stop.
                # currentRandomNode = stack.pop()
                break

        x = x + 1
        print("==========")
        print(str(len(stack)))
    return result_randomWalk


# Generate a probability value based on a given alpha
# Choose a number uniformly at random from 1, 100 inclusive.
# If number is less than or equal alpha * 100, return true. Else, false
def generateProbability():
    maxInt = 100
    num = random.randint(1, maxInt)
    alphaProbability = alpha * maxInt
    if num <= alphaProbability:
        return True
    elif num > alphaProbability or num <= maxInt:
        return False


# Assign each random-walk a random time step
# Return walksMap[0] = [t, t + k] and walksMap[1] = [PATH]
def assignTimeSteps(randomWalks, k):
    # Store data
    randomWalksMap = {}

    # Max time steps
    maxTime = TS - 1

    i = 1
    # Loop through all random-walks
    for walk in randomWalks:
        # Pick a start time step uniformly at random from [1, max time steps]
        startTime = random.randint(1, maxTime)

        # Calculate end time by: adding startTime + k
        endTime = startTime + k

        # If endTime is out of bounds: endTime = maxTime
        # This is the case when startTime + k is bigger than the allowed time steps
        if endTime > maxTime:
            endTime = maxTime

        timeStep = str(startTime) + "," + str(endTime)
        path = walk

        randomWalksMap["RandomWalk_" + str(i)] = [timeStep, path]
        i = i + 1

    return randomWalksMap


# For each time step, assign the list of walks that are active on that step
def listByTime(walksMap):
    i = 0
    timeMap = {}

    # For each walk, get lower-bound and upper-bound of the duration
    # Then, start at lower-bound time step and append the path until upper-bound time step
    # Repeat for all walks
    for walk in walksMap:
        # walksMap[walk] = {[t, t'], [path]}
        # index 0 of each walk is the time duration
        time = (walksMap[walk][0]).split(',')
        lowerBound = int(time[0])
        upperBound = int(time[1])

        # walksMap[walk] = {[t, t'], [path]}
        # index 1 of each walk is the actual path
        path = walksMap[walk][1]

        # Here appending the path for each time step per walk.
        for t in range(lowerBound, upperBound + 1):
            if int(t) in timeMap:
                timeMap[int(t)].append(path)
            else:
                walksList = [path]
                timeMap[int(t)] = walksList

    return timeMap


# Generate the connected components for each time step
# For each timestep, create 1D nodesMatrix (array).
# For each node, if a node is active then nodesMatrix[index of node] = 1
# Then create a subgraph that only consists of active nodes and get connected components
def aggregateRandomWalks(timeMap, G):
    numOfNodes = G.number_of_nodes()
    global graphN
    graphN = numOfNodes
    aggregateTimeMap = {}

    for t in timeMap:
        # Make a copy of current graph
        newG = G.copy()

        # Mark active nodes in a 1D matrix
        nodesMatrix = np.zeros((1, numOfNodes), dtype=np.int64)
        for node in timeMap[t]:
            node = list(map(int, node))
            print(node)
            nodesMatrix[0, node] = 1

        # Go through all active nodes and get list of connected components by removing inactive nodes from graph
        i = 0
        while i <= numOfNodes - 1:
            if nodesMatrix[0,i] == 0:
                newG.remove_node(str(i))
            i = i + 1

        # Generate active connected components
        for c in sorted(nx.connected_components(newG), key=len, reverse=True):
            if int(t) in aggregateTimeMap: # if time exists, append its connected component
                aggregateTimeMap[int(t)].append(c)
            else: # if time doesn't exist, add the time with its connected component
                walksList = [c]
                aggregateTimeMap[int(t)] = walksList
        print("--------")

    return aggregateTimeMap


# Save random walks in a txt file for analysis purposes
def saveRandomWalks(walksMap, graphPath):
    inputFile = open(graphPath + '/Data/' + nameFile('randomWalks.txt'), 'w')

    for walk in walksMap:
        # RandomWalk number
        result = walk + "\n"

        # Time duration
        result = result + "\t" + "Time:"
        result = result + "\t\t" + "[" + str(walksMap[walk][0]) + "]\n"

        # Path as a list of nodes
        result = result + "\t" + "Path:"
        result = result + "\t\t" + "[" + str(walksMap[walk][1]) + "]\n"

        # Line break
        result = result + "--------------------------------------------------"

        # print(result)
        inputFile.write(result + "\n")
        # inputFile.close()


# Save random walks per time step in txt
def saveTimeMap(timeMap, walksMap, graphPath):
    inputFile = open(graphPath + '/Data/' + nameFile('syntheticData.txt'), 'w')
    time = 0

    # Go through t = 0 until TS - 1 and list the random-walks for each time step
    while time <= TS - 1:
        # RandomWalk number
        result = "ts_" + str(time) + "\n"

        # Time duration
        result = result + "\t" + "Active Component(s):\n"

        if time in timeMap:
            for walk in timeMap[time]:
                result = result + str("\t\t") + str(walk) + "\n"

        # Line break
        result = result + "--------------------------------------------------"

        # print(result)
        inputFile.write(result + "\n")
        time = time + 1
        # inputFile.close()


# File naming convention, to avoid duplicate names
def nameFile(fname):
    # This creates a timestamped filename so we don't overwrite our good work
    return tStamp + '-' + 'ALPHA'+ str(alpha) +'_TS'+ str(TS) + '_'+fname
    # return tStamp + '-' + 'ALPHA'+ str(activePercent) +'_TS'+ str(TS) + '_'+fname


# File naming convention, to avoid duplicate names
def timeStamp(fmt='%m-%d--%H-%M-%S'):
    import datetime
    # This creates a timestamped filename so we don't overwrite our good work
    return datetime.datetime.now().strftime(fmt).format()


# Generate node data based on active paths. Active node = 1, otherwise = 0
#   folderName: name of folder where graph is stored
#   pathsData: dictionary of active paths from t=0 to t=n
def genInputFile(folderName, timeMap):
    print(timeMap)
    # subFolderName = 'TS' + str(TS)
    # inputFilePath = folderName + '/' + subFolderName

    # check if directory exists
    # isNewDirectory = genDirectories(inputFilePath)

    # create zeros matrix with 'number of nodes (graphN)' rows and 'max time steps (TS)' columns
    # if isNewDirectory:
    CSV = '.csv'
    inputFileName = folderName + '/Data/' + nameFile('input') + CSV

    nodeMatrix = np.zeros((graphN, TS), dtype=np.int64)
    print("graphN = " + str(graphN))

    # Go through t = 0 until TS - 1 and list the random-walks for each time step
    time = 0
    while time <= TS - 1:
        if time in timeMap:
            for walk in timeMap[time]:
                print(walk)
                for node in walk:
                    nodeMatrix[int(node), time] = 1
        time = time + 1

    # convert the matrix into a tab separated file
    np.savetxt(inputFileName, nodeMatrix, delimiter='\t', fmt='%d')

    # return inputFilePath, inputFileName
    return None, None
    # else:

    # return None, None


# generate directory to store data
def genDirectories(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False


main()
