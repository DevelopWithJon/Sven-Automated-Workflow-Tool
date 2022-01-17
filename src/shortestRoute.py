"""Shortest path with travelings salesman."""
import os
import sys
import inspect
import heapq
from statistics import mean

from utils.constants import DISTRIBUTION_CENTER_MAP
from utils.parse_route_data import payload_to_database
from routeSetup import ad_matrix, display_matrix, get_data
from itertools import permutations

# Setting parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# Implementation of traveling Salesman Problem
# https://www.geeksforgeeks.org/traveling-salesman-problem-tsp-implementation/

# TSP is looking for the highest profits rather than the shortest distance so we replace min_path with max_path
def travellingSalesmanProblem(graph, locations, s):
    V = len(graph)

    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    max_path = 0
    next_permutation = permutations(vertex)
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0
        current_dest = []

        # compute current path weight
        k = s
        for j in i:
            current_dest += [locations[k]]
            current_pathweight += graph[k][j]
            k = j
        current_dest += [locations[k]]
        current_pathweight += graph[k][s]

        # update minimum
        if max_path < current_pathweight:
            max_path = current_pathweight
            res = current_dest

    return (max_path, res)


def altered_tour(matrix, location):
    """Calculate which location to potentially remove"""
    least_profitable_location = sys.maxsize
    least_profitable_location_int = None

    # initate a least_profitable_location with max value
    # reach row in the matrix represents the profits of leaving the indexed location to every other locatoin
    # loop through each  location in the matrix and get the average profits
    # if the current least_profitable_location is higher than the current average profits assign least_profitable_location to average profits at that location

    for i, v in enumerate(matrix):
        if least_profitable_location > mean(v) and i != 0:
            least_profitable_location = mean(v)
            least_profitable_location_int = i

    # update matrix and location array to exclude the least_profitable_location

    matrix = (
        matrix[:least_profitable_location_int]
        + matrix[least_profitable_location_int + 1 :]
    )
    location = (
        location[:least_profitable_location_int]
        + location[least_profitable_location_int + 1 :]
    )
    return travellingSalesmanProblem(matrix, location, 0)


def loop_assignments(payload, center):

    matrix, location_map = ad_matrix(payload, center)
    print("#" * 50)
    print(display_matrix(matrix, location_map))
    print("#" * 50)

    location = list(location_map.values())
    full_route = travellingSalesmanProblem(matrix, location, 0)
    altered = altered_tour(matrix, location)
    altered += full_route
    print(f"normal: {full_route}")
    print(f"altered: {altered}")
    return max(full_route, altered)


def assign_to_warehouse(payload=None, gen_items=None):

    optimized_payload = get_data(payload=payload, gen_items=gen_items)
    candidates = []

    for center in DISTRIBUTION_CENTER_MAP:
        copy_payload = optimized_payload.copy()
        candidates.append(loop_assignments(copy_payload, center))

    assignment = max(candidates)
    print(f"final assignment: {assignment}")
    # payload_to_database(optimized_payload, assignment)

    return optimized_payload, assignment
