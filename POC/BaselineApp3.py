'''
Naive baseline implementation to solve the problem of maintaining active paths in streaming graphs

1) Generate a small-world graph G with params: n: number of nodes, p: edge wiring probability, k: number of neighbors

2) Keep original graph in memory, and save it as adjacency list in  *.txt file for future analysis

3) Generate synthetic data:
   Create connected components through a number of random-walks on graph G.
   Do not visit the same node per random-walk.
   Start at a node picked uniformly at random, for each iteration, there is probability 'alpha' of choosing a neighbor
   and a probability 'beta = 1 - alpha' of stopping

4) Each random-walk is now assigned a time duration [t, t'], where t' can be adjusted with param k.

5) Now each time step: 0, 1, 2..etc. will have a list of random-walks (i.e. active paths).
   e.g. t1: {[A,B,C], [CDE]}, t2: {[A,B,C], [D,F]}


5) An input file is then generated based on the paths. The input file is a matrix of 0's and 1's.
   node 'i' at timestep 'j' is active if it has value 1 (e.g. inputMatrix[i][j] == 1)

6) For each time step, generate connected components out of the active nodes
'''


import copy
from datetime import datetime
import os
import random
import pandas as pd
from random import choice

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# TODO:
# - Documentation and Clean Code
# - Prepare presentation and report in this order:
#       motivation
#       positioning
#       actual problem
#       different approaches
#       evaluations
# - Add statistics about random walks, graph ..etc.
#   - Average length of random walks
#   - Length of each random walk
#   - Number of connected components
#   -
# - Generate different synthetic data on the same graph. So basically make graph as input
# - Be able to generate output file by taking any input file and graph as input

# ******Goal********:

# Capstone Meeting April 3:
# - Go to 1 node, make it active, then randomly activate 2 of its neighbours
# - you go to these new 2, and do the same.
# - You end up with connected components
#
# - you can keep your generator that has non disjoint paths, it will give you good results
#
#
# Methods:
# - at every time step you know what are active nodes
# - start at 1 active node, run a BFS to discover the rest of active nodes that are connected to it
# - take them out of the total list of all active nodes
# - then repeat
# - Keep track of how much time you can do it
# - then find another method that can find it faster…… for the presentation to work!
#
# - Then do all of that for all time steps
#
# - Then would need to improve this by:
# 	- incrementing or something
# 	- Explore Mahta’s paper

# Distinguish between disjoint non-disjoint paths
# This problem occurs when you have non-disjoint paths so:
# (N * (N – 1)) / 2  = Number of pairs of nodes
# Assume: all paths are disjoint
#       Maintain visited nodes
#




# Work flow:
# 1) Create random walks file and its details
#   a) Include: Length of random walk, duration of random walk, average shortest path
#   b) Eliminate having sub paths like: [a b c] and [a b c d]
#   c) length of random walk should be 4 if alpha = 0.8
#   d) Assumptions: minimum 2 nodes per random-walk, Only
# 2) Create a file showing each time step and its list of paths
# 3) Create a matrix input file
# 4) Repeat the process for the same graph to end up with 3 different input matrix files
# 5) Input: one of the different matrix files, Output: Try to recreate the (each time step, list of paths) file
#   a) you have the graph and you have to find the active nodes by dfs and bfs.
#   b) if you find 1 active then find the active neighbours…etc.
#   c) start from an active node do i have n=other active nodes? no: stop. yes: go to the neighbour and keep going
#   d) if you have a case for an active nodes, you have more than 1 active neighbour
#      it could be a cross path between two paths? need to think about it and draw it

activeNodes = {}

# === GRAPH PARAMETERS ===

# Number of nodes in original graph G
graphN = 50

# Probability of edge rewiring in the original graph G
graphP = 0.01

# Number of k neighbors for each node in the original graph G
graphK = 5

# Number of attempts to create a connected graph
graphTries = 100

# Number of time steps of input
TS = 20

# graphSeed, currently unused
graphSeed = 0

# Number of RandomWalks.
numOfRandomWalks = TS + 3

# Random Walk probability
alpha = 0.8


