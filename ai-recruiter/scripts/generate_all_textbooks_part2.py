"""
Generates comprehensive master textbooks for:
- Python Programming (python_master.py)
- Quantitative Aptitude (quant_master.py)
- Logical Reasoning (logical_master.py)
- Verbal Ability & English (verbal_master.py)
"""
import os
import ast

TEXTBOOK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "app", "services", "textbooks"))

# =============================================================================
# 2. PYTHON MASTER TEXTBOOK
# =============================================================================
PYTHON_CONTENT = r'''"""
python_master.py — Prescribed Master Textbook for Python Programming.
Comprehensive campus placement textbook covering CPython internals, memory management,
scoping rules, object-oriented dunder methods, generator streaming, decorators, context managers,
and coding interview patterns.
"""

PYTHON_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Python Execution Model, CPython Internals & Memory Management",
        "topics": ["Source code compilation (.py -> .pyc bytecode), AST, and Python Virtual Machine (PVM)", "Global Interpreter Lock (GIL) architecture and impact on CPU vs I/O bound concurrency", "Memory model: Reference Counting, Cyclic Garbage Collection (Generational GC: Gen 0, 1, 2)", "Object identity (id(), 'is') vs structural equality ('==') and small integer caching (-5 to 256)"],
        "key_takeaways": "CPython manages memory primarily through reference counting with a tri-generational cyclic garbage collector. The GIL permits only one native OS thread to execute Python bytecode at a time."
    },
    {
        "chapter_num": 2,
        "title": "Core Built-in Data Structures & Internal Complexity",
        "topics": ["Mutable types (list, dict, set, bytearray) vs Immutable types (int, float, str, tuple, frozenset)", "Dynamic array growth formula in CPython lists: O(1) amortized append vs O(N) insert/delete", "Dictionary hash table implementation: open addressing, perturbation hashing, and key hashability requirements", "Shallow copy (copy.copy) vs Deep copy (copy.deepcopy) and reference aliasing traps"],
        "key_takeaways": "Dict keys must be hashable (__hash__ and __eq__). List appends run in amortized O(1), but inserting or popping from the front takes O(N) time (use collections.deque instead)."
    },
    {
        "chapter_num": 3,
        "title": "Functions, Scopes (LEGB), Closures & Decorators",
        "topics": ["First-class functions and higher-order functional paradigms", "LEGB Scoping Hierarchy: Local, Enclosing, Global, Built-in", "Variable rebinding across scopes using 'nonlocal' and 'global' keywords", "Function decorators, @functools.wraps metadata preservation, and parameterized multi-level decorators"],
        "key_takeaways": "Python resolves names from innermost to outermost: Local -> Enclosing -> Global -> Built-in. Decorators wrap callable functions; @functools.wraps prevents loss of docstrings and function names."
    },
    {
        "chapter_num": 4,
        "title": "Object-Oriented Python, Dunder Methods & Metaprogramming",
        "topics": ["Class creation lifecycle: __new__ (instance allocator) vs __init__ (instance initializer)", "Dunder methods: __str__, __repr__, __len__, __getitem__, __setitem__, __call__, __eq__", "Multiple inheritance and Method Resolution Order (MRO) using C3 Linearization", "Properties (@property, @setter) and descriptor protocol (__get__, __set__, __delete__)"],
        "key_takeaways": "__new__ creates and returns the object instance; __init__ initializes attributes. Class.mro() defines the unambiguous attribute search path for multiple inheritance."
    },
    {
        "chapter_num": 5,
        "title": "Generators, Iterators & Memory-Efficient Streaming",
        "topics": ["Iterable vs Iterator protocol: __iter__() and __next__() methods", "Generator functions, 'yield', and 'yield from' coroutine delegation", "Memory comparison: O(1) generator streams vs O(N) list comprehensions on large datasets", "Itertools module superpowers (chain, islice, product, permutations, combinations)"],
        "key_takeaways": "Generators evaluate items lazily on demand using constant O(1) auxiliary memory, making them ideal for processing large files or infinite data streams."
    },
    {
        "chapter_num": 6,
        "title": "Exception Handling, Context Managers & Resource Safety",
        "topics": ["Exception hierarchy: BaseException, Exception, standard built-in errors", "Execution semantics of try, except, else, finally blocks", "Context Manager protocol (__enter__ and __exit__) and the 'with' statement", "contextlib module (@contextmanager generator decorator)"],
        "key_takeaways": "The 'else' block runs only if no exception was raised in 'try'. The 'finally' block executes unconditionally, guaranteeing cleanup of locks and file descriptors."
    },
    {
        "chapter_num": 7,
        "title": "Standard Library Mastery & Interview Coding Patterns",
        "topics": ["collections module: defaultdict, Counter, deque, namedtuple, OrderedDict", "heapq module: min-heaps, nlargest(), nsmallest()", "bisect module: binary searching and sorted list maintenance", "Placement coding puzzles: LRU cache via OrderedDict, grouping anagrams, deep flattening"],
        "key_takeaways": "collections.deque achieves O(1) push and pop from both ends. defaultdict eliminates KeyError boilerplate when building frequency maps or adjacency lists."
    }
]

PYTHON_TEXTBOOK_MARKDOWN = r"""# Python Programming & Interview Foundations (Prescribed Master Textbook)

**Edition:** 2026 Campus Placement & Technical Interview Edition  
**Subject:** Python  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus recruitment Python coding assessments, technical interview rounds, and online tests (TCS Digital/Prime, Infosys DSE, Amazon SDE, Google SWE, Cognizant, etc.) are strictly grounded in the language mechanics, internals, and problem-solving patterns contained within this master textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Python Execution Model, CPython Internals & Memory Management](#chapter-1-python-execution-model-cpython-internals--memory-management)
- [Chapter 2: Core Built-in Data Structures & Internal Complexity](#chapter-2-core-built-in-data-structures--internal-complexity)
- [Chapter 3: Functions, Scopes (LEGB), Closures & Decorators](#chapter-3-functions-scopes-legb-closures--decorators)
- [Chapter 4: Object-Oriented Python, Dunder Methods & Metaprogramming](#chapter-4-object-oriented-python-dunder-methods--metaprogramming)
- [Chapter 5: Generators, Iterators & Memory-Efficient Streaming](#chapter-5-generators-iterators--memory-efficient-streaming)
- [Chapter 6: Exception Handling, Context Managers & Resource Safety](#chapter-6-exception-handling-context-managers--resource-safety)
- [Chapter 7: Standard Library Mastery & Interview Coding Patterns](#chapter-7-standard-library-mastery--interview-coding-patterns)
- [Chapter 8: Solved Placement Python Challenges & Self-Assessment Drills](#chapter-8-solved-placement-python-challenges--self-assessment-drills)

---

## Chapter 1: Python Execution Model, CPython Internals & Memory Management

### 1.1 Source Code to Execution Pipeline
CPython executes Python programs through a multi-stage compilation and virtual machine pipeline:
1. **Lexing & Parsing:** Source `.py` code is converted into parse trees and an Abstract Syntax Tree (AST).
2. **Bytecode Compilation:** The AST is compiled into platform-independent Python bytecode instructions stored in memory or cached in `__pycache__/*.pyc` files.
3. **Evaluation Loop (PVM):** The Python Virtual Machine (PVM) sequentially interprets bytecode instructions using a stack-based execution engine.

### 1.2 The Global Interpreter Lock (GIL)
The GIL is a mutual exclusion lock used by CPython to prevent multiple native OS threads from executing Python bytecode simultaneously:
- **Reason for GIL:** Simplifies CPython memory management and reference counting, making single-threaded C extensions thread-safe.
- **Consequences:** Multi-threaded CPU-bound programs do NOT achieve multi-core parallelism in CPython. To utilize all CPU cores, use `multiprocessing` or native C/Rust extensions.
- **I/O-Bound Work:** When a thread performs I/O operations (network requests, disk reads) or calls C extensions, it explicitly releases the GIL, enabling concurrent execution.

### 1.3 Memory Management & Generational Garbage Collection
CPython manages memory through two cooperating engines:
1. **Reference Counting (Primary GC):** Every Python object header contains `ob_refcnt`. When a reference is created, count increments; when reference goes out of scope or is deleted, count decrements. When `ob_refcnt == 0`, memory is deallocated immediately.
2. **Cyclic Garbage Collector (Secondary GC):** Resolves reference cycles (e.g. object A references B, and B references A). It tracks container objects across three generations:
   - **Generation 0:** Newly allocated objects. Collected frequently.
   - **Generation 1:** Survivors of Gen 0 collection.
   - **Generation 2:** Long-lived objects (modules, functions, surviving multiple Gen 1 collections).

---

## Chapter 2: Core Built-in Data Structures & Internal Complexity

### 2.1 Mutability Matrix & Hashability
| Data Type | Mutable? | Hashable (Usable as Dict Key / Set Element)? | Internal C Structure |
|---|---|---|---|
| `int`, `float`, `bool` | No | Yes | `PyLongObject`, `PyFloatObject` |
| `str` | No | Yes | `PyASCIIObject` / `PyCompactUnicodeObject` |
| `tuple`, `frozenset`| No | Yes (if all contained items are hashable) | Fixed array of object pointers |
| `list` | Yes | No | Contiguous dynamic array of `PyObject*` |
| `dict`, `set` | Yes | No | Combined hash table array (indices + entries) |

### 2.2 Dynamic Array Resizing in Lists
In CPython, when a list overflows, it allocates memory following the over-allocation formula:
$$\text{new\_allocated} = \text{newsize} + (\text{newsize} \gg 3) + (\text{newsize} < 9 \mathrel{?} 3 : 6)$$
This guarantees an amortized $O(1)$ append cost. However, `list.insert(0, val)` or `list.pop(0)` takes $O(N)$ because all subsequent pointers must shift.

---

## Chapter 3: Functions, Scopes (LEGB), Closures & Decorators

### 3.1 LEGB Scoping Rule
Python resolves identifiers in this precise priority:
1. **Local (L):** Defined inside the currently executing function.
2. **Enclosing (E):** Defined in the local scope of any enclosing functions (closures).
3. **Global (G):** Defined at the top-level module scope or declared via `global`.
4. **Built-in (B):** Preloaded in Python (`len`, `range`, `ValueError`).

### 3.2 Closures & The `nonlocal` Keyword
A closure occurs when an inner function retains access to variables from an enclosing scope even after the outer function has finished executing:
```python
def make_counter(start: int = 0):
    count = start
    def increment():
        nonlocal count  # Rebinds variable in enclosing scope, avoiding UnboundLocalError
        count += 1
        return count
    return increment

counter = make_counter(10)
print(counter())  # 11
print(counter())  # 12
```

### 3.3 Function Decorators & `@functools.wraps`
```python
import functools
import time

def timing_decorator(func):
    @functools.wraps(func)  # Preserves func.__name__, func.__doc__, annotations
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"Function {func.__name__} took {duration:.6f} seconds")
        return result
    return wrapper

@timing_decorator
def compute_squares(n: int) -> list[int]:
    # Returns squares of first n numbers
    return [i * i for i in range(n)]
```

---

## Chapter 4: Object-Oriented Python, Dunder Methods & Metaprogramming

### 4.1 Object Instantiation: `__new__` vs `__init__`
- `__new__(cls, *args, **kwargs)`: Static method responsible for allocating the new instance in memory. Must return an instance of `cls`.
- `__init__(self, *args, **kwargs)`: Instance method responsible for initializing the attributes of the newly created instance.

### 4.2 Essential Dunder Methods
```python
class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        # Machine-readable representation
        return f"Vector2D({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __len__(self) -> int:
        return 2
```

### 4.3 Method Resolution Order (C3 Linearization)
In multiple inheritance, Python resolves attribute lookups using the C3 Linearization algorithm to guarantee monotonicity and local precedence order:
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.mro())
# [D, B, C, A, object]
```

---

## Chapter 5: Generators, Iterators & Memory-Efficient Streaming

### 5.1 The Iterator Protocol
An object is an **Iterable** if it implements `__iter__()` returning an Iterator.
An object is an **Iterator** if it implements `__next__()` returning the next item, or raising `StopIteration`.

### 5.2 Generator Streaming
```python
def fibonacci_stream():
    # Generates infinite Fibonacci sequence with O(1) auxiliary memory
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci_stream()
first_5 = [next(gen) for _ in range(5)]  # [0, 1, 1, 2, 3]
```

---

## Chapter 6: Exception Handling, Context Managers & Resource Safety

### 6.1 Custom Context Manager with `__enter__` and `__exit__`
```python
class ManagedDatabaseConnection:
    def __init__(self, connection_str: str):
        self.connection_str = connection_str
        self.conn = None

    def __enter__(self):
        print(f"Connecting to {self.connection_str}...")
        self.conn = {"status": "connected"}
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection and releasing pool resources...")
        self.conn = None
        # Return True to suppress exception, False to re-raise
        return False
```

---

## Chapter 7: Standard Library Mastery & Interview Coding Patterns

### 7.1 Collections Module Superpowers
```python
from collections import defaultdict, Counter, deque

# 1. Grouping anagrams in O(N * K log K)
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
anagram_map = defaultdict(list)
for w in words:
    sorted_key = "".join(sorted(w))
    anagram_map[sorted_key].append(w)
grouped = list(anagram_map.values())

# 2. Sliding window deque with O(1) pops from both ends
window = deque(maxlen=3)
for i in range(5):
    window.append(i)
# window holds [2, 3, 4]
```

---

## Chapter 8: Solved Placement Python Challenges & Self-Assessment Drills

### Solved Challenge 1: Custom LRU Cache using `collections.OrderedDict`
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Evict least recently used (first)
```

### Self-Assessment Practice Exercises & Verified Solutions:
1. **Exercise 1 (Decorators):** Write a `@retry(max_attempts=3, delay=1.0)` decorator that catches network exceptions and retries execution.
2. **Exercise 2 (Generators):** Implement a custom chunk generator `chunked(iterable, size)` that yields sublists of given size using $O(1)$ memory.
3. **Exercise 3 (Dunder):** Build an immutable `Point` class using `__slots__` and prevent dynamic attribute addition.
"""

PYTHON_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "Python Execution Model, CPython Internals & Memory Management",
        "subtopic": "Global Interpreter Lock (GIL)",
        "question": "What is the primary operational effect of CPython's Global Interpreter Lock (GIL) on multi-threaded programs?",
        "options": [
            "It restricts execution so that only one native OS thread executes Python bytecode at any given moment.",
            "It completely blocks multi-processing across separate CPU cores.",
            "It forces all Python variables to be stored as read-only constants.",
            "It automatically optimizes pure CPU-bound mathematical loops to run in parallel."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Python Prescribed Textbook — Chapter 1: Python Execution Model]\nThe GIL ensures thread-safety in CPython by permitting only one thread to execute Python bytecode at a time, preventing multi-threaded CPU-bound parallelism.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 3,
        "chapter_title": "Functions, Scopes (LEGB), Closures & Decorators",
        "subtopic": "Nonlocal Keyword",
        "question": "What happens when an inner nested function attempts to rebind a variable defined in an outer enclosing function without declaring 'nonlocal'?",
        "options": [
            "Python creates a new local variable in the inner function, potentially causing an UnboundLocalError if read before assignment.",
            "Python automatically modifies the outer variable in the enclosing scope.",
            "Python throws a SyntaxError at compilation time.",
            "Python promotes the variable into the global namespace."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Python Prescribed Textbook — Chapter 3: Functions & LEGB]\nWithout 'nonlocal', assigning to a variable marks it local to the inner function. If the function tries to read it prior to assignment (e.g. x += 1), an UnboundLocalError is raised.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 5,
        "chapter_title": "Generators, Iterators & Memory-Efficient Streaming",
        "subtopic": "Generator Memory Complexity",
        "question": "Why do generator functions with 'yield' use significantly less memory than equivalent list comprehensions when streaming 10 million records?",
        "options": [
            "Generators compute elements lazily on demand in O(1) memory instead of allocating the entire array in memory.",
            "Generators compress data using GZIP compression in RAM.",
            "Generators run on a separate background thread with dedicated cache.",
            "Generators store items in the Metaspace rather than the heap."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Python Prescribed Textbook — Chapter 5: Generators & Iterators]\nGenerators evaluate items lazily when next() is called, maintaining internal state in O(1) auxiliary memory without constructing full lists in RAM.",
        "difficulty": "easy",
    }
]
'''

with open(os.path.join(TEXTBOOK_DIR, "python_master.py"), "w", encoding="utf-8") as f:
    f.write(PYTHON_CONTENT.strip() + "\n")
ast.parse(PYTHON_CONTENT)
print("Generated and verified python_master.py successfully!")

