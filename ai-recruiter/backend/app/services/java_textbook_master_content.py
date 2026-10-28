"""
java_textbook_master_content.py — Complete Prescribed Campus Placement Textbook for Java Programming.
Covers the entire Java language from foundational basics to JVM internals, OOP architecture,
concurrency, modern Java 21 LTS features, and campus placement interview scenarios.
"""

JAVA_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Java Architecture, JVM Internals & Memory Model",
        "topics": [
            "JDK vs JRE vs JVM architectural relationships",
            "Bytecode compilation (.java -> .class) & JIT Tiered Compilation (C1/C2)",
            "ClassLoader subsystem (Bootstrap, Platform, Application & Delegation Model)",
            "JVM Memory Areas (Heap, Thread Stack, Metaspace, PC Registers, Native Stacks)",
            "Garbage Collection mechanics (Generational Hypothesis, Minor vs Full GC, G1 & ZGC)",
            "Memory leak diagnosis & JVM diagnostic flags (-Xms, -Xmx, -XX:+HeapDumpOnOutOfMemoryError)"
        ],
        "key_takeaways": "Java achieves platform independence via bytecode executed on platform-specific JVMs. Stack stores thread-local execution frames; Heap manages all dynamically allocated object instances subject to Garbage Collection. Metaspace in native memory holds class metadata."
    },
    {
        "chapter_num": 2,
        "title": "Primitive Data Types, Operators & Modern Control Flow",
        "topics": [
            "8 Primitive types, bit widths, ranges, and IEEE 754 floating point precision",
            "Widening (implicit) vs narrowing (explicit) type casting with overflow boundaries",
            "Bitwise operators (&, |, ^, ~, <<, >>, >>> unsigned right shift)",
            "Short-circuit (&&, ||) vs non-short-circuit (&, |) logical evaluation",
            "Enhanced switch expressions (Java 14+) with arrow syntax, multiple case labels, and yield statements",
            "Loops (for, enhanced for-each, while, do-while) and labeled jump control"
        ],
        "key_takeaways": "Narrowing casts truncate high-order bits without runtime warning. Short-circuit operators prevent right-hand evaluation when the outcome is guaranteed. Enhanced switch expressions guarantee exhaustive matching and eliminate break statement fallthrough bugs."
    },
    {
        "chapter_num": 3,
        "title": "Object-Oriented Programming (OOP) Deep Dive & Object Lifecycle",
        "topics": [
            "The 4 OOP Pillars (Encapsulation, Inheritance, Polymorphism, Abstraction)",
            "Constructor mechanics, default constructors, and chaining via this() and super()",
            "Static initialization blocks, instance initialization blocks, and initialization order",
            "Dynamic Method Dispatch, method overriding vs overloading, covariant return types",
            "Abstract classes vs modern Interfaces (default, static, and private methods)",
            "The 'final' keyword on variables, methods, and classes",
            "Access modifiers matrix (private, package-private default, protected, public)",
            "java.lang.Object contracts (equals, hashCode, toString, clone, shallow vs deep copy)"
        ],
        "key_takeaways": "Overriding equals() strictly requires overriding hashCode() to preserve Hash collection contracts. Dynamic method dispatch resolves method calls at runtime using the object's virtual method table (vtable). Final classes prevent subclassing; final methods prevent overriding."
    },
    {
        "chapter_num": 4,
        "title": "String Architecture, Immutability & Memory Pooling",
        "topics": [
            "String immutability rationale (Security, HashCode caching, Thread safety, ClassLoader security)",
            "String Constant Pool (SCP) in Heap memory: literals vs new String() objects",
            "String interning via String.intern() and memory deduplication",
            "String vs StringBuilder (unsynchronized, high speed) vs StringBuffer (synchronized, thread-safe)",
            "Performance consequences of string concatenation (+) in loops (O(N^2) memory churn)",
            "Modern String utility methods (strip, lines, repeat, isBlank, formatted)"
        ],
        "key_takeaways": "String literals point to shared SCP entries; 'new String()' allocates distinct Heap objects. Always use StringBuilder for iterative concatenation in loops. String immutability enables stable hash codes essential for Map keys."
    },
    {
        "chapter_num": 5,
        "title": "Arrays, Wrapper Classes & Number Systems",
        "topics": [
            "Single, multidimensional, and jagged arrays memory layout",
            "java.util.Arrays utility algorithms (sort, binarySearch, copyOf, deepEquals)",
            "Primitive wrappers (Integer, Long, Double, etc.) and Autoboxing / Unboxing",
            "IntegerCache trap (-128 to 127) and identity (==) vs equality (equals) checks",
            "Arbitrary precision arithmetic: BigInteger and BigDecimal for financial accuracy"
        ],
        "key_takeaways": "Arrays in Java are first-class Heap objects with immutable length. Autoboxing caches Integer instances between -128 and 127; comparing boxed values outside this range with == checks reference identity and yields false. Use BigDecimal for non-floating-point financial logic."
    },
    {
        "chapter_num": 6,
        "title": "Exception Handling Architecture & Robust Design",
        "topics": [
            "Throwable class hierarchy: Error vs Exception",
            "Checked exceptions (IOException, SQLException) vs Unchecked exceptions (RuntimeException)",
            "try-catch-finally execution semantics and finally block execution guarantees",
            "try-with-resources statement & AutoCloseable interface for automatic resource management",
            "Multi-catch syntax, rethrowing exceptions, and custom exception design",
            "Exception anti-patterns: catching Throwable, swallowed exceptions, losing root cause"
        ],
        "key_takeaways": "Checked exceptions must be declared in method signatures or caught. Try-with-resources closes resources in reverse declaration order before any catch/finally blocks execute. Finally executes even if try returns, unless System.exit() halts the JVM."
    },
    {
        "chapter_num": 7,
        "title": "Java Collections Framework (JCF) & Internal Data Structures",
        "topics": [
            "Collection hierarchy: Iterable -> Collection -> List, Set, Queue, and Map",
            "ArrayList (dynamic array, 1.5x growth factor) vs LinkedList (doubly-linked nodes)",
            "HashSet (HashMap backed, O(1) avg) vs LinkedHashSet (insertion order) vs TreeSet (Red-Black tree, O(log N))",
            "PriorityQueue (binary Min-Heap) vs ArrayDeque (double-ended circular buffer)",
            "HashMap internal architecture: bucket table, hash spreading, (n-1)&hash indexing",
            "Collision handling: separate chaining and Treeification (threshold 8, min capacity 64 to Red-Black tree)",
            "LinkedHashMap (access-order LRU cache) and TreeMap (sorted keys)",
            "ConcurrentHashMap: CAS + synchronized bucket head locking, null key/value prohibition",
            "Comparable<T> (natural order) vs Comparator<T> (flexible external strategies)"
        ],
        "key_takeaways": "HashMap indexes buckets with (n - 1) & hash where n is power of two. When bucket collisions reach 8 with table capacity >= 64, buckets treeify into Red-Black trees to protect against O(N) hash flood attacks. ConcurrentHashMap offers thread safety without global table locking."
    },
    {
        "chapter_num": 8,
        "title": "Generics, Type Safety & Type Erasure",
        "topics": [
            "Generic classes, generic interfaces, and generic methods",
            "Compile-time type verification and elimination of runtime ClassCastException",
            "Type Erasure: bytecode transformation to raw types or upper bounds, bridge methods",
            "Bounded type parameters (<T extends Number & Comparable<T>>)",
            "Wildcards: Unbounded (?), Upper-bounded (? extends T), Lower-bounded (? super T)",
            "The PECS Rule: Producer Extends, Consumer Super",
            "Generic restrictions: primitive type restriction, no 'new T()', no generic array creation"
        ],
        "key_takeaways": "Generics are enforced at compile time and erased by the compiler for backward compatibility. Use 'extends' when reading data from a collection (Producer); use 'super' when writing elements into a collection (Consumer)."
    },
    {
        "chapter_num": 9,
        "title": "Multithreading, Concurrency & Thread Synchronization",
        "topics": [
            "Process vs Thread, thread lifecycle states (NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED)",
            "Thread creation: Thread class vs Runnable interface vs Callable<V> & Future<V>",
            "Intrinsic locks (monitors), synchronized methods, and synchronized statement blocks",
            "Inter-thread communication: wait(), notify(), notifyAll() monitor rules",
            "The 'volatile' keyword: CPU cache flushing, JMM happens-before, atomicity limitations",
            "Lock-free concurrency: java.util.concurrent.atomic (AtomicInteger, CAS instructions)",
            "High-level concurrency: ReentrantLock, CountDownLatch, CyclicBarrier, Semaphore",
            "ExecutorService & ThreadPoolExecutor architecture (corePoolSize, maxPoolSize, workQueue, rejection policies)",
            "Producer-Consumer pattern implementation with BlockingQueue"
        ],
        "key_takeaways": "Volatile guarantees visibility of memory writes across CPU cores but does NOT make compound operations like count++ atomic. Synchronized provides both mutual exclusion and memory visibility. Use ThreadPoolExecutor over manually spawning unmanaged raw threads."
    },
    {
        "chapter_num": 10,
        "title": "Lambdas, Functional Interfaces & Modern Stream API",
        "topics": [
            "Functional programming paradigms in Java: first-class behavior parameterization",
            "@FunctionalInterface annotation & Single Abstract Method (SAM) contract",
            "Core built-in interfaces: Predicate<T>, Function<T,R>, Consumer<T>, Supplier<T>, BiFunction",
            "Method references: Class::staticMethod, instance::method, Class::method, Class::new",
            "Stream API architecture: lazy evaluation, non-mutating pipelines, single-pass consumption",
            "Intermediate operations (filter, map, flatMap, distinct, sorted, peek, limit, skip)",
            "Terminal operations (collect, reduce, forEach, count, anyMatch, allMatch, findFirst)",
            "Collectors utility: toList, toSet, toMap, groupingBy, partitioningBy, joining, summarizingInt",
            "Optional<T> class best practices for eliminating NullPointerException",
            "Parallel streams: ForkJoinPool.commonPool() and concurrent performance caveats"
        ],
        "key_takeaways": "Streams process elements lazily; intermediate steps execute only when a terminal operation triggers the pipeline. Optional is intended as a method return type to represent potential absence of a value, not as a field or method parameter."
    },
    {
        "chapter_num": 11,
        "title": "Java I/O, NIO.2 & Object Serialization",
        "topics": [
            "Classic I/O: Byte Streams (InputStream/OutputStream) vs Character Streams (Reader/Writer)",
            "Buffered streams and performance optimization (BufferedReader, BufferedWriter)",
            "Java NIO.2 (java.nio.file): Path, Paths, and Files high-performance utility methods",
            "Object Serialization: Serializable marker interface, ObjectOutputStream / ObjectInputStream",
            "serialVersionUID role in preventing InvalidClassException across versions",
            "The 'transient' keyword: excluding sensitive fields from serialized state"
        ],
        "key_takeaways": "Always use buffered streams or NIO.2 Files utility for file operations. Any class implementing Serializable must declare an explicit private static final long serialVersionUID to guard against incompatible class definitions."
    },
    {
        "chapter_num": 12,
        "title": "Modern Java Features (Java 9 through Java 21 LTS)",
        "topics": [
            "Java 9 Module System (JPMS) and immutable collection factory methods (List.of, Map.of)",
            "Java 10 Local Variable Type Inference with 'var' keyword rules and restrictions",
            "Java 14/15 Text Blocks (\"\"\" ... \"\"\") for clean multiline strings",
            "Java 16 Records (record Point(int x, int y) {}): immutable data classes",
            "Java 17 Sealed Classes & Interfaces: permits clause and domain modeling",
            "Java 21 Virtual Threads (Project Loom): lightweight fibers scheduled by JVM on carrier threads",
            "Java 21 Pattern Matching for switch and Record Patterns",
            "Java 21 Sequenced Collections (SequencedCollection, SequencedSet, SequencedMap)"
        ],
        "key_takeaways": "Records eliminate boilerplate for immutable data-carrier classes. Virtual Threads permit millions of concurrent lightweight tasks on standard blocking I/O code without thread pool exhaustion. Pattern matching switch expressions guarantee compile-time exhaustiveness on sealed hierarchies."
    },
    {
        "chapter_num": 13,
        "title": "Placement Interview Puzzles, Memory Leaks & Design Patterns",
        "topics": [
            "Top 20 tricky Java output puzzles (Static initialization order, overloading with null, autoboxing traps)",
            "Detecting and fixing memory leaks in Java (unclosed streams, static collections, listener leaks)",
            "JVM Heap tuning flags and reading OutOfMemoryError heap dumps",
            "Singleton Pattern: Bill Pugh Holder Singleton vs Double-Checked Locking with volatile",
            "Factory and Builder Patterns for robust object construction",
            "Observer and Strategy Patterns implemented using modern Java functional interfaces"
        ],
        "key_takeaways": "Memory leaks in Java occur when unused objects remain reachable through live GC roots (such as static variables or uncleared collections). Always use volatile with Double-Checked Locking Singleton to prevent instruction reordering hazards."
    }
]

