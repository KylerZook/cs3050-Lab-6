# CS3050 Lab 6 Submission - Advanced Route Planning

**Author:** [Your Name]
**Implementation Language:** Python
**Submission Date:** [Date]

---

## Overview

This submission contains the implementation of time-window constrained routing and priority-based multi-destination routing for CS3050 Lab 6. The project extends standard shortest path algorithms to handle real-world routing constraints.

---

## Directory Structure

```
lab6_submission/
├── src/
│   ├── route_planner.py      # Main implementation (TO COMPLETE)
│   └── requirements.txt       # Python dependencies
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
├── profiling/
│   ├── profile_before.txt     # Profiling before optimization
│   ├── profile_after.txt      # Profiling after optimization
│   └── optimization_notes.md  # Optimization documentation
├── report/
│   └── lab6_report_outline.md # Report template (convert to PDF)
└── README.md                   # This file
```

---

## How to Complete This Assignment

This README provides a step-by-step guide to completing the lab. Follow these steps in order.

### Phase 1: Understanding (Week 1, Days 1-2)

#### Step 1: Understand the Existing Code

Before implementing anything, understand what you're building on:

```bash
# Navigate to the parent directory
cd ..

# Run the existing implementations
cd python
python3 route_planner.py ../data/nodes.csv ../data/edges.csv 1 3 dijkstra
python3 route_planner.py ../data/nodes.csv ../data/edges.csv 1 3 astar

cd ../c
make
./route_planner ../data/nodes.csv ../data/edges.csv 1 3 dijkstra

cd ../go
go run route_planner.go ../data/nodes.csv ../data/edges.csv 1 3 dijkstra
```

**What to observe:**
- How are graphs loaded?
- How are paths represented?
- How are results printed?
- How do Dijkstra and A* differ?

#### Step 2: Study the Template Code

```bash
cd ../lab6_submission/src
cat route_planner.py
```

**Key sections to understand:**
1. **Data structures:** `Node`, `Edge`, `State`, `Graph` classes
2. **Graph loading:** `load_graph()` function
3. **Helper functions:** `haversine_distance()` for A* heuristic
4. **TODO markers:** These indicate where you need to implement code

#### Step 3: Plan on Paper

**DO NOT START CODING YET!**

Draw a small graph (4 nodes) on paper:
```
Nodes:
1: [0, 100]    (time window: can arrive between 0-100)
2: [10, 50]
3: [25, 75]
4: [40, 100]

Edges:
1 -> 2: distance 15
2 -> 3: distance 20
1 -> 3: distance 40
3 -> 4: distance 25
```

**Manually trace:**
- Path from 1 to 4
- At what time do you arrive at each node?
- Do the arrivals fall within time windows?
- What if you take path 1->3->4 vs 1->2->3->4?

**Key insight:** The shortest *distance* path might violate time constraints!

### Phase 2: Implementation - Part 1 (Week 1, Days 3-7)

#### Step 4: Implement Time-Window Dijkstra

**Algorithm choice:** Start with Dijkstra (recommended for first implementation)

**Key decisions to make:**

1. **State representation:**
   - Regular Dijkstra: state = node_id
   - Time-window: state = (node_id, arrival_time)
   - Question: Do you discretize time? Or use continuous values?

2. **Waiting policy:**
   - Option A: Can wait at nodes (if arrive early, wait until earliest)
   - Option B: Cannot wait (must arrive exactly within window)
   - Recommendation: Allow waiting (simpler and more flexible)

3. **Pruning strategy:**
   - Prune if arrival_time > latest[node]
   - But can you also prune if you've visited the same node with earlier arrival?

**Implementation steps:**

1. **Modify the State class** (line ~35 in route_planner.py):
```python
@dataclass
class State:
    node_id: int
    arrival_time: float  # NEW: track when we arrive
    distance: float = 0.0

    def __lt__(self, other):
        # Should we compare by distance or arrival_time?
        # Think about what we're optimizing!
        return self.distance < other.distance
```

