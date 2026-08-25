# CLRS Exercise Patterns — Advanced Algorithm Notes

Patterns for creating exercises and assignments for CLRS-style advanced algorithm topics.

## Exercise Type Mix

Each CLRS chapter gets 3–6 hands-on exercises mixing three types:

### Type 1: Coding Exercises (implement from note)
- Implement the algorithm described in the note
- Include TODO comments guiding the approach
- Test cases: "Test with X → expect Y"
- Examples: Union-Find, Extended Euclidean, RSA encrypt/decrypt, Miller-Rabin, Graham's scan

### Type 2: Trace-by-Hand Exercises (manual walkthrough)
- Give a specific input and ask the learner to step through the algorithm
- Provide blank tables to fill in (iteration, state, values)
- Examples:
  - B-tree: "Insert keys F,S,Q,K,C into B-tree with t=3. Draw after every split."
  - Bellman-Ford: "Trace relaxation for 4 iterations. Record d[v] after each."
  - Floyd-Warshall: "Compute D^(0), D^(1), ..., D^(4) as matrices."
  - Simplex: "Trace first pivot. Identify entering/leaving variables."
  - Dynamic tables: "Compute Φ before/after each INSERT."

### Type 3: Theory/Proof Exercises
- Prove correctness, amortized bounds, or reduction correctness
- Construct duals, verify weak duality
- Write formal NP-completeness reductions
- Examples:
  - "Prove O(1) amortized for DECREASE-KEY using Φ = t(H) + 2m(H)"
  - "Construct the dual LP and verify weak duality"
  - "Prove CLIQUE ≤_P INDEPENDENT-SET"

## Assignment Mix

Assignments for CLRS chapters mix:

| Type | When to Use | Example |
|------|-------------|---------|
| LeetCode problems | When the algorithm maps to classic problems | Union-Find → LC 323, 684, 721 |
| Theory problems | For proofs, analysis, complexity | "Prove MST uniqueness with distinct weights" |
| Mini-projects | For substantial implementations | "Implement B-tree insert with split" |
| Comparison exercises | When multiple algorithms solve same problem | "Compare Dijkstra: binary heap vs Fibonacci heap" |

## Chapter-Specific Patterns

### Amortized Analysis (Ch 17)
- Exercises: trace tables for aggregate/accounting/potential methods
- Assignments: prove bounds, implement dynamic array

### B-Trees (Ch 18)
- Exercises: trace insertion/deletion by hand
- Assignments: B-tree implementation project, B+ tree design

### Fibonacci Heaps (Ch 19)
- Exercises: trace consolidation, cascading cut
- Assignments: full implementation project, compare with binary heap

### van Emde Boas Trees (Ch 20)
- Exercises: trace INSERT/SUCCESSOR with u=16
- Assignments: implement proto-vEB, analyze recursion depth

### Disjoint Sets (Ch 21)
- Exercises: implement Union-Find with rank + compression
- Assignments: LeetCode problems (LC 323, 684, 721, 130, 305, 924)

### MST (Ch 23)
- Exercises: trace Kruskal's and Prim's by hand
- Assignments: LC 1584 (Min Cost to Connect All Points)

### Shortest Paths (Ch 24–25)
- Exercises: trace Bellman-Ford, Floyd-Warshall matrices
- Assignments: LC 743, 787, 1514, 1334

### Maximum Flow (Ch 26)
- Exercises: trace augmenting paths, identify min-cut
- Assignments: Edmonds-Karp implementation project

### Linear Programming (Ch 29)
- Exercises: convert standard/slack form, trace Simplex, construct duals
- Assignments: LP modeling problems, Simplex implementation

### Number Theory (Ch 31)
- Exercises: Extended Euclid, RSA small example, Miller-Rabin, CRT
- Assignments: LC 204, 50, 1201, 365; RSA/Miller-Rabin projects

### Geometry (Ch 33)
- Exercises: cross product, segment intersection, Graham's scan trace
- Assignments: LC 587, 149, 836, 973

### NP-Completeness (Ch 34)
- Exercises: write formal reductions
- Assignments: prove P=NP implications, reduction chain exercises

### Approximation (Ch 35)
- Exercises: trace approximation algorithms by hand
- Assignments: implement 2-approx vertex cover, prove ln(n) set cover bound
