"""
curriculum_dsa.py - Complete 10 Chapters for Data Structures & Algorithms (DSA).
Every chapter contains:
1. Detailed Concepts & In-Depth Explanation
2. Key Formulas, Rules & Complexity Classes
3. Step-by-Step Solved Examples with code and line-by-line breakdown
4. Practice Questions with Answers & Explanations
5. Company Placement Technical Interview Questions & Answers
"""
from typing import List, Dict, Any

DSA_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Asymptotic Analysis, Complexity Classes & Recurrence Relations",
        "key_takeaways": "Master Big-O, Big-Omega, Big-Theta, recursion tree proofs, and the Master Theorem across all cases to evaluate any placement algorithm.",
        "topics": [
            "Formal definitions of Big-O, Big-Omega, Big-Theta",
            "Master Theorem for Divide-and-Conquer recurrences: T(n) = a*T(n/b) + f(n)",
            "Recursion tree method and substitution method proofs",
            "Space complexity: Auxiliary space vs call stack frame memory",
            "Complexity hierarchy: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!)"
        ],
        "sections": {
            "concept": """Asymptotic analysis is the mathematical foundation of algorithmic performance evaluation. Rather than measuring wall-clock time in seconds (which varies based on hardware architecture, background OS threads, and compiler optimizations), asymptotic analysis characterizes how execution time and memory space grow as input size $n$ approaches infinity ($n \\to \\infty$).

In top corporate campus recruitment (Google, Amazon, Microsoft, Flipkart, Uber, TCS Digital), candidates are expected to rigorously justify the bounds of their algorithms:
- **Big-O ($O$):** Mathematical upper bound representing worst-case time or space.
- **Big-Omega ($\Omega$):** Mathematical lower bound representing best-case performance.
- **Big-Theta ($\Theta$):** Asymptotically tight bound holding when an algorithm's upper and lower bounds coincide.

When evaluating recursive algorithms, divide-and-conquer recurrences partition problems of size $n$ into $a$ subproblems each of size $n/b$, with $f(n)$ work spent splitting and merging. The Master Theorem provides an immediate closed-form solution by comparing $f(n)$ to the critical leaf-cost polynomial $n^{\\log_b a}$.""",
            "formulas": """1. **Big-O Definition:**
   $$f(n) = O(g(n)) \\iff \\exists c > 0, n_0 \\ge 0 \\text{ s.t. } 0 \\le f(n) \\le c \\cdot g(n) \\quad \\forall n \\ge n_0$$
2. **Big-Omega Definition:**
   $$f(n) = \\Omega(g(n)) \\iff \\exists c > 0, n_0 \\ge 0 \\text{ s.t. } 0 \\le c \\cdot g(n) \\le f(n) \\quad \\forall n \\ge n_0$$
3. **Big-Theta Definition:**
   $$f(n) = \\Theta(g(n)) \\iff f(n) = O(g(n)) \\text{ and } f(n) = \\Omega(g(n))$$
4. **Master Theorem:**
   For $T(n) = a T(n/b) + f(n)$ where $a \\ge 1, b > 1$:
   - **Case 1 (Leaves Dominate):** If $f(n) = O(n^{\\log_b a - \\epsilon})$ for $\\epsilon > 0 \\implies T(n) = \\Theta(n^{\\log_b a})$
   - **Case 2 (Even Balance):** If $f(n) = \\Theta(n^{\\log_b a} \\cdot \\log^k n)$ for $k \\ge 0 \\implies T(n) = \\Theta(n^{\\log_b a} \\cdot \\log^{k+1} n)$
   - **Case 3 (Root Dominates):** If $f(n) = \\Omega(n^{\\log_b a + \\epsilon})$ for $\\epsilon > 0$ and $a f(n/b) \\le c f(n)$ for $c < 1 \\implies T(n) = \\Theta(f(n))$""",
            "solved_examples": [
                {
                    "title": "Merge Sort Recurrence Derivation",
                    "difficulty": "Medium | Amazon, Microsoft, TCS Digital",
                    "problem": "Solve the recurrence relation $T(n) = 2T(n/2) + cn$ with base case $T(1) = d$.",
                    "step_by_step": [
                        "Step 1: Extract recurrence parameters: $a = 2$, $b = 2$, $f(n) = cn = \\Theta(n^1)$.",
                        "Step 2: Calculate the boundary exponent: $n^{\\log_b a} = n^{\\log_2 2} = n^1 = n$.",
                        "Step 3: Compare $f(n)$ with $n^{\\log_b a}$. Both equal $n$, fitting Master Theorem Case 2 with $k = 0$.",
                        "Step 4: Compute final complexity: $T(n) = \\Theta(n^1 \\cdot \\log^{0+1} n) = \\Theta(n \\log n)$."
                    ],
                    "code_or_math": """def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged""",
                    "explanation": "At depth $k$ of the recursion tree, there are $2^k$ subproblems each operating on arrays of size $n/2^k$. The work at depth $k$ is $2^k \\times c(n/2^k) = cn$. Since the tree has $\\log_2 n$ levels, total work is $cn \\log_2 n = \\Theta(n \\log n)$. Auxiliary space is $O(n)$ for temporary arrays."
                },
                {
                    "title": "Binary Search Recurrence & Proof",
                    "difficulty": "Easy | Google, Infosys, Cognizant",
                    "problem": "Prove that binary search on a sorted array of size $n$ takes $O(\\log n)$ time.",
                    "step_by_step": [
                        "Step 1: In each iteration or recursive call, the search interval $[left, right]$ is halved: $T(n) = T(n/2) + O(1)$.",
                        "Step 2: Master Theorem parameters: $a = 1, b = 2, f(n) = O(1) = \\Theta(n^0)$.",
                        "Step 3: $n^{\\log_b a} = n^{\\log_2 1} = n^0 = 1 = \\Theta(f(n))$.",
                        "Step 4: Case 2 applies with $k = 0$: $T(n) = \\Theta(1 \\cdot \\log^1 n) = \\Theta(\\log n)$."
                    ],
                    "code_or_math": """def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2  # Safe calculation preventing 32-bit overflow
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
                    "explanation": "Halving the search space repeatedly produces sequence $n, n/2, n/4, \\dots, 1$. When $n/2^k = 1$, $2^k = n \\implies k = \\log_2 n$ iterations. Total time is strictly $O(\\log n)$ with $O(1)$ auxiliary space."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the tight bound $\\Theta$ of $T(n) = 8T(n/2) + 1000n^2$?",
                    "options": [
                        "A) $\\Theta(n^2)$",
                        "B) $\\Theta(n^3)$",
                        "C) $\\Theta(n^3 \\log n)$",
                        "D) $\\Theta(n^2 \\log n)$"
                    ],
                    "correct_answer": "B) $\\Theta(n^3)$",
                    "detailed_solution": "Here $a = 8, b = 2 \\implies n^{\\log_2 8} = n^3$. Since $f(n) = 1000n^2 = O(n^{3 - \\epsilon})$ for $\\epsilon = 1$, Master Theorem Case 1 applies. The leaf cost dominates: $T(n) = \\Theta(n^3)$."
                },
                {
                    "question": "Which of the following describes the space complexity of an in-order traversal of a balanced binary search tree with $n$ nodes?",
                    "options": [
                        "A) $O(1)$ auxiliary space",
                        "B) $O(\\log n)$ call stack space",
                        "C) $O(n)$ call stack space",
                        "D) $O(n^2)$ space"
                    ],
                    "correct_answer": "B) $O(\\log n)$ call stack space",
                    "detailed_solution": "In a balanced binary tree, maximum recursion depth corresponds to tree height $h = \\log_2 n$. Hence, the execution stack holds at most $O(\\log n)$ activation records simultaneously."
                },
                {
                    "question": "If an algorithm performs $1 + 2 + 3 + \\dots + n$ operations, what is its asymptotic complexity?",
                    "options": [
                        "A) $O(n)$",
                        "B) $O(n \\log n)$",
                        "C) $O(n^2)$",
                        "D) $O(2^n)$"
                    ],
                    "correct_answer": "C) $O(n^2)$",
                    "detailed_solution": "The arithmetic sum $\\sum_{i=1}^n i = \\frac{n(n+1)}{2} = \\frac{n^2 + n}{2} = \\Theta(n^2)$."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "Why is Quicksort preferred over Mergesort for internal sorting of arrays in C++ (std::sort), even though Quicksort has a worst-case of O(n^2)?",
                    "model_answer": "Quicksort has superior cache locality because it partitions elements in-place with contiguous memory reads. In contrast, Mergesort requires $O(n)$ auxiliary buffer allocation and continuous buffer copying, which incurs high cache miss penalties. Furthermore, randomized pivot selection or median-of-three heuristics makes Quicksort's worst-case probability infinitesimally small in practice ($O(n \\log n)$ average with smaller constant factors).",
                    "interviewer_tip": "Highlight hardware cache lines (L1/L2) and in-place partitioning mechanics."
                },
                {
                    "company": "Amazon",
                    "question": "What is the difference between Amortized Complexity and Average Case Complexity?",
                    "model_answer": "Average-case complexity considers probabilistic assumptions over all possible input distributions (e.g., assuming any permutation is equally likely in Quicksort). In contrast, Amortized complexity makes zero probabilistic assumptions about inputs: it guarantees the average cost per operation across any arbitrary sequence of $m$ operations in the worst case (e.g., dynamic array resizing where $N$ appends cost $O(N)$ total, so amortized cost per append is strictly $O(1)$).",
                    "interviewer_tip": "Cite the dynamic array vector doubling or aggregate accounting method to prove amortized $O(1)$."
                },
                {
                    "company": "Microsoft",
                    "question": "How do you solve a recurrence relation where subproblem sizes decrease by a constant amount, such as T(n) = T(n-1) + n?",
                    "model_answer": "For linear recurrences where $T(n) = T(n-1) + f(n)$, the Master Theorem cannot be used. We apply the iterative unrolling method: $T(n) = T(n-1) + n = T(n-2) + (n-1) + n = \\dots = T(1) + 2 + 3 + \\dots + n = \\Theta(n^2)$.",
                    "interviewer_tip": "Mention that this exact recurrence governs the worst-case behavior of Quicksort when the array is already sorted and the extreme element is chosen as pivot."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Arrays, Strings, Two Pointers & Sliding Window",
        "key_takeaways": "Master contiguous memory allocation, amortized doubling, opposite/same-directional two pointers, fixed/dynamic sliding window, and Kadane's algorithm.",
        "topics": [
            "Dynamic arrays memory allocation and amortized O(1) appending",
            "Opposite-directional two pointers (Two Sum II, Container With Most Water)",
            "Fast & slow pointers (In-place deduplication, partitioning)",
            "Fixed-size sliding window (Max sum subarray of size k)",
            "Variable-size sliding window with hash map (Longest substring without repeating characters)",
            "Kadane's algorithm for maximum contiguous subarray sum in O(n)"
        ],
        "sections": {
            "concept": """Arrays provide contiguous physical memory storage, granting $O(1)$ random index access via base address arithmetic: $\\text{Address}(arr[i]) = \\text{Base} + i \\times \\text{SizeOfElement}$. Dynamic arrays automatically resize when capacity is reached, doubling the buffer size to achieve amortized $O(1)$ append time.

Two Pointers and Sliding Window are fundamental algorithmic archetypes that reduce brute-force $O(n^2)$ nested search spaces down to optimal $O(n)$ single-pass execution:
1. **Opposite-Directional Two Pointers:** Pointers initialize at array boundaries (`left = 0`, `right = n - 1`) and converge toward each other based on monotonic conditions.
2. **Same-Directional (Fast & Slow):** Pointers move in the same direction at varying rates to filter, deduplicate, or partition elements in-place with $O(1)$ auxiliary memory.
3. **Sliding Window:** Maintains a contiguous subarray sub-state. In fixed windows of size $K$, the window slides forward by adding the incoming element and subtracting the outgoing element in $O(1)$. In dynamic windows, the `right` pointer expands the window until a condition is violated, whereupon the `left` pointer contracts the window until validity is restored.""",
            "formulas": """1. **Amortized Analysis (Accounting Method):**
   Charging $\$3$ per insertion: $\$1$ pays for insertion into array; $\$2$ credit banked. When array doubles from $N$ to $2N$, the $N$ banked credits pay for copying all $N$ elements into new memory. Amortized cost $= O(1)$.
2. **Fixed Sliding Window Sum Invariant:**
   $$\\text{WindowSum}_{i} = \\text{WindowSum}_{i-1} + arr[i] - arr[i - K]$$
3. **Kadane's Dynamic Recurrence:**
   $$\\text{CurrentMax}[i] = \\max(arr[i], \\text{CurrentMax}[i-1] + arr[i])$$
   $$\\text{GlobalMax} = \\max_{0 \\le i < n}(\\text{CurrentMax}[i])$$""",
            "solved_examples": [
                {
                    "title": "Container With Most Water (Optimal Two Pointers)",
                    "difficulty": "Medium | Google, Amazon, Flipkart",
                    "problem": "Given an integer array height of length $n$, find two lines that together with the x-axis form a container that contains the most water. Return the maximum area.",
                    "step_by_step": [
                        "Step 1: The area between two boundaries at index $i$ and $j$ is $\\text{Area} = (j - i) \\times \\min(height[i], height[j])$.",
                        "Step 2: Start with maximum width: `left = 0`, `right = n - 1`.",
                        "Step 3: At each step, the area is bounded by the shorter line. Moving the taller pointer cannot increase the area because width decreases while height remains limited by the shorter line.",
                        "Step 4: Therefore, greedily advance the pointer pointing to the shorter vertical bar."
                    ],
                    "code_or_math": """def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water""",
                    "explanation": "Since every step advances one pointer inward, the loop executes at most $n$ times. Time complexity is strictly $O(n)$ with $O(1)$ auxiliary space, compared to the brute force $O(n^2)$ approach."
                },
                {
                    "title": "Longest Substring Without Repeating Characters (Dynamic Window)",
                    "difficulty": "Medium | Microsoft, Uber, TCS Digital",
                    "problem": "Given a string `s`, find the length of the longest substring without repeating characters.",
                    "step_by_step": [
                        "Step 1: Maintain a hash map `char_index` storing the most recent 0-based index of each character encountered.",
                        "Step 2: Initialize `left = 0` and `max_len = 0`.",
                        "Step 3: Iterate `right` from 0 to len(s) - 1. If `s[right]` is already in `char_index` and its recorded position is $\\ge left$, jump `left = char_index[s[right]] + 1`.",
                        "Step 4: Update `char_index[s[right]] = right` and calculate `max_len = max(max_len, right - left + 1)`."
                    ],
                    "code_or_math": """def length_of_longest_substring(s: str) -> int:
    char_index = {}
    left = 0
    max_len = 0
    for right, ch in enumerate(s):
        if ch in char_index and char_index[ch] >= left:
            left = char_index[ch] + 1
        char_index[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len""",
                    "explanation": "The right pointer visits each character once. The left pointer only jumps forward, never backward. Time complexity is $O(n)$. Auxiliary space is $O(\\min(n, m))$ where $m$ is the character alphabet size (at most 128 for ASCII)."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the time and space complexity of Kadane's algorithm for finding the maximum subarray sum?",
                    "options": [
                        "A) $O(n)$ time, $O(n)$ space",
                        "B) $O(n)$ time, $O(1)$ space",
                        "C) $O(n \\log n)$ time, $O(1)$ space",
                        "D) $O(n^2)$ time, $O(1)$ space"
                    ],
                    "correct_answer": "B) $O(n)$ time, $O(1)$ space",
                    "detailed_solution": "Kadane's algorithm scans the array in a single pass maintaining two scalar variables: `current_sum` and `max_sum`. Thus it requires strictly $O(n)$ time and $O(1)$ auxiliary space."
                },
                {
                    "question": "In the Two Sum II problem on a sorted array, if `arr[left] + arr[right] > target`, what is the optimal next move?",
                    "options": [
                        "A) Increment `left`",
                        "B) Decrement `right`",
                        "C) Reset `left = 0`",
                        "D) Break the loop"
                    ],
                    "correct_answer": "B) Decrement `right`",
                    "detailed_solution": "Because the array is sorted in ascending order, decreasing `right` reduces the sum, moving it closer to the target."
                },
                {
                    "question": "When does the amortized cost of an operation differ from its worst-case cost?",
                    "options": [
                        "A) Only when recursion is used",
                        "B) When occasional expensive operations are offset by numerous cheap operations",
                        "C) When space complexity exceeds $O(n)$",
                        "D) Amortized cost is always identical to worst-case cost"
                    ],
                    "correct_answer": "B) When occasional expensive operations are offset by numerous cheap operations",
                    "detailed_solution": "Dynamic array resizing takes $O(n)$ in the worst case, but occurs so infrequently that across a sequence of $n$ operations, the average cost per operation is strictly $O(1)$."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "How would you handle negative numbers when applying the Sliding Window technique to find a subarray with sum equal to $K$?",
                    "model_answer": "The standard two-pointer sliding window relies on monotonicity (expanding increases sum, contracting decreases sum). When negative numbers exist, monotonicity is violated. Instead, we use Prefix Sums with a Hash Map. We maintain running `prefix_sum`. If `prefix_sum - K` exists in our hash map, the subarray between that recorded index and the current index sums exactly to $K$. This runs in $O(n)$ time and $O(n)$ space.",
                    "interviewer_tip": "Identifying when sliding window breaks and seamlessly transitioning to prefix sums + hash maps is an instant hire signal."
                },
                {
                    "company": "Flipkart",
                    "question": "Explain how to remove duplicates from a sorted array in-place with $O(1)$ extra memory.",
                    "model_answer": "Use two pointers: a slow pointer `write_idx = 1` and a fast pointer `i` iterating from 1 to $n-1$. Compare `arr[i]` with `arr[write_idx - 1]`. If they are different, copy `arr[write_idx] = arr[i]` and increment `write_idx`. At the end of the loop, `write_idx` holds the length of the deduplicated array.",
                    "interviewer_tip": "State clearly that the first element is always unique, so indices start at 1."
                },
                {
                    "company": "Microsoft",
                    "question": "Given an array of integers representing stock prices, how does Kadane's algorithm relate to finding the maximum single-trade profit?",
                    "model_answer": "The maximum stock profit problem ($\\max(prices[j] - prices[i])$ for $j > i$) can be transformed into the maximum subarray sum problem by taking differences between consecutive days: $\\Delta[k] = prices[k] - prices[k-1]$. The sum of differences $\\sum_{k=i+1}^j \\Delta[k] = prices[j] - prices[i]$ telescopes. Finding the maximum contiguous subarray sum of $\\Delta$ using Kadane's algorithm yields the maximum profit in $O(n)$ time and $O(1)$ space.",
                    "interviewer_tip": "Mentioning the telescoping sum equivalence showcases deep mathematical maturity."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Linked Lists & Fast-and-Slow Pointer Techniques",
        "key_takeaways": "Master node reference manipulation, in-place reversal, Floyd's Cycle Detection proof, fast/slow mid-finding, and LRU Cache doubly linked list architecture.",
        "topics": [
            "Singly vs doubly linked list memory models and pointer manipulation",
            "In-place iterative linked list reversal in O(n) time and O(1) space",
            "Floyd's Cycle Detection Algorithm (Tortoise and Hare) and mathematical proof",
            "Finding the middle node and palindromic linked list verification",
            "LRU Cache design using Hash Map + Doubly Linked List with O(1) get/put"
        ],
        "sections": {
            "concept": """Linked lists represent non-contiguous linear collections where each node stores a payload and one or more references (`next`, `prev`) to adjacent nodes. Unlike arrays, linked lists allow $O(1)$ insertions and deletions at known pointer positions without requiring element shifting, at the expense of losing $O(1)$ random indexing.

Floyd's Cycle Finding Algorithm (Tortoise and Hare) is an essential placement pattern. Two pointers traverse the list: `slow` advances 1 step per cycle while `fast` advances 2 steps. If a cycle exists, `fast` must enter the cycle and catch up to `slow` from behind because the distance between them shrinks by exactly 1 node per iteration. Once they collide, resetting `slow` to the head and advancing both pointers at 1 step per iteration leads directly to the cycle origin node.""",
            "formulas": """1. **Floyd's Cycle Distance Proof:**
   Let distance from head to cycle entrance $= L_1$.
   Let distance from cycle entrance to collision point $= L_2$.
   Let cycle perimeter $= C$.
   $$\\text{Distance}(\\text{slow}) = L_1 + L_2$$
   $$\\text{Distance}(\\text{fast}) = L_1 + L_2 + k \\cdot C$$
   Since $\\text{speed}(\\text{fast}) = 2 \\times \\text{speed}(\\text{slow})$:
   $$2(L_1 + L_2) = L_1 + L_2 + k \\cdot C \\implies L_1 + L_2 = k \\cdot C \\implies L_1 = k \\cdot C - L_2$$
   Hence, advancing a pointer from the head and one from the collision point at equal speeds causes them to meet at the cycle entrance!""",
            "solved_examples": [
                {
                    "title": "Reverse a Singly Linked List In-Place",
                    "difficulty": "Easy | Google, Amazon, TCS",
                    "problem": "Given the head of a singly linked list, reverse the list in-place and return the reversed list head.",
                    "step_by_step": [
                        "Step 1: Maintain three pointers: `prev = None`, `curr = head`, and `next_temp = None`.",
                        "Step 2: While `curr` is not null: save `next_temp = curr.next`.",
                        "Step 3: Reverse the current node pointer: `curr.next = prev`.",
                        "Step 4: Shift pointers forward: `prev = curr`, `curr = next_temp`.",
                        "Step 5: Return `prev` as the new head."
                    ],
                    "code_or_math": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev""",
                    "explanation": "Each node pointer is modified exactly once. Time complexity is $O(n)$ and auxiliary space is $O(1)$ because no new nodes are allocated."
                },
                {
                    "title": "Detect Cycle & Find Cycle Origin (Floyd's Algorithm)",
                    "difficulty": "Medium | Microsoft, Uber, Adobe",
                    "problem": "Given head of a linked list, return the node where the cycle begins. If no cycle exists, return null.",
                    "step_by_step": [
                        "Step 1: Initialize `slow = fast = head`.",
                        "Step 2: Advance `slow` by 1 and `fast` by 2 until `fast` is null or `slow == fast`.",
                        "Step 3: If `fast` reaches null, no cycle exists; return null.",
                        "Step 4: If collision occurs, reset `slow = head`.",
                        "Step 5: Advance both `slow` and `fast` by 1 step simultaneously. Their meeting node is the cycle start."
                    ],
                    "code_or_math": """def detect_cycle(head: ListNode) -> ListNode:
    slow = fast = head
    has_cycle = False
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            has_cycle = True
            break
    if not has_cycle:
        return None
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    return slow""",
                    "explanation": "Finding the collision takes $O(n)$ time. Locating the entrance takes $L_1 \\le n$ steps. Total time is $O(n)$ with $O(1)$ auxiliary space."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the time complexity to find the middle element of a linked list using the fast and slow pointer technique?",
                    "options": [
                        "A) $O(n)$ time, $O(n)$ space",
                        "B) $O(n)$ time, $O(1)$ space",
                        "C) $O(n^2)$ time, $O(1)$ space",
                        "D) $O(\\log n)$ time, $O(1)$ space"
                    ],
                    "correct_answer": "B) $O(n)$ time, $O(1)$ space",
                    "detailed_solution": "Fast pointer traverses $n$ nodes while slow traverses $n/2$ nodes in a single pass. Auxiliary memory consists of two pointers, taking strictly $O(1)$ space."
                },
                {
                    "question": "Why is a Doubly Linked List paired with a Hash Map in an LRU Cache implementation?",
                    "options": [
                        "A) To achieve $O(1)$ random indexing",
                        "B) To allow $O(1)$ node removal and insertion at both head and tail given node reference",
                        "C) To save memory over arrays",
                        "D) To automatically sort keys"
                    ],
                    "correct_answer": "B) To allow $O(1)$ node removal and insertion at both head and tail given node reference",
                    "detailed_solution": "In a singly linked list, deleting a node requires finding its predecessor in $O(n)$. A doubly linked list node stores `prev`, enabling $O(1)$ disconnection and relocation to the most-recently-used position."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "Design an LRU Cache with get(key) and put(key, value) operations executing in O(1) time.",
                    "model_answer": "Use a Hash Map mapping `key` to `Node(key, value)` and a Doubly Linked List with dummy `head` and `tail` sentinels. For `get(key)`: look up node in hash map; if present, unlink node and move it to `head.next` (most recently used), returning value. For `put(key, value)`: if key exists, update value and move to head. If key does not exist and cache is at capacity, remove the least recently used node at `tail.prev`, erase it from hash map, and insert new node at head.",
                    "interviewer_tip": "Always mention dummy head and tail sentinel nodes because they eliminate null checks on edge insertions/deletions."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Stacks, Queues & Monotonic Data Structures",
        "key_takeaways": "Master LIFO/FIFO mechanics, expression evaluation, monotonic stack pattern for Next Greater Element, and monotonic deque for sliding window maximum.",
        "topics": [
            "Stack & Queue abstract data types and array/linked-list backing",
            "Infix, prefix, and postfix expression evaluation and parenthesis balancing",
            "Monotonic Stack pattern: Next Greater Element and Next Smaller Element in O(n)",
            "Largest Rectangle in Histogram solved in O(n) via monotonic stack",
            "Sliding Window Maximum in O(n) via monotonic doubly-ended queue (deque)"
        ],
        "sections": {
            "concept": """Stacks (Last-In, First-Out: LIFO) and Queues (First-In, First-Out: FIFO) are core linear data structures managing constrained access orders. Stacks power runtime execution calls, depth-first searches, and backtracking, while Queues manage task scheduling, buffering, and breadth-first search.

The **Monotonic Stack / Deque** is an advanced pattern crucial for top-tier placement assessments. A monotonic stack maintains elements in strictly increasing or decreasing order. As each element is processed, existing elements that violate the monotonic invariant are popped off. Although elements are pushed and popped inside loops, every element enters and exits the stack at most once, delivering strictly $O(n)$ amortized running time across the entire array.""",
            "formulas": """1. **Monotonic Stack Invariant (Decreasing Stack for Next Greater Element):**
   When processing element $x$:
   $$\\text{while } (\\text{stack not empty} \\text{ and } \\text{stack.top}() < x): \\quad \\text{pop}() \\implies \\text{NextGreater}(\\text{popped}) = x$$
2. **Amortized Time Proof:**
   Each of $n$ elements is pushed once and popped at most once. Total push operations $= n$, total pop operations $\\le n$. Total work $\\le 2n = O(n)$.""",
            "solved_examples": [
                {
                    "title": "Next Greater Element I",
                    "difficulty": "Medium | Amazon, Flipkart, Goldman Sachs",
                    "problem": "Given an array of integers, find the next greater element for each item. If no greater element exists to the right, return -1.",
                    "step_by_step": [
                        "Step 1: Initialize an array `result` of size $n$ filled with -1, and an empty stack `st`.",
                        "Step 2: Iterate through the array with index `i` from 0 to $n-1$.",
                        "Step 3: While `st` is not empty and `arr[i] > arr[st[-1]]`: pop index `idx = st.pop()` and record `result[idx] = arr[i]`.",
                        "Step 4: Push current index `i` onto `st`.",
                        "Step 5: Remaining elements in stack have no greater element to their right (remain -1)."
                    ],
                    "code_or_math": """def next_greater_elements(nums):
    n = len(nums)
    res = [-1] * n
    stack = []  # Stores indices
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            res[idx] = nums[i]
        stack.append(i)
    return res""",
                    "explanation": "Each index is pushed once and popped once. Overall time complexity is strictly $O(n)$ with $O(n)$ auxiliary space."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the time complexity of finding the Largest Rectangle in Histogram using a monotonic stack?",
                    "options": [
                        "A) $O(n^2)$",
                        "B) $O(n \\log n)$",
                        "C) $O(n)$",
                        "D) $O(n^3)$"
                    ],
                    "correct_answer": "C) $O(n)$",
                    "detailed_solution": "By maintaining an increasing monotonic stack of bar indices, each bar is pushed and popped at most once to determine left and right boundaries, yielding $O(n)$ time."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "How does a Monotonic Deque solve Sliding Window Maximum in O(n) compared to a Priority Queue in O(n log k)?",
                    "model_answer": "A Priority Queue requires $O(\\log k)$ to push and pop window elements, resulting in $O(n \\log k)$ total time. A Monotonic Deque stores indices of elements in descending order. When sliding the window: 1) Pop indices from the front that have fallen out of the window (`dq[0] < i - k + 1`). 2) Pop indices from the back whose values are $\\le arr[i]$ since they can never be the maximum again. 3) Push `i` to back. The maximum of the current window is always at `dq[0]`. Since every index enters and leaves the deque at most once, total time is strictly $O(n)$.",
                    "interviewer_tip": "Mention that deque stores indices rather than values so expired window items can be identified in $O(1)$."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Binary Trees, Binary Search Trees & Balanced Trees",
        "key_takeaways": "Master tree traversals (in-order, pre-order, post-order, level-order), BST invariant, Lowest Common Ancestor, and self-balancing AVL/Red-Black rotation proofs.",
        "topics": [
            "Tree properties: Height, depth, diameter, full vs complete vs perfect trees",
            "Traversals: Recursive vs iterative (Morris Traversal for O(1) space)",
            "Binary Search Tree operations: Insertion, deletion with in-order successor, search",
            "Lowest Common Ancestor (LCA) in Binary Trees and BSTs",
            "Balanced Trees: AVL rotation mechanics (LL, RR, LR, RL) and Red-Black properties"
        ],
        "sections": {
            "concept": """A Binary Tree is a hierarchical non-linear structure where every node has at most two children (`left`, `right`). Binary Search Trees (BST) enforce the fundamental ordering property: for any node $X$, all keys in $X$'s left subtree are strictly less than $X.val$, and all keys in $X$'s right subtree are strictly greater than $X.val$. This enables $O(h)$ search, insertion, and deletion, where $h$ is the tree height.

If elements are inserted in sorted order, an un-balanced BST degenerates into a linear linked list of height $h = n$, degrading search time to $O(n)$. Self-balancing trees (AVL Trees and Red-Black Trees) dynamically maintain logarithmic height $h = O(\\log n)$ via tree rotations (Left Rotation and Right Rotation). In-order traversal of any valid BST yields all keys in strictly ascending sorted order.""",
            "formulas": """1. **Tree Properties:**
   - In a binary tree of height $h$ (where root height $= 0$): Maximum nodes $= 2^{h+1} - 1$.
   - For $n$ nodes, minimum height $= \\lfloor \\log_2 n \\rfloor$.
2. **AVL Balance Factor:**
   $$\\text{BalanceFactor}(N) = \\text{Height}(\\text{left}) - \\text{Height}(\\text{right}) \\in \\{-1, 0, +1\\}$$
3. **Lowest Common Ancestor in BST:**
   If $\\min(p.val, q.val) \\le root.val \\le \\max(p.val, q.val)$, then $root$ is the LCA!""",
            "solved_examples": [
                {
                    "title": "Lowest Common Ancestor in a Binary Search Tree",
                    "difficulty": "Easy | Amazon, Microsoft, TCS",
                    "problem": "Given a BST and two nodes $p$ and $q$, find their Lowest Common Ancestor (LCA).",
                    "step_by_step": [
                        "Step 1: Start at the root node.",
                        "Step 2: If both $p$ and $q$ have values less than root, LCA must reside in the left subtree: recurse left.",
                        "Step 3: If both $p$ and $q$ have values greater than root, LCA must reside in the right subtree: recurse right.",
                        "Step 4: If $p$ and $q$ diverge (one is on left, one is on right, or one equals root), the current node is the split point and hence the LCA."
                    ],
                    "code_or_math": """def lowest_common_ancestor_bst(root, p, q):
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return None""",
                    "explanation": "The algorithm visits at most one node per level. In a balanced BST of height $h = \\log n$, time complexity is $O(\\log n)$ with $O(1)$ auxiliary space."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the maximum number of nodes at level $k$ of a binary tree (root at level 0)?",
                    "options": [
                        "A) $2^k$",
                        "B) $2^{k-1}$",
                        "C) $2k$",
                        "D) $k^2$"
                    ],
                    "correct_answer": "A) $2^k$",
                    "detailed_solution": "Level 0 has $2^0 = 1$ node. Level 1 has $2^1 = 2$. Level $k$ has at most $2^k$ nodes."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "How do you validate whether a given binary tree is a valid Binary Search Tree?",
                    "model_answer": "Do not simply check if `root.left.val < root.val < root.right.val` because that only checks immediate children, not entire subtrees. Instead, carry a valid range `(min_val, max_val)` through a recursive DFS: for root, range is $(-\\infty, +\\infty)$. When recurring left, range becomes `(min_val, root.val)`. When recurring right, range becomes `(root.val, max_val)`. If any node violates `min_val < node.val < max_val`, return False. This checks the tree in $O(n)$ time and $O(h)$ space.",
                    "interviewer_tip": "Mention that an in-order traversal of a valid BST must produce a strictly increasing sequence."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Heaps, Priority Queues & Greedy Algorithms",
        "key_takeaways": "Master binary heap array storage, heapify proof of O(n) construction, Top-K elements, Median from Data Stream (two heaps), and greedy exchange arguments.",
        "topics": [
            "Complete binary tree representation in contiguous arrays",
            "Min-heap and Max-heap invariants: Sift-up and sift-down mechanics",
            "Mathematical proof of O(n) bottom-up heap construction vs O(n log n) naive insertion",
            "Find Median from Data Stream using Two Heaps (Max-Heap + Min-Heap)",
            "Greedy choice property, optimal substructure, and activity selection"
        ],
        "sections": {
            "concept": """A Binary Heap is a complete binary tree satisfying the Heap Property: in a Min-Heap, every parent node is $\\le$ its children (root holds the minimum element); in a Max-Heap, every parent node is $\\ge$ its children. Because complete binary trees have no missing nodes except on the bottom row from left to right, heaps are stored without pointers in a compact contiguous array:
- Parent of node at index $i$: $\\lfloor (i - 1) / 2 \\rfloor$
- Left child of index $i$: $2i + 1$
- Right child of index $i$: $2i + 2$

Building a heap from an unordered array of $n$ elements bottom-up via `build_heap()` runs in strictly $O(n)$ time—not $O(n \\log n)$—because the majority of nodes reside near the leaves where sift-down height is tiny.""",
            "formulas": """1. **Mathematical Proof of O(n) Heap Construction:**
   Let $h = \\log_2 n$. At height $k$, there are at most $\\lceil n / 2^{k+1} \\rceil$ nodes, each requiring at most $k$ operations:
   $$T(n) = \\sum_{k=0}^{\\lfloor \\log n \\rfloor} \\frac{n}{2^{k+1}} \\times k = \\frac{n}{2} \\sum_{k=0}^\\infty \\frac{k}{2^k}$$
   Since the arithmetico-geometric series $\\sum_{k=0}^\\infty \\frac{k}{2^k} = 2$:
   $$T(n) = \\frac{n}{2} \\times 2 = O(n)$$""",
            "solved_examples": [
                {
                    "title": "Find Kth Largest Element in an Array",
                    "difficulty": "Medium | Amazon, Facebook, Google",
                    "problem": "Find the $k$-th largest element in an unsorted array of size $n$.",
                    "step_by_step": [
                        "Step 1: Maintain a Min-Heap of capacity $k$.",
                        "Step 2: Iterate through each element in the array.",
                        "Step 3: Push current element to min-heap. If heap size exceeds $k$, pop the root (the smallest of the $k+1$ items).",
                        "Step 4: After processing all $n$ items, the min-heap contains the $k$ largest items, with the $k$-th largest at the root."
                    ],
                    "code_or_math": """import heapq

def find_kth_largest(nums, k):
    min_heap = []
    for x in nums:
        heapq.heappush(min_heap, x)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]""",
                    "explanation": "Heap size never exceeds $k+1$. Pushing and popping takes $O(\\log k)$. For $n$ items, total time is $O(n \\log k)$ with $O(k)$ auxiliary space, far outperforming $O(n \\log n)$ full sorting when $k \\ll n$."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the time complexity to insert an element into a binary heap containing $n$ elements?",
                    "options": [
                        "A) $O(1)$",
                        "B) $O(\\log n)$",
                        "C) $O(n)$",
                        "D) $O(n \\log n)$"
                    ],
                    "correct_answer": "B) $O(\\log n)$",
                    "detailed_solution": "Inserting an element appends it to the end and sifts it up to the root, which requires traversing at most the tree height $h = \\log_2 n$ levels."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "How do you find the running median from a continuous stream of numbers in real time?",
                    "model_answer": "Use two heaps: a Max-Heap `small` storing the smaller half of numbers, and a Min-Heap `large` storing the larger half. Maintain the balance invariant: `len(small) == len(large)` or `len(small) == len(large) + 1`. For incoming number $x$: push to `small`, then pop max from `small` and push to `large`. If `len(large) > len(small)`, pop min from `large` and push to `small`. Finding median takes $O(1)$: if lengths are equal, median is `(small[0] + large[0]) / 2.0`; otherwise median is `small[0]`. Insertion is $O(\\log n)$.",
                    "interviewer_tip": "Clearly articulate the two heap balancing invariants."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Graph Algorithms: Traversals, Shortest Paths & MST",
        "key_takeaways": "Master Adjacency Matrix vs List, BFS/DFS, topological sort (Kahn's), Dijkstra's algorithm, Bellman-Ford negative cycle detection, and Kruskal's MST.",
        "topics": [
            "Graph representations: Adjacency Matrix (O(V^2)) vs Adjacency List (O(V + E))",
            "Breadth-First Search (BFS) and Depth-First Search (DFS) dynamics",
            "Cycle detection in directed graphs & Topological Sorting (Kahn's Algorithm)",
            "Single-source shortest paths: Dijkstra's Algorithm (O((V + E) log V)) vs Bellman-Ford",
            "Minimum Spanning Trees: Kruskal's Algorithm using Disjoint Set Union (DSU) vs Prim's"
        ],
        "sections": {
            "concept": """A Graph $G = (V, E)$ consists of vertices $V$ connected by edges $E$. In placement evaluations, choosing between an Adjacency Matrix and an Adjacency List is critical: Adjacency Matrices take $O(V^2)$ space and are ideal only for dense graphs, whereas Adjacency Lists take $O(V + E)$ space and are optimal for sparse networks.

Graph traversal forms the core of network analysis:
- **BFS (Queue):** Discovers vertices level-by-level, identifying shortest paths in unweighted graphs in $O(V + E)$.
- **DFS (Stack/Recursion):** Explores deeply along branches, fundamental for cycle detection, connected components, and topological sorting.
- **Topological Sort:** Linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge $u \\to v$, $u$ appears before $v$. Kahn's algorithm computes this using in-degrees: vertices with in-degree 0 are queued and processed iteratively.""",
            "formulas": """1. **Dijkstra's Priority Queue Time Complexity:**
   With binary min-heap: each vertex is extracted once ($V \\log V$) and each edge relaxes at most once ($E \\log V$):
   $$T(V, E) = O((V + E) \\log V)$$
2. **Bellman-Ford Invariant:**
   Relax all $E$ edges $V - 1$ times. If any edge can still be relaxed on the $V$-th pass, a negative weight cycle exists!""",
            "solved_examples": [
                {
                    "title": "Course Schedule (Topological Sort / Cycle Detection)",
                    "difficulty": "Medium | Amazon, Google, Microsoft",
                    "problem": "Given $n$ courses labelled 0 to $n-1$ and prerequisite pairs $[a, b]$ meaning you must take course $b$ before $a$, determine if it is possible to finish all courses.",
                    "step_by_step": [
                        "Step 1: Build adjacency list and compute in-degree for all $n$ nodes.",
                        "Step 2: Initialize a queue containing all nodes with `in_degree == 0`.",
                        "Step 3: While queue is not empty: pop node `u`, increment `processed_count` by 1. For each neighbor `v` of `u`, decrement `in_degree[v]`. If `in_degree[v] == 0`, push `v` to queue.",
                        "Step 4: If `processed_count == n`, all courses can be finished (no cycle). Otherwise, a cycle exists."
                    ],
                    "code_or_math": """from collections import deque

def can_finish(num_courses, prerequisites):
    adj = {i: [] for i in range(num_courses)}
    in_degree = [0] * num_courses
    for dest, src in prerequisites:
        adj[src].append(dest)
        in_degree[dest] += 1
    
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        for nbr in adj[node]:
            in_degree[nbr] -= 1
            if in_degree[nbr] == 0:
                queue.append(nbr)
    return count == num_courses""",
                    "explanation": "Every node enters the queue once and every edge is decremented once. Time complexity is $O(V + E)$ with $O(V + E)$ space."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why can Dijkstra's algorithm fail on graphs with negative edge weights?",
                    "options": [
                        "A) It causes an infinite loop",
                        "B) The greedy choice assumption fails because a finalized node's distance could be decreased later via a negative edge",
                        "C) It cannot use an adjacency list",
                        "D) It only works on trees"
                    ],
                    "correct_answer": "B) The greedy choice assumption fails because a finalized node's distance could be decreased later via a negative edge",
                    "detailed_solution": "Dijkstra assumes that extracting the minimum distance vertex locks in its optimal shortest path. Negative edges violate this monotonic property."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft",
                    "question": "What is the difference between Prim's algorithm and Kruskal's algorithm for finding Minimum Spanning Trees?",
                    "model_answer": "Both find a Minimum Spanning Tree of weight sum minimum in a connected weighted undirected graph. Prim's algorithm is vertex-centric: it grows a single connected tree outward from an arbitrary start node using a priority queue, running in $O(E \\log V)$ time (superior for dense graphs). Kruskal's algorithm is edge-centric: it sorts all $E$ edges globally ($O(E \\log E)$) and greedily adds edges that do not form cycles using Disjoint Set Union (DSU with union-by-rank and path compression, taking $O(E \\alpha(V))$). Kruskal's is simpler and faster on sparse graphs.",
                    "interviewer_tip": "Mention Disjoint Set Union (DSU) and the inverse Ackermann function $\\alpha(V)$."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Dynamic Programming Foundations & Classical Archetypes",
        "key_takeaways": "Master optimal substructure, overlapping subproblems, memoization vs tabulation, 0/1 Knapsack, Longest Common Subsequence, and 1D space optimization.",
        "topics": [
            "Prerequisites for DP: Optimal Substructure & Overlapping Subproblems",
            "Top-Down Memoization vs Bottom-Up Tabulation state transitions",
            "0/1 Knapsack Problem and 1D array space optimization",
            "Longest Common Subsequence (LCS) and Edit Distance (Levenshtein)",
            "Longest Increasing Subsequence (LIS) in O(n log n) via Patience Sorting"
        ],
        "sections": {
            "concept": """Dynamic Programming (DP) solves complex optimization problems by decomposing them into overlapping subproblems and storing subproblem results to prevent redundant re-computation. A problem qualifies for DP if it satisfies two conditions:
1. **Optimal Substructure:** The optimal solution to the overall problem incorporates optimal solutions to its constituent subproblems.
2. **Overlapping Subproblems:** The recursive solution visits the same identical subproblem states repeatedly.

There are two primary paradigms:
- **Top-Down with Memoization:** Starts from the original problem and recurses downward, caching computed results in a hash table or array.
- **Bottom-Up Tabulation:** Iteratively builds solutions starting from the smallest base cases, avoiding recursive call stack overhead and enabling space optimization (e.g., rolling array or 1D buffer reduction).""",
            "formulas": """1. **0/1 Knapsack State Recurrence:**
   Let $dp[i][w]$ be the max value using a subset of first $i$ items with weight capacity $w$:
   $$dp[i][w] = \\begin{cases} dp[i-1][w] & \\text{if } wt[i-1] > w \\\\ \\max(dp[i-1][w], \\ val[i-1] + dp[i-1][w - wt[i-1]]) & \\text{if } wt[i-1] \\le w \\end{cases}$$
2. **1D Space Optimization:**
   Iterate $w$ backwards from $W$ down to $wt[i-1]$ to ensure each item is used at most once:
   $$dp[w] = \\max(dp[w], \\ val[i-1] + dp[w - wt[i-1]])$$""",
            "solved_examples": [
                {
                    "title": "0/1 Knapsack Problem with 1D Space Optimization",
                    "difficulty": "Medium | Amazon, Flipkart, Goldman Sachs",
                    "problem": "Given weights $wt$, values $val$, and max capacity $W$, find the maximum value subset fitting in capacity $W$.",
                    "step_by_step": [
                        "Step 1: Initialize 1D array `dp = [0] * (W + 1)`.",
                        "Step 2: Iterate through each item index $i$ from 0 to $n-1$.",
                        "Step 3: Iterate capacity $w$ backwards from $W$ down to $wt[i]$. (Iterating backwards ensures values from the current item are not reused).",
                        "Step 4: Update `dp[w] = max(dp[w], val[i] + dp[w - wt[i]])`.",
                        "Step 5: Return `dp[W]`."
                    ],
                    "code_or_math": """def knapsack(weights, values, W):
    n = len(weights)
    dp = [0] * (W + 1)
    for i in range(n):
        w_curr = weights[i]
        v_curr = values[i]
        for w in range(W, w_curr - 1, -1):
            dp[w] = max(dp[w], v_curr + dp[w - w_curr])
    return dp[W]""",
                    "explanation": "Time complexity is $O(n \\times W)$ (pseudo-polynomial). Space complexity is reduced from $O(n \\times W)$ to strictly $O(W)$."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why is the 0/1 Knapsack problem classified as NP-Complete rather than strictly polynomial time?",
                    "options": [
                        "A) Because it cannot be solved with recursion",
                        "B) Because running time $O(n W)$ is polynomial in the numeric value of $W$, but exponential in the input size (number of bits $\\log W$)",
                        "C) Because it requires sorting",
                        "D) Because negative values are disallowed"
                    ],
                    "correct_answer": "B) Because running time $O(n W)$ is polynomial in the numeric value of $W$, but exponential in the input size (number of bits $\\log W$)",
                    "detailed_solution": "Algorithms whose running times depend on numeric input magnitude rather than length in bits are called pseudo-polynomial."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "How do you optimize Longest Increasing Subsequence (LIS) from O(n^2) to O(n log n)?",
                    "model_answer": "Use Patience Sorting with Binary Search. Maintain an array `tails` where `tails[i]` stores the smallest tail of all increasing subsequences of length $i+1$ found so far. For each number $x$ in the input: binary search for the first element in `tails` $\\ge x$. If found, replace it with $x$ (greedily lowering the tail value for that length). If $x$ is greater than all elements in `tails`, append $x$. The length of `tails` at the end is the length of the LIS. For $n$ elements with binary search taking $O(\\log n)$, total time is strictly $O(n \\log n)$ with $O(n)$ space.",
                    "interviewer_tip": "Emphasize that `tails` is always sorted, which validates the binary search step."
                }
            ]
        }
    },
    {
        "chapter_num": 9,
        "title": "Advanced Data Structures: Tries, DSU & Segment Trees",
        "key_takeaways": "Master Prefix Trees (Trie), Disjoint Set Union with Path Compression and Union by Rank, and Segment Trees for O(log n) range query and point updates.",
        "topics": [
            "Trie (Prefix Tree) implementation: insert, search, startsWith in O(L)",
            "Disjoint Set Union (DSU): Path compression and union-by-rank proof of O(alpha(n))",
            "Segment Tree architecture: Build in O(n), Range Query in O(log n), Update in O(log n)",
            "Fenwick Tree (Binary Indexed Tree) for range prefix sums with O(n) space"
        ],
        "sections": {
            "concept": """Advanced data structures handle specialized high-throughput requirements in enterprise architectures:
1. **Trie (Prefix Tree):** An $m$-ary tree where nodes store characters along word paths. It enables $O(L)$ word insertion, search, and prefix matching (where $L$ is word length), independent of dictionary size. Powers autocomplete engines and search suggestion bars.
2. **Disjoint Set Union (DSU / Union-Find):** Tracks elements partitioned into disjoint subsets. With two critical optimizations—Path Compression (flattening tree during `find()`) and Union by Rank/Size (attaching smaller tree under deeper root)—operations run in amortized $O(\\alpha(n))$ time, where $\\alpha$ is the extremely slow-growing inverse Ackermann function (effectively $\\le 4$ for all realistic inputs).
3. **Segment Tree:** Complete binary tree storing aggregated range metrics (sum, min, max) over array segments. Allows both arbitrary range queries and point updates in strictly $O(\\log n)$ time.""",
            "formulas": """1. **DSU Inverse Ackermann Bound:**
   $$\\text{Time per operation} = O(\\alpha(n)) \\approx O(1)$$
2. **Segment Tree Properties:**
   For array of size $n$, array-backed tree size $\\le 4n$.
   $$\\text{Build Time} = O(n), \\quad \\text{Range Query} = O(\\log n), \\quad \\text{Point Update} = O(\\log n)$$""",
            "solved_examples": [
                {
                    "title": "Trie (Prefix Tree) Implementation",
                    "difficulty": "Medium | Amazon, Google, Microsoft",
                    "problem": "Implement a Trie with insert, search, and startsWith methods.",
                    "step_by_step": [
                        "Step 1: Define `TrieNode` having a dictionary of children and a boolean flag `is_end_of_word`.",
                        "Step 2: `insert(word)`: Traverse character by character from root, creating child nodes when missing, and mark final node as `is_end_of_word = True`.",
                        "Step 3: `search(word)`: Traverse characters; if path broken return False; else return `curr.is_end_of_word`.",
                        "Step 4: `starts_with(prefix)`: Traverse characters; if path broken return False; else return True."
                    ],
                    "code_or_math": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return curr.is_end

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True""",
                    "explanation": "All operations take strictly $O(L)$ time where $L$ is the string length. Space is bounded by total characters stored across nodes."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the amortized complexity of $m$ DSU operations on $n$ elements with path compression and union by rank?",
                    "options": [
                        "A) $O(m \\log n)$",
                        "B) $O(m \\alpha(n))$",
                        "C) $O(m n)$",
                        "D) $O(m \\log^2 n)$"
                    ],
                    "correct_answer": "B) $O(m \\alpha(n))$",
                    "detailed_solution": "Robert Tarjan proved that combining union by rank and path compression achieves $O(m \\alpha(n))$ across $m$ operations."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "When would you choose a Fenwick Tree (Binary Indexed Tree) over a Segment Tree?",
                    "model_answer": "A Fenwick Tree is simpler to implement (less than 15 lines of code) and uses strictly $O(n)$ space compared to $4n$ memory in Segment Trees. It is optimal for cumulative prefix sum queries and point updates. However, Segment Trees are required when range queries involve non-invertible operations (such as Range Minimum Query or Range GCD) or when range updates require Lazy Propagation.",
                    "interviewer_tip": "Mentioning the bitwise arithmetic `x & (-x)` for Fenwick Tree index advancement shows deep familiarity."
                }
            ]
        }
    },
    {
        "chapter_num": 10,
        "title": "Solved Hard Placement DSA Problems & Interview Drills",
        "key_takeaways": "Master end-to-end solutions to top corporate interview benchmarks: Trapping Rain Water, Merge K Sorted Lists, and Word Ladder.",
        "topics": [
            "Trapping Rain Water: Two-pointer optimal O(n) solution",
            "Merge K Sorted Lists: Min-Heap optimal O(N log k) solution",
            "Word Ladder: Bidirectional BFS shortest transformation sequence",
            "Placement coding interview rubrics, communication strategies, and edge testing"
        ],
        "sections": {
            "concept": """This capstone chapter synthesizes multi-structure algorithms on flagship corporate placement problems frequently asked in final coding rounds at FAANG, Tier 1 product firms, and premium IT services (TCS Digital, Infosys Power Programmer).

In high-stakes technical interviews, arriving at the correct answer is only 50% of the evaluation rubric:
1. **Clarifying Requirements & Constraints:** Confirming input boundaries, null/empty cases, negative values, and memory limitations.
2. **Brute Force Baseline:** Articulating the naive solution and identifying computational bottlenecks.
3. **Optimal Design & Intuition:** Communicating the algorithmic trade-off clearly before touching code.
4. **Clean, Bug-Free Code:** Writing modular, well-named, production-quality code.
5. **Dry Run & Edge Testing:** Tracing through edge cases (single-element, duplicate elements, empty arrays) to prove correctness.""",
            "formulas": """1. **Trapping Rain Water Invariant:**
   $$\\text{WaterAt}(i) = \\max(0, \\min(\\text{MaxLeft}[i], \\text{MaxRight}[i]) - height[i])$$
2. **Merge K Sorted Lists Complexity:**
   $$N = \\text{total nodes across all } k \\text{ lists} \\implies \\text{Time} = O(N \\log k), \\quad \\text{Space} = O(k)$$""",
            "solved_examples": [
                {
                    "title": "Trapping Rain Water (Two Pointers)",
                    "difficulty": "Hard | Google, Amazon, Microsoft, Uber",
                    "problem": "Given $n$ non-negative integers representing an elevation map where width of each bar is 1, compute how much water it can trap after raining.",
                    "step_by_step": [
                        "Step 1: Set `left = 0`, `right = n - 1`, `left_max = 0`, `right_max = 0`, `water = 0`.",
                        "Step 2: While `left < right`: compare `height[left]` and `height[right]`.",
                        "Step 3: If `height[left] < height[right]`: if `height[left] >= left_max`, update `left_max = height[left]`; else add `left_max - height[left]` to `water`. Increment `left`.",
                        "Step 4: Else: if `height[right] >= right_max`, update `right_max = height[right]`; else add `right_max - height[right]` to `water`. Decrement `right`.",
                        "Step 5: Return `water`."
                    ],
                    "code_or_math": """def trap(height):
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water""",
                    "explanation": "Executes in strictly $O(n)$ time with $O(1)$ auxiliary memory. The two pointers maintain dynamic boundaries without needing $O(n)$ prefix arrays."
                },
                {
                    "title": "Merge K Sorted Lists (Min-Heap)",
                    "difficulty": "Hard | Amazon, Facebook, Google",
                    "problem": "Merge $k$ sorted linked lists and return it as one sorted list.",
                    "step_by_step": [
                        "Step 1: Create a Min-Heap and insert the head node of all $k$ non-empty lists.",
                        "Step 2: Maintain a dummy sentinel node and a pointer `tail`.",
                        "Step 3: While heap is not empty: pop node with minimum value and attach to `tail.next`. Advance `tail`.",
                        "Step 4: If popped node has a `.next`, push that next node into the min-heap.",
                        "Step 5: Return `dummy.next`."
                    ],
                    "code_or_math": """import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            # Tuple contains (val, index, node) to break ties without comparing ListNode objects
            heapq.heappush(heap, (node.val, i, node))
    
    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
            
    return dummy.next""",
                    "explanation": "The heap stores at most $k$ nodes at any point. Popping and pushing takes $O(\\log k)$. With $N$ total elements across all lists, running time is $O(N \\log k)$ and auxiliary space is $O(k)$."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the optimal time complexity to solve the Median of Two Sorted Arrays problem?",
                    "options": [
                        "A) $O(m + n)$",
                        "B) $O(\\log(m + n))$",
                        "C) $O(\\min(m, n))$",
                        "D) $O((m + n) \\log(m + n))$"
                    ],
                    "correct_answer": "B) $O(\\log(m + n))$",
                    "detailed_solution": "Binary searching over the partition point of the smaller array divides the combined elements into two equal halves in $O(\\log(\\min(m, n)))$ time."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "In a coding interview, you write working code that passes all sample tests. What should you do before telling the interviewer you are finished?",
                    "model_answer": "Never immediately say you are done. 1) Manually trace the code step-by-step with a concrete sample input to verify variable states. 2) Proactively test boundary edge cases: empty input, single element, all duplicates, negative numbers, and extreme values. 3) Check for memory leaks or integer overflows. 4) State the final time and auxiliary space complexity clearly. This structured diligence signals senior software engineering habits.",
                    "interviewer_tip": "Interviewers frequently wait to see if candidates catch their own bugs during manual dry runs."
                }
            ]
        }
    }
]

