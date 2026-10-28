"""
generate_js_os_cn_dbms.py - Generates exhaustive 8-chapter curricula for:
1. JavaScript & TypeScript
2. Operating Systems
3. Computer Networks
4. DBMS & System Design
"""
from pathlib import Path

CURRICULUM_DIR = Path(__file__).resolve().parent.parent / "backend" / "app" / "services" / "comprehensive_curriculum"
CURRICULUM_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. JAVASCRIPT & TYPESCRIPT CURRICULUM
# -------------------------------------------------------------
def build_javascript_module():
    content = '''"""
curriculum_javascript.py - 8 Comprehensive Chapters for Modern JavaScript & TypeScript.
"""
from typing import List, Dict, Any

JAVASCRIPT_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "JavaScript Engine Architecture, Execution Context & Event Loop",
        "key_takeaways": "Master V8 Call Stack, Memory Heap, Microtask Queue (Promises) vs Macrotask Queue (setTimeout), and execution contexts.",
        "topics": [
            "V8 Engine architecture: Ignition interpreter, TurboFan optimizing compiler",
            "Execution Context: Creation phase (hoisting), Execution phase, Call Stack",
            "The Event Loop: Single-threaded non-blocking runtime dynamics",
            "Task Queues: Microtask Queue (process.nextTick, Promise.then) vs Macrotask Queue (setTimeout, setInterval, I/O)",
            "Hoisting: var (undefined) vs let/const (Temporal Dead Zone - TDZ)"
        ],
        "sections": {
            "concept": """JavaScript is a single-threaded, non-blocking, asynchronous concurrent runtime powered by an engine such as Google's V8.

**Execution Context & Hoisting:**
When JavaScript runs code, it creates an Execution Context in two phases:
1. **Creation Phase:** Memory is allocated for variables and functions. Function declarations are hoisted completely into memory. Variables declared with `var` are initialized to `undefined`. Variables declared with `let` and `const` are hoisted but uninitialized, placing them in the **Temporal Dead Zone (TDZ)** where accessing them before declaration throws `ReferenceError`.
2. **Execution Phase:** Code is evaluated line-by-line.

**The Event Loop:**
Because the Call Stack is single-threaded, asynchronous callbacks are offloaded to Web APIs. Upon completion, callbacks enter queues:
- **Microtask Queue:** Promise callbacks (`.then()`, `.catch()`, `async/await`), `queueMicrotask`, `MutationObserver`.
- **Macrotask Queue:** `setTimeout`, `setInterval`, `setImmediate`, DOM events.
The Event Loop continuously checks: whenever the Call Stack empties, it drains the **entire Microtask Queue** before picking a single task from the Macrotask Queue!""",
            "formulas": """1. **Event Loop Priority Rule:**
   $$\\\\text{Call Stack Empty} \\\\implies \\\\text{Flush ALL Microtasks} \\\\to \\\\text{Render Frame (if due)} \\\\to \\\\text{Execute ONE Macrotask}$$
2. **Temporal Dead Zone (TDZ):**
   $$\\\\text{Start of block} \\\\to \\\\text{Variable Declaration} \\\\implies \\\\text{TDZ (Access throws ReferenceError)}$$""",
            "solved_examples": [
                {
                    "title": "Predicting Event Loop Output with Promises and Timers",
                    "difficulty": "Medium | Amazon, Google, Uber",
                    "problem": "Determine the exact console output order of the following snippet.",
                    "step_by_step": [
                        "Step 1: `console.log(1)` is synchronous; logs 1 immediately.",
                        "Step 2: `setTimeout` queues a Macrotask callback for logging 2.",
                        "Step 3: `Promise.resolve().then(...)` queues a Microtask callback for logging 3.",
                        "Step 4: `console.log(4)` is synchronous; logs 4 immediately.",
                        "Step 5: Call stack empty. Drains Microtask Queue: logs 3.",
                        "Step 6: Microtasks clear. Picks Macrotask: logs 2."
                    ],
                    "code_or_math": """console.log(1);

setTimeout(() => {
    console.log(2);
}, 0);

Promise.resolve().then(() => {
    console.log(3);
});

console.log(4);

// Output:
// 1
// 4
// 3
// 2""",
                    "explanation": "Synchronous code runs first (1, 4), then Microtasks execute before Macrotasks (3, then 2)."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens if a microtask continually schedules another microtask inside a recursive loop?",
                    "options": [
                        "A) Browser automatically stops after 100 iterations",
                        "B) Starves the event loop, freezing UI rendering and preventing macrotasks from running",
                        "C) Throws Maximum Call Stack Exceeded error",
                        "D) Offloads to Web Worker"
                    ],
                    "correct_answer": "B) Starves the event loop, freezing UI rendering and preventing macrotasks from running",
                    "detailed_solution": "The event loop must exhaust all microtasks before yielding control, so an endless microtask loop starves macrotasks and DOM repaints."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "Explain the Temporal Dead Zone (TDZ) and why let/const differ from var.",
                    "model_answer": "Variables declared with `let` and `const` are hoisted to the top of their block scope during the creation phase, but unlike `var` (which is initialized to `undefined`), they remain completely uninitialized. The TDZ is the span of code from the start of the enclosing block until the line where the variable is explicitly declared. Accessing the variable within the TDZ throws a `ReferenceError`.",
                    "interviewer_tip": "Cite block scoping and preventing use before initialization."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Scopes, Closures & Prototype Inheritance",
        "key_takeaways": "Master lexical scope, closures, prototype chain (__proto__ vs prototype), Object.create, and Function.prototype.bind/call/apply.",
        "topics": [
            "Lexical Scoping and Scope Chain traversal",
            "Closures: Private variables and module patterns",
            "Prototype Chain: Object.prototype, Function.prototype, constructor functions",
            "Inheritance in ES5 (Object.create, call) vs ES6 class syntax (syntactic sugar)",
            "this binding rules: Default, Implicit, Explicit (call/apply/bind), and Arrow functions"
        ],
        "sections": {
            "concept": """JavaScript uses **Lexical Scoping**: variable access is determined by physical code structure at write time. A **Closure** is created when an inner function retains access to variables from its outer lexical scope even after the outer function has finished executing and returned.

**Prototype Inheritance:**
Unlike class-based languages (C++, Java), JavaScript uses prototypical inheritance: objects inherit properties directly from other objects via an internal link (`[[Prototype]]`, accessible via `Object.getPrototypeOf(obj)` or `__proto__`). When a property is queried on an object, JavaScript checks the object itself; if missing, it walks up the prototype chain until reaching `Object.prototype` (whose prototype is `null`).

**The `this` Keyword:**
`this` is determined dynamically at call time based on call-site:
1. `obj.method()`: Implicit binding to `obj`.
2. `fn.call(ctx, ...)`: Explicit binding to `ctx`.
3. `new Constructor()`: Bound to newly allocated object.
4. Arrow functions: Do NOT have their own `this`; they inherit `this` lexically from enclosing scope.""",
            "formulas": """1. **Prototype Chain Resolution:**
   $$\\\\text{obj.prop} \\\\implies \\\\text{obj} \\\\to \\\\text{obj.\\\\_\\\\_proto\\\\_\\\\_} \\\\to \\\\dots \\\\to \\\\text{Object.prototype} \\\\to \\\\text{null}$$
2. **Arrow Function this Invariant:**
   $$\\\\text{ArrowFunction.this} \\\\equiv \\\\text{EnclosingLexicalScope.this}$$""",
            "solved_examples": [
                {
                    "title": "Creating a Private Counter via Closures",
                    "difficulty": "Easy | Amazon, Microsoft, TCS",
                    "problem": "Create a function `createCounter()` that encapsulates state, exposing `increment()`, `decrement()`, and `getValue()` without allowing direct modification of the count variable.",
                    "step_by_step": [
                        "Step 1: Declare private variable `count = 0` inside outer function.",
                        "Step 2: Return an object containing closure methods that read and mutate `count`.",
                        "Step 3: External code cannot access `count` directly."
                    ],
                    "code_or_math": """function createCounter(initialValue = 0) {
    let count = initialValue; // Enclosed private state

    return {
        increment() { return ++count; },
        decrement() { return --count; },
        getValue() { return count; }
    };
}

const counter = createCounter(10);
console.log(counter.increment()); // 11
console.log(counter.getValue());  // 11
// counter.count is undefined (strictly encapsulated!)""",
                    "explanation": "The inner methods maintain a persistent reference to the enclosing `count` variable, providing robust data privacy."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the output of `(function(){ var a = b = 3; })(); console.log(typeof a, typeof b);` in non-strict mode?",
                    "options": [
                        "A) undefined, number",
                        "B) number, number",
                        "C) undefined, undefined",
                        "D) Throws ReferenceError"
                    ],
                    "correct_answer": "A) undefined, number",
                    "detailed_solution": "`var a = b = 3` evaluates right-to-left: `b = 3` creates an implicit global variable, while `var a` is scoped locally to the IIFE."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "What is the difference between Function.prototype.call, apply, and bind?",
                    "model_answer": "`call()` and `apply()` invoke the function immediately with explicit `this` binding. `call()` takes arguments separated by commas (`fn.call(ctx, arg1, arg2)`), while `apply()` takes arguments as an array (`fn.apply(ctx, [arg1, arg2])`). `bind()` does not execute the function immediately; it returns a new bound function with `this` permanently locked to the provided context.",
                    "interviewer_tip": "Mnemonic: 'A for Array (apply), C for Comma (call)'."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Asynchronous JavaScript: Promises & async/await",
        "key_takeaways": "Master Promise lifecycle (pending, fulfilled, rejected), Promise.all vs allSettled vs race vs any, and async/await error handling.",
        "topics": [
            "Callback Hell and inversion of control",
            "Promise states: Pending, Fulfilled, Rejected",
            "Promise chaining, error propagation, and .finally()",
            "Promise combinators: Promise.all, Promise.allSettled, Promise.race, Promise.any",
            "async/await syntactic sugar and try/catch error boundaries"
        ],
        "sections": {
            "concept": """Asynchronous JavaScript evolved from nested callbacks ('Callback Hell') to Promises and `async/await`:
- **Promise:** An object representing the eventual completion (or failure) of an asynchronous operation. A Promise is in one of three mutually exclusive states: `pending`, `fulfilled`, or `rejected`. Once settled, its state and value are immutable.
- **async/await:** Built on top of Promises and Generators. Marking a function `async` guarantees it returns a Promise. The `await` keyword pauses execution inside the async function until the Promise settles, resuming execution in the Microtask queue without blocking the main browser thread.""",
            "formulas": """1. **Promise Combinator Matrix:**
   - **Promise.all:** Rejects immediately if ANY promise rejects (Fail-Fast).
   - **Promise.allSettled:** Waits for ALL promises; returns status and value/reason for every item.
   - **Promise.race:** Settles as soon as the FIRST promise settles (fulfillment or rejection).
   - **Promise.any:** Fulfills as soon as the FIRST promise fulfills; rejects only if ALL reject (AggregateError).""",
            "solved_examples": [
                {
                    "title": "Robust Concurrent API Fetching with Promise.allSettled",
                    "difficulty": "Easy | Amazon, TCS Digital",
                    "problem": "Fetch user profile and user permissions concurrently, ensuring that failure of one API does not crash the other.",
                    "step_by_step": [
                        "Step 1: Execute promises in parallel using `Promise.allSettled()`.",
                        "Step 2: Inspect `status === 'fulfilled'` for each result."
                    ],
                    "code_or_math": """async function fetchUserData(userId) {
    const [profileRes, permsRes] = await Promise.allSettled([
        fetch(`/api/users/${userId}`),
        fetch(`/api/users/${userId}/permissions`)
    ]);

    const profile = profileRes.status === 'fulfilled' ? await profileRes.value.json() : null;
    const permissions = permsRes.status === 'fulfilled' ? await permsRes.value.json() : [];

    return { profile, permissions };
}""",
                    "explanation": "Promise.allSettled guarantees that partial failures do not prevent successful APIs from rendering."
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens if one promise in `Promise.all([p1, p2, p3])` rejects?",
                    "options": [
                        "A) It waits for all to finish then reports error",
                        "B) It rejects immediately with that error, ignoring other pending promises",
                        "C) It retries the rejected promise",
                        "D) Returns undefined"
                    ],
                    "correct_answer": "B) It rejects immediately with that error, ignoring other pending promises",
                    "detailed_solution": "Promise.all implements fail-fast behavior, immediately rejecting upon the first rejection."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "Can you use await outside an async function?",
                    "model_answer": "Traditionally, `await` was strictly disallowed outside `async` functions. However, modern JavaScript supports **Top-Level Await** in ECMAScript Modules (ESM). In ES modules, `await` can be used at the top level of a module to initialize asynchronous resources before dependent modules execute.",
                    "interviewer_tip": "Clarify that top-level await is valid in ES Modules (.mjs or type='module')."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Modern ES6+ Features & Functional Programming",
        "key_takeaways": "Master destructuring, rest/spread operators, Map/Set, WeakMap, Array higher-order functions (map, filter, reduce), and immutability.",
        "topics": [
            "Destructuring assignment: Objects, arrays, defaults, and aliases",
            "Rest parameters (...args) vs Spread operator (...iterable)",
            "Array functional methods: map, filter, reduce, some, every, flatMap",
            "Map and Set vs Object and Array, WeakMap for private data and memory safety",
            "Pure functions, immutability, and function currying"
        ],
        "sections": {
            "concept": """ECMAScript 6 (ES2015) transformed JavaScript into a modern, expressive language:
- **Destructuring:** Clean extraction of properties into distinct variables: `const { name: userName, age = 18 } = user`.
- **Spread & Rest (`...`):** Rest gathers function arguments into an array; Spread expands arrays or objects into elements.
- **Higher-Order Array Methods:**
  - `map`: Transforms each element 1-to-1.
  - `filter`: Extracts elements satisfying a boolean predicate.
  - `reduce`: Accumulates an array into a single scalar, object, or grouped dictionary.
- **WeakMap / WeakSet:** Keys must be objects and are held weakly. If no other references to a key object exist, it is garbage collected, preventing memory leaks in DOM metadata associations.""",
            "formulas": """1. **Array Reduce Accumulator Invariant:**
   $$\\\\text{arr.reduce}((acc, curr) \\\\implies \\\\text{nextAcc}, \\\\text{initialVal})$$""",
            "solved_examples": [
                {
                    "title": "Grouping and Aggregating Data with Array.prototype.reduce",
                    "difficulty": "Easy | Amazon, Flipkart",
                    "problem": "Given a list of transactions, calculate total spent per category using reduce.",
                    "step_by_step": [
                        "Step 1: Start with empty object `{}` accumulator.",
                        "Step 2: Add transaction amount to category tally.",
                        "Step 3: Return accumulator."
                    ],
                    "code_or_math": """const transactions = [
    { category: 'Food', amount: 20 },
    { category: 'Transport', amount: 15 },
    { category: 'Food', amount: 35 },
];

const totalByCategory = transactions.reduce((acc, { category, amount }) => {
    acc[category] = (acc[category] || 0) + amount;
    return acc;
}, {});

console.log(totalByCategory); // { Food: 55, Transport: 15 }""",
                    "explanation": "Replaces imperative for-loops with a clean, single-pass functional aggregation."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the key difference between Map and a standard JavaScript Object?",
                    "options": [
                        "A) Objects are faster for iteration",
                        "B) Map keys can be of any data type (including objects and functions), while Object keys must be strings or symbols",
                        "C) Objects preserve insertion order, Maps do not",
                        "D) Map cannot be converted to JSON"
                    ],
                    "correct_answer": "B) Map keys can be of any data type (including objects and functions), while Object keys must be strings or symbols",
                    "detailed_solution": "Map allows arbitrary object references as keys and provides a direct `.size` property."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft",
                    "question": "What is a Pure Function and why is immutability important in React/Redux architectures?",
                    "model_answer": "A Pure Function is deterministic (always returns identical output for identical inputs) and has zero side effects (does not mutate external variables, make I/O calls, or modify parameters). Immutability is crucial in modern frameworks like React because state changes can be detected via fast shallow reference equality checks (`prevProps !== nextProps`) in $O(1)$ time, avoiding expensive deep object comparisons.",
                    "interviewer_tip": "Mention shallow reference comparison ($O(1)$) in Virtual DOM diffing."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "TypeScript Type System & Strict Safety",
        "key_takeaways": "Master static typing, Interfaces vs Types, Generics, Union & Intersection types, Type Narrowing, and utility types (Partial, Pick, Omit).",
        "topics": [
            "TypeScript compilation: Transpilation to JavaScript and type erasure",
            "Interfaces vs Type Aliases (Declaration merging, union capabilities)",
            "Generics: Constrained generics (<T extends { id: string }>) and generic functions",
            "Type Narrowing: typeof, instanceof, in operator, and Discriminated Unions",
            "Utility Types: Partial, Required, Readonly, Pick, Omit, Record, ReturnType"
        ],
        "sections": {
            "concept": """TypeScript is a typed superset of JavaScript that compiles to plain JavaScript. All type annotations are stripped during compilation (**Type Erasure**), introducing zero runtime performance overhead.

Key Type System Features:
- **Interfaces vs Types:** Interfaces support **Declaration Merging** (extending third-party library definitions) and represent object contracts. Types support primitives, unions (`A | B`), intersections (`A & B`), and mapped types.
- **Discriminated Unions:** Pattern where each type in a union shares a common literal discriminator property (e.g., `kind: 'circle' | 'square'`), enabling exhaustiveness checks via `switch`.
- **Type Narrowing:** Refining broad types to specific subtypes using type guards (`typeof`, `instanceof`, custom `is` predicates).""",
            "formulas": """1. **Discriminated Union Structure:**
   $$\\\\text{type Shape} = \\\\{ \\\\text{kind: 'circle', radius: number} \\\\} \\\\mid \\\\{ \\\\text{kind: 'square', size: number} \\\\}$$
2. **Key Utility Types:**
   $$\\\\text{Pick<T, K>} = \\\\text{Extracts subset } K \\\\text{ of keys from } T$$
   $$\\\\text{Omit<T, K>} = \\\\text{Drops keys } K \\\\text{ from } T$$""",
            "solved_examples": [
                {
                    "title": "Generic API Response Wrapper with Type Constraints",
                    "difficulty": "Easy | Microsoft, Uber",
                    "problem": "Create a generic API response type that handles success and error payloads safely.",
                    "step_by_step": [
                        "Step 1: Define generic interface `ApiResponse<T>`.",
                        "Step 2: Use optional generic parameter with default type."
                    ],
                    "code_or_math": """interface ApiResponse<T> {
    success: boolean;
    data: T | null;
    error?: string;
    timestamp: number;
}

interface User {
    id: number;
    name: string;
}

// Type-safe consumption
const response: ApiResponse<User> = {
    success: true,
    data: { id: 101, name: "Alice" },
    timestamp: Date.now()
};""",
                    "explanation": "Provides compile-time safety ensuring `data` matches the expected type contract."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the difference between `unknown` and `any` in TypeScript?",
                    "options": [
                        "A) They are identical",
                        "B) any turns off type checking; unknown requires type narrowing before performing operations",
                        "C) unknown only accepts strings",
                        "D) any cannot be assigned to objects"
                    ],
                    "correct_answer": "B) any turns off type checking; unknown requires type narrowing before performing operations",
                    "detailed_solution": "unknown is the type-safe counterpart of any, requiring explicit type guards prior to access."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft",
                    "question": "What is Declaration Merging in TypeScript and when should you use an Interface over a Type?",
                    "model_answer": "Declaration Merging occurs when the TypeScript compiler merges two separate interfaces with the identical name into a single definition. It is essential when augmenting existing global libraries or window objects (e.g., adding custom properties to `Window` or `Express.Request`). Use an Interface when building public API libraries or object contracts that require extension. Use a Type for unions, tuples, primitives, or mapped transformations.",
                    "interviewer_tip": "Cite extending Express `req.user` as a practical production example."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "DOM Manipulation, Browser APIs & Event Propagation",
        "key_takeaways": "Master the DOM tree, Event Bubbling vs Capturing, Event Delegation, Debounce vs Throttle, and IntersectionObserver.",
        "topics": [
            "DOM tree representation, querySelector, and DocumentFragment for batch mutations",
            "Event Propagation: Capturing phase, Target phase, and Bubbling phase",
            "Event Delegation: Single listener on parent element for dynamic children",
            "Rate limiting: Debouncing (search input) vs Throttling (scroll events)",
            "Modern Web APIs: IntersectionObserver (lazy loading) and LocalStorage vs SessionStorage vs Cookies"
        ],
        "sections": {
            "concept": """The Document Object Model (DOM) is the tree representation of an HTML document in memory. Manipulating the DOM triggers expensive browser **Reflow** (recalculating geometric layout) and **Repaint** (drawing pixels). To optimize performance, batch DOM updates using `DocumentFragment`.

**Event Propagation (3 Phases):**
1. **Capturing Phase:** Event trickles down from `window` through ancestors to target.
2. **Target Phase:** Event reaches the target element.
3. **Bubbling Phase:** Event bubbles up from target back through ancestors to `window`.

**Event Delegation:**
Instead of attaching separate event listeners to 1,000 table rows, attach a single listener to the parent container (`<table>`), inspecting `e.target` during the bubbling phase. This saves memory and automatically handles dynamically created elements.""",
            "formulas": """1. **Rate Limiting Invariants:**
   - **Debounce:** Resets timer on every call. Executes only after a quiet period of $X$ milliseconds (e.g., search autocomplete).
   - **Throttle:** Executes at most once per fixed time interval $X$ (e.g., scroll/resize).""",
            "solved_examples": [
                {
                    "title": "Production Debounce Implementation",
                    "difficulty": "Medium | Amazon, Google, Flipkart",
                    "problem": "Implement a custom debounce function from scratch in vanilla JavaScript.",
                    "step_by_step": [
                        "Step 1: Return a closure maintaining a `timerId`.",
                        "Step 2: Clear existing timer on each invocation.",
                        "Step 3: Schedule new timer with `setTimeout` invoking callback with arguments."
                    ],
                    "code_or_math": """function debounce(func, delayMs) {
    let timerId = null;
    return function (...args) {
        if (timerId) clearTimeout(timerId);
        timerId = setTimeout(() => {
            func.apply(this, args);
        }, delayMs);
    };
}

// Usage:
const handleSearch = debounce((query) => {
    console.log("Searching for:", query);
}, 300);""",
                    "explanation": "Guarantees that rapid keystrokes trigger only a single network API call after the user stops typing."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary benefit of Event Delegation?",
                    "options": [
                        "A) Faster network requests",
                        "B) Reduced memory overhead and automatic handling of dynamically added child elements",
                        "C) Prevents event bubbling",
                        "D) Eliminates CSS animations"
                    ],
                    "correct_answer": "B) Reduced memory overhead and automatic handling of dynamically added child elements",
                    "detailed_solution": "A single listener on the parent leverages bubbling to intercept events from any child without per-element allocations."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is the difference between Reflow and Repaint in browser rendering?",
                    "model_answer": "Reflow (Layout) is the process where the browser calculates the positions and geometries of all elements in the document tree. It is computationally expensive. Modifying properties like `width`, `height`, `margin`, or `fontSize` triggers reflow. Repaint occurs when an element's visual appearance changes without altering layout geometry (e.g., `color`, `background-color`, `visibility`). Reflow always triggers a subsequent repaint, but repaint can occur without reflow.",
                    "interviewer_tip": "Mention using `transform` and `opacity` because they execute on the GPU compositor thread without triggering reflow."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Modules, Bundlers & Memory Management",
        "key_takeaways": "Master ES Modules (import/export) vs CommonJS (require), Tree Shaking, Garbage Collection (Mark and Sweep), and memory leaks.",
        "topics": [
            "Module systems: CommonJS (synchronous, runtime) vs ES Modules (static, compile-time)",
            "Tree Shaking: Dead code elimination via static ESM analysis",
            "V8 Garbage Collection: Generational Mark and Sweep with Scavenger",
            "Common JavaScript memory leaks: Forgotten timers, dangling event listeners, detached DOM nodes",
            "Chrome DevTools Memory Profiler (Heap Snapshots, Allocation Timelines)"
        ],
        "sections": {
            "concept": """JavaScript modularity transitioned from CommonJS (`require()`, Node.js legacy) to official **ES Modules (ESM)** (`import / export`):
- **CommonJS:** Dynamic and evaluated at runtime. Modules are loaded synchronously.
- **ES Modules:** Static structure determined at compile time. Enables bundlers (Webpack, Vite, Rollup) to perform **Tree Shaking**: automatically identifying and stripping unused exported functions from production bundles.

**Memory Leaks:**
V8 uses generational Mark-and-Sweep garbage collection. Memory leaks occur when active references prevent unused memory from being reclaimed:
1. Forgotten `setInterval()` references retaining large scope variables.
2. Event listeners attached to DOM elements that are removed from the page without `.removeEventListener()`.
3. Detached DOM nodes retained in global JavaScript arrays.""",
            "formulas": """1. **Tree Shaking Feasibility:**
   $$\\\\text{Static ESM (import { fn } from 'mod')} \\\\implies \\\\text{Tree Shakeable}$$
   $$\\\\text{Dynamic CommonJS (const mod = require('mod'))} \\\\implies \\\\text{Cannot be Tree Shaken}$$""",
            "solved_examples": [
                {
                    "title": "Detecting and Fixing Detached DOM Node Leaks",
                    "difficulty": "Medium | Google, Uber",
                    "problem": "Identify the memory leak in code appending DOM elements to a global array, and provide the fix.",
                    "step_by_step": [
                        "Step 1: Storing removed DOM elements in global variables keeps the entire subtree alive in Heap memory.",
                        "Step 2: Clear references or use WeakRef / WeakSet."
                    ],
                    "code_or_math": """// LEAKY CODE:
const leakedElements = [];
function createAndRemove() {
    const btn = document.createElement("button");
    document.body.appendChild(btn);
    leakedElements.push(btn); // Retains reference!
    document.body.removeChild(btn); // Detached from DOM, but retained in Heap!
}

// FIXED CODE:
function cleanCreateAndRemove() {
    const btn = document.createElement("button");
    document.body.appendChild(btn);
    // Perform operations...
    document.body.removeChild(btn);
    // Do NOT retain reference in global array; V8 reclaims memory automatically
}""",
                    "explanation": "Removing an element from the DOM does not free memory if references still exist in JavaScript arrays."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why can ES Modules be tree-shaken by bundlers while CommonJS cannot?",
                    "options": [
                        "A) ESM files are smaller",
                        "B) ESM imports/exports are static and known at build time, allowing dead code elimination",
                        "C) CommonJS is deprecated in browsers",
                        "D) ESM runs on multiple threads"
                    ],
                    "correct_answer": "B) ESM imports/exports are static and known at build time, allowing dead code elimination",
                    "detailed_solution": "Static analysis allows compilers to determine with certainty which exports are never referenced."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "How do you identify a memory leak in a single-page web application using Chrome DevTools?",
                    "model_answer": "Open Chrome DevTools Memory tab. 1) Take a baseline Heap Snapshot. 2) Perform the suspected leaky user interaction (e.g., opening and closing a dialog 10 times). 3) Take a second Heap Snapshot. 4) Use the 'Comparison' view between Snapshot 2 and Snapshot 1. Filter by 'Objects Allocated between Snapshot 1 and 2' or search for 'Detached HTML elements'. Inspect the Retainer tree to identify the root variable preventing garbage collection.",
                    "interviewer_tip": "Cite Heap Snapshots and the Retainer tree."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Solved Frontend Placement Coding Drills & System Design",
        "key_takeaways": "Master custom implementations of deep clone, Promise.all, memoize, flatten array, and frontend architecture design.",
        "topics": [
            "Deep Clone handling circular references and non-serializable types (structuredClone vs custom)",
            "Custom Promise.all polyfill implementation",
            "Function memoization cache decorator",
            "Flatten deeply nested arrays (Array.prototype.flat polyfill)",
            "Frontend System Design: Autocomplete Search component with debounce, caching, and race condition prevention"
        ],
        "sections": {
            "concept": """This capstone chapter covers machine coding rounds and technical interviews for frontend and full-stack software engineering roles.

Key polyfills and utility algorithms:
- **Deep Clone:** Recursively clones objects while tracking visited objects via `WeakMap` to avoid infinite recursion on circular graphs.
- **Promise.all Polyfill:** Maintains an output array and a counter of completed promises, resolving when `completedCount === promises.length`.
- **Race Condition Prevention in Autocomplete:** If request A is sent before request B, but request A takes longer and responds after request B, request A's stale data must not overwrite request B's newer data. Mitigated using request sequence tokens or `AbortController`.""",
            "formulas": """1. **Promise.all Polyfill Resolution:**
   $$\\\\text{Resolve Output} \\\\iff \\\\text{completedCount} === \\\\text{promises.length}$$""",
            "solved_examples": [
                {
                    "title": "Implement Custom Promise.all Polyfill",
                    "difficulty": "Hard | Google, Amazon, Uber",
                    "problem": "Implement a function `promiseAll(promises)` that behaves identically to `Promise.all`.",
                    "step_by_step": [
                        "Step 1: Return a new Promise.",
                        "Step 2: If input is empty, resolve with `[]` immediately.",
                        "Step 3: Track `completedCount = 0` and `results = []`.",
                        "Step 4: Iterate promises with index. Wrap with `Promise.resolve(p)` to handle raw values.",
                        "Step 5: On fulfill, store `results[i] = val` and increment counter. If counter equals length, resolve `results`.",
                        "Step 6: On any rejection, reject outer promise immediately."
                    ],
                    "code_or_math": """function promiseAll(promises) {
    return new Promise((resolve, reject) => {
        if (!Array.isArray(promises)) {
            return reject(new TypeError("Input must be an array"));
        }
        if (promises.length === 0) {
            return resolve([]);
        }

        const results = new Array(promises.length);
        let completed = 0;

        promises.forEach((p, index) => {
            Promise.resolve(p).then(
                (val) => {
                    results[index] = val;
                    completed += 1;
                    if (completed === promises.length) {
                        resolve(results);
                    }
                },
                (err) => {
                    reject(err); // Rejects immediately on first error
                }
            );
        });
    });
}""",
                    "explanation": "Properly preserves original index order and implements fail-fast rejection."
                }
            ],
            "practice_questions": [
                {
                    "question": "Why is `JSON.parse(JSON.stringify(obj))` insufficient for deep cloning arbitrary objects?",
                    "options": [
                        "A) It is slow and drops undefined, functions, Symbols, and throws errors on circular references",
                        "B) It cannot clone numbers",
                        "C) It only works on arrays",
                        "D) It mutates the original object"
                    ],
                    "correct_answer": "A) It is slow and drops undefined, functions, Symbols, and throws errors on circular references",
                    "detailed_solution": "JSON serialization fails on circular references and cannot preserve dates, functions, or undefined."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "How do you handle race conditions in search autocomplete when an earlier slow network request finishes after a later request?",
                    "model_answer": "Two primary techniques: 1) **AbortController:** Before firing a new search request, abort the previous pending request using `controller.abort()`. 2) **Request Sequence ID / Timestamp:** Maintain an integer counter `currentRequestId`. Increment it with each keystroke. Pass the ID into the async closure. When the network response returns, check if its ID matches `currentRequestId`; if it is stale, ignore the response.",
                    "interviewer_tip": "Recommend AbortController as the modern standard browser API."
                }
            ]
        }
    }
]
'''
    (CURRICULUM_DIR / "curriculum_javascript.py").write_text(content, encoding="utf-8")
    print("Created curriculum_javascript.py")

build_javascript_module()

