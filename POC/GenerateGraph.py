"""
Project: Finding Active Paths in Streaming Graph

Graph Generator

GenerateGraph():

Generate a sample connected graph and save it as an adjacency list in *.txt file.
The graph is then used for applying the naive implementation on different sets of synthetic data.

The following code generates a connected small-world graph G with params:
    n: number of nodes
    p: edge wiring probability
    k: number of neighbors

@author Sami Tarazi
"""

# Number of nodes in original graph G
import os

import networkx as nx
import matplotlib.pyplot as plt

graphN = 20

# Probability of edge rewiring in the original graph G
graphP = 0.15

# Number of k neighbors for each node in the original graph G
graphK = 8

# Number of attempts to create a connected graph
graphTries = 100


def main():

    # Generate small-world connected undirected graph with specified params
    G = genSampleGraph()

    # Create a graph directory. Directory name is the graph's parameters.
    # Save graph as an adjacency list in a txt file
    graphPath = saveGraph(G)


# Generate a connected undirected Small-world graph
# graphN: Number of nodes
# graphK: Number of neighbors per node
# graphP: Edge wiring probability
# graphTries: Number of tries to create a connected graph
def genSampleGraph():
    G = nx.connected_watts_strogatz_graph(n=graphN, k=graphK, p=graphP, tries=graphTries)  # small-world

    # nx.draw(G, node_size=100, pos=nx.circular_layout(G))
    # plt.show()
    return G


# Save graph as adjacency list and return its directory path
def saveGraph(G):
    numOfNodes = G.number_of_nodes()
    numOfEdges = G.number_of_edges()
    probabilityP = graphP
    numOfNeighbours = graphK if graphK % 2 == 0 else graphK - 1
    numOfTries = graphTries
    avgNodeDegree = getAvgNodeDegree(G, numOfNodes)

    # folder name includes details of graph:
    # Number of Nodes
    # Number of Edges
    # Probability p
    # Number of Neighbors per Node
    # Seed (if applicable)
    folderName = 'GRAPH_' + 'SW_' + 'N' + str(numOfNodes) + '_' + 'E' + str(numOfEdges) + \
                 '_' + 'P' + str(probabilityP) + '_' + 'K' + str(numOfNeighbours) + '_' + 'T' + str(numOfTries)

    # True if directory is newly created. False, if it already exists.
    isNewDirectory = genDirectories(folderName)

    # If directory has just been created, store graph in it
    # First, store graph adjacency list in Graph.txt
    # Second, Store graph params in GraphDetails.txt
    # Third, Append Graph.txt to GraphDetails.txt
    if isNewDirectory:
        graphFile = folderName + '/' + 'Graph.txt'
        detailsFile = folderName + '/' + 'GraphDetails.txt'

        # Store graph adjacency list in temporary file
        inputFile = open(graphFile, 'wb')
        nx.write_adjlist(G, path=graphFile)
        inputFile.close()

        # Store graph params and stats in main file
        inputFile = open(detailsFile, 'w')
        paramString = "# Number of Nodes (graphN) = " + str(numOfNodes) + "\n"
        paramString += "# Number of Neighbours per Node before Rewiring (graphK) = " + str(numOfNeighbours) + "\n"
        paramString += "# Rewiring Probability (graphP) = " + str(probabilityP) + "\n"
        paramString += "# Number of Tries (graphTries) = " + str(graphTries) + "\n"
        paramString += "# Number of Edges = " + str(numOfEdges) + "\n"
        paramString += "# Average Node Degree = " + str(avgNodeDegree) + "\n"
        paramString += "\n\n"

        inputFile.write(paramString)
        inputFile.close()

        # Append contents of graph file into details file
        with open(detailsFile, 'a') as detailsLines, open(graphFile, 'r') as graphLines:
            # for each line in the temp file, append it to main file
            for line in graphLines:
                detailsLines.write(line)
    else:
        print("Error: Graph with the same parameters exists")
    return folderName


# generate directory at specified path
# if directory exists, return false.
# if directory does not exist, create it and return true.
def genDirectories(path):
    if not os.path.exists(path):
        os.makedirs(path)
        os.makedirs(path + '/Data')
        return True
    else:
        return False


# Generate the average node degree
def getAvgNodeDegree(G, numOfNodes):
    avgNodeDegree = 0
    for (node, val) in G.degree(): # loop through nodes and their corresponding degree
        avgNodeDegree += val

    return avgNodeDegree/numOfNodes

main()