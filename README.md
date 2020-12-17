# Learning Active Paths in Streaming Graphs Project
Baseline implementation for finding active connected components in streaming graphs

## How to run:
1. Download code to your local machine

1. Run Terminal in EECS4080/POC

1. Generate your graph by doing the following:
    1. Edit *GenerateGraph.py* to choose graph parameters: *graphN*, *graphP*, *graphK* respectively referring to # of nodes, edge re-wiring probability, and # of neighbours per node.
    1. Generate a graph by running the following command: `python3 GenerateGraph.py` The graph will be saved in the current directory
    
1. Generate input file by running: `python3 DensityGenerator.py <graph folder name>`, for example:
    1. `python3 DensityGenerator.py GRAPH_SW_N20_E80_P0.15_K8_T100`
    1. The input file and synthetic data will be saved in /EECS4080/GRAPH_SW_N20_E80_P0.15_K8_T100/Data
    1. You can generate as many of this as you need, they will always be random
    1. You can always manipulate the parameter *density* in order to generate longer random-walks
    
1. Given a graph and an input file:  Find active paths (active connected components) by by executing `python3 FindActivePaths.py <graph folder name> <input file name.csv>`, for example:
    1. `python3 FindActivePaths.py GRAPH_SW_N20_E80_P0.15_K8_T100 04-18--16-57-47-input.csv`
    1. A file named *04-18--16-57-47-BFS-Output.txt* will be generated under /EECS4080/GRAPH_SW_N20_E80_P0.15_K8_T100/Data

## How the algorithm works

1. Generate a connected small world graph with parameters n, p, and k.
2. The graph is now a static graph consisting of nodes and edges
3. The graph is saved on the harddrive in an adjacency list representation

4. Generate a zeros matrix where columns are timestamps and rows are nods
5. Choose a density (e.g. 0.05)
6. Turn 5% of the matrix to 1



  
