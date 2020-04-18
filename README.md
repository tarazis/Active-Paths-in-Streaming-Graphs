# EECS4080
Baseline implementation for finding active connected components in streaming graphs

## How to run:
1. Download code to your local machine
1. Run Terminal in EECS4080/POC
1. Generate your graph by doing the following:
    1. Edit *GenerateGraph.py* to choose graph parameters: *graphN*, *graphP*, *graphK* respectively referring to # of nodes, edge re-wiring probability, and # of neighbours per node.
    1. Generate a graph by running the following command: `python3 GenerateGraph.py` The graph will be saved in the current directory
1. Generate input file by running: `python3 GenerateData.py <graph folder name>`, for example:
    1. `python3 GenerateData.py GRAPH_SW_N20_E80_P0.15_K8_T100`
    1. The input file and synthetic data will be saved in /EECS4080/GRAPH_SW_N20_E80_P0.15_K8_T100/Data
    1. You can generate as many of this as you need, they will always be random
1. Find active paths (active connected components) by specifying by executing: `python3 FindActivePaths.py <graph folder name> <input file name.csv> `, for example:
    1. `python3 FindActivePaths.py GRAPH_SW_N20_E80_P0.15_K8_T100 04-18--16-57-47-input.csv`
    1. A file named *04-18--16-57-47-Output.txt* will be generated under /EECS4080/GRAPH_SW_N20_E80_P0.15_K8_T100/Data
1. Input file


  
