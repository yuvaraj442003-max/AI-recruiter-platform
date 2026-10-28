"""
curriculum_rust.py - 8 Comprehensive Chapters for Rust Systems & Memory-Safe Placement Master Edition.
"""
from typing import List, Dict, Any

RUST_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Rust Philosophy, Cargo Toolchain, Immutability & Primitive Types",
        "key_takeaways": "Master Rust's memory safety guarantees without a garbage collector, Cargo tooling, immutable-by-default variables, shadowing, and scalar/compound types.",
        "topics": [
            "Why Rust? Memory safety without GC, data race freedom, and zero-cost abstractions",
            "Cargo Toolchain: `cargo check`, `cargo build --release`, `cargo test`, `cargo clippy`",
            "Variables: Immutable by default, `mut` keyword, and compile-time constants (`const`)",
            "Variable Shadowing vs Mutability: Re-binding types in the same scope",
            "Primitive Scalar Types (Integers, Floats, Booleans, Chars - 4-byte Unicode)",
            "Compound Types: Arrays (fixed stack buffer) and Tuples (heterogeneous)"
        ],
        "sections": {
            "concept": """Rust is a modern systems programming language that guarantees memory safety and thread safety without requiring a runtime garbage collector. It achieves this entirely at compile time through its strict type system and affine ownership model.

**Core Philosophy:**
1. **Zero-Cost Abstractions:** What you don't use, you don't pay for. High-level idioms compile to the exact same machine assembly as handwritten C.
2. **Immutable by Default:** In Rust, `let x = 5;` declares an immutable binding. Mutability must be explicitly declared with `let mut x = 5;`. This drastically reduces state-mutation bugs.
3. **Variable Shadowing:** Declaring `let x = x + 1;` creates a brand new variable that shadows the previous one. Shadowing allows transforming a value or changing its type without inventing temporary names (e.g., parsing a string into an integer).
4. **Compile-Time Safety Check:** Rust features no NULL pointers, no buffer overflows, and no dangling pointers in safe code.""",
            "formulas": """1. **Cargo Build Pipeline:**
   $$\\text{Source Code } (.rs) \\xrightarrow{\\text{rustc}} \\text{HIR} \\to \\text{MIR} \\xrightarrow{\\text{Borrow Checker}} \\text{LLVM IR} \\to \\text{Native Binary}$$
2. **Char Type Footprint:**
   $$\\text{sizeof}(\\text{char}) = 4 \\text{ bytes (Represents a valid Unicode Scalar Value)}$$""",
            "solved_examples": [
                {
                    "title": "Shadowing vs Mutability in Rust",
                    "difficulty": "Easy | Amazon, Microsoft, Infosys",
                    "problem": "Demonstrate the difference between mutating a variable with `mut` and shadowing a variable, specifically showing type transformation.",
                    "step_by_step": [
                        "Step 1: Declare a string slice `let spaces = \"   \";`.",
                        "Step 2: Shadow the variable with its integer length: `let spaces = spaces.len();`.",
                        "Step 3: Contrast with `let mut`, which would cause a compile error if the type changed."
                    ],
                    "code_or_math": """fn main() {
    // 1. Variable Shadowing allows type change
    let spaces = "   "; // &str
    let spaces = spaces.len(); // usize (shadowed successfully!)
    println!("Spaces count: {}", spaces);

    // 2. Mutability allows value change, but NOT type change
    let mut count = 0;
    count += 1; // Valid
    // count = "one"; // COMPILE ERROR: mismatched types!
    println!("Count: {}", count);
}""",
                    "explanation": "Shadowing allocates a new variable binding in the scope, allowing type changes. Mutability allows modifying the value of the same memory cell, requiring the type to remain strictly unchanged."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why does Rust make variables immutable by default?",
                    "options": [
                        "A) Immutable variables compile faster",
                        "B) To encourage functional programming, reduce accidental state bugs, and enable safe concurrent reading across threads without mutex locks",
                        "C) Because the OS prohibits stack memory mutation",
                        "D) Because Rust does not have pointers"
                    ],
                    "correct_answer": "B) To encourage functional programming, reduce accidental state bugs, and enable safe concurrent reading across threads without mutex locks",
                    "detailed_solution": "Default immutability eliminates an entire class of concurrency and state corruption bugs."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft, Amazon, Cloudflare",
                    "question": "What is the difference between `cargo check` and `cargo build`?",
                    "model_answer": "`cargo check` runs the compiler's parsing, type-checking, and borrow-checking passes without generating the final executable machine code. As a result, `cargo check` is significantly faster (often 3-5x faster) than `cargo build`, making it the standard command during iterative development.",
                    "interviewer_tip": "Mention skip of LLVM code generation."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Ownership, Move Semantics & Deterministic Resource Deallocation (Drop)",
        "key_takeaways": "Master the 3 Ownership Rules, Move vs Copy traits, String vs &str, and deterministic deallocation via the Drop trait.",
        "topics": [
            "The 3 Inviolable Rules of Ownership",
            "Stack vs Heap: Primitive types vs heap-allocated `String`",
            "Move Semantics: Shallow pointer copy + invalidation of the source",
            "The `Copy` Trait: Types that implicitly duplicate on the stack",
            "The `Clone` Trait: Explicit deep heap copying",
            "Resource Reclamation: The `Drop` trait (RAII) and scope exit"
        ],
        "sections": {
            "concept": """Ownership is Rust's most unique feature. It enables complete memory safety without the runtime overhead or pause times of a garbage collector.

**The 3 Rules of Ownership:**
1. Each value in Rust has an **owner**.
2. There can only be **one owner at a time**.
3. When the owner goes out of scope, the value is **automatically dropped** (freed).

**Move Semantics:**
When you assign a heap-allocated variable (like `String`) to another variable (`let s2 = s1;`), Rust copies the pointer, length, and capacity on the stack (a 24-byte shallow copy), and **immediately invalidates `s1`**. Any subsequent access to `s1` produces a compile-time error. This prevents the classical C++ 'double free' bug when variables exit scope.

**Copy Trait vs Clone Trait:**
- **`Copy`:** Types stored entirely on the stack (integers, floats, booleans, chars, tuples of Copy types) implement `Copy`. Assignment duplicates the bits automatically.
- **`Clone`:** For heap types (`String`, `Vec<T>`), duplicating the heap memory requires calling `.clone()` explicitly.""",
            "formulas": """1. **Ownership Invariant:**
   $$\\forall v \\in \\text{Values}, \\quad |\\{ \\text{Owner}(v) \\}| = 1$$
2. **Move Invalidation:**
   $$\\text{let } s_2 = s_1 \\implies s_1 \\text{ marked Uninitialized / Invalid by Compiler}$$""",
            "solved_examples": [
                {
                    "title": "Move Semantics and Ownership Transfer in Functions",
                    "difficulty": "Easy | Google, Microsoft, Meta",
                    "problem": "Show how passing a `String` into a function transfers ownership, making it unusable in the caller, and show how to fix it.",
                    "step_by_step": [
                        "Step 1: Create `let s = String::from(\"hello\");`.",
                        "Step 2: Pass `s` to `take_ownership(s)`.",
                        "Step 3: Attempting to print `s` afterwards yields `error[E0382]: borrow of moved value`.",
                        "Step 4: Fix: Pass a reference `&s` (borrowing) instead of moving ownership."
                    ],
                    "code_or_math": """fn take_ownership(str: String) {
    println!("Received: {}", str);
} // str goes out of scope and drop() frees heap memory!

fn main() {
    let s = String::from("hello");
    take_ownership(s);
    // println!("{}", s); // COMPILE ERROR: value borrowed here after move!

    let s2 = String::from("world");
    borrow_only(&s2);
    println!("Still valid: {}", s2); // Works! s2 was not moved.
}

fn borrow_only(str: &String) {
    println!("Borrowed: {}", str);
}""",
                    "explanation": "Passing a value by value moves ownership into the callee function. To retain ownership, the caller must pass a shared reference &s."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens under the hood when a `String` variable leaves its defining scope in Rust?",
                    "options": [
                        "A) The garbage collector marks it for collection during the next sweep",
                        "B) Rust automatically invokes `Drop::drop()`, which frees the heap buffer immediately and deterministically",
                        "C) It remains in memory until the program terminates",
                        "D) A runtime exception is raised"
                    ],
                    "correct_answer": "B) Rust automatically invokes `Drop::drop()`, which frees the heap buffer immediately and deterministically",
                    "detailed_solution": "Rust automatically injects code to call Drop::drop() at the closing brace of the variable's scope, releasing heap memory immediately."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Cloudflare, Meta",
                    "question": "Why does Rust not allow a type that implements the `Drop` trait to also implement the `Copy` trait?",
                    "model_answer": "If a type implemented both `Copy` and `Drop`, copying an instance would duplicate the resource handler without the type's knowledge. When both copies left scope, both destructors (`drop()`) would execute on the identical underlying resource (such as a file descriptor or heap pointer), causing a catastrophic double-free bug. Therefore, the Rust compiler strictly forbids `Drop` on any type implementing `Copy`.",
                    "interviewer_tip": "Cite the double-free hazard and deterministic destruction."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "References, Borrowing & The Compile-Time Borrow Checker",
        "key_takeaways": "Master Immutable vs Mutable Borrows, the Aliasing XOR Mutability theorem, and explicit Lifetime annotations ('a).",
        "topics": [
            "Borrowing: Accessing data without taking ownership (`&T` and `&mut T`)",
            "The Borrow Checker's Core Invariant: Aliasing XOR Mutability",
            "Dangling Reference Prevention: Lifetimes and compile-time verification",
            "Lifetime Annotations (`'a`): Linking output reference lifetime to input parameters",
            "Lifetime Elision Rules: When annotations are not needed",
            "Non-Lexical Lifetimes (NLL): Scope ends at last usage, not closing brace"
        ],
        "sections": {
            "concept": """Borrowing allows creating references to data without transferring ownership.

**The Golden Rule of the Borrow Checker:**
At any given time, you can have **EITHER**:
1. Any number of immutable references (`&T`) to a resource, **OR**
2. Exactly one mutable reference (`&mut T`),
**BUT NEVER BOTH SIMULTANEOUSLY.**

$$\\text{Data Race Freedom} \\iff (\\text{Multiple Readers}) \\oplus (\\text{Single Writer})$$

**Why This Prevents Data Races:**
A data race occurs when two or more pointers access the same memory concurrently, at least one is writing, and there is no synchronization. By enforcing Aliasing XOR Mutability at compile time, data races and iterator invalidations are rendered mathematically impossible in safe Rust!

**Lifetimes (`'a`):**
Lifetimes guarantee that no reference outlives the data it points to, preventing dangling references. Lifetime annotations don't change how long values live; they describe the relationship between parameters so the compiler can verify memory safety.""",
            "formulas": """1. **Borrow Checker Invariant:**
   $$\\text{Active Borrows} \\subseteq \\{ &T, &T, \\dots \\} \\quad \\lor \\quad \\text{Active Borrows} = \\{ &\\text{mut } T \\}$$
2. **Lifetime Relationship:**
   $$\\text{fn longest<'a>(x: &'a str, y: &'a str) -> &'a str}$$
   $$\\text{Lifetime of output} = \\min(\\text{Lifetime}(x), \\text{Lifetime}(y))$$""",
            "solved_examples": [
                {
                    "title": "Preventing Iterator Invalidation at Compile-Time",
                    "difficulty": "Medium | Google, Amazon, Adobe",
                    "problem": "Show how Rust's borrow checker prevents modifying a vector while iterating over it (a classic bug that causes crashes in C++ and Python).",
                    "step_by_step": [
                        "Step 1: Iterate over vector using an immutable borrow `for num in &vec`.",
                        "Step 2: Try to call `vec.push(42)` inside the loop.",
                        "Step 3: Observe that the borrow checker refuses to compile the code.",
                        "Step 4: Understand the invariant: `vec.push()` requires `&mut vec`, but `&vec` is already active."
                    ],
                    "code_or_math": """fn main() {
    let mut vec = vec![1, 2, 3];

    for num in &vec { // Active immutable borrow (&vec)
        println!("Number: {}", num);
        // vec.push(42); // COMPILE ERROR! cannot borrow `vec` as mutable
                         // because it is also borrowed as immutable
    }
}""",
                    "explanation": "In C++, pushing into a vector while iterating causes reallocation, turning the iterator into a dangling pointer and causing undefined behavior. In Rust, the borrow checker detects this at compile time and rejects it."
                }
            ],
            "practice_questions": [
                {
                    "question": "Which of the following scenarios is rejected by Rust's Borrow Checker at compile time?",
                    "options": [
                        "A) Creating two immutable references to the same struct simultaneously",
                        "B) Creating a mutable reference while an immutable reference is still active in scope",
                        "C) Passing an immutable reference to multiple functions",
                        "D) Reading an immutable reference inside a sub-block"
                    ],
                    "correct_answer": "B) Creating a mutable reference while an immutable reference is still active in scope",
                    "detailed_solution": "Rust forbids having a mutable reference and an immutable reference simultaneously to prevent data races and pointer invalidation."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Microsoft, Cloudflare",
                    "question": "What is the `'static` lifetime in Rust, and what does `T: 'static` mean?",
                    "model_answer": "The `'static` lifetime means the referenced data is guaranteed to live for the entire duration of the program (e.g. string literals stored directly in the read-only binary text segment `let s: &'static str = \"hello\";`). However, when used as a trait bound `T: 'static`, it means that the type `T` does NOT contain any non-static references (it owns its data entirely, such as `String` or `i32`), meaning it can live indefinitely or be sent safely across thread boundaries.",
                    "interviewer_tip": "Distinguish between &'static reference vs T: 'static trait bound."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Structs, Enums, Exhaustive Pattern Matching & Robust Error Handling",
        "key_takeaways": "Master algebraic data types, Option and Result enums, the ? operator, exhaustive match expressions, and custom error types.",
        "topics": [
            "Structs: Classic structs, Tuple Structs, and Unit-like structs",
            "Enums as Algebraic Data Types: Holding variants with heterogeneous data",
            "The `Option<T>` Enum: Eliminating the Billion-Dollar Mistake (Null)",
            "The `Result<T, E>` Enum: Explicit recoverable error handling",
            "Pattern Matching: `match` (exhaustive), `if let`, guards, and binding with `@`",
            "The `?` Operator: Idiomatic error propagation"
        ],
        "sections": {
            "concept": """Rust has no `null` or `nil` keyword. Instead, the possibility of absence is modeled explicitly using the **`Option<T>`** enum:
```rust
enum Option<T> {
    Some(T),
    None,
}
```
Because `Option<T>` and `T` are distinct types, you cannot accidentally use an `Option<T>` as if it were definitely present. You must explicitly unwrap or match it.

**Recoverable Errors with `Result<T, E>`:**
Operations that can fail return `Result<T, E>`:
```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

**The `?` Propagation Operator:**
If a function returns `Result`, placing `?` after an expression returning `Result`:
- If `Ok(val)`, unwraps `val` and continues execution.
- If `Err(e)`, returns early from the current function with `Err(From::from(e))`.""",
            "formulas": """1. **The ? Operator Expansion:**
   $$x? \\iff \\text{match } x \\{ \\text{Ok}(v) \\implies v, \\; \\text{Err}(e) \\implies \\text{return Err}(e.\\text{into}()) \\}$$
2. **Exhaustive Matching Invariant:**
   A `match` block must handle every possible enum variant; omitting a case triggers a compile error.""",
            "solved_examples": [
                {
                    "title": "Chaining File Parsing with the ? Operator",
                    "difficulty": "Medium | Amazon, Microsoft, Swiggy",
                    "problem": "Write an idiomatic Rust function to read an integer from a file, parse it, and return the result using the ? operator.",
                    "step_by_step": [
                        "Step 1: Open file with `File::open(\"number.txt\")?`.",
                        "Step 2: Read string into buffer with `file.read_to_string(&mut s)?`.",
                        "Step 3: Parse integer with `s.trim().parse::<i32>()?`.",
                        "Step 4: Wrap final number in `Ok(num)`."
                    ],
                    "code_or_math": """use std::fs::File;
use std::io::{self, Read};

fn read_number_from_file() -> Result<i32, Box<dyn std::error::Error>> {
    let mut file = File::open("number.txt")?; // Propagates io::Error
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;       // Propagates io::Error
    let number = contents.trim().parse::<i32>()?; // Propagates ParseIntError
    Ok(number)
}

fn main() {
    match read_number_from_file() {
        Ok(n) => println!("Parsed integer: {}", n),
        Err(e) => eprintln!("Failed to read/parse: {}", e),
    }
}""",
                    "explanation": "The ? operator propagates errors cleanly up the call stack, converting errors into the return type automatically via the From trait."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the key advantage of Rust's `Option<T>` over nullable pointers in C/Java?",
                    "options": [
                        "A) Option uses 0 bytes of memory",
                        "B) The compiler forces developers to handle the `None` case explicitly before accessing the underlying value, eliminating NullPointerException at compile time",
                        "C) Option can hold multiple values at once",
                        "D) Option automatically retries the operation if None"
                    ],
                    "correct_answer": "B) The compiler forces developers to handle the `None` case explicitly before accessing the underlying value, eliminating NullPointerException at compile time",
                    "detailed_solution": "In Rust, you cannot call methods on Option<T> as if it were T. You must explicitly unpack it using match, if let, or unwrap."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Cloudflare, Meta",
                    "question": "What is the Null Pointer Optimization (NPO) in Rust?",
                    "model_answer": "In Rust, references (`&T`), `Box<T>`, and non-null pointers are guaranteed never to be null. The compiler exploits this invariant when wrapping these types in `Option<T>` (e.g. `Option<&T>` or `Option<Box<T>>`). Instead of adding an extra discriminator tag byte to represent `Some` vs `None`, the compiler uses the 0x0 (null address) to represent `None`, and any non-zero pointer address to represent `Some(ref)`. This means `sizeof(Option<&T>) == sizeof(&T)` (8 bytes), achieving zero memory overhead for nullable references.",
                    "interviewer_tip": "Mention the discriminant optimization and size equality."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Traits, Generics, Trait Bounds & Dynamic Dispatch (dyn Trait)",
        "key_takeaways": "Master Traits as shared behavior, Static Dispatch via Monomorphization, Dynamic Dispatch via Trait Objects (dyn Trait), and Associated Types.",
        "topics": [
            "Traits: Defining shared behavior (Rust's interfaces)",
            "Default Method Implementations and Supertraits",
            "Trait Bounds: `where` clauses, multiple bounds (`T: Display + Clone`)",
            "Static Dispatch: Monomorphization (zero runtime cost)",
            "Dynamic Dispatch: Trait Objects (`Box<dyn Trait>`) and Fat Pointers (data ptr + vtable ptr)",
            "Object Safety Rules: Why some traits cannot be made into trait objects"
        ],
        "sections": {
            "concept": """Traits define interfaces that types can implement. They power both compile-time generics and runtime polymorphism.

**Static Dispatch (Monomorphization):**
When you write `fn process<T: Summary>(item: T)`:
- The compiler generates a specialized copy of the function for each concrete type used at compile time.
- Calls are direct and can be fully inlined.
- Runtime performance cost: **Zero**.
- Trade-off: Slightly larger binary executable size ('code bloat').

**Dynamic Dispatch (`dyn Trait`):**
When types are unknown until runtime (e.g., a collection of different shapes in a vector), Rust uses **Trait Objects** (`&dyn Trait` or `Box<dyn Trait>`):
- Implemented as a **Fat Pointer** (16 bytes on 64-bit architecture):
  1. Pointer to the concrete data object.
  2. Pointer to the class **vtable** (Virtual Method Table).
- Method calls incur a single indirect pointer jump.

**Object Safety:**
A trait is object-safe (can be used as `dyn Trait`) only if:
1. All methods return types that do not mention `Self`.
2. No method has generic type parameters.""",
            "formulas": """1. **Trait Object Fat Pointer:**
   $$\\text{sizeof}(\\&dyn \\text{Trait}) = \\text{Data Pointer} (8\\text{B}) + \\text{Vtable Pointer} (8\\text{B}) = 16 \\text{ bytes}$$
2. **Dispatch Trade-off:**
   $$\\text{Static (Generics)} \\implies \\text{Fastest Execution} \\land \\text{Larger Binary}$$
   $$\\text{Dynamic (dyn Trait)} \\implies \\text{Vtable Lookup Overhead} \\land \\text{Compact Binary}$$""",
            "solved_examples": [
                {
                    "title": "Heterogeneous Collection with Trait Objects (dyn Trait)",
                    "difficulty": "Medium | Google, Microsoft, Adobe",
                    "problem": "Create a `Drawable` trait and store different types (Circle, Square) inside a single vector, drawing them in a loop.",
                    "step_by_step": [
                        "Step 1: Define trait `Drawable` with `fn draw(&self)`.",
                        "Step 2: Implement `Drawable` for `Circle` and `Square`.",
                        "Step 3: Create `vec: Vec<Box<dyn Drawable>>`.",
                        "Step 4: Push boxed instances and iterate polymorphically."
                    ],
                    "code_or_math": """trait Drawable {
    fn draw(&self);
}

struct Circle { radius: f64 }
impl Drawable for Circle {
    fn draw(&self) { println!("Drawing Circle with radius {}", self.radius); }
}

struct Square { side: f64 }
impl Drawable for Square {
    fn draw(&self) { println!("Drawing Square with side {}", self.side); }
}

fn main() {
    let shapes: Vec<Box<dyn Drawable>> = vec![
        Box::new(Circle { radius: 5.0 }),
        Box::new(Square { side: 10.0 }),
    ];

    for shape in shapes {
        shape.draw(); // Dynamic dispatch via vtable
    }
}""",
                    "explanation": "Box<dyn Drawable> allows storing different concrete types in a single homogeneous Vec by wrapping them in uniform fat pointers."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is Monomorphization in Rust's generic compilation model?",
                    "options": [
                        "A) Converting code to bytecode",
                        "B) Duplicating and specializing generic functions for each concrete type used, producing direct non-virtual machine code calls",
                        "C) Compacting memory allocations",
                        "D) Runtime type reflection"
                    ],
                    "correct_answer": "B) Duplicating and specializing generic functions for each concrete type used, producing direct non-virtual machine code calls",
                    "detailed_solution": "Monomorphization is the compile-time expansion of generic code into specialized machine code for each type, providing zero-cost abstractions."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Cloudflare, Meta",
                    "question": "Why can't a trait with a method returning `Self` (like `fn clone(&self) -> Self`) be used as a trait object (`dyn Trait`)?",
                    "model_answer": "Trait objects use dynamic dispatch, meaning the compiler does not know the concrete type of the object behind the pointer. When a method returns `Self`, the size of `Self` is unknown at compile time. Because Rust must know the exact memory size of a return value to allocate stack space for the caller, returning an unknown-sized `Self` violates object safety.",
                    "interviewer_tip": "Cite sizedness and unknown stack frame allocation."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Smart Pointers & Interior Mutability: Box, Rc, Arc, RefCell & Mutex",
        "key_takeaways": "Master Box (heap allocation), Rc (single-threaded ref counting), Arc (atomic ref counting), and RefCell (runtime borrow checking).",
        "topics": [
            "Smart Pointers in Rust: Implementing `Deref` and `Drop`",
            "`Box<T>`: Unique heap allocation and recursive data structures",
            "`Rc<T>`: Reference counting for multiple ownership in single-threaded graphs",
            "`Arc<T>`: Atomic Reference Counting for thread-safe shared ownership",
            "Interior Mutability: Mutating data behind an immutable reference",
            "`RefCell<T>`: Enforcing borrow rules dynamically at runtime (`borrow()` and `borrow_mut()`)"
        ],
        "sections": {
            "concept": """Smart pointers are data structures that act like pointers while offering metadata and capabilities like reference counting.

**Smart Pointer Types:**
1. **`Box<T>`:**
   - Allocates data on the heap.
   - Size of `Box<T>` is strictly 1 pointer (8 bytes).
   - Essential for recursive types (e.g. Linked Lists, Trees) where size cannot be determined at compile time.
2. **`Rc<T>` (Reference Counted):**
   - Allows **multiple owners** of the same heap data in single-threaded programs.
   - Increments reference count on `.clone()`; deallocates data when count reaches 0.
   - Non-thread-safe (uses non-atomic integers for count).
3. **`Arc<T>` (Atomic Reference Counted):**
   - Same as `Rc<T>`, but uses atomic CPU instructions (`fetch_add`) to mutate the reference count safely across multiple threads.
4. **`RefCell<T>` (Interior Mutability):**
   - Allows mutating data even when held behind an immutable reference.
   - Moves the Borrow Checker from **compile-time to runtime**.
   - Calling `ref_cell.borrow_mut()` while another borrow is active causes a **runtime panic** instead of a compile error.""",
            "formulas": """1. **Pointer Selection Matrix:**
   $$\\begin{array}{|l|c|c|c|}
   \\hline
   \\textbf{Smart Pointer} & \\textbf{Ownership} & \\textbf{Thread Safe?} & \\textbf{Borrow Checking} \\\\
   \\hline
   \\text{Box<T>} & \\text{Single (Unique)} & \\text{Yes (if T: Send)} & \\text{Compile-time} \\\\
   \\text{Rc<T>} & \\text{Shared (Ref Count)} & \\textbf{No} & \\text{Compile-time} \\\\
   \\text{Arc<T>} & \\text{Shared (Atomic)} & \\textbf{Yes} & \\text{Compile-time} \\\\
   \\text{RefCell<T>} & \\text{Single} & \\textbf{No} & \\textbf{Runtime Panic} \\\\
   \\text{Arc<Mutex<T>>} & \\text{Shared} & \\textbf{Yes} & \\text{Runtime Blocking} \\\\
   \\hline
   \\end{array}$$""",
            "solved_examples": [
                {
                    "title": "Recursive Binary Tree Node using Box",
                    "difficulty": "Medium | Amazon, Microsoft, TCS Digital",
                    "problem": "Define a recursive Binary Tree structure in Rust and explain why Box<T> is mandatory.",
                    "step_by_step": [
                        "Step 1: A struct containing itself directly has infinite size at compile time.",
                        "Step 2: Wrap child nodes in `Option<Box<TreeNode>>`.",
                        "Step 3: `Box` provides a fixed 8-byte pointer size, allowing the compiler to compute struct size."
                    ],
                    "code_or_math": """struct TreeNode {
    val: i32,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn main() {
    let root = TreeNode {
        val: 10,
        left: Some(Box::new(TreeNode { val: 5, left: None, right: None })),
        right: Some(Box::new(TreeNode { val: 15, left: None, right: None })),
    };

    println!("Root value: {}", root.val);
    if let Some(left_node) = root.left {
        println!("Left child: {}", left_node.val);
    }
}""",
                    "explanation": "Box<T> introduces a layer of indirection, breaking the infinite recursive size dependency."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens if two mutable borrows are taken out simultaneously on a `RefCell<T>` via `borrow_mut()` at runtime?",
                    "options": [
                        "A) The thread blocks until the first borrow finishes",
                        "B) A compile-time error is reported",
                        "C) The program panics immediately with a runtime BorrowMutError",
                        "D) Memory is corrupted silently"
                    ],
                    "correct_answer": "C) The program panics immediately with a runtime BorrowMutError",
                    "detailed_solution": "RefCell enforces borrow rules at runtime. Violating the single-mutable-borrow rule triggers an immediate panic."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google, Meta, Cloudflare",
                    "question": "Why can't `Rc<T>` be sent across thread boundaries in Rust?",
                    "model_answer": "`Rc<T>` updates its reference count using non-atomic operations (standard `count += 1`). If two threads cloned or dropped an `Rc<T>` concurrently, a data race would occur on the counter, leading to inaccurate counts, memory leaks, or premature deallocation causing double-free crashes. Rust's type system prevents this by NOT implementing the `Send` marker trait for `Rc<T>`, causing any attempt to transfer it to another thread to fail at compile time. Use `Arc<T>` for multi-threaded sharing.",
                    "interviewer_tip": "Cite the absence of the Send marker trait."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Fearless Concurrency: Threads, Message Passing (mpsc) & Shared State",
        "key_takeaways": "Master OS thread spawning, move closures, mpsc channels, Arc<Mutex<T>> shared state, and Send/Sync marker traits.",
        "topics": [
            "Rust's Concurrency Guarantee: Data race freedom verified at compile-time",
            "Spawning Threads (`thread::spawn`) and `move` closures",
            "Message Passing Concurrency: `std::sync::mpsc` (Multiple Producer, Single Consumer)",
            "Shared-State Concurrency: `Arc<Mutex<T>>` for synchronized mutation across threads",
            "Deadlocks in Rust: Why Rust prevents data races, but not deadlocks",
            "The `Send` and `Sync` Marker Traits: The compiler's concurrency safety net"
        ],
        "sections": {
            "concept": """Rust's concurrency model is nicknamed **Fearless Concurrency** because the type system prevents data races before your code ever runs.

**The Send and Sync Marker Traits:**
- **`Send`:** Indicates that ownership of a type can be transferred across thread boundaries. Most types are `Send` except raw pointers and `Rc<T>`.
- **`Sync`:** Indicates that it is safe for multiple threads to access a reference `&T` concurrently. A type `T` is `Sync` if and only if `&T` is `Send`.

**Message Passing with `mpsc`:**
- `mpsc` stands for **Multiple Producer, Single Consumer**.
- Channels transfer ownership of values between threads. Once a thread sends a variable through a channel, it can no longer use it (ownership is moved), making race conditions physically impossible.

**Shared State with `Arc<Mutex<T>>`:**
- `Arc` provides multi-thread shared ownership.
- `Mutex` guarantees mutual exclusion.
- Calling `lock()` on a Mutex returns a `MutexGuard<T>` smart pointer that automatically releases the lock when it goes out of scope (RAII lock management).""",
            "formulas": """1. **Sync / Send Equivalence:**
   $$T: \\text{Sync} \\iff \\&T: \\text{Send}$$
2. **Mutex Invariant:**
   $$\\text{Only } 1 \\text{ active } MutexGuard \\text{ at any time across all threads}$$""",
            "solved_examples": [
                {
                    "title": "Thread-Safe Counter with Arc and Mutex",
                    "difficulty": "Medium | Amazon, Google, Microsoft",
                    "problem": "Spawn 5 threads to increment a shared counter 100 times each using Arc and Mutex.",
                    "step_by_step": [
                        "Step 1: Wrap counter in `counter = Arc::new(Mutex::new(0))`.",
                        "Step 2: In a loop, clone the `Arc` pointer: `let counter_clone = Arc::clone(&counter)`.",
                        "Step 3: Spawn thread with `move` closure and acquire lock: `let mut num = counter_clone.lock().unwrap();`.",
                        "Step 4: Join all thread handles to await completion."
                    ],
                    "code_or_math": """use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..5 {
        let counter_clone = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            for _ in 0..100 {
                let mut num = counter_clone.lock().unwrap();
                *num += 1;
            } // MutexGuard is dropped here, unlocking the mutex!
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Final Counter Value: {}", *counter.lock().unwrap()); // 500
}""",
                    "explanation": "Arc allows multiple threads to own references to the same Mutex, and Mutex ensures atomic synchronization."
                }
            ],
            "practice_questions": [
                {
                    "question": "Which marker trait in Rust allows a type's ownership to be transferred safely between different threads?",
                    "options": [
                        "A) Copy",
                        "B) Send",
                        "C) Sync",
                        "D) Drop"
                    ],
                    "correct_answer": "B) Send",
                    "detailed_solution": "The Send marker trait indicates that ownership of the type can be transferred across thread boundaries."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Cloudflare, Swiggy",
                    "question": "Does Rust guarantee that your code will never encounter a Deadlock at runtime?",
                    "model_answer": "No. Rust guarantees Data Race Freedom, but it does NOT prevent logical deadlocks. If Thread A acquires Lock 1 and waits for Lock 2, while Thread B acquires Lock 2 and waits for Lock 1, a classical deadlock occurs. Deadlock freedom is a runtime behavioral property that cannot be checked completely at compile time without restricting programming expressiveness.",
                    "interviewer_tip": "Explicitly distinguish between Data Race freedom (guaranteed) and Deadlock freedom (not guaranteed)."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Unsafe Rust, FFI, Performance Tuning & Placement Systems Challenges",
        "key_takeaways": "Master the 5 Unsafe Superpowers, raw pointers (*const T, *mut T), C Foreign Function Interface (FFI), and systems coding challenges.",
        "topics": [
            "The `unsafe` Keyword: Bypassing the borrow checker for systems programming",
            "The 5 Unsafe Superpowers (Dereference raw pointers, call unsafe functions, mutate static mut)",
            "Raw Pointers (`*const T` and `*mut T`): Bypassing lifetime and null checks",
            "Foreign Function Interface (FFI): Calling C functions (`extern \"C\"`) from Rust",
            "SIMD Vectorization and Zero-Cost Systems Coding Optimization",
            "Classic Placement Systems Coding Challenges Solved in Idiomatic Rust"
        ],
        "sections": {
            "concept": """Safe Rust guarantees that your code cannot exhibit undefined behavior. However, certain low-level hardware operations (such as memory-mapped I/O, calling C libraries, or building custom allocators) cannot be proved safe by the compiler. For these tasks, Rust provides **Unsafe Rust**.

**The 5 Unsafe Superpowers:**
Inside an `unsafe { ... }` block, you can:
1. Dereference raw pointers (`*const T`, `*mut T`).
2. Call an unsafe function or method.
3. Implement an unsafe trait (`unsafe impl Send for MyType`).
4. Mutate mutable static variables.
5. Access fields of a `union`.

**Raw Pointers vs References:**
Unlike Rust references, raw pointers:
- Can be NULL.
- Are allowed to ignore borrowing rules (multiple active mutable pointers to same memory).
- Are not tracked by the borrow checker.
- Creating a raw pointer is safe; **dereferencing** it requires an `unsafe` block.""",
            "formulas": """1. **Raw Pointer Dereferencing Rule:**
   $$\\text{let r = } \\&\\text{val as *const i32; (Safe)} \\implies *r \\text{ (Requires unsafe \\{ ... \\})}$$
2. **Safe Abstraction Principle:**
   $$\\text{Unsafe Core} \\subset \\text{Safe Public Wrapper API}$$""",
            "solved_examples": [
                {
                    "title": "Calling C Standard Library `abs` via Foreign Function Interface (FFI)",
                    "difficulty": "Medium | Microsoft, Qualcomm, Nvidia",
                    "problem": "Declare and call the C standard library function `int abs(int)` safely from Rust using FFI.",
                    "step_by_step": [
                        "Step 1: Declare the external C function inside `extern \"C\" { fn abs(input: i32) -> i32; }`.",
                        "Step 2: Wrap the call inside a safe Rust function.",
                        "Step 3: Execute inside `unsafe` block and return verified output."
                    ],
                    "code_or_math": """extern "C" {
    // Declaring external C ABI function
    fn abs(input: i32) -> i32;
}

// Safe wrapper around unsafe C foreign function
fn safe_c_abs(num: i32) -> i32 {
    unsafe {
        abs(num) // Calling external C code requires unsafe
    }
}

fn main() {
    let result = safe_c_abs(-42);
    println!("C abs(-42) result: {}", result); // 42
}""",
                    "explanation": "Because Rust cannot verify the memory safety or correctness of external C code, invoking C functions via FFI requires unsafe blocks."
                }
            ],
            "practice_questions": [
                {
                    "question": "Which of the following actions strictly requires an `unsafe` block in Rust?",
                    "options": [
                        "A) Creating a raw pointer from a reference (`&x as *const i32`)",
                        "B) Dereferencing a raw pointer (`*raw_ptr`)",
                        "C) Calling `.clone()` on an Arc",
                        "D) Iterating over a vector"
                    ],
                    "correct_answer": "B) Dereferencing a raw pointer (`*raw_ptr`)",
                    "detailed_solution": "Creating a raw pointer is safe, but dereferencing it is unsafe because the pointer may be null, dangling, or unaligned."
                }
            ],
            "interview_questions": [
                {
                    "company": "Nvidia, Apple, Google",
                    "question": "What is the 'Safe Abstraction' principle in Rust systems architecture?",
                    "model_answer": "The Safe Abstraction principle is the design pattern where low-level, performance-critical code that requires `unsafe` (e.g. allocating memory, pointer manipulation, system calls) is encapsulated inside a private module, exposing only a strictly safe public API to consumers. Standard library structures like `Vec<T>`, `String`, and `Mutex<T>` are internally implemented using `unsafe`, but their public interfaces are 100% safe, guaranteeing that consumers cannot trigger undefined behavior.",
                    "interviewer_tip": "Cite Vec and String as real-world examples of safe abstractions over unsafe pointer operations."
                }
            ]
        }
    }
]

