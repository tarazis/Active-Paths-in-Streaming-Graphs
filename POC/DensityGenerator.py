import datetime
import sys

import networkx as nx
import numpy as np

# Get graph path from input
graphPath = str(sys.argv[1])

# percentage of active nodes across the matrix
density = 0.1

# Number of time steps
TS = 1000

# File name prefix
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

    matrix = np.zeros((numOfNodes, TS), dtype=np.int64)
    count_target = int(round(numOfNodes * TS * density))

    count = 0
    while count < count_target:
        row_random = np.random.randint(0, numOfNodes)
        col_random = np.random.randint(0, TS)
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