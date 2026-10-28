"""
curriculum_cpp.py - 8 Comprehensive Chapters for C++ & Modern STL Placement Master Edition.
"""
from typing import List, Dict, Any

CPP_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Modern C++ Architecture, Namespaces, References & Memory Model",
        "key_takeaways": "Master differences between C and C++, references vs pointers, inline functions, namespaces, and auto type deduction.",
        "topics": [
            "Evolution of C++ (C++11, C++14, C++17, C++20)",
            "References vs Pointers: Syntax, re-seating restrictions, and aliasing rules",
            "Namespaces, Anonymous Namespaces, and the Koenig (ADL) Lookup",
            "Function Overloading, Default Arguments, and Name Mangling",
            "Type Deduction: auto, decltype, and structured bindings",
            "Memory Layout: Stack, Heap, Free Store (new/delete vs malloc/free)"
        ],
        "sections": {
            "concept": """C++ is a multi-paradigm, statically typed, compiled programming language that combines low-level memory control with high-level zero-cost abstractions.

Key Differences from C:
1. **References (`Type&`):** A reference is an immutable alias for an existing lvalue. Unlike pointers, references cannot be NULL, cannot be uninitialized, and cannot be reseated to point to another object after initialization.
2. **Dynamic Memory (`new` / `delete`):** Unlike `malloc()`, `new` automatically calculates the object size, invokes constructors, and returns a strongly-typed pointer. Similarly, `delete` invokes destructors prior to releasing memory.
3. **Namespaces:** Prevent global name collisions. The `inline` namespace provides library versioning, while anonymous namespaces provide translation-unit internal linkage (superior to `static`).
4. **Type Deduction (`auto` & `decltype`):** Introduced in C++11, `auto` deduces the type of a variable from its initializer at compile-time with zero runtime overhead.""",
            "formulas": """1. **Reference vs Pointer Comparison:**
   - Reference: No independent address (`&ref == &original`), non-null, automatic dereferencing.
   - Pointer: Independent memory cell storing an address, can be `nullptr`, requires explicit `*` dereference.
2. **new / delete Mechanics:**
   $$\\text{new } T \\iff \\text{operator new}(\\text{sizeof}(T)) \\xrightarrow{\\text{construct}} T::T()$$
   $$\\text{delete } p \\iff p\\to\\sim T() \\xrightarrow{\\text{free}} \\text{operator delete}(p)$$
3. **Array new / delete Rule:**
   Always pair `new T[]` with `delete[] p` to guarantee each array element's destructor is invoked.""",
            "solved_examples": [
                {
                    "title": "Pass by Reference vs Pass by Pointer in Function Parameters",
                    "difficulty": "Easy | Amazon, TCS, Infosys",
                    "problem": "Write a function to swap two integers without using pointer dereference syntax, and explain why pass-by-reference is preferred in modern C++.",
                    "step_by_step": [
                        "Step 1: Declare function parameters as lvalue references `int &a, int &b`.",
                        "Step 2: Inside the function, manipulate `a` and `b` as standard identifiers; compiler translates them to address offsets.",
                        "Step 3: Call `swapRef(x, y)` cleanly without taking addresses with `&`."
                    ],
                    "code_or_math": """#include <iostream>

void swapRef(int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    int x = 10, y = 20;
    swapRef(x, y);
    std::cout << "x: " << x << ", y: " << y << "\\n"; // x: 20, y: 10
    return 0;
}""",
                    "explanation": "Pass-by-reference avoids pointer null-checks, prevents accidental pointer arithmetic, and provides clean syntax with identical zero-cost assembly generation."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary difference between `malloc()` and the C++ `new` operator?",
                    "options": [
                        "A) malloc() is faster than new",
                        "B) new invokes object constructors; malloc() only allocates raw uninitialized memory bytes",
                        "C) malloc() returns a typed pointer whereas new returns void*",
                        "D) new cannot allocate arrays"
                    ],
                    "correct_answer": "B) new invokes object constructors; malloc() only allocates raw uninitialized memory bytes",
                    "detailed_solution": "The new operator allocates memory from the free store and calls the constructor. malloc() allocates raw bytes from the heap without invoking any constructor."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft, Cisco, Qualcomm",
                    "question": "What is Name Mangling in C++, and why is `extern \"C\"` required when linking C libraries into a C++ codebase?",
                    "model_answer": "C++ supports function overloading (multiple functions sharing the same name with different parameter signatures). To enable the linker to distinguish them, the C++ compiler 'mangles' function names into unique symbols encoding their return type and parameter types (e.g., `_Z7swapRefRiS_`). Because C compilers do not perform name mangling, linking a C function directly from C++ leads to unresolved external symbol errors. Wrapping C function declarations in `extern \"C\" { ... }\" disables C++ name mangling, instructing the linker to use C linkage.",
                    "interviewer_tip": "Mention function overloading and symbol table linkage."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Object-Oriented C++: Classes, Constructors, Destructors & Rule of Three/Five",
        "key_takeaways": "Master class encapsulation, constructor initialization lists, deep copying, move semantics, and the Rule of 5.",
        "topics": [
            "Classes vs Structs in C++ (default visibility)",
            "Member Initialization Lists: Performance vs assignment in constructor body",
            "Destructors and Deterministic Resource Management",
            "Copy Constructor and Copy Assignment Operator (Deep Copy vs Shallow Copy)",
            "C++11 Move Semantics: Rvalue references (`&&`), `std::move`, Move Constructor, Move Assignment",
            "The Rule of Three and The Rule of Five"
        ],
        "sections": {
            "concept": """In C++, an object's lifecycle is strictly deterministic. When an object leaves scope, its destructor is automatically called, guaranteeing resource cleanup without garbage collection pauses.

**Constructor Member Initialization Lists:**
Member variables should always be initialized in the initialization list `ClassName() : member_(val)` rather than inside the constructor body. Initializing in the body first default-constructs the member and then assigns it, resulting in redundant operations.

**Rule of Three (C++98) & Rule of Five (C++11):**
If a class manages a raw resource (such as a heap pointer, file descriptor, or socket), it must explicitly define:
1. Destructor `~ClassName()`
2. Copy Constructor `ClassName(const ClassName&)`
3. Copy Assignment Operator `ClassName& operator=(const ClassName&)`
4. Move Constructor `ClassName(ClassName&&) noexcept` (C++11)
5. Move Assignment Operator `ClassName& operator=(ClassName&&) noexcept` (C++11)

**Move Semantics:**
An lvalue represents an identifiable object residing at a specific memory address. An rvalue is a temporary value that does not persist beyond the expression. Move semantics transfers heap ownership from an rvalue to a new object in $O(1)$ time, avoiding expensive $O(N)$ deep memory copies.""",
            "formulas": """1. **Copy vs Move Complexity:**
   $$\\text{Deep Copy: } O(N) \\text{ memory allocation and element-by-element duplication}$$
   $$\\text{Move Transfer: } O(1) \\text{ pointer swap and source nullification}$$
2. **Value Categories:**
   - **Lvalue:** Has identity, cannot be moved from automatically (`int x = 5;`).
   - **Prvalue:** Pure rvalue, literal or temporary result (`x + 10`).
   - **Xvalue:** Expiring value, explicitly cast to rvalue reference via `std::move(x)`.""",
            "solved_examples": [
                {
                    "title": "Rule of Five String Buffer Class Implementation",
                    "difficulty": "Hard | Google, Amazon, Adobe",
                    "problem": "Implement a minimal Dynamic String Buffer class satisfying the Rule of Five to demonstrate move semantics and prevent double-free errors.",
                    "step_by_step": [
                        "Step 1: Allocate dynamic char array in constructor.",
                        "Step 2: Free dynamic memory in destructor.",
                        "Step 3: Implement Deep Copy constructor and Deep Copy assignment using copy-and-swap idiom.",
                        "Step 4: Implement Move constructor: steal source pointer and set source pointer to nullptr.",
                        "Step 5: Implement Move assignment: clean up existing memory, steal source pointer, clear source."
                    ],
                    "code_or_math": """#include <iostream>
#include <cstring>
#include <utility>

class DynamicString {
private:
    char* data_;
    size_t length_;

public:
    // 1. Constructor
    DynamicString(const char* str = "") {
        length_ = std::strlen(str);
        data_ = new char[length_ + 1];
        std::strcpy(data_, str);
    }

    // 2. Destructor
    ~DynamicString() {
        delete[] data_;
    }

    // 3. Copy Constructor (Deep Copy)
    DynamicString(const DynamicString& other) : length_(other.length_) {
        data_ = new char[length_ + 1];
        std::strcpy(data_, other.data_);
    }

    // 4. Move Constructor (O(1) Resource Steal)
    DynamicString(DynamicString&& other) noexcept : data_(other.data_), length_(other.length_) {
        other.data_ = nullptr;
        other.length_ = 0;
    }

    // 5. Copy Assignment
    DynamicString& operator=(const DynamicString& other) {
        if (this != &other) {
            delete[] data_;
            length_ = other.length_;
            data_ = new char[length_ + 1];
            std::strcpy(data_, other.data_);
        }
        return *this;
    }

    // 6. Move Assignment
    DynamicString& operator=(DynamicString&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            length_ = other.length_;
            other.data_ = nullptr;
            other.length_ = 0;
        }
        return *this;
    }
};""",
                    "explanation": "Move operations are marked noexcept to allow std::vector to safely use move constructors during reallocation."
                }
            ],
            "practice_questions": [
                {
                    "question": "What occurs if a class allocates heap memory in its constructor, but does not define a custom copy constructor?",
                    "options": [
                        "A) The compiler generates a compiler error upon copying",
                        "B) The compiler generates a default shallow copy constructor, copying the pointer address, leading to a double-free runtime crash upon destruction",
                        "C) The program automatically performs a deep copy",
                        "D) Memory is leaked without crashing"
                    ],
                    "correct_answer": "B) The compiler generates a default shallow copy constructor, copying the pointer address, leading to a double-free runtime crash upon destruction",
                    "detailed_solution": "The default copy constructor performs member-wise bitwise copying. Both objects share the identical heap address, causing double-free when both destructors run."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Bloomberg, Morgan Stanley",
                    "question": "What is `std::move()` in modern C++, and does it physically move any data by itself?",
                    "model_answer": "`std::move()` does NOT move any data. It is an unconditional static cast that converts an lvalue expression into an rvalue reference (`static_cast<std::remove_reference_t<T>&&>(val)`). This cast signals to the compiler that the object is expiring and its resources may be stolen by binding to an rvalue move constructor or move assignment operator.",
                    "interviewer_tip": "Explicitly state that std::move produces an rvalue reference cast, and actual moving occurs inside the move constructor."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Inheritance, Dynamic Polymorphism, Virtual Functions & V-Table Internals",
        "key_takeaways": "Master dynamic dispatch, vptr, vtable memory overhead, pure virtual functions, abstract classes, and virtual destructors.",
        "topics": [
            "Access Specifiers in Inheritance: public, protected, private inheritance",
            "Static Dispatch (Compile-time) vs Dynamic Dispatch (Runtime)",
            "Virtual Functions and the `override` / `final` specifiers",
            "Under the Hood: Virtual Method Table (vtable) and Virtual Table Pointer (vptr)",
            "Pure Virtual Functions and Abstract Classes (Interfaces)",
            "Virtual Destructors: Preventing memory leaks in polymorphic hierarchies"
        ],
        "sections": {
            "concept": """Dynamic polymorphism allows a base class pointer or reference to invoke derived class method overrides at runtime.

**Virtual Table Mechanism (vtable & vptr):**
1. For every class containing at least one `virtual` function, the compiler generates a static lookup array called the **vtable** (Virtual Method Table). This array contains function pointers to the most-derived implementations of the virtual functions.
2. Every instance of that class is augmented with a hidden pointer, the **vptr** (Virtual Pointer), pointing to its class's vtable.
3. When `ptr->virtualMethod()` is invoked:
   - Program dereferences `ptr` to find `vptr`.
   - Program looks up the function pointer at the known index offset in `vtable`.
   - Program executes indirect call to the resolved function address.
   Runtime cost: 1 additional pointer dereference + possible CPU cache-miss.

**Crucial Rule: Virtual Destructor in Base Classes:**
If a class is designed to be polymorphic and deleted through a pointer-to-base (`Base *b = new Derived(); delete b;`), the base class destructor **MUST** be declared `virtual`. Without `virtual`, only `~Base()` executes, skipping `~Derived()` and leaking derived resources.""",
            "formulas": """1. **Memory Overhead of Dynamic Polymorphism:**
   $$\\text{Instance Size} = \\text{Member Variables} + \\text{sizeof}(vptr) \\quad (8 \\text{ bytes on 64-bit systems})$$
2. **Virtual Function Resolution Time:**
   $$T = O(1) \\text{ constant-time array index lookup in vtable}$$
3. **Pure Virtual Syntax:**
   $$\\text{virtual void functionName() } = 0;$$""",
            "solved_examples": [
                {
                    "title": "Demonstrating Virtual Destructor Leak Prevention",
                    "difficulty": "Medium | Goldman Sachs, Adobe, CTS",
                    "problem": "Show how omitting virtual from a base destructor causes a memory leak, and write the corrected code.",
                    "step_by_step": [
                        "Step 1: Create class `Base` with a non-virtual destructor.",
                        "Step 2: Create class `Derived` inheriting `Base`, allocating dynamic memory.",
                        "Step 3: Point `Base*` to `Derived` and call `delete ptr`.",
                        "Step 4: Observe that `~Derived()` is never called.",
                        "Step 5: Mark `virtual ~Base()` to ensure correct top-down destruction."
                    ],
                    "code_or_math": """#include <iostream>

class Base {
public:
    Base() { std::cout << "Base Constructed\\n"; }
    // VIRTUAL DESTRUCTOR GUARANTEES POLYMORPHIC CLEANUP
    virtual ~Base() { std::cout << "Base Destructed\\n"; }
};

class Derived : public Base {
private:
    int* buffer_;
public:
    Derived() : buffer_(new int[1000]) { std::cout << "Derived Constructed\\n"; }
    ~Derived() override {
        delete[] buffer_;
        std::cout << "Derived Destructed (Buffer Freed)\\n";
    }
};

int main() {
    Base* p = new Derived();
    delete p; // Calls ~Derived() first, then ~Base()
    return 0;
}""",
                    "explanation": "Declaring ~Base() virtual places the destructor in the vtable. Deleting through a base pointer dynamically dispatches to ~Derived() first."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the size of an empty class in C++, and what is its size if a virtual function is added (on a 64-bit architecture)?",
                    "options": [
                        "A) 0 bytes empty, 4 bytes with virtual function",
                        "B) 1 byte empty (for distinct addressing), 8 bytes with virtual function (for the vptr)",
                        "C) 4 bytes empty, 8 bytes with virtual function",
                        "D) 1 byte empty, 16 bytes with virtual function"
                    ],
                    "correct_answer": "B) 1 byte empty (for distinct addressing), 8 bytes with virtual function (for the vptr)",
                    "detailed_solution": "Empty classes have size 1 byte so that two distinct instances possess unique memory addresses. Adding a virtual function introduces a 64-bit vptr (8 bytes)."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft, Nvidia, Qualcomm",
                    "question": "Can virtual functions be inlined in C++?",
                    "model_answer": "Yes, but only when resolved statically at compile-time (e.g., when invoked directly on an object value `Obj obj; obj.virtualFunc();`). When invoked polymorphically via a pointer or reference (`Base* ptr; ptr->virtualFunc();`), the compiler cannot determine the concrete type at compile-time and must use dynamic dispatch via vtable, which prevents inlining.",
                    "interviewer_tip": "Distinguish between static calls on object instances vs polymorphic pointer/reference calls."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "RAII & Modern Smart Pointers: unique_ptr, shared_ptr, weak_ptr",
        "key_takeaways": "Master Resource Acquisition Is Initialization, eliminate raw delete, solve circular reference memory leaks with weak_ptr.",
        "topics": [
            "The RAII Idiom (Resource Acquisition Is Initialization)",
            "`std::unique_ptr<T>`: Exclusive ownership and move-only semantics",
            "`std::shared_ptr<T>`: Shared ownership and reference-counted control block",
            "`std::make_unique` vs `std::make_shared` (single allocation optimization)",
            "`std::weak_ptr<T>`: Breaking reference cycles in graphs and caches",
            "Custom Deleters for file descriptors, C libraries, and mutex locks"
        ],
        "sections": {
            "concept": """Modern C++ (C++11 through C++20) adheres to the **RAII** architectural pattern: resource lifetime is bound to object lifetime. Resources are acquired in the constructor and released in the destructor.

**Smart Pointer Hierarchy:**
1. **`std::unique_ptr<T>`:**
   - Exclusive ownership model.
   - Zero memory and runtime overhead compared to a raw pointer.
   - Non-copyable; movable only (`std::move`).
   - Create using `std::make_unique<T>()`.
2. **`std::shared_ptr<T>`:**
   - Shared ownership model via an atomic reference count.
   - Allocates a **Control Block** containing: Strong Reference Count, Weak Reference Count, and Custom Deleter.
   - Object is destroyed when strong reference count reaches 0.
   - Use `std::make_shared<T>()` to allocate the managed object and control block in a single contiguous memory block (cache-friendly, avoids two heap allocations).
3. **`std::weak_ptr<T>`:**
   - Non-owning observer pointing to an object managed by `shared_ptr`.
   - Increments weak reference count without incrementing strong count.
   - Solves cyclic reference memory leaks in graphs, trees with parent pointers, and observer patterns.
   - To access the object, convert via `weak.lock()`, returning a valid `shared_ptr` or `nullptr` if expired.""",
            "formulas": """1. **Memory Overhead Comparison:**
   $$\\text{sizeof}(\\text{unique\\_ptr}) = 1 \\times \\text{pointer size} = 8 \\text{ bytes (Zero-cost abstraction)}$$
   $$\\text{sizeof}(\\text{shared\\_ptr}) = 2 \\times \\text{pointer size} = 16 \\text{ bytes (Object Ptr + Control Block Ptr)}$$
2. **Deallocation Condition:**
   $$\\text{Object Deallocated} \\iff \\text{Strong Count} == 0$$
   $$\\text{Control Block Deallocated} \\iff (\\text{Strong Count} == 0) \\land (\\text{Weak Count} == 0)$$""",
            "solved_examples": [
                {
                    "title": "Resolving Circular Dependency Leak Using weak_ptr",
                    "difficulty": "Medium | Amazon, Uber, Microsoft",
                    "problem": "Given two classes A and B where A holds a pointer to B and B holds a pointer to A, demonstrate how shared_ptr causes a memory leak and fix it using weak_ptr.",
                    "step_by_step": [
                        "Step 1: If both classes hold `std::shared_ptr`, when local pointers go out of scope, both strong refcounts remain at 1.",
                        "Step 2: Neither destructor ever fires, creating a silent heap memory leak.",
                        "Step 3: Replace one pointer with `std::weak_ptr`.",
                        "Step 4: Now, strong count correctly decrements to 0, destructors fire, and memory is reclaimed."
                    ],
                    "code_or_math": """#include <iostream>
#include <memory>

class NodeB; // Forward declaration

class NodeA {
public:
    std::shared_ptr<NodeB> b_ptr;
    ~NodeA() { std::cout << "NodeA Destroyed\\n"; }
};

class NodeB {
public:
    std::weak_ptr<NodeA> a_ptr; // FIXED: weak_ptr breaks reference cycle!
    ~NodeB() { std::cout << "NodeB Destroyed\\n"; }
};

int main() {
    {
        auto a = std::make_shared<NodeA>();
        auto b = std::make_shared<NodeB>();
        a->b_ptr = b;
        b->a_ptr = a; // Weak reference does not increment strong count
    } // Both a and b are properly destructed here!
    return 0;
}""",
                    "explanation": "std::weak_ptr observes the NodeA instance without holding ownership, allowing its reference count to reach zero upon exiting scope."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why is `std::make_shared<T>()` preferred over `std::shared_ptr<T>(new T())`?",
                    "options": [
                        "A) make_shared allows custom deleters",
                        "B) make_shared performs a single contiguous memory allocation for both the managed object and the control block, reducing allocation overhead and improving cache locality",
                        "C) make_shared is exception-unsafe",
                        "D) make_shared does not use atomic reference counting"
                    ],
                    "correct_answer": "B) make_shared performs a single contiguous memory allocation for both the managed object and the control block, reducing allocation overhead and improving cache locality",
                    "detailed_solution": "Calling new T() and shared_ptr performs two separate heap allocations. std::make_shared combines the object and control block into a single contiguous allocation."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google, Bloomberg, Goldman Sachs",
                    "question": "Is `std::shared_ptr` thread-safe in C++?",
                    "model_answer": "The reference count operations (increment and decrement) inside the Control Block are atomic and fully thread-safe. However, the managed object itself is NOT thread-safe: concurrent reads and writes to the underlying object without mutex synchronization cause data races. Additionally, reading and writing to the same `shared_ptr` instance across multiple threads requires external synchronization or `std::atomic<std::shared_ptr<T>>`.",
                    "interviewer_tip": "Differentiate between the thread-safety of the control block counter vs the thread-safety of the underlying object."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "C++ Templates, Metaprogramming & Compile-Time Computation",
        "key_takeaways": "Master function and class templates, template specialization, SFINAE, constexpr, and modern C++20 Concepts.",
        "topics": [
            "Function Templates and Class Templates",
            "Template Argument Deduction and Explicit Instantiation",
            "Full Specialization vs Partial Specialization",
            "Compile-Time Programming: `constexpr`, `consteval`, and `if constexpr`",
            "SFINAE (Substitution Failure Is Not An Error) and `std::enable_if`",
            "C++20 Concepts & Constraints: Readable template requirements"
        ],
        "sections": {
            "concept": """C++ templates provide compile-time parametric polymorphism, allowing algorithms and data structures to operate on arbitrary types without runtime overhead.

**Template Instantiation:**
Templates are blueprints. No machine code is emitted when a template is declared. Code is generated only when the template is instantiated with concrete type arguments (e.g., `vector<int>`).

**Specialization:**
- **Full (Explicit) Specialization:** Provides an alternative implementation for a specific concrete type (`template<> class Buffer<bool>`).
- **Partial Specialization:** Specializes a template for a subset of types (e.g., all pointer types `template<typename T> class Buffer<T*>`). *Note: Function templates can only be fully specialized; overload them instead.*

**Compile-Time Computation (`constexpr` & `if constexpr`):**
C++11 introduced `constexpr`, allowing functions to be evaluated at compile-time if arguments are constant expressions. C++17 added `if constexpr`, enabling compile-time branch pruning where untaken branches are not compiled.""",
            "formulas": """1. **Code Bloat Trade-off:**
   $$\\text{Runtime Cost} = 0 \\text{ (Inlined, optimized assembly)}$$
   $$\\text{Binary Size} = O(K \\times M) \\text{ where } K = \\text{instantiations}, M = \\text{template size}$$
2. **C++20 Concept Requirement:**
   $$\\text{template } <\\text{typename } T> \\text{ requires Integral}<T> \\implies \\text{Validates constraints at compile-time}$$""",
            "solved_examples": [
                {
                    "title": "Generic Compile-Time Factorial and Type Safe Print",
                    "difficulty": "Medium | Adobe, Google, Cisco",
                    "problem": "Write a `constexpr` function to compute factorials at compile-time, and demonstrate compile-time branching using `if constexpr`.",
                    "step_by_step": [
                        "Step 1: Define `constexpr unsigned long long factorial(unsigned int n)`.",
                        "Step 2: Evaluate using `constexpr auto val = factorial(10)` verified at compile-time.",
                        "Step 3: Write a template function using `if constexpr (std::is_pointer_v<T>)` to safely dereference pointers or print values directly."
                    ],
                    "code_or_math": """#include <iostream>
#include <type_traits>

// Compile-time evaluation
constexpr unsigned long long factorial(unsigned int n) {
    return (n <= 1) ? 1 : (n * factorial(n - 1));
}

// Compile-time branch pruning
template <typename T>
void smartPrint(const T& item) {
    if constexpr (std::is_pointer_v<T>) {
        if (item) std::cout << "Pointer value: " << *item << "\\n";
        else std::cout << "Nullptr\\n";
    } else {
        std::cout << "Direct value: " << item << "\\n";
    }
}

int main() {
    constexpr auto f10 = factorial(10); // Computed entirely at compile-time
    std::cout << "10! = " << f10 << "\\n";

    int val = 42;
    smartPrint(val);   // Compiles direct branch only
    smartPrint(&val);  // Compiles pointer branch only
    return 0;
}""",
                    "explanation": "if constexpr ensures invalid code branches (such as dereferencing a non-pointer) are pruned during compilation."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is SFINAE in C++ template metaprogramming?",
                    "options": [
                        "A) A runtime exception handling technique",
                        "B) Substitution Failure Is Not An Error: if substituting a deduced type into a template fails, the compiler discards that overload without throwing a compilation error",
                        "C) A static code analysis tool",
                        "D) A memory allocation strategy"
                    ],
                    "correct_answer": "B) Substitution Failure Is Not An Error: if substituting a deduced type into a template fails, the compiler discards that overload without throwing a compilation error",
                    "detailed_solution": "SFINAE allows developers to conditionally enable or disable function templates based on type traits (e.g. std::enable_if)."
                }
            ],
            "interview_questions": [
                {
                    "company": "Nvidia, Apple, Qualcomm",
                    "question": "Why are template definitions typically placed in `.hpp` header files instead of separate `.cpp` translation units?",
                    "model_answer": "The C++ compiler requires the full definition of a template to instantiate it for concrete types. If template definitions are isolated in a `.cpp` file, other translation units including only the `.hpp` declaration will generate compile-time references to symbols that do not exist, causing Linker Error: Unresolved External Symbol. Placing definitions in headers guarantees the compiler can instantiate the necessary code in every translation unit where it is used.",
                    "interviewer_tip": "Mention compilation stages and explicit template instantiation as the alternative."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "STL Sequence Containers: std::vector, std::deque, std::list & Iterator Invalidation",
        "key_takeaways": "Master vector growth amortized O(1), reserve vs resize, deque chunked memory, and iterator invalidation rules.",
        "topics": [
            "Standard Template Library (STL) Architecture: Containers, Iterators, Algorithms",
            "`std::vector`: Dynamic array, geometric growth factor (1.5x vs 2x), capacity vs size",
            "`reserve()` vs `resize()`: Memory allocation mechanics",
            "`std::deque`: Double-ended queue, segmented buffer array, non-contiguous blocks",
            "`std::list` (Doubly Linked List) and `std::forward_list` (Singly Linked List)",
            "Iterator Categories and Iterator Invalidation Rules"
        ],
        "sections": {
            "concept": """STL sequence containers organize elements in a strictly linear sequence.

**`std::vector` Architecture:**
- Implemented as a contiguous dynamic array managed by three internal pointers: `start`, `finish`, and `end_of_storage`.
- When `size == capacity`, inserting an element triggers reallocation:
  1. Allocates new memory buffer of size $K \\times \\text{capacity}$ (typically $2\\times$ in GCC/Clang, $1.5\\times$ in MSVC).
  2. Moves existing elements to the new buffer.
  3. Deallocates the old buffer.
- **Amortized Analysis:** While a single insertion may take $O(N)$ due to reallocation, $N$ successive push operations take $O(N)$ total time, yielding **amortized $O(1)$** insertion.

**`reserve()` vs `resize()`:**
- `vec.reserve(N)`: Allocates capacity for at least $N$ elements without constructing them (`size` remains unchanged).
- `vec.resize(N)`: Changes `size` to $N$, default-constructing new elements if expanding.

**Iterator Invalidation:**
- In `std::vector`, insertions that trigger reallocation invalidate **all** iterators and pointers. Insertions without reallocation invalidate iterators at and after the insertion point.
- In `std::list`, iterators remain valid across insertions and deletions (except iterators referencing the deleted element).""",
            "formulas": """1. **Vector Amortized Insertion Proof:**
   $$\\text{Total Operations for } N \\text{ elements} = N + (1 + 2 + 4 + \\dots + N) = N + 2N = 3N = O(N) \\implies O(1) \\text{ per element}$$
2. **Container Complexity Comparison:**
   $$\\begin{array}{|l|c|c|c|}
   \\hline
   \\textbf{Container} & \\textbf{Random Access} & \\textbf{Push Front} & \\textbf{Push Back} \\\\
   \\hline
   \\text{std::vector} & O(1) & O(N) & O(1) \\text{ amortized} \\\\
   \\text{std::deque} & O(1) & O(1) & O(1) \\\\
   \\text{std::list} & O(N) & O(1) & O(1) \\\\
   \\hline
   \\end{array}$$""",
            "solved_examples": [
                {
                    "title": "Safe Iterator Deletion in std::vector (Erase-Remove Idiom)",
                    "difficulty": "Medium | Amazon, TCS Digital, Cognizant",
                    "problem": "Given a `std::vector<int>`, remove all even numbers without causing undefined behavior from iterator invalidation.",
                    "step_by_step": [
                        "Step 1: Naive loops that do `vec.erase(it)` without updating `it` result in skipping elements or dereferencing invalidated iterators.",
                        "Step 2: Correct approach 1: Assign `it = vec.erase(it)` which returns the valid iterator to the next element.",
                        "Step 3: Modern C++20 idiomatic approach: Use `std::erase_if(vec, predicate)`."
                    ],
                    "code_or_math": """#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8};

    // Method 1: Traditional safe iterator loop
    for (auto it = nums.begin(); it != nums.end(); ) {
        if (*it % 2 == 0) {
            it = nums.erase(it); // Returns next valid iterator
        } else {
            ++it;
        }
    }

    // Method 2 (C++20 std::erase_if):
    // std::erase_if(nums, [](int n) { return n % 2 == 0; });

    for (int n : nums) std::cout << n << " "; // 1 3 5 7
    std::cout << "\\n";
    return 0;
}""",
                    "explanation": "std::vector::erase() shifts elements left and returns an iterator to the element following the removed one."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens to pointers referencing elements in a `std::vector` when `push_back()` causes `capacity()` to exceed its previous value?",
                    "options": [
                        "A) Pointers remain valid and continue pointing to original memory",
                        "B) Pointers are automatically remapped to new addresses",
                        "C) All existing pointers, references, and iterators are invalidated because memory was reallocated to a new buffer",
                        "D) A segmentation fault occurs immediately during insertion"
                    ],
                    "correct_answer": "C) All existing pointers, references, and iterators are invalidated because memory was reallocated to a new buffer",
                    "detailed_solution": "Reallocation moves the entire vector buffer to a fresh heap region and frees old memory, invalidating all existing pointers."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Microsoft, Infosys",
                    "question": "Why is `std::vector` almost always preferred over `std::list` even when many insertions/deletions occur?",
                    "model_answer": "Hardware Cache Locality. `std::vector` stores elements contiguously in memory, enabling CPU prefetchers to load entire cache lines (64 bytes) into L1/L2 cache, making iteration extremely fast. In contrast, `std::list` allocates each node independently on the heap, scattering memory and causing CPU cache misses on virtually every pointer dereference. Furthermore, each node in `std::list` has an 8-16 byte pointer overhead, wasting significant memory.",
                    "interviewer_tip": "Focus on CPU cache lines and spatial locality."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "STL Associative Containers: map, set, unordered_map & Hash Internals",
        "key_takeaways": "Master Red-Black Tree backed ordered containers vs Hash Table unordered containers, custom hash functions, and bucket sizing.",
        "topics": [
            "Ordered Containers: `std::set`, `std::map`, `std::multiset`, `std::multimap`",
            "Under the Hood: Self-balancing Red-Black Trees (Height $\\le 2\\log_2(N+1)$)",
            "Unordered Containers: `std::unordered_set`, `std::unordered_map`",
            "Hash Table Mechanics: Hash function, buckets, load factor, and rehashing",
            "Writing Custom Hash Functions and Equality Operators",
            "Time Complexity Comparison: Average vs Worst-case"
        ],
        "sections": {
            "concept": """Associative containers store elements as key-value pairs or distinct keys, providing fast key-based retrieval.

**Ordered Containers (`std::map`, `std::set`):**
- Implemented as balanced **Red-Black Binary Search Trees**.
- Keys are stored in strictly sorted order using `operator<` (strict weak ordering).
- Guarantee strict $O(\\log N)$ time complexity for Search, Insertion, and Deletion in all cases (including worst-case).

**Unordered Containers (`std::unordered_map`, `std::unordered_set`):**
- Implemented as **Hash Tables** using separate chaining (array of buckets with linked lists).
- Keys are transformed into bucket indices via `std::hash<Key>`.
- Average Time Complexity: $O(1)$ Search, Insert, Delete.
- Worst-case Time Complexity: $O(N)$ when hash collisions degrade buckets into linear lists.
- **Rehashing:** When `load_factor = size / bucket_count` exceeds `max_load_factor` (default 1.0), bucket array size is doubled and all keys are rehashed.""",
            "formulas": """1. **Complexity Comparison:**
   $$\\begin{array}{|l|c|c|c|}
   \\hline
   \\textbf{Operation} & \\textbf{std::map (RB-Tree)} & \\textbf{std::unordered\\_map (Avg)} & \\textbf{std::unordered\\_map (Worst)} \\\\
   \\hline
   \\text{Search / Find} & O(\\log N) & O(1) & O(N) \\\\
   \\text{Insertion} & O(\\log N) & O(1) & O(N) \\\\
   \\text{Deletion} & O(\\log N) & O(1) & O(N) \\\\
   \\hline
   \\end{array}$$
2. **Subscript Operator Warning:**
   `map[key]` automatically default-inserts `key` with a default-constructed value if `key` does not already exist. To inspect without mutating, always use `map.find(key)` or `map.count(key)`.""",
            "solved_examples": [
                {
                    "title": "Custom Struct as Key in std::unordered_map",
                    "difficulty": "Hard | Google, Amazon, Goldman Sachs",
                    "problem": "Create a custom struct `Point { int x, y; }` and use it as a key in `std::unordered_map<Point, std::string>`.",
                    "step_by_step": [
                        "Step 1: Provide `operator==` for equality checking inside buckets.",
                        "Step 2: Specialize `std::hash<Point>` with a hash combination formula (e.g., bitwise shift and XOR).",
                        "Step 3: Instantiate and test map insertion."
                    ],
                    "code_or_math": """#include <iostream>
#include <unordered_map>
#include <string>

struct Point {
    int x;
    int y;

    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

// Specialize std::hash for Point
namespace std {
    template <>
    struct hash<Point> {
        size_t operator()(const Point& p) const noexcept {
            // Hash combining algorithm
            size_t h1 = std::hash<int>{}(p.x);
            size_t h2 = std::hash<int>{}(p.y);
            return h1 ^ (h2 << 1);
        }
    };
}

int main() {
    std::unordered_map<Point, std::string> pointNames;
    pointNames[{0, 0}] = "Origin";
    pointNames[{10, 20}] = "Waypoint A";

    Point target = {0, 0};
    std::cout << "Target: " << pointNames[target] << "\\n"; // Origin
    return 0;
}""",
                    "explanation": "std::unordered_map requires both a hash specialization and an equality operator to detect and resolve bucket collisions."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the key danger of accessing a key using `myMap[key]` in `std::map` when the key is not present?",
                    "options": [
                        "A) It throws std::out_of_range exception",
                        "B) It returns nullptr",
                        "C) It silently inserts the key into the map with a default-constructed value",
                        "D) It corrupts the Red-Black tree"
                    ],
                    "correct_answer": "C) It silently inserts the key into the map with a default-constructed value",
                    "detailed_solution": "operator[] inserts a new key-value pair if the key is not present. Use find() or contains() to read without mutation."
                }
            ],
            "interview_questions": [
                {
                    "company": "Goldman Sachs, Google, Citadel",
                    "question": "When would you deliberately choose `std::map` over `std::unordered_map` despite the $O(\\log N)$ vs $O(1)$ difference?",
                    "model_answer": "1. When data must be iterated in sorted key order (e.g. range queries, printing in alphabetical order). 2. When strict upper/lower bound range queries (`lower_bound()`, `upper_bound()`) are required. 3. When worst-case latency guarantees are mission-critical (high-frequency trading or real-time gaming), because `std::map` strictly guarantees $O(\\log N)$ worst-case without hash collision degradation or unpredictable $O(N)$ rehash spikes.",
                    "interviewer_tip": "Mention sorted iteration and unpredictable rehash latency."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "STL Algorithms, Modern Lambdas & Placement Competitive Coding",
        "key_takeaways": "Master std::sort, binary_search, lambda capture semantics, std::priority_queue, and classical placement interview challenges.",
        "topics": [
            "STL Algorithm Design: Iterator-based non-member functions",
            "Sorting & Searching: `std::sort` (Introsort: Quick + Heap + Insertion), `std::lower_bound`",
            "Modern C++ Lambdas: `[=]`, `[&]`, mutable lambdas, and generic lambdas",
            "Container Adaptors: `std::priority_queue` (Max-heap and Min-heap)",
            "Transformations: `std::transform`, `std::accumulate`, `std::count_if`",
            "Top FAANG Coding Challenges Solved with Modern C++"
        ],
        "sections": {
            "concept": """STL algorithms are decoupled from container implementations through iterators. An algorithm operates on iterator ranges `[first, last)` without knowing whether the underlying data resides in a `vector`, array, or `deque`.

**`std::sort` Architecture (Introsort):**
Modern C++ `std::sort` uses **Introsort**, a hybrid algorithm combining:
1. **Quicksort:** Fast average performance $O(N\\log N)$.
2. **Heapsort:** Switches to Heapsort if recursion depth exceeds $2\\log_2 N$, guaranteeing $O(N\\log N)$ worst-case.
3. **Insertion Sort:** Switches to Insertion Sort for partitions smaller than 16 elements to maximize cache efficiency.

**Lambda Expressions:**
$$\\text{Syntax: } [\\text{capture}]( \\text{params} ) \\to \\text{ret} \\{ \\text{body} \\}$$
- `[]`: Captures nothing.
- `[&]`: Captures all outer variables by reference.
- `[=]`: Captures all outer variables by value (copy).
- `[x, &y]`: Captures `x` by value, `y` by reference.

**`std::priority_queue` Configuration:**
- Default: Max-Heap (`std::priority_queue<int>`).
- Min-Heap: `std::priority_queue<int, std::vector<int>, std::greater<int>>`.""",
            "formulas": """1. **std::sort Complexity:**
   $$O(N \\log N) \\text{ in all cases (worst, average, best)}$$
2. **Binary Search with std::lower_bound:**
   $$O(\\log N) \\text{ comparisons on random-access ranges}$$
3. **Heap Operations:**
   $$\\text{Push: } O(\\log N), \\quad \\text{Pop: } O(\\log N), \\quad \\text{Top: } O(1)$$""",
            "solved_examples": [
                {
                    "title": "Kth Largest Element in an Array (Min-Heap Pattern)",
                    "difficulty": "Medium | Amazon, Microsoft, TCS Digital",
                    "problem": "Given an integer array nums and an integer k, return the kth largest element using modern C++ STL.",
                    "step_by_step": [
                        "Step 1: Maintain a min-heap priority queue of size $k$.",
                        "Step 2: Iterate through nums; push each element.",
                        "Step 3: If heap size exceeds $k$, pop the minimum element.",
                        "Step 4: The top of the min-heap holds the kth largest element in $O(N\\log k)$ time."
                    ],
                    "code_or_math": """#include <iostream>
#include <vector>
#include <queue>

int findKthLargest(const std::vector<int>& nums, int k) {
    // Min-heap storing top k largest elements
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;

    for (int num : nums) {
        minHeap.push(num);
        if (minHeap.size() > static_cast<size_t>(k)) {
            minHeap.pop();
        }
    }
    return minHeap.top();
}

int main() {
    std::vector<int> nums = {3, 2, 1, 5, 6, 4};
    int k = 2;
    std::cout << k << "nd largest element is: " << findKthLargest(nums, k) << "\\n"; // 5
    return 0;
}""",
                    "explanation": "Using a min-heap of capacity k achieves optimal O(N log k) time complexity and O(k) space complexity."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the return value of `std::lower_bound()` on a sorted range `[first, last)` for value `val`?",
                    "options": [
                        "A) An iterator to the first element that is strictly greater than val",
                        "B) An iterator to the first element that is greater than or equal to val",
                        "C) The index of the exact match or -1",
                        "D) A boolean indicating whether val is found"
                    ],
                    "correct_answer": "B) An iterator to the first element that is greater than or equal to val",
                    "detailed_solution": "std::lower_bound returns an iterator pointing to the first element in the range that does not satisfy element < val (i.e., >= val)."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon, Microsoft, Google",
                    "question": "How does `std::sort()` guarantee $O(N\\log N)$ worst-case performance while retaining Quicksort's real-world speed?",
                    "model_answer": "Modern C++ std::sort implements Introsort. It starts with Quicksort. It tracks the recursion depth, and if depth exceeds $2\\log_2 N$ (indicating quadratic worst-case behavior from pathological pivot choices), it automatically switches to Heapsort, which guarantees $O(N\\log N)$ worst-case. For small partitions (<16 elements), it switches to Insertion Sort for maximum CPU cache efficiency.",
                    "interviewer_tip": "Name Introsort and describe the three-phase hybrid approach."
                }
            ]
        }
    }
]

