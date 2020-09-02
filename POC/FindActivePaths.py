"""
FindActivePaths.py

Given a graph and an input CSV file, find all active connected components for each time step (naively)

How the algorithm works:

For each time stamp:
    Pick a node uniformly at random from the list of active nodes.

    Run BFS starting on the first node to explore the active component that node belongs to
        Starting at a node, explore all of its active neighbours. Then explore all of the active neighbours' neighbours
        .. .. .. until BFS stops.

        When BFS stops, it means we have found an active component. Repeat for all active components.

    Write the list of active components in an output file

    **Note**: The current implementation is slow because it assumes a connected graph
          Time complexity: O(numOfActiveNodes * (U + V)) which is worst case O(N^2).
          This is slow because multiple BFS run for each active component. To fix this issue, modify the BFS
          implementation to account for a disconnected graph. this is a TODO.

"""
import random
import re
import sys
import timeit
from random import choice

import networkx as nx
import pandas as pd


# Number of time stamps
TS = 100

# Extract graph folder name
graphPath = str(sys.argv[1])

# Extract input file name
fileName = str(sys.argv[2])

# Time stamp of input file, will be used to name the output file
tStamp = re.search("([0-9]{2}\-[0-9]{2}\-\-[0-9]{2}\-[0-9]{2}\-[0-9]{2})", fileName)[0]

# Path of the input file
inputFilePath = graphPath + "/Data/" + fileName

# Create output file. Active components per time stamp will be saved here.
outputFile = open(graphPath + '/Data/' + tStamp + '-BFSOutput.txt', 'w')

def main():

    # Load graph into memory
    graphFile = open(graphPath + "/Graph.txt", 'rb')

    # Read graph from file
    G = nx.read_adjlist(graphFile)

    # Transform input file into a matrix
    inputMatrix = inputFileToMatrix(inputFilePath)

    # Start timer to measure running time
    start = timeit.default_timer()

    # Main method to generate active paths for each time step
    generateActivePaths(G, inputMatrix)

    # Stop timer
    stop = timeit.default_timer()

    # Measure running time
    runningTime = stop - start

    # Add running time to output file
    outputFile.write("Running time: " + str(runningTime * 1000) + " ms")

    outputFile.close()


# Find list of active components at each time stamp using BFS explorations.
# Using the list of active nodes, visit each active node and run BFS to explore its active component.
# Each time an active component is discovered, mark the members of the component as visited. Do  not visit them again.
# Repeat until all of the active nodes have been visited.
#
# @param original G The original graph
# @param inputFile the input file csv
# @return list of active paths per time stamp
def generateActivePaths(originalG, inputMatrix):

    # For each time stamp t
    for t in range(TS):

        # Get list of active nodes
        activeNodesList = getActiveNodesList(inputMatrix, t)

        # Start timer to measure running time
        start = timeit.default_timer()

        # initialize visited nodes list. NOTE: only active nodes will be added here.
        visitedNodes = set()

        # List of active components
        listOfActiveComponents = []

        # For each unvisited active node, run a BFS to find active connected component
        # Note: this is slow for disconnected graphs because it runs BFS multiple times per time stamp
        while len(activeNodesList) > 0:
            # Choose node uniformly at random from list of active nodes
            currentRandomNode = random.sample(activeNodesList, 1)[0]

            # Initialize queue and push initial node
            queue = [str(currentRandomNode)]

            # Mark node as visited
            visitedNodes.add(str(currentRandomNode))

            # BFS to explore active nodes using the original graph
            while len(queue) > 0:
                # Find node first in the queue
                currentNode = queue[0]

                # Find neighbours of current node
                neighbours = set(originalG.neighbors(str(currentNode)))

                # Loop through neighbours
                for neighbour in neighbours:

                    if str(neighbour) in activeNodesList:
                        # If neighbour is active and if neighbor is already visited, leave it.
                        if str(neighbour) in visitedNodes:
                            print("Node already visited!")

                        # If neighbour is active and unvisited:
                        else:
                            # Add neighbour to queue
                            queue.append(str(neighbour))

                            # Mark as visited
                            visitedNodes.add(str(neighbour))

                # Once all neighbours have been exhausted, remove that node from the list of active nodes.
                activeNodesList.remove(currentNode)

                # Pop that node from queue. We will not visit it again.
                queue.pop(0)

            # Once queue is empty, it means that the visited nodes form an active component.
            listOfActiveComponents.append(visitedNodes)

            # clear list of visited nodes for next iteration of BFS.
            visitedNodes = set()

        # Stop timer
        stop = timeit.default_timer()

        # Save active components info in output file
        outputFile.write("ts_" + str(t) + ":\n")
        outputFile.write("\tActive Component(s):\n")

        for component in listOfActiveComponents:
            outputFile.write("\t\t" + str(component) + "\n")

        # Measure running time
        runningTime = stop - start

        outputFile.write("\tRunning time per time stamp: " + str(runningTime * 1000) + " ms" + "\n")
        outputFile.write("--------------------------------------------------\n")


# Transform input file CSV into a matrix of 1's and 0's indicating active and inactive nodes respectively
#
# @param    inputFile a CSV file indicating active and inactive nodes at each time stamp
# @return   a data frame representing a matrix of 1's and 0's
def inputFileToMatrix(inputFile):
    df = pd.read_csv(inputFile, skipinitialspace=False, header=None, sep='\t', lineterminator='\n',
                     usecols=[x for x in range(TS)])
    return df


# Extract the list of active nodes at time t.
# Go through each node at column t in the input matrix and append active nodes (with value '1') to a list. return it.
#
# @param inputMatrix matrix of 1's and 0's indicating active and inactive nodes for all time stamps
# @ return a list of active nodes at time t
def getActiveNodesList(inputMatrix, t):

    # Extract column t from matrix. This is a list of 1's and 0's where the list index is the node number.
    listOfNodes = list(inputMatrix[t])

    # List of active nodes
    activeNodesList = set()

    # Go through each node. If node is active, add it to list of active nodes.
    nodeNumber = 0
    for x in listOfNodes:
        # if node is active, append it to list of active nodes
        if listOfNodes[nodeNumber] == 1:
            activeNodesList.add(str(nodeNumber))

        # Increment nodeNumber
        nodeNumber = nodeNumber + 1

    # return the list of active nodes at time 5
    return activeNodesList


main()