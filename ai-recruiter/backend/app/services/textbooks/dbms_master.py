"""
dbms_master.py — Prescribed Master Textbook for Database Management Systems (DBMS).
Comprehensive unabridged campus placement textbook covering 3-schema architecture,
ER modeling, relational algebra & calculus, functional dependencies, Armstrong's axioms,
1NF, 2NF, 3NF, BCNF, ACID transactions, conflict serializability, strict 2PL,
Write-Ahead Logging (WAL), ARIES recovery, B+ trees, and placement interview questions.
"""

DBMS_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "DBMS Architecture, Relational Model & ER Modeling",
        "topics": [
            "3-Schema Architecture: Physical, Conceptual, External views & Data Independence",
            "Entity-Relationship (ER) Modeling: Strong vs Weak entities, Cardinality ratios",
            "Specialization, Generalization, Aggregation & Enhanced ER (EER) concepts",
            "Algorithm for mapping ER diagrams to Relational schemas (foreign keys, associative tables)",
            "Relational Model constraints: Domain, Key, Entity Integrity, Referential Integrity (ON DELETE CASCADE)"
        ],
        "key_takeaways": "Logical Data Independence protects conceptual schema from physical storage modifications. Weak entities have no primary key of their own and depend on an identifying owner entity via a discriminator."
    },
    {
        "chapter_num": 2,
        "title": "Relational Algebra, Tuple Calculus & Query Processing",
        "topics": [
            "Fundamental operators: Selection (sigma), Projection (pi), Union, Set Difference, Cartesian Product (X)",
            "Derived operators: Natural Join (bowtie), Theta Join, Equi-Join, Semijoin, Division (/)",
            "Outer Joins: Left Outer Join, Right Outer Join, Full Outer Join semantics",
            "Tuple Relational Calculus (TRC) vs Domain Relational Calculus (DRC)",
            "Query optimization: Heuristic query execution trees, pushing selections down"
        ],
        "key_takeaways": "The Division operator (A / B) solves 'all' queries (e.g., find students enrolled in ALL courses taught by Professor X). Pushing selections down reduces Cartesian product sizes early."
    },
    {
        "chapter_num": 3,
        "title": "Functional Dependencies, Normalization & Decomposition (1NF to BCNF)",
        "topics": [
            "Functional Dependencies (FDs) definition and Armstrong's Axioms (Reflexivity, Augmentation, Transitivity)",
            "Attribute Closure (X+) algorithm and Candidate Key determination",
            "Minimal / Canonical Cover computation algorithm",
            "Normal Forms: 1NF (atomic values), 2NF (no partial dependency), 3NF (no transitive dependency), BCNF (strictly superkey LHS)",
            "Decomposition properties: Lossless Join test (R1 intersection R2 -> R1 or R2) and Dependency Preservation test"
        ],
        "key_takeaways": "A relation is in BCNF if for every non-trivial FD X -> Y, X is a superkey. BCNF decomposition guarantees lossless join, but does not always preserve functional dependencies; 3NF guarantees both."
    },
    {
        "chapter_num": 4,
        "title": "Transaction Management, ACID Properties & Concurrency Control",
        "topics": [
            "ACID properties: Atomicity (WAL), Consistency, Isolation (Locks), Durability",
            "Transaction states: Active, Partially Committed, Failed, Aborted, Committed",
            "Schedules & Serializability: Conflict Serializability vs View Serializability",
            "Precedence Graph (Serialization Graph) topological sorting for cycle detection",
            "Concurrency anomalies: Dirty Read (read uncommitted), Non-repeatable Read, Phantom Read, Lost Update",
            "Concurrency control protocols: Two-Phase Locking (2PL, Strict 2PL, Rigorous 2PL), Timestamp Ordering"
        ],
        "key_takeaways": "A schedule is conflict serializable if its precedence graph contains no directed cycles. Strict 2PL prevents cascading rollbacks by holding exclusive write locks until the transaction commits."
    },
    {
        "chapter_num": 5,
        "title": "Crash Recovery & Storage Architecture: WAL & ARIES",
        "topics": [
            "Failure classification: Transaction failure, System crash, Disk failure",
            "Buffer management policies: Steal / No-Steal and Force / No-Force",
            "Write-Ahead Logging (WAL) protocol: Log record must reach non-volatile disk before database page",
            "Checkpointing mechanics: Checkpoint records and active transaction tables",
            "ARIES recovery algorithm: Analysis phase, Redo phase (repeating history), Undo phase (rolling back losers)"
        ],
        "key_takeaways": "Modern enterprise DBMS use Steal/No-Force buffer management for maximum throughput, necessitating both Redo and Undo operations during crash recovery governed by the WAL protocol."
    },
    {
        "chapter_num": 6,
        "title": "Database Storage, File Organization & B+ Tree Indexing",
        "topics": [
            "Storage hierarchy: Memory vs Flash SSD vs Magnetic HDD block access",
            "File organization: Heap files, Sorted files, Hashing (Static vs Dynamic Extendible Hashing)",
            "Indexing architectures: Clustered vs Non-clustered, Primary vs Secondary, Dense vs Sparse indices",
            "B-Trees vs B+ Trees structural comparison (data pointers exclusively in leaf nodes in B+ Trees)",
            "B+ Tree operations: Search O(log_B N), node splitting on overflow, node merging on underflow"
        ],
        "key_takeaways": "B+ Trees store all actual record pointers in leaf nodes linked as a doubly-linked list, providing both O(log N) point queries and lightning-fast sequential range scans."
    },
    {
        "chapter_num": 7,
        "title": "Solved DBMS Placement Problems & Interview Assessment Drills",
        "topics": [
            "Candidate key computation step-by-step proofs",
            "Normal form classification & BCNF lossless decomposition",
            "Precedence graph cycle tracing for conflict serializability",
            "B+ Tree fanout, height, and maximum record capacity calculations",
            "SQL vs Relational Algebra translation puzzles"
        ],
        "key_takeaways": "Mastering Armstrong closure, serializability precedence graphs, and B+ tree node order equations guarantees top-percentile placement technical test performance."
    }
]

