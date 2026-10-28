"""
os_master.py — Prescribed Master Textbook for Operating Systems (OS).
Comprehensive unabridged campus placement textbook covering kernel architecture,
dual-mode operations, interrupt handling, PCB, CPU scheduling (SRTF, Round Robin),
Peterson's algorithm, semaphores, mutexes, classical IPC problems, Banker's algorithm,
paging, TLB EMAT calculations, virtual memory, Belady's anomaly, disk scheduling,
and solved placement interview problems.
"""

OS_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "OS Architecture, Dual-Mode Operations & System Calls",
        "topics": [
            "Dual-mode operation: User Mode (bit 1) vs Kernel Mode (bit 0) hardware protection",
            "Trap interrupts, hardware interrupts, and system call execution lifecycle",
            "Process Control Block (PCB) structure: Program Counter, CPU registers, memory limits, open files",
            "Context switching mechanics, CPU cache flushing overhead, and kernel vs user threads",
            "Monolithic vs Microkernel vs Hybrid kernel architectures"
        ],
        "key_takeaways": "User mode restricts privileged instructions (direct hardware I/O). System calls trigger a software interrupt (trap) to transition the CPU to kernel mode via the interrupt vector table."
    },
    {
        "chapter_num": 2,
        "title": "Process Management, Threads & CPU Scheduling",
        "topics": [
            "Process state diagram: New, Ready, Running, Waiting (Blocked), Terminated",
            "Processes vs Threads: Threads share address space (Heap, Data, Code) but maintain private Stacks and PCs",
            "CPU Scheduling criteria: Turnaround Time, Waiting Time, Response Time, Throughput",
            "Scheduling algorithms: FCFS (Convoy effect), SJF, SRTF (optimal waiting time proof), Round Robin (Quantum tuning), Priority & Aging",
            "Multilevel Feedback Queue (MLFQ) scheduling for interactive vs batch workloads"
        ],
        "key_takeaways": "Shortest Remaining Time First (SRTF) is mathematically provably optimal for minimizing average waiting time. Time quantum in Round Robin must be balanced: too small causes excessive context switches; too large degenerates into FCFS."
    },
    {
        "chapter_num": 3,
        "title": "Process Synchronization, Semaphores & Classical IPC",
        "topics": [
            "Race conditions and Critical Section Problem requirements: Mutual Exclusion, Progress, Bounded Waiting",
            "Peterson's Algorithm proof for two processes (turn and flag array)",
            "Hardware atomic instructions: Test-and-Set and Compare-and-Swap (CAS)",
            "Mutex Locks vs Semaphores (Counting Semaphore vs Binary Semaphore)",
            "Classical concurrency synchronization problems: Producer-Consumer (Bounded Buffer), Readers-Writers, Dining Philosophers"
        ],
        "key_takeaways": "Counting semaphores are initialized to N to guard finite resource pools. Wait/P decrements the semaphore; Signal/V increments it. Mutexes enforce strict thread ownership; binary semaphores do not."
    },
    {
        "chapter_num": 4,
        "title": "Deadlocks: Detection, Prevention & Banker's Avoidance",
        "topics": [
            "4 Coffman Conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait",
            "Resource Allocation Graph (RAG) cycle detection criteria (single vs multiple instances)",
            "Deadlock Prevention: Eliminating each of the 4 Coffman conditions",
            "Dijkstra's Banker's Algorithm for Deadlock Avoidance: Safe state validation and Need Matrix = Max - Allocation",
            "Deadlock Recovery: Process termination and resource preemption with rollback"
        ],
        "key_takeaways": "A deadlock can occur ONLY if all four Coffman conditions hold simultaneously. Banker's Algorithm ensures the system never enters an unsafe state by verifying a safe execution sequence exists before granting resources."
    },
    {
        "chapter_num": 5,
        "title": "Main Memory Management, Paging & Translation Lookaside Buffer (TLB)",
        "topics": [
            "Contiguous memory allocation: Fixed vs Variable partitioning, First-Fit, Best-Fit, Worst-Fit",
            "Internal vs External Fragmentation and compaction mechanics",
            "Non-contiguous allocation: Paging architecture, Page Table Base Register (PTBR), Page Table Entry (PTE)",
            "Translation Lookaside Buffer (TLB): Associative memory, TLB Hit/Miss, Effective Memory Access Time (EMAT) calculations",
            "Multi-level (Hierarchical) paging and Inverted Page Tables for 64-bit systems"
        ],
        "key_takeaways": "Paging eliminates external fragmentation completely but suffers from minor internal fragmentation in the last frame. TLB caches virtual-to-physical address translations in hardware to minimize memory lookup latency."
    },
    {
        "chapter_num": 6,
        "title": "Virtual Memory, Page Replacement & Thrashing",
        "topics": [
            "Demand Paging, Page Fault interrupt service routine lifecycle",
            "Page replacement algorithms: FIFO (Belady's Anomaly proof), Optimal (OPT / MIN), Least Recently Used (LRU), Clock (Second-Chance)",
            "Thrashing phenomenon: High page-fault rate causing CPU utilization to collapse",
            "Working Set Model (Peter Denning) and Page-Fault Frequency (PFF) control",
            "Copy-on-Write (CoW) optimization during fork() system calls"
        ],
        "key_takeaways": "Belady's Anomaly describes the phenomenon where increasing physical page frames paradoxically increases page faults under FIFO. LRU and Optimal belong to the Stack Algorithm family and are immune to Belady's Anomaly."
    },
    {
        "chapter_num": 7,
        "title": "Storage Management, File Systems & Disk Scheduling",
        "topics": [
            "Magnetic disk anatomy: Platters, tracks, sectors, cylinders, seek time vs rotational latency vs transfer time",
            "Disk Scheduling Algorithms: FCFS, SSTF (Shortest Seek Time First, starvation risk), SCAN (Elevator algorithm), C-SCAN, LOOK, C-LOOK",
            "File System allocation methods: Contiguous allocation, Linked allocation, Indexed allocation",
            "UNIX Inode Architecture: Direct blocks, single indirect, double indirect, triple indirect pointers"
        ],
        "key_takeaways": "C-SCAN treats cylinders as a circular list, scanning in one direction only and returning immediately to the beginning without servicing requests on the return path, providing uniform wait times."
    },
    {
        "chapter_num": 8,
        "title": "Solved Placement OS Interview Problems & Concurrency Drills",
        "topics": [
            "CPU Scheduling Round Robin & SRTF Gantt chart calculation walkthroughs",
            "Banker's Algorithm safe sequence step-by-step matrix evaluation",
            "Effective Memory Access Time (EMAT) numerical with 2-level paging and TLB",
            "Belady's Anomaly reference string proof walkthrough",
            "Self-assessment practice exercises with verified solutions"
        ],
        "key_takeaways": "Mastering Gantt chart calculations, Banker's Need matrix, and TLB EMAT equations guarantees top scores in technical tests for Microsoft, Amazon, Cisco, and TCS Digital."
    }
]

