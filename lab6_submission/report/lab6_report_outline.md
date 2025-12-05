# CS3050 Lab 6: Advanced Route Planning - Multi-Constraint Pathfinding

**Author:** [Your Name]
**Student ID:** [Your ID]
**Date:** [Submission Date]
**Course:** CS3050 - Advanced Algorithms

---

## 1. Introduction (0.5 pages)

### 1.1 Problem Overview

TODO: Briefly describe the problem this lab addresses

- Real-world routing requires more than just shortest paths
- Need to handle time windows, priorities, and multiple constraints
- Emergency services, delivery, ride-sharing applications

### 1.2 Approach Summary

TODO: Summarize your approach in 2-3 sentences

Example:
> "I implemented time-window constrained routing using a modified Dijkstra's algorithm with an expanded state space of (node_id, arrival_time) tuples. For priority-based routing, I developed a greedy algorithm with a configurable threshold parameter that balances distance optimization with priority ordering..."

### 1.3 Report Organization

This report is organized as follows: Section 2 details the implementation, Section 3 provides correctness proofs, Section 4 analyzes performance, Section 5 justifies design decisions, and Section 6 documents debugging and optimization efforts.

---

## 2. Implementation Details (2-3 pages)

### 2.1 Time-Window Constrained Routing

#### 2.1.1 Algorithm Choice

TODO: State which algorithm you chose as your base (Dijkstra, A*, or Bellman-Ford)

**I chose:** [Algorithm name]

**Reason:** [Brief justification - will expand in Section 5]

#### 2.1.2 State Space Modification

TODO: Explain how you modified the state space

**Standard shortest path state:**
- State = node_id only
- Track: distance to each node

**Modified state for time windows:**
- State = (node_id, arrival_time) or [describe your approach]
- Track: [what you track]
- Rationale: [why this state space works]

#### 2.1.3 Algorithm Modifications

TODO: Describe specific changes to the base algorithm

**Key modifications:**

1. **Initialization:**
   - [What changed]

2. **State exploration:**
   - [How you handle time windows during exploration]
   - [When do you prune states?]

3. **Feasibility checking:**
   - [How do you check if arrival_time ∈ [earliest, latest]?]

4. **Design decision - Early arrival:**
   - Can you arrive early and wait? [YES/NO]
   - Justification: [explain]

5. **Path reconstruction:**
   - [How do you track parent pointers with expanded state space?]

#### 2.1.4 Handling Infeasible Paths

TODO: Explain how you handle cases with no feasible solution

**When no path exists:**
1. [How do you detect infeasibility?]
2. [How do you identify which constraints were violated?]
3. [How do you suggest the "closest" feasible path?]

**Example:**
```
Input: Node 2 has window [10,20], but earliest arrival is 25
Output: "No feasible path. Violation: Arrive at node 2 at time 25, but latest allowed is 20. Suggestion: Relax node 2 window to [10,30]"
```

#### 2.1.5 Pseudocode

TODO: Provide pseudocode for your time-window algorithm

```
function dijkstra_with_time_windows(graph, start, end):
    // TODO: Fill in your pseudocode
    pq = empty priority queue
    visited = empty set

    add (distance=0, node=start, time=0) to pq

    while pq is not empty:
        // ...

    return path, distance, nodes_explored
```

### 2.2 Priority-Based Multi-Destination Routing

#### 2.2.1 Algorithm Design

TODO: Explain your approach to priority routing

**Problem:** Visit multiple destinations with priorities (HIGH, MEDIUM, LOW)

**Approach:** [Describe your strategy]

Options to consider:
- Greedy: Visit highest priority first, then next priority level
- Threshold-based: Allow reordering if distance savings > threshold
- Weighted: Assign penalties to priority violations

**I chose:** [Your approach]

#### 2.2.2 Threshold Parameter

TODO: Explain how the threshold parameter works

**Purpose:** [What does it control?]

**Implementation:** [How do you use it?]

**Example:**
```
threshold = 0.2 (20%)
If swapping order of two destinations saves >20% distance, allow it
Otherwise, maintain strict priority order
```

#### 2.2.3 Priority Violation Handling

TODO: Explain how you track and report violations

**Tracking:** [How do you detect violations?]

**Reporting:** [What information do you provide?]

