"""
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
