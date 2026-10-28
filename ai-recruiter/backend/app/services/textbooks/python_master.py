"""
python_master.py — Prescribed Master Textbook for Python Programming & Core Language Architecture.
Comprehensive unabridged campus placement textbook covering CPython internals, PVM,
GIL, memory management, reference counting, cyclic GC, LEGB scoping, closures, decorators,
OOP __new__ vs __init__, MRO C3 linearization, iterators, generators, asyncio,
and placement coding interview challenges.
"""

PYTHON_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Python Architecture, CPython Internals, PVM & The GIL",
        "topics": [
            "CPython execution pipeline: Source code -> Tokenizer -> AST -> Bytecode (.pyc) -> Python Virtual Machine (PVM)",
            "The Global Interpreter Lock (GIL): Mutex mechanism in CPython and its impact on multi-threading vs multiprocessing",
            "Memory Management: PyObject C-structure, PyGC_Head, and object allocator (PyMalloc)",
            "Garbage Collection mechanics: Reference counting and the generational cyclic garbage collector (Gen 0, 1, 2 thresholds)",
            "Python 3.12+ and 3.13 free-threaded Python (PEP 703) evolution"
        ],
        "key_takeaways": "CPython uses reference counting for immediate deallocation and a 3-generation cyclic garbage collector to detect circular references. The GIL permits only one native thread to execute Python bytecode at a time."
    },
    {
        "chapter_num": 2,
        "title": "Data Structures, Memory Representation & Mutability",
        "topics": [
            "Lists: Dynamic arrays of pointers, over-allocation growth formula, and amortized O(1) appending",
            "Tuples: Immutability, memory savings, tuple reuse pools, and hashability criteria",
            "Dictionaries: Compact hash table layout (indices array + entries array), collision resolution with quadratic probing",
            "Sets: Open addressing hash sets and mathematical set operations (union, intersection, symmetric difference)",
            "Shallow copy (copy.copy()) vs Deep copy (copy.deepcopy()) and recursive object graph traversal"
        ],
        "key_takeaways": "Python lists are arrays of 64-bit pointers to heap objects. Since Python 3.6+, dictionaries preserve insertion order by maintaining a dense array of entries indexed by a sparse hash table."
    },
    {
        "chapter_num": 3,
        "title": "Functions, Scoping Rules (LEGB), Closures & Decorators",
        "topics": [
            "The LEGB Scoping Rule: Local -> Enclosing -> Global -> Built-in namespace resolution",
            "The 'global' and 'nonlocal' keywords and mutating enclosed bindings",
            "First-Class Functions, closures, and the '__closure__' cell objects inspection",
            "Decorators: Function decorators, parameterized decorators, and class-based decorators",
            "Preserving introspection metadata: The role of @functools.wraps in production decorators"
        ],
        "key_takeaways": "Decorators wrap functions using closures. Applying @functools.wraps copies the original function's __name__, __doc__, and annotations to the wrapper, preventing loss of debugging metadata."
    },
    {
        "chapter_num": 4,
        "title": "Object-Oriented Python, Dunder Methods & Metaclasses",
        "topics": [
            "Object instantiation: '__new__' (object creation allocator) vs '__init__' (object state initialization)",
            "Multiple inheritance and Method Resolution Order (MRO): The C3 Linearization Algorithm",
            "Dunder methods: Operator overloading, '__str__' vs '__repr__', '__call__', and context managers ('__enter__', '__exit__')",
            "Property Descriptors: The descriptor protocol ('__get__', '__set__', '__delete__') and '@property' implementation",
            "Metaclasses: Classes as instances of 'type', metaclass creation, and '__init_subclass__'"
        ],
        "key_takeaways": "__new__ is the static method that actually allocates memory and creates the instance; __init__ initializes the instance after creation. MRO follows C3 linearization to prevent diamond inheritance ambiguity."
    },
    {
        "chapter_num": 5,
        "title": "Advanced Python: Iterators, Generators, Itertools & Coroutines",
        "topics": [
            "Iterator Protocol: '__iter__()' returning self and '__next__()' raising StopIteration",
            "Generators: The 'yield' keyword, suspension of frame execution, and state retention",
            "Bidirectional generator communication: '.send()', '.throw()', and '.close()'",
            "High-performance streaming using 'itertools': chain, islice, groupby, cycle, product, combinations",
            "Memory profiling: Iterators vs lists on gigabyte-scale datasets"
        ],
        "key_takeaways": "Generators compute values lazily on-the-fly, providing O(1) space complexity regardless of the size of the sequence being traversed."
    },
    {
        "chapter_num": 6,
        "title": "Concurrency in Python: Threading, Multiprocessing & Asyncio",
        "topics": [
            "The 'threading' module: Best practices for I/O-bound tasks (file downloads, network requests)",
            "The 'multiprocessing' module: Bypassing the GIL for CPU-bound computations with separate memory processes",
            "High-level concurrency: concurrent.futures (ThreadPoolExecutor vs ProcessPoolExecutor)",
            "Asynchronous programming: 'asyncio' event loop, coroutines ('async def' / 'await'), Tasks, and Futures",
            "Concurrency coordination: asyncio.gather(), asyncio.as_completed(), and handling task cancellations"
        ],
        "key_takeaways": "For CPU-bound tasks, multiprocessing bypasses the GIL by creating independent OS processes. For concurrent network I/O, asyncio provides cooperative single-threaded asynchronous execution with thousands of concurrent connections."
    },
    {
        "chapter_num": 7,
        "title": "Solved Python Placement Coding Challenges & Output Predictions",
        "topics": [
            "Tricky mutable default argument puzzle ('def append_to(item, target=[])')",
            "Late-binding closures in loops ('[lambda: i for i in range(5)]') output explanation",
            "Handwritten LRU Cache implementation using collections.OrderedDict",
            "Arbitrary nested list flattening generator implementation",
            "Self-assessment practice drills with verified solutions"
        ],
        "key_takeaways": "Mastering mutable default parameters, late-binding closures, and generator pipelines prevents classic bugs and guarantees high marks in technical Python rounds."
    }
]