2. **Implement `dijkstra_with_time_windows()`** (line ~150):

Pseudocode:
```
function dijkstra_with_time_windows(graph, start, end):
    # Initialize
    pq = priority queue
    visited = set()  # Track (node_id, arrival_time) pairs
    parent = dict()  # For path reconstruction

    # Start state
    initial_state = State(start, 0.0, 0.0)
    push initial_state to pq

    while pq not empty:
        current_state = pop from pq

        # Check if reached goal
        if current_state.node_id == end:
            # Reconstruct path and return
            ...

        # Mark as visited
        # Question: What exactly do you mark as visited?
        # Option 1: Just node_id (might revisit with different time)
        # Option 2: (node_id, arrival_time) (more states)
        # Option 3: (node_id, earliest_arrival_time_so_far)

        # Explore neighbors
        for edge in graph.get_neighbors(current_state.node_id):
            next_node = edge.to_node
            next_distance = current_state.distance + edge.distance
            next_arrival = current_state.arrival_time + edge.distance

            # Check time window constraint
            node = graph.nodes[next_node]
            if next_arrival > node.latest:
                continue  # Arrive too late, prune this path

            # Adjust for early arrival
            if next_arrival < node.earliest:
                # If allowing waiting:
                next_arrival = node.earliest
                # If not allowing waiting:
                # continue  # Cannot arrive early

            # Check if this state should be explored
            # (not visited, or better than previous visit)
            if should_explore(next_node, next_arrival, visited):
                new_state = State(next_node, next_arrival, next_distance)
                push new_state to pq
                parent[new_state] = current_state

    # No path found
    return None, 0.0, nodes_explored
```

**Testing after implementation:**
```bash
cd src
python3 route_planner.py ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv 1 4 dijkstra
```

Expected: Should find a feasible path

#### Step 5: Handle Infeasible Cases

Implement `find_infeasible_constraints()` and `suggest_closest_path()`:

**Approach:**
1. Run standard Dijkstra (ignoring time windows)
2. Check which nodes in the path violate their time windows
3. Report violations and suggest fixes

```python
def find_infeasible_constraints(graph, start, end):
    # Run shortest path without time constraints
    # Check each node's arrival time against its window
    # Return list of violations
    ...
```

#### Step 6: Create and Run Test Cases

```bash
# Test Case 1: Feasible path
python3 route_planner.py ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv 1 4 dijkstra

# Test Case 2: Infeasible path
python3 route_planner.py ../tests/data/test_infeasible_nodes.csv \
    ../tests/data/test_infeasible_edges.csv 1 4 dijkstra

# Test Case 3: Shortest path violates constraints
python3 route_planner.py ../tests/data/test_shortest_violates_nodes.csv \
    ../tests/data/test_shortest_violates_edges.csv 1 4 dijkstra
```

**Document results** in `tests/test_results.txt`

### Phase 3: Implementation - Part 2 (Week 2, Days 1-3)

#### Step 7: Implement Priority-Based Routing

**Problem:** Visit multiple destinations with priorities (HIGH, MEDIUM, LOW)

**Approach 1: Greedy with Priority Ordering**
```python
def priority_multi_destination_routing(graph, start, destinations, threshold):
    # Group destinations by priority
    high_priority = [node for node, pri in destinations.items() if pri == "HIGH"]
    medium_priority = [node for node, pri in destinations.items() if pri == "MEDIUM"]
    low_priority = [node for node, pri in destinations.items() if pri == "LOW"]

    # Visit in order: HIGH -> MEDIUM -> LOW
    route = [start]
    current = start
    total_distance = 0.0

    for priority_group in [high_priority, medium_priority, low_priority]:
        while priority_group:
            # Find nearest unvisited node in this priority group
            nearest = find_nearest(current, priority_group, graph)
            path, dist = shortest_path(current, nearest, graph)

            route.extend(path[1:])  # Append path (skip current node)
            total_distance += dist
            current = nearest
            priority_group.remove(nearest)

    return route, total_distance, []  # No violations if strict ordering
```

