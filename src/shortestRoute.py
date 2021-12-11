import os
import sys
import inspect
import heapq
from routeSetup import ad_matrix, display_matrix

# Setting parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

# importing from parent directory
from tests.test_routeSetup import test_payload


# A Python program for Dijkstra's shortest
# path algorithm for adjacency
# list representation of graph

from collections import defaultdict
import sys

# Python3 program to implement traveling salesman
# problem using naive approach.
from sys import maxsize
from itertools import permutations


# implementation of traveling Salesman Problem
def travellingSalesmanProblem(graph, locations, s):
    V=len(graph)

    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
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


matrix, location_map = ad_matrix()
display_matrix(matrix, location_map)
location = list(location_map.values())

print(travellingSalesmanProblem(matrix, location, 0))