PYTHON_TEXTBOOK_MARKDOWN = r"""# Python Programming & Core Language Architecture: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Python Programming  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement technical tests, Python programming evaluations, and core language interview questions are strictly grounded in the language specifications, CPython memory models, and standard library architectures detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Python Architecture, CPython Internals, PVM & The GIL](#chapter-1-python-architecture-cpython-internals-pvm--the-gil)
  - [1.1 The CPython Compilation Pipeline](#11-the-cpython-compilation-pipeline)
  - [1.2 The Global Interpreter Lock (GIL) Deep Dive](#12-the-global-interpreter-lock-gil-deep-dive)
  - [1.3 Memory Management & The PyObject Model](#13-memory-management--the-pyobject-model)
  - [1.4 Garbage Collection: Reference Counting & Cyclic GC](#14-garbage-collection-reference-counting--cyclic-gc)
- [Chapter 2: Data Structures, Memory Representation & Mutability](#chapter-2-data-structures-memory-representation--mutability)
  - [2.1 Python Lists: Dynamic Array Over-Allocation](#21-python-lists-dynamic-array-over-allocation)
  - [2.2 Tuples & Memory Internals](#22-tuples--memory-internals)
  - [2.3 Dictionaries: Modern Compact Hash Tables](#23-dictionaries-modern-compact-hash-tables)
  - [2.4 Shallow Copy vs Deep Copy](#24-shallow-copy-vs-deep-copy)
- [Chapter 3: Functions, Scoping Rules (LEGB), Closures & Decorators](#chapter-3-functions-scoping-rules-legb-closures--decorators)
  - [3.1 The LEGB Rule & Scope Resolution](#31-the-legb-rule--scope-resolution)
  - [3.2 First-Class Functions & Closures](#32-first-class-functions--closures)
  - [3.3 Practical Decorators & @functools.wraps](#33-practical-decorators--functoolswraps)
- [Chapter 4: Object-Oriented Python, Dunder Methods & Metaclasses](#chapter-4-object-oriented-python-dunder-methods--metaclasses)
  - [4.1 Instantiation Lifecycle: `__new__` vs `__init__`](#41-instantiation-lifecycle-__new__-vs-__init__)
  - [4.2 Method Resolution Order (MRO) & C3 Linearization](#42-method-resolution-order-mro--c3-linearization)
  - [4.3 High-Yield Dunder Methods](#43-high-yield-dunder-methods)
  - [4.4 The Descriptor Protocol & @property](#44-the-descriptor-protocol--property)
- [Chapter 5: Advanced Python: Iterators, Generators, Itertools & Coroutines](#chapter-5-advanced-python-iterators-generators-itertools--coroutines)
  - [5.1 The Iterator Protocol](#51-the-iterator-protocol)
  - [5.2 Generators & The `yield` Keyword](#52-generators--the-yield-keyword)
  - [5.3 High-Performance Iteration with `itertools`](#53-high-performance-iteration-with-itertools)
- [Chapter 6: Concurrency in Python: Threading, Multiprocessing & Asyncio](#chapter-6-concurrency-in-python-threading-multiprocessing--asyncio)
  - [6.1 Threading for I/O-Bound Workloads](#61-threading-for-io-bound-workloads)
  - [6.2 Multiprocessing for CPU-Bound Workloads](#62-multiprocessing-for-cpu-bound-workloads)
  - [6.3 Asynchronous Programming with `asyncio`](#63-asynchronous-programming-with-asyncio)
- [Chapter 7: Solved Python Placement Coding Challenges & Output Predictions](#chapter-7-solved-python-placement-coding-challenges--output-predictions)
  - [Challenge 1: The Mutable Default Argument Pitfall](#challenge-1-the-mutable-default-argument-pitfall)
  - [Challenge 2: Late-Binding Closures in Loops](#challenge-2-late-binding-closures-in-loops)
  - [Challenge 3: Handwritten LRU Cache via OrderedDict](#challenge-3-handwritten-lru-cache-via-ordereddict)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: Python Architecture, CPython Internals, PVM & The GIL

### 1.1 The CPython Compilation Pipeline
CPython is the reference implementation of Python written in C. When you execute `python script.py`, the source code undergoes a multi-stage transformation:

```
[ script.py ] 
       |
       v
[ Tokenizer / Lexer ] -> Stream of lexical tokens
       |
       v
[ Parser ]            -> Builds Abstract Syntax Tree (AST)
       |
       v
[ Bytecode Compiler ] -> Produces Python Bytecode (.pyc file stored in __pycache__)
       |
       v
[ Python Virtual Machine (PVM) ] -> Stack-based evaluation loop (ceval.c)
```

The PVM is a **stack-based evaluation machine**; it has no registers. It loads operands onto an evaluation stack, executes bytecode instructions (such as `BINARY_ADD` or `CALL_FUNCTION`), and pops results.

### 1.2 The Global Interpreter Lock (GIL) Deep Dive
The **Global Interpreter Lock (GIL)** is a mutual exclusion mutex in CPython that prevents multiple native OS threads from executing Python bytecode simultaneously.

- **Why the GIL Exists:** CPython's memory management is fundamentally non-thread-safe. Reference count variables on objects could easily suffer race conditions without locking. The GIL provides a coarse-grained lock ensuring thread safety without requiring microscopic per-object locks (which would devastate single-threaded performance).
- **Impact on Multi-Threading:**
  - **I/O-Bound Tasks (Good):** When a thread performs socket reads, file I/O, or sleeps (`time.sleep()`), it voluntarily releases the GIL, allowing other threads to run concurrently.
  - **CPU-Bound Tasks (Poor):** Multi-threaded CPU-heavy tasks run on only **one core**! In fact, due to OS thread switching overhead and lock contention, a multi-threaded CPU task can run slower than a single-threaded implementation on multi-core systems.
  - **The Solution:** Use the `multiprocessing` module, which spawns independent Python interpreter processes with separate memory spaces and individual GILs.

### 1.3 Memory Management & The PyObject Model
In CPython, **everything is an object**. Even a simple integer `x = 42` is a full heap-allocated C struct:

```c
// Base struct for all standard Python objects:
typedef struct _object {
    _PyObject_HEAD_EXTRA // Double-linked list pointers for tracing GC
    Py_ssize_t ob_refcnt; // Reference count (64-bit integer)
    struct _typeobject *ob_type; // Pointer to the object's type object
} PyObject;
```

A Python integer consumes **28 bytes** on a 64-bit machine:
- `ob_refcnt`: 8 bytes
- `ob_type`: 8 bytes
- `ob_size`: 8 bytes (indicates number of digits in arbitrary-precision int)
- `ob_digit`: 4 bytes (the actual integer payload)

### 1.4 Garbage Collection: Reference Counting & Cyclic GC
CPython manages memory via two cooperating mechanisms:
1. **Reference Counting (Primary):**
   - Every object maintains `ob_refcnt`.
   - When a variable points to an object, its reference count increments.
   - When a reference goes out of scope or is reassigned, `ob_refcnt` decrements.
   - When `ob_refcnt == 0`, the memory block is **immediately returned** to the memory allocator.
2. **Generational Cyclic Garbage Collector (Secondary):**
   - Reference counting fails when objects reference each other cyclically ($A \to B \to A$). If all outside references to $A$ and $B$ are removed, their reference counts remain 1, causing a permanent memory leak.
   - The cyclic GC inspects container objects (lists, dicts, custom class instances). It groups objects into 3 generations:
     - **Generation 0:** Newly created objects. Scanned frequently (threshold: 700 allocations).
     - **Generation 1:** Surviving objects from Gen 0.
     - **Generation 2:** Long-lived objects (e.g., modules, global constants). Scanned least frequently.

---

## Chapter 2: Data Structures, Memory Representation & Mutability

### 2.1 Python Lists: Dynamic Array Over-Allocation
A Python list is NOT a linked list; it is a **dynamic array of 64-bit pointers** pointing to objects in heap memory.

**The Growth / Over-Allocation Formula in CPython:**
When a list exceeds its current capacity, CPython allocates extra headroom to achieve amortized $O(1)$ appends:
$$\text{new\_allocated} = \text{newsize} + (\text{newsize} \gg 3) + (\text{newsize} < 9 \ ? \ 3 : 6)$$
For example, appending to an empty list grows capacity: $0 \to 4 \to 8 \to 16 \to 25 \to 35 \dots$

### 2.2 Tuples & Memory Internals
Tuples are immutable sequences:
- Once instantiated, their length and pointers cannot be modified.
- **Memory Optimization:** Empty tuples `()` are singletons; CPython caches up to 20,000 small tuples of size 1 to 20 in a free list pool to avoid repeated calls to `malloc()`.
- **Hashability:** A tuple is hashable (and can be used as a dictionary key or set element) if and only if **all of its contained elements are themselves hashable**.

### 2.3 Dictionaries: Modern Compact Hash Tables
Since Python 3.6 (formalized in 3.7), dicts utilize Raymond Hettinger's compact hash table design:

```
Legacy Dict (Sparse Table - 33% memory wasted):
[ Hash | Key | Value ] [ Empty ] [ Empty ] [ Hash | Key | Value ]

Modern Compact Dict:
Indices Array (Sparse): [ 0 | None | 1 | None | None ]
Entries Array (Dense):  [
    0: {hash: 0x44a, key: 'name', value: 'Alice'},
    1: {hash: 0x98f, key: 'role', value: 'Architect'}
]
```
- **Benefits:** Reduces dictionary memory consumption by 30% to 40% and guarantees that dictionaries maintain **insertion order**.

### 2.4 Shallow Copy vs Deep Copy
- **Shallow Copy (`copy.copy(x)`):** Constructs a new container object, but populates it with references to the exact same child objects contained in the original.
- **Deep Copy (`copy.deepcopy(x)`):** Recursively traverses the entire object graph, constructing brand new copies of every referenced container and nested object. Maintains a memo dictionary to prevent infinite loops on circular references.

---

## Chapter 3: Functions, Scoping Rules (LEGB), Closures & Decorators

### 3.1 The LEGB Rule & Scope Resolution
When an identifier is referenced inside a function, Python searches namespaces in strict order:

$$\mathbf{L} \text{ocal} \longrightarrow \mathbf{E} \text{nclosing} \longrightarrow \mathbf{G} \text{lobal} \longrightarrow \mathbf{B} \text{uilt-in}$$

- **`global` keyword:** Explicitly binds an identifier to the module-level global namespace.
- **`nonlocal` keyword:** Binds an identifier to the nearest enclosing non-global scope (mandatory when modifying an outer function's variable inside a closure).

### 3.2 First-Class Functions & Closures
A **Closure** occurs when an inner function remembers and has access to variables in its enclosing scope, even after the outer function has finished executing:

```python
def make_multiplier(factor):
    def multiplier(number):
        return number * factor # factor is captured in closure cell
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5)) # Outputs: 10
print(triple(5)) # Outputs: 15
print(double.__closure__[0].cell_contents) # Outputs: 2
```

### 3.3 Practical Decorators & @functools.wraps
A decorator is a callable that takes a function as an argument and returns an augmented function:

```python
import functools
import time

def timing_decorator(func):
    @functools.wraps(func) # Preserves func.__name__, func.__doc__, etc.
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"[METRIC] {func.__name__} executed in {duration:.4f}s")
        return result
    return wrapper

@timing_decorator
def calculate_heavy_primes(limit):
    # Calculates prime count up to limit.
    return sum(1 for i in range(2, limit) if all(i % d != 0 for d in range(2, int(i**0.5) + 1)))
```

---

## Chapter 4: Object-Oriented Python, Dunder Methods & Metaclasses

### 4.1 Instantiation Lifecycle: `__new__` vs `__init__`
1. `__new__(cls, *args, **kwargs)`:
   - A static method (treated specially) responsible for **allocating memory and returning a new instance of `cls`**.
   - Must return a valid object instance (typically via `super().__new__(cls)`).
   - Used in singleton patterns, immutable subclassing (`tuple`, `int`), and metaclasses.
2. `__init__(self, *args, **kwargs)`:
   - An instance method called immediately after `__new__` returns the instance.
   - Responsible for initializing attributes on `self`. Returns `None`.

```python
class SingletonService:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, service_name="Core"):
        self.service_name = service_name
```

### 4.2 Method Resolution Order (MRO) & C3 Linearization
In multiple inheritance, Python resolves attribute access using the **C3 Linearization Algorithm**:
- Preserves local precedence order (classes listed first take priority).
- Preserves monotonicity (if class $A$ precedes class $B$ in a parent's MRO, it must precede $B$ in all child MROs).
- Inspect via `ClassName.__mro__` or `ClassName.mro()`.

### 4.3 High-Yield Dunder Methods
- `__str__`: Human-readable string representation (used by `print()` and `str()`).
- `__repr__`: Unambiguous developer representation (used in debugging; ideal if `eval(repr(obj)) == obj`).
- `__call__`: Allows an instance to be invoked as a function (`obj()`).
- Context Managers:
  - `__enter__`: Sets up resource and returns target for `as` variable.
  - `__exit__(exc_type, exc_val, exc_tb)`: Tears down resource; returns `True` to suppress exception.

### 4.4 The Descriptor Protocol & @property
A **Descriptor** is an object attribute with binding behavior defined by methods in the descriptor protocol: `__get__()`, `__set__()`, and `__delete__()`.

```python
class PositiveNumber:
    def __init__(self, name):
        self.name = name
        
    def __get__(self, instance, owner):
        if instance is None: return self
        return instance.__dict__.get(self.name, 0)
        
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} must be >= 0")
        instance.__dict__[self.name] = value

class Account:
    balance = PositiveNumber("balance")
    
    def __init__(self, balance):
        self.balance = balance
```

---

## Chapter 5: Advanced Python: Iterators, Generators, Itertools & Coroutines

### 5.1 The Iterator Protocol
An object is an **Iterable** if it implements `__iter__()` returning an iterator.  
An object is an **Iterator** if it implements `__iter__()` and `__next__()`:
```python
class CountDown:
    def __init__(self, start):
        self.current = start
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val
```

### 5.2 Generators & The `yield` Keyword
When a function contains `yield`, Python compiles it as a **Generator Function**. Invoking it returns a generator object without executing the body:
- Calling `next(gen)` executes code up to the next `yield` expression, yields the value, and suspends execution frame state.
- Space Complexity: $O(1)$ memory overhead.

### 5.3 High-Performance Iteration with `itertools`
```python
import itertools

# Infinite counting
counter = itertools.count(start=10, step=2) # 10, 12, 14, 16...

# Chaining multiple iterables without concatenating
merged = itertools.chain([1, 2, 3], ["a", "b"], [100, 200])

# Cartesian product (replaces nested loops)
coords = list(itertools.product(range(3), range(3)))

# Grouping sorted data
data = sorted(["apple", "avocado", "banana", "blueberry", "cherry"], key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, "->", list(group))
```

---

## Chapter 6: Concurrency in Python: Threading, Multiprocessing & Asyncio

### 6.1 Threading for I/O-Bound Workloads
```python
from concurrent.futures import ThreadPoolExecutor
import urllib.request

urls = ["https://httpbin.org/delay/1" for _ in range(5)]

def fetch_url(url):
    with urllib.request.urlopen(url) as response:
        return len(response.read())

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_url, urls))
# Executes 5 parallel network requests in ~1 second instead of 5 seconds!
```

### 6.2 Multiprocessing for CPU-Bound Workloads
```python
from concurrent.futures import ProcessPoolExecutor
import math

def compute_heavy_factors(n):
    return [i for i in range(1, int(math.isqrt(n)) + 1) if n % i == 0]

numbers = [100000000 + i for i in range(8)]
with ProcessPoolExecutor() as executor:
    results = list(executor.map(compute_heavy_factors, numbers))
```

### 6.3 Asynchronous Programming with `asyncio`
```python
import asyncio

async def fetch_record(record_id):
    await asyncio.sleep(0.5) # Simulates non-blocking network I/O
    return {"id": record_id, "status": "verified"}

async def main():
    tasks = [fetch_record(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(f"Processed {len(results)} records asynchronously")

# asyncio.run(main())
```

---

## Chapter 7: Solved Python Placement Coding Challenges & Output Predictions

### Challenge 1: The Mutable Default Argument Pitfall
- **Question:** Predict the output of the following code:
  ```python
  def append_item(val, container=[]):
      container.append(val)
      return container

  print(append_item(1))
  print(append_item(2))
  print(append_item(3, []))
  print(append_item(4))
  ```
- **Explanation:**
  - In Python, **default parameter expressions are evaluated ONCE at function definition time**, not at invocation time.
  - The default list `container` is instantiated in heap memory once when the `def` statement executes.
  - `append_item(1)` appends to default list $\implies$ `[1]`.
  - `append_item(2)` appends to the **same** default list $\implies$ `[1, 2]`.
  - `append_item(3, [])` passes an explicit fresh list $\implies$ `[3]`.
  - `append_item(4)` appends to the original default list $\implies$ `[1, 2, 4]`.
- **Output:**
  ```
  [1]
  [1, 2]
  [3]
  [1, 2, 4]
  ```

### Challenge 2: Late-Binding Closures in Loops
- **Question:** Predict the output:
  ```python
  multipliers = [lambda x: x * i for i in range(4)]
  print([m(2) for m in multipliers])
  ```
- **Explanation:**
  - Python closures bind variables by **reference**, not by value.
  - The variable `i` is looked up in the enclosing scope when the function is **called**, not when it is created.
  - By the time the functions are called, the loop has completed and `i` has value `3`.
  - Every lambda executes `x * 3` $\implies 2 \times 3 = 6$.
- **Output:** `[6, 6, 6, 6]`
- **Fix:** Use default argument binding to freeze value: `[lambda x, i=i: x * i for i in range(4)]` $\implies `[0, 2, 4, 6]`.

### Challenge 3: Handwritten LRU Cache via OrderedDict
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move accessed key to end to mark as recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Evict least recently used (first item)
            self.cache.popitem(last=False)
```

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Is vs ==):** What is the difference between `a is b` and `a == b`?
   - *Solution:* `a == b` tests for equality of values by invoking `a.__eq__(b)`. `a is b` tests for identity; it checks whether `id(a) == id(b)` (whether both variables point to the exact same physical memory address in the heap).

2. **Exercise 2 (GIL and NumPy):** Why does NumPy code achieve 100% CPU multi-core utilization across all threads despite the GIL?
   - *Solution:* NumPy's underlying mathematical operations are written in compiled C/Fortran. Before executing vector arithmetic, NumPy explicitly calls `Py_BEGIN_ALLOW_THREADS` to release the GIL, and reacquires it via `Py_END_ALLOW_THREADS` only when returning back to Python.

3. **Exercise 3 (Generator Memory):** What is the memory footprint difference between `sum([i for i in range(10_000_000)])` and `sum(i for i in range(10_000_000))`?
   - *Solution:* The list comprehension instantiates a full list of 10 million integers in heap memory (~80 MB RAM). The generator expression yields one integer at a time on demand, consuming approximately 120 bytes of RAM total regardless of count.

4. **Exercise 4 (Dictionary Key Requirements):** What two dunder methods must a custom Python class implement to be safely used as a dictionary key or set element?
   - *Solution:* It must implement `__hash__()` to provide an integer hash value and `__eq__()` to handle hash collisions.

5. **Exercise 5 (Exception Chaining):** What does `raise RuntimeError("Failed") from err` do?
   - *Solution:* Implements explicit exception chaining (PEP 3134), setting the `__cause__` attribute on the new exception to `err`, allowing traceback inspection of the root cause.
"""

PYTHON_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "Python Architecture, CPython Internals, PVM & The GIL",
        "subtopic": "Global Interpreter Lock (GIL)",
        "question": "What is the primary architectural effect of the Global Interpreter Lock (GIL) in standard CPython?",
        "options": [
            "It allows only one native thread to execute Python bytecode at any given moment",
            "It prevents Python from creating child processes",
            "It forces all integer variables to be 32-bit floats",
            "It encrypts Python bytecode during execution"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Python Prescribed Textbook — Chapter 1: CPython Internals & The GIL]\nThe GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously in CPython.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 7,
        "chapter_title": "Solved Python Placement Coding Challenges & Output Predictions",
        "subtopic": "Mutable Default Arguments",
        "question": "In Python, when are default argument expressions in function definitions evaluated?",
        "options": [
            "Once, when the function definition statement is executed (definition time)",
            "Every time the function is called",
            "Only when the default parameter is explicitly modified",
            "During garbage collection sweep"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Python Prescribed Textbook — Chapter 7: Placement Puzzles]\nPython evaluates default argument expressions only once at function definition time. This causes mutable objects (lists, dicts) used as defaults to persist modifications across calls.",
        "difficulty": "easy",
    }
]
