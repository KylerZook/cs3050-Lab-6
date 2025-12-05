# CS3050 Lab 6 - Part 1: Implementation

**Author:** [Your Name]
**Implementation Language:** Python
**Submission:** Part 1 - Time-Window and Priority Routing (120 points)

---

## Overview

This directory contains the implementation for **Part 1** of Lab 6, which includes:
- **Task 1.1**: Time-Window Constrained Routing (60 points)
- **Task 1.2**: Priority-Based Multi-Destination Routing (60 points)

---

## Directory Structure

```
lab6_submission/
├── src/
│   ├── route_planner.py      # Main implementation
│   └── requirements.txt       # Python dependencies (none required)
├── tests/
│   ├── data/                  # Test case CSV files
│   │   ├── test_feasible_nodes.csv
│   │   ├── test_feasible_edges.csv
│   │   ├── test_infeasible_nodes.csv
│   │   ├── test_infeasible_edges.csv
│   │   ├── test_shortest_violates_nodes.csv
│   │   ├── test_shortest_violates_edges.csv
│   │   └── test_priorities.csv
│   └── test_results.txt       # Expected test outputs
└── README.md                   # This file
```

---

## Task 1.1: Time-Window Constrained Routing

### Objective

Implement a modified shortest path algorithm that respects time window constraints at each node.

### Implementation Approach

The key insight is that **state must include both node ID and arrival time**, not just node ID.

**Modified State Space:**
- Standard Dijkstra: state = node_id
- Time-window version: state = (node_id, arrival_time)

**Algorithm Modifications:**
1. Expand state to track `(node_id, arrival_time, distance)`
2. Check time window constraints: reject if `arrival_time > latest[node]`
3. Handle early arrival: wait until `earliest[node]` if arriving early
4. Prune dominated states: if already visited node with better time/distance

**Design Decision: Waiting Policy**
- **Allowed to wait**: If arrive before `earliest`, wait until window opens
- This makes more paths feasible and matches real-world delivery scenarios

### How to Run

```bash
cd src

# Test Case 1: Feasible path exists
python3 route_planner.py ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv 1 4 dijkstra

# Test Case 2: No feasible path (constraints violated)
python3 route_planner.py ../tests/data/test_infeasible_nodes.csv \
    ../tests/data/test_infeasible_edges.csv 1 4 dijkstra

# Test Case 3: Shortest distance path violates time constraints
python3 route_planner.py ../tests/data/test_shortest_violates_nodes.csv \
    ../tests/data/test_shortest_violates_edges.csv 1 4 dijkstra
```

### Test Cases

**Test 1: Feasible Path**
- All time windows are loose enough to allow feasible paths
- Algorithm should find a valid route

**Test 2: Infeasible Path**
- Time windows make it impossible to reach destination
- Should report constraint violations and which nodes are problematic

**Test 3: Shortest Path Violates Constraints**
- The shortest *distance* path arrives at nodes outside their time windows
- Algorithm must choose a longer path that respects time constraints
- Tests that algorithm prioritizes feasibility over distance optimization

### Key Implementation Details

```python
# State representation
@dataclass
class State:
    node_id: int
    arrival_time: float
    distance: float

# Time window checking
node = graph.nodes[next_node]
if next_arrival > node.latest:
    continue  # Prune: arrive too late

if next_arrival < node.earliest:
    next_arrival = node.earliest  # Wait until window opens
```

---

## Task 1.2: Priority-Based Multi-Destination Routing

### Objective

Route through multiple destinations with different priority levels (HIGH, MEDIUM, LOW) while balancing:
- Respecting priority order
- Minimizing total distance
- Using a threshold parameter for flexibility

### Implementation Approach

**Algorithm: Greedy with Threshold-Based Flexibility**

1. Group destinations by priority level
2. For each priority level (HIGH → MEDIUM → LOW):
   - Visit nearest unvisited destination in current priority level
3. Apply threshold: allow priority violations if distance savings exceeds threshold

**Threshold Parameter:**
- `threshold = 0.2` means "allow 20% longer path to maintain priority order"
- OR "allow priority swap if it saves >20% distance"

### How to Run

```bash
cd src

# Priority routing (needs to be implemented in main())
# You'll need to modify main() to accept priority file and threshold parameter
```

### Example Priority File Format

```csv
destination,priority
3,HIGH
5,MEDIUM
7,LOW
2,HIGH
6,MEDIUM
```

### Key Implementation Details

**Strict Priority Ordering:**
```python
high_priority = [node for node, pri in destinations.items() if pri == "HIGH"]
medium_priority = [node for node, pri in destinations.items() if pri == "MEDIUM"]
low_priority = [node for node, pri in destinations.items() if pri == "LOW"]

# Visit in order: HIGH -> MEDIUM -> LOW
for priority_group in [high_priority, medium_priority, low_priority]:
    for dest in priority_group:
        # Find shortest path from current location to dest
        # Add to route
```

