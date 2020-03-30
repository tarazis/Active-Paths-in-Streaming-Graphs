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

# Work flow:
# 1) Create a small-world graph (Connected)
# 2) Create at least TS random walks
# 3) Save all random walks in a file
# 4) Assign each random-walk a time step
# 5) Save a file showing all random walks and all timesteps assigned to it
# 6) Save a file showing all time steps and all random walks assigned to it
# 7) Create an input file matrix like before
# 8) Generate the active sub graphs by removing inactive edges

# 9) From the input file, re-generate the random-walks with timestep file!!!!


# Notes:
# - Document file
# - Add github users
# - Prepare presentation in this order:
#       motivation
#       positioning
#       actual problem
#       different approaches
#       evaluations
# 8)
# 2) Create a file of each time step with the list of random walks
#   a) Specify the number of random walks ( > time steps)
#   b) Specify that Alpha or beta used
#   c) Specify Number of edges, nodes, ..etc.
#   d) Each randomwalk will be assigned a random time step
#       e.g. randomWalk1 -> ts_1 to ts_3, randomWalk2 -> ts_2 to ts_10 ...etc.
#   e) Save file that contains each time step with a list of its random walks

# 3) Create the input file matrix from the random walks file

# 4) Generate

# To Do:
#   1) Specify Number of Random Walks
#   2) Save the output of Random Walks in a file:
#       save: number of random walks, alpha/beta details,
# number of randomwalks()
# save randomwalks in file
# every random walk wil be assigned to a timestep, time step can have multiple randomwalks!! and can intersect
# record useful statistics for each random walk
# Create 1 graph and create its input file that shows for each timestep there will be

# create a baseline method that generates the synthetic data all over just from the input file
# (input file has timesteps and list of randomwalks)
#
#hexken
#mahto0o
#
# Add more documentation
# Prepare presentation


activeNodes = {}
graphN = 100  # number of nodes
graphP = 0.1  # probability of creating edges
graphK = 5  # number of k neighbors for small world
graphTries = 100  # number of tries to get a connected graph
TS = 10  # number of timestamps
graphSeed = 0 # graphSeed

alpha = 0.8 # probability that random-walk continues


def main():
    timeNow = datetime.now()

    # Generate small world graph
    G = genSampleGraph()

    # save graph and get its directory path
    graphPath = saveGraph(G)

    # generate synthetic active paths through random-walk
    pathsData = generatePaths(G)
    for path in pathsData:
        print (path + ": " +  str(pathsData[path]))

    # Generate node data based on active paths. Active node = 1, otherwise = 0
    inputFilePath, inputFileName = genInputFile(graphPath,pathsData)

    # generate active graphs and store as adjacency list
    genActiveGraphs(inputFilePath, inputFileName, G, TS)

    timeLater = datetime.now()
    difference = timeLater - timeNow
    print(str(difference.microseconds))
    print(G.number_of_edges())


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
def genInputFile(folderName, pathsData):
    subFolderName = 'TS' + str(TS)
    inputFilePath = folderName + '/' + subFolderName

    # check if directory exists
    isNewDirectory = genDirectories(inputFilePath)

    # create zeros matrix with 'number of nodes (graphN)' rows and 'max time steps (TS)' columns
    if isNewDirectory:
        CSV = '.csv'
        inputFileName = inputFilePath + '/' + subFolderName + '_' + 'input' + CSV

        nodeMatrix = np.zeros((graphN, TS), dtype=np.int64)

        # for each time step, switch all active nodes to 1 in the matrix
        # e.g. nodeMatrix[t=1,node=5] = 1
        for time in pathsData:
            timeRange = time.split(",")
            lowerBound = int(timeRange[0])
            upperBound = int(timeRange[1])

            while lowerBound <= upperBound:
                for node in pathsData[time]:
                    # print("Activating index: " + str(node) + "," + str(lowerBound))
                    nodeMatrix[node, lowerBound] = 1

                lowerBound = lowerBound + 1

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
    if inputFilePath is not None:
        txt = '.txt'
        df = pd.read_csv(inputFileName, skipinitialspace=False, header=None, sep='\t', lineterminator='\n',
                         usecols=[x for x in range(t)])
        nodeNum = 0
        columnNum = 0
        for column in df: # each time step
            newG = G.copy()
            currFilePath = inputFilePath + '/SW_' + 'TS' + str(columnNum) + '_'
            inputFile = open(currFilePath + txt, 'wb')
            for node in df[column]: # each specific node per time step
                if node == 0:
                    newG.remove_node(nodeNum)
                nodeNum = nodeNum + 1
            nodeNum = 0
            columnNum = columnNum + 1
            nx.write_adjlist(newG, path=(currFilePath + txt))
            os.rename(currFilePath + txt,
                      currFilePath + 'N' + str(newG.number_of_nodes()) + '_' + 'E' + str(newG.number_of_edges()) + txt)
            inputFile.close()
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
def generatePaths(G):
    k = 3 # each path has time interval [t, t + k]
    paths = {}
    i = 0
    while i < TS - 1:
        path = randomWalk(G)
        paths[str(i) + "," +str(i + k)] = path
        i = i + k + 1

    return paths


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
    maxInt = 1000
    num = random.randint(1, maxInt)
    alphaProbability = alpha * maxInt
    if num <= alphaProbability:
        return True
    elif num > alphaProbability and num <= maxInt:
        return False
main()
