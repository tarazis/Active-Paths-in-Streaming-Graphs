import copy
from datetime import datetime
import os
import random
import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt


activeNodes = {}
graphN = 1000  # number of nodes
graphP = 0.1  # probability of creating edges
graphK = 4  # number of k neighbors for small world
graphTries = 100  # number of tries to get a connected graph
TS = 1000  # number of timestamps
graphSeed = 0 # graphSeed


def main():
    timeNow = datetime.now()
    G = genSampleGraph()
    graphPath = saveGraph(G)
    inputFilePath, inputFileName = genInputFile(graphPath)
    genActiveGraphs(inputFilePath, inputFileName, G, TS)

    timeLater = datetime.now()
    difference = timeLater - timeNow
    print(str(difference.microseconds))


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


def genInputFile(folderName):
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




main()
