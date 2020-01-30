import copy
import os
import random
import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt

'''
1) Graph Parameters:
    - nodes = 100, p = 0.3 (0.5) (0.9) , k = 10 (50) (90) 
    - nodes = 1000, p = 0.3 (0.5) (0.9) , k = 100 (500) (900)
    - nodes = 10000, p = 0.3 (0.5) (0.9), k = 1000 (5000) (10000)
    
    repeat for 100, 1000, 10000 time steps
    
2) What should the original graph file include? other files?

3) 10,000 is not efficient how to make efficient?
'''

activeNodes = {}
graphN = 100 # number of nodes
graphP = 0.3 # probability of creating edges
graphSeed = 7
graphK = 10 # number of k neighbors for small world
graphTries = 100 # number of tries to get a connected graph
TS = 1000 # number of timestamps


def main():
    random.seed(graphSeed)
    G = genSampleGraph()
    graphPath = saveGraph(G)
    inputFilePath, inputFileName = genInputFile(G, graphPath)
    # fileName = genInputFile(G)
    for x in range(TS):
        newG = genActiveGraph(inputFilePath, inputFileName, G, x)





    # activeNodes = findActiveNodes(fileName)
    # print(activeNodes)
    # newG = findActivePaths('t1', G, activeNodes)
    # print(nx.connected_components(newG))

    # genAndParseStream(G, 20)
    # findActivePaths(G)
    #
    # plotAndSave(G, 'original')


def saveGraph(G):
    folderName = 'GRAPHS_' + 'SW_' + 'N' + str(graphN) + '_' + 'E' + str(G.number_of_edges()) +\
                 '_' + 'P' + str(graphP) + '_' + 'K' + str(graphK) + '_' + 'T' + str(graphTries) + '_' +\
                 'S' + str(graphSeed)

    genDirectories(folderName)
    inputFile = open(folderName + '/' + 'originalGraph.txt', 'w')
    inputFile.write('----- Edge List -----\n')
    edgeList = nx.generate_edgelist(G, data=False)
    for edge in edgeList:
        inputFile.write(edge + '\n')

    inputFile.close()
    return folderName

# Generate sample undirected graph with 10 nodes
def genSampleGraph2():
    G = nx.gn_graph(n)
    G = G.to_undirected()

    # for (u, v) in G.edges():
    #     G.edges[u, v]['active'] = 0

    return copy.deepcopy(G)


def genInputFile(G, folderName):
    subFolderName = 'TS' + str(TS)
    inputFilePath = folderName + '/' + subFolderName
    genDirectories(inputFilePath)

    CSV = '.csv'
    inputFileName = inputFilePath + '/' + subFolderName + '_' + 'input' + CSV

    inputFile = open(inputFileName, 'w')
    # print(inputFileName)
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


def genDirectories(path):
    if not os.path.exists(path):
        os.makedirs(path)


def genActiveGraph(inputFilePath, inputFileName, G, t):

    currFilePath = inputFilePath + '/SW_' + 'TS' + str(t) + '_'
    txt = '.txt'
    newG = G.copy()
    df = pd.read_csv(inputFileName, skipinitialspace=False, header=None, sep='\t', lineterminator='\n',
                     usecols=[t])
    nodeNum = 0
    columnNum = 0
    for column in df:
        inputFile = open(currFilePath + txt, 'w')
        inputFile.write("Active Nodes:\n")
        for node in df[column]:
            if node == 0:
                newG.remove_node(nodeNum)
                # print("Remove node: " + str(nodeNum))
                # inputFile.write(str(nodeNum) + '\n')
            else:
                inputFile.write(str(nodeNum) + '\n')
            nodeNum = nodeNum + 1
        # plotAndSave(newG, 'ts' + str(columnNum))
        nodeNum = 0
        columnNum = columnNum + 1
        inputFile.write('----- Edge List -----\n')
        edgeList = nx.generate_edgelist(newG, data=False) # create my own method? or use write_edgelist
        for edge in edgeList:
            inputFile.write(edge + '\n')
        # print(newG.nodes.items())
        # plotAndSave(newG, fileName2)
        os.rename(currFilePath + txt, currFilePath + 'N' + str(newG.number_of_nodes()) + '_' + 'E' + str(newG.number_of_edges()) + txt)
        inputFile.close()

    inputFile.close()

    return newG


# def findActiveNodes(fileName):
#     invertedIndex = {}
#     df = pd.read_csv(fileName, skipinitialspace=False, header=None, sep='\t', lineterminator='\n',
#                      usecols=[x for x in range(10)])
#     nodeNum = 0
#     columnNum = 0
#     active = []
#     for column in df:
#         for node in df[column]:
#             if node == 1:
#                 # print("node" + " " + str(nodeNum) + " is active" )
#                 active.append(nodeNum)
#             nodeNum = nodeNum + 1
#         nodeNum = 0
#         invertedIndex["t" + str(columnNum)] = copy.deepcopy(active)
#         active = []
#         columnNum = columnNum + 1
#
#     return invertedIndex


# Generate sample undirected graph with  nodes
def genSampleGraph():
    G = nx.connected_watts_strogatz_graph(n=graphN, k=graphK, p=graphP, tries=graphTries, seed=graphSeed) # small-world
    return copy.deepcopy(G)


# Plot graph and save it as png
def plotAndSave(newG, name):
    nx.draw(newG, with_labels=1)
    # print(newG.edges.items())
    # plt.show()
    plt.savefig(name + '_' + 'graph.png')


# Generate a 0 or 1 for every time step
def genAndParseStream(G, n):
    t = 0

    while t <= 0:
        for node in G.nodes():
            value = genRandomValue()
            addValueToNode(G, node, value)

        t = t + 1

        # G.node[node]["hh"] = getHeavyHitter(stream)

    print("Nodes: ")
    for data in G.nodes().data():
        print(data)
        print("-------")

    print(activeNodes)


# Generate a random list of size n
def genRandomValue():
    return random.randint(0, 10) % 2


# Append 0 or 1 to node
def addValueToNode(G, node, value):
    streamList = [value]
    if len(G.node[node]) == 0:
        G.node[node]["stream"] = streamList
    else:
        (G.node[node]["stream"]).append(value)

    if value == 1:
        activeNodes.append(node)


def findActivePaths(time, G, activeNodes):
    originalG = nx.generate_edgelist(G, data=False)
    newG = nx.Graph()
    newG.to_undirected()
    # if 0 in activeNodes[time]:
    #     print(activeNodes[time])
    for edge in originalG:
        if int(edge[0]) in activeNodes[time]:
            if int(edge[2]) in activeNodes[time]:
                newG.add_edge(edge[0], edge[2])

    for edge in originalG:
        print(edge)

    for edge in nx.generate_edgelist(newG, data=False):
        print(edge)

    return newG



def findActivePaths2(G):
    newG = copy.deepcopy(G)

    for node in G.nodes():
        if node not in activeNodes:
            newG.remove_node(node)

    for node in activeNodes:
        print("--------")
        # print("Path between: " + str(activeNodes[0]) + ", " + str(node))
        try:
            print (nx.shortest_path(newG, source=activeNodes[0], target=node))
        except:
            print("no path")
        # print("--------")



main()
