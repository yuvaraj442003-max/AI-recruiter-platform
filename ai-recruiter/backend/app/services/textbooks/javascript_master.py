"""
javascript_master.py — Prescribed Master Textbook for JavaScript & Modern Web Stack.
Comprehensive unabridged campus placement textbook covering V8 engine architecture,
Event Loop (macrotasks vs microtasks), execution context, hoisting & TDZ, closures,
prototypal inheritance, Promises, async/await, ES6+, TypeScript static typing & generics,
DOM performance, debouncing/throttling, and solved placement coding challenges.
"""

JS_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "JavaScript Engine Internals: V8, Call Stack & The Event Loop",
        "topics": [
            "V8 Engine pipeline: Parser, AST, Ignition bytecode interpreter, TurboFan JIT optimizing compiler",
            "Execution Context lifecycle: Global vs Function context, Creation phase vs Execution phase",
            "Variable Environment, Lexical Environment, and Hoisting mechanics ('var' vs 'let'/'const' Temporal Dead Zone)",
            "The JavaScript Concurrency Model: Call Stack, Web APIs, Task (Macrotask) Queue, and Microtask Queue",
            "Event Loop execution ordering: Processing all Microtasks (Promises, queueMicrotask) before next Macrotask (setTimeout, I/O)"
        ],
        "key_takeaways": "Microtasks (Promise callbacks, MutationObserver) run immediately after the current call stack clears and before any macrotasks (setTimeout, setInterval). 'let' and 'const' are hoisted but remain uninitialized in the Temporal Dead Zone (TDZ)."
    },
    {
        "chapter_num": 2,
        "title": "Scope, Closures & Memory Management in JavaScript",
        "topics": [
            "Lexical scoping and Scope Chain resolution traversal",
            "Closures definition and internal [[Scopes]] property retention",
            "Practical closure design patterns: Private state encapsulation, Module pattern, Function currying, Memoization",
            "Garbage collection algorithms: Reference Counting (and circular reference pitfalls) vs Mark-and-Sweep",
            "Common JavaScript memory leaks: Accidental global variables, forgotten timers, detached DOM nodes, uncleared closures"
        ],
        "key_takeaways": "A closure is created when an inner function retains access to its enclosing lexical scope even after the outer function has finished execution and returned."
    },
    {
        "chapter_num": 3,
        "title": "Objects, Prototypes & Object-Oriented JavaScript",
        "topics": [
            "The Prototype Chain: '__proto__' accessor vs 'prototype' property on constructor functions",
            "Prototypal inheritance mechanics and 'Object.create(proto)' delegation",
            "ES6 'class' syntax as syntactic sugar over prototypal delegation (super, constructor, static methods)",
            "Property descriptors: 'value', 'writable', 'enumerable', 'configurable', and 'Object.freeze()' vs 'Object.seal()'",
            "The 'this' keyword binding rules: Default (window/undefined), Implicit (object method), Explicit (call, apply, bind), New, and Arrow lexical 'this'"
        ],
        "key_takeaways": "Arrow functions do not possess their own 'this', 'arguments', or 'super' bindings; they inherit 'this' lexically from their enclosing execution context at the time of definition."
    },
    {
        "chapter_num": 4,
        "title": "Asynchronous JavaScript: Promises, Async/Await & Concurrency",
        "topics": [
            "The asynchronous paradigm: Callback Hell and inversion of control",
            "Promises (ES6): States (Pending, Fulfilled, Rejected), immutability of settled state, then/catch/finally chaining",
            "Promise concurrency primitives: 'Promise.all()' (fail-fast), 'Promise.allSettled()', 'Promise.race()', 'Promise.any()' (first success)",
            "Async/Await (ES2017) syntax: Desugaring async functions to Generators and Promise resolution runners",
            "Error handling patterns in async workflows: try/catch blocks, unhandledrejection global listeners"
        ],
        "key_takeaways": "Promise.all() rejects immediately if any input promise rejects. Promise.allSettled() waits for all promises to settle regardless of rejection, making it safer for batch parallel requests."
    },
    {
        "chapter_num": 5,
        "title": "Modern ES6+ Features & TypeScript Fundamentals",
        "topics": [
            "Destructuring, Rest & Spread operators ('...'), Default parameters, Template literals",
            "Advanced data structures: Map, Set, WeakMap, and WeakSet (ephemeral object references for GC)",
            "Symbols as unique object property keys and well-known symbols (Symbol.iterator)",
            "Iterators and Generator functions ('function*') with 'yield' keyword mechanics",
            "TypeScript essentials: Static typing, Interfaces vs Type Aliases, Generics, Union & Intersection types",
            "TypeScript utility types: Partial<T>, Required<T>, Readonly<T>, Pick<T, K>, Omit<T, K>, Record<K, T>"
        ],
        "key_takeaways": "WeakMap keys must be objects and are weakly held; if no other reference to the key object exists, it is garbage collected, preventing memory leaks in metadata caching."
    },
    {
        "chapter_num": 6,
        "title": "DOM Manipulation, Browser APIs & Web Performance",
        "topics": [
            "The Critical Rendering Path: HTML Parsing -> DOM Tree -> CSSOM -> Render Tree -> Layout (Reflow) -> Paint -> Composite",
            "Minimizing browser reflows and repaints: DocumentFragment, batch DOM mutations, CSS transforms",
            "Event bubbling, capturing (trickling), and the Event Delegation design pattern ('event.target' vs 'event.currentTarget')",
            "Performance optimization algorithms: Debouncing vs Throttling implementation with closures and timers",
            "Web Storage architectures: LocalStorage (5MB synchronous) vs SessionStorage vs IndexedDB (async NoSQL)"
        ],
        "key_takeaways": "Debouncing postpones execution until a specified quiet period has elapsed with no new events (ideal for search autocomplete). Throttling guarantees execution at regular periodic intervals (ideal for scroll listeners)."
    },
    {
        "chapter_num": 7,
        "title": "Solved Placement Coding Challenges & Output Prediction Puzzles",
        "topics": [
            "Event Loop execution order output tracing puzzles",
            "Tricky 'this' binding and scope output predictions",
            "Handwritten polyfill: Custom Promise.all implementation",
            "Handwritten implementation: Debounce and Throttle functions",
            "Deep Clone algorithm handling circular references and non-serializable objects",
            "Self-assessment practice drills with verified answers"
        ],
        "key_takeaways": "Mastering event loop execution sequences and writing polyfills for Promise.all and debounce from memory is required in frontend technical interviews for companies like Google, Microsoft, and Uber."
    }
]

