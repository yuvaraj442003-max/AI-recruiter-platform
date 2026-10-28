"""
curriculum_java.py - Complete 10 Chapters for Core Java Programming & OOPs.
Every chapter contains:
1. Detailed Concepts & In-Depth Explanation
2. Key Formulas, Rules & JVM Mechanics
3. Step-by-Step Solved Examples with working Java code and breakdown
4. Practice Questions with Answers & Explanations
5. Company Placement Technical Interview Questions & Answers
"""
from typing import List, Dict, Any

JAVA_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "JVM Architecture, Memory Model & Bytecode Execution",
        "key_takeaways": "Master JDK vs JRE vs JVM, classloader subsystems, runtime data areas (Heap, Stack, Metaspace), and JIT compiler optimization.",
        "topics": [
            "JVM Architecture: ClassLoader, Execution Engine, JIT Compiler, Native Interface",
            "Runtime Data Areas: Heap, Thread Stack, Program Counter (PC), Native Method Stack, Metaspace",
            "Bytecode verification, Just-In-Time (JIT) compilation, and HotSpot profiling",
            "Stack Frame structure: Local Variable Array, Operand Stack, Frame Data",
            "Primitive types memory footprint vs Object reference headers"
        ],
        "sections": {
            "concept": """Java achieves platform independence ('Write Once, Run Anywhere') by compiling human-readable source code (`.java`) into intermediate bytecode (`.class`) rather than machine-specific binary. The Java Virtual Machine (JVM) executes this bytecode on host operating systems.

The JVM runtime memory is partitioned into distinct zones:
- **Heap Memory:** Shared across all threads. Stores all instantiated objects and instance arrays. Managed automatically by the Garbage Collector.
- **Thread Stack:** Dedicated per thread. Contains stack frames allocated for each method invocation. Stores primitive local variables and object reference addresses. Deallocated automatically upon method return.
- **Metaspace (Java 8+):** Stores class metadata, bytecode instructions, static variables, and runtime constant pools in native OS memory (replacing the legacy PermGen).
- **Execution Engine:** Combines an interpreter (for rapid initial startup) and the JIT (Just-In-Time) compiler (C1/C2 compilers that translate frequently executed 'hot' bytecode loops directly into native machine code).""",
            "formulas": """1. **Java Object Header Memory Overhead (64-bit JVM):**
   $$\\text{Object Header} = \\text{Mark Word (8 bytes)} + \\text{Klass Pointer (4 bytes with compressed OOPs)} = 12 \\text{ bytes}$$
   $$\\text{All objects padded to multiples of 8 bytes (8-byte alignment rule)}!$$
2. **Stack vs Heap Lifetime:**
   $$\\text{Stack: } LIFO \\text{ lifecycle, strictly deterministic, zero GC overhead}$$
   $$\\text{Heap: } Dynamic lifetime, non-deterministic, managed via GC mark-and-sweep$$""",
            "solved_examples": [
                {
                    "title": "Understanding Stack Frame Allocation & Object References",
                    "difficulty": "Easy | Amazon, TCS, Infosys",
                    "problem": "Trace the memory allocation of primitives and object references in the Heap vs Stack during method execution.",
                    "step_by_step": [
                        "Step 1: When `main()` executes, a stack frame is pushed to the main thread's Stack.",
                        "Step 2: Primitive variable `int x = 42` is allocated directly inside the stack frame's Local Variable Array.",
                        "Step 3: `new StringBuilder(\"Placement\")` allocates a dynamic object on the Heap. The variable `sb` on the stack stores a 4-byte reference pointer pointing to the heap address.",
                        "Step 4: Passing `sb` to a method passes a copy of the reference pointer (Pass-By-Value). Modifications through the reference mutate the heap object."
                    ],
                    "code_or_math": """public class MemoryDemo {
    public static void main(String[] args) {
        int primitiveVal = 100; // Stored in Stack Frame
        StringBuilder refVal = new StringBuilder("Java"); // Object on Heap, pointer on Stack
        
        modify(primitiveVal, refVal);
        
        System.out.println("primitiveVal = " + primitiveVal); // Still 100
        System.out.println("refVal = " + refVal);             // "Java Placement"
    }
    
    public static void modify(int x, StringBuilder sb) {
        x = 999;                    // Mutates local stack copy only
        sb.append(" Placement");    // Mutates shared Heap object
    }
}""",
                    "explanation": "Java is strictly pass-by-value. For primitives, the raw value is copied. For objects, the reference pointer is copied. Both references point to the same physical object in heap memory."
                }
            ],
            "practice_questions": [
                {
                    "question": "Where are static variables stored in Java 8 and beyond?",
                    "options": [
                        "A) Java Thread Stack",
                        "B) PermGen space",
                        "C) Heap Memory (associated with the Class object in Metaspace)",
                        "D) CPU Registers"
                    ],
                    "correct_answer": "C) Heap Memory (associated with the Class object in Metaspace)",
                    "detailed_solution": "Starting in Java 8, PermGen was removed. Class metadata resides in native Metaspace, while static variables and interned strings reside on the regular Java Heap."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "Is Java pass-by-reference or pass-by-value? Give a definitive technical explanation.",
                    "model_answer": "Java is strictly pass-by-value, without exception. When an object is passed as an argument to a method, what is passed is the value of the reference (memory address pointer), copied into the method's local stack frame. If you reassign the reference inside the method (`obj = new Object()`), the caller's reference remains unchanged. If you invoke mutator methods (`obj.setValue(...)`), you mutate the shared heap object.",
                    "interviewer_tip": "Emphasize reassigning the parameter reference to prove pass-by-value."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Object-Oriented Programming Mastery",
        "key_takeaways": "Master the 4 pillars of OOP: Encapsulation, Inheritance, Polymorphism (static vs dynamic), and Abstraction (Abstract Classes vs Interfaces).",
        "topics": [
            "Encapsulation: Access modifiers (private, default, protected, public) and immutable class design",
            "Inheritance: IS-A vs HAS-A composition relationships and the super keyword",
            "Polymorphism: Method Overloading (compile-time) vs Method Overriding (runtime dynamic dispatch)",
            "Abstraction: Abstract Classes vs Interfaces (Default and static methods in Java 8+)",
            "SOLID Principles applied to enterprise Java design"
        ],
        "sections": {
            "concept": """Object-Oriented Programming (OOP) models software systems as interacting objects that encapsulate state and behavior:
1. **Encapsulation:** Hiding internal object state behind accessor/mutator methods to maintain invariant integrity and prevent unauthorized coupling.
2. **Inheritance:** Code reuse mechanism where derived child classes inherit fields and methods from a base parent class (`extends`). Prefer Composition (`HAS-A`) over Inheritance (`IS-A`) to reduce tight coupling.
3. **Polymorphism:** Ability of an entity to take multiple forms. Compile-time polymorphism is achieved via Method Overloading (same method name, different parameter signatures). Runtime polymorphism is achieved via Method Overriding and Dynamic Method Dispatch via the virtual method table (vtable).
4. **Abstraction:** Exposing essential behavioral contracts while concealing concrete implementation details using Interfaces and Abstract Classes.""",
            "formulas": """1. **Dynamic Method Dispatch Resolution:**
   $$\\text{Parent ref } = \\text{new Child}(); \\implies \\text{ref.method}() \\text{ resolves to Child's implementation at runtime via vtable}$$
2. **Interface Evolution (Java 8+):**
   Interfaces can declare concrete `default` and `static` methods without breaking existing implementing classes.""",
            "solved_examples": [
                {
                    "title": "Creating an Immutable Class in Java",
                    "difficulty": "Medium | Goldman Sachs, Amazon, Morgan Stanley",
                    "problem": "Design a fully thread-safe, immutable class containing a primitive and a mutable Date/List object.",
                    "step_by_step": [
                        "Step 1: Declare the class `final` so it cannot be subclassed.",
                        "Step 2: Make all fields `private` and `final`.",
                        "Step 3: Do not provide setter methods.",
                        "Step 4: Initialize all fields via constructor performing deep defensive copying of mutable arguments.",
                        "Step 5: Return defensive copies in getter methods to prevent external mutation."
                    ],
                    "code_or_math": """import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class ImmutableCandidate {
    private final int id;
    private final String name;
    private final List<String> skills; // Mutable list

    public ImmutableCandidate(int id, String name, List<String> skills) {
        this.id = id;
        this.name = name;
        // Defensive copy on construction
        this.skills = (skills != null) ? new ArrayList<>(skills) : new ArrayList<>();
    }

    public int getId() { return id; }
    public String getName() { return name; }
    
    // Return unmodifiable view or defensive copy
    public List<String> getSkills() {
        return Collections.unmodifiableList(skills);
    }
}""",
                    "explanation": "Because `skills` is defensively copied on entry and wrapped in `unmodifiableList` on exit, callers cannot mutate the internal state of `ImmutableCandidate`."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens if a subclass attempts to override a method marked `final` in the parent class?",
                    "options": [
                        "A) Code compiles but throws RuntimeException",
                        "B) Compilation error",
                        "C) Method is shadowed",
                        "D) Method is executed only in debug mode"
                    ],
                    "correct_answer": "B) Compilation error",
                    "detailed_solution": "The `final` keyword explicitly prevents method overriding at compile time."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "Why should you prefer Composition over Inheritance in enterprise software design?",
                    "model_answer": "Inheritance breaks encapsulation because child classes depend intimately on implementation details of parent classes (fragile base class problem). Changes in parent methods can inadvertently break subclass invariants. Composition (`HAS-A`) provides loose coupling: components interact strictly through public interfaces, allowing runtime substitution of implementations (Strategy Pattern) and simplified unit testing via mocking.",
                    "interviewer_tip": "Cite the Fragile Base Class problem and testability via dependency injection."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Java Memory Management, Garbage Collection & String Pool",
        "key_takeaways": "Master JVM generations (Eden, Survivor, Tenured), Garbage Collection algorithms (G1, ZGC), and String Pool immutability.",
        "topics": [
            "Generational Garbage Collection hypothesis: Young Gen (Eden, S0, S1) vs Old Gen",
            "GC Algorithms: Serial, Parallel, CMS, G1 (Garbage-First), and low-latency ZGC",
            "String Pool (interning), String vs StringBuilder vs StringBuffer",
            "Memory leaks in Java: Unclosed resources, static collections, and thread locals",
            "Weak, Soft, and Phantom references"
        ],
        "sections": {
            "concept": """Automatic memory management in Java relies on the **Weak Generational Hypothesis**: the empirical observation that most allocated objects have extremely short lifetimes and die shortly after creation.

The JVM Heap is split into generations:
1. **Young Generation:**
   - **Eden Space:** All newly instantiated objects arrive here.
   - **Survivor Spaces (S0 / S1):** Objects surviving a Minor GC are copied between Survivor spaces, incrementing an age counter.
2. **Old (Tenured) Generation:** Objects that survive a threshold number of Minor GC cycles (tenuring threshold, default 15) are promoted to the Old Generation. Major/Full GC sweeps the Old Generation.

**String Constant Pool:**
Strings are immutable in Java. Literals (`String s = \"test\"`) reside in the String Pool inside Heap memory, allowing multiple references to share the identical physical character array. Using `new String(\"test\")` forces the creation of a separate new object outside the pool.""",
            "formulas": """1. **String Comparison Invariant:**
   $$\"java\" == \"java\" \\implies \\text{TRUE (identical String Pool reference)}$$
   $$\"java\" == \\text{new String}(\"java\") \\implies \\text{FALSE (different heap addresses)}$$
   $$\\text{Always use: } s1.\\text{equals}(s2) \\text{ for logical value equality!}$$""",
            "solved_examples": [
                {
                    "title": "Diagnosing String Pool Allocation & intern() Method",
                    "difficulty": "Easy | Infosys, Wipro, TCS",
                    "problem": "Evaluate the output of string reference comparisons with and without intern().",
                    "step_by_step": [
                        "Step 1: `s1 = \"Hello\"` places literal in String Pool.",
                        "Step 2: `s2 = new String(\"Hello\")` allocates a new object in general Heap.",
                        "Step 3: `s3 = s2.intern()` looks up the pool; finds existing literal and returns pool address.",
                        "Step 4: `s1 == s2` is false (distinct addresses). `s1 == s3` is true."
                    ],
                    "code_or_math": """public class StringPoolDemo {
    public static void main(String[] args) {
        String s1 = "Hello";
        String s2 = new String("Hello");
        String s3 = s2.intern();

        System.out.println(s1 == s2);      // false (Pool vs General Heap)
        System.out.println(s1 == s3);      // true  (Both point to Pool object)
        System.out.println(s1.equals(s2)); // true  (Identical character sequence)
    }
}""",
                    "explanation": "The `intern()` method ensures that all identical strings return the canonical pooled reference, saving memory."
                }
            ],
            "practice_questions": [
                {
                    "question": "Which Garbage Collector is designed for multi-gigabyte heaps to maintain pause times under 10 milliseconds?",
                    "options": [
                        "A) Serial GC",
                        "B) Parallel GC",
                        "C) ZGC (Z Garbage Collector)",
                        "D) Mark-Sweep GC"
                    ],
                    "correct_answer": "C) ZGC (Z Garbage Collector)",
                    "detailed_solution": "ZGC performs all heavy GC work concurrently with running application threads using colored pointers and load barriers."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "Can a memory leak occur in Java despite automatic Garbage Collection? Give a realistic example.",
                    "model_answer": "Yes. A memory leak in Java occurs when an object is no longer needed by application logic, but an active, reachable reference from a GC root prevents the Garbage Collector from reclaiming it. Common examples: 1) Static collections that continually append objects without eviction. 2) Unregistered event listeners or callbacks. 3) Unclosed system resources (database connections, file streams). 4) Un-cleared ThreadLocal variables in pooled thread environments.",
                    "interviewer_tip": "Cite ThreadLocal leaks in web container thread pools (Tomcat)."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Exception Handling & Robust Error Architecture",
        "key_takeaways": "Master Checked vs Unchecked exceptions, try-catch-finally control flow, try-with-resources (AutoCloseable), and custom exception architecture.",
        "topics": [
            "Throwable hierarchy: Error vs Exception (Checked vs Unchecked/RuntimeException)",
            "try-catch-finally execution semantics and System.exit() behavior",
            "try-with-resources and AutoCloseable interface for leak prevention",
            "Custom domain exceptions and exception chaining (getCause())",
            "Exception anti-patterns: Swallowing exceptions and catch-all Exception blocks"
        ],
        "sections": {
            "concept": """Java uses exceptions to separate error-handling code from normal business logic. All errors derive from `java.lang.Throwable`:
- **Error:** Serious hardware or JVM problems (e.g., `OutOfMemoryError`, `StackOverflowError`) that applications should not attempt to catch.
- **Exception (Checked):** Subclasses of `Exception` excluding `RuntimeException`. Represents recoverable conditions (e.g., `IOException`, `SQLException`) enforced at compile time.
- **RuntimeException (Unchecked):** Programming bugs or logic errors (e.g., `NullPointerException`, `IndexOutOfBoundsException`, `IllegalArgumentException`).

`try-with-resources` automatically closes any object implementing `java.lang.AutoCloseable` at block termination, even when exceptions are thrown, eliminating `finally` cleanup boilerplate.""",
            "formulas": """1. **Throwable Hierarchy:**
   $$\\text{Throwable} \\implies \\begin{cases} \\text{Error (Unchecked, JVM level)} \\\\ \\text{Exception} \\implies \\begin{cases} \\text{RuntimeException (Unchecked)} \\\\ \\text{Checked Exceptions (Compile-time verified)} \\end{cases} \\end{cases}$$""",
            "solved_examples": [
                {
                    "title": "Automated Resource Management with try-with-resources",
                    "difficulty": "Easy | Amazon, TCS, Cognizant",
                    "problem": "Safely read the first line of a file using try-with-resources, guaranteeing resource deallocation.",
                    "step_by_step": [
                        "Step 1: Declare the `BufferedReader` inside the `try (...)` parentheses.",
                        "Step 2: Read line.",
                        "Step 3: The reader is automatically closed at the closing brace."
                    ],
                    "code_or_math": """import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ResourceSafety {
    public static String readFirstLine(String path) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            return br.readLine();
        } // br.close() is guaranteed to execute automatically here
    }
}""",
                    "explanation": "Replaces bulky try-catch-finally patterns and handles suppressed exceptions automatically if both block and close() throw."
                }
            ],
            "practice_questions": [
                {
                    "question": "When does a finally block NOT execute?",
                    "options": [
                        "A) When an unhandled RuntimeException is thrown",
                        "B) When a return statement is encountered in the try block",
                        "C) When System.exit(0) is called in the try block",
                        "D) When an OutOfMemoryError occurs"
                    ],
                    "correct_answer": "C) When System.exit(0) is called in the try block",
                    "detailed_solution": "System.exit() terminates the entire JVM process immediately, bypassing pending finally blocks."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft",
                    "question": "What is the difference between throw and throws in Java?",
                    "model_answer": "The `throw` keyword is used inside method bodies to explicitly instantiate and raise an exception object (`throw new IllegalArgumentException(...)`). The `throws` keyword is used in method signatures to declare to callers that this method may propagate checked exceptions, forcing the caller to either handle them with try-catch or declare them in its own throws clause.",
                    "interviewer_tip": "Be crisp: throw acts on an instance, throws acts on method declaration."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Java Collections Framework Deep Dive",
        "key_takeaways": "Master ArrayList vs LinkedList, HashMap internal collision resolution (hash buckets to Red-Black trees), ConcurrentHashMap, and Comparable vs Comparator.",
        "topics": [
            "Collection hierarchy: List, Set, Queue, Deque, Map",
            "ArrayList amortized resizing vs LinkedList node overhead",
            "HashMap internals: Hashing, bucket array, load factor (0.75), and treeification (Red-Black trees at threshold 8)",
            "ConcurrentHashMap: CAS (Compare-And-Swap) and synchronized bucket locks",
            "Comparable (natural order) vs Comparator (custom strategies)"
        ],
        "sections": {
            "concept": """The Java Collections Framework (JCF) provides unified data structures:
- **List:** Ordered collections allowing duplicates. `ArrayList` uses contiguous arrays for $O(1)$ index lookup. `LinkedList` uses doubly-linked nodes with higher memory overhead.
- **Set:** Unique elements. `HashSet` uses an internal `HashMap` where values are dummy sentinels. `TreeSet` uses Red-Black tree for $O(\\log n)$ sorted order.
- **Map:** Key-value pairs. `HashMap` computes bucket index via `(n - 1) & hash(key)`. When multiple keys map to the same bucket, elements chain as linked lists. If bucket length exceeds 8 and total map capacity $\\ge 64$, the bucket treeifies into a Red-Black tree, improving worst-case search from $O(n)$ to $O(\\log n)$.""",
            "formulas": """1. **HashMap Bucket Index Formula:**
   $$\\text{index} = (\\text{capacity} - 1) \\ \\&\\ \\text{hash}(key)$$
2. **Threshold for Resizing:**
   $$\\text{Threshold} = \\text{Capacity} \\times \\text{Load Factor (default 0.75)}$$""",
            "solved_examples": [
                {
                    "title": "Sorting Objects with Multiple Comparator Criteria",
                    "difficulty": "Easy | Amazon, TCS, Infosys",
                    "problem": "Sort candidates primarily by score descending, and secondarily by name ascending.",
                    "step_by_step": [
                        "Step 1: Use `Comparator.comparingInt(...).reversed()` for score descending.",
                        "Step 2: Chain `.thenComparing(...)` for name alphabetical ascending.",
                        "Step 3: Invoke `candidates.sort(...)`."
                    ],
                    "code_or_math": """import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Candidate {
    String name;
    int score;
    Candidate(String n, int s) { name = n; score = s; }
}

public class SortDemo {
    public static void main(String[] args) {
        List<Candidate> list = new ArrayList<>();
        list.add(new Candidate("Alice", 85));
        list.add(new Candidate("Bob", 92));
        list.add(new Candidate("Charlie", 85));

        list.sort(Comparator.comparingInt((Candidate c) -> c.score)
                            .reversed()
                            .thenComparing(c -> c.name));
    }
}""",
                    "explanation": "Chaining comparators creates concise, readable sorting strategies without implementing legacy verbose comparator classes."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the contract between equals() and hashCode() in Java?",
                    "options": [
                        "A) If hashCode() is equal, equals() must return true",
                        "B) If equals() returns true, hashCode() must return identical values for both objects",
                        "C) They operate independently",
                        "D) hashCode() is only used in lists"
                    ],
                    "correct_answer": "B) If equals() returns true, hashCode() must return identical values for both objects",
                    "detailed_solution": "If two objects are logically equal via equals(), they must produce identical hash codes so hash-based collections place them in the same bucket."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "How does ConcurrentHashMap achieve thread safety without locking the entire map like Hashtable?",
                    "model_answer": "Legacy Hashtable uses synchronized methods that lock the entire table for every read and write. ConcurrentHashMap uses fine-grained locking: reads are completely lock-free via volatile memory reads. Writes use Lock-Free Compare-And-Swap (CAS) to insert nodes into empty buckets, and lock only the single head node of the target bucket (`synchronized (node)`) when chaining into collisions. This allows concurrent writes across different buckets.",
                    "interviewer_tip": "Contrast segment locking (Java 7) with CAS + bucket node synchronization (Java 8+)."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Java Generics, Reflection & Annotations",
        "key_takeaways": "Master type safety, type erasure, PECS rule (Producer Extends, Consumer Super), Reflection API, and custom runtime annotations.",
        "topics": [
            "Generics type safety and compile-time verification",
            "Type Erasure: How bytecode preserves backwards compatibility",
            "Wildcards: Upper bounded (? extends T) vs Lower bounded (? super T)",
            "PECS Rule: Producer Extends, Consumer Super",
            "Reflection API and custom annotations with RetentionPolicy.RUNTIME"
        ],
        "sections": {
            "concept": """Generics provide compile-time type safety, eliminating runtime `ClassCastException` hazards. 

**Type Erasure:**
To ensure backwards compatibility with pre-generic Java versions, the Java compiler enforces generic type checks at compile-time and then erases all type parameters, substituting raw types or boundary types in generated bytecode.

**PECS Rule:**
- **Producer Extends (`? extends T`):** Use when you only READ elements from the collection.
- **Consumer Super (`? super T`):** Use when you WRITE elements into the collection.""",
            "formulas": """1. **PECS Mnemonic:**
   $$\\text{Producer Extends (READ ONLY)} \\iff \\text{List<? extends Number> list}$$
   $$\\text{Consumer Super (WRITE ALLOWED)} \\iff \\text{List<? super Integer> list}$$""",
            "solved_examples": [
                {
                    "title": "Applying PECS to Generic Collections Copy",
                    "difficulty": "Medium | Google, Oracle",
                    "problem": "Write a generic copy method that transfers numbers from a source list to a destination list.",
                    "step_by_step": [
                        "Step 1: Source produces data: `List<? extends T> src`.",
                        "Step 2: Destination consumes data: `List<? super T> dest`.",
                        "Step 3: Iterate and add."
                    ],
                    "code_or_math": """import java.util.List;

public class GenericsHelper {
    public static <T> void copy(List<? super T> dest, List<? extends T> src) {
        for (T item : src) {
            dest.add(item);
        }
    }
}""",
                    "explanation": "Guarantees complete compile-time type safety allowing flexible inheritance hierarchies."
                }
            ],
            "practice_questions": [
                {
                    "question": "Can you instantiate a generic array directly such as `T[] arr = new T[10];`?",
                    "options": [
                        "A) Yes",
                        "B) No, because of Type Erasure the exact component type is not known at runtime",
                        "C) Only for Integer types",
                        "D) Yes, if marked public"
                    ],
                    "correct_answer": "B) No, because of Type Erasure the exact component type is not known at runtime",
                    "detailed_solution": "Arrays require reified runtime type information, which conflicts with generic type erasure."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "Explain Type Erasure and its consequences in Java.",
                    "model_answer": "Type Erasure replaces all generic type parameters with their bounds (or `Object` if unbounded) and inserts explicit casts where necessary in bytecode. Consequences: 1) You cannot use `instanceof` with generic types (`list instanceof List<String>` is illegal). 2) You cannot create instances of type parameters (`new T()`). 3) You cannot create generic arrays (`new T[10]`).",
                    "interviewer_tip": "Cite backwards compatibility with Java 1.4 as the engineering rationale."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Multithreading, Concurrency & Java Memory Model",
        "key_takeaways": "Master thread lifecycle, synchronized, volatile visibility, Deadlocks, ExecutorService thread pools, and ReentrantLock.",
        "topics": [
            "Thread lifecycle: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED",
            "Java Memory Model: Main Memory, CPU Caches, and the volatile keyword",
            "Synchronization: Intrinsic locks (monitors), synchronized methods, and reentrancy",
            "Deadlock conditions and prevention strategies",
            "ExecutorService, ThreadPoolExecutor, Callable, and Future"
        ],
        "sections": {
            "concept": """Multithreading executes concurrent paths of execution within the same process, sharing Heap memory. 

**Java Memory Model (JMM) & `volatile`:**
CPUs retain local L1/L2 caches. If Thread A modifies a shared variable, the new value may reside in CPU cache without writing to Main Memory, leaving Thread B with a stale copy. Marking a variable `volatile` guarantees **Visibility** (all reads and writes bypass local caches directly to Main Memory) and establishes a **Happens-Before** relationship, preventing instruction reordering. It does NOT guarantee atomicity for compound operations like `count++`.

**Thread Pools:**
Managing raw threads causes high overhead. `ExecutorService` pools reusable worker threads via blocking task queues (`LinkedBlockingQueue`).""",
            "formulas": """1. **Deadlock Conditions (Coffman Conditions):**
   $$\\text{Mutual Exclusion} \\land \\text{Hold and Wait} \\land \\text{No Preemption} \\land \\text{Circular Wait}$$
2. **Volatile vs Synchronized:**
   $$\\text{volatile} = \\text{Visibility only (Zero lock overhead)}$$
   $$\\text{synchronized} = \\text{Visibility} + \\text{Mutual Exclusion Atomicity}$$""",
            "solved_examples": [
                {
                    "title": "Thread-Safe Singleton with Double-Checked Locking",
                    "difficulty": "Medium | Amazon, Microsoft, Uber",
                    "problem": "Implement a thread-safe, lazy-initialized Singleton in Java.",
                    "step_by_step": [
                        "Step 1: Declare constructor private.",
                        "Step 2: Declare static instance as `private static volatile`.",
                        "Step 3: Check null twice: once without lock, then inside synchronized block."
                    ],
                    "code_or_math": """public class ThreadSafeSingleton {
    private static volatile ThreadSafeSingleton instance;

    private ThreadSafeSingleton() {}

    public static ThreadSafeSingleton getInstance() {
        if (instance == null) { // 1st check (no locking overhead)
            synchronized (ThreadSafeSingleton.class) {
                if (instance == null) { // 2nd check (under lock)
                    instance = new ThreadSafeSingleton();
                }
            }
        }
        return instance;
    }
}""",
                    "explanation": "The `volatile` modifier is strictly required to prevent instruction reordering where a partially constructed object reference is published."
                }
            ],
            "practice_questions": [
                {
                    "question": "Does `volatile` guarantee atomicity for `count++`?",
                    "options": [
                        "A) Yes",
                        "B) No, because count++ consists of 3 distinct bytecode operations: read, modify, write",
                        "C) Only on 64-bit JVMs",
                        "D) Yes, if count is an integer"
                    ],
                    "correct_answer": "B) No, because count++ consists of 3 distinct bytecode operations: read, modify, write",
                    "detailed_solution": "Use `AtomicInteger` with CAS (Compare-And-Swap) for atomic increments."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is the difference between Callable and Runnable?",
                    "model_answer": "Runnable's `run()` method returns void and cannot throw checked exceptions. Callable's `call()` method returns a generic parameterized result (`Future<V>`) and can throw checked exceptions.",
                    "interviewer_tip": "Mention pairing Callable with ExecutorService and Future.get()."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Java 8+ Functional Programming & Streams API",
        "key_takeaways": "Master Lambda expressions, Functional Interfaces (@FunctionalInterface), Streams API (map, filter, reduce), and Optional pattern.",
        "topics": [
            "Functional interfaces: Function, Predicate, Consumer, Supplier",
            "Lambda syntax and lexical scoping (effectively final variables)",
            "Streams API pipeline: Source -> Intermediate Operations (lazy) -> Terminal Operation (eager)",
            "Collectors: groupingBy, partitioningBy, joining, and toMap",
            "Optional<T> best practices for eliminating NullPointerException"
        ],
        "sections": {
            "concept": """Java 8 introduced functional programming concepts to declarative data processing:
- **Functional Interface:** Interface with exactly one abstract method (SAM), annotated with `@FunctionalInterface`.
- **Lambda Expressions:** Anonymous functions passed as data. Can access local variables from enclosing scopes only if they are `final` or effectively final.
- **Streams API:** Computations on collections using lazy execution pipelines. Intermediate operations (e.g., `filter()`, `map()`, `sorted()`) do not execute until a Terminal Operation (e.g., `collect()`, `reduce()`, `count()`) is invoked.""",
            "formulas": """1. **Stream Pipeline Structure:**
   $$\\text{Collection} \\to \\text{.stream()} \\to \\text{filter/map (Lazy Intermediate)} \\to \\text{.collect() (Eager Terminal)}$$""",
            "solved_examples": [
                {
                    "title": "Group Employees by Department and Calculate Average Salary",
                    "difficulty": "Easy | Amazon, TCS Digital",
                    "problem": "Given a list of Employees, group them by department name and compute average salary per department.",
                    "step_by_step": [
                        "Step 1: Convert list to stream.",
                        "Step 2: Collect using `Collectors.groupingBy()` with downstream collector `Collectors.averagingDouble()`."
                    ],
                    "code_or_math": """import java.util.*;
import java.util.stream.Collectors;

class Emp {
    String dept;
    double sal;
    Emp(String d, double s) { dept = d; sal = s; }
    public String getDept() { return dept; }
    public double getSal() { return sal; }
}

public class StreamDemo {
    public static Map<String, Double> avgSalaryByDept(List<Emp> emps) {
        return emps.stream()
                   .collect(Collectors.groupingBy(
                       Emp::getDept,
                       Collectors.averagingDouble(Emp::getSal)
                   ));
    }
}""",
                    "explanation": "Executes in a single pass over the collection with clean, declarative syntax."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens if you invoke multiple terminal operations on the same Stream instance?",
                    "options": [
                        "A) It recalculates results",
                        "B) Throws IllegalStateException: stream has already been operated upon or closed",
                        "C) Returns empty stream",
                        "D) Automatically resets"
                    ],
                    "correct_answer": "B) Throws IllegalStateException: stream has already been operated upon or closed",
                    "detailed_solution": "Streams are single-use traversals that cannot be reused once consumed."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "Why should Optional<T> not be used as method parameters or class fields?",
                    "model_answer": "Optional is designed strictly as a method return type to signal the possible absence of a value without returning null. Using Optional as method parameters forces callers to wrap values unnecessarily (`Optional.of(val)`) and does not prevent callers from passing `null` into the Optional parameter itself. Furthermore, `Optional` does not implement `Serializable`, which breaks serialization frameworks when used as class fields.",
                    "interviewer_tip": "Cite Brian Goetz's design guidelines for Optional."
                }
            ]
        }
    },
    {
        "chapter_num": 9,
        "title": "I/O Streams, Serialization & Modern Networking",
        "key_takeaways": "Master Byte streams vs Character streams, Buffering, Java Serialization mechanics, serialVersionUID, and Non-blocking NIO.2.",
        "topics": [
            "Byte streams (InputStream/OutputStream) vs Character streams (Reader/Writer)",
            "Buffered streams and I/O performance optimization",
            "Java Serialization, transient keyword, and serialVersionUID validation",
            "NIO.2: Path, Files, Channels, and Buffers",
            "Socket programming and non-blocking I/O (NIO Selectors)"
        ],
        "sections": {
            "concept": """Java I/O handles streaming data:
- **Byte Streams:** Process raw binary data (images, compiled classes, audio) 8 bits at a time.
- **Character Streams:** Automatically handle character encoding/decoding (UTF-8) 16 bits at a time.
- **Serialization:** Converting active in-memory object graphs into byte streams for disk persistence or network transmission (`implements Serializable`). Marking a field `transient` prevents it from being serialized.""",
            "formulas": """1. **serialVersionUID Invariant:**
   If `serialVersionUID` in serialized stream does not match class loader version:
   $$\\implies \\text{Throws InvalidClassException}$$""",
            "solved_examples": [
                {
                    "title": "High-Performance File Copying with NIO.2 Files.copy()",
                    "difficulty": "Easy | Infosys, TCS",
                    "problem": "Copy a file safely utilizing modern NIO.2 APIs with replacement.",
                    "step_by_step": [
                        "Step 1: Obtain `Path` instances via `Path.of()`.",
                        "Step 2: Use `Files.copy()` with `StandardCopyOption.REPLACE_EXISTING`."
                    ],
                    "code_or_math": """import java.nio.file.*;
import java.io.IOException;

public class FileCopyDemo {
    public static void copyFile(String src, String dest) throws IOException {
        Path srcPath = Path.of(src);
        Path destPath = Path.of(dest);
        Files.copy(srcPath, destPath, StandardCopyOption.REPLACE_EXISTING);
    }
}""",
                    "explanation": "Leverages operating-system-level zero-copy file transfer primitives where available."
                }
            ],
            "practice_questions": [
                {
                    "question": "What does the transient keyword signify on an instance variable?",
                    "options": [
                        "A) It is thread-safe",
                        "B) It is omitted from the object's serialized byte stream",
                        "C) It cannot be modified",
                        "D) It is stored in Metaspace"
                    ],
                    "correct_answer": "B) It is omitted from the object's serialized byte stream",
                    "detailed_solution": "Transient fields are skipped during default serialization and reset to default values upon deserialization."
                }
            ],
            "interview_questions": [
                {
                    "company": "Oracle",
                    "question": "Why should every Serializable class explicitly declare a private static final long serialVersionUID?",
                    "model_answer": "If a class does not explicitly declare `serialVersionUID`, the JVM runtime calculates a default hash based on class structure, fields, and method signatures. Even minor modifications (such as changing a method name or adding a private field) alter this computed hash, causing previously serialized objects to fail deserialization with an `InvalidClassException`. Declaring an explicit `serialVersionUID` guarantees version compatibility across compiler versions.",
                    "interviewer_tip": "Explain that it maintains cross-version backwards compatibility."
                }
            ]
        }
    },
    {
        "chapter_num": 10,
        "title": "Java Placement Coding Patterns & Enterprise Architecture",
        "key_takeaways": "Master top enterprise design patterns (Factory, Builder, Strategy, Observer) and technical placement coding rounds.",
        "topics": [
            "Creational Patterns: Builder pattern with fluent API and Factory method",
            "Behavioral Patterns: Strategy and Observer patterns in Spring architectures",
            "Dependency Injection and Inversion of Control (IoC) fundamentals",
            "Placement coding drills: LRU Cache in Java, Custom ThreadPool, and Concurrent Queue",
            "Senior placement interview communication and code review best practices"
        ],
        "sections": {
            "concept": """This capstone chapter covers enterprise architecture and structural design patterns tested in technical interviews:
- **Builder Pattern:** Separates complex object construction from its representation, providing fluent, readable object configuration without telescoping constructors.
- **Factory Pattern:** Defines an interface for object creation, delegating instantiation to specialized subclasses.
- **Strategy Pattern:** Defines a family of algorithms, encapsulating each one, making them interchangeable at runtime.
- **Dependency Injection (DI):** Objects receive their dependencies from an external assembler (such as the Spring IoC container) rather than instantiating dependencies internally via `new`.""",
            "formulas": """1. **Builder Pattern Fluent Structure:**
   $$\\text{User } u = \\text{User.builder}().\\text{name}(\"Alice\").\\text{email}(\"a@test.com\").\\text{build}();$$""",
            "solved_examples": [
                {
                    "title": "Builder Pattern Implementation with Fluent API",
                    "difficulty": "Medium | Amazon, Google, Flipkart",
                    "problem": "Implement the Builder pattern for a `HttpRequest` configuration object.",
                    "step_by_step": [
                        "Step 1: Private constructor taking static inner `Builder` class.",
                        "Step 2: Static `builder()` method returning new `Builder`.",
                        "Step 3: Fluent setter methods on `Builder` returning `this`.",
                        "Step 4: `build()` method returning validated `HttpRequest`."
                    ],
                    "code_or_math": """public class HttpRequest {
    private final String url;
    private final String method;
    private final int timeoutMs;

    private HttpRequest(Builder builder) {
        this.url = builder.url;
        this.method = builder.method;
        this.timeoutMs = builder.timeoutMs;
    }

    public static class Builder {
        private String url;
        private String method = "GET"; // Default
        private int timeoutMs = 5000;  // Default

        public Builder url(String url) { this.url = url; return this; }
        public Builder method(String method) { this.method = method; return this; }
        public Builder timeoutMs(int timeoutMs) { this.timeoutMs = timeoutMs; return this; }

        public HttpRequest build() {
            if (url == null) throw new IllegalStateException("URL is mandatory");
            return new HttpRequest(this);
        }
    }
}""",
                    "explanation": "Provides immutable object construction with clean, readable parameter configuration."
                }
            ],
            "practice_questions": [
                {
                    "question": "Which design pattern is utilized when passing a Comparator lambda to `list.sort()`?",
                    "options": [
                        "A) Singleton Pattern",
                        "B) Strategy Pattern",
                        "C) Decorator Pattern",
                        "D) Prototype Pattern"
                    ],
                    "correct_answer": "B) Strategy Pattern",
                    "detailed_solution": "The sorting algorithm remains fixed while the comparison strategy is supplied interchangeably at runtime."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is Inversion of Control (IoC) and how does Dependency Injection realize it?",
                    "model_answer": "In traditional programming, high-level components control execution flow by directly instantiating their low-level dependencies using `new`. Inversion of Control inverts this control: an external container manages component lifecycles. Dependency Injection is the mechanism realizing IoC: instead of a class looking up or instantiating its dependencies, the dependencies are injected into the class via constructors, setters, or fields at runtime.",
                    "interviewer_tip": "Connect IoC to decoupling and simplified unit testing."
                }
            ]
        }
    }
]