OS_TEXTBOOK_MARKDOWN = r"""# Operating Systems & Concurrency Architecture: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Operating Systems (OS)  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, OS technical interviews, and online test evaluations (Microsoft, Amazon, Cisco, Google, TCS Digital) are strictly grounded in the kernel mechanisms, synchronization proofs, memory paging formulas, and scheduling algorithms detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: OS Architecture, Dual-Mode Operations & System Calls](#chapter-1-os-architecture-dual-mode-operations--system-calls)
  - [1.1 Dual-Mode Operation & Hardware Protection](#11-dual-mode-operation--hardware-protection)
  - [1.2 The System Call Execution Lifecycle](#12-the-system-call-execution-lifecycle)
  - [1.3 Process Control Block (PCB) & Context Switching](#13-process-control-block-pcb--context-switching)
  - [1.4 Kernel Architectures: Monolithic vs Microkernel](#14-kernel-architectures-monolithic-vs-microkernel)
- [Chapter 2: Process Management, Threads & CPU Scheduling](#chapter-2-process-management-threads--cpu-scheduling)
  - [2.1 Process State Transition Diagram](#21-process-state-transition-diagram)
  - [2.2 Processes vs Threads Memory Layout](#22-processes-vs-threads-memory-layout)
  - [2.3 CPU Scheduling Metrics & Criteria](#23-cpu-scheduling-metrics--criteria)
  - [2.4 Scheduling Algorithms: FCFS, SJF, SRTF, RR & Priority](#24-scheduling-algorithms-fcfs-sjf-srtf-rr--priority)
- [Chapter 3: Process Synchronization, Semaphores & Classical IPC](#chapter-3-process-synchronization-semaphores--classical-ipc)
  - [3.1 Race Conditions & Critical Section Criteria](#31-race-conditions--critical-section-criteria)
  - [3.2 Peterson's Algorithm & Formal Correctness Proof](#32-petersons-algorithm--formal-correctness-proof)
  - [3.3 Hardware Synchronization: Test-and-Set & CAS](#33-hardware-synchronization-test-and-set--cas)
  - [3.4 Mutexes vs Semaphores](#34-mutexes-vs-semaphores)
  - [3.5 Classical Concurrency Problems: Producer-Consumer & Readers-Writers](#35-classical-concurrency-problems-producer-consumer--readers-writers)
- [Chapter 4: Deadlocks: Detection, Prevention & Banker's Avoidance](#chapter-4-deadlocks-detection-prevention--bankers-avoidance)
  - [4.1 The 4 Coffman Conditions](#41-the-4-coffman-conditions)
  - [4.2 Resource Allocation Graphs (RAG)](#42-resource-allocation-graphs-rag)
  - [4.3 Deadlock Prevention Techniques](#43-deadlock-prevention-techniques)
  - [4.4 Dijkstra's Banker's Algorithm for Avoidance](#44-dijkstras-bankers-algorithm-for-avoidance)
- [Chapter 5: Main Memory Management, Paging & Translation Lookaside Buffer (TLB)](#chapter-5-main-memory-management-paging--translation-lookaside-buffer-tlb)
  - [5.1 Contiguous Allocation & Fragmentation](#51-contiguous-allocation--fragmentation)
  - [5.2 Paging Hardware Architecture](#52-paging-hardware-architecture)
  - [5.3 Translation Lookaside Buffer (TLB) & EMAT Calculations](#53-translation-lookaside-buffer-tlb--emat-calculations)
  - [5.4 Multi-Level & Inverted Page Tables](#54-multi-level--inverted-page-tables)
- [Chapter 6: Virtual Memory, Page Replacement & Thrashing](#chapter-6-virtual-memory-page-replacement--thrashing)
  - [6.1 Demand Paging & Page Fault Handling](#61-demand-paging--page-fault-handling)
  - [6.2 Page Replacement: FIFO, Optimal & LRU](#62-page-replacement-fifo-optimal--lru)
  - [6.3 Belady's Anomaly Proof](#63-beladys-anomaly-proof)
  - [6.4 Thrashing & The Working Set Model](#64-thrashing--the-working-set-model)
- [Chapter 7: Storage Management, File Systems & Disk Scheduling](#chapter-7-storage-management-file-systems--disk-scheduling)
  - [7.1 Disk Drive Geometry & Access Latency](#71-disk-drive-geometry--access-latency)
  - [7.2 Disk Scheduling: FCFS, SSTF, SCAN, C-SCAN](#72-disk-scheduling-fcfs-sstf-scan-c-scan)
  - [7.3 UNIX Inode Architecture & File Allocation](#73-unix-inode-architecture--file-allocation)
- [Chapter 8: Solved Placement OS Interview Problems & Concurrency Drills](#chapter-8-solved-placement-os-interview-problems--concurrency-drills)
  - [Solved Problem 1: Round Robin Scheduling Gantt Chart & Waiting Time](#solved-problem-1-round-robin-scheduling-gantt-chart--waiting-time)
  - [Solved Problem 2: Banker's Algorithm Safe State Determination](#solved-problem-2-bankers-algorithm-safe-state-determination)
  - [Solved Problem 3: Multi-Level Paging EMAT Calculation](#solved-problem-3-multi-level-paging-emat-calculation)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: OS Architecture, Dual-Mode Operations & System Calls

### 1.1 Dual-Mode Operation & Hardware Protection
To prevent buggy or malicious user software from crashing the operating system or reading memory allocated to other users, modern CPU hardware enforces **Dual-Mode Operation**:

```
                       +-------------------------------+
                       | User Space (User Mode: Bit 1)  |
                       |  - Cannot execute privileged   |
                       |    instructions (I/O, HLT)    |
                       +---------------+---------------+
                                       |
                   Trap / Syscall      |      RTI (Return from Interrupt)
                   (Mode Bit: 1 -> 0)  |      (Mode Bit: 0 -> 1)
                                       v
                       +---------------+---------------+
                       | Kernel Space (Kernel Mode: 0)  |
                       |  - Full access to all hardware |
                       |    registers and CPU memory   |
                       +-------------------------------+
```

1. **User Mode (Mode Bit = 1):** The CPU restricts execution of privileged instructions. Attempting to execute instructions such as `HLT` (halt CPU), modifying base/limit memory registers, or initiating direct hardware I/O instructions causes the CPU to throw a hardware protection exception.
2. **Kernel / Supervisor Mode (Mode Bit = 0):** The CPU possesses unrestricted access to all hardware instructions, memory spaces, and peripheral devices.
3. **Transition Mechanics:** The mode bit is switched from `1` to `0` exclusively via **Hardware Interrupts** (e.g., timer interrupt, keyboard press) or **Software Interrupts / Traps** (e.g., executing a system call, divide-by-zero exception). When the kernel finishes handling the trap, it executes the privileged `RTI` instruction, resetting the mode bit to `1`.

### 1.2 The System Call Execution Lifecycle
A system call provides the programmatic interface between an application in user space and the services provided by the kernel:

1. User application calls a library wrapper function (e.g., `read()` in POSIX C).
2. The library sets up system call parameters in designated CPU registers (e.g., file descriptor, buffer pointer, byte length).
3. Places the unique **System Call Number** in register `EAX` / `RAX`.
4. Executes the software interrupt instruction (`syscall` in x86-64, `int 0x80` in x86-32, `svc` in ARM).
5. Hardware switches CPU Mode Bit from `1` to `0`, saves the user Program Counter (`PC`) on the Kernel Stack, and jumps to the address loaded in the **Interrupt Vector Table (IVT)**.
6. The kernel dispatch table reads `RAX`, executes `sys_read()`, validates user pointers, and reads data from the hardware disk controller into the buffer.
7. Kernel places the return status in register `RAX`, executes `sysret` / `iret`, restoring Mode Bit to `1` and resuming user application execution.

### 1.3 Process Control Block (PCB) & Context Switching
A process is a program in execution. The operating system kernel tracks every process using a dedicated data structure called the **Process Control Block (PCB)**:

```
+-----------------------------------------------------------+
| Process Control Block (PCB) Structure                     |
+-----------------------------------------------------------+
| Process ID (PID) & Parent Process ID (PPID)               |
| Process State (Ready, Running, Waiting, Terminated)       |
| Program Counter (PC) (Memory address of next instruction) |
| CPU Registers (Accumulator, Index Registers, Stack Pointer)|
| CPU Scheduling Info (Priority, Queue Pointers)            |
| Memory Management Info (Page Tables, Segment Tables)      |
| Accounting Info (CPU time consumed, Process limits)       |
| I/O Status Info (List of open file descriptors, devices)  |
+-----------------------------------------------------------+
```

**Context Switch Mechanics:**
Switching the CPU core from executing Process $P_1$ to Process $P_2$:
1. Save the hardware context of $P_1$ (PC, registers, stack pointer) into $P_1$'s PCB.
2. Update $P_1$'s state to Ready (or Waiting).
3. The CPU scheduler selects $P_2$ from the Ready Queue.
4. Load $P_2$'s hardware context from $P_2$'s PCB into CPU registers.
5. Invalidate / flush the Memory Management Unit's Translation Lookaside Buffer (TLB) unless Address Space Identifiers (ASID) are supported.
6. Set Program Counter to $P_2$'s saved instruction pointer and resume execution.
- **Overhead:** Context switching is pure computational overhead; during a context switch, the CPU performs zero useful user work. It takes typically 1 to 5 microseconds.

### 1.4 Kernel Architectures: Monolithic vs Microkernel
- **Monolithic Kernel (Linux, UNIX):** All operating system services (Virtual Memory, Process Scheduler, File Systems, Device Drivers, Network Stack) run together inside kernel space in a single address space.
  - *Advantage:* Blazing-fast IPC; system calls execute as simple in-memory function calls.
  - *Disadvantage:* A crash in a third-party printer device driver can crash the entire kernel.
- **Microkernel (Mach, QNX, Minix):** Strips kernel down to the absolute bare minimum: Inter-Process Communication (IPC), basic low-level scheduling, and low-level memory mapping. File systems, networking, and drivers run in **User Space** as independent user processes.
  - *Advantage:* High reliability and fault isolation.
  - *Disadvantage:* Significant performance overhead due to repeated context switches and IPC message copying between user processes and the microkernel.

---

## Chapter 2: Process Management, Threads & CPU Scheduling

### 2.1 Process State Transition Diagram
A process transitions through distinct states during its lifecycle:

```
            +-------------+
            |     New     |
            +------+------+
                   | Admitted by Long-Term Scheduler
                   v
            +-------------+    Dispatch (Short-Term Scheduler)    +-------------+
   +------->|    Ready    |-------------------------------------->|   Running   |
   |        +-------------+                                       +------+------+
   |               ^                                                     |
   | I/O or Event  |                Interrupt (Timer / Preemption)        |
   | Completion    +-----------------------------------------------------+
   |                                                                     |
   |        +-------------+         I/O or Wait for Event / Child        |
   +--------|   Waiting   |<---------------------------------------------+
            |  (Blocked)  |
            +-------------+
```

- **New:** Process is being created.
- **Ready:** Loaded in memory and waiting to be allocated CPU time by the scheduler.
- **Running:** Instructions are currently being executed on a CPU core.
- **Waiting (Blocked):** Process is suspended waiting for an external event (I/O completion, child process exit). Cannot run even if CPU is completely idle!
- **Terminated:** Process has completed execution; OS is reclaiming resources.

### 2.2 Processes vs Threads Memory Layout
A **Thread** (Lightweight Process) is the basic unit of CPU execution. Multiple threads within the same process share:
- **Shared Memory:** Code (Text) Segment, Data (Global/Static) Segment, Heap (Dynamic allocations), and OS Resources (Open File Descriptors, Network Sockets).
- **Private Per-Thread Memory:** Thread ID, Program Counter (PC), Register Set, and **Private Stack** (local function parameters and return frames).

```
Single-Threaded Process:                Multi-Threaded Process:
+-----------------------------------+   +-----------------------------------+
| Code | Data | Heap                |   | Code | Data | Heap                |
| Open Files                        |   | Open Files                        |
| Stack (Process Stack)             |   | Stack (T1) | Stack (T2) | Stack(T3)|
| Registers, PC                     |   | Regs/PC(T1)| Regs/PC(T2)|Regs/PC(T3)|
+-----------------------------------+   +-----------------------------------+
```

### 2.3 CPU Scheduling Metrics & Criteria
Let Arrival Time be $AT$, Burst Time be $BT$, and Completion Time be $CT$:
1. **Turnaround Time ($TAT$):** Total elapsed time from process arrival to final termination:
   $$TAT = CT - AT$$
2. **Waiting Time ($WT$):** Total time the process spent waiting in the Ready queue:
   $$WT = TAT - BT$$
3. **Response Time ($RT$):** Time from process arrival to first CPU allocation:
   $$RT = \text{First Run Time} - AT$$
4. **Throughput:** Number of processes completed per unit time.

### 2.4 Scheduling Algorithms: FCFS, SJF, SRTF, RR & Priority
- **First-Come, First-Served (FCFS):** Non-preemptive. Simple FIFO queue.
  - *Convoy Effect:* Short I/O-bound processes get stuck waiting behind one massive CPU-bound process, resulting in terrible average waiting times.
- **Shortest Job First (SJF):** Non-preemptive. Associates each process with its next CPU burst length.
  - *Provably Optimal Theorem:* Minimizes average waiting time among all non-preemptive algorithms.
- **Shortest Remaining Time First (SRTF):** Preemptive version of SJF. If a newly arrived process has a burst time shorter than the remaining burst of the currently running process, the CPU preempts the current process!
- **Round Robin (RR):** Preemptive. Allocates each process a fixed slice of time called a **Time Quantum ($q$)**.
  - If $q$ is extremely large ($q \to \infty$): RR degenerates into **FCFS**.
  - If $q$ is extremely small ($q \to 0$): System behaves as processor sharing (each of $N$ processes has a virtual processor running at $1/N$ speed), but CPU wastes 90% of cycles on context switching overhead!
  - *Rule of Thumb:* 80% of CPU bursts should be shorter than the time quantum $q$ (typically $10\text{ms}$ to $50\text{ms}$).

---

## Chapter 3: Process Synchronization, Semaphores & Classical IPC

### 3.1 Race Conditions & Critical Section Criteria
A **Race Condition** occurs when multiple processes or threads concurrently read and write shared memory, and the final outcome depends on the non-deterministic execution order of thread scheduling.

The **Critical Section** is the block of code where shared resources are modified. Any valid solution to the Critical Section Problem must satisfy three mandatory criteria:
1. **Mutual Exclusion:** If process $P_i$ is executing in its critical section, no other process can be executing in their critical section.
2. **Progress:** If no process is executing in its critical section and some processes wish to enter, only those processes not executing in their remainder section can participate in deciding who enters next, and this selection cannot be postponed indefinitely.
3. **Bounded Waiting:** A bound must exist on the number of times other processes are allowed to enter their critical sections after a process has made a request to enter and before that request is granted (prevents starvation).

### 3.2 Peterson's Algorithm & Formal Correctness Proof
Peterson's Algorithm is a classic software-based solution for two concurrent processes ($P_0$ and $P_1$):

```c
// Shared variables:
boolean flag[2]; // flag[i] = true indicates Pi is ready to enter critical section
int turn;        // indicates whose turn it is to enter

// Process Pi (where j = 1 - i):
do {
    flag[i] = true;         // Announce intent to enter
    turn = j;               // Give turn to other process (polite gesture)
    while (flag[j] && turn == j); // Busy wait (spin lock)

    // CRITICAL SECTION
    
    flag[i] = false;        // Exit section

    // REMAINDER SECTION
} while (true);
```

**Formal Correctness Proof:**
- **Mutual Exclusion:** For both $P_0$ and $P_1$ to be in the critical section simultaneously, both `while` loop conditions must have been false simultaneously. That requires:
  $$(\text{flag}[1] == \text{false} \lor \text{turn} == 0) \land (\text{flag}[0] == \text{false} \lor \text{turn} == 1)$$
  Since both processes set their `flag` to `true`, this requires $\text{turn} == 0$ AND $\text{turn} == 1$ simultaneously. Because `turn` is a scalar variable that can hold only one value at any instant, a contradiction arises. Mutual Exclusion is preserved!

### 3.3 Hardware Synchronization: Test-and-Set & CAS
Modern multicore CPUs provide hardware atomic instructions executed with hardware cache-bus locks:
- **Test-and-Set:** Atomically reads a memory location and sets it to `true`.
- **Compare-and-Swap (CAS):** Atomically checks if memory holds expected value $A$; if yes, writes new value $B$. Foundational to Java's `java.util.concurrent.atomic` and lock-free data structures.

### 3.4 Mutexes vs Semaphores
- **Mutex (Mutual Exclusion Lock):** A binary locking mechanism with strict **Thread Ownership**. The thread that acquires (locks) the mutex MUST be the exact same thread that releases (unlocks) it.
- **Counting Semaphore (Dijkstra):** An integer variable $S$ accessed exclusively via two atomic operations:
  - `wait(S)` (or `P(S)` - Dutch *proberen* / test):
    ```c
    wait(S) {
        while (S <= 0); // Busy wait (or sleep in blocking semaphore)
        S--;
    }
    ```
  - `signal(S)` (or `V(S)` - Dutch *verhogen* / increment):
    ```c
    signal(S) {
        S++;
    }
    ```
  - *No Ownership:* Any thread can signal a semaphore to wake up waiting threads (ideal for signaling events).

### 3.5 Classical Concurrency Problems: Producer-Consumer & Readers-Writers
#### The Bounded-Buffer (Producer-Consumer) Problem
Using counting semaphores `empty` (initialized to buffer capacity $N$) and `full` (initialized to $0$), and binary mutex `mutex` (initialized to $1$):

```c
// Producer:
do {
    // produce item
    wait(empty);  // Decrement empty slots (blocks if buffer is full)
    wait(mutex);  // Lock buffer
    // add item to buffer
    signal(mutex);// Unlock buffer
    signal(full); // Increment full slots (wakes up waiting consumer)
} while (true);

// Consumer:
do {
    wait(full);   // Decrement full slots (blocks if buffer is empty)
    wait(mutex);  // Lock buffer
    // remove item from buffer
    signal(mutex);// Unlock buffer
    signal(empty);// Increment empty slots (wakes up waiting producer)
    // consume item
} while (true);
```

---

## Chapter 4: Deadlocks: Detection, Prevention & Banker's Avoidance

### 4.1 The 4 Coffman Conditions
A deadlock can occur if and only if all four conditions hold simultaneously in the system:
1. **Mutual Exclusion:** At least one resource must be held in a non-shareable mode (only one process at a time).
2. **Hold and Wait:** A process must be currently holding at least one resource and requesting additional resources that are currently being held by other processes.
3. **No Preemption:** Resources cannot be forcibly preempted from a process; they can only be released voluntarily by the holding process after completing its task.
4. **Circular Wait:** A closed chain of processes $\{P_0, P_1, \dots, P_n\}$ exists such that $P_0$ is waiting for a resource held by $P_1$, $P_1$ is waiting for $P_2$, ..., and $P_n$ is waiting for $P_0$.

### 4.2 Resource Allocation Graphs (RAG)
- Directed Graph $G = (V, E)$ with Process nodes $P_i$ and Resource nodes $R_j$.
- **Request Edge ($P_i \to R_j$):** Directed from process to resource.
- **Assignment Edge ($R_j \to P_i$):** Directed from resource instance to process.
- **Cycle Theorem:**
  - If the RAG contains **no cycles**, the system is **guaranteed deadlock-free**.
  - If the RAG contains a cycle and every resource has **strictly 1 instance**, **deadlock has occurred**.
  - If resources have multiple instances, a cycle indicates a *potential* deadlock, not a certainty.

### 4.3 Deadlock Prevention Techniques
Eliminating at least one of the 4 Coffman conditions:
1. **Eliminate Mutual Exclusion:** Make resources shareable (e.g., read-only files). Impossible for write-intensive hardware like printers or mutex locks.
2. **Eliminate Hold and Wait:** Mandate that a process must request and receive ALL required resources at once before beginning execution, or release held resources before requesting new ones (low resource utilization).
3. **Eliminate No Preemption:** If process holding resources requests an unavailable resource, all of its held resources are preempted and returned to the free pool.
4. **Eliminate Circular Wait (Havender's Protocol):** Impose a strict global linear ordering function $F: R \to \mathbb{N}$ on all resource types. Mandate that processes can request resources strictly in **monotonically increasing order** ($F(R_i) < F(R_j)$). Mathematically prevents cycles!

### 4.4 Dijkstra's Banker's Algorithm for Avoidance
Let $n$ be number of processes and $m$ be number of resource types:
- **Available $[m]$:** Vector of available instances per resource type.
- **Max $[n \times m]$:** Maximum demand of each process.
- **Allocation $[n \times m]$:** Resources currently allocated to each process.
- **Need $[n \times m]$:** Remaining resources needed to complete:
  $$\text{Need}[i][j] = \text{Max}[i][j] - \text{Allocation}[i][j]$$

**Safety Algorithm:**
1. Initialize `Work = Available` and `Finish[i] = false` for all $i$.
2. Find an index $i$ such that:
   $$\text{Finish}[i] == \text{false} \land \text{Need}[i] \le \text{Work}$$
   If no such $i$ exists, jump to step 4.
3. $\text{Work} = \text{Work} + \text{Allocation}[i]$; $\text{Finish}[i] = \text{true}$. Repeat from step 2.
4. If $\text{Finish}[i] == \text{true}$ for ALL $i$, the system is in a **Safe State**; otherwise, it is in an **Unsafe State**.

---

## Chapter 5: Main Memory Management, Paging & Translation Lookaside Buffer (TLB)

### 5.1 Contiguous Allocation & Fragmentation
- **Internal Fragmentation:** Memory allocated to a process is slightly larger than requested memory. Unused memory inside the allocated partition is wasted (e.g., allocating a 4 KB frame to a 1 KB process wastes 3 KB).
- **External Fragmentation:** Total free memory space exists to satisfy a request, but the available storage is fragmented into tiny non-contiguous slivers. Overcome via non-contiguous allocation (**Paging**).

### 5.2 Paging Hardware Architecture
The Memory Management Unit (MMU) splits logical addresses into:
- **Page Number ($p$):** Used as an index into the process's **Page Table**.
- **Page Offset ($d$):** Offset within the page.

Physical Address $= \text{Frame Number }(f) \times \text{Page Size} + d$.

```
Logical Address: [ Page Number (p) | Offset (d) ]
                         |
                         v
                +-----------------+
                |   Page Table    |
                | p -> Frame f    |
                +-----------------+
                         |
                         v
Physical Address: [ Frame Number (f) | Offset (d) ]
```

### 5.3 Translation Lookaside Buffer (TLB) & EMAT Calculations
A hardware associative cache storing recent virtual-to-physical address mappings:
Let $h$ be the **TLB Hit Ratio**, $t_{\text{tlb}}$ be TLB lookup time, and $t_{\text{mem}}$ be main memory access time:

$$\text{EMAT} = h \cdot (t_{\text{tlb}} + t_{\text{mem}}) + (1 - h) \cdot (t_{\text{tlb}} + 2 \cdot t_{\text{mem}})$$

*(Note: On a TLB Miss, the MMU accesses the page table in memory ($t_{\text{mem}}$), and then fetches the actual data operand ($t_{\text{mem}}$), totalling $2 \cdot t_{\text{mem}}$).*

### 5.4 Multi-Level & Inverted Page Tables
- **Multi-Level Paging:** Breaks hierarchical page tables into multi-level pages to avoid keeping non-contiguous unused page table entries in memory. For a $k$-level page table, memory access on TLB miss requires $k + 1$ memory lookups.
- **Inverted Page Table:** Maintains one entry per physical frame in memory rather than per virtual page, indexed by $\langle \text{PID}, \text{PageNumber} \rangle$.

---

## Chapter 6: Virtual Memory, Page Replacement & Thrashing

### 6.1 Demand Paging & Page Fault Handling
Pages are loaded into RAM only when referenced during execution (**Lazy Swapper**):
1. CPU references virtual memory address.
2. MMU checks valid/invalid bit in Page Table Entry.
3. If bit is `0` (invalid), a **Page Fault Trap** is triggered.
4. OS traps to kernel, suspends process, and locates requested page on backing swap disk.
5. OS selects a free frame (or executes page replacement to evict a victim page, writing it to disk if dirty bit is 1).
6. Reads requested page from disk into the allocated physical frame.
7. Updates page table valid bit to `1` and restarts the interrupted instruction!

### 6.2 Page Replacement: FIFO, Optimal & LRU
1. **FIFO (First-In, First-Out):** Replaces the oldest page loaded into memory.
2. **Optimal Page Replacement (OPT / MIN):** Replaces the page that will not be used for the longest period of time in the future. Provably optimal minimum page faults (used as a theoretical benchmark).
3. **Least Recently Used (LRU):** Replaces the page that has not been referenced for the longest period of time in the past (approximates OPT using past history).

### 6.3 Belady's Anomaly Proof
**Belady's Anomaly:** The counter-intuitive phenomenon where increasing the number of physical page frames results in an **INCREASE** in page faults.
- Occurs under **FIFO** replacement for reference strings such as:
  $$1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5$$
  - With 3 frames: **9 page faults**.
  - With 4 frames: **10 page faults!**
- **Stack Algorithms:** Algorithms where the set of pages in memory for $N$ frames is always a strict subset of the pages in memory for $N + 1$ frames ($M(N) \subset M(N+1)$). LRU and Optimal are stack algorithms and are **provably immune to Belady's Anomaly**.

### 6.4 Thrashing & The Working Set Model
- **Thrashing:** When a process does not have enough physical page frames, it spends more time paging (swapping pages in and out of disk) than executing useful instructions. CPU utilization drops to near zero.
- **Working Set Model (Peter Denning):**
  - Defines the working-set window $\Delta$.
  - Working Set $WSS_i = \text{total pages referenced in the most recent } \Delta \text{ time units}$.
  - System demand $D = \sum WSS_i$.
  - If $D > \text{Total Memory Frames}$, thrashing occurs; the OS must suspend one or more processes to restore stability.

---

## Chapter 7: Storage Management, File Systems & Disk Scheduling

### 7.1 Disk Drive Geometry & Access Latency
$$\text{Total Disk Access Time} = \text{Seek Time} + \text{Rotational Latency} + \text{Transfer Time}$$
- **Seek Time:** Time for read/write head to move to target cylinder track ($T_{\text{seek}} \approx 3-10\text{ms}$).
- **Rotational Latency:** Time for target sector to rotate beneath the head:
  $$\text{Average Rotational Latency} = \frac{1}{2 \times \text{RPM}} \times 60 \text{ seconds}$$
  *(For 7200 RPM disk: $\frac{60}{14400} \approx 4.16\text{ms}$).*

### 7.2 Disk Scheduling: FCFS, SSTF, SCAN, C-SCAN
- **Shortest Seek Time First (SSTF):** Selects request closest to current head position. Minimizes seek time but causes starvation of distant requests.
- **SCAN (Elevator Algorithm):** Head sweeps in one direction servicing requests until reaching the end of the disk, then reverses direction.
- **C-SCAN (Circular SCAN):** Head sweeps in one direction servicing requests. When it reaches the end, it immediately returns to the beginning of the disk without servicing any requests on the return trip, providing uniform wait times.

### 7.3 UNIX Inode Architecture & File Allocation
An Inode (Index Node) contains file metadata (owner, permissions, size, timestamps) and direct/indirect block pointers:
- 12 Direct Pointers (point directly to data blocks).
- 1 Single Indirect Pointer (points to a block containing pointers).
- 1 Double Indirect Pointer (points to a block containing single indirect blocks).
- 1 Triple Indirect Pointer (enables support for multi-terabyte files).

---

## Chapter 8: Solved Placement OS Interview Problems & Concurrency Drills

### Solved Problem 1: Round Robin Scheduling Gantt Chart & Waiting Time
- **Problem:** Given processes arriving at time $AT = 0$:
  - $P_1: BT = 5\text{ ms}$
  - $P_2: BT = 3\text{ ms}$
  - $P_3: BT = 1\text{ ms}$
  Time quantum $q = 2\text{ ms}$. Compute completion times, turnaround times, and average waiting time.
- **Solution:**
  1. Gantt Chart:
     `[P1: 0-2] -> [P2: 2-4] -> [P3: 4-5] -> [P1: 5-7] -> [P2: 7-8] -> [P1: 8-9]`
  2. Completion Times:
     - $P_3$ completes at $CT = 5\text{ ms}$.
     - $P_2$ completes at $CT = 8\text{ ms}$.
     - $P_1$ completes at $CT = 9\text{ ms}$.
  3. Turnaround Times ($TAT = CT - AT$):
     - $TAT(P_1) = 9 - 0 = 9\text{ ms}$.
     - $TAT(P_2) = 8 - 0 = 8\text{ ms}$.
     - $TAT(P_3) = 5 - 0 = 5\text{ ms}$.
  4. Waiting Times ($WT = TAT - BT$):
     - $WT(P_1) = 9 - 5 = 4\text{ ms}$.
     - $WT(P_2) = 8 - 3 = 5\text{ ms}$.
     - $WT(P_3) = 5 - 1 = 4\text{ ms}$.
  5. Average Waiting Time:
     $$\text{Avg } WT = \frac{4 + 5 + 4}{3} = \frac{13}{3} = \mathbf{4.33\text{ ms}}$$

### Solved Problem 2: Banker's Algorithm Safe State Determination
- **Problem:** System with 3 processes ($P_0, P_1, P_2$) and 1 resource type with 10 total instances.
  - Allocation: $P_0 = 2, P_1 = 3, P_2 = 2$.
  - Max: $P_0 = 5, P_1 = 6, P_2 = 4$.
  Is the system in a safe state? If yes, find a safe sequence.
- **Solution:**
  1. Total allocated $= 2 + 3 + 2 = 7$.
  2. Available $= 10 - 7 = 3$.
  3. Compute Need matrix:
     - $\text{Need}(P_0) = 5 - 2 = 3$.
     - $\text{Need}(P_1) = 6 - 3 = 3$.
     - $\text{Need}(P_2) = 4 - 2 = 2$.
  4. Safety Check:
     - Available $= 3$. Can we satisfy $P_2$? $\text{Need}(P_2) = 2 \le 3$.
     - Allocate to $P_2$, run to completion. Reclaims: $\text{Available} = 3 + 2 = 5$.
     - Now Available $= 5$. Can we satisfy $P_0$? $\text{Need}(P_0) = 3 \le 5$.
     - Allocate to $P_0$, run to completion. Reclaims: $\text{Available} = 5 + 2 = 7$.
     - Now Available $= 7$. Can we satisfy $P_1$? $\text{Need}(P_1) = 3 \le 7$.
     - Allocate to $P_1$, run to completion.
  5. **Safe Sequence:** $\mathbf{\langle P_2, P_0, P_1 \rangle}$ (or $\langle P_0, P_2, P_1 \rangle$). System is in a **Safe State**.

### Solved Problem 3: Multi-Level Paging EMAT Calculation
- **Problem:** A 32-bit system uses 2-level paging. Main memory access time is $100\text{ ns}$, TLB lookup time is $20\text{ ns}$, and TLB hit ratio is $90\%$. What is the Effective Memory Access Time?
- **Solution:**
  1. For 2-level paging, a TLB miss requires accessing:
     - Outer Page Table ($100\text{ ns}$)
     - Inner Page Table ($100\text{ ns}$)
     - Physical Data Frame ($100\text{ ns}$)
     - Total miss access time $= t_{\text{tlb}} + 3 \cdot t_{\text{mem}} = 20 + 300 = 320\text{ ns}$.
  2. A TLB hit requires:
     - TLB lookup ($20\text{ ns}$) + Physical Data Frame ($100\text{ ns}$) $= 120\text{ ns}$.
  3. $\text{EMAT} = 0.90(120) + 0.10(320) = 108 + 32 = \mathbf{140\text{ ns}}$.

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Semaphore Value):** A counting semaphore initialized to 7 undergoes $12\text{ wait}()$ operations and $9\text{ signal}()$ operations. What is its final value?
   - *Solution:* $\text{Value} = 7 - 12 + 9 = \mathbf{4}$.

2. **Exercise 2 (Deadlock Free Condition):** A system has $P$ processes, and each process needs at most $K$ units of resource $R$. What is the minimum number of units of $R$ required to ensure deadlock can never occur?
   - *Solution:* $R \ge P \cdot (K - 1) + 1$.

3. **Exercise 3 (Belady's Anomaly Immunity):** Why are LRU and Optimal algorithms immune to Belady's Anomaly?
   - *Solution:* Both belong to the class of **Stack Algorithms**, where the set of pages stored in $N$ frames is mathematically guaranteed to be a strict subset of the pages stored in $N+1$ frames for any reference string at any step.

4. **Exercise 4 (Aging Technique):** How does the Aging technique prevent starvation in Priority Scheduling?
   - *Solution:* Aging gradually increases the priority of processes that wait in the ready queue for extended periods of time, guaranteeing that even the lowest-priority process eventually achieves the highest priority and executes.

5. **Exercise 5 (Copy-on-Write Benefit):** How does Copy-on-Write (CoW) optimize the `fork()` system call when immediately followed by `exec()`?
   - *Solution:* Instead of duplicating the entire parent process address space in RAM during `fork()`, parent and child share the same physical pages marked read-only. If the child calls `exec()` immediately, new code is loaded without ever copying the parent's memory pages.
"""

