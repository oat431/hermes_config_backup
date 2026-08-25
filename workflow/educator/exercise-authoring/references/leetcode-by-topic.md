# LeetCode Problems by Topic

Curated problem sets for algorithm and data-structure notes. Each topic maps to 6–10 problems with difficulty and key technique.

---

## 01 Data Structures

### Arrays & Linked Lists
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 1 | Two Sum | 🟢 Easy | Array + HashMap |
| LC 26 | Remove Duplicates from Sorted Array | 🟢 Easy | Two Pointers |
| LC 283 | Move Zeroes | 🟢 Easy | Two Pointers |
| LC 21 | Merge Two Sorted Lists | 🟢 Easy | Linked List Merge |
| LC 141 | Linked List Cycle | 🟢 Easy | Fast & Slow Pointers |
| LC 206 | Reverse Linked List | 🟢 Easy | Linked List |
| LC 15 | 3Sum | 🟡 Medium | Two Pointers + Sort |
| LC 19 | Remove Nth Node From End | 🟡 Medium | Two Pointers |
| LC 11 | Container With Most Water | 🟡 Medium | Two Pointers |
| LC 3 | Longest Substring Without Repeating | 🟡 Medium | Sliding Window |

### Deque
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 20 | Valid Parentheses | 🟢 Easy | Stack (Deque) |
| LC 225 | Implement Stack using Queues | 🟢 Easy | Deque as Stack |
| LC 239 | Sliding Window Maximum | 🔴 Hard | Monotonic Deque |
| LC 641 | Design Circular Deque | 🟡 Medium | Deque Implementation |
| LC 1438 | Longest Continuous Subarray With Abs Diff ≤ Limit | 🟡 Medium | Monotonic Deque |
| LC 1499 | Max Value of Equation | 🔴 Hard | Monotonic Deque |

### Hash Tables
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 1 | Two Sum | 🟢 Easy | HashMap Lookup |
| LC 217 | Contains Duplicate | 🟢 Easy | HashSet |
| LC 242 | Valid Anagram | 🟢 Easy | Frequency Count |
| LC 49 | Group Anagrams | 🟡 Medium | HashMap Grouping |
| LC 347 | Top K Frequent Elements | 🟡 Medium | HashMap + Heap |
| LC 128 | Longest Consecutive Sequence | 🟡 Medium | HashSet |
| LC 560 | Subarray Sum Equals K | 🟡 Medium | Prefix Sum + HashMap |
| LC 146 | LRU Cache | 🟡 Medium | LinkedHashMap / Map+DLL |

### Heaps & Priority Queues
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 703 | Kth Largest Element in a Stream | 🟢 Easy | Min-Heap of size K |
| LC 1046 | Last Stone Weight | 🟢 Easy | Max-Heap |
| LC 215 | Kth Largest Element in Array | 🟡 Medium | Min-Heap / Quickselect |
| LC 347 | Top K Frequent Elements | 🟡 Medium | HashMap + Heap |
| LC 973 | K Closest Points to Origin | 🟡 Medium | Max-Heap of size K |
| LC 295 | Find Median from Data Stream | 🔴 Hard | Two Heaps |
| LC 23 | Merge K Sorted Lists | 🔴 Hard | Min-Heap of list heads |
| LC 621 | Task Scheduler | 🟡 Medium | Max-Heap + Cooldown |

### Stacks & Queues
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 20 | Valid Parentheses | 🟢 Easy | Stack Matching |
| LC 232 | Implement Queue using Stacks | 🟢 Easy | Two Stacks |
| LC 155 | Min Stack | 🟡 Medium | Auxiliary Stack |
| LC 150 | Evaluate Reverse Polish Notation | 🟡 Medium | Stack Evaluation |
| LC 739 | Daily Temperatures | 🟡 Medium | Monotonic Stack |
| LC 503 | Next Greater Element II | 🟡 Medium | Monotonic Stack (Circular) |
| LC 394 | Decode String | 🟡 Medium | Stack (Nested) |
| LC 84 | Largest Rectangle in Histogram | 🔴 Hard | Monotonic Stack |