JS_TEXTBOOK_MARKDOWN = r"""# JavaScript, TypeScript & Modern Web Stack: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** JavaScript, TypeScript & Modern Web Stack  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, frontend engineering technical interviews, and online coding evaluations (Google, Amazon, Flipkart, Uber, Razorpay, TCS Digital) are strictly grounded in the engine mechanics, ECMAScript standards, TypeScript types, and polyfills detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: JavaScript Engine Internals: V8, Call Stack & The Event Loop](#chapter-1-javascript-engine-internals-v8-call-stack--the-event-loop)
  - [1.1 Inside the V8 Engine: Parser, Ignition & TurboFan](#11-inside-the-v8-engine-parser-ignition--turbofan)
  - [1.2 Execution Context: Creation vs Execution Phase](#12-execution-context-creation-vs-execution-phase)
  - [1.3 Hoisting & The Temporal Dead Zone (TDZ)](#13-hoisting--the-temporal-dead-zone-tdz)
  - [1.4 The JavaScript Event Loop, Macrotasks & Microtasks](#14-the-javascript-event-loop-macrotasks--microtasks)
- [Chapter 2: Scope, Closures & Memory Management in JavaScript](#chapter-2-scope-closures--memory-management-in-javascript)
  - [2.1 Lexical Scope & The Scope Chain](#21-lexical-scope--the-scope-chain)
  - [2.2 Deep Dive into Closures](#22-deep-dive-into-closures)
  - [2.3 Practical Closure Design Patterns](#23-practical-closure-design-patterns)
  - [2.4 Garbage Collection & Memory Leaks](#24-garbage-collection--memory-leaks)
- [Chapter 3: Objects, Prototypes & Object-Oriented JavaScript](#chapter-3-objects-prototypes--object-oriented-javascript)
  - [3.1 The Prototype Chain & Prototypal Inheritance](#31-the-prototype-chain--prototypal-inheritance)
  - [3.2 ES6 Classes vs Prototypal Delegation](#32-es6-classes-vs-prototypal-delegation)
  - [3.3 Property Descriptors & Immutability](#33-property-descriptors--immutability)
  - [3.4 The 5 Rules of the `this` Keyword](#34-the-5-rules-of-the-this-keyword)
- [Chapter 4: Asynchronous JavaScript: Promises, Async/Await & Concurrency](#chapter-4-asynchronous-javascript-promises-asyncawait--concurrency)
  - [4.1 The Promise Lifecycle & Chaining Mechanics](#41-the-promise-lifecycle--chaining-mechanics)
  - [4.2 Promise Concurrency APIs (all, allSettled, race, any)](#42-promise-concurrency-apis-all-allsettled-race-any)
  - [4.3 Async/Await Internals (Generators & Runners)](#43-asyncawait-internals-generators--runners)
- [Chapter 5: Modern ES6+ Features & TypeScript Fundamentals](#chapter-5-modern-es6-features--typescript-fundamentals)
  - [5.1 ES6+ Essentials: Spread, Destructuring & Symbols](#51-es6-essentials-spread-destructuring--symbols)
  - [5.2 WeakMap & WeakSet for Memory Management](#52-weakmap--weakset-for-memory-management)
  - [5.3 TypeScript Fundamentals: Interfaces vs Types](#53-typescript-fundamentals-interfaces-vs-types)
  - [5.4 TypeScript Generics & High-Yield Utility Types](#54-typescript-generics--high-yield-utility-types)
- [Chapter 6: DOM Manipulation, Browser APIs & Web Performance](#chapter-6-dom-manipulation-browser-apis--web-performance)
  - [6.1 The Critical Rendering Path & Minimizing Reflows](#61-the-critical-rendering-path--minimizing-reflows)
  - [6.2 Event Bubbling, Capturing & Delegation](#62-event-bubbling-capturing--delegation)
  - [6.3 Debouncing vs Throttling Algorithm Implementation](#63-debouncing-vs-throttling-algorithm-implementation)
- [Chapter 7: Solved Placement Coding Challenges & Output Prediction Puzzles](#chapter-7-solved-placement-coding-challenges--output-prediction-puzzles)
  - [Solved Challenge 1: The Event Loop & Microtask Execution Order](#solved-challenge-1-the-event-loop--microtask-execution-order)
  - [Solved Challenge 2: Handwritten Polyfill for `Promise.all`](#solved-challenge-2-handwritten-polyfill-for-promiseall)
  - [Solved Challenge 3: Handwritten Debounce Function with Immediate Flag](#solved-challenge-3-handwritten-debounce-function-with-immediate-flag)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: JavaScript Engine Internals: V8, Call Stack & The Event Loop

### 1.1 Inside the V8 Engine: Parser, Ignition & TurboFan
Google's V8 engine (powers Chrome and Node.js) executes JavaScript through an advanced Just-In-Time (JIT) compilation pipeline:

```
[ Source Code ] 
       |
       v
[ Parser / Lexer ] -> Generates Abstract Syntax Tree (AST) & Scopes
       |
       v
[ Ignition Bytecode Interpreter ] -> Generates compact bytecode and executes rapidly
       |
       |  (Type Feedback / Profiling)
       v
[ TurboFan JIT Compiler ] -> Optimizes "hot" functions into raw machine code
       |
       v  (Deoptimization if polymorphic type assumptions fail)
[ Native Machine Code / CPU ]
```

1. **Parser & AST:** Breaks JavaScript source text into lexical tokens and builds the Abstract Syntax Tree (AST).
2. **Ignition Interpreter:** Translates AST into bytecode. Starts executing code with near-zero latency without waiting for machine-code compilation.
3. **TurboFan Optimizing Compiler:** Monitors "hot functions" (code executed repeatedly). If parameter types remain monomorphic (e.g., function always called with integers), TurboFan compiles the bytecode directly into highly optimized native CPU assembly. If a type check subsequently fails (polymorphic deoptimization), TurboFan bails out back to Ignition bytecode.

### 1.2 Execution Context: Creation vs Execution Phase
Whenever JavaScript code executes, it does so within an **Execution Context**:
- **Global Execution Context (GEC):** Created when script starts; defines `window` (browser) or `global` (Node), and `this`.
- **Function Execution Context (FEC):** Created whenever a function is invoked.

**Every Execution Context is created in two distinct phases:**
1. **Creation Phase (Memory Allocation):**
   - The engine creates the `Activation Object` / `Lexical Environment`.
   - Allocates memory space for function declarations and variables.
   - Sets the value of `this`.
   - Builds the Scope Chain link to the outer environment.
2. **Execution Phase (Line-by-Line Code Evaluation):**
   - Assigns actual values to variables and executes statements sequentially.

### 1.3 Hoisting & The Temporal Dead Zone (TDZ)
Hoisting is the JavaScript engine's behavior of allocating memory for declarations during the Creation Phase before executing code:

- **Function Declarations:** Fully hoisted along with their function body implementation:
  ```javascript
  sayHello(); // Works perfectly! Outputs: "Hello"
  function sayHello() { console.log("Hello"); }
  ```
- **`var` Declarations:** The variable name is hoisted and initialized to `undefined`:
  ```javascript
  console.log(score); // Outputs: undefined
  var score = 100;
  console.log(score); // Outputs: 100
  ```
- **`let` and `const` Declarations & The TDZ:**
  `let` and `const` variables are hoisted into memory, but are **NOT initialized**. The time window between the start of the block scope and the actual line where the variable is declared is known as the **Temporal Dead Zone (TDZ)**. Accessing the variable inside the TDZ throws an uncatchable `ReferenceError`:
  ```javascript
  // TDZ for user starts here
  console.log(user); // Uncaught ReferenceError: Cannot access 'user' before initialization
  let user = "Alice"; // TDZ ends here
  ```

### 1.4 The JavaScript Event Loop, Macrotasks & Microtasks
JavaScript is single-threaded: it has one Call Stack and one Memory Heap. Asynchronous concurrency is orchestrated by the browser/Node runtime via the **Event Loop**:

```
[ Call Stack ]  <------- Executes synchronous JS frames
      ^
      |
      |   (When Call Stack is 100% EMPTY)
      |
[ Microtask Queue ] <--- HIGHEST PRIORITY: Promise.then(), queueMicrotask(), MutationObserver
      ^                  *Drains entire queue completely before moving on!*
      |
[ Macrotask Queue ] <--- setTimeout(), setInterval(), setImmediate(), I/O, UI Rendering
```

**The Strict Event Loop Execution Order:**
1. Execute synchronous code on the Call Stack until the Call Stack is completely empty.
2. Check the **Microtask Queue**: Drain and execute **ALL** available microtasks until the Microtask Queue is completely empty. (If a microtask enqueues another microtask, that new microtask runs immediately in the same cycle!).
3. Trigger UI Render/Repaint (in browser environments).
4. Take the **single oldest task** from the **Macrotask Queue** and push it onto the Call Stack to execute.
5. Repeat from Step 1.

---

## Chapter 2: Scope, Closures & Memory Management in JavaScript

### 2.1 Lexical Scope & The Scope Chain
JavaScript employs **Lexical Scoping** (Static Scoping): the scope of an identifier is determined by its physical location within the written source code at authoring time, NOT by where or how it is invoked at runtime.
- When an identifier is referenced, the engine searches the current local lexical environment.
- If not found, it traverses upward along the **Scope Chain** to the enclosing outer environment, continuing until it reaches the Global Environment.
- If still not found in the global scope, it throws a `ReferenceError` (in strict mode).

### 2.2 Deep Dive into Closures
**Formal Definition:** A **Closure** is the combination of a function bundled together with references to its surrounding lexical environment (`[[Scopes]]`). A closure gives an inner function access to its outer function's scope even after the outer function has completed execution and its execution context has been popped off the Call Stack.

```javascript
function createCounter(initialValue = 0) {
  let count = initialValue; // Enclosed lexical variable
  return {
    increment() { count++; return count; },
    decrement() { count--; return count; },
    getValue() { return count; }
  };
}

const counterA = createCounter(10);
console.log(counterA.increment()); // 11
console.log(counterA.increment()); // 12
console.log(counterA.getValue());  // 12
// count is completely inaccessible from external global code!
```

### 2.3 Practical Closure Design Patterns
1. **Private Variables & Data Encapsulation:** Emulates private object properties before native `#privateField` syntax was introduced.
2. **Function Currying:** Transforming a function taking multiple arguments $f(a, b, c)$ into a sequence of unary functions $f(a)(b)(c)$:
   ```javascript
   const multiply = a => b => a * b;
   const double = multiply(2);
   console.log(double(5)); // 10
   ```
3. **Memoization Cache:** Storing previous expensive calculation results in an enclosed dictionary:
   ```javascript
   function memoize(fn) {
     const cache = new Map();
     return function(...args) {
       const key = JSON.stringify(args);
       if (cache.has(key)) return cache.get(key);
       const result = fn.apply(this, args);
       cache.set(key, result);
       return result;
     };
   }
   ```

### 2.4 Garbage Collection & Memory Leaks
V8 utilizes the **Mark-and-Sweep** Garbage Collection algorithm:
- The GC designates a set of **GC Roots** (Global window object, currently active stack frames, DOM tree root).
- The GC traverses all object references starting from roots, "marking" every reachable object.
- In the "Sweep" phase, any memory block in the heap not marked as reachable is deallocated.

**The Top 4 JavaScript Memory Leaks:**
1. **Accidental Global Variables:** Assigning `foo = "bar"` without `let/const` attaches `foo` to `window`, preventing GC forever.
2. **Uncleared Timers:** `setInterval(() => { ... })` retains all variables in its callback scope until explicitly passed to `clearInterval()`.
3. **Detached DOM Nodes:** Retaining a JavaScript variable reference to a removed DOM element (`const btn = document.getElementById('btn'); document.body.removeChild(btn);`). The DOM element cannot be freed because `btn` still holds a reference.
4. **Improper Closures:** Giant data structures retained in outer scopes of functions that are kept alive long-term.

---

## Chapter 3: Objects, Prototypes & Object-Oriented JavaScript

### 3.1 The Prototype Chain & Prototypal Inheritance
In JavaScript, inheritance is based on **Objects delegating to Objects** via the Prototype Chain:
- Every JavaScript object has an internal hidden slot `[[Prototype]]`, accessible via `Object.getPrototypeOf(obj)` or `__proto__`.
- When accessing `obj.prop`, if `prop` is not found on `obj` directly, the engine traverses `obj.__proto__`. If not found there, it inspects `obj.__proto__.__proto__`, continuing until it hits `Object.prototype.__proto__ === null`.

```javascript
const animal = {
  eats: true,
  walk() { return "Walking..."; }
};

// Create rabbit with animal as its prototype
const rabbit = Object.create(animal);
rabbit.hops = true;

console.log(rabbit.hops); // true (own property)
console.log(rabbit.eats); // true (inherited from animal via prototype chain)
console.log(rabbit.walk()); // "Walking..."
```

### 3.2 ES6 Classes vs Prototypal Delegation
ES6 `class` syntax is strictly **syntactic sugar** layered over prototype delegation:
```javascript
class Person {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hello, I am ${this.name}`;
  }
}
// Under the hood, this is equivalent to:
// Person.prototype.greet = function() { return `Hello, I am ${this.name}`; };
```

### 3.3 Property Descriptors & Immutability
Every object property is configured with an internal **Property Descriptor**:
- `value`: The stored data value.
- `writable`: If `false`, the property's value cannot be altered via assignment.
- `enumerable`: If `false`, the property is omitted from `for...in` loops and `Object.keys()`.
- `configurable`: If `false`, descriptor attributes cannot be changed and property cannot be deleted.

```javascript
const user = {};
Object.defineProperty(user, 'id', {
  value: 42,
  writable: false,
  configurable: false,
  enumerable: true
});
user.id = 99; // Silent failure in non-strict mode; TypeError in strict mode!
```

**Immutability Levels:**
- `Object.preventExtensions(obj)`: Prevents adding new properties; existing can be modified or deleted.
- `Object.seal(obj)`: Prevents adding/deleting properties; existing writable properties can still be modified.
- `Object.freeze(obj)`: Shallow immutable. Prevents adding, deleting, or modifying existing properties.

### 3.4 The 5 Rules of the `this` Keyword
The value of `this` is evaluated dynamically based on **how the function is called**:

1. **Default Binding:** Standalone invocation `fn()`. In non-strict mode, `this` is `window` (global). In strict mode (`"use strict";`), `this` is `undefined`.
2. **Implicit Binding:** Method invocation `obj.fn()`. `this` refers to the contextual object to the left of the dot (`obj`).
3. **Explicit Binding (`call`, `apply`, `bind`):**
   - `fn.call(context, arg1, arg2)`: Executes immediately with explicit `context`.
   - `fn.apply(context, [arg1, arg2])`: Executes immediately with arguments as an array.
   - `fn.bind(context, arg1)`: Returns a new permanently bound function.
4. **New Binding:** `new ConstructorFn()`. Creates a new empty object `{}` and binds `this` to it.
5. **Arrow Function Lexical `this`:** Arrow functions (`() => {}`) **never** bind their own `this`. They capture `this` from their immediately enclosing lexical scope at definition time. `call`, `apply`, or `bind` cannot alter an arrow function's `this`!

---

## Chapter 4: Asynchronous JavaScript: Promises, Async/Await & Concurrency

### 4.1 The Promise Lifecycle & Chaining Mechanics
A **Promise** represents the eventual completion or failure of an asynchronous operation:
- **Pending:** Initial state; neither fulfilled nor rejected.
- **Fulfilled:** Operation succeeded; produces a resolved value.
- **Rejected:** Operation failed; produces a rejection reason (error).
- Once a Promise reaches **Fulfilled** or **Rejected**, it is **Settled** and permanently immutable.

```javascript
function fetchUserData(userId) {
  return new Promise((resolve, reject) => {
    if (!userId) {
      reject(new Error("UserId is mandatory"));
      return;
    }
    setTimeout(() => {
      resolve({ id: userId, name: "Placement Candidate" });
    }, 100);
  });
}

fetchUserData(101)
  .then(user => {
    console.log("Fetched user:", user.name);
    return user.id; // Returned values are wrapped in a new resolved Promise
  })
  .then(id => {
    console.log("Processed ID:", id);
  })
  .catch(err => {
    console.error("Pipeline failure:", err.message);
  })
  .finally(() => {
    console.log("Cleanup executed unconditionally");
  });
```

### 4.2 Promise Concurrency APIs (all, allSettled, race, any)
| API Method | Resolution Condition | Rejection Condition | Primary Placement Use Case |
|:---|:---|:---|:---|
| `Promise.all([p1, p2])` | Resolves when **ALL** promises fulfill (returns array of results). | **Rejects immediately** on the FIRST promise that rejects (Fail-Fast). | Parallel dependent fetches where all data is mandatory. |
| `Promise.allSettled([p1, p2])` | Resolves when **ALL** promises have settled (fulfilled or rejected). | **Never rejects**. Returns array of `{status: 'fulfilled'\|'rejected', value\|reason}`. | Bulk tasks where partial failures are acceptable (e.g. sending bulk notifications). |
| `Promise.race([p1, p2])` | Settles as soon as the **FIRST** promise settles (fulfills OR rejects). | Rejects if the first settled promise was rejected. | Request timeout races (`Promise.race([fetch(url), timeout(5000)])`). |
| `Promise.any([p1, p2])` | Resolves as soon as the **FIRST** promise fulfills. | Rejects only if **ALL** promises reject (returns `AggregateError`). | Querying redundant CDN mirrors where first successful response wins. |

### 4.3 Async/Await Internals (Generators & Runners)
`async/await` syntax is built on top of ES6 Generator functions (`function*`) and Promises. An `async` function always returns a Promise:
```javascript
// This async/await function:
async function loadDashboard() {
  const user = await fetchUser();
  const stats = await fetchStats(user.id);
  return { user, stats };
}

// Desugars conceptually into a generator execution runner:
function loadDashboardDesugared() {
  return spawn(function* () {
    const user = yield fetchUser();
    const stats = yield fetchStats(user.id);
    return { user, stats };
  });
}
```

---

## Chapter 5: Modern ES6+ Features & TypeScript Fundamentals

### 5.1 ES6+ Essentials: Spread, Destructuring & Symbols
- **Spread & Rest Operators (`...`):**
  - Rest (parameters): `function sum(...nums) { return nums.reduce((a, b) => a + b, 0); }`
  - Spread (arrays/objects): `const cloned = { ...original, timestamp: Date.now() };` (Shallow clone).
- **Symbols:** Primitive datatype guaranteeing unique, non-colliding property keys:
  ```javascript
  const idSym1 = Symbol("id");
  const idSym2 = Symbol("id");
  console.log(idSym1 === idSym2); // false! Guaranteed distinct.
  ```

### 5.2 WeakMap & WeakSet for Memory Management
- **`Map` vs `WeakMap`:**
  - `Map` allows keys of any datatype and prevents keys from being garbage collected as long as the map lives.
  - `WeakMap` keys **MUST be Objects** and are held as **weak references**.
  - If no other reference to a key object exists outside the `WeakMap`, the key object and its associated value are automatically garbage collected.
  - `WeakMap` is not iterable (no `.size`, no `.keys()`) because GC timing is non-deterministic.

### 5.3 TypeScript Fundamentals: Interfaces vs Types
| Feature | TypeScript `interface` | TypeScript `type` Alias |
|:---|:---|:---|
| **Declaration Merging** | Yes: Declaring same interface twice merges properties automatically. | No: Duplicate identifier compilation error. |
| **Primitives & Unions** | Cannot represent union or primitive aliases directly. | Ideal for unions, primitives, tuples: `type Status = 'pending' \| 'approved';` |
| **Extends / Implements** | Extends via `extends` keyword; classes can `implement` interfaces. | Intersects via `&` operator; classes can also implement static object types. |
| **Recommended Usage** | Public library APIs and object/class contract modeling. | Complex union types, tuples, function signatures, and utility compositions. |

### 5.4 TypeScript Generics & High-Yield Utility Types
Generics allow building reusable, type-safe components without resorting to `any`:
```typescript
interface ApiResponse<T> {
  success: boolean;
  timestamp: number;
  data: T;
}

// High-Yield Utility Types Built into TypeScript:
interface UserProfile {
  id: string;
  name: string;
  email: string;
  age?: number;
}

type ReadonlyUser = Readonly<UserProfile>; // All properties immutable
type PartialUser  = Partial<UserProfile>;  // All properties optional
type UserContact  = Pick<UserProfile, 'name' | 'email'>; // Extracts subset
type UserNoId     = Omit<UserProfile, 'id'>;            // Excludes subset
type UserRegistry = Record<string, UserProfile>;         // Map of key -> value
```

---

## Chapter 6: DOM Manipulation, Browser APIs & Web Performance

### 6.1 The Critical Rendering Path & Minimizing Reflows
The browser renders web pages through sequential pipeline stages:

```
[ HTML Parser ] -> [ DOM Tree   ] \
                                     --> [ Render Tree ] -> [ Layout (Reflow) ] -> [ Paint ] -> [ Composite ]
[ CSS Parser  ] -> [ CSSOM Tree ] /
```

- **Reflow (Layout):** Recomputing geometry, widths, heights, and positions of all elements on screen. Triggered by modifying layout-sensitive CSS properties (`width`, `height`, `margin`, `fontSize`, `top`, `display`) or querying layout measurements (`offsetWidth`, `scrollHeight`, `getBoundingClientRect()`).
- **Repaint:** Re-coloring pixels without altering geometry (`color`, `background-color`, `visibility`).
- **Composite:** GPU layers assembled together (`transform`, `opacity`). Triggering composite operations bypasses reflow and repaint entirely, achieving smooth 60fps animations.
- **Optimization Best Practice:** Use `document.createDocumentFragment()` to batch DOM node additions offscreen before inserting into the live DOM tree.

### 6.2 Event Bubbling, Capturing & Delegation
When a user clicks an element inside the DOM, the event travels in 3 distinct phases:
1. **Capturing Phase:** Event trickles down from `window` $\to$ `document` $\to$ parent elements to the target.
2. **Target Phase:** Event reaches the actual node clicked (`event.target`).
3. **Bubbling Phase:** Event bubbles upward from target back to `window`.

**Event Delegation Pattern:**
Instead of attaching 1,000 separate `click` event listeners to individual table rows or list items, attach a **single** listener to the parent container and inspect `event.target`:
```javascript
document.getElementById('user-list').addEventListener('click', function(e) {
  const item = e.target.closest('.user-item');
  if (item) {
    console.log("Clicked user ID:", item.dataset.id);
  }
});
```

### 6.3 Debouncing vs Throttling Algorithm Implementation
- **Debouncing:** Delays execution of a function until after $N$ milliseconds of silence have passed since the last invocation. (Best for search inputs, resize listeners).
- **Throttling:** Ensures that a function is executed at most once per every $N$ milliseconds interval. (Best for scroll position tracking, mousemove games).

---

## Chapter 7: Solved Placement Coding Challenges & Output Prediction Puzzles

### Solved Challenge 1: The Event Loop & Microtask Execution Order
- **Puzzle:** Predict the exact printed console output order of the following snippet:
  ```javascript
  console.log("1");

  setTimeout(() => {
    console.log("2");
  }, 0);

  Promise.resolve()
    .then(() => {
      console.log("3");
    })
    .then(() => {
      console.log("4");
    });

  console.log("5");
  ```
- **Step-by-Step Execution Trace:**
  1. Synchronous statement `console.log("1")` executes $\implies$ Prints **`1`**.
  2. `setTimeout(..., 0)` registers a timer with the browser Web API. When timer finishes, callback `() => console.log("2")` is queued in the **Macrotask Queue**.
  3. `Promise.resolve().then(...)` registers microtask `() => console.log("3")` in the **Microtask Queue**.
  4. Synchronous statement `console.log("5")` executes $\implies$ Prints **`5`**.
  5. Synchronous stack is now completely empty. Event loop checks the **Microtask Queue**:
     - Executes first microtask $\implies$ Prints **`3`**.
     - Its chained `.then()` queues another microtask `() => console.log("4")` in the current Microtask Queue!
     - Microtask queue is not empty yet. Engine executes next microtask $\implies$ Prints **`4`**.
  6. Microtask queue is now empty. Event loop pulls from **Macrotask Queue**:
     - Executes `setTimeout` callback $\implies$ Prints **`2`**.
- **Final Output:**
  ```
  1
  5
  3
  4
  2
  ```

### Solved Challenge 2: Handwritten Polyfill for `Promise.all`
- **Problem:** Implement a custom `promiseAll(iterable)` polyfill matching native `Promise.all` behavior without using the built-in method.
- **Solution:**
  ```javascript
  function promiseAll(promises) {
    return new Promise((resolve, reject) => {
      // Handle non-array or empty input
      if (!Array.isArray(promises)) {
        return reject(new TypeError("Argument must be an array"));
      }
      
      const total = promises.length;
      if (total === 0) {
        return resolve([]);
      }
      
      const results = new Array(total);
      let completedCount = 0;
      
      promises.forEach((promiseItem, index) => {
        // Wrap with Promise.resolve to handle primitive non-promise values
        Promise.resolve(promiseItem)
          .then(value => {
            results[index] = value; // Preserve original input ordering!
            completedCount++;
            if (completedCount === total) {
              resolve(results);
            }
          })
          .catch(error => {
            // Reject immediately on FIRST error encountered (fail-fast)
            reject(error);
          });
      });
    });
  }
  ```

### Solved Challenge 3: Handwritten Debounce Function with Immediate Flag
- **Problem:** Implement a robust `debounce(fn, wait, immediate)` utility in JavaScript.
- **Solution:**
  ```javascript
  function debounce(fn, wait = 300, immediate = false) {
    let timeoutId = null;
    
    return function debounced(...args) {
      const context = this;
      const callNow = immediate && !timeoutId;
      
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      
      timeoutId = setTimeout(() => {
        timeoutId = null;
        if (!immediate) {
          fn.apply(context, args);
        }
      }, wait);
      
      if (callNow) {
        fn.apply(context, args);
      }
    };
  }
  ```

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Tricky Scope):** What is printed by the following code?
   ```javascript
   for (var i = 0; i < 3; i++) {
     setTimeout(() => console.log(i), 100);
   }
   ```
   - *Solution:* Prints `3, 3, 3`. Because `var` is function-scoped (or globally scoped here), all three `setTimeout` callbacks reference the exact same mutable variable `i`, which reaches `3` by the time the timer callbacks execute. Replacing `var` with block-scoped `let` creates a fresh `i` binding per loop iteration, printing `0, 1, 2`.

2. **Exercise 2 (Arrow Function 'this'):** What is printed by `obj.getGreeting()`?
   ```javascript
   const obj = {
     name: "Placement Candidate",
     getGreeting: () => `Hello, ${this.name}`
   };
   ```
   - *Solution:* Prints `"Hello, undefined"` (or `"Hello, "` in browsers where `window.name` is empty). Arrow functions inherit `this` lexically from their enclosing scope (here, the global window/module), NOT from the object literal `obj`.

3. **Exercise 3 (WeakMap Object Lifespan):** Can a JavaScript primitive string like `"authToken"` be used as a key in a `WeakMap`?
   - *Solution:* **No**. `WeakMap` keys must strictly be objects (`typeof key === 'object' && key !== null`). Supplying a primitive throws an uncatchable `TypeError: Invalid value used as weak map key`.

4. **Exercise 4 (Promise.race vs Promise.any):** If promise $P_1$ rejects after 10ms with error $E$, and promise $P_2$ resolves after 50ms with value $V$, what will `Promise.race([P1, P2])` and `Promise.any([P1, P2])` return?
   - *Solution:* `Promise.race` rejects after 10ms with error $E$ (first to settle). `Promise.any` ignores the rejection and resolves after 50ms with value $V$ (first to fulfill).

5. **Exercise 5 (Event Delegation Benefits):** Why does event delegation conserve client memory when rendering a virtualized list of 10,000 table rows?
   - *Solution:* Instead of instantiating 10,000 distinct closure functions and event listener objects in the V8 heap, event delegation instantiates strictly 1 listener on the table element. When rows are dynamically inserted or recycled during scrolling, no listener teardown or re-attachment is required.
"""

