"""
Generates unabridged master textbooks for:
- Data Engineering & Distributed Systems (data_eng_master.py)
- Artificial Intelligence & Machine Learning (ai_ml_master.py)
"""
import os
import ast

TEXTBOOK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "app", "services", "textbooks"))

# =============================================================================
# DATA ENGINEERING & DISTRIBUTED SYSTEMS
# =============================================================================
DATA_ENG_CODE = r'''"""
data_eng_master.py — Prescribed Master Textbook for Data Engineering & Big Data Systems.
Comprehensive unabridged campus placement textbook covering CAP theorem, HDFS,
Apache Spark internals (Catalyst, Tungsten, RDDs, wide vs narrow dependencies),
columnar storage (Parquet, Iceberg, Delta Lake), Apache Kafka (partitions, ISR, EOS),
dimensional modeling (Star, Snowflake, SCD Type 1/2), and solved placement architecture drills.
"""

DATA_ENG_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Distributed Systems Foundations, CAP Theorem & Storage Architectures",
        "topics": [
            "CAP Theorem: Consistency, Availability, Partition Tolerance trade-offs",
            "PACELC Theorem: Consistency vs Latency trade-offs in normal operating conditions",
            "Distributed Consensus mechanisms: Raft vs Paxos leader election and log replication",
            "Hadoop Distributed File System (HDFS): NameNode (active/standby), DataNodes, 128MB block sizing",
            "Rack awareness, block replication topology (default factor 3), and Heartbeat / Block Reports"
        ],
        "key_takeaways": "Network partitions are inevitable in real-world distributed infrastructure; systems must choose between Consistency (CP) and Availability (AP). HDFS uses 128MB blocks to minimize NameNode metadata memory footprint."
    },
    {
        "chapter_num": 2,
        "title": "Distributed Processing: MapReduce & Apache Spark Architecture",
        "topics": [
            "The MapReduce paradigm: Map, Shuffle & Sort, Reduce lifecycle and disk I/O bottlenecks",
            "Apache Spark architecture: Driver Program, Cluster Manager (YARN/K8s), Executors, Cores",
            "Resilient Distributed Datasets (RDDs): Lineage DAGs, immutability, lazy evaluation",
            "Narrow dependencies (map, filter) vs Wide dependencies (groupByKey, join, shuffle operations)",
            "Spark Optimization Engines: Catalyst query optimizer (logical/physical plans) and Project Tungsten (off-heap memory, code generation)"
        ],
        "key_takeaways": "Narrow transformations do not require network shuffles and execute within local partitions; wide transformations require full data shuffling across cluster nodes, dominating network latency."
    },
    {
        "chapter_num": 3,
        "title": "Columnar Storage Formats & Modern Data Lakehouses",
        "topics": [
            "Row-oriented (CSV, JSON, Avro) vs Columnar (Apache Parquet, ORC) storage paradigms",
            "Parquet file internals: File metadata, Row Groups, Column Chunks, Pages, Dictionary Encoding, and RLE",
            "Data Lakehouse architecture: Adding ACID transactions and schema enforcement to cloud object storage (S3/GCS)",
            "Modern table formats: Apache Iceberg, Delta Lake, and Apache Hudi",
            "Time-travel queries, partition evolution, and Copy-on-Write (CoW) vs Merge-on-Read (MoR)"
        ],
        "key_takeaways": "Columnar formats drastically reduce analytical query I/O through column pruning (reading only queried columns) and predicate pushdown (skipping entire row groups using min/max page statistics)."
    },
    {
        "chapter_num": 4,
        "title": "Real-Time Event Streaming & Message Brokers: Apache Kafka",
        "topics": [
            "Kafka architectural primitives: Producers, Brokers, Consumers, Topics, Partitions, Offsets",
            "Partitioning strategies: Round-robin vs Key-based hashing (Murmur2) and partition ordering guarantee",
            "Replication and fault tolerance: In-Sync Replicas (ISR) and 'acks=all' configuration",
            "Consumer Groups, Partition Rebalancing (Eager vs Cooperative Sticky), and Consumer Offsets (__consumer_offsets)",
            "Delivery semantics: At-least-once, At-most-once, and Exactly-Once Semantics (EOS) via Idempotent Producers & Two-Phase Commit"
        ],
        "key_takeaways": "Kafka guarantees strict total ordering strictly within a single partition, never across different partitions of a topic. Exactly-once processing requires idempotent producer keys combined with transactional offset commits."
    },
    {
        "chapter_num": 5,
        "title": "Data Warehousing, Dimensional Modeling & ETL/ELT Pipelines",
        "topics": [
            "Ralph Kimball Dimensional Modeling: Fact tables (additive, semi-additive, non-additive) vs Dimension tables",
            "Schema design: Star Schema (denormalized, high query performance) vs Snowflake Schema (normalized dimensions)",
            "Slowly Changing Dimensions (SCD): SCD Type 0 (fixed), SCD Type 1 (overwrite), SCD Type 2 (historical tracking with valid_from/valid_to/is_current), SCD Type 3 (previous column)",
            "ETL (Extract-Transform-Load) vs ELT (Extract-Load-Transform in modern cloud warehouses: Snowflake, BigQuery, Databricks)",
            "Modern data transformation frameworks: dbt (data build tool) testing, documentation, and DAG orchestration"
        ],
        "key_takeaways": "SCD Type 2 is the gold standard for tracking audit history in analytical data warehouses by inserting a new record with active date ranges whenever dimensional attributes change."
    },
    {
        "chapter_num": 6,
        "title": "Solved Data Engineering Placement Problems & Architecture Drills",
        "topics": [
            "End-to-end real-time ingestion pipeline design for 50,000 events/second",
            "SCD Type 2 SQL merge script implementation and validation",
            "Kafka partition count calculation based on producer throughput and consumer processing latency",
            "Spark data skew troubleshooting (Salting technique) and broadcast join optimization",
            "Self-assessment practice drills with verified solutions"
        ],
        "key_takeaways": "Mastering Kafka capacity planning, Spark broadcast joins, and SCD Type 2 implementations provides the foundation for data engineering interviews at Netflix, Uber, Amazon, and Walmart Labs."
    }
]

DATA_ENG_TEXTBOOK_MARKDOWN = r"""# Data Engineering & Distributed Systems: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Data Engineering & Distributed Systems  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, data engineering technical interviews, and distributed systems coding evaluations (Amazon, Uber, Microsoft, Databricks, Snowflake, Walmart Labs) are strictly grounded in the distributed theorems, storage engines, streaming protocols, and modeling practices detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Distributed Systems Foundations, CAP Theorem & Storage Architectures](#chapter-1-distributed-systems-foundations-cap-theorem--storage-architectures)
  - [1.1 The CAP Theorem & PACELC Trade-Offs](#11-the-cap-theorem--pacelc-trade-offs)
  - [1.2 Distributed Consensus: Raft vs Paxos](#12-distributed-consensus-raft-vs-paxos)
  - [1.3 Hadoop Distributed File System (HDFS) Architecture](#13-hadoop-distributed-file-system-hdfs-architecture)
  - [1.4 Rack Awareness & Block Replication Topologies](#14-rack-awareness--block-replication-topologies)
- [Chapter 2: Distributed Processing: MapReduce & Apache Spark Architecture](#chapter-2-distributed-processing-mapreduce--apache-spark-architecture)
  - [2.1 From MapReduce to In-Memory Spark](#21-from-mapreduce-to-in-memory-spark)
  - [2.2 Spark Cluster Architecture & Execution Lifecycle](#22-spark-cluster-architecture--execution-lifecycle)
  - [2.3 RDDs, Lineage Graphs & Dependency Taxonomy](#23-rdds-lineage-graphs--dependency-taxonomy)
  - [2.4 Catalyst Optimizer & Project Tungsten](#24-catalyst-optimizer--project-tungsten)
- [Chapter 3: Columnar Storage Formats & Modern Data Lakehouses](#chapter-3-columnar-storage-formats--modern-data-lakehouses)
  - [3.1 Row-Oriented vs Columnar Storage Paradigms](#31-row-oriented-vs-columnar-storage-paradigms)
  - [3.2 Apache Parquet File Anatomy & Encoding Techniques](#32-apache-parquet-file-anatomy--encoding-techniques)
  - [3.3 The Data Lakehouse: Delta Lake, Apache Iceberg & Hudi](#33-the-data-lakehouse-delta-lake-apache-iceberg--hudi)
- [Chapter 4: Real-Time Event Streaming & Message Brokers: Apache Kafka](#chapter-4-real-time-event-streaming--message-brokers-apache-kafka)
  - [4.1 Kafka Core Architecture: Topics, Partitions & Offsets](#41-kafka-core-architecture-topics-partitions--offsets)
  - [4.2 Producer Partitioning, Replication & In-Sync Replicas (ISR)](#42-producer-partitioning-replication--in-sync-replicas-isr)
  - [4.3 Consumer Groups & Rebalance Protocols](#43-consumer-groups--rebalance-protocols)
  - [4.4 Achieving Exactly-Once Semantics (EOS)](#44-achieving-exactly-once-semantics-eos)
- [Chapter 5: Data Warehousing, Dimensional Modeling & ETL/ELT Pipelines](#chapter-5-data-warehousing-dimensional-modeling--etlelt-pipelines)
  - [5.1 Kimball Dimensional Modeling: Facts vs Dimensions](#51-kimball-dimensional-modeling-facts-vs-dimensions)
  - [5.2 Star Schema vs Snowflake Schema](#52-star-schema-vs-snowflake-schema)
  - [5.3 Slowly Changing Dimensions (SCD Types 1, 2, 3)](#53-slowly-changing-dimensions-scd-types-1-2-3)
  - [5.4 Modern ELT with dbt (data build tool)](#54-modern-elt-with-dbt-data-build-tool)
- [Chapter 6: Solved Data Engineering Placement Problems & Architecture Drills](#chapter-6-solved-data-engineering-placement-problems--architecture-drills)
  - [Solved Problem 1: End-to-End Real-Time Ingestion Architecture](#solved-problem-1-end-to-end-real-time-ingestion-architecture)
  - [Solved Problem 2: SCD Type 2 Implementation SQL Walkthrough](#solved-problem-2-scd-type-2-implementation-sql-walkthrough)
  - [Solved Problem 3: Spark Data Skew Resolution via Key Salting](#solved-problem-3-spark-data-skew-resolution-via-key-salting)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: Distributed Systems Foundations, CAP Theorem & Storage Architectures

### 1.1 The CAP Theorem & PACELC Trade-Offs
Formulated by Eric Brewer and formally proven by Gilbert and Lynch, the **CAP Theorem** states that in an asynchronous network subject to partitions, a distributed data store can guarantee at most two out of three properties:

```
                  [ Consistency (C) ]
                         /\
                        /  \
                       /    \
                      /  CA  \   (Only possible in theoretical 
                     /        \   zero-partition local networks)
                    /          \
   [ Partition     /------------\ [ Availability (A) ]
     Tolerance (P) ]     CP   AP
```

- **Consistency (Linearizability):** Every read receives the most recent write or an error.
- **Availability:** Every non-failing node returns a non-error response for every request (without guaranteeing it contains the most recent write).
- **Partition Tolerance:** The system continues to operate despite an arbitrary number of messages being dropped or delayed by the network between nodes.
- **Real-World Reality:** Network cables get cut, routers reboot, and cloud switches experience latency spikes; **Partition Tolerance ($P$) is non-negotiable** in distributed physical systems. Therefore, architectures must choose between:
  - **CP Systems (Consistency over Availability):** E.g., Apache HBase, Google Spanner, ZooKeeper, etcd. If a network partition occurs, un-synchronized nodes reject requests to preserve strict data correctness.
  - **AP Systems (Availability over Consistency):** E.g., Apache Cassandra, Amazon DynamoDB, Couchbase. Nodes accept reads and writes during partitions, guaranteeing high availability and resolving conflicts eventually (**Eventual Consistency**).

**The PACELC Theorem Extension (Daniel Abadi):**
If there is a **P**artition ($P$), trade off **A**vailability ($A$) vs **C**onsistency ($C$); **E**lse ($E$), trade off **L**atency ($L$) vs **C**onsistency ($C$). (E.g., MongoDB is $PC/EC$; Cassandra is $PA/EL$).

### 1.2 Distributed Consensus: Raft vs Paxos
Distributed systems coordinate state via consensus algorithms:
- **Paxos (Leslie Lamport):** Mathematically rigorous but notoriously difficult to implement in production software.
- **Raft (Ongaro & Ousterhout):** Designed specifically for understandability, dividing consensus into 3 independent subproblems:
  1. **Leader Election:** Heartbeat timers. If a follower detects no heartbeat within a randomized election timeout (150-300ms), it transitions to candidate, increments term, and requests votes. Needs majority vote ($N/2 + 1$).
  2. **Log Replication:** Leader accepts client writes, appends entry to local log, and broadcasts `AppendEntries` RPC to followers. Entry is committed once replicated to a majority of nodes.
  3. **Safety Guarantee:** A candidate can only be elected leader if its log contains all committed entries from all previous terms (Election Restriction).

### 1.3 Hadoop Distributed File System (HDFS) Architecture
HDFS provides scalable, fault-tolerant distributed storage on commodity hardware using a master-worker topology:

```
[ Active NameNode ] <--- Metadata: Inode tree, block locations in RAM
       |  (EditLog / FsImage checkpoints)
[ Standby NameNode ]
       |
  +----+------------------------+------------------------+
  |                             |                        |
  v                             v                        v
[ DataNode 1 ]            [ DataNode 2 ]           [ DataNode 3 ]
(Local Disk: Block A, B)  (Local Disk: Block B, C) (Local Disk: Block A, C)
```

- **NameNode (Master):** Stores the entire file system namespace (directories, files, block mappings) entirely in **RAM** for microsecond lookup performance. Changes are persisted to an append-only `EditLog` on disk and merged periodically into the `FsImage` checkpoint file by the Standby NameNode.
- **DataNodes (Workers):** Store raw data blocks as regular files on local Linux ext4/xfs disks. DataNodes send Heartbeats every 3 seconds and periodic Block Reports to the NameNode.
- **128 MB Block Size Rationale:** Standard operating system disk blocks are 4 KB. HDFS defaults to 128 MB (or 256 MB) to minimize disk seek time ($T_{\text{seek}} \approx 10\text{ms}$ vs transfer time) and prevent the NameNode's RAM from exhausting its capacity (each block metadata entry consumes ~150 bytes in NameNode RAM).

### 1.4 Rack Awareness & Block Replication Topologies
To maximize fault tolerance while minimizing cross-switch network bandwidth, HDFS enforces the **Rack Awareness Replication Policy** for default replication factor 3:
1. **Replica 1:** Placed on a local DataNode in the same rack as the client writer.
2. **Replica 2:** Placed on a DataNode in a **different remote rack** (protects data against catastrophic top-of-rack switch or power failure).
3. **Replica 3:** Placed on a **different DataNode within the same remote rack** as Replica 2 (minimizes cross-rack switch saturation during read operations).

---

## Chapter 2: Distributed Processing: MapReduce & Apache Spark Architecture

### 2.1 From MapReduce to In-Memory Spark
Hadoop MapReduce revolutionized big data processing but suffered severe performance bottlenecks: every intermediate computation had to be serialized and written out to physical HDFS disks and re-read over the network across stages.

**Apache Spark** solved this by keeping intermediate datasets in **RAM** across iterative computation cycles, delivering up to **100x faster execution**:

```
MapReduce: [HDFS Read] -> [Map] -> [Disk Spill] -> [Shuffle/Sort] -> [Reduce] -> [HDFS Write]
                                   ^------------- High Disk I/O -------------^

Spark:     [Memory/Disk Read] -> [Transformation 1] -> [Transformation 2] -> [Action (Result)]
                                 ^------- In-Memory RDD Pipeline -------^
```

### 2.2 Spark Cluster Architecture & Execution Lifecycle
- **Driver Program:** Runs the user's `main()` function, instantiates `SparkSession`, converts user code into a Directed Acyclic Graph (DAG) of execution, schedules tasks, and coordinates with cluster managers.
- **Cluster Manager:** Allocates compute resources across the cluster (Apache YARN, Kubernetes, Apache Mesos, or Spark Standalone).
- **Executors:** Worker processes running on cluster nodes. Each executor runs multiple concurrent tasks in separate CPU thread slots and caches RDD partitions in local memory or disk storage.

### 2.3 RDDs, Lineage Graphs & Dependency Taxonomy
**Resilient Distributed Datasets (RDDs)** are immutable, lazily-evaluated distributed collections of records partitioned across cluster nodes.

```
                  Narrow Dependency (No Shuffle)
[ Partition 0 ] -------------------------------> [ Partition 0 ]
[ Partition 1 ] -------------------------------> [ Partition 1 ]
(e.g., map(), filter(), flatMap(), mapPartitions())

                  Wide Dependency (Mandatory Shuffle)
[ Partition 0 ] -------\   /-------------------> [ Partition 0 ]
                        \ /
                         X
                        / \
[ Partition 1 ] -------/   \-------------------> [ Partition 1 ]
(e.g., groupByKey(), reduceByKey(), join(), distinct())
```

- **Narrow Dependencies:** Each partition of the parent RDD is consumed by at most one partition of the child RDD. Operations execute entirely in local memory across pipeline stages with zero network transfers.
- **Wide Dependencies (Shuffle Dependencies):** Multiple child partitions depend on data from multiple parent partitions. Requires a cluster-wide **Shuffle** operation: partitioning data by hash, writing spill files to disk, and transferring partitions over the network.
- **Lazy Evaluation & Lineage:** Transformations (`map`, `filter`) do not execute immediately; they simply register an entry in the RDD **Lineage DAG**. Execution is triggered ONLY when an **Action** (`count()`, `collect()`, `saveAsTextFile()`, `take()`) is called. If a node fails, Spark reconstructs the lost partitions by replaying the lineage graph from the source.

### 2.4 Catalyst Optimizer & Project Tungsten
Modern Spark SQL and DataFrames run on top of two core performance engines:
1. **Catalyst Optimizer:**
   - Translates relational SQL queries into an Abstract Syntax Tree.
   - Applies rule-based optimizations: **Predicate Pushdown** (pushing filters down to storage layers before scanning) and **Projection Pruning** (dropping unreferenced columns).
   - Cost-Based Optimizer (CBO) evaluates table statistics to select optimal physical execution plans (e.g., choosing Broadcast Hash Join over Sort-Merge Join).
2. **Project Tungsten:**
   - Bypasses JVM garbage collection overhead by managing memory off-heap in compact raw binary format (**Unsafe Row**).
   - Generates whole-stage bytecode at runtime (**Whole-Stage Code Generation**) to keep variables inside CPU registers.

---

## Chapter 3: Columnar Storage Formats & Modern Data Lakehouses

### 3.1 Row-Oriented vs Columnar Storage Paradigms
- **Row-Oriented Formats (CSV, JSON, Apache Avro):**
  - Consecutive fields of a record are stored sequentially on disk: `[ID1, Name1, Age1, Salary1][ID2, Name2, Age2, Salary2]`.
  - *Best for:* OLTP transactional workloads where entire records are read or written together.
  - *Disadvantage for Analytics:* To calculate the average salary of 1 billion rows, the system must read all IDs, Names, and Ages off disk, wasting 90% of I/O throughput.
- **Columnar Formats (Apache Parquet, Apache ORC):**
  - Values of the same column are stored contiguously on disk: `[Salary1, Salary2, Salary3...][Age1, Age2, Age3...]`.
  - *Best for:* OLAP analytical queries (`SELECT AVG(salary) FROM employees`). The query engine reads ONLY the salary column bytes off disk (**Column Pruning**).

### 3.2 Apache Parquet File Anatomy & Encoding Techniques
A Parquet file is structured into self-contained segments:

```
+-----------------------------------------------------------+
| Header: "PAR1" magic bytes                                |
+-----------------------------------------------------------+
| Row Group 1 (typically 128 MB to 512 MB of rows)          |
|   - Column Chunk: User_ID   [Page 1][Page 2]              |
|   - Column Chunk: Timestamp [Page 1][Page 2]              |
|   - Column Chunk: Amount    [Page 1][Page 2] (Min/Max stat|
+-----------------------------------------------------------+
| Row Group 2 ...                                           |
+-----------------------------------------------------------+
| Footer: File Metadata, Schema, Row Group offsets & stats  |
+-----------------------------------------------------------+
```

**Advanced Encoding Mechanisms:**
1. **Dictionary Encoding:** Replaces repetitive strings (e.g., country codes `"USA"`, `"IND"`) with small integer keys (0, 1) in a local dictionary table.
2. **Run-Length Encoding (RLE):** Compresses consecutive identical values: `USA, USA, USA, USA` is stored as `(4, "USA")`.
3. **Predicate Pushdown:** The Parquet footer stores `min_value` and `max_value` statistics for every column chunk in each row group. If a query requests `WHERE amount > 1000`, and Row Group 1 has `max_value = 450`, Spark skips reading Row Group 1 entirely without reading a single data byte!

### 3.3 The Data Lakehouse: Delta Lake, Apache Iceberg & Hudi
Traditional Data Lakes on cloud object storage (AWS S3, Google Cloud Storage) lacked transaction support, leading to dirty reads, failed partial writes, and inability to update records.

**The Open Table Format Revolution (Iceberg, Delta Lake, Hudi):**
- Adds an **ACID Transaction Log** on top of Parquet files.
- **Time Travel:** Query historic snapshots of data (`SELECT * FROM sales TIMESTAMP AS OF '2026-01-01'`).
- **Schema Evolution:** Add, rename, or reorder columns without rewriting petabytes of existing files.
- **Partition Evolution (Iceberg):** Change partitioning granularity (e.g., by day to by hour) without invalidating historical data layouts.

---

## Chapter 4: Real-Time Event Streaming & Message Brokers: Apache Kafka

### 4.1 Kafka Core Architecture: Topics, Partitions & Offsets
Apache Kafka is a distributed, append-only commit log designed for high-throughput, low-latency pub-sub event streaming:

```
Topic: 'user-clicks'
  Partition 0: [Offset 0][Offset 1][Offset 2][Offset 3]... -> Leader: Broker 1
  Partition 1: [Offset 0][Offset 1][Offset 2]...          -> Leader: Broker 2
  Partition 2: [Offset 0][Offset 1][Offset 2][Offset 3]... -> Leader: Broker 3
```

- **Topic:** Logical category or feed name to which records are published.
- **Partition:** The unit of parallelism and scalability in Kafka. Each partition is an ordered, immutable sequence of records continuously appended to a structured commit log.
- **Offset:** A sequential 64-bit integer assigned monotonically to each record within a partition.
- **Ordering Guarantee:** Kafka guarantees total strict order ONLY within a single partition. There is **no global ordering guarantee** across different partitions of the same topic.

### 4.2 Producer Partitioning, Replication & In-Sync Replicas (ISR)
- **Producer Partitioning Strategies:**
  - **Explicit Partition:** Record specifies target partition number directly.
  - **Key-Based Hashing:** Record contains a non-null key. Kafka hashes the key using Murmur2:
    $$\text{Partition} = \text{Murmur2}(\text{Key}) \bmod \text{Total Partitions}$$
    All messages with the same key (e.g., `user_id = "USR-4421"`) are guaranteed to land on the exact same partition in strict chronological order.
  - **Round-Robin / Sticky Partitioner:** Used when message key is null to balance load evenly across brokers.
- **Replication & In-Sync Replicas (ISR):**
  - Each partition has 1 **Leader** broker and $N - 1$ **Follower** brokers.
  - Followers actively replicate messages from the Leader. Followers that keep up with the Leader's log are members of the **ISR (In-Sync Replicas)** set.
  - **Durability Guarantee (`acks` setting):**
    - `acks=0`: Fire-and-forget. Maximum throughput, high data loss risk.
    - `acks=1`: Leader writes to local log and immediately acknowledges. If leader dies before follower replicates, data is lost.
    - `acks=all` (or `-1`): Leader waits for acknowledgment from all replicas in the ISR set before confirming success. Guarantees zero data loss when paired with `min.insync.replicas=2`.

### 4.3 Consumer Groups & Rebalance Protocols
- **Consumer Group:** A set of consumers cooperating to consume data from a topic.
- **Partition Assignment Rule:** Each partition is assigned to strictly **one consumer** within a consumer group at any given time.
  - If a topic has 4 partitions, and the consumer group has 4 consumers, each consumer reads 1 partition.
  - If the group has 6 consumers for 4 partitions, 2 consumers sit idle as hot standbys.
  - **Rule:** To maximize parallelism, the number of consumer instances should equal the number of partitions!
- **Consumer Rebalance:** When a consumer crashes or joins, the group coordinator reassigns partitions across active members. Modern Kafka utilizes **Cooperative Sticky Rebalance** to avoid stopping all consumers during rebalancing.

### 4.4 Achieving Exactly-Once Semantics (EOS)
Standard Kafka streaming provides **At-Least-Once** delivery (duplicate records on network retries) or **At-Most-Once** delivery (lost messages on pre-emptive offset commits).

**Enabling End-to-End Exactly-Once Processing:**
1. **Idempotent Producer (`enable.idempotence=true`):** Producer assigns a unique Producer ID (`PID`) and monotonically increasing sequence number to every message. The broker detects and discards duplicate sequence numbers caused by network retries.
2. **Transactional API:** Coordinates atomic writes across multiple output topics and consumer offset commits using a two-phase commit protocol managed by the Transaction Coordinator.

---

## Chapter 5: Data Warehousing, Dimensional Modeling & ETL/ELT Pipelines

### 5.1 Kimball Dimensional Modeling: Facts vs Dimensions
Developed by Ralph Kimball, dimensional modeling optimizes databases for fast analytical querying:

- **Fact Tables:** Contain numerical quantitative measurements, metrics, and facts resulting from a business process (e.g., `SalesFact`: revenue, units_sold, discount_amount, foreign keys).
  - *Additive Facts:* Can be meaningfully summed across all dimensions (e.g., `Total Revenue`).
  - *Semi-Additive Facts:* Can be summed across some dimensions but not time (e.g., `Account Balance` at end of month).
  - *Non-Additive Facts:* Cannot be summed across dimensions (e.g., `Unit Price`, profit margins, ratios).
- **Dimension Tables:** Contain qualitative context describing who, what, where, and when (e.g., `DimCustomer`, `DimProduct`, `DimDate`). Dimensions contain descriptive text attributes used for filtering and slicing (`WHERE customer_region = 'West'`).

### 5.2 Star Schema vs Snowflake Schema
```
Star Schema (Denormalized)              Snowflake Schema (Normalized)

     [ DimDate ]                             [ DimDate ]
         \                                       \
          \                                       \
[ DimStore ]--[ FactSales ]--[ DimCustomer ]   [ DimStore ]--[ FactSales ]--[ DimCustomer ]
          /                                                   /                   |
         /                                                   /              [ DimCity ]
   [ DimProduct ]                                      [ DimProduct ]             |
                                                             |              [ DimCountry ]
                                                       [ DimCategory ]
```

| Metric | Star Schema | Snowflake Schema |
|:---|:---|:---|
| **Normalization Level** | Denormalized (Dimensions contain redundant descriptive data). | Normalized (Dimensions split into hierarchical sub-tables: Category, Subcategory). |
| **Query Complexity** | Simple queries with minimal table `JOIN` operations. | Complex queries requiring multiple relational `JOIN` operations across hierarchies. |
| **Storage Footprint** | Slightly higher storage redundancy. | Minimal storage redundancy. |
| **Query Performance** | Blazing-fast in modern columnar data warehouses (Snowflake, BigQuery). | Slower query execution due to expensive multi-table joins. |

### 5.3 Slowly Changing Dimensions (SCD Types 1, 2, 3)
How an analytical warehouse handles updates to descriptive dimensional attributes (e.g., customer changes residential address):

1. **SCD Type 1 (Overwrite):**
   - Directly overwrites the existing attribute with the new value.
   - *Advantage:* Simple to implement; zero table storage growth.
   - *Disadvantage:* **Destroys historical context**. Previous sales are retroactively attributed to the new location.
2. **SCD Type 2 (Historical Tracking via New Row):**
   - Keeps the existing row unchanged and inserts a **new row** with a new surrogate primary key.
   - Adds audit tracking columns: `start_date`, `end_date`, and `is_current` (boolean flag).
   - *Advantage:* **Preserves complete, pristine historical accuracy** for all past reporting.
3. **SCD Type 3 (Previous Value Column):**
   - Keeps the same row and adds a new column: `previous_city` alongside `current_city`.
   - Tracks only the immediate last historical state; cannot track multiple historical revisions.

---

## Chapter 6: Solved Data Engineering Placement Problems & Architecture Drills

### Solved Problem 1: End-to-End Real-Time Ingestion Architecture
- **Problem Statement (Amazon / Uber Placement):** Design an end-to-end data platform to ingest 50,000 real-time payment transactions per second, perform fraud anomaly detection within 2 seconds, and store records for historical analytics with sub-second dashboard query performance.
- **Architectural Solution & Blueprint:**
  ```
  [ Mobile App / Gateway ]
             |
             v  (50,000 JSON events/sec)
  [ Apache Kafka Cluster ] (Topic: payments, Partitions: 60, acks=all)
        /           \
       /             \
      v               v
  [ Flink / Spark ]   [ Kafka Connect / S3 Ingestion ]
  Streaming Engine            |
  - Window: 2s tumbling       v
  - Fraud rule scoring   [ Cloud Object Storage (S3 / GCS) ]
  - Emits alerts to SMS       |
  (Latency < 500ms)           v
                         [ Apache Iceberg / Delta Lake ]
                         - Formatted as Snappy-compressed Parquet
                         - Partitioned by day and hour
                              |
                              v
                         [ Snowflake / ClickHouse Engine ]
                         - Powers real-time executive BI dashboards
  ```
  - **Kafka Partition Sizing:** 50,000 events/sec $\times$ 1 KB/event $= 50\text{ MB/sec}$. A single consumer thread safely processes $1\text{ MB/sec}$. Minimum partitions $= 50 / 1 = 50$ partitions. We allocate **60 partitions** for headroom.

### Solved Problem 2: SCD Type 2 Implementation SQL Walkthrough
- **Problem:** Write an idempotent SQL merge statement to implement SCD Type 2 on a target dimension table `dim_customer` using an incoming staging table `stage_customer`.
- **Solution:**
  ```sql
  -- Step 1: Expire previous active records where incoming data has changed
  UPDATE dim_customer
  SET 
      end_date = CURRENT_TIMESTAMP(),
      is_current = FALSE
  WHERE customer_id IN (
      SELECT s.customer_id
      FROM stage_customer s
      JOIN dim_customer d ON s.customer_id = d.customer_id
      WHERE d.is_current = TRUE 
        AND (s.address != d.address OR s.tier != d.tier)
  ) AND is_current = TRUE;

  -- Step 2: Insert new rows for both brand-new customers and updated records
  INSERT INTO dim_customer (customer_id, name, address, tier, start_date, end_date, is_current)
  SELECT 
      s.customer_id,
      s.name,
      s.address,
      s.tier,
      CURRENT_TIMESTAMP() AS start_date,
      NULL AS end_date,
      TRUE AS is_current
  FROM stage_customer s
  LEFT JOIN dim_customer d 
      ON s.customer_id = d.customer_id AND d.is_current = TRUE
  WHERE d.customer_id IS NULL 
     OR (s.address != d.address OR s.tier != d.tier);
  ```

### Solved Problem 3: Spark Data Skew Resolution via Key Salting
- **Problem:** A PySpark join between `transactions` (1 billion rows) and `merchants` (10,000 rows) stalls at 99% progress because 80% of transactions belong to a single merchant ID (`merchant_id = 9999` — Amazon). How do you resolve this data skew?
- **Solution (Salting Technique):**
  1. The single heavy key causes 80% of data to funnel into a single executor partition, causing Out-Of-Memory (OOM) errors and straggler tasks.
  2. **Add a Salt to the Large Table:** Append a random integer between 0 and $K-1$ (e.g., $K = 20$) to the skewed key:
     `salted_key = concat(merchant_id, '_', floor(rand() * 20))`
  3. **Replicate the Small Table (Explode):** Replicate each row of the small table 20 times, matching every possible salt suffix (from 0 to 19):
     `exploded_key = concat(merchant_id, '_', explode(sequence(0, 19)))`
  4. **Join on Salted Keys:** The join `ON transactions.salted_key = merchants.exploded_key` now distributes the skewed merchant records evenly across 20 separate partitions, restoring linear parallel processing!

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (CAP Classification):** Why is Apache Cassandra classified as an AP system under the CAP theorem?
   - *Solution:* Cassandra uses decentralized peer-to-peer ring topology with masterless replication. When network partitions split nodes, each partition continues accepting write and read requests locally without blocking, trading immediate linearizable consistency for 100% continuous availability.

2. **Exercise 2 (Spark Narrow vs Wide):** Classify the following Spark operations as Narrow or Wide: `filter()`, `reduceByKey()`, `map()`, `join()`.
   - *Solution:* `filter()`: **Narrow**; `reduceByKey()`: **Wide** (triggers shuffle); `map()`: **Narrow**; `join()`: **Wide** (unless one table is small enough for a Broadcast join).

3. **Exercise 3 (Parquet Efficiency):** Why does Parquet provide significantly higher compression ratios than CSV even when using the same gzip compression algorithm?
   - *Solution:* Parquet organizes identical data types contiguously in column chunks (e.g. all 32-bit integers together). Adjacent data values possess high statistical similarity and low entropy, allowing dictionary encoding and run-length encoding to compress data drastically before generic gzip/snappy compression is applied.

4. **Exercise 4 (Kafka Partition Parallelism):** If topic `orders` has 12 partitions, what is the maximum number of consumer processes in a single consumer group that can actively read data in parallel?
   - *Solution:* **12 consumers**. Each partition is assigned to strictly one consumer within a consumer group. Any consumer instances beyond 12 will remain idle.

5. **Exercise 5 (SCD Type 1 Risk):** What business risk is introduced when an enterprise replaces SCD Type 2 with SCD Type 1 in a sales commission tracking mart?
   - *Solution:* Overwriting historical dimensional records (SCD Type 1) recalculates historical historical commissions using the sales representative's current territory rather than the territory they were assigned to when the sale occurred, distorting historical revenue audits.
"""

DATA_ENG_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "Distributed Systems Foundations, CAP Theorem & Storage Architectures",
        "subtopic": "HDFS Block Sizing Rationale",
        "question": "Why does HDFS use a large default block size (128 MB or 256 MB) compared to traditional operating systems (4 KB)?",
        "options": [
            "To minimize disk seek time overhead and reduce the memory footprint required to store metadata on the NameNode",
            "To prevent network switches from overheating",
            "Because physical disks cannot write blocks smaller than 128 MB",
            "To enforce AES-256 encryption on all files"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Data Eng Prescribed Textbook — Chapter 1: Distributed Foundations & HDFS]\nA 128 MB block ensures that the time to transfer data outweighs disk seek latency (~10ms). Crucially, the NameNode holds all filesystem metadata in RAM (~150 bytes per block); large blocks keep the total block count manageable.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 4,
        "chapter_title": "Real-Time Event Streaming & Message Brokers: Apache Kafka",
        "subtopic": "Kafka Message Ordering Guarantee",
        "question": "What is the exact scope of Apache Kafka's message ordering guarantee?",
        "options": [
            "Messages are guaranteed to be in strict total order strictly within a single partition",
            "Messages are guaranteed to be ordered globally across all partitions in a topic",
            "Messages are ordered based on the consumer arrival timestamp",
            "Ordering is strictly random to optimize throughput"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Data Eng Prescribed Textbook — Chapter 4: Apache Kafka]\nKafka guarantees strict monotonically increasing order of messages only within an individual partition. It provides no global ordering across different partitions.",
        "difficulty": "easy",
    }
]
'''

