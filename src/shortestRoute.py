import os
import sys
import inspect
import heapq

from utils.constants import DISTRIBUTION_CENTER_MAP
from routeSetup import ad_matrix, display_matrix
from itertools import permutations

# Setting parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

# importing from parent directory
from tests.test_routeSetup import test_payload

# implementation of traveling Salesman Problem 
# https://www.geeksforgeeks.org/traveling-salesman-problem-tsp-implementation/
def travellingSalesmanProblem(graph, locations, s):
    V=len(graph)

    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    min_path = sys.maxsize
    next_permutation=permutations(vertex)
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0
        current_dest = []

        # compute current path weight
        k = s
        for j in i:
            current_dest +=  [locations[k]]
            current_pathweight += graph[k][j]
            k = j
        current_dest += [locations[k]]
        current_pathweight += graph[k][s]

        # update minimum
        if min_path > current_pathweight:
            min_path = current_pathweight
            res = current_dest
        
    return (res, min_path)

def assign_to_warehouse(payload):
    
    candidates = []
    
    for center in DISTRIBUTION_CENTER_MAP:
        matrix, location_map = ad_matrix(payload, center)
        print("#"*50)
        print(display_matrix(matrix, location_map))
        print("#"*50)
        location = list(location_map.values())
        
        candidates.append(travellingSalesmanProblem(matrix, location, 0))
    return min(candidates)

if __name__ == "__main__":
    print(assign_to_warehouse(test_payload))