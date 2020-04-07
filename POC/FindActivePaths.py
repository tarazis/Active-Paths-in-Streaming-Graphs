import re
import sys

import networkx as nx
import pandas as pd


TS = 20

# Get graph path from input
graphPath = str(sys.argv[1])
fileName = str(sys.argv[2])
tStamp = re.search("([0-9]{2}\-[0-9]{2}\-\-[0-9]{2}\-[0-9]{2}\-[0-9]{2})", fileName)[0]


inputFilePath = graphPath + "/Data/" + fileName

def main():
    # print(tStamp)
    # Load graph into memory
    graphFile = open(graphPath + "/Graph.txt", 'rb')
    G = nx.read_adjlist(graphFile)
    genActiveGraphs(graphPath, inputFilePath, G, TS)


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
                    newG.remove_node(str(nodeNum))
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


def saveTimeMapOutput(timeMap, walksMap, graphPath):
    inputFile = open(graphPath + '/Data/' + tStamp + '-timePerRandomWalksOutput.txt', 'w')
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


main()