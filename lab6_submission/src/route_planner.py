#!/usr/bin/env python3
"""
CS3050 Lab 6: Advanced Route Planning - Time-Window Constrained Routing
Student Implementation Template

This file contains the structure for implementing time-window constrained routing
and priority-based multi-destination routing.

Author: [Your Name]
Date: [Date]
"""

import sys
import csv
import heapq
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from math import radians, cos, sin, asin, sqrt


@dataclass
class Node:
    """Represents a node in the graph with optional time window constraints."""
    id: int
    lat: float
    lon: float
    earliest: float = 0.0  # Earliest allowable arrival time
    latest: float = float('inf')  # Latest allowable arrival time


@dataclass
class Edge:
    """Represents a directed edge in the graph."""
    from_node: int
    to_node: int
    distance: float


@dataclass
class State:
    """
    Represents a state in the search space.

    TODO: For time-window routing, you need to track more than just the node!
    Think about: What makes two visits to the same node different?

    Hint: Consider (node_id, arrival_time) as your state.
    """
    node_id: int
    arrival_time: float = 0.0
    distance: float = 0.0

    def __lt__(self, other):
        """For priority queue comparison."""
        return self.distance < other.distance


class Graph:
    """Graph representation for route planning."""

    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.edges: Dict[int, List[Edge]] = {}  # Adjacency list

    def add_node(self, node: Node):
        """Add a node to the graph."""
        self.nodes[node.id] = node
        if node.id not in self.edges:
            self.edges[node.id] = []

    def add_edge(self, edge: Edge):
        """Add an edge to the graph."""
        if edge.from_node not in self.edges:
            self.edges[edge.from_node] = []
        self.edges[edge.from_node].append(edge)

    def get_neighbors(self, node_id: int) -> List[Edge]:
        """Get all outgoing edges from a node."""
        return self.edges.get(node_id, [])


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on earth.
    Returns distance in kilometers.
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers
    r = 6371
    return c * r


