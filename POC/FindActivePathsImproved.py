"""
Pseudo code for the set intersection algorithm:

Input:
    G(V, E)
    N X T matrix file

Start:
    Variables:
        1) activeComponents_t-1 = []
        2) activeNodes_t-1 = []
        3) activeNodes_t = []
        4) result = []
        Note: The above are sets of subgraphs.

    Compute 3 sets:

        1) Nodes that were active at t - 1, and stopped being active at t:
            setB = activeNodes_t-1 DIFFERENCE setA
                Remove nodes that are no longer active, and readjust the components (split if needed)

        2) Nodes that were active at t - 1, and remained active at t:
            setA = activeNodes_t-1 INTERSECT activeNodes_t


        3) Nodes that were not active at t - 1, but became active at t:
            setC = activeNodes_t DIFFERENCE setA
                Compute the components of newly  active nodes, merge newly generated components if needed

    Is this correct algorithm?
    Is it faster than the baseline? and in which cases would it be faster?








"""

# TODO: Write on paper and figure out how to choose the correct neighbours
# Keep a list of active nodes
# Keep a list of visited nodes
# WHILE list of active nodes is NOT empty:
# Pick a node at random
# Push to stack
# Add to visited
# WHILE stack is NOT empty:
# Peek on stack and find its neighbours. Loop through neighbours.
# For each neighbour, if it is in the active list: check if visited. If visited: leave it. If unvisited:
# Push unvisited node to stack
# Add unvisited node to visited
# Find its neighbours... repeat.
# if neighbour is not in the active list, leave it
# if all neighbours are either inactive or visited:
# pop stack
# remove that node from the list of active node
# Peek on stack and repeat.


# Read input file
# for each time step (column): for each node (row):
#   if the node is inactive: remove it from original graph
#   if the node is active: Add it into list of activeNodes
# A = [, , , ], G = graph of active nodes
# Now you have:
# 1) Graph with only active nodes
# 2) List of active nodes
#
# Pick a random active node, and run DFS to find all of its active neighbors
# Every time you visit an active node, delete it from the list of activeNodes
# Repeat until the list of activeNodes becomes empty

# Return active connected components for each time step.
# InputFilePath = graph folder name (e.g. GRAPH_SW_N20_E80_P1_K8_T100)
# InputFileName = input file name (e.g. 04-07--07-30-09-input.csv)
# G = original graph
# t = number of timesteps
# TODO:Revisit graph with all its details, write up a pseudocode, update its documentation,
#      and isolate for running time
# TODO: Describe running time complexity theoretically O.
#       See if it validates my current running time for the different graphs
# TODO:
#    - Working baseline
#    - Extensive algorithm running time evaluation

