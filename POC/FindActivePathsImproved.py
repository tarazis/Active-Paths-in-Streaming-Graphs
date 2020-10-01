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

    Is this a correct algorithm?
    Is it faster than the baseline? and in which cases would it be faster?
"""