**With Threshold Flexibility:**
- Calculate strict priority route distance
- Calculate optimal distance route (ignoring priorities)
- If `(strict_distance - optimal_distance) / optimal_distance > threshold`:
  - Allow some priority violations to reduce distance

---

## Implementation Status

### Completed
- [x] Directory structure created
- [x] Test CSV files for time-window routing
- [x] Template code with TODOs and guidance
- [x] Test cases documented

### To Complete (Task 1.1)
- [ ] Implement `dijkstra_with_time_windows()` function
- [ ] Implement `find_infeasible_constraints()` function
- [ ] Implement `suggest_closest_path()` function
- [ ] Test all three test cases
- [ ] Document actual test results in `tests/test_results.txt`

### To Complete (Task 1.2)
- [ ] Implement `priority_multi_destination_routing()` function
- [ ] Create test cases with multiple destinations
- [ ] Test with different threshold values
- [ ] Document behavior with different thresholds

---

## Quick Start Guide

### Step 1: Understand the Problem

**Time-Window Routing:**
- You have a graph with nodes that have time windows `[earliest, latest]`
- You must arrive at each node within its time window
- The shortest distance path might violate time constraints

**Priority Routing:**
- Visit multiple destinations
- HIGH priority should be visited before MEDIUM before LOW
- But strict ordering might make the route much longer
- Threshold allows flexibility

### Step 2: Implement Task 1.1

Open `src/route_planner.py` and find the `dijkstra_with_time_windows()` function.

**Key steps:**
1. Change state from `node_id` to `(node_id, arrival_time)`
2. Check time windows when exploring neighbors
3. Handle early arrival (wait vs. reject)
4. Track parent pointers for path reconstruction

**Pseudocode:**
```python
def dijkstra_with_time_windows(graph, start, end):
    pq = []  # Priority queue
    visited = set()
    parent = {}

    # Initial state: (distance=0, node=start, time=0)
    heappush(pq, (0, start, 0))

    while pq:
        dist, node, time = heappop(pq)

        if node == end:
            # Reconstruct and return path
            ...

        if (node, time) in visited:
            continue
        visited.add((node, time))

        for edge in graph.get_neighbors(node):
            next_node = edge.to_node
            next_dist = dist + edge.distance
            next_time = time + edge.distance  # Assuming distance = time

            # Check time window
            window = graph.nodes[next_node]
            if next_time > window.latest:
                continue  # Too late

            if next_time < window.earliest:
                next_time = window.earliest  # Wait

            # Add to queue
            heappush(pq, (next_dist, next_node, next_time))
            parent[(next_node, next_time)] = (node, time)

    return None  # No feasible path
```

### Step 3: Test Task 1.1

```bash
cd src
python3 route_planner.py ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv 1 4 dijkstra
```

Expected: Should find a path and print it

### Step 4: Implement Task 1.2

Implement the `priority_multi_destination_routing()` function.

**Approach:**
1. Start at source node
2. Visit all HIGH priority nodes (in order of proximity)
3. Then all MEDIUM priority nodes
4. Then all LOW priority nodes
5. Apply threshold to allow flexibility

### Step 5: Document Results

Fill in `tests/test_results.txt` with actual outputs from your implementation.

---

## Testing Checklist

- [ ] Feasible path test passes
- [ ] Infeasible path correctly reports violations
- [ ] Shortest-violates test chooses correct (longer but feasible) path
- [ ] Priority routing visits HIGH before MEDIUM before LOW
- [ ] Threshold parameter works correctly
- [ ] Edge cases handled (start=end, no path exists, etc.)

---

## Common Implementation Pitfalls

1. **Forgetting to expand state space**
   - Don't just track `visited[node_id]`
   - Must track `visited[(node_id, arrival_time)]`

2. **Confusing distance and time**
   - In this lab, edge weight represents both distance AND time
   - 1 km = 1 time unit

3. **Not handling early arrival**
   - If you arrive at time 15 but window is [20, 30], can you wait?
   - Decision: YES (wait until 20) is more flexible

4. **Pruning too aggressively**
   - Don't prune just because you've visited a node before
   - Later arrival at same node might lead to different feasible paths

---

## Tips

1. **Start simple**: Test on the small 4-node graphs first
2. **Add print statements**: See what your algorithm is doing
3. **Draw the graph on paper**: Manually trace the algorithm
4. **Test edge cases**: What if start == end? What if no path exists?

---

## Submission Checklist

- [ ] Code runs without errors
- [ ] Task 1.1 implemented and tested
- [ ] Task 1.2 implemented and tested
- [ ] Test results documented
- [ ] Code has clear comments explaining approach
- [ ] CSV test files demonstrate required scenarios

---

## Notes

This is **Part 1 only**. Future parts will include:
- Part 2: Algorithmic analysis (proofs, complexity)
- Part 3: Design justification
- Part 4: Debugging and optimization

Focus on getting the implementation working correctly first.

---

**Good luck!**
