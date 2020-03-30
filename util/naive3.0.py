'''
This is my third attempt at a naive implementation
The code is not being developed any further, refer to BaselineApp.py for newest updates
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
graphN = 10  # number of nodes
graphP = 0.1  # probability of creating edges
graphK = 2  # number of k neighbors for small world
graphTries = 100  # number of tries to get a connected graph
TS = 12  # number of timestamps
graphSeed = 0 # graphSeed

alpha = 0.8 # probability that randomwalk continues


def main():
    timeNow = datetime.now()
    G = genSampleGraph()
    graphPath = saveGraph(G)
    pathsData = generatePaths(G, graphPath)
    for path in pathsData:
        print (path + ": " +  str(pathsData[path]))

    inputFilePath, inputFileName = genInputFile(graphPath,pathsData)

    genActiveGraphs(inputFilePath, inputFileName, G, TS)
    #
    # timeLater = datetime.now()
    # difference = timeLater - timeNow
    # print(str(difference.microseconds))


def saveGraph(G):

    folderName = 'GRAPHS_' + 'SW_' + 'N' + str(graphN) + '_' + 'E' + str(G.number_of_edges()) + \
                 '_' + 'P' + str(graphP) + '_' + 'K' + str(graphK) + '_' + 'T' + str(graphTries) + '_' + \
                 'S'
    isNewDirectory = genDirectories(folderName)
    if isNewDirectory:
        inputFile = open(folderName + '/' + 'originalGraph.txt', 'wb')
        nx.write_adjlist(G, path=(folderName + '/' + 'originalGraph.txt'))

        inputFile.close()

    return folderName


def genInputFile(folderName, pathsData):
    subFolderName = 'TS' + str(TS)
    inputFilePath = folderName + '/' + subFolderName
    isNewDirectory = genDirectories(inputFilePath)

    if isNewDirectory:
        CSV = '.csv'
        inputFileName = inputFilePath + '/' + subFolderName + '_' + 'input' + CSV

        nodeMatrix = np.zeros((graphN, TS), dtype=np.int64)

        for time in pathsData:
            timeRange = time.split(",")
            lowerBound = int(timeRange[0])
            upperBound = int(timeRange[1])

            while lowerBound <= upperBound:
                for node in pathsData[time]:
                    print("Activating index: " + str(node) + "," + str(lowerBound))
                    nodeMatrix[node, lowerBound] = 1

                lowerBound = lowerBound + 1

        np.savetxt(inputFileName, nodeMatrix, delimiter='\t', fmt='%d')
        return inputFilePath, inputFileName
    else:
        return None, None


def genInputFile2(folderName):
    subFolderName = 'TS' + str(TS)
    inputFilePath = folderName + '/' + subFolderName
    isNewDirectory = genDirectories(inputFilePath)

    if isNewDirectory:
        CSV = '.csv'
        inputFileName = inputFilePath + '/' + subFolderName + '_' + 'input' + CSV

        inputFile = open(inputFileName, 'w')
        i = 0
        j = 0
        while i < graphN:
            while j < TS:
                if j == 0:
                    inputFile.write(str(0))
                else:
                    inputFile.write(str(genRandomValue()))
                inputFile.write('\t')
                j = j + 1

            inputFile.write('\n')
            i = i + 1
            j = 0

        inputFile.close()
        return inputFilePath, inputFileName
    else:
        return None, None


def genDirectories(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False


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


# Generate sample undirected graph with  nodes
def genSampleGraph():
    G = nx.connected_watts_strogatz_graph(n=graphN, k=graphK, p=graphP, tries=graphTries)  # small-world
    return G


# Plot graph and save it as png
def plotAndSave(newG, name):
    nx.draw(newG, with_labels=1)
    # print(newG.edges.items())
    # plt.show()
    plt.savefig(name + '_' + 'graph.png')


# Generate a random list of size n
def genRandomValue():
    return random.randint(0, 10) % 2


#
def generatePaths(G, graphPath):
    k = 3 # each path has time interval [t, t+k]
    paths = {}

    i = 0
    while i < TS - 1:
        # paths.append(str(i) + ", " + str(i + k))
        path = randomWalk(G)
        paths[str(i) + "," +str(i + k)] = path
        i = i + k + 1

    return paths


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
    return finalPath

def randomWalk2(G):
    allNodes = G.nodes()
    visitedNodes = {}
    stack = []
    finalPath = []

    # Choose node uniformly at random
    currentRandomNode = choice(list(allNodes))

    # push node into stack and mark as visited
    stack.append(currentRandomNode)
    visitedNodes[currentRandomNode] = True
    finalPath.append(visitedNodes)

    # print ("Node added. Stack: " + str(stack))

    x = 0
    # while x < 2 and len(stack) > 0:
    # Get neighbours of node
    neighbors = G.neighbors(currentRandomNode)
    # print(iteratorLength(neighbors))
    # try :
        # if neighbors is not empty
        # if iteratorLength(neighbors) > 0:
            # print(iteratorLength(neighbors))
            # Choose a neighbor randomly
    randomNeighbor = choice(neighborsToList(neighbors))
            # print(randomNeighbor)

            # make sure neighbor is not visited
        #     while visitedNodes[randomNeighbor]:
        #         neighbors.remove(randomNeighbor)
        #         if iteratorLength(neighbors) > 0:
        #             randomNeighbor = choice(neighbors)
        #         else:
        #             break
        #
        #     if iteratorLength(neighbors) <= 0:
        #         currentRandomNode = backTrack(stack)
        #     else:
        #         # Add random neigbor to stack, mark as visited, and add to final path
        #         stack.append(randomNeighbor)
        #         visitedNodes[randomNeighbor] = True
        #         finalPath.append(randomNeighbor)
        #
        #         # update currentNode
        #         currentRandomNode = randomNeighbor
        #
        # else: # if neighbors is empty, backtrack to previous node
        #     currentRandomNode = backTrack(stack)
    # except:
        # print("error!")

    # x = x + 1
    #     return "random walk!"


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
