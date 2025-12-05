# Performance Optimization Notes

## Initial Profiling Analysis

### Step 1: Profile the Code

```bash
# Generate profile data
python -m cProfile -o profile_before.stats ../src/route_planner.py \
    ../tests/data/test_feasible_nodes.csv \
    ../tests/data/test_feasible_edges.csv \
    1 4 dijkstra

# Analyze results
python3 << 'EOF'
import pstats
p = pstats.Stats('profile_before.stats')
p.sort_stats('cumulative')
p.print_stats(20)
EOF
```

### Step 2: Identify Bottlenecks

TODO: Document your findings

Questions to answer:
1. What function consumes the most time?
2. How many times is it called?
3. Is the bottleneck algorithmic or implementation-specific?

## Optimization Strategies Considered

### Option 1: [Name of optimization]

**Description:**

**Expected speedup:**

**Tradeoffs:**

**Implementation:**

**Result:**

### Option 2: [Name of optimization]

**Description:**

**Expected speedup:**

**Tradeoffs:**

**Implementation:**

**Result:**

## Common Python Performance Tips

### 1. Use Appropriate Data Structures
- Dictionary lookups: O(1) average
- Set membership: O(1) average
- List search: O(n)

### 2. Avoid Repeated Computations
```python
# Bad
for i in range(len(some_list)):
    if expensive_function(x) > 10:
        ...

# Good
result = expensive_function(x)
for i in range(len(some_list)):
    if result > 10:
        ...
```

### 3. Use Built-in Functions
- Built-ins are implemented in C, faster than Python loops
- `map()`, `filter()`, list comprehensions

### 4. Minimize State Copies
```python
# Bad - creates many tuple copies
state = (node, time, dist)
new_state = (state[0], state[1] + delta, state[2])

# Better - use class with __slots__
@dataclass
class State:
    __slots__ = ['node', 'time', 'dist']
    node: int
    time: float
    dist: float
```

### 5. Early Termination
- Add pruning conditions to skip unnecessary work
- Check constraints before expensive operations

## Specific Optimizations for This Lab

### Optimization: Visited State Management

**Problem:**
Checking if a state (node, arrival_time) has been visited might be slow if done inefficiently.

**Solutions:**
1. Use a set with tuples: `visited = set(); visited.add((node_id, time))`
2. Use a dict: `visited = {}; visited[(node_id, time)] = True`
3. Discretize time: Round arrival times to reduce state space

**Tradeoff:** Discretizing time might miss optimal solutions but reduces complexity.

### Optimization: Priority Queue Operations

**Problem:**
Many heappush/heappop operations slow down the algorithm.

**Solutions:**
1. Better pruning to reduce queue size
2. Fibonacci heap (not in Python standard library)
3. Check if state is better before adding to queue

### Optimization: Avoid Redundant Path Reconstruction

**Problem:**
Reconstructing the full path repeatedly during search.

**Solutions:**
1. Only reconstruct path at the end
2. Store incremental path updates
3. Use parent pointers efficiently

## Measurement Methodology

### Baseline Measurement
```python
import time

start = time.perf_counter()
path, dist, explored = dijkstra_with_time_windows(graph, start, end)
elapsed = time.perf_counter() - start

print(f"Runtime: {elapsed * 1000:.2f} ms")
```

### Multiple Trials
```python
import time
import statistics

times = []
for _ in range(10):
    start = time.perf_counter()
    path, dist, explored = dijkstra_with_time_windows(graph, start, end)
    elapsed = time.perf_counter() - start
    times.append(elapsed)

print(f"Mean: {statistics.mean(times) * 1000:.2f} ms")
print(f"Stdev: {statistics.stdev(times) * 1000:.2f} ms")
```

### Different Graph Sizes
Test on graphs of varying sizes to see if optimization scales:
- 10 nodes
- 50 nodes
- 100 nodes
- 500 nodes

## Final Results

TODO: Document your optimization results

### What I Changed:
1.
2.
3.

### Performance Improvement:
- Before: ___ ms
- After: ___ ms
- Speedup: ___% (target: ≥20%)

### Tradeoffs:
-
-

### Lessons Learned:
-
-

## Alternative Approaches Not Implemented

### Approach 1:
**Why not implemented:**

### Approach 2:
**Why not implemented:**
