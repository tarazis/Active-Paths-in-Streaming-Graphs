"""
DensityGenerator.py

Generate an input matrix with a pre-defined density of active nodes across the whole matrix.
For example, density = 0.05 creates a matrix with 5% of matrix entries are 1's while the rest are 0's. The 1's are
randomly distributed across the matrix.


"""

import datetime
import sys

import networkx as nx
import numpy as np

# Get graph path from input
graphPath = str(sys.argv[1])

# percentage of active nodes across the matrix
density = 0.05

# Number of time steps
TS = 1000

# Unique file name prefix
tStamp = datetime.datetime.now().strftime('%m-%d--%H-%M-%S').format()


def main():

    # Get number of nodes
    numOfNodes = getNumberOfNodes()

    # Generate input matrix with specified number of nodes, number of time stamps, and percentage of active nodes
    inputMatrix = generateInputMatrix(numOfNodes)

    # Generate CSV file containing the input matrix
    generateInputFile(inputMatrix)


def getNumberOfNodes():
    # Load graph into memory
    graphFile = open(graphPath + "/Graph.txt", 'rb')

    # Read graph from file
    G = nx.read_adjlist(graphFile)

    # Assign number of nodes dynamically
    numOfNodes = G.number_of_nodes()

    return numOfNodes


def generateInputMatrix(numOfNodes):

    # Create a zeros matrix
    matrix = np.zeros((numOfNodes, TS), dtype=np.int64)

    # calculate the number of active nodes by calculating: density * number of entries.
    count_target = int(round(numOfNodes * TS * density))

    # Keep track of the number of 1's entered so far
    count = 0
    while count < count_target:
        # Choose a random row
        row_random = np.random.randint(0, numOfNodes)

        # Choose a random column
        col_random = np.random.randint(0, TS)

        # If entry at [row_random][col_random] is inactive, make it active
        if matrix[row_random][col_random] == 0:
            matrix[row_random][col_random] = 1
            count = count + 1

    return matrix


def generateInputFile(matrix):
    CSV = '.csv'
    inputFileName = graphPath + '/Data/' + nameFile('input') + CSV
    np.savetxt(inputFileName, matrix, delimiter='\t', fmt='%d')


# File naming convention, to avoid duplicate names
def nameFile(fname):
    # This creates a timestamped filename so we don't overwrite our good work
    return tStamp + '-' + 'DENSITY' + str(density) + '_TS' + str(TS) + '_' + fname

main()