**Approach 2: Threshold-Based Flexibility**
```python
# Allow swapping if distance savings > threshold
# Example: If visiting MEDIUM before HIGH saves >20% distance, allow it
```

**Implementation recommendation:** Start with strict ordering (Approach 1), then add threshold flexibility.

#### Step 8: Test Priority Routing

Create a test file with multiple destinations:
```bash
# You'll need to create a multi-destination test graph
# Or modify the main() function to load priorities from CSV
```

### Phase 4: Analysis and Proofs (Week 2, Days 4-7)

#### Step 9: Write Correctness Proof

Open `report/lab6_report_outline.md` and fill in Section 3.

**Proof strategy - Loop Invariant:**

**Invariant:** After processing k states, for all nodes in visited set, we have found the earliest feasible arrival time that minimizes distance.

**Proof structure:**
1. **Initialization:** Invariant holds with k=0 (only start node)
2. **Maintenance:** Show that extracting next state maintains invariant
   - Why? Because we process states in order of increasing distance
   - And we prune infeasible states
3. **Termination:** When we reach the goal, invariant guarantees optimality

**Tip:** Use concrete examples to illustrate your proof

#### Step 10: Analyze Time Complexity

**Standard Dijkstra:** O((V + E) log V)

**Your algorithm:**
- State space: (node_id, arrival_time)
- How many possible arrival times per node?
  - If continuous: potentially infinite (but practical limit)
  - If discretized by edge weights: O(W) where W is max window size
- Total states: O(V × W) in worst case
- Each state explores E edges
- Priority queue operations: O(log(V × W))

**Complexity:** O((V × W + E) log(V × W))

**Fill this in** in Section 4.1 of the report

#### Step 11: Experimental Performance Validation

Create test graphs of varying sizes:

```python
# Create a script to generate random graphs
def generate_random_graph(num_nodes, edge_density):
    # Generate random lat/lon coordinates
    # Generate random edges
    # Generate random time windows
    # Save to CSV
    ...

# Test on sizes: 10, 50, 100, 500
import time

for size in [10, 50, 100, 500]:
    graph = generate_graph(size)
    start_time = time.perf_counter()
    path, dist, explored = dijkstra_with_time_windows(graph, 1, size)
    elapsed = time.perf_counter() - start_time
    print(f"Size {size}: {elapsed*1000:.2f} ms")
```

**Plot results** (can use matplotlib or create in spreadsheet):
- X-axis: graph size
- Y-axis: runtime

**Document in report** Section 4.3

### Phase 5: Design Justification (Week 2, Day 7 - Week 3, Day 2)

#### Step 12: Justify Algorithm Choice

Fill in Section 5 of the report.

**Why Dijkstra?**
- Time windows don't create negative weights
- Priority queue efficiently handles state exploration
- Optimal with non-negative weights

**Why NOT A*?**
- Heuristic (haversine distance) doesn't account for time constraints
- Might mislead search toward geographically close but temporally infeasible nodes
- Could still work but requires careful heuristic design

**Why NOT Bellman-Ford?**
- Slower: O(V × E) vs O((V+E) log V)
- Designed for negative weights, which we don't have
- No advantage for this problem

#### Step 13: Propose Alternative Speedup Approaches

**Approach 1: Preprocessing with Time-Distance Index**

Idea: Precompute reachable nodes within time budgets

```
Preprocessing:
For each node v and time budget t:
    Compute which nodes are reachable from v within time t
    Store in index: index[v][t] = {reachable nodes}

During search:
    When at node v with remaining time t:
        Only explore nodes in index[v][t]
```