# === Main Method ===
def main():
    # Generate time for calculating duration of computation
    timeNow = datetime.now()

    # Generate small-world connected undirected graph
    # Public parameters are graphN, graphK, graphP, graphTries
    G = genSampleGraph()

    # Create a graph directory. Directory name is the graph's parameters.
    # Save graph as an adjacency list in a txt file
    graphPath = saveGraph(G)

    # generate random-walks. Do not visit nodes twice
    randomWalks = generateRandomWalks(G)

    # Assign a time step DURATION to each Random Walk.
    # Walk starts at a random t and ends at t + k
    # return walksMap[0] = [t, t + k] and walksMap[1] = [PATH]
    # e.g. randomWalk_1: {[1,3], [A,B,C]}
    walksMap = assignTimeSteps(randomWalks, k=2)

    # Break each time step duration into a single time step.
    # Return a list of random-walks for each single time step
    timeMap  = listByTime(walksMap)
    print("Printing time map!!!!!!!!!!!!!!!!!! ")
    for t in timeMap:
        print(str(t) + ":")
        print(timeMap[t])
        print("===")

    print("FINISHHH time map!!!!!!!!!!!!!!!!!! ")


    # Aggregate random walks for each time step
    aggregateTimeMap = aggregateRandomWalks(timeMap, G)

    for t in aggregateTimeMap:
        print(str(t) + ":")
        print(aggregateTimeMap[t])
        print("===")

    saveRandomWalks(walksMap, graphPath)
    saveTimeMap(aggregateTimeMap, walksMap, graphPath)

    # # Generate node data based on active paths. Active node = 1, otherwise = 0
    inputFilePath, inputFileName = genInputFile(graphPath,walksMap)

    # generate active graphs and store as adjacency list
    genActiveGraphs(inputFilePath, inputFileName, G, TS)
    # #
    # # timeLater = datetime.now()
    # # difference = timeLater - timeNow
    # # print(str(difference.microseconds))
    # # print(G.number_of_edges())


# Generate the connected components for each time step
def aggregateRandomWalks(timeMap, G):
    timeMap2 = {}
    for t in timeMap:
        newG = G.copy()

        # Mark active nodes
        nodesMatrix = np.zeros((1, graphN), dtype=np.int64)
        for node in timeMap[t]:
            print("nooooode"+ str(node))
            nodesMatrix[0, node] = 1

        # Go through all active nodes and get list of connected components
        i = 0
        while i <= graphN - 1:
            if nodesMatrix[0,i] == 0:
                newG.remove_node(i)
            i = i + 1

        for c in sorted(nx.connected_components(newG), key=len, reverse=True):
            if int(t) in timeMap2:
                timeMap2[int(t)].append(c)
            else:
                walksList = [c]
                timeMap2[int(t)] = walksList
        print("--------")

    return timeMap2


# Save graph and get its directory path
def saveGraph(G):

    # folder name includes details of graph: number of nodes and edges, probability p, k neighbors
    # graph tries T (number of times to attempt to generate a connected graph) and seed s if available.
    folderName = 'GRAPHS_' + 'SW_' + 'N' + str(graphN) + '_' + 'E' + str(G.number_of_edges()) + \
                 '_' + 'P' + str(graphP) + '_' + 'K' + str(graphK) + '_' + 'T' + str(graphTries) + '_' + \
                 'S'

    # Generate directory to store the graph
    isNewDirectory = genDirectories(folderName)
    if isNewDirectory:
        inputFile = open(folderName + '/' + 'originalGraph.txt', 'wb')
        nx.write_adjlist(G, path=(folderName + '/' + 'originalGraph.txt'))

        inputFile.close()

    return folderName


# Generate node data based on active paths. Active node = 1, otherwise = 0
#   folderName: name of folder where graph is stored
#   pathsData: dictionary of active paths from t=0 to t=n
def genInputFile(folderName, walksMap):
    subFolderName = 'TS' + str(TS)
    inputFilePath = folderName + '/' + subFolderName

    # check if directory exists
    isNewDirectory = genDirectories(inputFilePath)

    # create zeros matrix with 'number of nodes (graphN)' rows and 'max time steps (TS)' columns
    if isNewDirectory:
        CSV = '.csv'
        inputFileName = inputFilePath + '/' + subFolderName + '_' + 'input' + CSV

        nodeMatrix = np.zeros((graphN, TS), dtype=np.int64)

        for walk in walksMap:
            time = (walksMap[walk][0]).split(",")
            lowerBound = int(time[0])
            upperBound = int(time[1])

            path = walksMap[walk][1]
            for node in path:
                for t in range(lowerBound, upperBound + 1):
                    nodeMatrix[node, t] = 1

        # convert the matrix into a tab separated file
        np.savetxt(inputFileName, nodeMatrix, delimiter='\t', fmt='%d')

        return inputFilePath, inputFileName
    else:
        return None, None


