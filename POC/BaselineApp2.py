'''
Naive baseline implementation to solve the problem of maintaining active paths in streaming graphs

1) Generate a small-world graph G with params: n: number of nodes, p: edge wiring probability, k: number of neighbors

2) Keep original graph in memory, and save it as adjacency list in in corresponding *.txt file for future reference

3) Generate synthetic data by creating paths through a random walk on graph G.
   Start at a node picked uniformly at random, for each iteration, there is probability 'alpha' of choosing a neighbor
   and a probability 'beta = 1 - alpha' of stopping

4) Each path is from time [t, t'] where t' can be adjusted with param k.

5) An input file is then generated based on the paths

6) For each time step, an active graph is generated and stored as adjacency list in a *.txt file

7) The files can now be used to generated the connected components of each active graph
   by specifying the filename and executing python3 genConnected.py
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
# - Documentation
# - Prepare presentation and report in this order:
#       motivation
#       positioning
#       actual problem
#       different approaches
#       evaluations
#
# Work flow:
# 1) Create random walks file and its details
#   a) Include: Length of random walk, duration of random walk, average shortest path
#   b) Eliminate having sub paths like: [a b c] and [a b c d]
#   c) length of random walk should be 4 if alpha = 0.8
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
graphN = 30

# Probability of edge rewiring in the original graph G
graphP = 0.01

# Number of k neighbors for each node in the original graph
graphK = 2

# Number of attempts to create a connected graph
graphTries = 100

# Number of time steps of input
TS = 10

# graphSeed, currently unused
graphSeed = 0

# Number of RandomWalks.
numOfRandomWalks = TS + 3

# Random Walk probability
alpha = 0.3


# === Main Method ===
def main():
    # Generate time for calculating duration of computation
    timeNow = datetime.now()

    # Generate small world graph
    G = genSampleGraph()

    # save graph and get its directory path
    graphPath = saveGraph(G)

    # generate synthetic active paths through a random-walk algorithm
    randomWalks = generateRandomWalks(G)

    # Assign a time step to each Random Walk
    walksMap = assignTimeSteps(randomWalks)
    timeMap  = listByTime(walksMap)

    for t in timeMap:
        print(str(t) + ":")
        print(timeMap[t])
        print("--")
    # Aggregate random walks for each time step
    timeMap2 = aggregateRandomWalks(timeMap, G)

    for t in timeMap2:
        print(str(t) + ":")
        print(timeMap2[t])
        print("===")

    saveRandomWalks(walksMap, graphPath)
    saveTimeMap(timeMap2, walksMap, graphPath)

    # Generate node data based on active paths. Active node = 1, otherwise = 0
    inputFilePath, inputFileName = genInputFile(graphPath,walksMap)

    #
    # # generate active graphs and store as adjacency list
    genActiveGraphs(inputFilePath, inputFileName, G, TS)
    #
    # timeLater = datetime.now()
    # difference = timeLater - timeNow
    # print(str(difference.microseconds))
    # print(G.number_of_edges())

def aggregateRandomWalks(timeMap, G):
    timeMap2 = {}
    for t in timeMap:
        newG = G.copy()

        # Mark active nodes
        nodesMatrix = np.zeros((1, graphN), dtype=np.int64)
        for node in timeMap[t]:
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


        # for each time step, switch all active nodes to 1 in the matrix
        # e.g. nodeMatrix[t=1,node=5] = 1
        # for time in pathsData:
        #     timeRange = time.split(",")
        #     lowerBound = int(timeRange[0])
        #     upperBound = int(timeRange[1])
        #
        #     while lowerBound <= upperBound:
        #         for node in pathsData[time]:
        #             # print("Activating index: " + str(node) + "," + str(lowerBound))
        #             nodeMatrix[node, lowerBound] = 1
        #
        #         lowerBound = lowerBound + 1

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
            # nx.write_adjlist(newG, path=(currFilePath + txt))
            # os.rename(currFilePath + txt,
            #           currFilePath + 'N' + str(newG.number_of_nodes()) + '_' + 'E' + str(newG.number_of_edges()) + txt)
            # inputFile.close()
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


# generate active paths through random-walk
# return dictionary of active paths (e.g. {
#                                           't=0,t=2' : [node 1, node 2, node 6]
#                                           't=3,t=4 : [node 6, node 3]
#                                         })
def generateRandomWalks(G):
    k = 3 # each path has time interval [t, t + k]
    randomWalks = []
    i = 1
    while i <= numOfRandomWalks:
        walk = randomWalk(G)
        randomWalks.append(walk)
        i = i + 1

    return randomWalks


# random-walk on graph G with probability alpha
def randomWalk(G):
    allNodes = G.nodes()
    visitedNodes = {}
    stack = []
    finalPath = []

    # Choose node uniformly at random
    currentRandomNode = choice(list(allNodes))

    # push node into stack and mark as visited
    stack.append(currentRandomNode)
    visitedNodes[currentRandomNode] = True
    finalPath.append(currentRandomNode)


    x = 0
    while len(stack) > 0 and generateProbability():

        print("Current Node: " + str(currentRandomNode))
        print("Stack: " + str(stack))
        print("Visited Nodes: " + str(visitedNodes))

        # Get neighbours of node
        neighbors = list(G.neighbors(currentRandomNode))

        print("Number of Neighbors: " + str(len(neighbors)))

        # if neighbors is not empty
        if len(neighbors) > 0:
            # Choose a neighbor randomly
            randomNeighbor = choice(neighbors)

            # Check if neighbor is visited, if it is, look for another neighbor
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
                finalPath.append(randomNeighbor)
                currentRandomNode = randomNeighbor
            else: # if all neighbors are visited, back track to previous node
                currentRandomNode = stack.pop()

        x = x + 1
        print("==========")
        print(str(len(stack)))
    return finalPath


def backTrack(stack):
    return stack.pop()


def neighborsToList(neighbors):
    neighbors_list = []
    [neighbors_list.append(neighbor) for neighbor in neighbors]
    print("neighbors to list ..")
    print(neighbors_list)

    return neighbors_list


def iteratorLength(iterator):
    return sum(1 for _ in iterator)


def generateProbability():
    maxInt = 100
    num = random.randint(1, maxInt)
    alphaProbability = alpha * maxInt
    if num <= alphaProbability:
        return True
    elif num > alphaProbability or num <= maxInt:
        return False


# Assign each random-walk a random time step with a fixed k duration
# e.g. [randomwalk1] -> [t, t + k]
def assignTimeSteps(randomWalks):
    # Store random-walk -> time step
    randomWalksMap = {}

    # Max time steps
    maxTime = TS - 1

    # k time steps parameter
    k = 2

    i = 1
    # Assign random walks
    for walk in randomWalks:
        # Generate a start time step uniformly at random from [1, max time steps]
        startTime = random.randint(1, maxTime)

        # Add k time steps
        endTime = startTime + k

        # If endTime is out of bounds: endTime = maxTime
        if endTime > maxTime:
            endTime = maxTime

        timeStep = str(startTime) + "," + str(endTime)
        path = walk

        randomWalksMap["RandomWalk_" + str(i)] = [timeStep, path]
        i = i + 1


    print("I am assigning random walks now!")
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

    # for time in timeMap:
    #     # RandomWalk number
    #     result = "ts_"+ str(time) + "\n"
    #
    #     # Time duration
    #     result = result + "\t" + "RandomWalks:\n"
    #
    #     for walk in timeMap[time]:
    #         result = result + "\t\t"+ str(walk) + "\n"
    #
    #     # Line break
    #     result = result + "--------------------------------------------------"
    #
    #     # print(result)
    #     inputFile.write(result + "\n")
    #     # inputFile.close()


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

    # for time in timeMap:
    #     # RandomWalk number
    #     result = "ts_"+ str(time) + "\n"
    #
    #     # Time duration
    #     result = result + "\t" + "RandomWalks:\n"
    #
    #     for walk in timeMap[time]:
    #         result = result + "\t\t"+ str(walk) + "\n"
    #
    #     # Line break
    #     result = result + "--------------------------------------------------"
    #
    #     # print(result)
    #     inputFile.write(result + "\n")
    #     # inputFile.close()


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
