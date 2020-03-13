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

activeNodes = {}
graphN = 1000  # number of nodes
graphP = 0.1  # probability of creating edges
graphK = 4  # number of k neighbors for small world
graphTries = 100  # number of tries to get a connected graph
TS = 100  # number of timestamps
graphSeed = 0 # graphSeed

alpha = 0.9 # probability that random-walk continues


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
    while len(stack) > 0 and random.uniform(0, 1) <= alpha:

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

main()
