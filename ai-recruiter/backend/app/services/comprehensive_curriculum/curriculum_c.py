"""
curriculum_c.py - 8 Comprehensive Chapters for C Programming Language & Placement Foundations.
"""
from typing import List, Dict, Any

C_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "C Compilation Pipeline, Memory Layout & Preprocessor",
        "key_takeaways": "Master Preprocessing, Compilation, Assembly, Linking, and Process Virtual Memory Segments (Text, Data, BSS, Stack, Heap).",
        "topics": [
            "4 Stages of C Compilation: Preprocessor (cpp) -> Compiler (cc1) -> Assembler (as) -> Linker (ld)",
            "Memory Segments: Text, Initialized Data, Uninitialized BSS, Heap (brk/mmap), and Stack",
            "Preprocessor Directives: #define macros, #include guards, token concatenation (##), and stringizing (#)",
            "Storage Classes: auto, register, static (internal vs external linkage), and extern",
            "Header Files and Translation Units"
        ],
        "sections": {
            "concept": """The C compilation pipeline transforms human-readable source code into machine-executable binary across four distinct phases:
1. **Preprocessing (`cpp`):** Strips comments, expands `#include` header files, evaluates conditional compilation (`#ifdef`), and expands `#define` macros.
2. **Compilation (`gcc -S`):** Parses syntax, performs semantic analysis, optimizes code, and translates C tokens into assembly language.
3. **Assembly (`as`):** Translates assembly instructions into relocatable machine-code object files (`.o`).
4. **Linking (`ld`):** Resolves symbolic cross-references between object files and static/dynamic libraries (`libc`), setting up the executable ELF or PE file.

When executed, an operating system assigns each C process a 32-bit or 64-bit **Virtual Memory Layout**:
- **Text (Code) Segment:** Read-only segment housing machine code instructions.
- **Data Segment:** Holds explicitly initialized global and static variables (`int g = 42;`).
- **BSS Segment (Block Started by Symbol):** Holds uninitialized global and static variables (`int count;`), zero-initialized by the kernel at runtime.
- **Heap:** Dynamically managed memory growing upwards via `brk()` and `mmap()` syscalls (`malloc`/`free`).
- **Stack:** LIFO frame structure growing downwards, holding local variables, function arguments, and return addresses.""",
            "formulas": """1. **Process Memory Layout Direction:**
   $$\\text{Low Addresses} \\to \\text{Text} \\to \\text{Data} \\to \\text{BSS} \\to \\text{Heap} (\\uparrow) \\quad \\dots \\quad \\text{Stack} (\\downarrow) \\to \\text{High Addresses}$$
2. **Storage Class Linkage Matrix:**
   - `static` global variable: Internal Linkage (visible only within current translation unit).
   - `extern` global variable: External Linkage (accessible across multiple object files).
   - `static` local variable: Retains value across function calls, stored in Data or BSS segment.""",
            "solved_examples": [
                {
                    "title": "Memory Segment Allocation Trace",
                    "difficulty": "Medium | TCS Digital, Zoho, CTS",
                    "problem": "Determine which memory segment holds each of the following variables: (1) `static int a;`, (2) `int b = 10;` outside main, (3) `int c = 5;` inside a function, (4) `char *str = \"Hello\";`.",
                    "step_by_step": [
                        "Step 1: `static int a;` is an uninitialized static variable -> allocated in the BSS segment (zero-initialized).",
                        "Step 2: `int b = 10;` is an initialized global variable -> allocated in the Initialized Data segment.",
                        "Step 3: `int c = 5;` is a local automatic variable within function scope -> allocated on the Stack.",
                        "Step 4: `\"Hello\"` is a string literal placed in the read-only Text segment; the pointer variable `str` itself resides on the Stack."
                    ],
                    "code_or_math": """#include <stdio.h>
int b = 10;          // Data Segment
static int a;        // BSS Segment

void demo() {
    int c = 5;       // Stack
    char *str = "Hello"; // "Hello" in Text, str pointer on Stack
}""",
                    "explanation": "Understanding process memory layout prevents segmentation faults and dangling references."
                }
            ],
            "practice_questions": [
                {
                    "question": "Where does an uninitialized global variable reside in a C process's memory layout?",
                    "options": ["A) Stack", "B) Heap", "C) BSS Segment", "D) Text Segment"],
                    "correct_answer": "C) BSS Segment",
                    "detailed_solution": "Uninitialized global and static variables are stored in the BSS segment and zero-initialized upon process launch."
                }
            ],
            "interview_questions": [
                {
                    "question": "What is the difference between `#include <file.h>` and `#include \"file.h\"`?",
                    "company_tag": "Zoho, Qualcomm, Cisco",
                    "answer": "Angle brackets `<>` instruct the preprocessor to search standard system include directories first (`/usr/include`). Double quotes `\"\"` instruct the preprocessor to search the current working directory of the source file first, falling back to system paths if not found."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "C Pointers Mastery: Addressing, Pointer Arithmetic & Double Pointers",
        "key_takeaways": "Master address-of (&), dereferencing (*), pointer arithmetic scale factors, void pointers, function pointers, and double pointers.",
        "topics": [
            "Memory Addressing & the Dereference Operator",
            "Pointer Arithmetic: Scaling by sizeof(type)",
            "Pointers to Pointers (Double Pointers `**ptr`) and Modifying Arguments in-place",
            "Void Pointers (`void*`) and Generic Memory Operations",
            "Function Pointers (`void (*fp)(int)`) and Callbacks in C"
        ],
        "sections": {
            "concept": """A pointer is a variable whose value is the physical address of another variable in memory.
- `&` (Address-of operator): Retrieves the starting byte address of an operand.
- `*` (Dereference operator): Accesses or modifies the value stored at the referenced address.

**Pointer Arithmetic:**
Adding an integer $k$ to a pointer $p$ of type $T*$ advances the address by $k \\times \\text{sizeof}(T)$ bytes:
$$\\text{New Address} = \\text{Base Address} + k \\times \\text{sizeof}(T)$$

**Double Pointers (`**ptr`):**
To modify a pointer's target address inside a function, you must pass the pointer by reference using a pointer-to-pointer (`Type **`). This is essential for dynamic memory allocation functions and linked list head modifications.

**Function Pointers:**
Functions reside in the Text segment and have memory entry points. Function pointers allow passing algorithms as callbacks to higher-order functions like `qsort()`.""",
            "formulas": """1. **Pointer Arithmetic Formula:**
   $$\\&p[i] = p + (i \\times \\text{sizeof}(*p))$$
2. **Function Pointer Syntax:**
   $$\\text{ReturnType} \\; (*\\text{ptrName})(\\text{ParamType1}, \\text{ParamType2});$$
3. **Array Decays to Pointer:**
   $$arr[i] \\equiv *(arr + i) \\equiv *(i + arr) \\equiv i[arr]$$""",
            "solved_examples": [
                {
                    "title": "Modifying Linked List Head via Double Pointer",
                    "difficulty": "Medium | Amazon, Zoho, Infosys",
                    "problem": "Write a C function `insert_front` that prepends a node to a singly linked list. Explain why a double pointer `Node** head_ref` is required.",
                    "step_by_step": [
                        "Step 1: If we pass `Node* head`, C passes the pointer by value; altering `head` only changes the local copy.",
                        "Step 2: Passing `Node** head_ref` allows us to dereference `*head_ref` and mutate the original caller's pointer.",
                        "Step 3: Allocate new node, set its next pointer to `*head_ref`, and update `*head_ref` to point to the new node."
                    ],
                    "code_or_math": """typedef struct Node {
    int data;
    struct Node *next;
} Node;

void insert_front(Node **head_ref, int new_data) {
    Node *new_node = (Node*)malloc(sizeof(Node));
    new_node->data = new_data;
    new_node->next = *head_ref;
    *head_ref = new_node; // Caller's head updated!
}""",
                    "explanation": "Passing Node** head_ref ensures that modifications to the list head persist in the caller's stack frame."
                }
            ],
            "practice_questions": [
                {
                    "question": "If `int *p = 1000;` on a 64-bit architecture where `sizeof(int) == 4`, what is the value of `p + 2`?",
                    "options": ["A) 1002", "B) 1004", "C) 1008", "D) 1016"],
                    "correct_answer": "C) 1008",
                    "detailed_solution": "Pointer arithmetic scales by sizeof(int) = 4 bytes: 1000 + (2 * 4) = 1008."
                }
            ],
            "interview_questions": [
                {
                    "question": "What is the difference between `const int *ptr`, `int * const ptr`, and `const int * const ptr`?",
                    "company_tag": "Qualcomm, TCS Ninja, Amazon",
                    "answer": "`const int *ptr` (pointer to const): The data being pointed to is read-only, but the pointer can point elsewhere. `int * const ptr` (const pointer): The pointer cannot point elsewhere, but the referenced data can be mutated. `const int * const ptr`: Both the pointer address and the referenced data are immutable."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Dynamic Memory Allocation & Memory Safety",
        "key_takeaways": "Master malloc, calloc, realloc, free, memory leaks, dangling pointers, buffer overflows, and Valgrind debugging.",
        "topics": [
            "Heap Allocation with `malloc()`, `calloc()`, and `realloc()`",
            "Deallocation with `free()` and Heap Fragmentation",
            "Dangling Pointers and Wild Pointers",
            "Memory Leaks and Heap Corruption",
            "Buffer Overflows and Stack Smashing Protections"
        ],
        "sections": {
            "concept": """Dynamic memory allocation enables reserving memory of arbitrary runtime dimensions on the heap.
- `malloc(size)`: Allocates `size` contiguous uninitialized bytes. Returns `NULL` if allocation fails.
- `calloc(num, size)`: Allocates zero-initialized memory for `num` elements of `size` bytes each.
- `realloc(ptr, new_size)`: Resizes previously allocated block, potentially moving it to a new heap location.
- `free(ptr)`: Releases the allocated block back to the heap manager.

**Critical Memory Hazards in C:**
1. **Memory Leak:** Failing to call `free()` on allocated heap pointers before losing reference to them.
2. **Dangling Pointer:** A pointer still referencing an address after the memory block was freed (`free(p); p->x = 10;`). Fix: immediately assign `p = NULL;` after deallocation.
3. **Double Free:** Invoking `free()` twice on the same memory block, causing heap metadata corruption.
4. **Buffer Overflow:** Writing beyond allocated boundaries, corrupting adjacent heap chunks or stack return addresses.""",
            "formulas": """1. **Memory Allocation Safety Pattern:**
   ```c
   int *arr = (int*)malloc(n * sizeof(int));
   if (arr == NULL) { /* Handle out-of-memory */ exit(EXIT_FAILURE); }
   /* Use memory ... */
   free(arr);
   arr = NULL; // Defuse dangling pointer
   ```
2. **Calloc vs Malloc:**
   $$\\text{calloc}(n, s) \\equiv \\text{malloc}(n \\times s) + \\text{memset}(0)$$""",
            "solved_examples": [
                {
                    "title": "Dynamic Resizing with realloc()",
                    "difficulty": "Medium | Cognizant, Wipro, Google",
                    "problem": "Implement a dynamic integer buffer that doubles its capacity using `realloc()` safely without risking a memory leak if `realloc()` fails.",
                    "step_by_step": [
                        "Step 1: Never assign `realloc()` directly back to original pointer: `ptr = realloc(ptr, ...)` leaks the original memory if it returns NULL.",
                        "Step 2: Assign result to a temporary pointer `temp`.",
                        "Step 3: If `temp != NULL`, update `ptr = temp` and double capacity. If NULL, retain original buffer and handle error."
                    ],
                    "code_or_math": """int *grow_array(int *arr, int *capacity) {
    int new_cap = (*capacity) * 2;
    int *temp = (int*)realloc(arr, new_cap * sizeof(int));
    if (temp == NULL) {
        // Original arr is STILL VALID! Do not overwrite with NULL
        fprintf(stderr, "Out of memory\\n");
        return arr;
    }
    *capacity = new_cap;
    return temp;
}""",
                    "explanation": "Using a temporary pointer prevents memory leaks during realloc failures."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary difference between `malloc()` and `calloc()`?",
                    "options": [
                        "A) malloc allocates on stack, calloc on heap",
                        "B) calloc initializes allocated bytes to zero, malloc leaves memory uninitialized",
                        "C) malloc is faster because it frees itself automatically",
                        "D) calloc cannot allocate contiguous blocks"
                    ],
                    "correct_answer": "B) calloc initializes allocated bytes to zero, malloc leaves memory uninitialized",
                    "detailed_solution": "calloc takes two parameters and zeroes out all allocated memory, whereas malloc leaves memory with whatever residual garbage values existed."
                }
            ],
            "interview_questions": [
                {
                    "question": "What happens when you dereference a freed pointer?",
                    "company_tag": "Microsoft, TCS, Amazon",
                    "answer": "Dereferencing a freed pointer leads to Undefined Behavior (UB). It may return stale data, cause an immediate segmentation fault (SIGSEGV), or corrupt newly allocated heap structures if the memory manager has reused that chunk."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Arrays, Strings & Character Pointer Mechanics",
        "key_takeaways": "Master 1D/2D arrays, array-pointer decay, null-terminated strings, string manipulation functions, and memory-safe string parsing.",
        "topics": [
            "Array Representation in Memory & Row-Major Order",
            "Array Decay to Pointers and sizeof Quirks",
            "C Strings: The Null-Terminator (`'\\0'`) Contract",
            "Standard String Functions: `strlen`, `strcpy`, `strcat`, `strcmp`, `snprintf`",
            "Buffer Overflow Hazards in `gets()` and `strcpy()` vs Safe Alternatives"
        ],
        "sections": {
            "concept": """In C, an array is a sequence of elements of identical type placed in contiguous memory locations.
**Array Decay:**
When an array name is passed into an expression (or function argument), it decays into a pointer pointing to its first element (`arr` becomes `&arr[0]`), losing its dimension information. Inside the called function, `sizeof(arr)` evaluates to pointer size (8 bytes on 64-bit systems), not total array capacity.

**C Strings:**
A string in C is simply a 1D character array terminated by a null character (`'\\0'`, ASCII code 0).
- `char s[] = \"Hello\";` allocates 6 bytes (`'H','e','l','l','o','\\0'`) on the Stack (mutable).
- `char *s = \"Hello\";` places `\"Hello\"` in read-only Text segment; attempting to mutate `s[0] = 'h'` triggers a segmentation fault.

**Security:** Unbounded functions like `gets()` and `strcpy()` cause stack smashing; production C code must use `fgets()` and `snprintf()`.""",
            "formulas": """1. **2D Array Element Addressing (Row-Major Order):**
   $$\\text{Address}(A[i][j]) = \\text{Base} + (i \\times C + j) \\times \\text{sizeof}(\\text{element})$$
   where $C$ is the number of columns.
2. **String Length vs Sizeof:**
   $$\\text{strlen}(s) = \\text{Number of characters before } '\\0'$$
   $$\\text{sizeof}(\\text{array}) = \\text{Total allocated bytes including } '\\0'$$""",
            "solved_examples": [
                {
                    "title": "In-Place String Reversal Algorithm",
                    "difficulty": "Easy | Infosys, TCS, Cognizant",
                    "problem": "Write an in-place string reversal function in C using two pointers. Do not allocate extra memory.",
                    "step_by_step": [
                        "Step 1: Compute string length $N$ using `strlen()`.",
                        "Step 2: Initialize two pointers: `left = str` and `right = str + N - 1`.",
                        "Step 3: Swap characters at `left` and `right`, increment `left`, decrement `right` until `left >= right`."
                    ],
                    "code_or_math": """void reverse_string(char *str) {
    if (!str) return;
    char *left = str;
    char *right = str + strlen(str) - 1;
    while (left < right) {
        char temp = *left;
        *left = *right;
        *right = temp;
        left++;
        right--;
    }
}""",
                    "explanation": "Runs in O(N) time and O(1) auxiliary space, directly modifying the null-terminated buffer."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is printed by `char arr[] = \"AI\"; printf(\"%zu, %zu\", sizeof(arr), strlen(arr));`?",
                    "options": ["A) 2, 2", "B) 3, 2", "C) 8, 2", "D) 3, 3"],
                    "correct_answer": "B) 3, 2",
                    "detailed_solution": "sizeof includes the terminating null byte '\\0' (3 bytes), whereas strlen counts only the characters before '\\0' (2 characters)."
                }
            ],
            "interview_questions": [
                {
                    "question": "Why is `char *p = \"hello\"; p[0] = 'H';` invalid in C?",
                    "company_tag": "Zoho, Microsoft, Accenture",
                    "answer": "`\"hello\"` is a string literal placed in the read-only Text/Data segment of the process. Attempting to write to read-only virtual memory invokes a segmentation fault."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Structures, Unions, Bit-fields & Memory Alignment",
        "key_takeaways": "Master struct definitions, member access via dot and arrow, struct padding and memory alignment rules, unions, and bitfields.",
        "topics": [
            "Structure Declaration & Member Access (`.` and `->`)",
            "Structure Padding, Alignment & Data Bus Optimization",
            "Unions: Memory Sharing Across Members",
            "Bit-fields: Sub-byte Packing & Hardware Registers",
            "Self-Referential Structures (Linked Lists, Trees)"
        ],
        "sections": {
            "concept": """A `struct` is a user-defined composite type grouping variables of diverse types under a contiguous memory block.
**Structure Padding & Alignment:**
CPUs access memory faster when operands are stored at memory addresses divisible by their size (e.g. 4-byte integers aligned to multiples of 4). Compilers insert unused **padding bytes** to enforce alignment:
- Total struct size is padded to a multiple of its largest primitive member's alignment requirement.
- Reordering struct members from largest to smallest minimizes padding waste.

**Unions:**
A `union` stores all members at the exact same starting memory address. The total size of a union is equal to the size of its largest member. Writing to one member overwrites the others. Unions are widely used for type punning and memory-constrained embedded systems.

**Bit-fields:**
Bit-fields allow specifying the exact number of bits used by integer members, ideal for packing network headers and microcontroller hardware registers.""",
            "formulas": """1. **Memory Alignment Rule:**
   $$\\text{Address}(\\text{member}) \\equiv 0 \\pmod{\\text{sizeof}(\\text{member})}$$
2. **Padding Minimization Rule:** Order struct members in descending order of size:
   $$\\text{pointers (8B)} \\to \\text{double (8B)} \\to \\text{int (4B)} \\to \\text{short (2B)} \\to \\text{char (1B)}$$""",
            "solved_examples": [
                {
                    "title": "Calculating Struct Size with Padding",
                    "difficulty": "Medium | Qualcomm, Zoho, TCS Prime",
                    "problem": "Calculate `sizeof(struct S)` on a 64-bit architecture:\n```c\nstruct S {\n    char a;\n    int b;\n    char c;\n};\n```",
                    "step_by_step": [
                        "Step 1: `char a` takes offset 0 (1 byte).",
                        "Step 2: `int b` requires 4-byte alignment; compiler inserts 3 padding bytes (offsets 1, 2, 3). `b` is placed at offset 4-7.",
                        "Step 3: `char c` takes offset 8 (1 byte). Total used = 9 bytes.",
                        "Step 4: The struct's largest member alignment is 4 bytes. Total struct size must be a multiple of 4; compiler appends 3 tail padding bytes (offsets 9, 10, 11).",
                        "Step 5: Total size = 12 bytes."
                    ],
                    "code_or_math": """// Optimized ordering (8 bytes instead of 12):
struct OptimizedS {
    int b;   // offset 0-3 (4 bytes)
    char a;  // offset 4 (1 byte)
    char c;  // offset 5 (1 byte)
    // 2 bytes tail padding -> Total = 8 bytes
};""",
                    "explanation": "Grouping smaller types together reduces padding bytes from 6 down to 2."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the size of `union Data { int i; double d; char c; };` on a 64-bit architecture?",
                    "options": ["A) 1 byte", "B) 4 bytes", "C) 8 bytes", "D) 13 bytes"],
                    "correct_answer": "C) 8 bytes",
                    "detailed_solution": "A union's size equals its largest member. `double d` takes 8 bytes, so the union size is 8 bytes."
                }
            ],
            "interview_questions": [
                {
                    "question": "What is the `#pragma pack(1)` directive used for in C?",
                    "company_tag": "Cisco, Qualcomm, Goldman Sachs",
                    "answer": "`#pragma pack(1)` forces the compiler to disable struct padding and align members on 1-byte boundaries. It eliminates wasted memory, which is essential when mapping structures directly onto binary network packets or disk file headers."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Bitwise Operators & Low-Level Manipulation Techniques",
        "key_takeaways": "Master AND, OR, XOR, NOT, left/right shifts, bitmasking, clearing/setting/toggling bits, and placement bit tricks.",
        "topics": [
            "Bitwise Operators: `&`, `|`, `^`, `~`, `<<`, `>>`",
            "Bit Masking: Setting, Clearing, Toggling, and Testing Bits",
            "Bitwise Arithmetic Hacks: Power of 2 check, Counting set bits",
            "Swapping two numbers using XOR without temporary variables",
            "Finding the single non-repeating element in an array"
        ],
        "sections": {
            "concept": """Bitwise operations operate directly at the level of individual binary digits (bits), executing in a single CPU clock cycle.
- `&` (AND): Returns 1 only if both bits are 1. Used to **test** or **mask** bits.
- `|` (OR): Returns 1 if either bit is 1. Used to **set** bits.
- `^` (XOR): Returns 1 if bits differ. Properties: $x \\oplus x = 0$, $x \\oplus 0 = x$. Used to **toggle** bits and eliminate duplicates.
- `~` (NOT): Inverts all bits (one's complement).
- `<<` (Left Shift): Multiplies integer by $2^k$ (shifts bits left, fills with 0).
- `>>` (Right Shift): Divides integer by $2^k$.

**Essential Bit Manipulation Idioms:**
1. Set $k$-th bit: `num |= (1 << k);`
2. Clear $k$-th bit: `num &= ~(1 << k);`
3. Toggle $k$-th bit: `num ^= (1 << k);`
4. Test $k$-th bit: `(num & (1 << k)) != 0;`
5. Clear lowest set bit: `num & (num - 1)` (Brian Kernighan's Algorithm)""",
            "formulas": """1. **Power of 2 Check:**
   $$(n > 0) \\;\\&\\&\\; ((n \\;\\&\\; (n - 1)) == 0)$$
2. **XOR Swap:**
   $$a = a \\oplus b; \\quad b = a \\oplus b; \\quad a = a \\oplus b;$$
3. **Lowest Set Bit Mask:**
   $$\\text{LowestBit}(x) = x \\;\\&\\; (-x)$$""",
            "solved_examples": [
                {
                    "title": "Brian Kernighan's Set Bit Counter",
                    "difficulty": "Easy | Accenture, TCS, Capgemini",
                    "problem": "Write an efficient C function to count the number of 1-bits in a 32-bit unsigned integer.",
                    "step_by_step": [
                        "Step 1: In standard iteration, we would shift 32 times.",
                        "Step 2: Using Brian Kernighan's trick `n = n & (n - 1)`, each iteration clears the lowest set bit.",
                        "Step 3: The loop executes only as many times as there are set bits (e.g. for 16 = 10000_2, loop runs exactly once)."
                    ],
                    "code_or_math": """int count_set_bits(unsigned int n) {
    int count = 0;
    while (n > 0) {
        n &= (n - 1); // Clears lowest set bit
        count++;
    }
    return count;
}""",
                    "explanation": "Executes in O(K) time where K is the count of set bits, significantly faster than O(32)."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the result of `12 ^ 12` in C?",
                    "options": ["A) 24", "B) 12", "C) 0", "D) 1"],
                    "correct_answer": "C) 0",
                    "detailed_solution": "Any number XORed with itself produces 0, as identical bits cancel out."
                }
            ],
            "interview_questions": [
                {
                    "question": "Given an array where every element appears twice except one, how do you find the unique element in O(N) time and O(1) space?",
                    "company_tag": "Amazon, Microsoft, Google",
                    "answer": "XOR all elements together in a single loop. Because x ^ x = 0 and x ^ 0 = x, and XOR is commutative and associative, all paired elements cancel out to 0, leaving only the unique element."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "File I/O, Error Handling & System Calls in C",
        "key_takeaways": "Master fopen, fclose, fread, fwrite, fprintf, fscanf, errno, fseek/ftell, and binary vs text mode.",
        "topics": [
            "Streams and File Descriptors (`FILE*`)",
            "Text vs Binary File Modes (`\"r\"`, `\"w\"`, `\"rb\"`, `\"wb\"`)",
            "Formatted I/O (`fprintf`, `fscanf`) vs Block I/O (`fread`, `fwrite`)",
            "Random Access with `fseek()`, `ftell()`, and `rewind()`",
            "Error Diagnostics with `errno`, `perror()`, and `strerror()`"
        ],
        "sections": {
            "concept": """In C, file input/output is managed through standard library abstractions called streams via `FILE*` pointers.
- `fopen(path, mode)`: Opens a stream; returns `NULL` on error.
- `fclose(fp)`: Flushes buffers and closes the underlying OS file descriptor.
- `fprintf(fp, format, ...)` / `fscanf(fp, format, ...)`: Formatted ASCII text I/O.
- `fread(buf, size, count, fp)` / `fwrite(buf, size, count, fp)`: Direct binary block transfer without formatting overhead.

**File Seeking (`fseek` / `ftell`):**
- `SEEK_SET`: Seek from the beginning of the file.
- `SEEK_CUR`: Seek from current stream position.
- `SEEK_END`: Seek from the end of the file (useful to measure file size: `fseek(fp, 0, SEEK_END); size = ftell(fp);`).

**Error Handling:**
Standard C library functions set the global integer `errno` on failure. `perror(\"msg\")` prints the message followed by a human-readable interpretation of `errno`.""",
            "formulas": """1. **File Size Discovery Idiom:**
   ```c
   fseek(fp, 0, SEEK_END);
   long file_size = ftell(fp);
   fseek(fp, 0, SEEK_SET);
   ```
2. **Binary Read Verification:**
   ```c
   size_t read_count = fread(buffer, sizeof(Record), N, fp);
   if (read_count < N && ferror(fp)) { perror("Read error"); }
   ```""",
            "solved_examples": [
                {
                    "title": "Copying Binary Files Safely",
                    "difficulty": "Medium | Zoho, Infosys, CTS",
                    "problem": "Write a robust C program that copies a source binary file to a destination file using a 4KB chunk buffer.",
                    "step_by_step": [
                        "Step 1: Open source with `\"rb\"` and destination with `\"wb\"`.",
                        "Step 2: Allocate 4096-byte buffer on the Stack.",
                        "Step 3: Read chunks with `fread()` and write exactly the read count with `fwrite()`.",
                        "Step 4: Close both file handles and check errors."
                    ],
                    "code_or_math": """int copy_file(const char *src, const char *dst) {
    FILE *in = fopen(src, "rb");
    if (!in) return -1;
    FILE *out = fopen(dst, "wb");
    if (!out) { fclose(in); return -2; }
    
    char buffer[4096];
    size_t bytes;
    while ((bytes = fread(buffer, 1, sizeof(buffer), in)) > 0) {
        fwrite(buffer, 1, bytes, out);
    }
    fclose(in);
    fclose(out);
    return 0;
}""",
                    "explanation": "Using binary mode avoids unintended newline conversions on Windows platforms."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is returned by `fopen()` if the requested file cannot be opened?",
                    "options": ["A) -1", "B) 0", "C) NULL", "D) EOF"],
                    "correct_answer": "C) NULL",
                    "detailed_solution": "fopen() returns a valid FILE* on success and NULL on failure, updating errno."
                }
            ],
            "interview_questions": [
                {
                    "question": "What is the difference between buffered I/O (`fread`/`fwrite`) and unbuffered system calls (`read`/`write`)?",
                    "company_tag": "Linux Kernel, Red Hat, Amazon",
                    "answer": "`fread` and `fwrite` are C standard library functions operating with an in-memory user-space buffer to minimize expensive context switches. `read` and `write` are direct OS system calls that invoke the kernel trap on every call without user-space buffering."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Classic Campus Placement C Coding Challenges & Pointer Traps",
        "key_takeaways": "Master solved placement coding questions in C: Linked lists, string anagrams, matrix rotations, and tricky output predictions.",
        "topics": [
            "Singly Linked List: Cycle Detection (Floyd's Tortoise and Hare)",
            "String Anagram Checking via Frequency Array",
            "Matrix In-Place 90-Degree Rotation",
            "Tricky C Operator Precedence & Evaluation Order Puzzles",
            "Placement Interview Code Tracing"
        ],
        "sections": {
            "concept": """Campus recruitment coding rounds (TCS Prime, Zoho, Cognizant Next, Wipro Turbo) require writing idiomatic, memory-safe C code without STL abstractions.
Key skills tested:
1. **Pointers to Structures:** Linked list transformations, merging sorted lists, detecting cycles.
2. **Frequency Arrays:** Using character ASCII values (`str[i] - 'a'`) as hash table indices for $O(N)$ string matching.
3. **Matrix Pointer Arithmetic:** Navigating 2D contiguous arrays in-place.
4. **Tricky Precedence:** Post-increment vs pre-increment (`*p++` vs `(*p)++`), assignment in conditionals (`if (x = 5)`).""",
            "formulas": """1. **Floyd's Cycle Finding Rule:**
   $$\\text{If a cycle exists, } \\text{fast (2 steps)} \\text{ and } \\text{slow (1 step)} \\text{ will meet inside the loop.}$$
2. **Pointer Dereference Precedence:**
   - `*p++`: Evaluates to `*p`, then increments pointer `p`.
   - `(*p)++`: Evaluates to `*p`, then increments the value at `p`.
   - `*++p`: Increments pointer `p` first, then dereferences.""",
            "solved_examples": [
                {
                    "title": "Floyd's Cycle Detection in C",
                    "difficulty": "Medium | Amazon, TCS Digital, Zoho",
                    "problem": "Write a C function to detect whether a linked list contains a cycle using Floyd's Tortoise and Hare algorithm.",
                    "step_by_step": [
                        "Step 1: Initialize `slow = head` and `fast = head`.",
                        "Step 2: Advance `slow` by 1 step (`slow = slow->next`) and `fast` by 2 steps (`fast = fast->next->next`).",
                        "Step 3: If `fast == NULL` or `fast->next == NULL`, there is no cycle (return 0).",
                        "Step 4: If `slow == fast`, a cycle exists (return 1)."
                    ],
                    "code_or_math": """typedef struct Node {
    int data;
    struct Node *next;
} Node;

int has_cycle(Node *head) {
    Node *slow = head, *fast = head;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            return 1; // Cycle detected
        }
    }
    return 0; // Terminated at NULL -> No cycle
}""",
                    "explanation": "Executes in O(N) time and O(1) memory, preventing infinite traversal loops."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the output of `int a[] = {10, 20, 30}; int *p = a; printf(\"%d\", *p++);`?",
                    "options": ["A) 10", "B) 20", "C) 30", "D) Undefined"],
                    "correct_answer": "A) 10",
                    "detailed_solution": "The post-increment returns the current value *p (10) before advancing the pointer to point to 20."
                }
            ],
            "interview_questions": [
                {
                    "question": "How do you check if two strings are anagrams of each other in C?",
                    "company_tag": "Zoho, TCS, Infosys",
                    "answer": "Allocate an integer array of size 256 initialized to zero. Iterate through the first string incrementing counts (`count[s1[i]]++`) and through the second string decrementing counts (`count[s2[i]]--`). If all 256 slots are zero at the end, the strings are anagrams in O(N) time and O(1) space."
                }
            ]
        }
    }
]