**Example output:**
```
Route: 1 -> 2 -> 5 -> 3 -> 6 -> 7
Total distance: 45.2 km
Priority violations: Visited MEDIUM node 5 before HIGH node 3 (saved 8.3 km, 18.4% improvement)
```

### 2.3 Key Challenges and Solutions

TODO: Discuss 2-3 major challenges you encountered

**Challenge 1:** [Description]
- **Problem:** [What was difficult?]
- **Solution:** [How did you solve it?]
- **Lesson learned:** [What did you learn?]

**Challenge 2:** [Description]
- **Problem:**
- **Solution:**
- **Lesson learned:**

---

## 3. Correctness Proof (2-3 pages)

### 3.1 Problem Statement

TODO: Formally state what you're proving

**Claim:** My time-window algorithm finds a feasible path from start to end if one exists, and the path minimizes [distance / arrival time / other metric].

### 3.2 Assumptions

TODO: List all assumptions clearly

1. **Graph properties:**
   - All edge weights are non-negative (distance ≥ 0)
   - Graph may be directed or undirected
   - May contain cycles

2. **Time window properties:**
   - For each node v: earliest[v] ≤ latest[v]
   - Time progresses monotonically (can't go backwards)
   - [Other assumptions]

3. **Waiting policy:**
   - [Can/cannot] wait at nodes
   - If yes: waiting has no cost / waiting has cost X

### 3.3 Proof Strategy

TODO: State your proof approach

I will prove correctness using [loop invariants / induction / exchange argument].

### 3.4 Proof

TODO: Write your actual proof

#### 3.4.1 Loop Invariant Approach (if using)

**Invariant:** After k iterations, for all nodes in the visited set, we have found the [earliest feasible arrival time / shortest feasible path / etc.].

**Proof:**

**Initialization (k=0):**
- Initially, visited = {start node with time 0}
- This satisfies the invariant because: [explain]

**Maintenance:**
- Assume invariant holds after k iterations
- Show it holds after k+1 iterations
- Consider the next state (u, t) removed from priority queue
- [Detailed reasoning why invariant is maintained]

**Termination:**
- Loop terminates when: [condition]
- At termination, invariant guarantees: [conclusion]
- Therefore, algorithm is correct.

#### 3.4.2 Alternative Proof Approaches

TODO: If not using loop invariants, provide your proof here

**Option 1: Induction on path length**
- Base case: Paths of length 0 (start node)
- Inductive step: If algorithm correctly handles paths of length k, show it handles length k+1

**Option 2: Contradiction**
- Assume algorithm returns suboptimal path or fails to find existing path
- Show this leads to contradiction

### 3.5 Counterexample or Completeness Proof

TODO: Either provide a counterexample OR prove none exists

**Option A: Counterexample**

If your algorithm has limitations, provide a specific graph where it fails:

```
Graph:
Nodes: 1, 2, 3
Edges: 1->2 (dist=10), 2->3 (dist=10), 1->3 (dist=15)
Time windows: 1[0,100], 2[25,30], 3[35,50]

My algorithm returns: [result]
Correct answer: [correct result]
Reason for failure: [explanation]
```

**Option B: Completeness**

If your algorithm always finds a feasible path when one exists, prove it:

"There cannot exist a graph configuration where my algorithm fails to find a feasible path because... [reasoning]"

### 3.6 Optimality Discussion

TODO: Discuss whether your algorithm finds the optimal solution

**What does "optimal" mean with time windows?**
- Shortest distance? Earliest arrival? Fewest constraint violations?

**Does my algorithm guarantee optimality?**
- [YES/NO with explanation]

**If not optimal, how far from optimal can it be?**
- [Approximation ratio or bounds]

---

## 4. Performance Analysis (2-3 pages)

### 4.1 Time Complexity Analysis

#### 4.1.1 Theoretical Analysis

TODO: Derive worst-case time complexity

**Standard Dijkstra:** O((V + E) log V)
- V insertions into priority queue
- E edge relaxations
- Each operation: O(log V)

**My time-window algorithm:**

**State space size:**
- Standard Dijkstra: V states (one per node)
- My algorithm: [V × W / V × T / other] states
  - Where W = [definition]
- Worst case: [number] states

**Operations:**
- Priority queue insertions: [count]
- Priority queue deletions: [count]
- Each operation cost: [O(log ...)]

**Total complexity:** O([your formula])

**Comparison to standard Dijkstra:**
- When is mine faster? [scenario]
- When is mine slower? [scenario]
- Bottleneck: [what dominates the runtime?]

#### 4.1.2 Breakdown of Complexity

TODO: Analyze each component

| Operation | Count | Cost per operation | Total |
|-----------|-------|-------------------|-------|
| Priority queue insert | [formula] | O(log n) | [result] |
| Priority queue delete | [formula] | O(log n) | [result] |
| Time window check | [formula] | O(1) | [result] |
| Visited check | [formula] | O(1) or O(log n) | [result] |
| **Overall** | | | **O([final])** |

### 4.2 Space Complexity Analysis

TODO: Derive space complexity

**Additional state tracked:**
- Visited set: [size]
- Priority queue: [max size]
- Parent pointers: [size]
- Other: [describe]

**Total space complexity:** O([your formula])

**Comparison to standard Dijkstra:** [analysis]

### 4.3 Experimental Validation

#### 4.3.1 Experimental Setup

TODO: Describe your experiments

**Test graphs:**
- Sizes: |V| ∈ {10, 50, 100, 500}
- Edge density: [describe]
- Time window ranges: [describe]

**Measurement methodology:**
- Tool: Python's `time.perf_counter()`
- Number of trials per size: [count]
- Hardware: [MacBook / PC / etc.]
- Statistical analysis: mean, standard deviation

#### 4.3.2 Results

TODO: Present experimental results

**Runtime vs Graph Size:**

| |V| | |E| | Runtime (ms) | Std Dev | Nodes Explored |
|-----|-----|--------------|---------|----------------|
| 10 | [edges] | [time] | [±std] | [count] |
| 50 | [edges] | [time] | [±std] | [count] |
| 100 | [edges] | [time] | [±std] | [count] |
| 500 | [edges] | [time] | [±std] | [count] |

**Graph: Runtime vs. |V|**

TODO: Include a plot showing runtime vs graph size

```
Expected shape: [linear / quadratic / log-linear / etc.]
Actual shape: [describe what you observe]
```

#### 4.3.3 Theoretical vs. Empirical Comparison

TODO: Compare theoretical predictions with actual results

**Theoretical complexity:** O([your formula])
**Expected growth:** [describe expected growth pattern]

**Empirical results:**
- From 10 to 50 nodes: runtime increased by [X]×
- From 50 to 100 nodes: runtime increased by [Y]×
- Growth pattern: [matches / doesn't match] theoretical prediction

**Discrepancies:**
- [Explain any differences between theory and practice]
- Possible reasons: [constant factors, cache effects, Python overhead, etc.]

**Conclusion:** [Does your empirical data support your theoretical analysis?]

### 4.4 Comparison of Algorithms

TODO: Compare different algorithm variants

**Test:** Same graph, different algorithms

| Algorithm | Runtime (ms) | Nodes Explored | Path Length |
|-----------|--------------|----------------|-------------|
| Standard Dijkstra | [time] | [count] | [length] |
| Time-window Dijkstra | [time] | [count] | [length] |
| Time-window A* | [time] | [count] | [length] |

**Analysis:** [Which is faster? Why?]

---

## 5. Design Justification (2-3 pages)

### 5.1 Algorithm Selection

#### 5.1.1 Why I Chose [Dijkstra / A* / Bellman-Ford]

TODO: Detailed justification of your algorithm choice

**Context:** Three options available:
1. Dijkstra's algorithm
2. A* with haversine heuristic
3. Bellman-Ford algorithm

**My choice:** [algorithm]

**Reasons:**

1. **Compatibility with time windows:**
   - [Explain how time windows interact with this algorithm]
   - [Why is this algorithm well-suited?]

2. **Performance characteristics:**
   - Time complexity: [analysis]
   - Expected speedup from [heuristic / early termination / etc.]: [reasoning]

3. **Implementation simplicity:**
   - [Ease of modifying for time windows]
   - [Complexity of state management]

**Concrete example:**

Consider this graph: [describe a specific example]

- Dijkstra would: [behavior]
- A* would: [behavior]
- Bellman-Ford would: [behavior]

In this case, [your choice] is better because: [specific reasoning]

#### 5.1.2 Tradeoffs vs. Alternative Algorithms

TODO: Discuss what you gave up by not choosing alternatives

**vs. Dijkstra (if you didn't choose it):**
- **Advantage of Dijkstra:** [what it's good at]
- **Why I didn't choose it:** [reasoning]
- **Scenario where Dijkstra would be better:** [example]

**vs. A* (if you didn't choose it):**
- **Advantage of A*:** [what it's good at]
- **Why I didn't choose it:** [reasoning]
- **Scenario where A* would be better:** [example]

**vs. Bellman-Ford (if you didn't choose it):**
- **Advantage of Bellman-Ford:** [what it's good at]
- **Why I didn't choose it:** [reasoning]
- **Scenario where Bellman-Ford would be better:** [example]

#### 5.1.3 Modifying an Alternative Algorithm

TODO: Show how you would modify a DIFFERENT algorithm for the same task

**Algorithm:** [pick one you didn't implement]

**How to modify it for time windows:**

1. **State space:** [changes needed]
2. **Priority function:** [changes needed]
3. **Termination condition:** [changes needed]
4. **Special considerations:** [algorithm-specific issues]

**Pseudocode sketch:**
```
function alternative_algorithm_with_time_windows(...):
    // Modifications from standard version:
    // 1. ...
    // 2. ...
```

**Comparison with my approach:**
- **Similarities:** [what's the same?]
- **Differences:** [what's different?]
- **When would this be better?** [scenario]

### 5.2 Alternative Approaches for Speedup

#### 5.2.1 Speedup Approach #1: [Name]

TODO: Propose a concrete optimization

**Description:**

Detailed explanation of the optimization. For example:
> "Preprocess the graph to build an index of reachable nodes within time budgets. For each node v and time t, store which nodes can be reached from v within time t. During search, use this index to prune unreachable states early."

**Implementation details:**
- [How would you implement this?]
- [What data structures are needed?]
- [Preprocessing step: what and when?]

**Tradeoff analysis:**

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1: space / time / complexity]
- [Disadvantage 2]

**Speedup estimate:**

- **Order of magnitude:** [2× / 10× / 100× / etc.]
- **Reasoning:** [why this speedup?]
- **Best case:** [scenario where it works best]
- **Worst case:** [scenario where it provides no benefit]

**When it fails:**

This optimization is ineffective when:
1. [Scenario 1]
2. [Scenario 2]

**Graph properties that make it ineffective:**
- [Dense vs. sparse]
- [Wide vs. narrow time windows]
- [Other properties]

#### 5.2.2 Speedup Approach #2: [Name]

TODO: Propose a second optimization

**Description:**

[Detailed explanation]

**Implementation details:**

[How to implement]

**Tradeoff analysis:**

**Pros:**
-

**Cons:**
-

**Speedup estimate:**
- **Order of magnitude:** [X×]
- **Reasoning:** [why?]

**When it fails:**

[Scenarios and graph properties]

#### 5.2.3 Comparison of Speedup Approaches

| Aspect | Approach #1 | Approach #2 |
|--------|-------------|-------------|
| Speedup | [estimate] | [estimate] |
| Memory overhead | [analysis] | [analysis] |
| Implementation complexity | [low/med/high] | [low/med/high] |
| Best use case | [scenario] | [scenario] |

**Which would I choose?** [Approach X] because [reasoning]

---

## 6. Debugging and Optimization (1-2 pages)

### 6.1 Bug Hunt

#### 6.1.1 Identifying the Bug

TODO: Document which buggy file has the bug and what it is

**File analyzed:** route_planner_buggy.[c/py/go]

**Bug location:** [Line number and function]

**Bug description:**

```[language]
// Buggy code:
[paste the buggy code section]

// Correct code should be:
[paste the corrected version]
```

#### 6.1.2 Why It Causes Incorrect Results

TODO: Explain the bug's behavior

**What goes wrong:**
- [Describe the incorrect behavior]
- [Why does it produce "reasonable but wrong" results?]

**Example that triggers the bug:**

```
Input graph:
Nodes: [description]
Edges: [description]

Buggy output: [what it returns]
Correct output: [what it should return]
```

#### 6.1.3 How I Found the Bug

TODO: Document your debugging process

**Debugging steps:**

1. **Initial observation:**
   - Ran the buggy code on [test case]
   - Expected: [result]
   - Got: [different result]

2. **Hypothesis:**
   - Suspected the issue was in [component]
   - Reason: [why I thought this]

3. **Testing:**
   - Created test case: [description]
   - Added print statements to trace: [what values]
   - Observed: [what I found]

4. **Root cause:**
   - The bug is in [location] because [explanation]

5. **Verification:**
   - Fixed the bug
   - Tested on: [test cases]
   - All tests now pass

**Lesson learned:**
- [What this taught you about debugging / algorithm implementation]

### 6.2 Performance Optimization

#### 6.2.1 Profiling

TODO: Document profiling results

**Before optimization:**

```
Top functions by cumulative time:
1. dijkstra_with_time_windows: 450ms (90%)
2. heappop: 100ms (20%)
3. heappush: 80ms (16%)
...
```

**Bottleneck identified:**
- Function: [name]
- Why it's slow: [reason]
- [Number] of calls
- [Time] per call

#### 6.2.2 Optimization Implementation

TODO: Describe what you changed

**Problem:** [What was the bottleneck?]

**Solution:** [What did you change?]

**Code changes:**

```python
# Before:
[old code]

# After:
[new code]
```

**Why this helps:**
- [Explanation of why this is faster]
- [What operation is now cheaper?]

#### 6.2.3 Performance Measurements

TODO: Document before/after results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total runtime (ms) | [value] | [value] | [%] |
| Function calls | [value] | [value] | [%] |
| Memory usage (MB) | [value] | [value] | [%] |

**Did I achieve 20% speedup?** [YES/NO]

If yes:
- Actual speedup: [X]%
- This was achieved by: [summary]

If no:
- Best speedup achieved: [Y]%
- Why 20% wasn't possible: [explanation]
- Alternative approaches tried: [list]

#### 6.2.4 Tradeoffs

TODO: Discuss any tradeoffs

**What did the optimization cost?**

**Code complexity:**
- Before: [simple / moderate / complex]
- After: [simple / moderate / complex]
- [Is it harder to understand / maintain?]

**Memory usage:**
- [Increased / decreased / same]
- [By how much?]

**Correctness:**
- [Does it still produce correct results?]
- [Any edge cases now broken?]

**Conclusion:** The tradeoff is [worth it / not worth it] because [reasoning]

---

## 7. Conclusion (0.5 pages)

### 7.1 Summary

TODO: Summarize what you accomplished

In this lab, I:
1. Implemented [algorithm] for time-window constrained routing
2. Developed priority-based multi-destination routing with threshold parameter
3. Proved [what you proved] about correctness
4. Analyzed time complexity of O([formula]) and validated experimentally
5. Found and fixed a bug in [component]
6. Achieved [X]% performance improvement through [optimization]

### 7.2 Lessons Learned

TODO: Reflect on what you learned

**Technical lessons:**
1. [Lesson about algorithms]
2. [Lesson about implementation]
3. [Lesson about debugging/profiling]

**Conceptual lessons:**
1. [Understanding of time-window routing]
2. [Tradeoffs between different approaches]
3. [Real-world applications of graph algorithms]

### 7.3 Future Improvements

TODO: What would you do differently or extend?

**If I had more time:**
1. [Enhancement 1]
2. [Enhancement 2]
3. [Enhancement 3]

**Real-world extensions:**
- [How could this be adapted for actual delivery routing?]
- [What other constraints would be important?]
- [How to handle dynamic edge weights (traffic)?]

### 7.4 Reflection on AI Tool Usage

TODO: If you used AI tools, reflect on how

**Tools used:**
- [ChatGPT / Copilot / other]
- [For what purpose: debugging / explaining concepts / etc.]

**What worked well:**
- [Positive experiences]

**What didn't work:**
- [Where AI struggled or gave wrong answers]

**How I verified AI assistance:**
- [Testing / manual verification / understanding checks]

**Understanding achieved:**
- [Can you explain your code? Can you defend your proofs?]

---

## References

TODO: Cite any resources you used

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

2. Kleinberg, J., & Tardos, É. (2005). *Algorithm Design*. Pearson.

3. [Any papers on time-dependent shortest paths]

4. [Course materials]

5. [Online resources - be specific]

---

## Appendix

### A. Complete Test Cases

TODO: Include full test case definitions

### B. Profiling Output

TODO: Full profiling data (if not in profiling/ folder)

### C. Graph Visualizations

TODO: Any diagrams or visualizations (optional)

---

**Total pages: 8-12 (adjust sections as needed)**
