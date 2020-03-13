import networkx as nx
import matplotlib.pyplot as plt


def main():
    graphN = 10  # number of nodes
    graphP = 0.1  # probability of creating edges
    graphK = 2  # number of k neighbors for small world
    inputFile = open('testGraphs' + '/' + 'testExpected.txt', 'rb')
    print("--- Generating Connected Components ---")
    G = nx.read_adjlist(inputFile)
    print("Number of Nodes = " + str(G.number_of_nodes()))
    print("Number of Edges = " + str(G.number_of_edges()))

    inputFile.close()

    print("\nActive Components:")
    [print(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]


main()