# def genActiveGraphs(inputFilePath, inputFileName, G, t):
#     # Final result
#     outputMap = {}
#
#     # Read input file
#     if inputFilePath is not None:
#         df = pd.read_csv(inputFileName, skipinitialspace=False, header=None, sep='\t', lineterminator='\n',
#                          usecols=[x for x in range(t)])
#         nodeNum = 0
#         columnNum = 0
#         for column in df: # each time step
#             activeNodes = {}
#             newG = G.copy() # copy current graph
#
#             for node in df[column]: # each specific node per time step
#                 # if node is inactive, remove it from graph
#                 if node == 0:
#                     newG.remove_node(str(nodeNum))
#                 else: # if node is active, add it to list of active nodes
#                     activeNodes[str(nodeNum)] = True
#
#                 nodeNum = nodeNum + 1
#             nodeNum = 0
#             columnNum = columnNum + 1
#
#             ####### DFS to find connected components ########
#
#             result_paths = []  # final paths to be returned per time step
#
#             print("Time step: " + str(columnNum))
#             # While list of active nodes is not empty:
#             while len(list(activeNodes.keys())) > 0:
#
#                 # Choose node uniformly at random from active graph newG
#                 currentRandomNode = choice(list(activeNodes.keys()))
#
#                 # Initialize list of visited nodes
#                 visitedNodes = {}
#
#                 # initialize stack
#                 stack = []
#
#                 # push node into stack and mark as visited
#                 stack.append(currentRandomNode)
#                 visitedNodes[currentRandomNode] = True
#
#                 # delete current visited node from list of active nodes
#                 del activeNodes[currentRandomNode]
#
#                 x = 0
#
#                 # Initialize list of nodes in current path
#                 currentPath = []
#                 currentPath.append(currentRandomNode)
#
#                 # Keep visiting nodes inside the stack
#                 while len(stack) > 0:
#
#                     print("Current Node: " + str(currentRandomNode))
#                     print("Stack: " + str(stack))
#                     print("Visited Nodes: " + str(visitedNodes))
#
#                     if currentRandomNode in activeNodes:
#                         del activeNodes[currentRandomNode]
#
#                     # Get neighbours of current node
#                     neighbors = list(newG.neighbors(currentRandomNode))
#
#                     print("Number of Neighbors: " + str(len(neighbors)))
#
#                     # if node has neighbours
#                     if len(neighbors) > 0:
#                         # Choose a neighbor uniformly at random
#                         randomNeighbor = choice(neighbors)
#
#                         # Check if neighbor is visited. If yes:
#                         # remove it from the list of neighbours. Then pick another neighbour.
#                         # Repeat until you have a new neighbour
#                         while randomNeighbor in visitedNodes:
#                             print("Neighbour Exists! now removing: " + str(randomNeighbor))
#                             neighbors.remove(randomNeighbor)
#
#                             if len(neighbors) > 0:
#                                 randomNeighbor = choice(neighbors)
#
#                             # if all neighbours have been exhausted: break
#                             else:
#                                 # currentRandomNode = stack.pop()
#                                 break
#
#                         if len(neighbors) > 0:  # if there exists an unvisited neighbor then add it
#                             # print neighbor
#                             print("Neighbour Found: " + str(randomNeighbor))
#
#                             # Add random neighbor to stack, mark as visited, and add to final path
#                             stack.append(randomNeighbor)
#                             visitedNodes[randomNeighbor] = True
#                             currentPath.append(randomNeighbor)
#                             currentRandomNode = randomNeighbor
#
#                             # Mark current node as visited by deleting from list of active nodes
#                             if currentRandomNode in activeNodes:
#                                 del activeNodes[currentRandomNode]
#                         else:  # if all neighbors are visited, pop stack
#                             stack.pop()
#                             if len(stack) > 0:
#                                 currentRandomNode = stack[len(stack) - 1]
#
#                     # if node has no neighbours left, pop stack
#                     else:
#                         stack.pop()
#                         if len(stack) > 0:
#                             currentRandomNode = stack[len(stack) - 1]
#                 result_paths.append(currentPath)
#
#             # TODO: Just write the components directly to the file without overwhelming memory
#             # Append connected components per time step in a map
#             for c in sorted(result_paths): # for each connected component
#                 if int(column) in outputMap: # if time step exists already, append another connected component to it
#                     outputMap[int(column)].append(c)
#                 else: # else: add the timestep and add its first connected component to it
#                     walksList = [c]
#                     outputMap[int(column)] = walksList
#         return outputMap
#     else:
#         print("Graph already exists!")


# !!!! NOT USED !!!!
# same as genActiveGraphs but with using NetworkX to find connected components
# def genActiveGraphs2(inputFilePath, inputFileName, G, t):
#     outputMap = {}
#     if inputFilePath is not None:
#         txt = '.txt'
#         df = pd.read_csv(inputFileName, skipinitialspace=False, header=None, sep='\t', lineterminator='\n',
#                          usecols=[x for x in range(t)])
#         nodeNum = 0
#         columnNum = 0
#         for column in df: # each time step
#             newG = G.copy()
#             currFilePath = inputFilePath + '/SW_' + 'TS' + str(columnNum) + '_'
#             # inputFile = open(currFilePath + txt, 'wb')
#             for node in df[column]: # each specific node per time step
#                 if node == 0:
#                     newG.remove_node(str(nodeNum))
#                 nodeNum = nodeNum + 1
#             nodeNum = 0
#             columnNum = columnNum + 1
#             for c in sorted(nx.connected_components(newG), key=len, reverse=True):
#                 if int(column) in outputMap:
#                     outputMap[int(column)].append(c)
#                 else:
#                     walksList = [c]
#                     outputMap[int(column)] = walksList
#
#         saveTimeMapOutput(outputMap, inputFilePath)
#     else:
#         print("Graph already exists!")


# For each time step, write the list of active components
# def saveTimeMapOutput(timeMap, graphPath, runningTime):
#     inputFile = open(graphPath + '/Data/' + tStamp + '-NaiveOutput.txt', 'w')
#     print("Printing some stuffs:")
#     print(timeMap)
#     time = 0
#     while time <= TS - 1:
#
#         # Time step
#         result = "ts_" + str(time) + "\n"
#         result = result + "\t" + "Active Component(s):\n"
#
#         # if there exists any active node in time step 'time', print it:
#         if time in timeMap:
#             for path in timeMap[time]:
#                 result = result + "\t\t"+ str(path) + "\n"
#
#         # Line break
#         result = result + "--------------------------------------------------"
#
#         # print(result)
#         inputFile.write(result + "\n")
#         time = time + 1
#         # inputFile.close()
#
#     # Track the running time of this script
#     inputFile.write("Running time: " + str(runningTime) + " seconds")
