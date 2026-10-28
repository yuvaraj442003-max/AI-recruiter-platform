"""
generate_curriculum_modules.py - Comprehensive generators for:
1. Python Programming (8 chapters)
2. JavaScript & TypeScript (8 chapters)
3. Operating Systems (8 chapters)
4. Computer Networks (8 chapters)
5. DBMS & System Design (8 chapters)
6. Quantitative Aptitude (8 chapters)
7. Logical Reasoning (8 chapters)
8. Verbal Ability (8 chapters)
9. Data Engineering (8 chapters)
10. AI & Machine Learning (8 chapters)
"""
import sys
from pathlib import Path

CURRICULUM_DIR = Path(__file__).resolve().parent.parent / "backend" / "app" / "services" / "comprehensive_curriculum"
CURRICULUM_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. PYTHON CURRICULUM
# -------------------------------------------------------------
def build_python_module():
    content = '''"""
curriculum_python.py - 8 Comprehensive Chapters for Python Programming & Placement.
"""
from typing import List, Dict, Any

PYTHON_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Python Core Semantics, Dynamic Typing & Memory Model",
        "key_takeaways": "Master Python's object model, mutability, references, id(), LEGB scoping, and CPython reference counting.",
        "topics": [
            "Everything is an object: PyObject, type pointers, reference counts",
            "Mutable (list, dict, set) vs Immutable (int, str, tuple, frozenset) data types",
            "Variable assignment as name-binding, shallow vs deep copying",
            "LEGB Scope Resolution (Local, Enclosing, Global, Built-in)",
            "Memory management: Reference counting and cyclic garbage collector"
        ],
        "sections": {
            "concept": """In Python, 'everything is an object'. Variables do not contain data values directly; rather, variables are symbolic names (pointers) bound to `PyObject` structures allocated on the heap. Every `PyObject` contains at least a type pointer (`ob_type`) and an integer reference count (`ob_refcnt`).

Mutability defines whether an object's state can change after allocation:
- **Immutable Types:** `int`, `float`, `str`, `tuple`, `bytes`, `frozenset`. Any modifying operation allocates a brand new object on the heap.
- **Mutable Types:** `list`, `dict`, `set`, `bytearray`. Elements can be inserted, removed, or updated in-place without altering the object's identity (`id()`).

Python resolves identifier names using the strict **LEGB Rule**: Local scope -> Enclosing functions (closures) -> Global module scope -> Built-in namespace. CPython reclaims memory primarily via deterministic reference counting, supplemented by a generational cyclic garbage collector for detecting cyclic reference graphs.""",
            "formulas": """1. **LEGB Rule Resolution:**
   $$\\\\text{Local} \\\\to \\\\text{Enclosing} \\\\to \\\\text{Global} \\\\to \\\\text{Built-in}$$
2. **Copy Semantics:**
   - Assignment (`b = a`): Copies object reference only (`id(a) == id(b)`).
   - Shallow Copy (`b = copy.copy(a)`): Creates new outer container, copies references to nested items.
   - Deep Copy (`b = copy.deepcopy(a)`): Recursively clones all nested objects.""",
            "solved_examples": [
                {
                    "title": "Default Mutable Arguments Trap in Python",
                    "difficulty": "Easy | Google, Amazon, TCS",
                    "problem": "Explain why `def append_to(element, target=[]): target.append(element); return target` exhibits unexpected behavior, and provide the correct idiomatic implementation.",
                    "step_by_step": [
                        "Step 1: In Python, default argument expressions are evaluated once at function definition time, NOT at invocation time.",
                        "Step 2: A single list instance is created and shared across all subsequent invocations.",
                        "Step 3: Fix: Use `None` as sentinel default and assign a fresh list inside function body."
                    ],
                    "code_or_math": """# Correct Idiomatic Implementation
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

# Verification:
print(append_to(1)) # [1]
print(append_to(2)) # [2] (Independent fresh list)""",
                    "explanation": "Using None as default sentinel ensures that a fresh list is instantiated on every call where the argument is omitted."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the output of `a = [1, 2]; b = a; a.append(3); print(len(b))`?",
                    "options": ["A) 2", "B) 3", "C) Throws error", "D) None"],
                    "correct_answer": "B) 3",
                    "detailed_solution": "b and a reference the identical physical list in memory; mutating through a updates b."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "How does Python handle memory management and avoid memory leaks from circular references?",
                    "model_answer": "CPython uses Reference Counting as its primary memory management mechanism. When refcount hits 0, the object is immediately deallocated. To solve circular references (e.g., Object A references B and B references A, where refcount never hits 0), CPython runs a cyclic Garbage Collector based on 3 generations. It isolates container objects, tracks double-linked pointer chains, decrements internal trial counts, and reclaims unreachable reference islands.",
                    "interviewer_tip": "Emphasize reference counting + generational cyclic collector."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Advanced Data Structures: Lists, Tuples, Dictionaries & Sets",
        "key_takeaways": "Master Python list over-allocation, dict hash table open addressing (compact dicts), and set operations in O(1).",
        "topics": [
            "List implementation: Contiguous array of pointers and over-allocation strategy",
            "Tuples: Immutability, hashability, and memory efficiency",
            "Dictionary architecture: Compact dicts, hash tables with open addressing and perturbation",
            "Set theory in Python: Hash sets, union, intersection, difference in O(min(len(s), len(t)))",
            "List, Dict, and Set Comprehensions performance advantages"
        ],
        "sections": {
            "concept": """Python's built-in collections are highly engineered C data structures:
- **List:** Stored as a contiguous array of 8-byte object pointers. When capacity is exceeded, CPython uses an over-allocation growth pattern ($0, 4, 8, 16, 24, 32, 40, 52 \\dots$) to ensure amortized $O(1)$ appends.
- **Dictionary (Python 3.6+ Compact Dict):** Uses two arrays: a sparse indices table and a dense array storing `[hash, key_ptr, val_ptr]`. This guarantees insertion order while reducing memory consumption by 30-40%. Collisions are resolved using open addressing with quadratic pseudo-random perturbation.
- **Set:** Implemented as a hash table with dummy values, granting average $O(1)$ membership lookup (`x in my_set`).""",
            "formulas": """1. **List Resizing Formula (CPython):**
   $$\\\\text{new\\_allocated} = \\\\text{newsize} + (\\\\text{newsize} \\\\gg 3) + (3 \\\\text{ if newsize } < 9 \\\\text{ else } 6)$$
2. **Dict Hash Lookup:**
   $$\\\\text{index} = \\\\text{hash(key)} \\\\ \\\\& \\\\ (\\\\text{size} - 1)$$""",
            "solved_examples": [
                {
                    "title": "Group Anagrams using Hash Map (Optimal O(N * K))",
                    "difficulty": "Medium | Amazon, Google, Uber",
                    "problem": "Given an array of strings, group anagrams together.",
                    "step_by_step": [
                        "Step 1: Create a default dict mapping tuple keys to lists.",
                        "Step 2: For each word, create a 26-element character count frequency tuple.",
                        "Step 3: Append word to hash map under its character count tuple key."
                    ],
                    "code_or_math": """from collections import defaultdict

def group_anagrams(strs):
    ans = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        ans[tuple(count)].append(s)
    return list(ans.values())""",
                    "explanation": "Character frequency tuple serves as a hashable key in $O(K)$ time per word. For $N$ words of length $K$, running time is strictly $O(N \\\\times K)$."
                }
            ],
            "practice_questions": [
                {
                    "question": "Can a list be used as a key in a Python dictionary?",
                    "options": [
                        "A) Yes",
                        "B) No, because lists are mutable and unhashable",
                        "C) Only if all elements are integers",
                        "D) Yes, if converted using id()"
                    ],
                    "correct_answer": "B) No, because lists are mutable and unhashable",
                    "detailed_solution": "Dictionary keys must implement __hash__() and remain immutable; lists raise TypeError: unhashable type: 'list'."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "How do Python dictionaries preserve insertion order since Python 3.7?",
                    "model_answer": "Compact dicts separate hash indices from entries. The entries array stores key-value pairs in the exact sequential order they are added. A separate sparse hash table stores indices into this entries array. Iterating the dictionary simply iterates the contiguous entries array, preserving insertion order naturally.",
                    "interviewer_tip": "Cite compact dictionary architecture introduced in PyPy and adopted in CPython 3.6/3.7."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Functions, Scopes, Closures & Decorators",
        "key_takeaways": "Master *args, **kwargs, first-class functions, closures (__closure__), and custom parameterized decorators with functools.wraps.",
        "topics": [
            "First-class functions: Passing, returning, and assigning functions",
            "Variable positional (*args) and keyword (**kwargs) argument packing",
            "Closures: Cell objects, lexical binding, and state preservation",
            "Function Decorators: Pre/post execution interception",
            "Preserving metadata using @functools.wraps"
        ],
        "sections": {
            "concept": """In Python, functions are first-class citizens: they can be assigned to variables, passed as arguments, and returned from other functions.

**Closures:**
When an inner nested function references variables from its enclosing scope, Python constructs a closure. Even after the outer function finishes execution and returns, the inner function retains access to these enclosed variables via `__closure__` cell objects on the heap.

**Decorators:**
A decorator is a callable that accepts a function as input and returns an augmented function as output (`@decorator` syntax is syntactic sugar for `fn = decorator(fn)`). Always decorate wrappers with `@functools.wraps(fn)` to preserve the original function's `__name__`, docstrings, and parameter annotations.""",
            "formulas": """1. **Decorator Syntactic Equivalence:**
   $$@\\\\text{my\\_decorator} \\\\quad \\\\text{def func(): pass} \\\\iff \\\\text{func} = \\\\text{my\\_decorator}(\\\\text{func})$$""",
            "solved_examples": [
                {
                    "title": "Creating an Execution Timing Decorator with functools.wraps",
                    "difficulty": "Easy | Amazon, TCS, Infosys",
                    "problem": "Write a reusable decorator that measures and logs function execution time.",
                    "step_by_step": [
                        "Step 1: Import `time` and `functools.wraps`.",
                        "Step 2: Define outer function accepting target `fn`.",
                        "Step 3: Define inner `wrapper(*args, **kwargs)` decorated with `@wraps(fn)`.",
                        "Step 4: Record start time, execute `fn`, record elapsed, print metric, return result."
                    ],
                    "code_or_math": """import time
import functools

def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"[{func.__name__}] executed in {duration:.6f}s")
        return result
    return wrapper""",
                    "explanation": "@functools.wraps copies the original function's name and docstring to the wrapper, preventing debugging confusion."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the purpose of @functools.wraps in a decorator?",
                    "options": [
                        "A) To make the function run asynchronously",
                        "B) To copy the original function's name, docstrings, and signature to the wrapper",
                        "C) To prevent recursion",
                        "D) To optimize bytecode compilation"
                    ],
                    "correct_answer": "B) To copy the original function's name, docstrings, and signature to the wrapper",
                    "detailed_solution": "Without @functools.wraps, the decorated function takes on the name 'wrapper' and loses its original docstrings."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft",
                    "question": "How do you write a decorator that accepts arguments, such as @repeat(num_times=3)?",
                    "model_answer": "A decorator with arguments requires three nested function levels: 1) The outermost function accepts the decorator parameters (`repeat(num_times)`). 2) The middle function accepts the target function (`decorator(func)`). 3) The innermost wrapper intercepts calls (`wrapper(*args, **kwargs)`). The middle function returns the wrapper, and the outer function returns the decorator.",
                    "interviewer_tip": "Write the three-tier nested function template clearly."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Object-Oriented Python & Dunder Methods",
        "key_takeaways": "Master classes, instances, __init__, __str__ vs __repr__, __eq__, __hash__, operator overloading, and inheritance with super().",
        "topics": [
            "Class attributes vs instance attributes and memory savings with __slots__",
            "Special Dunder methods: __init__, __repr__, __str__, __len__, __getitem__",
            "Operator overloading: __add__, __lt__, __eq__, and __hash__",
            "Multiple inheritance, Diamond problem, and Method Resolution Order (MRO / C3 Linearization)",
            "Class methods (@classmethod) vs Static methods (@staticmethod)"
        ],
        "sections": {
            "concept": """Python implements flexible OOP through magic or 'dunder' (double-underscore) methods:
- `__repr__`: Unambiguous string representation for developers.
- `__str__`: Human-friendly string representation.
- `__eq__` & `__hash__`: Contract for set membership and dictionary keys. If a class overrides `__eq__` without implementing `__hash__`, Python marks it unhashable.
- `__slots__`: Prevents dynamic `__dict__` creation per instance, reducing object memory footprint by up to 60%.

**Method Resolution Order (MRO):**
Python resolves multiple inheritance hierarchies using the **C3 Linearization Algorithm**, guaranteeing that child classes precede parents and preserving local precedence order without duplicate visits.""",
            "formulas": """1. **MRO Inspection:**
   $$\\\\text{Class.mro}() \\\\implies \\\\text{Deterministic resolution sequence for method dispatch}$$""",
            "solved_examples": [
                {
                    "title": "Implementing Comparable & Hashable Custom Class",
                    "difficulty": "Easy | Amazon, Google",
                    "problem": "Create a Point(x, y) class supporting equality, hashing, and addition.",
                    "step_by_step": [
                        "Step 1: Implement `__init__(self, x, y)`.",
                        "Step 2: Implement `__eq__` checking coordinates.",
                        "Step 3: Implement `__hash__` hashing `(self.x, self.y)`.",
                        "Step 4: Implement `__add__` returning new `Point`."
                    ],
                    "code_or_math": """class Point:
    __slots__ = ('x', 'y') # Optimizes memory

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})" """,
                    "explanation": "Instances can now be inserted into sets, used as dict keys, and combined using the `+` operator."
                }
            ],
            "practice_questions": [
                {
                    "question": "What does defining `__slots__` in a Python class achieve?",
                    "options": [
                        "A) Prevents inheritance",
                        "B) Eliminates the default instance __dict__, saving substantial memory",
                        "C) Makes all attributes private",
                        "D) Enforces multithreading"
                    ],
                    "correct_answer": "B) Eliminates the default instance __dict__, saving substantial memory",
                    "detailed_solution": "__slots__ replaces dynamic per-instance dictionaries with static pointer arrays."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is the difference between @classmethod and @staticmethod?",
                    "model_answer": "@classmethod receives the class object itself (`cls`) as its first argument, enabling alternative factory constructors and subclass-aware operations. @staticmethod receives neither `self` nor `cls`; it acts as an ordinary utility function bound to the class namespace.",
                    "interviewer_tip": "Cite factory methods (`cls.from_json()`) as the primary use case for classmethod."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Iterators, Generators & Context Managers",
        "key_takeaways": "Master iterator protocol (__iter__, __next__), memory-efficient generator functions (yield), and context managers (__enter__, __exit__).",
        "topics": [
            "Iterator protocol: Iterable vs Iterator, StopIteration exception",
            "Generators: The yield statement, lazy evaluation, and generator expressions",
            "Streaming huge datasets with O(1) memory via generators",
            "Context Managers: with statement, __enter__, and __exit__",
            "Writing context managers using @contextlib.contextmanager"
        ],
        "sections": {
            "concept": """Iterators provide sequential data consumption with minimal memory overhead:
- **Iterable:** Object implementing `__iter__()` returning an Iterator.
- **Iterator:** Object implementing `__next__()` returning elements one at a time until raising `StopIteration`.
- **Generators:** Functions containing `yield`. Instead of returning a full list and terminating, they return a generator object, pausing state at the `yield` expression and resuming on the next `next()` call. Ideal for streaming multi-gigabyte logs with $O(1)$ memory.
- **Context Managers (`with` statement):** Guarantee resource setup and teardown via `__enter__()` and `__exit__()`, handling exceptions safely.""",
            "formulas": """1. **Generator Memory Invariant:**
   $$\\\\text{Memory}([x \\\\text{ for } x \\\\text{ in } 10^8]) = O(N) \\\\approx 800 \\\\text{ MB}$$
   $$\\\\text{Memory}((x \\\\text{ for } x \\\\text{ in } 10^8)) = O(1) \\\\approx 112 \\\\text{ bytes!}$$""",
            "solved_examples": [
                {
                    "title": "Chunked Large File Reader with Generator",
                    "difficulty": "Easy | Google, Amazon",
                    "problem": "Read a multi-gigabyte text file in 4KB chunks without exhausting memory.",
                    "step_by_step": [
                        "Step 1: Open file in context manager.",
                        "Step 2: Read chunk in a while loop; if chunk empty, break.",
                        "Step 3: Yield chunk."
                    ],
                    "code_or_math": """def read_large_file(file_path, chunk_size=4096):
    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk""",
                    "explanation": "Consumes strictly $O(\\\\text{chunk\\\\_size})$ memory regardless of total file size."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens when a generator function completes execution?",
                    "options": [
                        "A) Returns None",
                        "B) Raises StopIteration exception",
                        "C) Resets to start",
                        "D) Deletes itself"
                    ],
                    "correct_answer": "B) Raises StopIteration exception",
                    "detailed_solution": "When a generator reaches return or the end of its body, CPython automatically raises StopIteration to terminate iteration."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What parameters does __exit__() receive and how do you suppress an exception within a context manager?",
                    "model_answer": "`__exit__()` receives three parameters: `(exc_type, exc_val, exc_tb)`. If no exception occurred, all three are `None`. If an exception was raised, `__exit__()` can suppress it from propagating up the call stack by returning `True`. If it returns `False` or `None`, the exception is re-raised automatically.",
                    "interviewer_tip": "Explicitly mention returning True to suppress exceptions."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Error Handling, File I/O & Serialization",
        "key_takeaways": "Master try-except-else-finally, custom exceptions, JSON serialization, and pickle security warnings.",
        "topics": [
            "Exception hierarchy: BaseException vs Exception",
            "try-except-else-finally control flow semantics",
            "Creating custom domain exceptions",
            "JSON parsing and serialization with custom JSONEncoder",
            "Pickle serialization mechanics and remote code execution vulnerabilities"
        ],
        "sections": {
            "concept": """Python handles errors via exceptions derived from `Exception` (avoid catching `BaseException`, which catches `KeyboardInterrupt` and `SystemExit`).
- `try`: Code that may raise exceptions.
- `except`: Catches and handles specific exception classes.
- `else`: Executes if and only if NO exception was raised in the `try` block.
- `finally`: Guarantees cleanup execution under all conditions.

**Serialization:**
- `json`: Safe, portable, standard text representation.
- `pickle`: Python-specific binary object serializer. Never unpickle untrusted data because `pickle` can execute arbitrary bytecode during deserialization.""",
            "formulas": """1. **Control Flow:**
   $$\\\\text{try} \\\\to \\\\text{except (on error)} \\\\quad \\\\text{or} \\\\quad \\\\text{else (on success)} \\\\to \\\\text{finally (always)}$$""",
            "solved_examples": [
                {
                    "title": "Custom JSON Encoder for Datetime and UUID",
                    "difficulty": "Easy | Amazon, TCS",
                    "problem": "Serialize custom objects containing datetime and UUID fields to JSON.",
                    "step_by_step": [
                        "Step 1: Subclass `json.JSONEncoder`.",
                        "Step 2: Override `default(self, obj)`.",
                        "Step 3: Convert datetime to ISO format, UUID to str; fallback to `super().default(obj)`."
                    ],
                    "code_or_math": """import json
from datetime import datetime
import uuid

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)""",
                    "explanation": "Allows seamless JSON encoding of complex domain objects."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why is unpickling data received from untrusted network sources hazardous?",
                    "options": [
                        "A) It is slow",
                        "B) It can execute arbitrary malicious code via the __reduce__ method",
                        "C) It causes memory leaks",
                        "D) It corrupts the GIL"
                    ],
                    "correct_answer": "B) It can execute arbitrary malicious code via the __reduce__ method",
                    "detailed_solution": "Pickle allows serialized streams to instantiate arbitrary callables, enabling remote code execution."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "What is the difference between catching Exception vs BaseException in Python?",
                    "model_answer": "BaseException is the root of the exception hierarchy. It includes system-exiting exceptions like `KeyboardInterrupt` (Ctrl+C) and `SystemExit`. Subclassing `Exception` excludes these system events. Catching `BaseException` intercepts user aborts, preventing graceful program shutdown.",
                    "interviewer_tip": "Advise always catching specific Exception subclasses."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Concurrency & Asynchronous Programming",
        "key_takeaways": "Master the Global Interpreter Lock (GIL), threading for I/O bounds, multiprocessing for CPU bounds, and asyncio event loops.",
        "topics": [
            "The Global Interpreter Lock (GIL) and bytecode execution safety",
            "Multithreading (threading): When it helps (I/O bound) vs hurts (CPU bound)",
            "Multiprocessing (multiprocessing): Bypassing the GIL with IPC shared memory",
            "Asynchronous programming: asyncio event loops, coroutines (async/await), and tasks",
            "Race conditions, Locks, and thread-safe queues"
        ],
        "sections": {
            "concept": """Python concurrency is defined by the **Global Interpreter Lock (GIL)**: a mutex protecting CPython memory management and reference counts, allowing only one native thread to execute Python bytecode at any given moment.

**Choosing Concurrency Paradigms:**
1. **CPU-Bound Tasks (Image processing, machine learning math):** Multithreading cannot run on multiple CPU cores due to the GIL. Use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` to spawn separate OS processes each with its own independent GIL.
2. **I/O-Bound Tasks (HTTP requests, database calls):** Threads release the GIL while waiting on socket I/O. Use `threading` or `asyncio`.
3. **Asynchronous I/O (`asyncio`):** Single-threaded cooperative multitasking utilizing an Event Loop with non-blocking sockets. Runs thousands of concurrent I/O operations with minimal memory overhead.""",
            "formulas": """1. **Concurrency Selection Matrix:**
   $$\\\\text{CPU Bound} \\\\implies \\\\text{multiprocessing}$$
   $$\\\\text{I/O Bound (Thousands of connections)} \\\\implies \\\\text{asyncio (async/await)}$$
   $$\\\\text{I/O Bound (Simple blocking calls)} \\\\implies \\\\text{ThreadPoolExecutor}$$""",
            "solved_examples": [
                {
                    "title": "Concurrent URL Fetcher using asyncio",
                    "difficulty": "Medium | Google, Uber",
                    "problem": "Fetch multiple URLs concurrently without blocking the main event loop.",
                    "step_by_step": [
                        "Step 1: Define async fetch coroutine.",
                        "Step 2: Collect tasks using `asyncio.gather()`."
                    ],
                    "code_or_math": """import asyncio

async def fetch_url(url_id: int):
    await asyncio.sleep(1) # Simulates non-blocking network I/O
    return f"Response {url_id}"

async def main():
    tasks = [fetch_url(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(results)

# asyncio.run(main())""",
                    "explanation": "All 5 network requests run concurrently, completing in ~1.0 second total instead of 5.0 seconds sequentially."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why does a CPU-heavy computation run slower on 4 threads than on 1 thread in standard CPython?",
                    "options": [
                        "A) Because threads crash",
                        "B) Because the GIL forces serial execution while thread context switching incurs overhead",
                        "C) Because CPU clock speed decreases",
                        "D) Because memory is halved"
                    ],
                    "correct_answer": "B) Because the GIL forces serial execution while thread context switching incurs overhead",
                    "detailed_solution": "The GIL forces CPU-bound threads to execute one at a time, so thread scheduling contention adds net overhead."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is the GIL, why does it exist in CPython, and how do you bypass it?",
                    "model_answer": "The Global Interpreter Lock (GIL) is a mutual exclusion lock preventing multiple native threads from executing Python bytecode simultaneously. It exists because CPython's memory management uses reference counting, which is not thread-safe; without the GIL, concurrent updates could corrupt reference counts. To bypass it: 1) Use `multiprocessing` to utilize multiple OS processes. 2) Offload computation to C/C++ extensions (like NumPy) that release the GIL during heavy number crunching. 3) Use free-threaded Python 3.13+ builds.",
                    "interviewer_tip": "Mention C extensions (NumPy) releasing the GIL."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Python Algorithms, Testing & Placement Interview Patterns",
        "key_takeaways": "Master pytest unit testing, fixtures, mocks, profiling with cProfile, and high-performance placement coding idioms.",
        "topics": [
            "Unit testing with pytest: Test discovery, assertions, and parameterized tests",
            "Fixtures and mocking dependencies with unittest.mock",
            "Performance profiling using cProfile and timeit",
            "Top Python placement coding idioms: bisect, collections.Counter, itertools",
            "Placement coding interview communication rubric"
        ],
        "sections": {
            "concept": """This capstone chapter focuses on software engineering quality, automated testing, and high-performance algorithms tested in tech placement interviews.

Standard library tools that supercharge interview coding speed:
- `collections.Counter`: Instantly creates frequency tables.
- `collections.defaultdict`: Eliminates key-existence boilerplate.
- `itertools`: Provides memory-efficient iterators (`chain`, `combinations`, `permutations`).
- `bisect`: In-place binary search on sorted sequences (`bisect_left`, `bisect_right`).
- `heapq`: Fast binary min-heap operations.""",
            "formulas": """1. **Binary Search with bisect:**
   $$\\\\text{index} = \\\\text{bisect.bisect\\_left}(sorted\\_arr, target) \\\\implies O(\\\\log n)$$""",
            "solved_examples": [
                {
                    "title": "Parameterized Unit Testing with pytest",
                    "difficulty": "Easy | Amazon, TCS Digital",
                    "problem": "Write a parameterized test verifying palindrome strings with multiple test cases.",
                    "step_by_step": [
                        "Step 1: Write palindrome logic.",
                        "Step 2: Use `@pytest.mark.parametrize` with inputs and expected outputs."
                    ],
                    "code_or_math": """def is_palindrome(s: str) -> bool:
    clean = ''.join(c.lower() for c in s if c.isalnum())
    return clean == clean[::-1]

# In test_palindrome.py:
# import pytest
# @pytest.mark.parametrize("text, expected", [
#     ("A man, a plan, a canal: Panama", True),
#     ("race a car", False),
#     ("", True),
# ])
# def test_is_palindrome(text, expected):
#     assert is_palindrome(text) == expected""",
                    "explanation": "Parametrized testing covers diverse edge cases concisely without redundant test functions."
                }
            ],
            "practice_questions": [
                {
                    "question": "Which module provides binary search functionality on sorted lists in Python?",
                    "options": ["A) search", "B) bisect", "C) algorithm", "D) binary"],
                    "correct_answer": "B) bisect",
                    "detailed_solution": "bisect.bisect_left and bisect.bisect_right implement logarithmic binary searches."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "In Python, why is `''.join(list_of_strings)` significantly faster than repeated string concatenation `s += item` in a loop?",
                    "model_answer": "Strings are immutable. In `s += item`, Python must allocate a new memory buffer of size `len(s) + len(item)` and copy all characters from `s` on every iteration, leading to $O(N^2)$ quadratic copying. In contrast, `''.join(list_of_strings)` computes the total length of all strings in a single pass, allocates the exact destination buffer once, and copies all strings in linear $O(N)$ time.",
                    "interviewer_tip": "Cite quadratic $O(N^2)$ vs linear $O(N)$ memory allocations."
                }
            ]
        }
    }
]
'''
    (CURRICULUM_DIR / "curriculum_python.py").write_text(content, encoding="utf-8")
    print("Created curriculum_python.py")

build_python_module()
