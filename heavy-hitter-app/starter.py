# Streaming graph naive linear implementation:

# Generate a random undirected graph with chosen number of nodes
# Each edge starts with the attribute 'active' = 0
# Generate a stream of n elements for each node, and find its heavy hitter 'hh'
# Generate a Dictionary containing heavy hitters as keys, and list of corresponding nodes as values
# loop through dictionary and identify active edges for each node and its neighbours which share the same heavy hitter
# now, every active edge is (active = 1)
# plot graph, where active edges are solid black

# How to improve?

import copy

import networkx as nx
import matplotlib.pyplot as plt
import random
import warnings
from countminsketch import HeavyHitters


warnings.filterwarnings("ignore", category=UserWarning)


def main():
    # Generate sample undirected graph with inactive nodes
    G = genSampleGraph()

    # Generate stream of 20 elements for each node. Each element in the stream belongs to [0, 1, 2,...9]
    # Find the heavy hitter for each node stream
    genAndParseStream(G, 20)

    # Get dictionary containing heavy hitters and their corresponding nodes.
    # e.g. 5 : [node1, node4]
    #      3 : [node2, node6]
    #          ..
    #          ..
    nodeDict = GetNodesDict(G)

    # Loop through heavy hitters in dictionary.
    # If neighbour nodes correspond to the same heavy hitter, label their edge as active (active = 1)
    labelActivePaths(nodeDict, G)

    # Plot graph where active paths are solid black.
    plotAndSave(G)
    displayActivePaths(G)


# Find heavy hitter of a given stream
# width is the maximum output value for each hash function
# depth is the # of hash functions used. The more, the more accurate.
def getHeavyHitter(stream):
    heavyHitter = HeavyHitters(num_hitters=1, width=1000, depth=7)
    for s in stream:
        heavyHitter.add(str(s), 1)

    return next(iter(heavyHitter.heavyhitters))


def displayActivePaths(G):
    print("Edges: ")
    for edge in G.edges().data():
        print(edge)
        print("-------")


# Loop through heavy hitters in dictionary.
# If neighbour nodes correspond to the same heavy hitter, label their edge as active (active = 1)
def labelActivePaths(nodeDict, G):
    for key in nodeDict:
        for node in nodeDict[key]:
            for neighbor in G.neighbors(node):
                if neighbor in nodeDict[key]:
                    G.add_edge(node, neighbor, active=1)


# Get dictionary containing heavy hitter values and their corresponding nodes.
# e.g. 5 : [node1, node4]
#      3 : [node2, node6]
#          ..
#          ..
def GetNodesDict(G):
    NAME_INDEX = 0 # node name index
    DATA_INDEX = 1 # node data index
    nodeDict = {}
    for node in G.nodes().data():
        heavyHitter = node[DATA_INDEX]["hh"]
        nodeDict.setdefault(heavyHitter, []).append(node[NAME_INDEX])

    return dict(nodeDict)


# Generate a stream for each node and get the heavy hitter of that stream
def genAndParseStream(G, n):
    for node in G.nodes():
        stream = genRandomStream(n)
        G.node[node]["stream"] = stream
        G.node[node]["hh"] = getHeavyHitter(stream)

    print("Nodes: ")
    for data in G.nodes().data():
        print(data)
        print("-------")


# Plot graph and save it as png
def plotAndSave(G):
    activeNodes = [(u, v) for (u, v, d) in G.edges(data=True) if d['active'] > 0]
    inActiveNodes = [(u, v) for (u, v, d) in G.edges(data=True) if d['active'] <= 0]

    pos = nx.circular_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=300)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=activeNodes,
                           width=3)
    nx.draw_networkx_edges(G, pos, edgelist=inActiveNodes,
                           width=3, alpha=0.3,  edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')


    plt.axis('off')
    # plt.show()
    # nx.draw(G, with_labels = True)
    plt.savefig('graph.png')


# Generate sample undirected graph with inactive nodes
def genSampleGraph():

    G = nx.gn_graph(20)
    G = G.to_undirected()

    for (u, v) in G.edges():
        G.edges[u, v]['active'] = 0

    return copy.deepcopy(G)


# Generate a random list of size n
def genRandomStream(n):
    return copy.copy([random.randint(0, 9) for x in range(0, n)])


# Generate a random graph with at least 3 edges
def genRandomGraph():
    G = nx.Graph()
    nodes = ["A", "B", "C", "D", "E"]
    maxEdges = (len(nodes) * (len(nodes) - 1))/2
    numOfEdges = random.randint(3, maxEdges)

    i = 0
    while i < numOfEdges:
        node1 = random.randint(0, len(nodes) - 1)
        node2 = random.randint(0, len(nodes) - 1)
        while node1 == node2:
            node2 = random.randint(0, len(nodes) - 1)

        print("node1: %s, node2: %s, num of edges: %d, current edge len: %d"
              % (nodes[node1], nodes[node2], numOfEdges, len(G.edges())))
        if G.has_edge(nodes[node1], nodes[node2]):
            print("nodes are repeated")
            continue

        G.add_edge(nodes[node1], nodes[node2])
        i += 1

    return copy.deepcopy(G)


if __name__ == '__main__':
    main()