DBMS_TEXTBOOK_MARKDOWN = r"""# Database Management Systems: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Database Management Systems (DBMS)  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, DBMS technical interviews, and online test questions are strictly grounded in the relational algebra, normalization theorems, concurrency protocols, and indexing mathematics detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: DBMS Architecture, Relational Model & ER Modeling](#chapter-1-dbms-architecture-relational-model--er-modeling)
  - [1.1 3-Schema Architecture & Data Independence](#11-3-schema-architecture--data-independence)
  - [1.2 Entity-Relationship (ER) Modeling Principles](#12-entity-relationship-er-modeling-principles)
  - [1.3 Mapping ER Diagrams to Relational Schemas](#13-mapping-er-diagrams-to-relational-schemas)
  - [1.4 Relational Integrity Constraints](#14-relational-integrity-constraints)
- [Chapter 2: Relational Algebra, Tuple Calculus & Query Processing](#chapter-2-relational-algebra-tuple-calculus--query-processing)
  - [2.1 Fundamental & Derived Relational Algebra Operators](#21-fundamental--derived-relational-algebra-operators)
  - [2.2 The Relational Division Operator for Universal Quantification](#22-the-relational-division-operator-for-universal-quantification)
  - [2.3 Query Trees & Heuristic Optimization](#23-query-trees--heuristic-optimization)
- [Chapter 3: Functional Dependencies, Normalization & Decomposition (1NF to BCNF)](#chapter-3-functional-dependencies-normalization--decomposition-1nf-to-bcnf)
  - [3.1 Functional Dependencies & Armstrong's Axioms](#31-functional-dependencies--armstrongs-axioms)
  - [3.2 Candidate Key Determination via Attribute Closure](#32-candidate-key-determination-via-attribute-closure)
  - [3.3 Normal Forms Hierarchy: 1NF, 2NF, 3NF & BCNF](#33-normal-forms-hierarchy-1nf-2nf-3nf--bcnf)
  - [3.4 Lossless Join & Dependency Preservation Proofs](#34-lossless-join--dependency-preservation-proofs)
- [Chapter 4: Transaction Management, ACID Properties & Concurrency Control](#chapter-4-transaction-management-acid-properties--concurrency-control)
  - [4.1 ACID Properties Deep Dive](#41-acid-properties-deep-dive)
  - [4.2 Concurrency Anomalies & SQL Isolation Levels](#42-concurrency-anomalies--sql-isolation-levels)
  - [4.3 Conflict Serializability & Precedence Graphs](#43-conflict-serializability--precedence-graphs)
  - [4.4 Locking Protocols: 2PL, Strict 2PL & Rigorous 2PL](#44-locking-protocols-2pl-strict-2pl--rigorous-2pl)
- [Chapter 5: Crash Recovery & Storage Architecture: WAL & ARIES](#chapter-5-crash-recovery--storage-architecture-wal--aries)
  - [5.1 Buffer Management: Steal/No-Steal and Force/No-Force](#51-buffer-management-stealno-steal-and-forceno-force)
  - [5.2 Write-Ahead Logging (WAL) Protocol](#52-write-ahead-logging-wal-protocol)
  - [5.3 The ARIES Recovery Algorithm (Analysis, Redo, Undo)](#53-the-aries-recovery-algorithm-analysis-redo-undo)
- [Chapter 6: Database Storage, File Organization & B+ Tree Indexing](#chapter-6-database-storage-file-organization--b-tree-indexing)
  - [6.1 Clustered vs Non-Clustered Indices](#61-clustered-vs-non-clustered-indices)
  - [6.2 B-Trees vs B+ Trees Architecture](#62-b-trees-vs-b-trees-architecture)
  - [6.3 B+ Tree Node Capacity, Height & Search Complexity](#63-b-tree-node-capacity-height--search-complexity)
- [Chapter 7: Solved DBMS Placement Problems & Interview Assessment Drills](#chapter-7-solved-dbms-placement-problems--interview-assessment-drills)
  - [Solved Problem 1: Candidate Key & BCNF Decomposition Proof](#solved-problem-1-candidate-key--bcnf-decomposition-proof)
  - [Solved Problem 2: Precedence Graph Serializability Analysis](#solved-problem-2-precedence-graph-serializability-analysis)
  - [Solved Problem 3: B+ Tree Fanout & Maximum Records Numerical](#solved-problem-3-b-tree-fanout--maximum-records-numerical)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: DBMS Architecture, Relational Model & ER Modeling

### 1.1 3-Schema Architecture & Data Independence
The ANSI/SPARC 3-Schema Architecture separates user views from internal physical storage:

```
[ External Level ]  -> View 1 (Student View)  View 2 (Faculty View)  View 3 (Finance View)
      |
      |   (Logical Data Independence)
      v
[ Conceptual Level ] -> Global Relational Schema (Tables, Foreign Keys, Constraints)
      |
      |   (Physical Data Independence)
      v
[ Internal Level ]   -> Storage structures (B+ trees, page layouts, hashing, file paths)
```

1. **Logical Data Independence:** The capacity to modify the conceptual schema (adding columns, splitting tables) without having to alter existing external schemas or rewrite user application queries.
2. **Physical Data Independence:** The capacity to alter internal storage structures (adding B+ tree indexes, migrating from HDD to SSD, changing block sizes) without requiring changes to the conceptual or external schema.

### 1.2 Entity-Relationship (ER) Modeling Principles
- **Entity:** An identifiable real-world object (e.g., `Student`, `Course`).
- **Weak Entity:** An entity that cannot be uniquely identified by its own attributes alone and possesses no primary key. It depends on an **Identifying Owner Entity** via an **Identifying Relationship**. Its distinguishing attribute is a **Partial Key / Discriminator** (denoted with a dashed underline in Chen notation).
- **Cardinality Ratios:** $1:1$ (One-to-One), $1:N$ (One-to-Many), $M:N$ (Many-to-Many).
- **Participation Constraints:**
  - **Total Participation (Double Line):** Every entity instance must participate in the relationship (e.g., every `Employee` MUST belong to a `Department`).
  - **Partial Participation (Single Line):** Some entity instances may not participate.

### 1.3 Mapping ER Diagrams to Relational Schemas
1. **Strong Entity Set:** Map directly to a table with all simple attributes. Choose candidate key as Primary Key.
2. **Weak Entity Set:** Create table containing all simple attributes of weak entity + Primary Key of Identifying Owner Entity as Foreign Key. Composite Primary Key = (Owner PK + Partial Discriminator).
3. **1:N Relationship:** Place the Primary Key of the "1" side as a Foreign Key in the table representing the "N" side.
4. **M:N Relationship:** Mandatory creation of a separate **Cross-Reference / Associative Table** containing Foreign Keys referencing both participating entity tables. Primary Key is composite of both foreign keys.
5. **Multivalued Attributes:** Create a new table containing the attribute value + Primary Key of parent entity. Composite PK = (Parent PK + Attribute Value).

### 1.4 Relational Integrity Constraints
- **Domain Constraint:** Values in a column must strictly adhere to the declared data type and nullability definition.
- **Entity Integrity Constraint:** No primary key column value may be `NULL`.
- **Referential Integrity Constraint:** A Foreign Key value in table $R_1$ referencing table $R_2$ must either match an existing Primary Key value in $R_2$ or be `NULL`.
  - Cascading Actions: `ON DELETE CASCADE` (deletes dependent child rows), `ON DELETE SET NULL` (nullifies foreign key column), `ON DELETE RESTRICT / NO ACTION` (rejects parent deletion if child references exist).

---

## Chapter 2: Relational Algebra, Tuple Calculus & Query Processing

### 2.1 Fundamental & Derived Relational Algebra Operators
Relational algebra is a procedural query language consisting of operations that take one or two relations as input and produce a new relation as output:

1. **Selection ($\sigma_C(R)$):** Filters rows satisfying predicate $C$. Unary, commutative: $\sigma_{C_1}(\sigma_{C_2}(R)) = \sigma_{C_2}(\sigma_{C_1}(R))$.
2. **Projection ($\pi_{A_1, \dots, A_k}(R)$):** Selects specified columns and removes duplicate rows (relational sets).
3. **Cartesian Product ($R \times S$):** Combines every tuple of $R$ ($n_1$ rows, $m_1$ cols) with every tuple of $S$ ($n_2$ rows, $m_2$ cols), producing $n_1 \times n_2$ rows and $m_1 + m_2$ columns.
4. **Set Union ($R \cup S$), Intersection ($R \cap S$), Difference ($R - S$):** Require relations to be **Union Compatible** (identical number of attributes with corresponding compatible domains).
5. **Natural Join ($R \bowtie S$):** Performs equality match on all common attribute names and projects out duplicate columns:
   $$R \bowtie S = \pi_{\text{Distinct Attrs}}(\sigma_{R.A = S.A}(R \times S))$$
6. **Theta Join ($R \bowtie_\theta S$):** Cartesian product followed by selection condition $\theta$: $\sigma_\theta(R \times S)$.

### 2.2 The Relational Division Operator for Universal Quantification
The division operator ($R \div S$) is used for queries involving the phrase **"for all"** or **"every"**:
- Let $R$ have attributes $(A, B)$ and $S$ have attribute $(B)$.
- $R \div S$ returns all values of $A$ from $R$ that are associated with **every** value of $B$ in $S$.

$$\text{Definition: } R \div S = \pi_A(R) - \pi_A((\pi_A(R) \times S) - R)$$

*Interview Example:* Find students who have taken all courses offered in the Computer Science department:
$$\pi_{\text{StudentID, CourseID}}(\text{Takes}) \div \pi_{\text{CourseID}}(\sigma_{\text{Dept} = 'CS'}(\text{Courses}))$$

---

## Chapter 3: Functional Dependencies, Normalization & Decomposition (1NF to BCNF)

### 3.1 Functional Dependencies & Armstrong's Axioms
A functional dependency $X \to Y$ holds on relation $R$ if for every pair of tuples $t_1, t_2 \in R$, whenever $t_1[X] = t_2[X]$, then $t_1[Y] = t_2[Y]$.

**Armstrong's Axioms (Sound and Complete):**
1. **Reflexivity Rule:** If $Y \subseteq X$, then $X \to Y$. (Trivial dependency)
2. **Augmentation Rule:** If $X \to Y$, then $XZ \to YZ$ for any attribute set $Z$.
3. **Transitivity Rule:** If $X \to Y$ and $Y \to Z$, then $X \to Z$.

**Derived Secondary Rules:**
- **Union:** If $X \to Y$ and $X \to Z$, then $X \to YZ$.
- **Decomposition:** If $X \to YZ$, then $X \to Y$ and $X \to Z$.
- **Pseudo-Transitivity:** If $X \to Y$ and $WY \to Z$, then $WX \to Z$.

### 3.2 Candidate Key Determination via Attribute Closure
**Attribute Closure ($X^+$):** The complete set of all attributes functionally determined by $X$ under a set of FDs $F$.

**Algorithm to Compute $X^+$:**
1. Initialize $\text{closure} = X$.
2. Repeat until no more attributes can be added:
   - For each FD $Y \to Z \in F$:
     - If $Y \subseteq \text{closure}$, then $\text{closure} = \text{closure} \cup Z$.
3. Return $\text{closure}$.

**Candidate Key Test:** $X$ is a **Candidate Key** of relation $R$ if:
1. $X^+ = R$ (Superkey property: determines all attributes in the relation).
2. For no proper subset $Y \subset X$ does $Y^+ = R$ (Minimality property).

### 3.3 Normal Forms Hierarchy: 1NF, 2NF, 3NF & BCNF

```
+---------------------------------------------------------------+
| BCNF: For every non-trivial X -> Y, X must be a Superkey       |
|   +-------------------------------------------------------+   |
|   | 3NF: For every X -> Y, X is Superkey OR Y is Prime    |   |
|   |   +-----------------------------------------------+   |   |
|   |   | 2NF: No non-prime attribute partially depends |   |   |
|   |   |      on any candidate key                     |   |   |
|   |   |   +---------------------------------------+   |   |   |
|   |   |   | 1NF: All attribute values are atomic   |   |   |   |
|   |   |   +---------------------------------------+   |   |   |
|   |   +-----------------------------------------------+   |   |
|   +-------------------------------------------------------+   |
+---------------------------------------------------------------+
```

- **First Normal Form (1NF):** Every column contains strictly atomic (indivisible) values. No repeating groups or nested arrays.
- **Second Normal Form (2NF):** Must be in 1NF, and **NO non-prime attribute is partially dependent on any candidate key**. (A partial dependency occurs when a proper subset of a composite candidate key determines a non-prime attribute).
- **Third Normal Form (3NF):** Must be in 2NF, and for every non-trivial functional dependency $X \to Y$:
  - Either $X$ is a **Superkey**, OR
  - $Y$ is a **Prime Attribute** (a member of any candidate key).
  *(Eliminates transitive dependencies between non-prime attributes).*
- **Boyce-Codd Normal Form (BCNF):** Must be in 3NF, and for every non-trivial functional dependency $X \to Y$:
  - **$X$ MUST be a Superkey.** (No exceptions for prime attributes on the RHS).

### 3.4 Lossless Join & Dependency Preservation Proofs
When decomposing relation $R$ into $R_1$ and $R_2$:

1. **Lossless Join Condition:** The decomposition is lossless if and only if the common attributes form a superkey of at least one of the decomposed relations:
   $$(R_1 \cap R_2) \to R_1 \quad \text{OR} \quad (R_1 \cap R_2) \to R_2$$
2. **Dependency Preservation Condition:** The decomposition preserves dependencies if the union of FDs enforceable on each sub-relation directly recovers the entire original closure: $(F_1 \cup F_2)^+ = F^+$.
   - **Crucial Placement Fact:** Any relation schema can always be decomposed into **3NF** satisfying both **Lossless Join** AND **Dependency Preservation**. Decomposing into **BCNF** guarantees **Lossless Join**, but cannot always preserve functional dependencies.

---

## Chapter 4: Transaction Management, ACID Properties & Concurrency Control

### 4.1 ACID Properties Deep Dive
- **Atomicity:** All-or-nothing execution. Guaranteed by the DBMS recovery manager via Write-Ahead Logging (WAL) and Undo rollback operations.
- **Consistency:** Transactions must transition the database from one valid state satisfying all schema integrity constraints to another valid state.
- **Isolation:** Execution of concurrent transactions produces the same state as if they were executed serially. Controlled by the concurrency control manager (locking, MVCC).
- **Durability:** Once a transaction commits, its updates persist permanently on non-volatile disk storage even in the event of an immediate catastrophic power failure. Guaranteed by Redo logging.

### 4.2 Concurrency Anomalies & SQL Isolation Levels
| SQL Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Mechanism Employed |
|:---|:---:|:---:|:---:|:---|
| **Read Uncommitted** | Possible | Possible | Possible | Transactions read uncommitted dirty buffer pages without locks. |
| **Read Committed** | **Prevented** | Possible | Possible | Short-term Shared read locks released immediately after statement execution; exclusive locks held until commit. (PostgreSQL / Oracle default). |
| **Repeatable Read** | **Prevented** | **Prevented** | Possible | Shared read locks held until end of transaction; prevent in-place record updates. (MySQL InnoDB default). |
| **Serializable** | **Prevented** | **Prevented** | **Prevented** | Strict two-phase locking with predicate/range locks or SSI (Serializable Snapshot Isolation). |

### 4.3 Conflict Serializability & Precedence Graphs
Two operations $O_1 \in T_1$ and $O_2 \in T_2$ are in **conflict** if:
1. They belong to different transactions ($T_1 \ne T_2$).
2. They operate on the same data item $Q$.
3. At least one of the operations is a **Write** ($W(Q)$).
*(Conflicts: Read-Write, Write-Read, Write-Write).*

**Precedence Graph (Serialization Graph) Algorithm:**
1. Create a node for each committed transaction $T_i$.
2. Draw a directed edge $T_i \to T_j$ if an operation in $T_i$ conflicts with an operation in $T_j$, and $T_i$ executed the operation before $T_j$.
3. **Serializability Theorem:** A schedule $S$ is **Conflict Serializable** if and only if its precedence graph contains **NO directed cycles**.
4. The equivalent serial schedule order is obtained by performing a **Topological Sort** on the acyclic graph.

### 4.4 Locking Protocols: 2PL, Strict 2PL & Rigorous 2PL
- **Two-Phase Locking (2PL):**
  - **Growing Phase:** Transaction may acquire locks, but cannot release any lock.
  - **Lock Point:** Moment when the transaction has acquired all necessary locks.
  - **Shrinking Phase:** Transaction may release locks, but cannot acquire any new lock.
  - *Guarantees Conflict Serializability, but susceptible to Cascading Rollbacks and Deadlocks.*
- **Strict 2PL:** All **Exclusive (Write) locks** acquired by a transaction must be held until the transaction explicitly Commits or Aborts. *(Prevents Cascading Aborts).*
- **Rigorous 2PL:** All **Exclusive (Write) and Shared (Read) locks** must be held until transaction termination. *(Guarantees Strictness and easy recovery).*

---

## Chapter 5: Crash Recovery & Storage Architecture: WAL & ARIES

### 5.1 Buffer Management: Steal/No-Steal and Force/No-Force
- **Steal Policy:** The buffer manager can flush dirty pages modified by an active uncommitted transaction to disk to free RAM frames. *(Requires Undo logging to rollback on crash).*
- **No-Force Policy:** The buffer manager does not force dirty committed pages to disk at commit time. *(Requires Redo logging to reapply committed writes on crash).*
- **Industry Standard:** Enterprise DBMS (PostgreSQL, MySQL, Oracle) utilize **Steal / No-Force** because it maximizes disk I/O throughput by avoiding synchronous random disk writes at transaction commit.

### 5.2 Write-Ahead Logging (WAL) Protocol
The WAL protocol mandates two fundamental rules before writing data to disk:
1. **Rule 1 (Undo Rule):** Before a dirty database frame is written from memory to disk (Steal), the log records associated with the update must be flushed to stable disk storage.
2. **Rule 2 (Redo Rule):** Before a transaction is acknowledged as committed (No-Force), all of its log records (including the `COMMIT` record) must be flushed to stable disk storage.

### 5.3 The ARIES Recovery Algorithm (Analysis, Redo, Undo)
Developed by C. Mohan at IBM, ARIES recovers from crashes in 3 distinct sequential passes over the transaction log:

1. **Analysis Pass:** Scans forward from the last checkpoint to the end of the log:
   - Reconstructs the **Dirty Page Table (DPT)** and the active **Transaction Table (TT)**.
   - Identifies all "Loser" transactions that were active when the system crashed.
2. **Redo Pass (Repeating History):** Scans forward from the smallest `RecLSN` in the DPT to the end of the log:
   - Re-executes the actions of ALL transactions (both committed and uncommitted) to restore the database buffer pool to the exact state at the instant of crash.
3. **Undo Pass:** Scans backward from the end of the log:
   - Rolls back the operations of all "Loser" transactions in reverse chronological order.
   - Writes **Compensation Log Records (CLRs)** for each undone operation to prevent cascading undo in case of crashes during the recovery process itself.

---

## Chapter 6: Database Storage, File Organization & B+ Tree Indexing

### 6.1 Clustered vs Non-Clustered Indices
| Architectural Metric | Clustered Index (Primary Index) | Non-Clustered Index (Secondary Index) |
|:---|:---|:---|
| **Data Row Organization** | The physical order of data rows on disk strictly matches the index key order. | The physical order of data rows on disk is independent of index order. |
| **Indices Allowed Per Table** | Strictly **1** clustered index per table (since data can only be physically sorted one way). | Multiple secondary indexes allowed per table (typically up to 64 or 128). |
| **Leaf Node Content** | Leaf nodes ARE the actual data records (or data pages containing full rows). | Leaf nodes store the index key value + a pointer (RID or Primary Key) to the row. |
| **Range Scan Performance** | Ultra-fast sequential I/O; rows on adjacent pages are contiguous on disk. | Slower; requires random disk lookups for each pointer unless covering index is used. |

### 6.2 B-Trees vs B+ Trees Architecture
- **B-Tree:** Data pointers (pointers to actual table rows) are stored in internal nodes as well as leaf nodes.
  - *Drawback:* Internal nodes have low fan-out because large data pointers occupy node space, leading to deeper trees and higher disk I/O.
- **B+ Tree:**
  - **Internal Nodes:** Store strictly search keys and child node page pointers. High fan-out ($B \approx 100 \text{ to } 500$), resulting in shallow tree heights of only 3 or 4 levels.
  - **Leaf Nodes:** Store all actual data records (or RIDs) along with search keys.
  - **Linked Leaves:** Leaf nodes are chained together in a **Doubly-Linked List**, enabling blazing-fast $O(k)$ range scan queries (`WHERE salary BETWEEN 50000 AND 80000`).

### 6.3 B+ Tree Node Capacity, Height & Search Complexity
Let $B$ be the order (fan-out) of a B+ tree node, $P$ be disk block size, $K$ be key size, and $p_t$ be pointer size:
$$B \times p_t + (B - 1) \times K \le P \implies B \le \frac{P + K}{p_t + K}$$

- **Search Time Complexity:** Point query takes $O(\log_B N)$ disk block reads.
- **Tree Height:** $h \le \lceil \log_{\lceil B / 2 \rceil} (N) \rceil + 1$. For a fanout $B = 200$, a 3-level B+ tree can index:
  $$N \approx 200^3 = 8,000,000 \text{ records with at most 3 disk I/O operations!}$$

---

## Chapter 7: Solved DBMS Placement Problems & Interview Assessment Drills

### Solved Problem 1: Candidate Key & BCNF Decomposition Proof
- **Problem:** Relation $R(A, B, C, D, E)$ with functional dependencies:
  $$F = \{ A \to BC, \ CD \to E, \ B \to D, \ E \to A \}$$
  1. Find all candidate keys of $R$.
  2. Determine the highest normal form of $R$.
  3. If not in BCNF, decompose $R$ into BCNF relations losslessly.
- **Solution:**
  1. **Candidate Key Determination:**
     - Check attribute occurrences: $A$ is on LHS, $B$ on RHS, $C$ on RHS, $D$ on RHS, $E$ on RHS. Neither $C$ nor $D$ appears alone on LHS.
     - Compute $A^+$:
       - Start with $\{A\}$.
       - $A \to BC \implies \{A, B, C\}$.
       - $B \to D \implies \{A, B, C, D\}$.
       - $CD \to E \implies \{A, B, C, D, E\} = R$.
       - Hence, **$A$ is a candidate key**.
     - Since $E \to A$, compute $E^+$:
       - $\{E\} \to \{E, A\} \to \{E, A, B, C, D\} = R$.
       - Hence, **$E$ is a candidate key**.
     - Check if $CD$ or $BC$ can derive $A$:
       - $(CD)^+ = \{C, D, E, A, B\} = R$. But does a subset work? $C^+ = \{C\}$, $D^+ = \{D\}$. So **$CD$ is a candidate key**.
       - Since $B \to D$, $(BC)^+ = (BCD)^+ = \{B, C, D, E, A\} = R$. Can a subset work? $B^+ = \{B, D\}$, $C^+ = \{C\}$. Neither is a superkey. So **$BC$ is a candidate key**.
     - Candidate Keys: **$\{A\}, \{E\}, \{CD\}, \{BC\}$**.
     - Prime Attributes: $\{A, B, C, D, E\}$ (All attributes are prime!).
  2. **Highest Normal Form:**
     - Is it in 1NF? Yes (atomic attributes).
     - Is it in 2NF? Check for partial dependencies:
       - $CD$ is a candidate key. $D$ is non-prime? No, all attributes are prime. In 2NF, partial dependency is defined strictly as a proper subset of a key determining a *non-prime* attribute. Since all attributes are prime, no non-prime attribute exists $\implies$ **2NF holds**.
     - Is it in 3NF?
       - For $X \to Y$, either $X$ is superkey or $Y$ is prime.
       - Since every attribute is prime, the condition "$Y$ is prime" holds vacuously for all FDs in $F$!
       - Therefore, $R$ is in **3NF**.
     - Is it in BCNF?
       - Check FD $B \to D$: Is $B$ a superkey? $B^+ = \{B, D\} \ne R$. $B$ is NOT a superkey.
       - Therefore, $R$ violates BCNF.
       - **Highest Normal Form is 3NF.**
  3. **Lossless BCNF Decomposition:**
     - Decompose along violating FD $B \to D$:
       - $R_1(B, D)$ with FD $\{B \to D\}$. Candidate key is $B$. In BCNF.
       - $R_2(R - \{D\} \cup \{B\}) = R_2(A, B, C, E)$ with FDs $\{A \to BC, E \to A\}$. Candidate keys $\{A\}, \{E\}, \{BC\}$. In BCNF.
     - Lossless check: $R_1 \cap R_2 = \{B\}$. In $R_1$, $B^+ = \{B, D\} = R_1$. Common attribute is a superkey of $R_1 \implies$ **Lossless Join guaranteed**.

### Solved Problem 2: Precedence Graph Serializability Analysis
- **Problem:** Analyze the following schedule $S$ for conflict serializability:
  $$S: R_1(X); \ R_2(X); \ W_1(X); \ R_1(Y); \ W_2(X); \ W_1(Y); \ C_1; \ C_2$$
- **Solution:**
  1. Identify conflicting operations between $T_1$ and $T_2$:
     - $R_2(X)$ occurs before $W_1(X) \implies$ Directed edge: $T_2 \to T_1$.
     - $W_1(X)$ occurs before $W_2(X) \implies$ Directed edge: $T_1 \to T_2$.
  2. Graph Analysis:
     - The precedence graph contains directed edges $T_2 \to T_1$ and $T_1 \to T_2$, forming a directed cycle:
       $$T_1 \rightleftarrows T_2$$
  3. Conclusion: The schedule $S$ is **NOT Conflict Serializable** and will cause race condition inconsistencies.

### Solved Problem 3: B+ Tree Fanout & Maximum Records Numerical
- **Problem:** A database system has disk block size $P = 4096\text{ bytes}$. The search key is $K = 16\text{ bytes}$, and a block pointer is $p = 8\text{ bytes}$.
  1. Calculate the maximum order (fan-out) $B$ of an internal node.
  2. If the leaf nodes have capacity for 30 record entries, calculate the maximum number of records indexed by a 3-level B+ tree (root at level 1, internal nodes at level 2, leaf nodes at level 3).
- **Solution:**
  1. Internal node equation:
     $$B \cdot p + (B - 1) \cdot K \le P$$
     $$B(8) + (B - 1)(16) \le 4096 \implies 8B + 16B - 16 \le 4096 \implies 24B \le 4112 \implies B \le 171.33$$
     - Maximum internal node order (fan-out) is $\mathbf{B = 171}$.
  2. Capacity for 3-level B+ tree:
     - Level 1 (Root): 1 node with up to $B = 171$ child pointers.
     - Level 2 (Internal): Up to 171 nodes, each having up to 171 leaf pointers $\implies 171 \times 171 = 29,241$ leaf nodes.
     - Level 3 (Leaf): Each leaf node stores 30 records.
     - Maximum Records $= 29,241 \times 30 = \mathbf{877,230\text{ records}}$.

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Relational Algebra):** Given relations $\text{Employee}(\text{EmpId}, \text{Name}, \text{DeptId})$ and $\text{Department}(\text{DeptId}, \text{DeptName})$, write a relational algebra expression to retrieve the names of employees working in the 'Research' department.
   - *Solution:* $\pi_{\text{Name}}(\sigma_{\text{DeptName} = 'Research'}(\text{Employee} \bowtie \text{Department}))$.

2. **Exercise 2 (Decomposition Test):** Relation $R(A, B, C)$ with $FD = \{A \to B\}$ is decomposed into $R_1(A, B)$ and $R_2(B, C)$. Is the decomposition lossless?
   - *Solution:* $R_1 \cap R_2 = \{B\}$. For lossless join, $B$ must determine $R_1$ ($B \to A$) or $R_2$ ($B \to C$). Since $B^+ = \{B\}$, $B$ is neither a superkey of $R_1$ nor $R_2$. Therefore, the decomposition is **Lossy**.

3. **Exercise 3 (Strict 2PL vs 2PL):** Why does Strict 2PL prevent cascading rollbacks while basic 2PL does not?
   - *Solution:* In basic 2PL, a transaction can release an exclusive write lock in its shrinking phase before committing. Another transaction can read that updated uncommitted data. If the first transaction subsequently aborts, the second transaction must also be rolled back (cascading abort). In Strict 2PL, all exclusive locks are retained until commit/abort, guaranteeing that uncommitted data is never exposed.

4. **Exercise 4 (ARIES CLR Log Records):** What is the purpose of Compensation Log Records (CLRs) written during the Undo phase of the ARIES recovery algorithm?
   - *Solution:* CLRs record the reversal of an aborted transaction's update. Each CLR contains an `UndoNextLSN` pointer pointing to the next log record to be undone. If the system crashes during the recovery undo phase itself, ARIES uses the CLR and `UndoNextLSN` to resume undo without repeating already undone operations, preventing infinite recovery loops.

5. **Exercise 5 (Cardinality of Cross Product):** Relation $R$ has 1,000 tuples and relation $S$ has 2,000 tuples. What are the minimum and maximum possible number of tuples in $R \bowtie S$ (natural join on common attribute $A$)?
   - *Solution:* Minimum tuples $= 0$ (if no values of $A$ match between $R$ and $S$). Maximum tuples $= 1,000 \times 2,000 = \mathbf{2,000,000}$ (if all tuples in both relations have the exact same value for attribute $A$).
"""