OS_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "OS Architecture, Dual-Mode Operations & System Calls",
        "subtopic": "Dual-Mode Execution",
        "question": "What happens at the hardware level when a user application program executes a system call instruction?",
        "options": [
            "A software interrupt (trap) transitions the CPU Mode Bit from 1 (User) to 0 (Kernel) and jumps to the Interrupt Vector Table",
            "The program terminates immediately and reboots the operating system",
            "The CPU increases its clock frequency to execute instructions in parallel",
            "Memory management units allocate a new virtual thread"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [OS Prescribed Textbook — Chapter 1: OS Architecture]\nA system call executes a trap instruction, setting the hardware mode bit to 0 (Kernel Mode) and passing control to the kernel interrupt vector table.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 4,
        "chapter_title": "Deadlocks: Detection, Prevention & Banker's Avoidance",
        "subtopic": "Coffman Conditions",
        "question": "Which of the following conditions is NOT one of the four mandatory Coffman conditions required for a deadlock to occur?",
        "options": [
            "Preemptive Resource Allocation",
            "Mutual Exclusion",
            "Hold and Wait",
            "Circular Wait"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [OS Prescribed Textbook — Chapter 4: Deadlocks]\nThe four Coffman conditions are Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. Preemption breaks deadlocks; 'No Preemption' is the condition that enables them.",
        "difficulty": "easy",
    }
]