### Trees & BSTs
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 226 | Invert Binary Tree | 🟢 Easy | Recursion |
| LC 104 | Maximum Depth of Binary Tree | 🟢 Easy | DFS |
| LC 100 | Same Tree | 🟢 Easy | Recursion |
| LC 98 | Validate BST | 🟡 Medium | Inorder / Bounds |
| LC 102 | Level Order Traversal | 🟡 Medium | BFS (Queue) |
| LC 235 | Lowest Common Ancestor of BST | 🟡 Medium | BST Property |
| LC 236 | Lowest Common Ancestor of Binary Tree | 🟡 Medium | Recursion |
| LC 208 | Implement Trie | 🟡 Medium | Trie |

### Graphs
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 733 | Flood Fill | 🟢 Easy | DFS/BFS on Grid |
| LC 463 | Island Perimeter | 🟢 Easy | Grid Traversal |
| LC 200 | Number of Islands | 🟡 Medium | DFS/BFS Connected Components |
| LC 133 | Clone Graph | 🟡 Medium | BFS/DFS + HashMap |
| LC 207 | Course Schedule | 🟡 Medium | Topological Sort / Cycle Detection |
| LC 210 | Course Schedule II | 🟡 Medium | Topological Sort (Kahn's) |
| LC 127 | Word Ladder | 🔴 Hard | BFS on Implicit Graph |
| LC 743 | Network Delay Time | 🟡 Medium | Dijkstra's |

---

## 02 Algorithms

### Searching
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 704 | Binary Search | 🟢 Easy | Standard Binary Search |
| LC 35 | Search Insert Position | 🟢 Easy | Lower Bound |
| LC 278 | First Bad Version | 🟢 Easy | Lower Bound |
| LC 33 | Search in Rotated Sorted Array | 🟡 Medium | Modified Binary Search |
| LC 153 | Find Minimum in Rotated Sorted Array | 🟡 Medium | Binary Search |
| LC 875 | Koko Eating Bananas | 🟡 Medium | Binary Search on Answer |
| LC 162 | Find Peak Element | 🟡 Medium | Binary Search |
| LC 74 | Search a 2D Matrix | 🟡 Medium | Binary Search |

### Sorting
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 912 | Sort an Array | 🟡 Medium | Merge / Quick Sort |
| LC 88 | Merge Sorted Array | 🟢 Easy | Merge (Two Pointers) |
| LC 75 | Sort Colors | 🟡 Medium | Dutch National Flag |
| LC 56 | Merge Intervals | 🟡 Medium | Sort + Merge |
| LC 215 | Kth Largest Element | 🟡 Medium | Quickselect |
| LC 324 | Wiggle Sort II | 🟡 Medium | Sort + Interleave |
| LC 164 | Maximum Gap | 🔴 Hard | Radix Sort / Bucket |
| LC 315 | Count of Smaller Numbers After Self | 🔴 Hard | Merge Sort + Count |

### Recursion & Backtracking
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 78 | Subsets | 🟡 Medium | Backtracking (Include/Exclude) |
| LC 46 | Permutations | 🟡 Medium | Backtracking (Used Array) |
| LC 39 | Combination Sum | 🟡 Medium | Backtracking + Pruning |
| LC 17 | Letter Combinations of Phone Number | 🟡 Medium | Backtracking |
| LC 22 | Generate Parentheses | 🟡 Medium | Backtracking + Pruning |
| LC 79 | Word Search | 🟡 Medium | DFS + Backtracking on Grid |
| LC 51 | N-Queens | 🔴 Hard | Backtracking |
| LC 37 | Sudoku Solver | 🔴 Hard | Backtracking |

### Divide & Conquer
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 912 | Sort an Array | 🟡 Medium | Merge Sort |
| LC 53 | Maximum Subarray | 🟡 Medium | D&C / Kadane's |
| LC 169 | Majority Element | 🟢 Easy | D&C / Boyer-Moore |
| LC 215 | Kth Largest Element | 🟡 Medium | Quickselect (D&C) |
| LC 241 | Different Ways to Add Parentheses | 🟡 Medium | D&C Recursion |
| LC 4 | Median of Two Sorted Arrays | 🔴 Hard | Binary Search D&C |

### Greedy
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 121 | Best Time to Buy and Sell Stock | 🟢 Easy | Greedy (track min) |
| LC 55 | Jump Game | 🟡 Medium | Greedy Reach |
| LC 45 | Jump Game II | 🟡 Medium | Greedy (BFS-like) |
| LC 435 | Non-overlapping Intervals | 🟡 Medium | Activity Selection |
| LC 763 | Partition Labels | 🟡 Medium | Greedy (last occurrence) |
| LC 621 | Task Scheduler | 🟡 Medium | Greedy (frequency) |
| LC 452 | Minimum Number of Arrows | 🟡 Medium | Interval Greedy |
| LC 135 | Candy | 🔴 Hard | Greedy (two passes) |

### Dynamic Programming
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 70 | Climbing Stairs | 🟢 Easy | 1D DP (Fibonacci) |
| LC 198 | House Robber | 🟡 Medium | 1D DP |
| LC 322 | Coin Change | 🟡 Medium | 1D DP (Unbounded Knapsack) |
| LC 300 | Longest Increasing Subsequence | 🟡 Medium | 1D DP / Binary Search |
| LC 1143 | Longest Common Subsequence | 🟡 Medium | 2D DP |
| GFG | 0/1 Knapsack | 🟡 Medium | 2D DP |
| LC 72 | Edit Distance | 🟡 Medium | 2D DP |
| LC 139 | Word Break | 🟡 Medium | 1D DP + HashSet |
| LC 62 | Unique Paths | 🟡 Medium | 2D DP |

### String Algorithms
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 28 | Find Index of First Occurrence | 🟢 Easy | String Matching |
| LC 242 | Valid Anagram | 🟢 Easy | Frequency Count |
| LC 459 | Repeated Substring Pattern | 🟢 Easy | KMP / Pattern |
| LC 5 | Longest Palindromic Substring | 🟡 Medium | Expand Around Center / DP |
| LC 49 | Group Anagrams | 🟡 Medium | Hash + Anagram Key |
| LC 76 | Minimum Window Substring | 🔴 Hard | Sliding Window + HashMap |
| LC 214 | Shortest Palindrome | 🔴 Hard | KMP LPS |

### Math Algorithms
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 204 | Count Primes | 🟡 Medium | Sieve of Eratosthenes |
| LC 50 | Pow(x, n) | 🟡 Medium | Fast Exponentiation |
| LC 1492 | The kth Factor of n | 🟡 Medium | Divisors |
| LC 263 | Ugly Number | 🟢 Easy | GCD / Prime Factors |
| LC 1071 | GCD of Strings | 🟢 Easy | GCD on Strings |
| LC 372 | Super Pow | 🟡 Medium | Modular Exponentiation |
| LC 357 | Count Numbers with Unique Digits | 🟡 Medium | Combinatorics |
| LC 878 | Nth Magical Number | 🔴 Hard | LCM + Binary Search |

---

## 03 Problem Solving

### Patterns & Strategies (Mixed)
| # | Problem | Difficulty | Technique |
|---|---------|:----------:|-----------|
| LC 1 | Two Sum | 🟢 Easy | HashMap |
| LC 53 | Maximum Subarray | 🟡 Medium | Kadane's / DP |
| LC 56 | Merge Intervals | 🟡 Medium | Sort + Merge |
| LC 3 | Longest Substring Without Repeating | 🟡 Medium | Sliding Window |
| LC 11 | Container With Most Water | 🟡 Medium | Two Pointers |
| LC 560 | Subarray Sum Equals K | 🟡 Medium | Prefix Sum + HashMap |
| LC 200 | Number of Islands | 🟡 Medium | BFS/DFS |
| LC 207 | Course Schedule | 🟡 Medium | Topological Sort |
| LC 146 | LRU Cache | 🟡 Medium | HashMap + DLL |
| LC 4 | Median of Two Sorted Arrays | 🔴 Hard | Binary Search |