DBMS_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 3,
        "chapter_title": "Functional Dependencies, Normalization & Decomposition (1NF to BCNF)",
        "subtopic": "BCNF Definition",
        "question": "Which condition must hold for every non-trivial functional dependency X -> Y in a relational schema to be strictly in Boyce-Codd Normal Form (BCNF)?",
        "options": [
            "X must be a Superkey",
            "Y must be a Prime Attribute",
            "X must be a proper subset of a candidate key",
            "Y must contain no composite domains"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [DBMS Prescribed Textbook — Chapter 3: Normalization]\nA relation is in BCNF if for every non-trivial FD X -> Y, the left-hand side X is strictly a Superkey. 3NF allows Y to be a prime attribute, but BCNF removes that exception.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 4,
        "chapter_title": "Transaction Management, ACID Properties & Concurrency Control",
        "subtopic": "Conflict Serializability",
        "question": "Under the Precedence Graph (Serialization Graph) testing method, when is a concurrent schedule guaranteed to be conflict serializable?",
        "options": [
            "If and only if the precedence graph contains no directed cycles",
            "If all transactions execute 2-phase commit",
            "If all read operations precede write operations",
            "If the total number of transactions is fewer than the available CPU cores"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [DBMS Prescribed Textbook — Chapter 4: Concurrency Control]\nA schedule is conflict serializable if and only if its precedence graph contains no directed cycles. An acyclic precedence graph allows topological sorting to find an equivalent serial order.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 6,
        "chapter_title": "Database Storage, File Organization & B+ Tree Indexing",
        "subtopic": "B+ Tree Leaf Node Structure",
        "question": "Why do B+ Trees provide superior performance for SQL range scan queries compared to standard B-Trees?",
        "options": [
            "All leaf nodes in a B+ Tree are linked together in a doubly-linked list, allowing sequential traversal without traversing the tree root repeatedly",
            "B+ Trees store data records only in the root node",
            "B+ Trees use hash buckets instead of sorted pointers",
            "B+ Trees eliminate all disk block read operations"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [DBMS Prescribed Textbook — Chapter 6: B+ Tree Indexing]\nIn a B+ Tree, leaf nodes contain all keys and data pointers and are linked in a continuous doubly-linked list. A range query (e.g. BETWEEN A AND B) locates the starting leaf in O(log N) and then traverses sequentially through the leaf list.",
        "difficulty": "easy",
    }
]