# =============================================================================
# ARTIFICIAL INTELLIGENCE & MACHINE LEARNING
# =============================================================================
AI_ML_CODE = r'''"""
ai_ml_master.py — Prescribed Master Textbook for Artificial Intelligence & Machine Learning.
Comprehensive unabridged campus placement textbook covering supervised/unsupervised learning,
gradient descent mathematics, regression/classification, bias-variance tradeoff,
decision trees, Random Forest, XGBoost, deep learning, backpropagation derivations,
CNNs, Transformers, multi-head attention equations, RAG architectures, and solved placement ML problems.
"""

AI_ML_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Foundations of Machine Learning & Mathematical Fundamentals",
        "topics": [
            "Taxonomy of AI: Supervised, Unsupervised, Semi-supervised, and Reinforcement Learning",
            "Linear Algebra essentials: Vectors, matrix multiplications, eigenvalues & eigenvectors, SVD",
            "Multivariable Calculus: Gradients, partial derivatives, chain rule for tensor operations",
            "Loss functions: Mean Squared Error (MSE), Binary Cross-Entropy (BCE), Categorical Cross-Entropy",
            "Maximum Likelihood Estimation (MLE) and statistical foundations of learning"
        ],
        "key_takeaways": "Machine learning optimizes model parameters by minimizing loss functions using gradient descent. Cross-entropy loss measures the divergence between true label probability distributions and model predicted probabilities."
    },
    {
        "chapter_num": 2,
        "title": "Supervised Learning: Regression, Classification & Optimization",
        "topics": [
            "Linear Regression: Ordinary Least Squares (OLS) normal equation vs iterative Gradient Descent",
            "Gradient Descent variants: Batch GD, Stochastic GD (SGD), Mini-batch GD, and Adam optimizer (momentum + RMSprop)",
            "Logistic Regression: Sigmoid activation function, log-odds (logit), and decision boundary derivation",
            "Regularization techniques: L1 Lasso (sparsity and feature selection) vs L2 Ridge (weight shrinkage) vs ElasticNet",
            "K-Nearest Neighbors (KNN): Distance metrics (Euclidean, Manhattan), curse of dimensionality, k hyperparameter selection"
        ],
        "key_takeaways": "L1 regularization drives coefficients to exactly zero, performing automatic feature selection; L2 regularization shrinks weights smoothly toward zero, preventing collinearity explosions."
    },
    {
        "chapter_num": 3,
        "title": "Model Evaluation, Bias-Variance Tradeoff & Feature Engineering",
        "topics": [
            "The Bias-Variance Decomposition: Underfitting (High Bias) vs Overfitting (High Variance)",
            "Confusion Matrix metrics: Accuracy, Precision, Recall (Sensitivity), F1-Score, Specificity",
            "Receiver Operating Characteristic (ROC) curve and Area Under Curve (AUC-ROC) interpretation",
            "Cross-Validation: K-Fold, Stratified K-Fold (for imbalanced datasets), Leave-One-Out (LOOCV)",
            "Feature Engineering: Standardization (Z-score) vs Min-Max Normalization, One-Hot Encoding vs Target Encoding, handling missing data"
        ],
        "key_takeaways": "In imbalanced domains (e.g. fraud detection), raw accuracy is misleading. Precision measures purity of positive predictions; Recall measures capture rate of actual positives. F1-Score represents their harmonic mean."
    },
    {
        "chapter_num": 4,
        "title": "Tree-Based Algorithms & Ensemble Learning",
        "topics": [
            "Decision Trees: Splitting criteria (Shannon Entropy & Information Gain vs Gini Impurity)",
            "Tree Pruning: Pre-pruning (max_depth, min_samples_split) vs Cost-Complexity Post-Pruning (alpha)",
            "Bagging (Bootstrap Aggregating): Random Forest (feature subsampling, out-of-bag error estimation)",
            "Boosting fundamentals: Sequential error correction on residual errors",
            "Gradient Boosting Machines (GBM), XGBoost (second-order Taylor approximation, tree leaf regularization), and LightGBM"
        ],
        "key_takeaways": "Random Forest builds independent trees in parallel on bootstrapped subsets to reduce variance. Gradient Boosting builds sequential trees to predict the negative gradient (residual) of the loss function to reduce bias."
    },
    {
        "chapter_num": 5,
        "title": "Deep Learning Architectures & The Backpropagation Algorithm",
        "topics": [
            "The Artificial Neuron (Perceptron) and Multi-Layer Perceptrons (MLP)",
            "Activation functions: Sigmoid, Tanh, ReLU, Leaky ReLU, GELU, and Softmax",
            "Mathematical derivation of Backpropagation: Forward pass, loss calculation, backward chain-rule error propagation",
            "Vanishing and Exploding Gradients: Causes, Xavier/He weight initialization, Batch Normalization, Layer Normalization",
            "Convolutional Neural Networks (CNN): Kernels/filters, padding ('valid' vs 'same'), stride, pooling, and spatial hierarchy"
        ],
        "key_takeaways": "ReLU activation eliminates vanishing gradients in the positive domain. Backpropagation computes the partial derivative of the loss function with respect to every weight tensor via the multivariate chain rule."
    },
    {
        "chapter_num": 6,
        "title": "Sequence Models, Transformers, Attention & Modern LLMs",
        "topics": [
            "Recurrent Neural Networks (RNN) and Long Short-Term Memory (LSTM) gating units (Forget, Input, Output gates)",
            "The Transformer Revolution ('Attention Is All You Need'): Architecture breakdown",
            "Self-Attention mechanics: Query (Q), Key (K), and Value (V) projections, Scaled Dot-Product Attention equation",
            "Multi-Head Attention (MHA) and Positional Encodings (sinusoidal & rotary embeddings)",
            "LLM paradigms: Autoregressive Decoders (GPT), Encoders (BERT), and Retrieval-Augmented Generation (RAG) pipelines"
        ],
        "key_takeaways": "Scaled Dot-Product Attention allows every token in a sequence to attend to every other token in parallel in O(1) sequential steps, overcoming RNN sequential execution bottlenecks."
    },
    {
        "chapter_num": 7,
        "title": "Solved AI/ML Placement Interview Problems & Assessment Drills",
        "topics": [
            "Mathematical derivation of Gradient Descent weight update for Linear Regression",
            "Precision, Recall, and F1-Score step-by-step numerical calculation from confusion matrix",
            "Self-Attention dimension computation for Transformer layers",
            "Bias-variance diagnosis scenario walkthrough with regularization remedies",
            "Self-assessment practice drills with verified solutions"
        ],
        "key_takeaways": "Mastering the mathematics of backpropagation, self-attention dimension tracking, and evaluation metrics ensures high placement test scores at Google, Microsoft, Amazon, and NVIDIA."
    }
]

AI_ML_TEXTBOOK_MARKDOWN = r"""# Artificial Intelligence & Machine Learning: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Artificial Intelligence & Machine Learning  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, AI/ML engineering technical interviews, and online test evaluations (Google, Microsoft, Amazon, NVIDIA, Adobe, TCS Digital) are strictly grounded in the loss functions, optimization proofs, neural architectures, and Transformer equations detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Foundations of Machine Learning & Mathematical Fundamentals](#chapter-1-foundations-of-machine-learning--mathematical-fundamentals)
  - [1.1 Taxonomy of Machine Learning Paradigms](#11-taxonomy-of-machine-learning-paradigms)
  - [1.2 Essential Linear Algebra & Multivariable Calculus](#12-essential-linear-algebra--multivariable-calculus)
  - [1.3 Core Loss Functions: MSE vs Cross-Entropy](#13-core-loss-functions-mse-vs-cross-entropy)
- [Chapter 2: Supervised Learning: Regression, Classification & Optimization](#chapter-2-supervised-learning-regression-classification--optimization)
  - [2.1 Linear Regression & The Normal Equation](#21-linear-regression--the-normal-equation)
  - [2.2 Gradient Descent Optimization: Batch, SGD, Mini-Batch & Adam](#22-gradient-descent-optimization-batch-sgd-mini-batch--adam)
  - [2.3 Logistic Regression & The Sigmoid Function](#23-logistic-regression--the-sigmoid-function)
  - [2.4 Regularization: L1 Lasso vs L2 Ridge](#24-regularization-l1-lasso-vs-l2-ridge)
- [Chapter 3: Model Evaluation, Bias-Variance Tradeoff & Feature Engineering](#chapter-3-model-evaluation-bias-variance-tradeoff--feature-engineering)
  - [3.1 The Bias-Variance Decomposition](#31-the-bias-variance-decomposition)
  - [3.2 The Confusion Matrix & Classification Metrics](#32-the-confusion-matrix--classification-metrics)
  - [3.3 ROC Curves & AUC Analysis](#33-roc-curves--auc-analysis)
  - [3.4 Feature Scaling & Encoding Pipelines](#34-feature-scaling--encoding-pipelines)
- [Chapter 4: Tree-Based Algorithms & Ensemble Learning](#chapter-4-tree-based-algorithms--ensemble-learning)
  - [4.1 Decision Tree Splitting: Entropy vs Gini Impurity](#41-decision-tree-splitting-entropy-vs-gini-impurity)
  - [4.2 Bagging & Random Forest Architecture](#42-bagging--random-forest-architecture)
  - [4.3 Boosting: GBM, XGBoost & LightGBM](#43-boosting-gbm-xgboost--lightgbm)
- [Chapter 5: Deep Learning Architectures & The Backpropagation Algorithm](#chapter-5-deep-learning-architectures--the-backpropagation-algorithm)
  - [5.1 Multi-Layer Perceptrons & Activation Functions](#51-multi-layer-perceptrons--activation-functions)
  - [5.2 Complete Mathematical Derivation of Backpropagation](#52-complete-mathematical-derivation-of-backpropagation)
  - [5.3 Vanishing Gradients & Normalization Techniques](#53-vanishing-gradients--normalization-techniques)
  - [5.4 Convolutional Neural Networks (CNNs)](#54-convolutional-neural-networks-cnns)
- [Chapter 6: Sequence Models, Transformers, Attention & Modern LLMs](#chapter-6-sequence-models-transformers-attention--modern-llms)
  - [5.1 From RNNs and LSTMs to Attention](#61-from-rnns-and-lstms-to-attention)
  - [6.2 Scaled Dot-Product Self-Attention Mathematics](#62-scaled-dot-product-self-attention-mathematics)
  - [6.3 Multi-Head Attention & Transformer Architecture](#63-multi-head-attention--transformer-architecture)
  - [6.4 Modern LLM Foundations & Retrieval-Augmented Generation (RAG)](#64-modern-llm-foundations--retrieval-augmented-generation-rag)
- [Chapter 7: Solved AI/ML Placement Interview Problems & Assessment Drills](#chapter-7-solved-aiml-placement-interview-problems--assessment-drills)
  - [Solved Problem 1: Gradient Descent Weight Update Derivation](#solved-problem-1-gradient-descent-weight-update-derivation)
  - [Solved Problem 2: Confusion Matrix & F1-Score Numerical](#solved-problem-2-confusion-matrix--f1-score-numerical)
  - [Solved Problem 3: Self-Attention Tensor Dimension Tracing](#solved-problem-3-self-attention-tensor-dimension-tracing)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: Foundations of Machine Learning & Mathematical Fundamentals

### 1.1 Taxonomy of Machine Learning Paradigms
- **Supervised Learning:** Training data consists of input features $X \in \mathbb{R}^{n \times d}$ paired with ground-truth labels $y \in \mathbb{R}^n$. The algorithm learns a mapping function $f: X \to y$.
  - *Regression:* Target $y$ is continuous (e.g., house price, salary).
  - *Classification:* Target $y$ is categorical (e.g., spam vs non-spam, tumor benign vs malignant).
- **Unsupervised Learning:** Training data consists strictly of features $X$ without labels. The algorithm discovers hidden intrinsic structure, clusters, or lower-dimensional representations.
  - *Clustering:* K-Means, DBSCAN, Hierarchical Clustering.
  - *Dimensionality Reduction:* Principal Component Analysis (PCA), t-SNE, UMAP.
- **Reinforcement Learning:** An **Agent** interacts with an **Environment** through **Actions** $a$, receiving **Rewards** $r$ and transitioning between **States** $s$, guided by the Bellman Equation to maximize cumulative expected discounted return.

### 1.2 Essential Linear Algebra & Multivariable Calculus
- **Matrix Multiplication:** Given $A \in \mathbb{R}^{m \times k}$ and $B \in \mathbb{R}^{k \times n}$, product $C = AB \in \mathbb{R}^{m \times n}$:
  $$C_{ij} = \sum_{p=1}^k A_{ip} B_{pj}$$
- **Eigenvalues and Eigenvectors:** For square matrix $A$:
  $$A v = \lambda v, \quad \det(A - \lambda I) = 0$$
  In PCA, principal component directions correspond strictly to the eigenvectors of the data covariance matrix with the largest eigenvalues.
- **The Gradient Vector ($\nabla f$):** The vector of all first-order partial derivatives pointing in the direction of steepest ascent:
  $$\nabla_\theta J(\theta) = \left[ \frac{\partial J}{\partial \theta_0}, \frac{\partial J}{\partial \theta_1}, \dots, \frac{\partial J}{\partial \theta_d} \right]^T$$

### 1.3 Core Loss Functions: MSE vs Cross-Entropy
- **Mean Squared Error (MSE) — For Regression:**
  $$J(\theta) = \frac{1}{2m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})^2$$
- **Binary Cross-Entropy (BCE) / Log Loss — For Binary Classification:**
  $$J(\theta) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln(\hat{y}^{(i)}) + (1 - y^{(i)}) \ln(1 - \hat{y}^{(i)}) \right]$$
  Where $\hat{y} = \sigma(\theta^T x) \in [0, 1]$.
- **Categorical Cross-Entropy — For Multi-Class ($K$ classes) with Softmax:**
  $$J(\theta) = -\sum_{i=1}^m \sum_{k=1}^K y_k^{(i)} \ln(\hat{y}_k^{(i)}), \quad \hat{y}_k = \frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}}$$

---

## Chapter 2: Supervised Learning: Regression, Classification & Optimization

### 2.1 Linear Regression & The Normal Equation
Model hypothesis:
$$\hat{y} = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d = \theta^T x$$
In matrix form with design matrix $X \in \mathbb{R}^{m \times (d+1)}$:
$$\hat{y} = X\theta$$

**Closed-Form Analytical Solution (The Normal Equation):**
Setting $\nabla_\theta J(\theta) = 0$:
$$\theta = (X^T X)^{-1} X^T y$$
- *Computational Complexity:* Matrix inversion $(X^T X)^{-1}$ takes $O(d^3)$ time. For $d > 10,000$ features, the normal equation becomes prohibitively slow, necessitating iterative Gradient Descent.

### 2.2 Gradient Descent Optimization: Batch, SGD, Mini-Batch & Adam
General parameter update rule:
$$\theta := \theta - \alpha \nabla_\theta J(\theta)$$
Where $\alpha$ is the learning rate.

| Optimization Algorithm | Samples per Gradient Step | Convergence Behavior | Computational Efficiency |
|:---|:---|:---|:---|
| **Batch Gradient Descent** | All $m$ samples in dataset | Smooth, deterministic trajectory toward global minimum. | Slow for massive datasets; requires entire dataset in RAM. |
| **Stochastic GD (SGD)** | Exactly $1$ random sample | Highly oscillatory/noisy; can escape local minima. | Fast updates, but oscillations can prevent settling at exact minimum. |
| **Mini-Batch GD** | Batch size $B$ (e.g., 32, 64, 128) | Balanced stability with vectorized GPU matrix execution. | **Industry standard** for training modern neural networks. |
| **Adam Optimizer** | Mini-batch with adaptive learning rates | Computes exponentially decaying moving averages of past gradients (momentum $m_t$) and squared gradients ($v_t$). | Fastest convergence, default optimizer for deep learning. |

### 2.3 Logistic Regression & The Sigmoid Function
Logistic regression maps real-valued linear predictions $z = \theta^T x$ into probabilities $[0, 1]$ via the **Sigmoid (Logistic) Function**:
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

- **Property of Sigmoid Derivative:**
  $$\frac{d\sigma(z)}{dz} = \sigma(z) \cdot (1 - \sigma(z))$$
- **Decision Boundary:** The model predicts positive class $y = 1$ when $\hat{y} \ge 0.5 \iff z = \theta^T x \ge 0$.

### 2.4 Regularization: L1 Lasso vs L2 Ridge
Prevents overfitting by penalizing large model weight magnitudes:

- **L2 Regularization (Ridge Regression):**
  $$J_{\text{Ridge}}(\theta) = \text{MSE} + \lambda \sum_{j=1}^d \theta_j^2$$
  - Weight update: $\theta_j := \theta_j (1 - 2\alpha\lambda) - \alpha \frac{\partial \text{MSE}}{\partial \theta_j}$ (Weight Decay).
  - Shrinks all weights smoothly toward zero; handles multicollinearity effectively.
- **L1 Regularization (Lasso Regression):**
  $$J_{\text{Lasso}}(\theta) = \text{MSE} + \lambda \sum_{j=1}^d |\theta_j|$$
  - The L1 diamond constraint region possesses sharp corners along axes, forcing less informative coefficients to become **identically zero**.
  - Serves as an embedded **Automatic Feature Selection** mechanism.

---

## Chapter 3: Model Evaluation, Bias-Variance Tradeoff & Feature Engineering

### 3.1 The Bias-Variance Decomposition
Expected test error decomposes into three fundamental components:
$$\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}[\hat{f}(x)]^2 + \text{Var}[\hat{f}(x)] + \sigma^2 \text{ (Irreducible Error)}$$

```
Error ^
      |           Total Error
      |         \             /
      |          \    *      /
      |  Variance \  / \    /  Variance (Overfitting)
      |            \/   \  /
      |  Bias       \    \/
      |  (Underfitting)   \  Bias
      +------------------------------------> Model Complexity
```

- **High Bias (Underfitting):** Model is overly simplistic and makes strong incorrect assumptions (e.g., fitting a linear model to a cubic dataset). High error on both training and test sets.
  - *Remedy:* Increase model capacity, add polynomial features, reduce regularization $\lambda$.
- **High Variance (Overfitting):** Model memorizes random noise in the training set (e.g., deep unpruned decision tree). Low training error but high test error.
  - *Remedy:* Add more training data, apply L1/L2 regularization, feature selection, prune tree depth, use bagging ensemble.

### 3.2 The Confusion Matrix & Classification Metrics
Given binary ground truth ($P, N$) and predictions:

```
                  Predicted Positive   Predicted Negative
Actual Positive: [ True Positive (TP)  | False Negative (FN) - Type II Error ]
Actual Negative: [ False Positive (FP) | True Negative (TN)  - Type I Error  ]
```

1. **Accuracy:** $\frac{TP + TN}{TP + TN + FP + FN}$ (Misleading in imbalanced classes!).
2. **Precision:** $\frac{TP}{TP + FP}$ — "Out of all instances the model predicted positive, how many were actually positive?" (Crucial when False Positives are expensive, e.g. spam filters).
3. **Recall (Sensitivity):** $\frac{TP}{TP + FN}$ — "Out of all actual positive instances, how many did the model capture?" (Crucial when False Negatives are fatal, e.g. cancer diagnosis, fraud detection).
4. **F1-Score:** The harmonic mean of Precision and Recall:
   $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2TP}{2TP + FP + FN}$$

### 3.3 ROC Curves & AUC Analysis
- **Receiver Operating Characteristic (ROC) Curve:** Plots **True Positive Rate** (Recall, Y-axis) against **False Positive Rate** ($FPR = \frac{FP}{FP + TN}$, X-axis) across all possible classification probability thresholds ($0.0 \to 1.0$).
- **Area Under Curve (AUC-ROC):**
  - $\text{AUC} = 1.0$: Perfect classifier.
  - $\text{AUC} = 0.5$: Random guess (diagonal line).
  - Represents the probability that the classifier ranks a randomly chosen positive instance higher than a randomly chosen negative instance.

---

## Chapter 4: Tree-Based Algorithms & Ensemble Learning

### 4.1 Decision Tree Splitting: Entropy vs Gini Impurity
- **Shannon Entropy ($H(S)$):** Measures information disorder:
  $$H(S) = -\sum_{i=1}^C p_i \log_2(p_i)$$
  - For binary split with equal classes ($p = 0.5$): $H(S) = - (0.5 \log_2 0.5 + 0.5 \log_2 0.5) = 1.0\text{ bit}$ (maximum uncertainty).
  - For pure node ($p = 1.0$): $H(S) = 0\text{ bits}$.
- **Information Gain ($IG$):**
  $$IG(S, A) = H(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v)$$
- **Gini Impurity ($G$):** Computationally faster because it avoids logarithm calculations:
  $$G(S) = 1 - \sum_{i=1}^C p_i^2$$

### 4.2 Bagging & Random Forest Architecture
- **Bagging (Bootstrap Aggregating):** Trains $B$ independent base learners in parallel on distinct bootstrap samples (sampling $m$ instances with replacement). Final prediction is obtained via majority voting (classification) or averaging (regression).
- **Random Forest:** Enhances bagging by introducing **Random Feature Subspace Sampling**:
  - At every candidate split in every tree, the algorithm considers strictly a random subset of $k$ features:
    $$k = \sqrt{d} \text{ for classification}, \quad k = \frac{d}{3} \text{ for regression}$$
  - **Decorrelation Effect:** Prevents dominant features from appearing at the root of every tree, decorrelating the trees and drastically reducing ensemble variance!

### 4.3 Boosting: GBM, XGBoost & LightGBM
Unlike bagging, **Boosting** trains trees sequentially, where each new tree is trained to correct the residual errors made by the previous ensemble:

```
[ Input X ] -> [ Tree 1 ] -> Calculates Residuals e1 = y - y_hat1
                     |
                     v
               [ Tree 2 ] -> Fits on Residuals e1 -> Calculates Residuals e2
                     |
                     v
               [ Tree 3 ] -> Fits on Residuals e2 ...
```

- **XGBoost (Extreme Gradient Boosting):**
  - Approximates the loss function using a **Second-Order Taylor Series Expansion** (computing both first derivative / gradient $g_i$ and second derivative / hessian $h_i$).
  - Incorporates explicit regularization parameters ($\gamma$ penalty per tree leaf, $\lambda$ L2 regularization on leaf weights) directly into the objective function.
  - Employs exact and quantile sketch greedy split-finding algorithms with built-in handling for sparse matrices and missing values.

---

## Chapter 5: Deep Learning Architectures & The Backpropagation Algorithm

### 5.1 Multi-Layer Perceptrons & Activation Functions
- **Perceptron Equation:** $z = W x + b, \quad a = g(z)$
- **Non-Linear Activation Functions:**
  - **ReLU (Rectified Linear Unit):** $g(z) = \max(0, z)$. Derivative is $1$ if $z > 0$, $0$ if $z \le 0$. Blazing-fast computation; eliminates vanishing gradient in positive domain. (Susceptible to "Dying ReLU" if large gradients push activations into permanently negative territory).
  - **Leaky ReLU:** $g(z) = \max(\alpha z, z)$, with $\alpha = 0.01$. Prevents dying neurons.
  - **GELU (Gaussian Error Linear Unit):** Smooth non-linearity used in modern Transformers (BERT, GPT).

### 5.2 Complete Mathematical Derivation of Backpropagation
Consider an $L$-layer neural network with loss $J$:
Let $z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}$, and $a^{[l]} = g(z^{[l]})$.

By the multivariable chain rule:
$$\frac{\partial J}{\partial W^{[l]}} = \frac{\partial J}{\partial z^{[l]}} \cdot \frac{\partial z^{[l]}}{\partial W^{[l]}} = \delta^{[l]} (a^{[l-1]})^T$$
Where the error vector $\delta^{[l]}$ is defined as:
$$\delta^{[l]} = \frac{\partial J}{\partial z^{[l]}}$$

**Backward Error Recursion:**
1. **For Output Layer $L$ (with Softmax and Cross-Entropy):**
   $$\delta^{[L]} = a^{[L]} - y$$
2. **For Hidden Layer $l$:**
   $$\delta^{[l]} = \left( (W^{[l+1]})^T \delta^{[l+1]} \right) \odot g'(z^{[l]})$$
   Where $\odot$ represents the element-wise Hadamard product.
3. **Weight & Bias Gradient Updates:**
   $$\frac{\partial J}{\partial W^{[l]}} = \frac{1}{m} \delta^{[l]} (a^{[l-1]})^T$$
   $$\frac{\partial J}{\partial b^{[l]}} = \frac{1}{m} \sum_{i=1}^m \delta^{[l](i)}$$

### 5.3 Vanishing Gradients & Normalization Techniques
- **Vanishing Gradients:** When using Sigmoid or Tanh activations, derivatives satisfy $|g'(z)| \le 0.25$. As gradients multiply backward across 50 layers via chain rule, $\prod_{l=1}^{50} (0.25) \approx 0$, freezing weights in the earliest layers.
- **Batch Normalization (Ioffe & Szegedy):** Normalizes activations across the mini-batch dimension to mean 0 and variance 1, followed by learned scale ($\gamma$) and shift ($\beta$) parameters. Reduces internal covariate shift and stabilizes deep network training.

---

## Chapter 6: Sequence Models, Transformers, Attention & Modern LLMs

### 6.1 From RNNs and LSTMs to Attention
- **Recurrent Neural Networks (RNNs):** Process sequences sequentially one token at a time: $h_t = \tanh(W x_t + U h_{t-1} + b)$.
  - *Catastrophic Limitation:* Gradients vanish over sequences longer than ~20 steps; cannot parallelize training because step $t$ strictly requires step $t-1$.
- **LSTMs (Hochreiter & Schmidhuber):** Introduced an explicit **Cell State ($C_t$)** regulated by 3 non-linear gates: Forget Gate ($f_t$), Input Gate ($i_t$), and Output Gate ($o_t$). Improved long-term memory but remained fundamentally sequential.

### 6.2 Scaled Dot-Product Self-Attention Mathematics
Introduced by Vaswani et al. (2017) in *"Attention Is All You Need"*, the self-attention mechanism processes all tokens simultaneously in parallel.

For an input sequence matrix $X \in \mathbb{R}^{n \times d_{\text{model}}}$:
Each token is projected into three distinct vector spaces via learned weight matrices:
$$Q = X W_Q, \quad K = X W_K, \quad V = X W_V$$
Where $W_Q, W_K \in \mathbb{R}^{d_{\text{model}} \times d_k}$, and $W_V \in \mathbb{R}^{d_{\text{model}} \times d_v}$.

**The Scaled Dot-Product Attention Equation:**
$$\text{Attention}(Q, K, V) = \text{Softmax}\left( \frac{Q K^T}{\sqrt{d_k}} \right) V$$

```
Step 1: Compute Raw Similarity Matrix:  S = Q * K^T  (Shape: n x n)
Step 2: Scale by 1 / sqrt(d_k):         Prevents dot products from exploding for large dimensions
                                        (which would cause Softmax gradients to vanish!)
Step 3: Apply Softmax:                  Produces probability weights summing to 1 across rows
Step 4: Multiply by Value Matrix V:     Computes weighted sum of value representations
```

### 6.3 Multi-Head Attention & Transformer Architecture
Instead of computing attention once with large dimension $d_{\text{model}}$, **Multi-Head Attention (MHA)** projects queries, keys, and values $h$ times into distinct lower-dimensional subspaces ($d_k = d_{\text{model}} / h$):

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W_O$$
Where:
$$\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$$

- Allows the model to attend simultaneously to information from different representation subspaces (e.g., one head focuses on grammatical syntax, another on semantic pronoun references, another on temporal markers).

### 6.4 Modern LLM Foundations & Retrieval-Augmented Generation (RAG)
- **Autoregressive Decoder LLMs (GPT-3, GPT-4, Llama 3):** Employ causal masking (lower-triangular mask) to prevent tokens from attending to future tokens, trained on the next-token prediction objective: $\max \sum \log P(w_t \mid w_1, \dots, w_{t-1})$.
- **Retrieval-Augmented Generation (RAG):** Overcomes LLM hallucinations and static training cutoffs by grounding generations in external knowledge:
  1. Chunk external documents (e.g. 500-token chunks with 50-token overlap).
  2. Generate dense vector embeddings using an embedding model (e.g., text-embedding-ada-002, BGE).
  3. Store and index embeddings in a Vector Database (Qdrant, Pinecone, Milvus) using HNSW (Hierarchical Navigable Small World) graphs.
  4. At query time, compute cosine similarity between the user query embedding and document chunks:
     $$\text{Cosine Similarity} = \frac{u \cdot v}{\|u\| \|v\|}$$
  5. Inject the top-$k$ relevant chunks into the LLM system prompt as verified context.

---

## Chapter 7: Solved AI/ML Placement Interview Problems & Assessment Drills

### Solved Problem 1: Gradient Descent Weight Update Derivation
- **Problem:** Derive the exact gradient update formula for single-variable linear regression with Mean Squared Error loss:
  $$J(w, b) = \frac{1}{2m} \sum_{i=1}^m (w x^{(i)} + b - y^{(i)})^2$$
- **Solution:**
  1. Compute partial derivative with respect to weight $w$:
     $$\frac{\partial J}{\partial w} = \frac{1}{2m} \sum_{i=1}^m 2(w x^{(i)} + b - y^{(i)}) \cdot \frac{\partial}{\partial w}(w x^{(i)} + b - y^{(i)})$$
     $$\frac{\partial J}{\partial w} = \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)}) x^{(i)}$$
  2. Compute partial derivative with respect to bias $b$:
     $$\frac{\partial J}{\partial b} = \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})$$
  3. The gradient update rules:
     $$w := w - \frac{\alpha}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)}) x^{(i)}$$
     $$b := b - \frac{\alpha}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})$$

### Solved Problem 2: Confusion Matrix & F1-Score Numerical
- **Problem (TCS Digital / Amazon Placement):** A machine learning model is evaluated on a fraud test set of 1,000 transactions:
  - Total actual fraudulent transactions: 100
  - Total actual legitimate transactions: 900
  - The model correctly flags 80 fraudulent transactions as fraud.
  - The model falsely flags 20 legitimate transactions as fraud.
  Calculate: Accuracy, Precision, Recall, and F1-Score.
- **Solution:**
  1. Construct Confusion Matrix:
     - Actual Positives $= 100 \implies TP = 80, \ FN = 100 - 80 = 20$.
     - Actual Negatives $= 900 \implies FP = 20, \ TN = 900 - 20 = 880$.
  2. Accuracy:
     $$\text{Accuracy} = \frac{TP + TN}{\text{Total}} = \frac{80 + 880}{1000} = \frac{960}{1000} = \mathbf{96.0\%}$$
  3. Precision:
     $$\text{Precision} = \frac{TP}{TP + FP} = \frac{80}{80 + 20} = \frac{80}{100} = \mathbf{0.80 \ (80.0\%)}$$
  4. Recall (Sensitivity):
     $$\text{Recall} = \frac{TP}{TP + FN} = \frac{80}{80 + 20} = \frac{80}{100} = \mathbf{0.80 \ (80.0\%)}$$
  5. F1-Score:
     $$F_1 = 2 \times \frac{0.80 \times 0.80}{0.80 + 0.80} = \frac{1.28}{1.60} = \mathbf{0.80 \ (80.0\%)}$$

### Solved Problem 3: Self-Attention Tensor Dimension Tracing
- **Problem:** In a Transformer layer, sequence length is $n = 512$, and model dimension is $d_{\text{model}} = 768$. Number of attention heads is $h = 12$.
  1. What is the dimension $d_k$ of each individual attention head?
  2. What is the exact tensor shape of $Q, K, V$ before head splitting?
  3. What is the shape of the attention score matrix $Q K^T$ for a single head?
- **Solution:**
  1. Dimension per head:
     $$d_k = \frac{d_{\text{model}}}{h} = \frac{768}{12} = \mathbf{64}$$
  2. Tensor shapes:
     $$X \in \mathbb{R}^{512 \times 768}, \quad W_Q \in \mathbb{R}^{768 \times 768} \implies Q, K, V \in \mathbb{R}^{\mathbf{512 \times 768}}$$
  3. For a single head, $Q_i \in \mathbb{R}^{512 \times 64}$ and $K_i \in \mathbb{R}^{512 \times 64}$:
     $$Q_i K_i^T \in \mathbb{R}^{512 \times 64} \times \mathbb{R}^{64 \times 512} = \mathbb{R}^{\mathbf{512 \times 512}}$$
     *(The attention matrix has size $n \times n = 512 \times 512$, quadratic with sequence length).*

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Scaling Factor in Attention):** Why does the scaled dot-product attention formula divide $Q K^T$ by $\sqrt{d_k}$?
   - *Solution:* For large dimensions $d_k$, the dot products grow large in magnitude, pushing the Softmax function into regions with extremely tiny gradients (near 0 or 1), leading to vanishing gradients during backpropagation. Dividing by $\sqrt{d_k}$ scales the variance of the dot products back to 1.

2. **Exercise 2 (L1 vs L2 Weight Shrinkage):** Why does L1 regularization produce sparse models with zero coefficients while L2 regularization only shrinks coefficients close to zero?
   - *Solution:* The L1 norm penalty contour is an $L_1$ diamond with sharp non-differentiable vertices touching the parameter axes. When the elliptical contours of the MSE loss intersect the constraint boundary, they frequently hit these axis vertices where one or more coordinates are identically zero. The L2 norm constraint is a smooth circle/hypersphere, which almost never intersects the loss ellipse exactly on an axis.

3. **Exercise 3 (Out-of-Bag Error):** What is the theoretical percentage of dataset samples left out of any single bootstrap sample in Random Forest?
   - *Solution:* When sampling $m$ items with replacement, probability of an item NOT being picked in a single draw is $1 - 1/m$. Over $m$ draws: $\lim_{m \to \infty} (1 - 1/m)^m = \frac{1}{e} \approx \mathbf{36.8\%}$. These ~36.8% unpicked samples form the Out-of-Bag (OOB) validation set.

4. **Exercise 4 (ReLU Dead Neurons):** Under what condition does a neuron with a standard ReLU activation become a "Dead ReLU"?
   - *Solution:* If a large gradient causes the neuron's weights to update such that the weighted input $z = Wx + b \le 0$ for all training examples, the activation outputs 0 and the gradient $g'(z) = 0$. Consequently, the neuron never updates again during backpropagation and remains permanently inactive.

5. **Exercise 5 (RAG Cosine Similarity):** If two normalized document embedding vectors have a dot product of $1.0$, what is the geometric angle between them and what does it indicate?
   - *Solution:* Angle $\theta = 0^\circ$ ($\cos 0^\circ = 1.0$). It indicates that the two text passages have identical directional semantic embeddings in vector space.
"""

AI_ML_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 6,
        "chapter_title": "Sequence Models, Transformers, Attention & Modern LLMs",
        "subtopic": "Scaled Dot-Product Attention Equation",
        "question": "In the Transformer Self-Attention mechanism, what is the purpose of dividing the dot product Q * K^T by sqrt(d_k)?",
        "options": [
            "To prevent the dot products from growing excessively large, which would cause Softmax gradients to vanish",
            "To convert the matrix into a lower-triangular causal mask",
            "To reduce the number of parameters in the multi-head projection",
            "To invert the token positions in the sequence"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [AI/ML Prescribed Textbook — Chapter 6: Transformers & Attention]\nAs vector dimension d_k increases, the magnitude of the dot product grows large, pushing the Softmax function into flat regions with near-zero gradients. Scaling by 1/sqrt(d_k) preserves unit variance and healthy gradient flow.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 3,
        "chapter_title": "Model Evaluation, Bias-Variance Tradeoff & Feature Engineering",
        "subtopic": "Classification Metrics in Imbalanced Datasets",
        "question": "Which evaluation metric is the most appropriate when evaluating a credit card fraud detection model where only 0.1% of transactions are fraudulent?",
        "options": [
            "Precision, Recall, and F1-Score (or PR-AUC)",
            "Raw Classification Accuracy",
            "Mean Absolute Percentage Error",
            "Adjusted R-Squared"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [AI/ML Prescribed Textbook — Chapter 3: Model Evaluation]\nIn severely imbalanced datasets, a trivial model predicting 'Legitimate' for every transaction achieves 99.9% accuracy while failing to detect any fraud. Precision, Recall, and the F1-Score are required to measure actual detection efficacy.",
        "difficulty": "easy",
    }
]
'''

with open(os.path.join(TEXTBOOK_DIR, "data_eng_master.py"), "w", encoding="utf-8") as f:
    f.write(DATA_ENG_CODE.strip() + "\n")
ast.parse(DATA_ENG_CODE)
print("data_eng_master.py generated and verified!")

with open(os.path.join(TEXTBOOK_DIR, "ai_ml_master.py"), "w", encoding="utf-8") as f:
    f.write(AI_ML_CODE.strip() + "\n")
ast.parse(AI_ML_CODE)
print("ai_ml_master.py generated and verified!")