def load_graph(nodes_file: str, edges_file: str) -> Graph:
    """
    Load graph from CSV files.

    Nodes file format: id,lat,lon[,earliest,latest]
    Edges file format: from,to,distance
    """
    graph = Graph()

    # Load nodes
    with open(nodes_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = Node(
                id=int(row['id']),
                lat=float(row['lat']),
                lon=float(row['lon']),
                earliest=float(row.get('earliest', 0.0)),
                latest=float(row.get('latest', float('inf')))
            )
            graph.add_node(node)

    # Load edges
    with open(edges_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            edge = Edge(
                from_node=int(row['from']),
                to_node=int(row['to']),
                distance=float(row['distance'])
            )
            graph.add_edge(edge)

    return graph


def dijkstra_with_time_windows(graph: Graph, start: int, end: int) -> Tuple[Optional[List[int]], float, int]:
    """
    Modified Dijkstra's algorithm to handle time window constraints.

    Returns: (path, total_distance, nodes_explored)

    TODO: Implement this algorithm!

    Key considerations:
    1. State space: You need to track (node_id, arrival_time) not just node_id
    2. When can you prune a state?
       - If arrival_time > latest[node]: infeasible
       - If you've already visited this node earlier: dominated
    3. Can you wait at a node if you arrive too early?
       - Design decision: Document your choice!
    4. How do you reconstruct the path?

    Algorithm outline:
    1. Initialize priority queue with (distance=0, start_node, arrival_time=0)
    2. Track visited states (consider what makes a state unique)
    3. For each state:
       a. Check if we've reached the goal
       b. Check time window constraints
       c. Explore neighbors
       d. Add valid next states to queue
    4. Return path or None if infeasible

    Hint: You may need to track parent pointers to reconstruct the path
    """

    # TODO: Initialize data structures
    pq = []  # Priority queue: (distance, node_id, arrival_time)
    visited = set()  # Track visited states
    parent = {}  # For path reconstruction
    nodes_explored = 0

    # TODO: Add start state to queue
    # heapq.heappush(pq, (0, start, 0))  # (distance, node_id, arrival_time)

    # TODO: Implement main loop
    # while pq:
    #     current_dist, current_node, arrival_time = heapq.heappop(pq)
    #
    #     # Check time window constraints
    #     # Check if we've reached the goal
    #     # Explore neighbors
    #     # ...

    # TODO: Reconstruct path if found
    # path = []
    # current = end
    # while current != start:
    #     path.append(current)
    #     current = parent[current]
    # path.append(start)
    # path.reverse()

    # Placeholder return
    print("ERROR: dijkstra_with_time_windows not implemented!")
    return None, 0.0, 0


def priority_multi_destination_routing(
    graph: Graph,
    start: int,
    destinations: Dict[int, str],  # {node_id: priority_level}
    threshold: float = 0.2
) -> Tuple[List[int], float, List[str]]:
    """
    Find a route visiting multiple destinations with priority constraints.

    Args:
        graph: The graph
        start: Starting node
        destinations: Dict mapping node_id -> priority ("HIGH", "MEDIUM", "LOW")
        threshold: Allow path to be this much longer to maintain priority order

    Returns: (route, total_distance, priority_violations)

    TODO: Implement this function!

    Key considerations:
    1. This is NOT the traveling salesman problem
    2. You need to balance:
       - Visiting HIGH priority nodes first
       - Keeping total distance reasonable
       - Allowing some flexibility based on threshold
    3. Possible approaches:
       - Greedy: Visit closest HIGH, then MEDIUM, then LOW
       - Threshold-based: Allow swaps if distance savings > threshold
       - Weighted: Assign distance penalties to priority violations

    Algorithm outline:
    1. Group destinations by priority level
    2. For each priority level (HIGH -> MEDIUM -> LOW):
       a. Find shortest path to nearest unvisited node in this level
       b. OR consider threshold-based swaps
    3. Track any priority violations
    4. Return complete route
    """

    # TODO: Implement priority routing
    route = [start]
    total_distance = 0.0
    violations = []

    # Placeholder return
    print("ERROR: priority_multi_destination_routing not implemented!")
    return route, total_distance, violations


def astar_with_time_windows(graph: Graph, start: int, end: int) -> Tuple[Optional[List[int]], float, int]:
    """
    A* algorithm with time window constraints and haversine heuristic.

    TODO: Optional - implement if you chose A* as your base algorithm.

    The heuristic h(n) = haversine_distance(n, goal) is admissible because:
    - It never overestimates the actual distance
    - Straight-line distance is always <= actual path distance

    Key consideration: How do time windows affect the heuristic?
    """

    print("ERROR: astar_with_time_windows not implemented!")
    return None, 0.0, 0


def find_infeasible_constraints(graph: Graph, start: int, end: int) -> List[str]:
    """
    When no feasible path exists, identify which constraints were violated.

    TODO: Implement constraint violation detection.

    Approach:
    1. Run shortest path WITHOUT time constraints
    2. Check which nodes violate their time windows
    3. Suggest the "closest" feasible path
    """

    violations = []

    # TODO: Implement violation detection

    return violations


def suggest_closest_path(graph: Graph, start: int, end: int) -> Tuple[List[int], float, List[str]]:
    """
    Find the path that minimizes constraint violations.

    TODO: Implement this to handle infeasible cases.

    One approach:
    1. Find path that violates fewest constraints
    2. Find path that minimizes sum of violation amounts
    3. Return path with explanation of violations
    """

    print("ERROR: suggest_closest_path not implemented!")
    return [], 0.0, []


def print_results(path: Optional[List[int]], distance: float, nodes_explored: int, algorithm: str):
    """Print routing results in a formatted way."""

    print(f"\n=== {algorithm} ===")

    if path is None:
        print("No feasible path found satisfying time constraints")
        return

    print(f"Path: {' -> '.join(map(str, path))}")
    print(f"Total distance: {distance:.2f} km")
    print(f"Nodes explored: {nodes_explored}")


def main():
    """Main program entry point."""

    if len(sys.argv) < 5:
        print("Usage: python route_planner.py <nodes.csv> <edges.csv> <start> <end> [algorithm]")
        print("  algorithm: dijkstra (default), astar")
        sys.exit(1)

    nodes_file = sys.argv[1]
    edges_file = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    algorithm = sys.argv[5] if len(sys.argv) > 5 else "dijkstra"

    # Load graph
    print(f"Loading graph from {nodes_file} and {edges_file}...")
    graph = load_graph(nodes_file, edges_file)
    print(f"Loaded {len(graph.nodes)} nodes and {sum(len(edges) for edges in graph.edges.values())} edges")

    # Run algorithm
    if algorithm == "dijkstra":
        path, distance, explored = dijkstra_with_time_windows(graph, start, end)
        print_results(path, distance, explored, "Dijkstra with Time Windows")
    elif algorithm == "astar":
        path, distance, explored = astar_with_time_windows(graph, start, end)
        print_results(path, distance, explored, "A* with Time Windows")
    else:
        print(f"Unknown algorithm: {algorithm}")
        sys.exit(1)

    # If no path found, suggest alternatives
    if path is None:
        violations = find_infeasible_constraints(graph, start, end)
        print("\nConstraint violations:")
        for v in violations:
            print(f"  - {v}")

        print("\nSuggesting closest path...")
        closest_path, closest_dist, closest_violations = suggest_closest_path(graph, start, end)
        print(f"Closest path: {' -> '.join(map(str, closest_path))}")
        print(f"Distance: {closest_dist:.2f} km")
        print(f"Violations: {', '.join(closest_violations)}")


if __name__ == "__main__":
    main()