COMPLETE_JAVA_TEXTBOOK_MARKDOWN = r"""# Core Java Programming & Placement Foundations (Prescribed Master Textbook)

**Edition:** 2026 Comprehensive Campus Placement Edition  
**Subject:** Java Programming Language  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, topic practice quizzes, coding labs, and technical interview simulations on this website are strictly grounded in the concepts, code implementations, and architectural principles detailed in this textbook. Study this book to achieve 100% placement readiness.

---

## 📑 Complete Table of Contents

- [Chapter 1: Java Architecture, JVM Internals & Memory Model](#chapter-1-java-architecture-jvm-internals--memory-model)
- [Chapter 2: Primitive Types, Operators & Modern Control Flow](#chapter-2-primitive-types-operators--modern-control-flow)
- [Chapter 3: Object-Oriented Programming (OOP) Deep Dive & Object Lifecycle](#chapter-3-object-oriented-programming-oop-deep-dive--object-lifecycle)
- [Chapter 4: String Architecture, Immutability & Memory Pooling](#chapter-4-string-architecture-immutability--memory-pooling)
- [Chapter 5: Arrays, Wrapper Classes & Number Systems](#chapter-5-arrays-wrapper-classes--number-systems)
- [Chapter 6: Exception Handling Architecture & Robust Design](#chapter-6-exception-handling-architecture--robust-design)
- [Chapter 7: Java Collections Framework (JCF) & Internal Data Structures](#chapter-7-java-collections-framework-jcf--internal-data-structures)
- [Chapter 8: Generics, Type Safety & Type Erasure](#chapter-8-generics-type-safety--type-erasure)
- [Chapter 9: Multithreading, Concurrency & Thread Synchronization](#chapter-9-multithreading-concurrency--thread-synchronization)
- [Chapter 10: Lambdas, Functional Interfaces & Modern Stream API](#chapter-10-lambdas-functional-interfaces--modern-stream-api)
- [Chapter 11: Java I/O, NIO.2 & Object Serialization](#chapter-11-java-io-nio2--object-serialization)
- [Chapter 12: Modern Java Features (Java 9 through Java 21 LTS)](#chapter-12-modern-java-features-java-9-through-java-21-lts)
- [Chapter 13: Placement Interview Puzzles, Memory Leaks & Design Patterns](#chapter-13-placement-interview-puzzles-memory-leaks--design-patterns)

---

## Chapter 1: Java Architecture, JVM Internals & Memory Model

### 1.1 The JDK, JRE, and JVM Triad
Java's core architecture follows the "Write Once, Run Anywhere" (WORA) philosophy. Understanding the separation between development tools, execution environments, and the virtual machine is vital for every placement candidate:

1. **JDK (Java Development Kit):** The complete software development bundle containing the Java Compiler (`javac`), debugger (`jdb`), archiver (`jar`), diagnostic tools (`jps`, `jstat`, `jstack`), and the JRE.
2. **JRE (Java Runtime Environment):** The runtime execution bundle containing the JVM implementation alongside core standard libraries (`java.base`, `rt.jar`) required to execute compiled bytecode.
3. **JVM (Java Virtual Machine):** The abstract computing machine with its own instruction set that interprets or compiles bytecode into native machine instructions on the host CPU.

```
+-------------------------------------------------------------------+
|                        Java Development Kit (JDK)                 |
|  [javac, jdb, jstat, jcmd, jar, javadoc tools]                    |
|  +-------------------------------------------------------------+  |
|  |                  Java Runtime Environment (JRE)             |  |
|  |  [Standard Class Libraries: java.lang, java.util, java.io]  |  |
|  |  +-------------------------------------------------------+  |  |
|  |  |             Java Virtual Machine (JVM)                |  |  |
|  |  |  ClassLoader | Runtime Data Areas | Execution Engine  |  |  |
|  |  +-------------------------------------------------------+  |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```

### 1.2 The ClassLoader Subsystem
When a Java program starts, classes are dynamically loaded into JVM memory by the **ClassLoader Subsystem** following a three-phase lifecycle: **Loading**, **Linking**, and **Initialization**.

#### The Delegation Hierarchy:
1. **Bootstrap ClassLoader:** Written in native C/C++, loads core runtime classes from `<JAVA_HOME>/lib` (e.g., `java.lang.Object`, `String`).
2. **Platform / Extension ClassLoader:** Loads platform extension modules and classes from `<JAVA_HOME>/lib/ext`.
3. **Application / System ClassLoader:** Loads user-defined application classes found on the system `CLASSPATH` or application module path.

> **Key Rule (Delegation Principle):** When a ClassLoader receives a request to load a class, it always delegates the request upwards to its parent first. Only if the parent cannot locate the class does the child attempt to load it. This ensures core Java classes cannot be maliciously overridden.

### 1.3 JVM Runtime Data Areas (Memory Model)
The JVM divides memory into five distinct runtime areas:

| Memory Area | Shared Across Threads? | Lifetime | Primary Purpose |
|:---|:---|:---|:---|
| **Heap Memory** | **Yes** (Universal) | JVM startup to shutdown | Stores all instantiated objects, arrays, and instance variables. Managed by GC. |
| **JVM Thread Stack** | **No** (Per Thread) | Created with thread | Stores stack frames containing local variables, partial results, and method invocation frames. |
| **Metaspace (Java 8+)** | **Yes** (Universal) | JVM lifecycle | Stored in native OS memory; holds loaded class metadata, bytecode definitions, and static variables. |
| **Program Counter (PC) Register**| **No** (Per Thread) | Thread lifecycle | Holds the memory address of the JVM bytecode instruction currently being executed. |
| **Native Method Stack** | **No** (Per Thread) | Thread lifecycle | Contains execution frames for native C/C++ methods called via JNI (Java Native Interface). |

```
JVM RUNTIME MEMORY
+----------------------------------------------------------------------+
|  SHARED AREAS (Across All Threads):                                  |
|  +----------------------------------------------------------------+  |
|  | HEAP MEMORY                                                    |  |
|  |  +------------------------+  +-------------------------------+ |  |
|  |  | Young Gen (Eden, S0, S1)|  | Old Gen (Tenured Objects)     | |  |
|  |  +------------------------+  +-------------------------------+ |  |
|  +----------------------------------------------------------------+  |
|  +----------------------------------------------------------------+  |
|  | METASPACE (Native Memory - Class Definitions & Bytecode)       |  |
|  +----------------------------------------------------------------+  |
+----------------------------------------------------------------------+
|  THREAD-SPECIFIC AREAS (Per Active Thread):                          |
|  [ Thread 1: Stack | PC Register ]   [ Thread 2: Stack | PC Register ]|
+----------------------------------------------------------------------+
```

### 1.4 Garbage Collection (GC) Mechanics
Java manages Heap memory automatically through the Garbage Collector. An object becomes eligible for GC when it is no longer reachable through any chain of live references originating from **GC Roots** (Thread stack references, static variables, JNI references).

#### The Generational Hypothesis:
Empirical data shows that most objects have very short lifespans (over 90% die shortly after allocation). The Heap is therefore segmented:
1. **Young Generation:**
   - **Eden Space:** All newly created objects are initially allocated here.
   - **Survivor Spaces (S0 & S1):** Objects that survive a **Minor GC** in Eden are copied between S0 and S1. A generational age counter is incremented on each survival.
2. **Old Generation (Tenured):**
   - When an object's age exceeds the tenuring threshold (default: 15 cycles, `-XX:MaxTenuringThreshold=15`), it is promoted to the Old Generation.
   - Collected during **Major / Full GC** cycles using algorithms such as Mark-Sweep-Compact.

#### Modern Production Garbage Collectors:
- **G1 GC (Garbage-First):** Default since Java 9. Divides heap into equal-sized regions and collects regions with the highest amount of garbage first to meet user-defined latency goals (`-XX:MaxGCPauseMillis=200`).
- **ZGC (Z Garbage Collector):** Ultra-low-latency collector introduced in Java 15/17/21 capable of managing multi-terabyte heaps with pause times consistently below 1 millisecond.

---

## Chapter 2: Primitive Types, Operators & Modern Control Flow

### 2.1 The 8 Primitive Types
Java strictly defines 8 primitive types with fixed platform-independent sizes:

```java
// Integral Types
byte  b = 127;                // 8 bits  [-128 to 127]
short s = 32767;              // 16 bits [-32,768 to 32,767]
int   i = 2_147_483_647;      // 32 bits [-2^31 to 2^31 - 1]
long  l = 9_223_372_036_854_775_807L; // 64 bits [-2^63 to 2^63 - 1]

// Floating Point Types (IEEE 754)
float  f = 3.14159f;          // 32 bits single precision
double d = 2.718281828459045; // 64 bits double precision

// Textual & Logical
char    c = 'A';              // 16 bits Unicode [0 to 65,535 (\u0000 to \uffff)]
boolean bool = true;          // 1 bit logical (JVM uses int under the hood)
```

> **Placement Trap (Floating Point Precision):** In IEEE 754 floating point arithmetic, values like `0.1 + 0.2 == 0.3` evaluate to `false` because binary representation cannot precisely express 0.1 and 0.2 without infinite repeating fractions (`0.30000000000000004`). In financial systems, always use `java.math.BigDecimal`.

### 2.2 Type Casting: Widening vs Narrowing
- **Widening (Implicit):** Converting a smaller data type to a larger data type (e.g., `int` -> `long` -> `float` -> `double`). Safe; performed automatically without data loss.
- **Narrowing (Explicit):** Converting a larger data type to a smaller data type. Requires an explicit cast operator `(type)` and truncates higher-order bits:

```java
int large = 130;
byte b = (byte) large; // Truncates 32-bit int to 8 bits
System.out.println(b); // Output: -126 (due to two's complement overflow)
```

### 2.3 Short-Circuit vs Non-Short-Circuit Operators
- **Short-Circuit (`&&`, `||`):** Evaluates the right-hand expression only if the outcome cannot be determined from the left-hand operand.
- **Non-Short-Circuit (`&`, `|`):** Always evaluates both operands regardless of the left-hand outcome.

```java
String text = null;
// Safe: Short-circuit prevents NullPointerException
if (text != null && text.length() > 0) {
    System.out.println("Has text");
}

// Dangerous: Will throw NullPointerException because right-hand side always evaluates
// if (text != null & text.length() > 0) { ... }
```

### 2.4 Modern Enhanced Switch Expressions (Java 14+)
Traditional switch statements suffered from error-prone fallthrough and mandatory `break` statements. Modern Java provides arrow syntax (`->`) and `yield` expressions:

```java
public static int getWorkDays(String day) {
    return switch (day.toUpperCase()) {
        case "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY" -> 1;
        case "SATURDAY", "SUNDAY" -> 0;
        default -> {
            System.err.println("Unrecognized calendar day: " + day);
            yield -1; // yield returns value from multi-line block
        }
    };
}
```

---

## Chapter 3: Object-Oriented Programming (OOP) Deep Dive & Object Lifecycle

### 3.1 The 4 Pillars of OOP in Java
1. **Encapsulation:** Wrapping state and behavior into a single unit (class) while restricting direct field access via `private` fields and providing controlled `public` accessor/mutator methods.
2. **Inheritance:** Code reuse mechanism where a child class acquires fields and methods of a parent class via `extends`. Java supports single class inheritance to eliminate the **Diamond Problem**.
3. **Polymorphism:** The ability of an object to take many forms. Manifests as compile-time overloading and runtime method overriding via dynamic method dispatch.
4. **Abstraction:** Exposing only essential features while hiding low-level implementation details through `abstract` classes and `interface` contracts.

### 3.2 Constructor Chaining & Object Initialization Order
When an object is instantiated (`new Dog()`), the JVM follows a deterministic initialization sequence:
1. **Static Initializer Blocks & Static Field Initializers** of Parent class, then Child class (executed once when class is loaded).
2. **Instance Initializer Blocks & Instance Field Initializers** of Parent class.
3. **Parent Class Constructor**.
4. **Instance Initializer Blocks & Instance Field Initializers** of Child class.
5. **Child Class Constructor**.

```java
class Animal {
    static { System.out.println("1. Animal Static Block"); }
    { System.out.println("3. Animal Instance Block"); }
    Animal() { System.out.println("4. Animal Constructor"); }
}

class Dog extends Animal {
    static { System.out.println("2. Dog Static Block"); }
    { System.out.println("5. Dog Instance Block"); }
    Dog() {
        super(); // Invokes Animal()
        System.out.println("6. Dog Constructor");
    }
}
// Execution of 'new Dog()' outputs: 1 -> 2 -> 3 -> 4 -> 5 -> 6
```

### 3.3 Method Overriding vs Method Overloading
```
+------------------------------------+-------------------------------------+
| Method Overloading (Compile-Time)  | Method Overriding (Runtime Dynamic) |
+------------------------------------+-------------------------------------+
| Same method name, different args.  | Same name AND identical parameters. |
| In the same class or subclass.     | Must be between superclass & child. |
| Return type can be different.      | Must have same or covariant return. |
| Resolved by compiler at compile.   | Resolved at runtime via vtable.     |
| Private/static methods CAN overload| Private/static CANNOT be overridden.|
+------------------------------------+-------------------------------------+
```

### 3.4 The `equals()` and `hashCode()` Contract
Every Java class inherits `equals()` and `hashCode()` from `java.lang.Object`.
- The default `Object.equals(Object o)` compares **memory references** (`this == o`).
- The default `Object.hashCode()` computes an integer based on the internal object memory address.

> **CRITICAL PLACEMENT RULE:** If two objects are equal according to `equals()`, they **MUST** produce the exact same `hashCode()`. If you override `equals()`, you **MUST** override `hashCode()`. Failure to do so corrupts hash-based collections (`HashSet`, `HashMap`), resulting in duplicate keys or unretrievable values.

```java
public class Employee {
    private final int id;
    private final String department;

    public Employee(int id, String department) {
        this.id = id;
        this.department = department;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Employee emp)) return false;
        return this.id == emp.id && Objects.equals(this.department, emp.department);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, department);
    }
}
```

---

## Chapter 4: String Architecture, Immutability & Memory Pooling

### 4.1 Why Strings are Immutable in Java
In Java, `java.lang.String` is `final` and immutable. Once created, its character array cannot be altered:
1. **String Constant Pool (SCP):** Immutability allows the JVM to cache string literals. Thousands of variables pointing to `"admin"` share a single heap allocation.
2. **Security:** Strings carry sensitive database credentials, network URLs, and filesystem paths. Mutability would allow malicious callers to alter connection strings after authorization.
3. **Thread-Safety:** Being immutable, String instances can be freely shared across concurrent threads without locks or synchronization.
4. **HashCode Caching:** String caches its `hash` integer upon first computation, making Map lookups O(1) without recalculation.

```java
String s1 = "Placement";         // Allocated in String Constant Pool
String s2 = "Placement";         // Reuses cached reference in SCP
String s3 = new String("Placement"); // Forces new allocation in regular Heap

System.out.println(s1 == s2);      // true (same SCP memory address)
System.out.println(s1 == s3);      // false (SCP vs regular Heap object)
System.out.println(s1.equals(s3)); // true (compares character content)
System.out.println(s1 == s3.intern()); // true (intern() returns SCP reference)
```

### 4.2 String vs StringBuilder vs StringBuffer
```
+----------------+---------------+------------------+-------------------+
| Characteristic | String        | StringBuilder    | StringBuffer      |
+----------------+---------------+------------------+-------------------+
| Mutability     | Immutable     | Mutable          | Mutable           |
| Thread Safety  | Thread-Safe   | Not Thread-Safe  | Thread-Safe (Sync)|
| Performance    | Slow on loop +| Fast (No locks)  | Slower (Mutex lock)|
| Introduced in  | Java 1.0      | Java 1.5         | Java 1.0          |
+----------------+---------------+------------------+-------------------+
```

---

## Chapter 5: Arrays, Wrapper Classes & Number Systems

### 5.1 Arrays in Java
Arrays in Java are Heap-allocated objects with a fixed `length` attribute. Java provides the `java.util.Arrays` utility class for efficient binary search, parallel sorting, and equality verification:

```java
int[] numbers = {45, 12, 85, 32, 89, 39, 69, 44};
Arrays.sort(numbers); // Dual-Pivot Quicksort O(N log N)
int idx = Arrays.binarySearch(numbers, 45); // O(log N) lookup
```

### 5.2 Autoboxing & The Integer Cache Trap
Autoboxing is the automatic conversion the Java compiler makes between primitive types and their corresponding object wrapper classes (e.g., `int` -> `Integer.valueOf(i)`).

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b); // true (reused from IntegerCache [-128 to 127])

Integer x = 128;
Integer y = 128;
System.out.println(x == y); // FALSE! Outside cache; evaluates distinct references
System.out.println(x.equals(y)); // true! Always use equals() for wrapper objects
```

---

## Chapter 6: Exception Handling Architecture & Robust Design

### 6.1 The Throwable Hierarchy
```
                      Throwable
                     /         \
                Exception       Error (Out of Memory, StackOverflow)
               /         \
    Checked Exceptions    RuntimeException (Unchecked)
    (IOException,         (NullPointerException,
     SQLException)         ArithmeticException,
                           IllegalArgumentException)
```

### 6.2 Try-With-Resources (Java 7+)
Prior to Java 7, resources were closed in `finally` blocks, often leading to leaked file descriptors when closing itself threw an exception. Modern Java uses **try-with-resources**, requiring the resource to implement `java.lang.AutoCloseable`:

```java
public static String readFirstLine(String path) throws IOException {
    // BufferedReader automatically closed in reverse order of declaration
    try (var br = new BufferedReader(new FileReader(path))) {
        return br.readLine();
    }
}
```

---

## Chapter 7: Java Collections Framework (JCF) & Internal Data Structures

### 7.1 Collection Framework Architecture Overview
```
                       Iterable<E>
                           |
                      Collection<E>
                     /      |      \
               List<E>   Set<E>    Queue<E>
               /     \      |    \      |
      ArrayList   LinkedList|  TreeSet  PriorityQueue
                         HashSet
                         LinkedHashSet

             Map<K, V> (Independent Hierarchy)
             /       \         \
       HashMap    TreeMap   ConcurrentHashMap
       LinkedHashMap
```

### 7.2 HashMap Deep Internal Mechanics
The `HashMap` is the most frequently tested data structure in campus technical interviews.

#### Core Parameters:
- **Default Initial Capacity:** 16 (always a power of 2).
- **Default Load Factor:** 0.75.
- **Resize Threshold:** `capacity * loadFactor` (16 * 0.75 = 12). When size exceeds 12, capacity doubles to 32.

#### Index Calculation Formula:
Instead of slow modulus division (`hash % n`), Java uses bitwise AND masking:
$$\text{Index} = (n - 1) \ \& \ \text{hash}$$
This bitwise calculation is valid because $n$ is always a power of 2.

#### Treeification (Java 8+):
When hash collisions occur, entries are stored in a bucket linked list. If collisions in a single bucket reach **8** (`TREEIFY_THRESHOLD`) and total table capacity is at least **64**, the linked list converts into a self-balancing **Red-Black Tree** (`TreeNode`). This elevates search time from $O(N)$ worst-case to $O(\log N)$.

```
HASHMAP BUCKET ARCHITECTURE
Bucket Index
[0] -> null
[1] -> Node(K1, V1) -> Node(K2, V2) -> null (Linked List, collisions < 8)
[2] -> null
[3] -> [Red-Black Tree Root] (Treeified bucket, collisions >= 8)
       /                 \
     TreeNode          TreeNode
```

---

## Chapter 8: Generics, Type Safety & Type Erasure

### 8.1 Why Generics?
Introduced in Java 5, Generics provide compile-time type checking, eliminate explicit type casts, and prevent `ClassCastException` at runtime.

### 8.2 Type Erasure
Java implements generics using **Type Erasure**. The compiler enforces type constraints during compilation and then strips out all generic type parameters from the generated bytecode, replacing them with `Object` (or the declared upper bound) and inserting synthetic casts. This ensures backward compatibility with pre-Java 5 JVM bytecode.

### 8.3 The PECS Principle (Producer Extends, Consumer Super)
- **`? extends T` (Upper Bounded Wildcard):** Used when the collection is a **Producer** (you only read data from it).
- **`? super T` (Lower Bounded Wildcard):** Used when the collection is a **Consumer** (you write data into it).

```java
// Reads numbers from src (Producer Extends) and writes into dest (Consumer Super)
public static <T> void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) {
        dest.add(item); // Safe write into super T
    }
}
```

---

## Chapter 9: Multithreading, Concurrency & Thread Synchronization

### 9.1 Thread Lifecycle States
A Java thread operates within 6 states managed by `java.lang.Thread.State`:
1. **NEW:** Created but `start()` has not been called.
2. **RUNNABLE:** Executing on the CPU or waiting in OS ready queue.
3. **BLOCKED:** Waiting to acquire an intrinsic monitor lock.
4. **WAITING:** Waiting indefinitely for another thread via `wait()` or `join()`.
5. **TIMED_WAITING:** Waiting for a specified duration via `sleep(ms)` or `wait(ms)`.
6. **TERMINATED:** Completed its execution or died from an unhandled exception.

### 9.2 The `volatile` Modifier
When multiple threads access a variable, each CPU core caches its value in local registers. The `volatile` keyword instructs the JVM:
1. Every write to the variable is immediately written back to **Main Memory**.
2. Every read of the variable is fetched directly from **Main Memory**.
3. Establishes a **Happens-Before** memory ordering guarantee.

> **Warning:** `volatile` guarantees visibility, but **NOT atomicity**. For compound operations like `count++` (which involves read, increment, and write), use `AtomicInteger` or `synchronized`.

### 9.3 ThreadPoolExecutor Architecture
```java
// Production ThreadPool Creation
ExecutorService pool = new ThreadPoolExecutor(
    4,                             // Core pool size (active threads)
    10,                            // Maximum pool size
    60L, TimeUnit.SECONDS,         // Keep-alive time for idle threads
    new ArrayBlockingQueue<>(100), // Work queue for waiting tasks
    new ThreadPoolExecutor.CallerRunsPolicy() // Backpressure rejection policy
);
```

---

## Chapter 10: Lambdas, Functional Interfaces & Modern Stream API

### 10.1 Core Functional Interfaces (`java.util.function`)
| Interface | Method Signature | Purpose | Real-World Example |
|:---|:---|:---|:---|
| `Predicate<T>` | `boolean test(T t)` | Filtering / boolean test | `x -> x > 18` |
| `Function<T, R>` | `R apply(T t)` | Transformation | `String::length` |
| `Consumer<T>` | `void accept(T t)` | Side-effect action | `System.out::println` |
| `Supplier<T>` | `T get()` | Lazy value factory | `() -> Math.random()` |

### 10.2 Stream API Data Processing Pipeline
Streams provide a declarative, functional approach to processing collections. Streams are lazy and do not modify the backing collection:

```java
List<String> topPerformers = employees.stream()
    .filter(e -> e.getSalary() > 80_000)          // Intermediate (Lazy)
    .sorted(Comparator.comparing(Employee::getName)) // Intermediate
    .map(Employee::getName)                       // Intermediate
    .limit(5)                                     // Intermediate
    .collect(Collectors.toList());                // Terminal (Eager Execution)
```

---

## Chapter 11: Java I/O, NIO.2 & Object Serialization

### 11.1 Java NIO.2 (`java.nio.file`)
Java 7+ introduced NIO.2, simplifying file operations over older `java.io.File`:

```java
Path path = Paths.get("placement_data.txt");
// Read all lines into a List in one line
List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);

// Stream lines for massive files without high memory consumption
try (Stream<String> stream = Files.lines(path)) {
    stream.filter(l -> l.contains("ACCEPTED")).forEach(System.out::println);
}
```

### 11.2 Serialization & `serialVersionUID`
To serialize an object to bytes, it must implement `java.io.Serializable`.
- `serialVersionUID` is a version stamp used during deserialization to verify that the sender and receiver agree on a compatible class structure.
- The `transient` keyword marks fields that should be skipped during serialization (e.g., passwords, live database connections).

---

## Chapter 12: Modern Java Features (Java 9 through Java 21 LTS)

### 12.1 Java 16 Records
Records provide a concise syntax for immutable data carriers, automatically synthesizing canonical constructors, `getters`, `equals()`, `hashCode()`, and `toString()`:

```java
// 1 line replaces 60 lines of traditional boilerplate POJO
public record Candidate(String name, String college, double cgpa) {}
```

### 12.2 Java 17 Sealed Classes
Sealed classes restrict which other classes or interfaces may extend or implement them, enabling safe algebraic domain modeling:

```java
public abstract sealed class Round permits TechnicalRound, HRRound {}
public final class TechnicalRound extends Round {}
public final class HRRound extends Round {}
```

### 12.3 Java 21 Virtual Threads (Project Loom)
Virtual threads are lightweight threads managed entirely by the JVM rather than the underlying OS kernel. While a platform thread consumes ~1 MB of memory and is capped around a few thousand, a single JVM can comfortably execute **millions of virtual threads** simultaneously:

```java
// Starts a virtual thread using standard synchronous blocking code
Thread.startVirtualThread(() -> {
    String result = fetchCandidateDataFromExternalAPI();
    System.out.println("Result: " + result);
});
```

---

## Chapter 13: Placement Interview Puzzles, Memory Leaks & Design Patterns

### 13.1 Tricky Interview Puzzle 1: Static vs Instance Initialization
```java
class Test {
    static int x = 10;
    static {
        x += 5;
    }
    public static void main(String[] args) {
        System.out.println(Test.x); // Prints 15
    }
}
```

### 13.2 Tricky Interview Puzzle 2: Overloading Resolution with `null`
```java
public class Puzzle {
    public static void print(Object o) { System.out.println("Object"); }
    public static void print(String s) { System.out.println("String"); }

    public static void main(String[] args) {
        print(null); // Prints "String"!
        // Explanation: Java always chooses the most specific method matching the argument.
        // String is a subclass of Object, so String is more specific.
    }
}
```

### 13.3 Thread-Safe Singleton Pattern (Bill Pugh Holder Idiom)
The recommended production approach to implement a thread-safe lazy Singleton in Java without requiring explicit synchronization:

```java
public class PlacementDatabaseManager {
    private PlacementDatabaseManager() {}

    // Inner static class loaded only upon first invocation of getInstance()
    private static class InstanceHolder {
        private static final PlacementDatabaseManager INSTANCE = new PlacementDatabaseManager();
    }

    public static PlacementDatabaseManager getInstance() {
        return InstanceHolder.INSTANCE;
    }
}
```

---

## 🎯 Final Study & Examination Strategy

1. **Review Code Examples:** Ensure you can explain the memory implications of each chapter's code snippets.
2. **Practice in the Coding Lab:** Implement custom `LinkedList`, `HashMap`, and multithreaded Producer-Consumer queues in our interactive coding editor.
3. **Take Timed Quizzes:** Use our 30-seconds-per-question placement exam practice tests to build speed and accuracy for company assessments.
"""

