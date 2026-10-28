"""
curriculum_go.py - 8 Comprehensive Chapters for Go (Golang) Cloud Systems & Placement Master Edition.
"""
from typing import List, Dict, Any

GOLANG_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Go Toolchain, Language Architecture & Runtime Memory Model",
        "key_takeaways": "Master Go's static compilation, package architecture, zero values, escape analysis, and the Go runtime scheduler (GMP model).",
        "topics": [
            "Design Philosophy of Go: Simplicity, concurrency, fast compilation",
            "Go Workspace: Modules (`go.mod`), Packages, and Visibility (Capitalization rule)",
            "Data Types, Zero Values, and Short Variable Declarations (`:=`)",
            "Escape Analysis: Stack vs Heap Allocation (`go build -gcflags='-m'`)",
            "Under the Hood: The Go Runtime & The GMP Scheduler (Goroutine, Machine, Processor)",
            "Garbage Collector: Tri-color concurrent mark-sweep with sub-millisecond pauses"
        ],
        "sections": {
            "concept": """Go (Golang) is an open-source, statically typed, compiled programming language engineered at Google by Robert Griesemer, Rob Pike, and Ken Thompson. It prioritizes simplicity, direct machine-code compilation, safety, and native concurrency.

**Core Language Foundations:**
1. **Compilation Model:** Go compiles directly to static native machine code binaries without intermediate bytecode or virtual machines. Binaries pack the user code alongside a minimal lightweight runtime that includes the garbage collector and GMP scheduler.
2. **Identifier Visibility:** Visibility is determined strictly by the first letter's capitalization:
   - Capitalized (`func CalculateTotal()`): Exported (Public across packages).
   - Lowercase (`func calculateTax()`): Unexported (Private to the package).
3. **Zero Values:** Variables declared without an explicit initial value are automatically initialized to their zero value: `0` for numerics, `false` for booleans, `""` for strings, and `nil` for pointers, slices, maps, channels, and interfaces.
4. **Escape Analysis:** The Go compiler analyzes whether a variable outlives the stack frame of the function that created it. If it outlives the frame, it 'escapes to the heap'; otherwise, it is allocated on the fast stack.
5. **The GMP Scheduler:**
   - **G (Goroutine):** Lightweight green thread with an initial 2KB segmented stack.
   - **M (Machine):** OS kernel thread managed by the OS scheduler.
   - **P (Processor):** Logical execution context (usually equal to `GOMAXPROCS` or CPU cores) managing a local run-queue of goroutines.""",
            "formulas": """1. **Initial Stack Footprint Comparison:**
   $$\\text{OS Thread Stack} = 1\\text{MB} - 8\\text{MB}$$
   $$\\text{Go Goroutine Stack} = 2\\text{KB (Dynamically growing and shrinking)}$$
2. **Escape Analysis Rule:**
   $$\\text{Pointer returned outside function} \\implies \\text{Heap Allocation (Escapes to Heap)}$$
   $$\\text{Local usage only} \\implies \\text{Stack Allocation (Zero GC Overhead)}$$""",
            "solved_examples": [
                {
                    "title": "Demonstrating Escape Analysis with Stack vs Heap Allocation",
                    "difficulty": "Medium | Uber, Google, Razorpay",
                    "problem": "Write two functions: one where a struct stays on the stack, and one where the struct escapes to the heap because its pointer is returned.",
                    "step_by_step": [
                        "Step 1: Function `stayOnStack()` instantiates a struct and uses it locally.",
                        "Step 2: Function `escapeToHeap()` instantiates a struct and returns its memory address `&s`.",
                        "Step 3: Run escape analysis via `go build -gcflags=\"-m\"` to observe compiler output."
                    ],
                    "code_or_math": """package main

import "fmt"

type User struct {
    ID   int
    Name string
}

// Stack allocated: Does NOT escape
func stayOnStack() int {
    u := User{ID: 1, Name: "Alice"}
    return u.ID
}

// Heap allocated: Escapes because pointer outlives function scope
func escapeToHeap() *User {
    u := User{ID: 2, Name: "Bob"}
    return &u // Compiler allocates u on heap safely
}

func main() {
    id := stayOnStack()
    user := escapeToHeap()
    fmt.Printf("ID: %d, User: %+v\\n", id, user)
}""",
                    "explanation": "In C/C++, returning a pointer to a local variable results in a dangling pointer. In Go, the compiler's escape analysis detects this and automatically allocates the struct on the heap."
                }
            ],
            "practice_questions": [
                {
                    "question": "In Go, which entity represents a logical processor holding the local run-queue in the GMP scheduler?",
                    "options": [
                        "A) G (Goroutine)",
                        "B) M (Machine / OS Thread)",
                        "C) P (Processor)",
                        "D) K (Kernel)"
                    ],
                    "correct_answer": "C) P (Processor)",
                    "detailed_solution": "In the GMP model, P represents a logical processor (context). Each P holds a local run-queue of Goroutines (G) and binds to an OS thread (M) for execution."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google, Uber, Cloudflare",
                    "question": "How does Go achieve sub-millisecond Garbage Collection pauses?",
                    "model_answer": "Go uses a concurrent Tri-Color Mark-Sweep garbage collector. Objects are colored White (unvisited/candidates for reclamation), Grey (visited, children unvisited), and Black (visited, children confirmed reachable). The collector runs concurrently with user goroutines (mutators). To preserve pointer invariants during concurrent writes, Go employs a Write Barrier. Stop-The-World (STW) pauses are only required for microsecond phases (starting the write barrier and sweeping completion), resulting in pause times typically under 1 millisecond.",
                    "interviewer_tip": "Highlight the Tri-color concurrent marking and the write barrier."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Functions, Pointers, Structs & Receiver Methods (Value vs Pointer)",
        "key_takeaways": "Master Go functions as first-class citizens, pointer semantics, struct composition, and value vs pointer method receivers.",
        "topics": [
            "Functions: Multiple return values, named returns, and variadic parameters",
            "Pointers in Go: Dereference (`*`), Address-of (`&`), and absence of pointer arithmetic",
            "Structs: Anonymous fields, embedded structs for composition (not inheritance)",
            "Method Receivers: Value Receiver `(t Type)` vs Pointer Receiver `(t *Type)`",
            "Constructor Idioms: `NewObject()` factory functions and functional options pattern"
        ],
        "sections": {
            "concept": """Go rejects classical class-based inheritance in favor of **composition via embedded structs**.

**Multiple Return Values & Error Handling Idiom:**
Go functions can return multiple values. The standard idiom for operations that can fail is returning the result alongside an `error` as the last return value:
`func ReadData() (string, error)`

**Pointers in Go:**
Pointers store memory addresses (`*int`, `*User`). Crucially, Go does **NOT** support pointer arithmetic (such as `ptr++`) to prevent buffer overflows and memory corruption.

**Value Receivers vs Pointer Receivers:**
- **Value Receiver `func (u User) GetName() string`:** Receives a distinct copy of the struct. Modifications inside the method do not affect the caller's struct.
- **Pointer Receiver `func (u *User) SetName(name string)`:** Receives the memory pointer. Modifications directly mutate the caller's instance in-place.
- **Guideline:** Use a pointer receiver if: (1) the method modifies the struct, (2) the struct is large and copying is expensive, or (3) consistency demands that all receivers on that struct type be uniform.""",
            "formulas": """1. **Receiver Mutability Rule:**
   $$\\text{Value Receiver: } \\Delta \\text{State} = \\text{Discarded upon return (Mutates local copy)}$$
   $$\\text{Pointer Receiver: } \\Delta \\text{State} = \\text{Persisted in-place}$$
2. **Safety Invariant:**
   $$\\text{Go Pointers} \\implies \\text{No raw arithmetic} \\land \\text{Type-safe} \\land \\text{GC-tracked}$$""",
            "solved_examples": [
                {
                    "title": "Value Receiver vs Pointer Receiver Demonstration",
                    "difficulty": "Easy | Infosys, CTS, TCS Digital",
                    "problem": "Create a `BankAccount` struct with methods `Deposit` (mutates balance) and `Balance` (reads balance), demonstrating why pointer receivers are mandatory for mutation.",
                    "step_by_step": [
                        "Step 1: Define `type BankAccount struct { balance float64 }`.",
                        "Step 2: Define `Deposit(amount float64)` with a pointer receiver `(a *BankAccount)`.",
                        "Step 3: Define `Balance() float64` with a value receiver `(a BankAccount)`.",
                        "Step 4: Demonstrate that calling Deposit updates the actual account balance."
                    ],
                    "code_or_math": """package main

import "fmt"

type BankAccount struct {
    owner   string
    balance float64
}

// Pointer Receiver: Modifies original struct
func (a *BankAccount) Deposit(amount float64) {
    a.balance += amount
}

// Value Receiver: Read-only copy
func (a BankAccount) Balance() float64 {
    return a.balance
}

func main() {
    account := BankAccount{owner: "Raj", balance: 1000.0}
    account.Deposit(500.0) // Mutates balance
    fmt.Printf("Owner: %s, Current Balance: ₹%.2f\\n", account.owner, account.Balance())
    // Output: Owner: Raj, Current Balance: ₹1500.00
}""",
                    "explanation": "If Deposit used a value receiver (a BankAccount), the balance increment would be performed on a transient copy and discarded."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the result if you invoke a method with a pointer receiver on a value type in Go (e.g. `acc.Deposit(100)` where `acc` is a value)?",
                    "options": [
                        "A) Compile-time type mismatch error",
                        "B) Go automatically takes the address `(&acc).Deposit(100)` as syntactic sugar if the value is addressable",
                        "C) Runtime panic",
                        "D) Deposit executes as a value copy"
                    ],
                    "correct_answer": "B) Go automatically takes the address `(&acc).Deposit(100)` as syntactic sugar if the value is addressable",
                    "detailed_solution": "Go automatically interprets acc.Deposit() as (&acc).Deposit() if acc is an addressable value."
                }
            ],
            "interview_questions": [
                {
                    "company": "Docker, Kubernetes, HashiCorp",
                    "question": "Why does Go not support class-based inheritance, and how does struct embedding achieve polymorphism?",
                    "model_answer": "Go favors 'Composition over Inheritance' to avoid fragile base class problems, deep hierarchies, and tight coupling. Through struct embedding (anonymous fields), an outer struct promotes all methods and fields of the embedded inner struct to its own interface. This provides code reuse and delegation without the rigid subtyping of classical OOP.",
                    "interviewer_tip": "Cite the fragile base class problem and composition over inheritance."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Slices, Arrays, Maps & Memory Allocation Internals",
        "key_takeaways": "Master the 3-word Slice Header (ptr, len, cap), append reallocation mechanics, map hash table buckets, and map concurrency safety.",
        "topics": [
            "Arrays: Fixed-size, value semantics (copy on assignment)",
            "Slices: Dynamic reference views, Slice Header (`Data *T`, `Len int`, `Cap int`)",
            "`make([]T, len, cap)` vs slice literals",
            "The `append()` function: Geometric growth factor and underlying array detachment",
            "Maps: Hash table structure (hmap, bmap buckets), key constraints, and 2-value lookup",
            "Map Concurrency: Fatal runtime error on concurrent read/write and `sync.Map`"
        ],
        "sections": {
            "concept": """In Go, arrays have fixed compile-time lengths (`[5]int`), and passing an array copies all elements by value. In contrast, **Slices** are dynamic, lightweight window views over an underlying array.

**Slice Header Internals:**
A slice is physically a 24-byte structure (on 64-bit systems) containing:
1. `Data unsafe.Pointer`: Pointer to the first element in the backing array.
2. `Len int`: Number of elements currently present.
3. `Cap int`: Maximum elements from the start of the slice to the end of the backing array.

**The `append()` Growth Mechanics:**
When `append()` is called and `len + 1 <= cap`, Go updates `len` and inserts the element into the existing backing array. If `len + 1 > cap`, Go allocates a new, larger backing array (doubling size for small slices, scaling by ~1.25x for large slices), copies elements, and returns a new slice header.

**Map Architecture (`hmap`):**
A Go map is a pointer to an internal `hmap` structure. It consists of an array of **buckets** (`bmap`), where each bucket stores up to 8 key-value pairs using top-hash byte comparisons.
- **Important:** Go maps are **NOT thread-safe**. Concurrent reading and writing to a standard map without a mutex triggers a non-recoverable fatal runtime error: `fatal error: concurrent map writes`.""",
            "formulas": """1. **Slice Memory Header Size:**
   $$\\text{sizeof}(\\text{SliceHeader}) = \\text{sizeof}(\\text{Pointer}) + 2 \\times \\text{sizeof}(\\text{int}) = 8 + 8 + 8 = 24 \\text{ bytes}$$
2. **Sub-slicing Formula:**
   For `s[low:high:max]`:
   $$\\text{New Len} = high - low, \\quad \\text{New Cap} = max - low$$
3. **Map Retrieval Idiom:**
   $$\\text{val, ok := myMap[key]} \\implies ok = \\text{true if key present, false otherwise}$$""",
            "solved_examples": [
                {
                    "title": "Slice Backing Array Mutation vs Append Reallocation Trap",
                    "difficulty": "Medium | Amazon, Google, Razorpay",
                    "problem": "Explain what happens when two slices share a backing array, and how append causes detachment.",
                    "step_by_step": [
                        "Step 1: Create a slice `a := []int{10, 20, 30, 40, 50}`.",
                        "Step 2: Sub-slice `b := a[1:3]` (holds 20, 30, shares backing array).",
                        "Step 3: Mutating `b[0] = 99` alters `a[1]`.",
                        "Step 4: Calling `b = append(b, 100, 200, 300)` exceeds `cap(b)`, detaching `b` into its own fresh allocation."
                    ],
                    "code_or_math": """package main

import "fmt"

func main() {
    a := []int{10, 20, 30, 40, 50}
    b := a[1:3] // len=2, cap=4 (points to elements 20, 30)

    b[0] = 99 // Shared memory mutation!
    fmt.Println("a after mutating b[0]:", a) // [10 99 30 40 50]

    // Append exceeding capacity creates new backing array
    b = append(b, 100, 200, 300) // Exceeds cap 4 -> reallocates!
    b[0] = 777 // b is now detached!
    fmt.Println("a remains unchanged:", a) // [10 99 30 40 50]
    fmt.Println("b is independent:", b)     // [777 30 100 200 300]
}""",
                    "explanation": "Before reallocation, sub-slices mutate identical backing memory. After reallocation, append allocates a fresh buffer, isolating the slices."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens if two goroutines simultaneously read and write to the same standard Go map without synchronization?",
                    "options": [
                        "A) One goroutine waits automatically via implicit locks",
                        "B) An error is returned from the map lookup",
                        "C) The program crashes immediately with a fatal runtime error that cannot be recovered with recover()",
                        "D) Data is read with a slight delay"
                    ],
                    "correct_answer": "C) The program crashes immediately with a fatal runtime error that cannot be recovered with recover()",
                    "detailed_solution": "Go maps have built-in race detection flags. A concurrent read and write triggers an unrecoverable fatal runtime error."
                }
            ],
            "interview_questions": [
                {
                    "company": "Uber, Google, Datadog",
                    "question": "Why is it important to preallocate slices with `make([]T, 0, capacity)` when the element count is known beforehand?",
                    "model_answer": "Preallocating capacity eliminates repeated dynamic reallocations and memory copies during successive `append()` calls. Each reallocation requires allocating a new memory block, copying all existing elements, and waiting for the garbage collector to reclaim the old slice. Setting `cap` up-front achieves $O(1)$ amortized insertion with zero GC allocation pressure.",
                    "interviewer_tip": "Mention reduction of GC pressure and zero reallocations."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Interfaces, Duck Typing, Type Assertions & Polymorphic Composition",
        "key_takeaways": "Master implicit interface implementation, the 2-word Interface Header (type pointer, data pointer), and the nil interface trap.",
        "topics": [
            "Implicit Interfaces: 'If it walks like a duck and quacks like a duck, it is a duck'",
            "Small Interfaces: `io.Reader`, `io.Writer`, `fmt.Stringer`",
            "The Empty Interface: `any` (`interface{}`)",
            "Under the Hood: `iface` (itab + data) and `eface` (type + data)",
            "The Infamous `nil` Interface Trap: Why `var p *MyType = nil; var i MyInterface = p; i != nil`",
            "Type Assertions (`val.(TargetType)`) and Type Switches"
        ],
        "sections": {
            "concept": """In Go, interfaces are satisfied **implicitly**. A type does not use an `implements` keyword; if a type implements all methods declared by an interface, it automatically satisfies that interface.

**Interface Representation in Memory:**
An interface is a 16-byte structure consisting of two pointers:
1. **`itab` (Type Information):** Points to the type metadata and the virtual method table (interface table).
2. **`data` (Value Pointer):** Points to the actual underlying concrete object.

**The Infamous `nil` Interface Trap:**
An interface value is equal to `nil` **ONLY IF both its type pointer and its data pointer are `nil`**:
$$\\text{interface} == nil \\iff (\\text{type} == nil) \\land (\\text{data} == nil)$$
If you assign a typed `nil` pointer (e.g., `var u *User = nil`) to an interface variable `var r Runner = u`, the interface's data pointer is `nil`, but its type pointer points to `*User`. Therefore, **`r != nil` evaluates to `true`**, leading to unexpected runtime panics if dereferenced!""",
            "formulas": """1. **Interface Equality Rule:**
   $$\\text{Interface Value} = (\\text{Type Pointer}, \\text{Data Pointer})$$
   $$\\text{Interface is } nil \\iff \\text{Type} == nil \\land \\text{Data} == nil$$
2. **Type Assertion Safe Idiom:**
   $$\\text{val, ok := i.(ConcreteType)} \\implies ok = \\text{false on mismatch (no panic)}$$""",
            "solved_examples": [
                {
                    "title": "The Nil Interface Trap Solved",
                    "difficulty": "Hard | Google, Amazon, Microsoft",
                    "problem": "Demonstrate why returning a typed nil error struct pointer from a function causes the caller's `err != nil` check to evaluate to true, and fix it.",
                    "step_by_step": [
                        "Step 1: Define a custom error struct `type CustomError struct {}`.",
                        "Step 2: Have a function declare `var ce *CustomError = nil` and return `ce` as `error`.",
                        "Step 3: Caller receives `err := doSomething()`; test `if err != nil`.",
                        "Step 4: It prints 'Error occurred!' because `err` holds `(*CustomError, nil)`.",
                        "Step 5: Fix: Return explicit untyped `nil` on success."
                    ],
                    "code_or_math": """package main

import "fmt"

type CustomError struct {
    Msg string
}

func (e *CustomError) Error() string {
    return e.Msg
}

// BUGGY FUNCTION: Returns typed nil pointer
func buggyFunc() error {
    var ce *CustomError = nil
    return ce // Returns interface with Type=*CustomError, Data=nil
}

// CORRECT FUNCTION: Returns explicit nil
func correctFunc() error {
    var ce *CustomError = nil
    if ce == nil {
        return nil // Returns interface with Type=nil, Data=nil
    }
    return ce
}

func main() {
    err1 := buggyFunc()
    if err1 != nil {
        fmt.Println("Bug: err1 is NOT nil because Type pointer is set!")
    }

    err2 := correctFunc()
    if err2 == nil {
        fmt.Println("Correct: err2 is truly nil!")
    }
}""",
                    "explanation": "Always return an explicit nil literal when returning the error interface from a function to prevent returning an interface holding non-nil type metadata."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the memory size of an interface variable on a 64-bit architecture?",
                    "options": [
                        "A) 8 bytes (single pointer)",
                        "B) 16 bytes (type pointer + data pointer)",
                        "C) 24 bytes",
                        "D) 32 bytes"
                    ],
                    "correct_answer": "B) 16 bytes (type pointer + data pointer)",
                    "detailed_solution": "An interface consists of two 8-byte pointers: one to the type metadata (itab) and one to the underlying data value."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google, HashiCorp, Docker",
                    "question": "Why does Go promote many small interfaces (such as `io.Reader` and `io.Writer` with just 1 method) rather than large monolithic interfaces?",
                    "model_answer": "Small interfaces maximize composability, reusability, and loose coupling. A single-method interface like `io.Reader` (`Read(p []byte) (n int, err error)`) can be satisfied by network sockets, files, in-memory byte buffers, compression streams, and HTTP bodies without needing artificial inheritance. Types only implement what they need, adhering cleanly to the Interface Segregation Principle.",
                    "interviewer_tip": "Cite the Go proverb: 'The bigger the interface, the weaker the abstraction'."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Goroutines, Channels & Communicating Sequential Processes (CSP)",
        "key_takeaways": "Master the CSP philosophy, unbuffered vs buffered channels, channel directions, range over channels, and closing mechanics.",
        "topics": [
            "The CSP Concurrency Model: 'Do not communicate by sharing memory; share memory by communicating'",
            "Launching Goroutines (`go func()`)",
            "Unbuffered Channels: Synchronous handoff and rendezvous points",
            "Buffered Channels: Asynchronous circular FIFO ring buffers",
            "Channel Directions: Send-only (`chan<- T`) and Receive-only (`<-chan T`)",
            "Closing Channels, Detecting Closed Channels (`val, ok := <-ch`), and Panic Rules"
        ],
        "sections": {
            "concept": """Go concurrency is rooted in Tony Hoare's mathematical formalism: **Communicating Sequential Processes (CSP)**.

**Goroutines vs Threads:**
- Goroutines are managed in user space by Go's runtime, starting at only 2KB of memory.
- Switching between goroutines takes nanoseconds (only ~3 registers need saving), whereas OS thread context switching takes microseconds.

**Channels (`chan T`):**
Channels are typed conduits through which goroutines synchronize and exchange values:
1. **Unbuffered Channels (`make(chan T)`):** Have zero capacity. A send blocks until another goroutine receives from the channel (synchronous rendezvous).
2. **Buffered Channels (`make(chan T, capacity)`):** Hold a circular buffer of values. Sends block only when the buffer is full. Receives block only when the buffer is empty.

**The 3 Golden Channel Rules (Prevent Panics):**
1. Sending to a closed channel causes a **runtime panic**.
2. Closing an already closed channel causes a **runtime panic**.
3. Sending or receiving on a `nil` channel **blocks forever** (causing deadlocks if uncoordinated).
*Rule of thumb:* Only the sender should close a channel, never the receiver.""",
            "formulas": """1. **Channel Blocking Matrix:**
   $$\\begin{array}{|l|c|c|c|}
   \\hline
   \\textbf{Operation} & \\textbf{Nil Channel} & \\textbf{Open Channel} & \\textbf{Closed Channel} \\\\
   \\hline
   \\text{Send} & \\text{Blocks forever} & \\text{Blocks if full} & \\textbf{Panics!} \\\\
   \\text{Receive} & \\text{Blocks forever} & \\text{Blocks if empty} & \\text{Returns zero value, ok=false} \\\\
   \\text{Close} & \\textbf{Panics!} & \\text{Closes successfully} & \\textbf{Panics!} \\\\
   \\hline
   \\end{array}$$""",
            "solved_examples": [
                {
                    "title": "Producer-Consumer Pipeline with Channel Closing and Range Loop",
                    "difficulty": "Medium | Amazon, Microsoft, TCS Digital",
                    "problem": "Implement a pipeline where a producer generates square numbers into a channel, closes it, and a consumer drains the channel using a range loop.",
                    "step_by_step": [
                        "Step 1: Create a channel `ch := make(chan int, 5)`.",
                        "Step 2: Launch producer goroutine: loop, send squares, then `close(ch)`.",
                        "Step 3: Main goroutine drains using `for val := range ch` which automatically terminates when channel is closed and empty."
                    ],
                    "code_or_math": """package main

import "fmt"

func producer(n int, ch chan<- int) {
    for i := 1; i <= n; i++ {
        ch <- i * i
    }
    close(ch) // Signal that no more items will be sent
}

func main() {
    ch := make(chan int, 3) // Buffered channel
    go producer(5, ch)

    // Consumer loop: terminates gracefully upon channel close
    for val := range ch {
        fmt.Println("Received:", val)
    }
    fmt.Println("Pipeline finished successfully.")
}""",
                    "explanation": "Closing the channel informs the range loop to break cleanly once all buffered values have been received."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens when you receive from a closed channel that has no remaining buffered elements?",
                    "options": [
                        "A) The receiving goroutine panics",
                        "B) The receive operation blocks indefinitely",
                        "C) It immediately returns the zero value of the channel's type with ok=false",
                        "D) It returns nil"
                    ],
                    "correct_answer": "C) It immediately returns the zero value of the channel's type with ok=false",
                    "detailed_solution": "Receiving from a closed, empty channel does not panic; it immediately yields the type's zero value and ok=false."
                }
            ],
            "interview_questions": [
                {
                    "company": "Uber, Google, Netflix",
                    "question": "Why does sending to a `nil` channel block forever, and how can this behavior be exploited intentionally?",
                    "model_answer": "A nil channel has no allocated buffer or waiting queues, so operations on it block permanently. While this causes bugs if accidental, it is intentionally exploited inside `select` statements to dynamically disable a branch. By setting an active channel variable to `nil`, that `case` branch is permanently taken out of consideration by the `select` multiplexer without terminating the event loop.",
                    "interviewer_tip": "Mention disabling select cases dynamically."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Concurrency Primitives, Select Multiplexing & Context Cancellation",
        "key_takeaways": "Master select timeout patterns, sync.WaitGroup, sync.Mutex, atomic operations, and context.WithTimeout.",
        "topics": [
            "The `select` Statement: Non-blocking channel operations and timeouts (`time.After`)",
            "`sync.WaitGroup`: Synchronizing fan-out / fan-in goroutines",
            "`sync.Mutex` and `sync.RWMutex`: Protecting shared state against data races",
            "`sync/atomic`: Lock-free primitive operations (`AddInt64`, `CompareAndSwap`)",
            "`sync.Once`: Thread-safe lazy singleton initialization",
            "The `context` Package: Propagation of deadlines, cancellations, and request-scoped values"
        ],
        "sections": {
            "concept": """While channels are ideal for transferring ownership of data, traditional synchronization primitives are superior for managing low-level shared state and coordination.

**`sync.WaitGroup` Coordination:**
Used to wait for a collection of goroutines to finish:
- `wg.Add(n)`: Increment counter. **Must be called BEFORE launching the goroutines.**
- `wg.Done()`: Decrements counter (typically placed inside `defer wg.Done()`).
- `wg.Wait()`: Blocks until counter reaches zero.

**`sync.Mutex` vs `sync.RWMutex`:**
- `sync.Mutex`: Mutual exclusion lock. Only one goroutine can read or write at a time.
- `sync.RWMutex`: Multiple readers can acquire `RLock()` concurrently. Writers acquire exclusive `Lock()`, blocking all readers and other writers. Ideal for read-heavy workloads.

**`context.Context` (Cancellation & Timeouts):**
Context provides a standard mechanism to propagate cancellation signals, deadlines, and trace metadata down a call tree across API boundaries and goroutines. Calling `cancel()` terminates downstream operations immediately, preventing goroutine leaks.""",
            "formulas": """1. **Select Multiplexing Rule:**
   If multiple `case` branches are ready simultaneously, `select` chooses one pseudo-randomly with uniform distribution.
2. **Context Timeout Idiom:**
   $$ctx, cancel := \\text{context.WithTimeout}(\\text{context.Background}(), 2\\times\\text{time.Second})$$
   $$\\text{defer } cancel() \\implies \\text{Releases timer resources immediately}$$""",
            "solved_examples": [
                {
                    "title": "Worker Pool with sync.WaitGroup and Context Cancellation",
                    "difficulty": "Hard | Google, Amazon, Microsoft",
                    "problem": "Build a worker pool of 3 concurrent workers processing tasks from a job channel, with graceful shutdown support via context.",
                    "step_by_step": [
                        "Step 1: Create a jobs channel and a `sync.WaitGroup`.",
                        "Step 2: Launch 3 workers with `select` listening to both `jobs` and `ctx.Done()`.",
                        "Step 3: Push jobs, close jobs channel, and call `wg.Wait()`."
                    ],
                    "code_or_math": """package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

func worker(ctx context.Context, id int, jobs <-chan int, wg *sync.WaitGroup) {
    defer wg.Done()
    for {
        select {
        case <-ctx.Done():
            fmt.Printf("Worker %d: Stopped via context\\n", id)
            return
        case job, ok := <-jobs:
            if !ok {
                return // Channel closed
            }
            fmt.Printf("Worker %d: Processed job %d\\n", id, job)
            time.Sleep(50 * time.Millisecond)
        }
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
    defer cancel()

    jobs := make(chan int, 10)
    var wg sync.WaitGroup

    // Launch 3 workers
    for w := 1; w <= 3; w++ {
        wg.Add(1)
        go worker(ctx, w, jobs, &wg)
    }

    // Send jobs
    for j := 1; j <= 6; j++ {
        jobs <- j
    }
    close(jobs)

    wg.Wait()
    fmt.Println("All workers terminated cleanly.")
}""",
                    "explanation": "Context timeout ensures workers do not hang indefinitely, preventing goroutine resource leaks."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why must `wg.Add(1)` be called outside the goroutine before `go worker()` rather than inside the worker function?",
                    "options": [
                        "A) Go compiler throws a syntax error if wg.Add is called inside",
                        "B) If placed inside, the main thread may execute `wg.Wait()` before the spawned goroutines have even started running, exiting prematurely",
                        "C) wg.Add is not thread-safe",
                        "D) It has no effect where it is placed"
                    ],
                    "correct_answer": "B) If placed inside, the main thread may execute `wg.Wait()` before the spawned goroutines have even started running, exiting prematurely",
                    "detailed_solution": "If wg.Add is inside the goroutine, a race condition exists where wg.Wait() executes before the goroutines start and increment the counter."
                }
            ],
            "interview_questions": [
                {
                    "company": "Uber, Google, Cisco",
                    "question": "What is a Goroutine Leak in Go, and how does it happen in production?",
                    "model_answer": "A goroutine leak occurs when a goroutine is launched but becomes permanently blocked waiting on a channel send, channel receive, or unreleased lock, and is therefore never terminated. Because goroutines are not reclaimed by the garbage collector while blocked on channels, their stack memory and referenced heap objects remain allocated permanently. Over time, millions of leaked goroutines consume all system RAM, leading to Out-Of-Memory (OOM) crashes. Common causes include unbuffered channels with no active receiver, or forgetting to pass and listen to `ctx.Done()`.",
                    "interviewer_tip": "Explain that the GC cannot garbage collect a running or blocked goroutine."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Error Handling Idioms, Panic, Recover & Defer Mechanics",
        "key_takeaways": "Master explicit error handling, custom error types, errors.Is/As (Go 1.13+), defer LIFO execution, and panic/recover boundaries.",
        "topics": [
            "Philosophy of Errors as Values: No exceptions in standard control flow",
            "The `error` Built-in Interface: `Error() string`",
            "Sentinel Errors vs Custom Error Structs",
            "Modern Error Wrapping: `fmt.Errorf(\"%w\", err)`, `errors.Is()`, and `errors.As()`",
            "The `defer` Statement: LIFO stack execution and argument evaluation timing",
            "`panic` and `recover`: Graceful crash containment at HTTP server boundaries"
        ],
        "sections": {
            "concept": """Go rejects try-catch exception handling in favor of treating errors as first-class explicit values.

**Error Wrapping (Go 1.13+):**
- Use `fmt.Errorf(\"... %w\", err)` with the `%w` verb to wrap an underlying error into an error chain.
- `errors.Is(err, target)`: Traverses the error chain to check if any unwrapped error matches `target` (replaces `err == target`).
- `errors.As(err, &target)`: Traverses the chain to check if any error matches a specific type and binds it (replaces type assertions).

**The `defer` Statement:**
`defer` defers execution of a function until the surrounding outer function returns:
1. **LIFO Order:** Deferred calls are pushed onto a per-goroutine call stack and executed in Last-In, First-Out order.
2. **Immediate Evaluation of Arguments:** The arguments to deferred functions are evaluated immediately when the `defer` statement is reached, not when the function actually executes!

**Panic and Recover:**
- `panic()` terminates normal execution immediately, unwinding the goroutine's stack and running deferred functions.
- `recover()` can capture a panicking goroutine, but **only if called directly inside a deferred function**. It restores normal execution, preventing process termination.""",
            "formulas": """1. **Defer Execution Order:**
   $$\\text{defer } F_1(); \\quad \\text{defer } F_2(); \\quad \\text{defer } F_3() \\implies \\text{Executed: } F_3() \\to F_2() \\to F_1()$$
2. **Defer Argument Timing:**
   $$\\text{defer fmt.Println}(x) \\implies x \\text{ is captured at defer declaration time}$$""",
            "solved_examples": [
                {
                    "title": "HTTP Panic Recovery Middleware Implementation",
                    "difficulty": "Medium | Amazon, Razorpay, Cloudflare",
                    "problem": "Write a production HTTP middleware function that recovers from unexpected handler panics, logs the stack trace, and returns HTTP 500.",
                    "step_by_step": [
                        "Step 1: Create an HTTP middleware wrapper function.",
                        "Step 2: Inside the handler, `defer` an anonymous function.",
                        "Step 3: Call `r := recover()`; if non-nil, respond with `http.StatusInternalServerError`."
                    ],
                    "code_or_math": """package main

import (
    "fmt"
    "net/http"
)

func RecoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                fmt.Printf("RECOVERED FROM PANIC: %v\\n", rec)
                w.WriteHeader(http.StatusInternalServerError)
                w.Write([]byte("500 - Internal Server Error"))
            }
        }()
        next.ServeHTTP(w, r)
    })
}

func dangerousHandler(w http.ResponseWriter, r *http.Request) {
    var ptr *int = nil
    *ptr = 42 // Will panic with nil pointer dereference!
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/panic", dangerousHandler)
    // Server wrapped with RecoveryMiddleware never crashes!
    fmt.Println("Server configured with recovery middleware.")
}""",
                    "explanation": "Calling recover() inside a deferred function arrests the panicking sequence, allowing HTTP servers to remain resilient."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the output of the following Go code?\nfunc test() (val int) {\n    defer func() { val += 5 }()\n    return 10\n}",
                    "options": [
                        "A) 10",
                        "B) 15",
                        "C) 5",
                        "D) Compilation error"
                    ],
                    "correct_answer": "B) 15",
                    "detailed_solution": "Named return values are initialized to zero and bound to the function scope. The return 10 sets val = 10, then the deferred function runs and increments val to 15 before the function physically exits."
                }
            ],
            "interview_questions": [
                {
                    "company": "HashiCorp, Google, Datadog",
                    "question": "What is the difference between `errors.Is()` and direct error comparison with `==` in modern Go?",
                    "model_answer": "Direct comparison `err == ErrNotFound` only checks the top-level error reference. If the error has been wrapped with context using `fmt.Errorf(\"user repository: %w\", err)`, the equality check fails. `errors.Is()` recursively unwraps the error chain (by inspecting the `Unwrap() error` method), verifying whether the target error appears anywhere within the chain.",
                    "interviewer_tip": "Mention the %w wrap verb and the recursive Unwrap() method."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Building Production Cloud Microservices & Go Placement Challenges",
        "key_takeaways": "Master net/http standard library, JSON streaming encoders, middleware chaining, rate limiting, and top competitive coding challenges.",
        "topics": [
            "Building REST APIs with `net/http` and `http.ServeMux` (Go 1.22 routing)",
            "JSON Handling: `json.Marshal` vs `json.NewDecoder` (Streaming performance)",
            "Middleware Pattern: Chaining decorators for logging, auth, and metrics",
            "Rate Limiting with Token Bucket Algorithm (`golang.org/x/time/rate`)",
            "Graceful Server Shutdown (`server.Shutdown(ctx)`)",
            "Classic FAANG & Placement Coding Challenges Solved in Go"
        ],
        "sections": {
            "concept": """Go has become the undisputed language of the cloud (powering Docker, Kubernetes, Terraform, Prometheus, and Etcd) because its standard library includes production-ready networking and HTTP primitives.

**Streaming JSON vs Buffering:**
- `json.Unmarshal([]byte)`: Requires loading the entire JSON payload into a memory byte buffer first.
- `json.NewDecoder(r.Body).Decode(&data)`: Reads directly from the `io.Reader` stream chunk-by-chunk, minimizing memory allocations and handling large payloads with optimal throughput.

**Graceful HTTP Server Shutdown:**
In containerized cloud environments (Kubernetes), pods receive `SIGTERM` before termination. A production server must:
1. Intercept OS signals via `signal.Notify`.
2. Stop accepting new incoming requests.
3. Wait for existing in-flight connections to complete up to a deadline using `server.Shutdown(ctx)`.""",
            "formulas": """1. **Token Bucket Rate Limiter Formula:**
   $$\\text{Tokens}(t) = \\min(B, \\text{Tokens}(t_0) + (t - t_0) \\times R)$$
   Where $B$ is Burst capacity and $R$ is replenishment rate per second.
2. **JSON Streaming Memory Savings:**
   $$\\text{Memory overhead: } O(1) \\text{ streaming decoder} \\ll O(N) \\text{ memory byte buffer}$$""",
            "solved_examples": [
                {
                    "title": "Production REST API Endpoint with Graceful JSON Validation",
                    "difficulty": "Medium | Google, Uber, Swiggy",
                    "problem": "Write an idiomatic Go HTTP handler that decodes a JSON payload, validates fields, and responds with structured JSON.",
                    "step_by_step": [
                        "Step 1: Define request/response structs with `json:\"key\"` tags.",
                        "Step 2: Use `json.NewDecoder(r.Body)` to parse payload.",
                        "Step 3: Validate input and send JSON response."
                    ],
                    "code_or_math": """package main

import (
    "encoding/json"
    "net/http"
)

type CreateUserRequest struct {
    Username string `json:"username"`
    Email    string `json:"email"`
}

type UserResponse struct {
    ID       int    `json:"id"`
    Username string `json:"username"`
    Status   string `json:"status"`
}

func createUserHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid JSON payload", http.StatusBadRequest)
        return
    }

    resp := UserResponse{
        ID:       101,
        Username: req.Username,
        Status:   "created",
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/api/v1/users", createUserHandler)
    // Server setup ready for deployment
}""",
                    "explanation": "json.NewDecoder reads directly from the request stream, minimizing allocations compared to ioutil.ReadAll."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why is `json.NewDecoder(r.Body).Decode(&req)` preferred over `io.ReadAll(r.Body)` followed by `json.Unmarshal()` in high-throughput HTTP APIs?",
                    "options": [
                        "A) json.NewDecoder performs automatic schema validation",
                        "B) It streams directly from the network socket without copying the entire request body into an intermediate memory buffer, drastically reducing GC allocations",
                        "C) json.Unmarshal cannot parse nested structs",
                        "D) It converts JSON to Protobuf automatically"
                    ],
                    "correct_answer": "B) It streams directly from the network socket without copying the entire request body into an intermediate memory buffer, drastically reducing GC allocations",
                    "detailed_solution": "Streaming decoders avoid loading full byte slices into heap memory, preventing memory spikes under high request volume."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Cloudflare, Swiggy",
                    "question": "How do you achieve Zero-Downtime deployments and graceful shutdown in a Go microservice running inside Kubernetes?",
                    "model_answer": "1. Create a channel listening for `os.Interrupt` and `syscall.SIGTERM`. 2. When Kubernetes sends `SIGTERM`, block main and call `server.Shutdown(ctx)` with a timeout context (e.g. 15 seconds). 3. `Shutdown()` stops listening on the port, closes idle connections, and waits for active requests to finish processing. 4. Release remaining database and cache connections cleanly before allowing the main function to exit.",
                    "interviewer_tip": "Mention SIGTERM and server.Shutdown(ctx)."
                }
            ]
        }
    }
]