# generate directory to store data
def genDirectories(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False


# Convert input file into an adjacency list and save it
# for each time step: for each node: if the node is inactive, remove it from original graph
# return the original graph with only active nodes
def genActiveGraphs(inputFilePath, inputFileName, G, t):
    outputMap = {}
    if inputFilePath is not None:
        txt = '.txt'
        df = pd.read_csv(inputFileName, skipinitialspace=False, header=None, sep='\t', lineterminator='\n',
                         usecols=[x for x in range(t)])
        nodeNum = 0
        columnNum = 0
        for column in df: # each time step
            newG = G.copy()
            currFilePath = inputFilePath + '/SW_' + 'TS' + str(columnNum) + '_'
            # inputFile = open(currFilePath + txt, 'wb')
            for node in df[column]: # each specific node per time step
                if node == 0:
                    newG.remove_node(nodeNum)
                nodeNum = nodeNum + 1
            nodeNum = 0
            columnNum = columnNum + 1
            for c in sorted(nx.connected_components(newG), key=len, reverse=True):
                if int(column) in outputMap:
                    outputMap[int(column)].append(c)
                else:
                    walksList = [c]
                    outputMap[int(column)] = walksList

        saveTimeMapOutput(outputMap, [], inputFilePath)
    else:
        print("Graph already exists!")


# Generate sample undirected graph with nodes
def genSampleGraph():
    G = nx.connected_watts_strogatz_graph(n=graphN, k=graphK, p=graphP, tries=graphTries)  # small-world
    return G


# Plot graph and save it as png
# not used in this implementation
def plotAndSave(newG, name):
    nx.draw(newG, with_labels=1)
    # print(newG.edges.items())
    # plt.show()
    plt.savefig(name + '_' + 'graph.png')


# Generate a random list of size n
# not used in this implementation
def genRandomValue():
    return random.randint(0, 10) % 2


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


def neighborsToList(neighbors):
    neighbors_list = []
    [neighbors_list.append(neighbor) for neighbor in neighbors]
    print("neighbors to list ..")
    print(neighbors_list)

    return neighbors_list


def iteratorLength(iterator):
    return sum(1 for _ in iterator)


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


def saveRandomWalks(walksMap, graphPath):
    inputFile = open(graphPath + '/' + 'randomWalks.txt', 'w')

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


def saveTimeMap(timeMap, walksMap, graphPath):
    inputFile = open(graphPath + '/' + 'timePerRandomWalks.txt', 'w')
    time = 0
    while time <= TS - 1:
        # RandomWalk number
        result = "ts_" + str(time) + "\n"

        # Time duration
        result = result + "\t" + "RandomWalks:\n"

        if time in timeMap:
            for walk in timeMap[time]:
                result = result + "\t\t"+ str(walk) + "\n"

        # Line break
        result = result + "--------------------------------------------------"

        # print(result)
        inputFile.write(result + "\n")
        time = time + 1
        # inputFile.close()


def saveTimeMapOutput(timeMap, walksMap, graphPath):
    inputFile = open(graphPath + '/' + 'timePerRandomWalksOutput.txt', 'w')
    print("Printing some stuffs:")
    print(timeMap)
    time = 0
    while time <= TS - 1:
        # RandomWalk number
        result = "ts_" + str(time) + "\n"

        # Time duration
        result = result + "\t" + "RandomWalks:\n"

        if time in timeMap:
            for walk in timeMap[time]:
                result = result + "\t\t"+ str(walk) + "\n"

        # Line break
        result = result + "--------------------------------------------------"

        # print(result)
        inputFile.write(result + "\n")
        time = time + 1
        # inputFile.close()


def listByTime(walksMap):
    i = 0
    timeMap = {}

    for walk in walksMap:
        time = (walksMap[walk][0]).split(',')
        lowerBound = int(time[0])
        upperBound = int(time[1])

        path = walksMap[walk][1]
        for t in range(lowerBound, upperBound + 1):
            if int(t) in timeMap:
                timeMap[int(t)].append(path)
            else:
                walksList = [path]
                timeMap[int(t)] = walksList
    return timeMap


main()