JAVA_EXPANDED_BOOK_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "Java Architecture, JVM Internals & Memory Model",
        "subtopic": "JVM Memory Areas & GC",
        "question": "In the JVM Runtime Data Areas, which memory area is shared among all threads and holds all object instances and their associated arrays?",
        "options": ["Heap Area", "Java Thread Stack", "Program Counter (PC) Register", "Native Method Stack"],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 1: Java Architecture, JVM Internals & Memory Model]\nThe Heap Area is created upon JVM startup and is universally shared across all threads. All object instances and arrays are allocated on the Heap and managed by the Garbage Collector.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 1,
        "chapter_title": "Java Architecture, JVM Internals & Memory Model",
        "subtopic": "Metaspace & Class Loading",
        "question": "Since Java 8, where does the JVM store class metadata, runtime constant pools, and method bytecode definitions?",
        "options": ["Metaspace (allocated in native OS memory)", "Permanent Generation (PermGen in Heap)", "Java Thread Stack", "Direct Memory Buffer"],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 1: Java Architecture, JVM Internals & Memory Model]\nJava 8 completely removed PermGen from Heap memory and replaced it with Metaspace, which resides in native process memory and automatically resizes by default.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 2,
        "chapter_title": "Primitive Data Types, Operators & Modern Control Flow",
        "subtopic": "Floating Point Precision Trap",
        "question": "In standard Java, what is the result of evaluating the boolean expression `(0.1 + 0.2 == 0.3)` and why?",
        "options": [
            "false, because IEEE 754 binary floating-point representation cannot precisely represent fractions like 0.1 and 0.2.",
            "true, because Java's math library automatically rounds floating-point sums.",
            "Compile-time error, because double literals cannot be compared using ==.",
            "true, because both sides evaluate to 0.3 exactly."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 2: Primitive Data Types, Operators & Modern Control Flow]\nDue to IEEE 754 binary floating point precision, 0.1 + 0.2 evaluates to 0.30000000000000004. Comparing it directly to 0.3 with == yields false. BigDecimal should be used for exact arithmetic.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 3,
        "chapter_title": "Object-Oriented Programming (OOP) Deep Dive & Object Lifecycle",
        "subtopic": "equals and hashCode Contract",
        "question": "According to the Java contract between equals() and hashCode(), which statement is strictly mandatory?",
        "options": [
            "If obj1.equals(obj2) is true, then obj1.hashCode() MUST equal obj2.hashCode().",
            "If obj1.hashCode() == obj2.hashCode(), then obj1.equals(obj2) must always be true.",
            "Overriding equals() never requires overriding hashCode().",
            "Two distinct objects in different memory locations must always produce different hash codes."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 3: Object-Oriented Programming (OOP) Deep Dive & Object Lifecycle]\nThe contract explicitly requires that if two objects are equal according to equals(), their hashCode() methods must produce the exact same integer value. Failing this breaks hash collections like HashMap and HashSet.",
        "difficulty": "hard",
    },
    {
        "chapter_num": 3,
        "chapter_title": "Object-Oriented Programming (OOP) Deep Dive & Object Lifecycle",
        "subtopic": "Dynamic Method Dispatch",
        "question": "When `Animal a = new Dog(); a.makeSound();` is executed, how does the JVM determine which `makeSound()` implementation to call?",
        "options": [
            "At runtime via Dynamic Method Dispatch using the virtual method table (vtable) of the actual Dog instance.",
            "At compile time based strictly on the reference type Animal.",
            "By performing reflection on every method call.",
            "By checking the constructor of the enclosing class."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 3: Object-Oriented Programming (OOP) Deep Dive & Object Lifecycle]\nJava uses Dynamic Method Dispatch. At runtime, the JVM inspects the actual object type in Heap memory (Dog) via its vtable and invokes Dog's overridden method.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 4,
        "chapter_title": "String Architecture, Immutability & Memory Pooling",
        "subtopic": "String Constant Pool & Identity",
        "question": "Given: `String s1 = \"placement\"; String s2 = new String(\"placement\");` What will `s1 == s2` and `s1 == s2.intern()` evaluate to?",
        "options": [
            "s1 == s2 is false; s1 == s2.intern() is true.",
            "s1 == s2 is true; s1 == s2.intern() is true.",
            "s1 == s2 is false; s1 == s2.intern() is false.",
            "Both throw NullPointerException."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 4: String Architecture, Immutability & Memory Pooling]\ns1 points to the String Constant Pool literal. s2 points to a distinct Heap object, so s1 == s2 is false. Calling s2.intern() returns the canonical SCP reference, so s1 == s2.intern() evaluates to true.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 5,
        "chapter_title": "Arrays, Wrapper Classes & Number Systems",
        "subtopic": "Integer Cache Trap",
        "question": "Given `Integer a = 127, b = 127; Integer c = 128, d = 128;` What are the results of `(a == b)` and `(c == d)`?",
        "options": [
            "a == b is true; c == d is false.",
            "a == b is true; c == d is true.",
            "a == b is false; c == d is false.",
            "a == b is false; c == d is true."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 5: Arrays, Wrapper Classes & Number Systems]\nJava caches Integer objects within the range -128 to 127 via IntegerCache. Autoboxed values in this range reuse cached instances (same reference). Values outside 127 allocate distinct objects, causing reference comparison (==) to return false.",
        "difficulty": "hard",
    },
    {
        "chapter_num": 6,
        "chapter_title": "Exception Handling Architecture & Robust Design",
        "subtopic": "Finally Execution Semantics",
        "question": "In which of the following scenarios will a `finally` block NOT execute after entering a `try` block?",
        "options": [
            "If System.exit(0) is invoked inside the try block.",
            "If the try block contains a return statement.",
            "If an unchecked RuntimeException is thrown inside the try block.",
            "If a checked exception is caught and rethrown."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 6: Exception Handling Architecture & Robust Design]\nThe finally block executes in almost all conditions, including when return is called. However, it will not execute if the JVM halts execution via System.exit(), or if a fatal OS crash/power failure terminates the JVM process.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 7,
        "chapter_title": "Java Collections Framework (JCF) & Internal Data Structures",
        "subtopic": "HashMap Treeification Threshold",
        "question": "In Java 8+, what happens to a HashMap bucket when the number of colliding entries exceeds the threshold of 8 and the table capacity is at least 64?",
        "options": [
            "The linked list bucket converts into a balanced Red-Black Tree, improving lookup from O(N) to O(log N).",
            "The HashMap throws an OutOfMemoryError.",
            "The oldest elements in the bucket are evicted via FIFO policy.",
            "The HashMap doubles its load factor and deletes duplicate hash codes."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 7: Java Collections Framework (JCF) & Internal Data Structures]\nTo prevent worst-case collision denial-of-service attacks, Java 8 treeifies bucket linked lists into self-balancing Red-Black trees when collisions exceed TREEIFY_THRESHOLD (8) and table capacity is >= 64.",
        "difficulty": "hard",
    },
    {
        "chapter_num": 8,
        "chapter_title": "Generics, Type Safety & Type Erasure",
        "subtopic": "PECS Principle",
        "question": "According to the PECS rule in Java Generics, which wildcard should you use if your method only reads (consumes elements from) a collection?",
        "options": [
            "? extends T (Producer Extends)",
            "? super T (Consumer Super)",
            "<?> (Unbounded wildcard)",
            "<T extends Object>"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 8: Generics, Type Safety & Type Erasure]\nPECS stands for 'Producer Extends, Consumer Super'. If a collection produces values for you to read, use '? extends T'. If you write elements into the collection, use '? super T'.",
        "difficulty": "hard",
    },
    {
        "chapter_num": 9,
        "chapter_title": "Multithreading, Concurrency & Thread Synchronization",
        "subtopic": "Volatile vs Synchronized",
        "question": "What guarantee does the `volatile` modifier provide to a shared field in a multi-threaded Java program?",
        "options": [
            "Guarantees visibility of reads and writes directly to main memory, preventing CPU register caching.",
            "Guarantees that compound operations like `count++` are atomic.",
            "Prevents other threads from reading the variable while one thread writes.",
            "Ensures the variable is automatically serialized across network sockets."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 9: Multithreading, Concurrency & Thread Synchronization]\nVolatile guarantees that any write to the variable is immediately flushed to main memory and subsequent reads see the latest write. However, it does NOT provide mutual exclusion or compound atomicity.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 10,
        "chapter_title": "Lambdas, Functional Interfaces & Modern Stream API",
        "subtopic": "Stream Intermediate vs Terminal Operations",
        "question": "Why does `stream.filter(x -> x > 10).map(x -> x * 2);` execute zero filtering or mapping computations if no terminal operation is appended?",
        "options": [
            "Because Stream intermediate operations are evaluated lazily and only execute when a terminal operation triggers the pipeline.",
            "Because Java streams discard unreferenced streams immediately.",
            "Because lambdas require synchronized execution.",
            "Because map() and filter() must always be called inside a try block."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 10: Lambdas, Functional Interfaces & Modern Stream API]\nStream pipelines are lazy. Intermediate operations (filter, map) construct the pipeline definition. Traversal and computation commence only when an eager terminal operation (such as collect(), forEach(), or reduce()) is invoked.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 12,
        "chapter_title": "Modern Java Features (Java 9 through Java 21 LTS)",
        "subtopic": "Virtual Threads (Project Loom)",
        "question": "What is the primary breakthrough of Java 21's Virtual Threads compared to traditional platform threads?",
        "options": [
            "They are lightweight user-mode threads managed by the JVM, allowing millions of concurrent tasks with standard synchronous blocking code.",
            "They eliminate the need for the Garbage Collector.",
            "They execute Python code natively inside the JVM without JNI.",
            "They replace all CPU registers with virtual registers."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 12: Modern Java Features (Java 9 through Java 21 LTS)]\nVirtual Threads (Project Loom in Java 21) are managed by the JVM instead of 1-to-1 OS kernel threads. When a virtual thread blocks on I/O, the JVM unmounts it from the carrier platform thread, permitting millions of concurrent tasks with minimal memory footprint.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 13,
        "chapter_title": "Placement Interview Puzzles, Memory Leaks & Design Patterns",
        "subtopic": "Method Resolution with null argument",
        "question": "Given `public void test(Object o)` and `public void test(String s)`, what will `test(null)` invoke and why?",
        "options": [
            "test(String s), because String is more specific than Object in the inheritance hierarchy.",
            "test(Object o), because Object is the universal root class.",
            "Compile error due to ambiguous method call.",
            "NullPointerException at runtime."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Java Prescribed Textbook — Chapter 13: Placement Interview Puzzles, Memory Leaks & Design Patterns]\nJava's method overload resolution selects the most specific method that matches the arguments. Since String is a subtype of Object, String is more specific, so test(String s) is chosen without ambiguity.",
        "difficulty": "hard",
    }
]