**Tradeoffs:**
- Speedup: ~10-100× depending on graph density
- Cost: O(V²W) preprocessing time and space
- Fails when: Time windows are very tight and varied

**Approach 2: Bidirectional Search**

Idea: Search from both start and end simultaneously

**Tradeoffs:**
- Speedup: ~2-4× (explore roughly half the states)
- Cost: More complex implementation, two priority queues
- Fails when: Time constraints are directional (can't easily search backward)

**Document these** in Section 5.2 of the report

### Phase 6: Debugging (Week 3, Days 3-4)

#### Step 14: Find the Bug in Buggy Implementation

Navigate to `assignment_materials/` and examine the buggy files:

```bash
cd ../assignment_materials
ls route_planner_buggy.*
```

**Debugging strategy:**

1. **Run the buggy code:**
```bash
python3 route_planner_buggy.py [test data]
```

2. **Compare with correct implementation:**
   - Run your working implementation on same data
   - Compare outputs

3. **Look for suspicious patterns:**
   - Off-by-one errors
   - Wrong comparison operators (< vs <=)
   - Missing constraint checks
   - Incorrect initialization
   - Wrong loop termination

4. **Common bugs in Bellman-Ford:**
   - Not running V-1 iterations
   - Not checking all edges in each iteration
   - Incorrect relaxation logic
   - Not detecting negative cycles

5. **Add print statements:**
```python
# Inside the algorithm
print(f"Processing node {node}, distance {dist}")
print(f"Relaxing edge {u} -> {v}, old dist: {distance[v]}, new: {distance[u] + weight}")
```

6. **Create minimal test case:**
   - 3-4 node graph that triggers the bug
   - Manually compute correct answer
   - See where algorithm diverges

**Document your process** in Section 6.1 of the report

### Phase 7: Optimization (Week 3, Days 5-6)

#### Step 15: Profile Your Code

```bash
cd ../lab6_submission/src

# Generate profiling data
python3 -m cProfile -o profile.stats route_planner.py \
    ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv \
    1 4 dijkstra

# Analyze
python3 << 'EOF'
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative')
p.print_stats(20)
EOF
```

**Save output** to `../profiling/profile_before.txt`

**Identify bottleneck:**
- Which function takes most time?
- Which function is called most often?
- Where should you optimize?

#### Step 16: Implement Optimization

**Common bottlenecks and fixes:**

1. **Priority queue operations:**
   ```python
   # Before: Many duplicate insertions
   for edge in edges:
       heapq.heappush(pq, (dist, node, time))

   # After: Check before inserting
   for edge in edges:
       if not already_have_better_path(node, time):
           heapq.heappush(pq, (dist, node, time))
   ```

2. **Visited set lookups:**
   ```python
   # Before: set of tuples (slower for complex tuples)
   visited = set()
   visited.add((node, arrival_time))

   # After: dict with compound key
   visited = {}
   visited[f"{node}:{arrival_time}"] = True
   # OR discretize time
   visited[f"{node}:{int(arrival_time)}"] = True
   ```

3. **Redundant time window checks:**
   ```python
   # Before: Check time window every time
   for edge in edges:
       if graph.nodes[edge.to_node].earliest <= time <= graph.nodes[edge.to_node].latest:
           ...

   # After: Cache time window checks
   valid_transitions = {}  # Cache: (from_node, to_node, time) -> bool
   ```

#### Step 17: Measure Improvement

```bash
# Run profiling again
python3 -m cProfile -o profile_optimized.stats route_planner.py \
    ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv \
    1 4 dijkstra
```

**Compare:**
- Before: X ms
- After: Y ms
- Improvement: (X-Y)/X × 100%

**Goal:** ≥20% improvement

**Save output** to `../profiling/profile_after.txt`

**Document** in `../profiling/optimization_notes.md` and Section 6.2 of report

### Phase 8: Report Writing (Week 3, Day 7)

#### Step 18: Complete the Report

Use `report/lab6_report_outline.md` as a template.

**Sections to complete:**
1. Introduction (0.5 pages) - Overview of problem and your approach
2. Implementation Details (2-3 pages) - Algorithm modifications, design decisions
3. Correctness Proof (2-3 pages) - Formal proof of algorithm correctness
4. Performance Analysis (2-3 pages) - Complexity analysis + experiments
5. Design Justification (2-3 pages) - Why you chose your approach, alternatives
6. Debugging and Optimization (1-2 pages) - Bug found, optimization results
7. Conclusion (0.5 pages) - Lessons learned, future work

**Convert to PDF:**
```bash
# If using Markdown:
pandoc lab6_report_outline.md -o lab6_report.pdf

# Or use Overleaf/LaTeX if you prefer that format
# Or write in Word/Google Docs and export to PDF
```

**Proofreading checklist:**
- [ ] All TODO sections filled in
- [ ] Code matches what's described in report
- [ ] Proofs are clear and logical
- [ ] Graphs and tables are readable
- [ ] Citations are formatted correctly
- [ ] No spelling/grammar errors
- [ ] 8-12 pages total

---

## Quick Start Commands

### Build and Run

```bash
# Navigate to source directory
cd src

# Run time-window routing
python3 route_planner.py \
    ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv \
    1 4 dijkstra

# Run with A* (if implemented)
python3 route_planner.py \
    ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv \
    1 4 astar
```

### Testing

```bash
# Run all test cases
cd src

# Test 1: Feasible path
python3 route_planner.py ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv 1 4 dijkstra

# Test 2: Infeasible path
python3 route_planner.py ../tests/data/test_infeasible_nodes.csv \
    ../tests/data/test_infeasible_edges.csv 1 4 dijkstra

# Test 3: Shortest path violates constraints
python3 route_planner.py ../tests/data/test_shortest_violates_nodes.csv \
    ../tests/data/test_shortest_violates_edges.csv 1 4 dijkstra
```

### Profiling

```bash
cd src

# Generate profile
python3 -m cProfile -o profile.stats route_planner.py \
    ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv \
    1 4 dijkstra

# View profile (cumulative time)
python3 -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"

# View profile (time per call)
python3 -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('time'); p.print_stats(20)"
```

---

## Implementation Checklist

### Part 1: Time-Window Routing (60 points)
- [ ] State class includes arrival_time tracking
- [ ] dijkstra_with_time_windows() implemented
- [ ] Time window constraints checked for each node
- [ ] Early arrival handling (wait vs reject)
- [ ] Late arrival rejection
- [ ] Path reconstruction with time-aware states
- [ ] find_infeasible_constraints() implemented
- [ ] suggest_closest_path() implemented
- [ ] Test cases created and documented
- [ ] Code is well-commented

### Part 2: Priority Routing (60 points)
- [ ] priority_multi_destination_routing() implemented
- [ ] Destinations grouped by priority level
- [ ] Routing respects priority order (HIGH -> MEDIUM -> LOW)
- [ ] Threshold parameter implemented
- [ ] Priority violations tracked and reported
- [ ] Test cases with multiple destinations
- [ ] Trade-off between distance and priority ordering handled

### Part 3: Correctness Proof (45 points)
- [ ] Assumptions clearly stated
- [ ] Loop invariant or induction proof provided
- [ ] Proof addresses YOUR specific algorithm
- [ ] Counterexample OR completeness proof included
- [ ] Optimality discussion included
- [ ] Mathematical rigor appropriate for undergraduate level

### Part 4: Performance Analysis (45 points)
- [ ] Time complexity derived: O(?)
- [ ] Space complexity derived: O(?)
- [ ] Comparison to standard Dijkstra
- [ ] Test graphs generated (sizes: 10, 50, 100, 500)
- [ ] Experimental runtimes measured
- [ ] Results plotted (graph size vs runtime)
- [ ] Theoretical vs empirical comparison discussed
- [ ] Discrepancies explained

### Part 5: Algorithm Selection (30 points)
- [ ] Choice of base algorithm justified
- [ ] Tradeoffs vs alternatives discussed
- [ ] Modification of DIFFERENT algorithm shown
- [ ] Comparative analysis with concrete examples
- [ ] Real-world implications considered

### Part 6: Alternative Approaches (30 points)
- [ ] Two speedup approaches proposed
- [ ] Each approach described in detail
- [ ] Tradeoffs analyzed for each
- [ ] Speedup estimates provided (order of magnitude)
- [ ] Failure scenarios identified
- [ ] Graph properties that affect effectiveness discussed

### Part 7: Bug Hunt (15 points)
- [ ] Bug identified in buggy implementation
- [ ] Bug location specified (file, line, function)
- [ ] Explanation of why it causes incorrect results
- [ ] Test case that triggers the bug
- [ ] Bug fixed and verified
- [ ] Debugging process documented

### Part 8: Optimization (15 points)
- [ ] Code profiled with cProfile
- [ ] Bottleneck identified
- [ ] Optimization implemented
- [ ] Before/after measurements documented
- [ ] ≥20% speedup achieved (or well-documented attempt)
- [ ] Tradeoffs discussed (complexity, memory, correctness)
- [ ] Results saved in profiling/ folder

### Report Quality (15 points)
- [ ] 8-12 pages total
- [ ] Well-organized with clear sections
- [ ] No spelling/grammar errors
- [ ] Figures and tables are readable
- [ ] Citations properly formatted
- [ ] Code snippets formatted correctly
- [ ] PDF exported and ready for submission

### Code Quality (15 points)
- [ ] Code compiles/runs without errors
- [ ] Clear comments explaining complex sections
- [ ] Functions have docstrings
- [ ] Variable names are descriptive
- [ ] Code follows consistent style
- [ ] No hardcoded values (use constants)
- [ ] Error handling for edge cases

---

## Common Pitfalls to Avoid

### Implementation Pitfalls

1. **Not rethinking state space**
   - Time windows fundamentally change the problem
   - State must include both node AND arrival time

2. **Confusing distance and time**
   - Edge weights represent both distance AND time
   - In this lab, they're the same (1 km = 1 time unit)
   - But be clear about what you're optimizing

3. **Incorrect pruning**
   - Don't prune just because you visited a node before
   - A later arrival might still be useful if earlier arrivals violated constraints

4. **Forgetting edge cases**
   - Start node = end node
   - No path exists
   - All time windows are [0, ∞]
   - Single node with impossible time window

### Proof Pitfalls

1. **Code walkthrough instead of proof**
   - "Line 15 sets x to 0, then line 20 increments it" ← NOT a proof
   - "By induction on path length, we show..." ← Better

2. **Assuming what you need to prove**
   - "The algorithm finds the shortest path because it uses Dijkstra" ← Circular
   - "Dijkstra guarantees optimality for non-negative weights, and our modification preserves this property because..." ← Better

3. **Ignoring your modifications**
   - You can't just cite Dijkstra's correctness proof
   - You must prove YOUR modified algorithm is correct

### Analysis Pitfalls

1. **Single test run**
   - Systems are noisy
   - Run multiple trials and average
   - Report standard deviation

2. **Ignoring theory/practice mismatch**
   - If experiments don't match theory, investigate!
   - Don't just report and move on

3. **Forgetting constant factors**
   - O(n log n) with huge constants might be slower than O(n²) for small n

---

## Tips for Success

### Time Management

**Week 1:**
- Day 1-2: Understand existing code, plan on paper
- Day 3-5: Implement time-window routing
- Day 6-7: Test, debug, handle edge cases

**Week 2:**
- Day 1-3: Implement priority routing
- Day 4-5: Write proofs
- Day 6-7: Performance analysis, experiments

**Week 3:**
- Day 1-2: Design justification section
- Day 3-4: Bug hunt
- Day 5-6: Optimization
- Day 7: Report writing and final review

### Testing Strategy

1. **Start simple:** 3-4 node graphs you can trace manually
2. **Test edge cases:** No path, start=end, tight windows
3. **Stress test:** Large graphs (100+ nodes)
4. **Real-world:** Mimic actual delivery scenarios

### Using AI Tools Responsibly

**Good uses:**
- "Explain how Dijkstra's algorithm works"
- "What's the difference between Dijkstra and Bellman-Ford?"
- "Why is my Python code giving a KeyError on line 50?"
- "What does O(V log V) mean in practical terms?"

**Bad uses:**
- "Write the time-window Dijkstra algorithm for me"
- "Prove that my algorithm is correct"
- "What algorithm should I use for this assignment?"

**Remember:** You must be able to explain and defend your work!

---

## Submission Checklist

Before submitting, verify:

- [ ] All code files in `src/` directory
- [ ] All test files in `tests/` directory with expected outputs
- [ ] Profiling data in `profiling/` directory
- [ ] Report PDF in `report/` directory (8-12 pages)
- [ ] Code runs without errors
- [ ] All test cases pass
- [ ] README.md explains how to run everything
- [ ] No TODOs left in code or report
- [ ] Files zipped as `lab6_submission.zip`

### Final Submission Structure

```
lab6_submission.zip
└── lab6_submission/
    ├── src/
    │   ├── route_planner.py     ✓ Complete implementation
    │   ├── requirements.txt      ✓ Dependencies
    │   └── README.md             ✓ How to run
    ├── tests/
    │   ├── data/*.csv            ✓ All test data
    │   └── test_results.txt      ✓ Expected outputs
    ├── profiling/
    │   ├── profile_before.txt    ✓ Before optimization
    │   ├── profile_after.txt     ✓ After optimization
    │   └── optimization_notes.md ✓ Documentation
    ├── report/
    │   └── lab6_report.pdf       ✓ 8-12 pages
    └── README.md                 ✓ This file
```

---

## Getting Help

### Before Asking for Help

1. Read the error message carefully
2. Check the assignment materials and hints
3. Try to debug it yourself (use print statements!)
4. Search course resources

### Good Questions

- "My algorithm gives incorrect results on this specific graph [show graph]. I expect path [1,2,3] but get [1,4,3]. Here's my reasoning..."
- "I'm stuck on proving why my algorithm handles early arrivals correctly. I've shown X and Y, but can't connect to Z..."

### Where to Ask

- Office hours
- Course discussion board
- Study groups (but write your own code!)

---

## Grading Expectations

| Component | Points | What Matters |
|-----------|--------|--------------|
| Time-Window Implementation | 60 | Correctness, edge cases, code quality |
| Priority Routing | 60 | Logic, threshold handling, testing |
| Correctness Proof | 45 | Rigor, clarity, addresses YOUR algorithm |
| Performance Analysis | 45 | Accurate complexity, good experiments |
| Algorithm Selection | 30 | Depth of understanding, comparison |
| Alternative Approaches | 30 | Creativity, feasibility, tradeoffs |
| Bug Hunt | 15 | Found bug, clear explanation, tests |
| Optimization | 15 | Measurable improvement, documentation |
| **Total** | **300** | |

**Extra credit opportunities (+30):**
- Exceptional report quality (+15)
- Exceptional code quality (+15)

---

## Final Notes

This is a challenging assignment designed to deepen your understanding of:
- Graph algorithms beyond simple shortest paths
- Algorithm correctness and analysis
- Real-world constraint satisfaction
- Software engineering and testing

**The struggle is where the learning happens.** Don't get discouraged if it's hard!

**Start early, test thoroughly, and think deeply.**

Good luck! 🚀

---

**Last updated:** December 2024