JS_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "JavaScript Engine Internals: V8, Call Stack & The Event Loop",
        "subtopic": "Event Loop Task Priorities",
        "question": "In the JavaScript Event Loop, which queue is checked and completely drained immediately after the Call Stack becomes empty, before any setTimeout callbacks are executed?",
        "options": [
            "The Microtask Queue (Promise.then, queueMicrotask)",
            "The Macrotask Queue",
            "The Web API Network Queue",
            "The Garbage Collection Sweep Queue"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [JS Prescribed Textbook — Chapter 1: Engine Internals & Event Loop]\nMicrotasks (Promises, MutationObserver, queueMicrotask) have absolute priority over macrotasks. The event loop drains all pending microtasks completely before executing the next macrotask (setTimeout, setInterval).",
        "difficulty": "medium",
    },
    {
        "chapter_num": 3,
        "chapter_title": "Objects, Prototypes & Object-Oriented JavaScript",
        "subtopic": "Arrow Function this Binding",
        "question": "How is the 'this' keyword evaluated inside a standard JavaScript ES6 arrow function?",
        "options": [
            "It inherits 'this' lexically from its enclosing execution context at the time of definition",
            "It binds to the object to the left of the calling dot",
            "It defaults to the global window object in all strict modes",
            "It is dynamically assigned to the function's prototype"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [JS Prescribed Textbook — Chapter 3: Prototypes & this]\nArrow functions do not bind their own 'this'. Instead, they capture 'this' lexically from the scope in which they were created.",
        "difficulty": "easy",
    }
]

JAVASCRIPT_MASTER_CHAPTERS = JS_MASTER_CHAPTERS
JAVASCRIPT_TEXTBOOK_MARKDOWN = JS_TEXTBOOK_MARKDOWN
JAVASCRIPT_EXPANDED_QUESTIONS = JS_EXPANDED_QUESTIONS
