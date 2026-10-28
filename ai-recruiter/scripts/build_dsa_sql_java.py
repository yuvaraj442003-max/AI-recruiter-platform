"""
build_dsa_sql_java.py - Generates exhaustive chapter-by-chapter curriculum for:
1. Data Structures & Algorithms (10 Chapters)
2. SQL & Relational Databases (8 Chapters)
3. Core Java Programming & OOPs (10 Chapters)
"""

def generate_dsa_chapters():
    chapters = [
        {
            "chapter_num": 1,
            "title": "Asymptotic Analysis, Complexity Classes & Recurrence Relations",
            "key_takeaways": "Master Big-O, Big-Omega, Big-Theta, recursion tree proofs, and the Master Theorem across all cases to evaluate any placement algorithm.",
            "topics": [
                "Formal definitions of Big-O, Big-Omega, Big-Theta",
                "Master Theorem for Divide-and-Conquer recurrences: T(n) = a*T(n/b) + f(n)",
                "Recursion tree method and substitution method",
                "Space complexity: Auxiliary space vs call stack frame memory",
                "Complexity hierarchy: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!)"
            ],
            "sections": {
                "concept": """Asymptotic analysis is the mathematical cornerstone of computer science and technical campus interviews. Rather than measuring wall-clock time in seconds (which varies drastically based on CPU hardware, compiler optimizations, and background processes), asymptotic analysis evaluates how algorithm execution time and memory consumption scale as the input size $n$ approaches infinity.

In high-stakes corporate hiring (Google, Amazon, Microsoft, Flipkart), candidates must immediately state both the time and auxiliary space complexities of their solutions. Algorithms are categorized into complexity classes:
- **Constant Time $O(1)$:** Array index access, hash map lookup (average), stack push/pop.
- **Logarithmic Time $O(\log n)$:** Binary search, balanced BST search, Euclidean GCD.
- **Linear Time $O(n)$:** Single-pass array traversal, counting sort, Kadane's algorithm.
- **Linearithmic Time $O(n \log n)$:** Merge sort, heap sort, quick sort (average).
- **Quadratic Time $O(n^2)$:** Bubble sort, nested brute-force pair comparisons.
- **Exponential Time $O(2^n)$:** Recursive Fibonacci, power set generation, naive subset sum.
- **Factorial Time $O(n!)$:** Traveling Salesperson Problem (TSP) via brute-force permutations.""",
                "formulas": """1. **Big-O (Asymptotic Upper Bound):**
   $$f(n) = O(g(n)) \iff \exists\ c > 0, n_0 \ge 0 \text{ such that } 0 \le f(n) \le c \cdot g(n) \quad \forall n \ge n_0$$
2. **Big-Omega (Asymptotic Lower Bound):**
   $$f(n) = \Omega(g(n)) \iff \exists\ c > 0, n_0 \ge 0 \text{ such that } 0 \le c \cdot g(n) \le f(n) \quad \forall n \ge n_0$$
3. **Big-Theta (Asymptotic Tight Bound):**
   $$f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \text{ and } f(n) = \Omega(g(n))$$
4. **Master Theorem for Recurrences:**
   For $T(n) = a \cdot T(n/b) + f(n)$ where $a \ge 1, b > 1$:
   - **Case 1:** If $f(n) = O(n^{\log_b a - \epsilon})$ for $\epsilon > 0 \implies T(n) = \Theta(n^{\log_b a})$
   - **Case 2:** If $f(n) = \Theta(n^{\log_b a} \cdot \log^k n)$ for $k \ge 0 \implies T(n) = \Theta(n^{\log_b a} \cdot \log^{k+1} n)$
   - **Case 3:** If $f(n) = \Omega(n^{\log_b a + \epsilon})$ for $\epsilon > 0$ and $a \cdot f(n/b) \le c \cdot f(n)$ for $c < 1 \implies T(n) = \Theta(f(n))$""",
                "solved_examples": [
                    {
                        "title": "Solving Merge Sort Recurrence Relation",
                        "difficulty": "Medium | Amazon, Microsoft, TCS Digital",
                        "problem": "Derive the tight asymptotic time complexity for Merge Sort having recurrence $T(n) = 2T(n/2) + \Theta(n)$ with base case $T(1) = \Theta(1)$.",
                        "step_by_step": [
                            "Step 1: Identify Master Theorem parameters: $a = 2$ (two recursive subproblems), $b = 2$ (input halved each stage), and $f(n) = \Theta(n)$ (combining sorted subarrays).",
                            "Step 2: Compute the critical exponent boundary $n^{\log_b a} = n^{\log_2 2} = n^1 = n$.",
                            "Step 3: Compare $f(n) = \Theta(n)$ with $n^{\log_b a} = n$. Notice they are equal with $k = 0$, satisfying Master Theorem Case 2.",
                            "Step 4: Apply Case 2 formula: $T(n) = \Theta(n^{\log_b a} \cdot \log^{k+1} n) = \Theta(n^1 \cdot \log^{0+1} n) = \Theta(n \log n)$."
                        ],
                        "code_or_math": """# Merge Sort Implementation with strictly O(n log n) time and O(n) space
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result""",
                        "explanation": "At each level of the recursion tree, the total work performed during the merge step across all nodes is exactly $c \cdot n$. Since the tree depth is $\\log_2 n$, the overall running time is $c \\cdot n \\cdot \\log_2 n = \\Theta(n \\log n)$. Auxiliary space is $O(n)$ to hold temporary merged subarrays."
                    },
                    {
                        "title": "Binary Search Recurrence & Substitution Verification",
                        "difficulty": "Easy | Google, Infosys, Cognizant",
                        "problem": "Solve $T(n) = T(n/2) + O(1)$ using both Master Theorem and the iterative unrolling method.",
                        "step_by_step": [
                            "Step 1: Master Theorem parameters: $a = 1, b = 2, f(n) = O(1) = \Theta(n^0)$.",
                            "Step 2: Compute $n^{\log_b a} = n^{\log_2 1} = n^0 = 1$.",
                            "Step 3: Since $f(n) = \Theta(n^{\log_b a} \cdot \log^0 n)$, Master Theorem Case 2 applies with $k = 0$.",
                            "Step 4: Result: $T(n) = \Theta(n^0 \cdot \log^1 n) = \Theta(\log n)$."
                        ],
                        "code_or_math": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2  # Prevents integer overflow in languages like C++/Java
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
                        "explanation": "Binary search reduces search space by half in each iteration in $O(1)$ operations. The search terminates when search space size reaches 1 ($n / 2^k = 1 \implies k = \log_2 n$). Hence time complexity is $O(\log n)$ and auxiliary space is $O(1)$."
                    }
                ],
                "practice_questions": [
                    {
                        "question": "What is the time complexity of the recurrence relation $T(n) = 4T(n/2) + n^2$?",
                        "options": [
                            "A) $\Theta(n^2)$",
                            "B) $\Theta(n^2 \log n)$",
                            "C) $\Theta(n^3)$",
                            "D) $\Theta(n \log n)$"
                        ],
                        "correct_answer": "B) $\Theta(n^2 \log n)$",
                        "detailed_solution": "Here $a = 4, b = 2 \implies n^{\log_2 4} = n^2$. Since $f(n) = n^2 = \Theta(n^{\log_b a})$, Master Theorem Case 2 applies ($k = 0$). Thus $T(n) = \Theta(n^2 \log n)$."
                    },
                    {
                        "question": "Which of the following functions grows asymptotically the slowest as $n \to \infty$?",
                        "options": [
                            "A) $2^{\sqrt{\log n}}$",
                            "B) $n^{\log (\log n)}$",
                            "C) $(\log n)^{\log n}$",
                            "D) $\sqrt{n}$"
                        ],
                        "correct_answer": "A) $2^{\sqrt{\log n}}$",
                        "detailed_solution": "Taking logarithms of both: $\log(2^{\sqrt{\log n}}) = \sqrt{\log n}$, whereas $\log(\sqrt{n}) = 0.5 \log n$. Since $\sqrt{\log n} \ll \log n$, option A grows substantially slower than all others."
                    },
                    {
                        "question": "What is the auxiliary space complexity of a recursive algorithm with depth $d$ where each frame uses $O(1)$ local variables?",
                        "options": [
                            "A) $O(1)$",
                            "B) $O(d)$",
                            "C) $O(2^d)$",
                            "D) $O(d^2)$"
                        ],
                        "correct_answer": "B) $O(d)$",
                        "detailed_solution": "The call stack retains $d$ active stack frames simultaneously. With $O(1)$ memory per frame, total stack memory consumed is $O(d)$."
                    }
                ],
                "interview_questions": [
                    {
                        "company": "Google",
                        "question": "Why does Python's `sort()` (Timsort) run in $O(n)$ in the best case while Merge Sort is always $\Theta(n \log n)$?",
                        "model_answer": "Standard Merge Sort unconditionally splits the array down to single elements and merges them, requiring $\log n$ levels of $O(n)$ work even on already sorted data. Timsort detects pre-existing sorted contiguous subsequences (called natural runs). If the input is fully sorted, Timsort traverses the array once to identify a single run of length $n$ without splitting or merging, executing in strictly $O(n)$ time.",
                        "interviewer_tip": "Always mention that Timsort is a hybrid stable sorting algorithm combining Merge Sort and Insertion Sort with $O(n)$ best, $O(n \log n)$ average and worst case."
                    },
                    {
                        "company": "Amazon",
                        "question": "What is the difference between Auxiliary Space and Space Complexity? Can an algorithm have $O(n)$ space complexity but $O(1)$ auxiliary space?",
                        "model_answer": "Yes. Space Complexity refers to the total memory used by an algorithm, including both the input data and any extra memory allocated during execution. Auxiliary Space refers exclusively to the extra or temporary workspace allocated beyond the input. For example, an algorithm that finds the maximum element in an array of size $n$ by inspecting elements in-place has $O(n)$ total space complexity (to store the $n$ inputs) but strictly $O(1)$ auxiliary space.",
                        "interviewer_tip": "Interviewers frequently probe whether you allocate new data structures or modify inputs in-place. Always clarify if input modification is allowed."
                    },
                    {
                        "company": "Microsoft",
                        "question": "How do you solve a recurrence relation when Master Theorem fails, such as $T(n) = 2T(n/2) + n \log n$?",
                        "model_answer": "When Master Theorem fails (or for extended cases where $f(n)$ contains polylogarithmic factors), we use the Recursion Tree Method. For $T(n) = 2T(n/2) + n \log n$: at depth $i$, there are $2^i$ subproblems each of size $n/2^i$. The work at depth $i$ is $2^i \cdot (n/2^i) \log(n/2^i) = n (\log n - i)$. Summing across all levels $i = 0$ to $\log_2 n$: $\sum_{i=0}^{\log n} n(\log n - i) = n \sum_{j=0}^{\log n} j = n \cdot \frac{(\log n)^2}{2} = \Theta(n \log^2 n)$.",
                        "interviewer_tip": "Demonstrating the summation of recursion tree levels displays profound mathematical fluency that immediately distinguishes top candidates."
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
                "concept": """Arrays provide contiguous physical memory storage, granting $O(1)$ random index access via base address arithmetic: $\\text{Address}(arr[i]) = \\text{Base} + i \\times \\text{SizeOfElement}$. Dynamic arrays (such as C++ `std::vector`, Java `ArrayList`, Python `list`) automatically resize when capacity is reached, doubling the buffer size to achieve amortized $O(1)$ append time.

Two Pointers and Sliding Window are fundamental algorithmic archetypes that reduce brute-force $O(n^2)$ nested search spaces down to optimal $O(n)$ single-pass execution:
1. **Opposite-Directional Two Pointers:** Pointers initialize at array boundaries (`left = 0`, `right = n - 1`) and converge toward each other based on monotonic conditions (e.g., sorted array target search).
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
                            "C) $O(n \log n)$ time, $O(1)$ space",
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
                        "model_answer": "The maximum stock profit problem ($\max(prices[j] - prices[i])$ for $j > i$) can be transformed into the maximum subarray sum problem by taking differences between consecutive days: $\Delta[k] = prices[k] - prices[k-1]$. The sum of differences $\sum_{k=i+1}^j \Delta[k] = prices[j] - prices[i]$ telescopes. Finding the maximum contiguous subarray sum of $\Delta$ using Kadane's algorithm yields the maximum profit in $O(n)$ time and $O(1)$ space.",
                        "interviewer_tip": "Mentioning the telescoping sum equivalence showcases deep mathematical maturity."
                    }
                ]
            }
        }
    ]
    return chapters

print("DSA generator logic ready.")

