"""
Expands SQL (sql_master.py) and Operating Systems (os_master.py) into unabridged, master textbooks.
"""
import os
import ast

TEXTBOOK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "app", "services", "textbooks"))

# =============================================================================
# SQL & RELATIONAL DATABASES
# =============================================================================
SQL_CODE = r'''"""
sql_master.py — Prescribed Master Textbook for SQL & Relational Database Queries.
Comprehensive unabridged campus placement textbook covering relational theory,
1NF to BCNF normalization, SQL execution order, NULL three-valued logic,
INNER/LEFT/RIGHT/FULL/CROSS/SELF joins, subqueries, correlated subqueries,
Common Table Expressions (CTEs), Recursive CTEs, Window Functions (ROW_NUMBER, RANK,
DENSE_RANK, LEAD, LAG), Indexing (B-Tree, Leftmost Prefix, Clustered), ACID isolation,
and solved LeetCode/HackerRank SQL placement queries.
"""

SQL_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Relational Theory, Schema Design & Normalization",
        "topics": [
            "Relational model fundamentals: Relations, attributes, tuples, domains, and keys",
            "Integrity constraints: Primary Key, Foreign Key (referential integrity), Unique, Not Null, Check",
            "Functional Dependencies and anomaly elimination (Insertion, Deletion, Update anomalies)",
            "Normalization pipeline: 1NF (atomic attributes), 2NF (no partial dependency), 3NF (no transitive dependency), BCNF (superkey LHS)",
            "Denormalization trade-offs: Read optimization vs write amplification and data duplication"
        ],
        "key_takeaways": "A relation is in 3NF if it is in 2NF and for every non-trivial FD X -> Y, either X is a superkey or Y is a prime attribute. Normalization eliminates data redundancy and anomalies."
    },
    {
        "chapter_num": 2,
        "title": "SQL Query Execution Order & Deep Filtering Mechanics",
        "topics": [
            "The 10-Step Query Execution Order: FROM -> ON -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT/OFFSET",
            "WHERE vs HAVING operational boundaries: Pre-aggregation vs post-aggregation filtering",
            "Three-Valued Boolean Logic: TRUE, FALSE, UNKNOWN and handling NULL in expressions",
            "String manipulation and pattern matching: LIKE (wildcards %, _), ILIKE, and regular expressions (REGEXP / ~)",
            "Conditional expressions: CASE WHEN THEN ELSE END syntax and pivot modeling"
        ],
        "key_takeaways": "WHERE filters rows before aggregation; HAVING filters groups after aggregation. Comparing any value to NULL using = yields UNKNOWN, not TRUE or FALSE; always use IS NULL or IS NOT NULL."
    },
    {
        "chapter_num": 3,
        "title": "Mastering SQL Joins & Set Operations",
        "topics": [
            "Join anatomy: INNER JOIN, LEFT OUTER JOIN, RIGHT OUTER JOIN, FULL OUTER JOIN",
            "CROSS JOIN (Cartesian product) and generating combinations",
            "Self-Joins for hierarchical data (Employee-to-Manager reporting chains)",
            "Non-Equi Joins: Joining on range boundaries (salary between min_sal and max_sal)",
            "Set Operations: UNION vs UNION ALL, INTERSECT, EXCEPT / MINUS, and schema compatibility rules"
        ],
        "key_takeaways": "UNION ALL appends result sets without deduplication and runs in O(N); UNION performs an expensive distinct sort/hash operation to eliminate duplicate rows, running in O(N log N)."
    },
    {
        "chapter_num": 4,
        "title": "Subqueries, Correlated Subqueries & CTEs",
        "topics": [
            "Subquery classifications: Scalar subqueries, Column subqueries (IN, ANY, ALL), Row subqueries, Table subqueries",
            "Correlated Subqueries: Row-by-row execution semantics and EXISTS vs IN performance comparison",
            "Common Table Expressions (CTEs): The WITH clause and modular query structuring",
            "Recursive CTEs: Anchor member, recursive member, UNION ALL termination condition, and tree traversal",
            "Performance pitfalls of subqueries vs optimizer join rewrites"
        ],
        "key_takeaways": "EXISTS stops scanning as soon as the first matching row is found (short-circuit boolean evaluation), outperforming IN when subquery tables are large."
    },
    {
        "chapter_num": 5,
        "title": "Advanced Window Functions & Analytical SQL",
        "topics": [
            "The OVER clause architecture: PARTITION BY (grouping), ORDER BY (sorting), and ROWS/RANGE framing",
            "Ranking functions: ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE(k)",
            "Value navigation functions: LEAD(col, offset, default), LAG(), FIRST_VALUE(), LAST_VALUE()",
            "Cumulative aggregations: Running totals, moving 7-day averages, and year-to-date sums",
            "Difference between ROWS BETWEEN and RANGE BETWEEN in sliding window frames"
        ],
        "key_takeaways": "RANK() leaves gaps in sequence following ties (1, 2, 2, 4); DENSE_RANK() leaves no gaps (1, 2, 2, 3). Window functions do not collapse rows, unlike GROUP BY."
    },
    {
        "chapter_num": 6,
        "title": "Database Indexing, Query Plans & Performance Optimization",
        "topics": [
            "B-Tree index architecture: Root node, branch pages, leaf pages, fan-out, and binary search",
            "Clustered index (dictates physical storage order) vs Non-Clustered secondary indexes",
            "Composite indexes and the Leftmost Prefix Rule (multi-column index traversal)",
            "Covering Indexes (Index-Only Scans) bypassing table heap lookups",
            "Reading query execution plans: EXPLAIN, EXPLAIN ANALYZE, Seq Scan vs Index Scan vs Bitmap Heap Scan"
        ],
        "key_takeaways": "A composite index on (A, B, C) accelerates queries filtering on (A) or (A, B), but cannot be utilized for queries filtering solely on (B) or (C) because B-Tree traversal requires the leftmost prefix."
    },
    {
        "chapter_num": 7,
        "title": "Transactions, ACID Properties & Concurrency Isolation",
        "topics": [
            "ACID properties: Atomicity, Consistency, Isolation, Durability",
            "Transaction control language: BEGIN, COMMIT, ROLLBACK, SAVEPOINT",
            "Concurrency anomalies: Dirty Read, Non-Repeatable Read, Phantom Read, Serialization Anomaly",
            "ANSI SQL Isolation Levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable",
            "Pessimistic Locking (SELECT ... FOR UPDATE) vs Optimistic Locking (version columns)"
        ],
        "key_takeaways": "Read Committed prevents Dirty Reads. Repeatable Read prevents Dirty and Non-Repeatable Reads. Serializable isolates transactions entirely via predicate locks or snapshot isolation."
    },
    {
        "chapter_num": 8,
        "title": "Solved Placement SQL Queries & Technical Coding Challenges",
        "topics": [
            "N-th highest salary queries using DENSE_RANK and LIMIT/OFFSET",
            "Consecutive login streak identification using LAG and date arithmetic",
            "Department top-3 earners using window partition ranking",
            "Hierarchical employee tree traversal using Recursive CTEs",
            "Self-assessment practice drills with verified SQL solutions"
        ],
        "key_takeaways": "Mastering DENSE_RANK, LAG date-difference streaks, and Recursive CTEs guarantees success in technical SQL rounds for Amazon, Google, Flipkart, and TCS Digital."
    }
]

SQL_TEXTBOOK_MARKDOWN = r"""# SQL & Database Queries: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** SQL & Relational Database Systems  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement technical tests, SQL assessment queries, and database interview rounds are strictly grounded in the concepts, queries, and optimization strategies detailed in this master textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Relational Theory, Schema Design & Normalization](#chapter-1-relational-theory-schema-design--normalization)
  - [1.1 Relational Foundations & Keys Taxonomy](#11-relational-foundations--keys-taxonomy)
  - [1.2 Integrity Constraints in Relational DDL](#12-integrity-constraints-in-relational-ddl)
  - [1.3 The Normalization Pipeline (1NF, 2NF, 3NF, BCNF)](#13-the-normalization-pipeline-1nf-2nf-3nf-bcnf)
- [Chapter 2: SQL Query Execution Order & Deep Filtering Mechanics](#chapter-2-sql-query-execution-order--deep-filtering-mechanics)
  - [2.1 The 10-Step Query Processing Pipeline](#21-the-10-step-query-processing-pipeline)
  - [2.2 WHERE vs HAVING Operational Boundaries](#22-where-vs-having-operational-boundaries)
  - [2.3 Three-Valued Logic & NULL Pitfalls](#23-three-valued-logic--null-pitfalls)
  - [2.4 Conditional CASE WHEN Expressions & Pivoting](#24-conditional-case-when-expressions--pivoting)
- [Chapter 3: Mastering SQL Joins & Set Operations](#chapter-3-mastering-sql-joins--set-operations)
  - [3.1 The 4 Core Joins: INNER, LEFT, RIGHT, FULL](#31-the-4-core-joins-inner-left-right-full)
  - [3.2 CROSS JOIN & Non-Equi Joins](#32-cross-join--non-equi-joins)
  - [3.3 Self-Joins for Hierarchical Reporting](#33-self-joins-for-hierarchical-reporting)
  - [3.4 Set Operations: UNION, UNION ALL, INTERSECT, EXCEPT](#34-set-operations-union-union-all-intersect-except)
- [Chapter 4: Subqueries, Correlated Subqueries & CTEs](#chapter-4-subqueries-correlated-subqueries--ctes)
  - [4.1 Subquery Types: Scalar, Multi-Row & Table Subqueries](#41-subquery-types-scalar-multi-row--table-subqueries)
  - [4.2 Correlated Subqueries & EXISTS vs IN](#42-correlated-subqueries--exists-vs-in)
  - [4.3 Common Table Expressions (CTEs) & Readability](#43-common-table-expressions-ctes--readability)
  - [4.4 Recursive CTEs for Trees & Graphs](#44-recursive-ctes-for-trees--graphs)
- [Chapter 5: Advanced Window Functions & Analytical SQL](#chapter-5-advanced-window-functions--analytical-sql)
  - [5.1 The OVER Clause Architecture](#51-the-over-clause-architecture)
  - [5.2 Ranking Functions: ROW_NUMBER vs RANK vs DENSE_RANK](#52-ranking-functions-row_number-vs-rank-vs-dense_rank)
  - [5.3 Value Navigation: LEAD, LAG & FIRST_VALUE](#53-value-navigation-lead-lag--first_value)
  - [5.4 Moving Averages & Cumulative Framing](#54-moving-averages--cumulative-framing)
- [Chapter 6: Database Indexing, Query Plans & Performance Optimization](#chapter-6-database-indexing-query-plans--performance-optimization)
  - [6.1 B-Tree Index Mechanics](#61-b-tree-index-mechanics)
  - [6.2 Clustered vs Secondary Indexes](#62-clustered-vs-secondary-indexes)
  - [6.3 Composite Indexes & The Leftmost Prefix Rule](#63-composite-indexes--the-leftmost-prefix-rule)
  - [6.4 Query Plan Analysis with EXPLAIN ANALYZE](#64-query-plan-analysis-with-explain-analyze)
- [Chapter 7: Transactions, ACID Properties & Concurrency Isolation](#chapter-7-transactions-acid-properties--concurrency-isolation)
  - [7.1 ACID Properties](#71-acid-properties)
  - [7.2 Concurrency Anomalies & ANSI Isolation Levels](#72-concurrency-anomalies--ansi-isolation-levels)
  - [7.3 Pessimistic vs Optimistic Locking](#73-pessimistic-vs-optimistic-locking)
- [Chapter 8: Solved Placement SQL Queries & Technical Coding Challenges](#chapter-8-solved-placement-sql-queries--technical-coding-challenges)
  - [Challenge 1: N-th Highest Salary (FAANG Classic)](#challenge-1-n-th-highest-salary-faang-classic)
  - [Challenge 2: Consecutive Login Streaks (Gaps and Islands)](#challenge-2-consecutive-login-streaks-gaps-and-islands)
  - [Challenge 3: Department Top 3 Earners](#challenge-3-department-top-3-earners)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: Relational Theory, Schema Design & Normalization

### 1.1 Relational Foundations & Keys Taxonomy
In relational theory, data is organized into **Relations** (tables), which consist of a schema defining the relation name and set of **Attributes** (columns), and an instance consisting of a set of **Tuples** (rows).

**Hierarchy of Relational Keys:**
1. **Superkey:** Any set of one or more attributes that uniquely identifies every tuple in the relation.
2. **Candidate Key:** A **minimal Superkey** (no proper subset is also a superkey). A table can possess multiple candidate keys.
3. **Primary Key:** The single candidate key selected by the database designer as the primary identifier for tuples in the table. Must strictly contain no `NULL` values.
4. **Alternate Key:** Any candidate key not chosen as the primary key.
5. **Foreign Key:** An attribute (or set of attributes) in table $R_1$ that references the primary key (or unique key) of table $R_2$, enforcing referential integrity.
6. **Composite Key:** A key composed of two or more attributes.

### 1.2 Integrity Constraints in Relational DDL
```sql
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    salary NUMERIC(12, 2) CHECK (salary >= 20000.00),
    dept_id INT REFERENCES departments(dept_id) ON DELETE CASCADE,
    hire_date DATE DEFAULT CURRENT_DATE
);
```

### 1.3 The Normalization Pipeline (1NF, 2NF, 3NF, BCNF)
Normalization systematically decomposes relation schemas to eliminate redundant data storage and insertion, update, and deletion anomalies:

```
[ Unnormalized Table ] -> [ 1NF: Atomic values; no repeating groups ]
                              |
                              v
                          [ 2NF: 1NF + No partial functional dependencies ]
                              |
                              v
                          [ 3NF: 2NF + No transitive dependencies (X->Y where X superkey or Y prime) ]
                              |
                              v
                          [ BCNF: 3NF + Strictly X is superkey for EVERY non-trivial FD X->Y ]
```

---

## Chapter 2: SQL Query Execution Order & Deep Filtering Mechanics

### 2.1 The 10-Step Query Processing Pipeline
In procedural programming languages, code executes sequentially from top to bottom. In declarative SQL, the database engine evaluates clauses in a **strictly defined logical execution order** fundamentally different from the lexical written order:

```
Lexical Written Order:            Logical Database Execution Order:
1. SELECT                         1. FROM & JOINs (identify & merge source tables)
2. DISTINCT                       2. ON (filter join match conditions)
3. FROM & JOIN                    3. WHERE (filter individual raw rows)
4. WHERE                          4. GROUP BY (aggregate rows into distinct groups)
5. GROUP BY                       5. HAVING (filter aggregated groups)
6. HAVING                         6. SELECT (evaluate expressions & window functions)
7. WINDOW                         7. DISTINCT (deduplicate result rows)
8. UNION / SET                    8. ORDER BY (sort output rows)
9. ORDER BY                       9. LIMIT / OFFSET (slice final output page)
10. LIMIT / OFFSET
```

**Why This Order Matters in Interviews:**
- **Aliases Defined in `SELECT` Cannot Be Used in `WHERE`:** Because `WHERE` executes at Step 3, before `SELECT` has evaluated aliases at Step 6:
  ```sql
  -- FAILS: Column alias 'total_comp' does not exist yet when WHERE executes!
  SELECT salary + COALESCE(bonus, 0) AS total_comp
  FROM employees
  WHERE total_comp > 100000; -- Syntax error!

  -- CORRECT: Repeat expression or use CTE:
  SELECT salary + COALESCE(bonus, 0) AS total_comp
  FROM employees
  WHERE salary + COALESCE(bonus, 0) > 100000;
  ```

### 2.2 WHERE vs HAVING Operational Boundaries
| Feature | `WHERE` Clause | `HAVING` Clause |
|:---|:---|:---|
| **Execution Point** | Step 3 (Pre-aggregation) | Step 5 (Post-aggregation) |
| **Operates On** | Individual raw table rows | Clustered aggregated groups |
| **Aggregate Functions** | **Forbidden** (e.g., `WHERE AVG(salary) > 50000` is illegal) | **Allowed and encouraged** (`HAVING AVG(salary) > 50000`) |
| **Performance** | Filters rows early, minimizing data sent to grouping/sorting | Evaluates after memory-heavy grouping has completed |

```sql
SELECT dept_id, AVG(salary) AS avg_sal, COUNT(*) AS emp_count
FROM employees
WHERE salary > 30000 -- Step 3: Excludes entry-level interns before aggregation
GROUP BY dept_id     -- Step 4: Groups remaining rows by department
HAVING COUNT(*) >= 5 -- Step 5: Retains departments with at least 5 qualifying staff
ORDER BY avg_sal DESC;
```

### 2.3 Three-Valued Logic & NULL Pitfalls
In SQL, `NULL` represents missing or unknown data. Comparisons involving `NULL` evaluate not to `TRUE` or `FALSE`, but to **`UNKNOWN`**:

```
Truth Tables for 3-Valued Logic:
AND        TRUE      FALSE     UNKNOWN       OR         TRUE      FALSE     UNKNOWN
TRUE       TRUE      FALSE     UNKNOWN       TRUE       TRUE      TRUE      TRUE
FALSE      FALSE     FALSE     FALSE         FALSE      TRUE      FALSE     UNKNOWN
UNKNOWN    UNKNOWN   FALSE     UNKNOWN       UNKNOWN    TRUE      UNKNOWN   UNKNOWN
```

- **The Equality Pitfall:** `salary = NULL` evaluates to `UNKNOWN`. In a `WHERE` clause, only expressions evaluating strictly to `TRUE` are returned. Thus, `salary = NULL` returns 0 rows! Always use `IS NULL` or `IS NOT NULL`.
- **The NOT IN Trap:** If a subquery returns even a single `NULL` value, `NOT IN` will return **0 rows** for the entire query:
  ```sql
  -- DANGEROUS: If any inactive employee has NULL manager_id, this returns NO rows!
  SELECT * FROM employees WHERE emp_id NOT IN (SELECT manager_id FROM employees);

  -- BULLETPROOF: Use NOT EXISTS or filter out NULLs:
  SELECT e.* FROM employees e
  WHERE NOT EXISTS (
      SELECT 1 FROM employees m WHERE m.manager_id = e.emp_id
  );
  ```

### 2.4 Conditional CASE WHEN Expressions & Pivoting
```sql
-- Dynamic Salary Grade Tagging
SELECT first_name, salary,
       CASE 
           WHEN salary >= 120000 THEN 'Executive'
           WHEN salary >= 80000  THEN 'Senior'
           WHEN salary >= 50000  THEN 'Mid-Level'
           ELSE 'Associate'
       END AS compensation_tier
FROM employees;

-- Pivoting Rows into Columns via Conditional Aggregation
SELECT 
    dept_id,
    SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) AS female_count,
    COUNT(*) AS total_count
FROM employees
GROUP BY dept_id;
```

---

## Chapter 3: Mastering SQL Joins & Set Operations

### 3.1 The 4 Core Joins: INNER, LEFT, RIGHT, FULL
Given Table $A$ (Left) and Table $B$ (Right):

```
       INNER JOIN                     LEFT JOIN                     FULL OUTER JOIN
    +-------+-------+             +-------+-------+             +-------+-------+
    |   A   |  A∩B  |             |   A   |  A∩B  |             |   A   |  A∩B  |   B   |
    |       |   X   |             |   X   |   X   |             |   X   |   X   |   X   |
    +-------+-------+             +-------+-------+             +-------+-------+
    Only matching rows            All of A + matching B         All rows from A and B
```

- **INNER JOIN:** Returns records where the join predicate evaluates to `TRUE` in both tables.
- **LEFT (OUTER) JOIN:** Returns all records from the left table, and matching records from the right table. Non-matching right columns are populated with `NULL`.
- **RIGHT (OUTER) JOIN:** Returns all records from the right table, and matching left records.
- **FULL OUTER JOIN:** Returns all records when there is a match in either left or right table.

### 3.2 CROSS JOIN & Non-Equi Joins
- **CROSS JOIN:** Produces the Cartesian product of two tables. If table $A$ has $N$ rows and table $B$ has $M$ rows, result has $N \times M$ rows. Essential for generating test grids, date-spine tables, or product-size matrix combinations.
- **Non-Equi Join:** Uses comparison operators other than equality (`<`, `>`, `<=`, `>=`, `BETWEEN`):
  ```sql
  -- Tag employee salaries against tax bracket intervals
  SELECT e.first_name, e.salary, b.bracket_name, b.tax_rate
  FROM employees e
  JOIN tax_brackets b 
    ON e.salary BETWEEN b.min_salary AND b.max_salary;
  ```

### 3.3 Self-Joins for Hierarchical Reporting
Joining a table to itself to resolve recursive parent-child relationships:
```sql
SELECT 
    e.first_name AS employee_name,
    e.salary AS employee_salary,
    COALESCE(m.first_name, 'Top Executive') AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```

### 3.4 Set Operations: UNION, UNION ALL, INTERSECT, EXCEPT
- **UNION:** Combines result sets of two queries and eliminates duplicate rows (executes internal sort/hash deduplication).
- **UNION ALL:** Combines result sets and preserves all duplicates. Executes significantly faster than `UNION`.
- **INTERSECT:** Returns only rows present in both query result sets.
- **EXCEPT / MINUS:** Returns rows present in the first query result set that do not exist in the second.

---

## Chapter 4: Subqueries, Correlated Subqueries & CTEs

### 4.1 Subquery Types: Scalar, Multi-Row & Table Subqueries
- **Scalar Subquery:** Returns exactly 1 row and 1 column. Can be placed anywhere a constant value is accepted (in `SELECT`, `WHERE`, `HAVING`).
- **Multi-Row Subquery:** Returns a single column with multiple rows. Evaluated using operators:
  - `IN`: Equality to any member.
  - `> ALL (...)`: Greater than every value in the subquery set (greater than max).
  - `> ANY (...)`: Greater than at least one value in the subquery set (greater than min).

### 4.2 Correlated Subqueries & EXISTS vs IN
A **Correlated Subquery** references a column from the outer query: it executes once for every candidate row evaluated by the outer query:

```sql
-- Find employees who earn more than the average salary of their own department
SELECT e1.emp_id, e1.first_name, e1.salary, e1.dept_id
FROM employees e1
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.dept_id = e1.dept_id -- Correlated reference
);
```

### 4.3 Common Table Expressions (CTEs) & Readability
CTEs define temporary named result sets within the execution scope of a single SQL statement using the `WITH` keyword:
```sql
WITH DeptAvg AS (
    SELECT dept_id, AVG(salary) AS avg_dept_salary
    FROM employees
    GROUP BY dept_id
),
HighEarners AS (
    SELECT e.emp_id, e.first_name, e.salary, e.dept_id, d.avg_dept_salary
    FROM employees e
    JOIN DeptAvg d ON e.dept_id = d.dept_id
    WHERE e.salary > d.avg_dept_salary
)
SELECT * FROM HighEarners ORDER BY salary DESC;
```

### 4.4 Recursive CTEs for Trees & Graphs
A Recursive CTE references its own name. It requires an **Anchor Member**, a `UNION ALL`, and a **Recursive Member** with a termination condition:

```sql
WITH RECURSIVE OrgChart AS (
    -- 1. Anchor Member: Find CEO (manager_id is NULL)
    SELECT emp_id, first_name, manager_id, 1 AS hierarchy_level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 2. Recursive Member: Find all direct reports
    SELECT e.emp_id, e.first_name, e.manager_id, o.hierarchy_level + 1
    FROM employees e
    JOIN OrgChart o ON e.manager_id = o.emp_id
)
SELECT * FROM OrgChart ORDER BY hierarchy_level, manager_id;
```

---

## Chapter 5: Advanced Window Functions & Analytical SQL

### 5.1 The OVER Clause Architecture
Window functions perform calculations across a set of table rows that are related to the current row, **without collapsing individual rows into a single summary row**:

$$\text{FUNCTION}() \ \mathbf{OVER} \ ( \ [\mathbf{PARTITION \ BY} \ \text{partition\_cols}] \ [\mathbf{ORDER \ BY} \ \text{sort\_cols}] \ [\mathbf{ROWS|RANGE} \ \text{frame\_clause}] \ )$$

### 5.2 Ranking Functions: ROW_NUMBER vs RANK vs DENSE_RANK
Given salaries: `100k, 90k, 90k, 80k`:

| Function | Output Values | Behavior on Ties | Subsequent Numbering |
|:---|:---|:---|:---|
| `ROW_NUMBER()` | `1, 2, 3, 4` | Arbitrary tie-breaker | Strict sequential progression |
| `RANK()` | `1, 2, 2, 4` | Identical rank to ties | **Leaves gaps** (skips rank 3) |
| `DENSE_RANK()` | `1, 2, 2, 3` | Identical rank to ties | **No gaps** (subsequent rank is 3) |

```sql
SELECT first_name, salary, dept_id,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS row_num,
       RANK()       OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rank_val,
       DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rank_val
FROM employees;
```

### 5.3 Value Navigation: LEAD, LAG & FIRST_VALUE
- `LAG(col, offset, default)`: Accesses data from a preceding row in the same partition.
- `LEAD(col, offset, default)`: Accesses data from a succeeding row in the same partition.

```sql
-- Compute Month-over-Month (MoM) Revenue Growth Percentage
WITH MonthlyRevenue AS (
    SELECT DATE_TRUNC('month', order_date) AS rev_month,
           SUM(total_amount) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    rev_month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY rev_month) AS prev_month_revenue,
    ROUND(
        ((revenue - LAG(revenue, 1) OVER (ORDER BY rev_month)) / 
        LAG(revenue, 1) OVER (ORDER BY rev_month)) * 100.0, 2
    ) AS mom_growth_pct
FROM MonthlyRevenue;
```

### 5.4 Moving Averages & Cumulative Framing
```sql
SELECT order_date, daily_sales,
       -- Cumulative Running Total from start of year to current row
       SUM(daily_sales) OVER (
           ORDER BY order_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total,
       
       -- 7-Day Centered Moving Average
       AVG(daily_sales) OVER (
           ORDER BY order_date
           ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
       ) AS moving_avg_7d
FROM daily_sales_summary;
```

---

## Chapter 6: Database Indexing, Query Plans & Performance Optimization

### 6.1 B-Tree Index Mechanics
A B-Tree (Balanced Tree) index keeps keys sorted in a multi-level balanced hierarchy:
- Searching for a key requires $O(\log_B N)$ disk page reads, where $B$ is the node fan-out factor ($B \approx 100-500$).
- High fan-out ensures that a table with 10 million rows can be traversed in at most 3 or 4 disk block reads.

### 6.2 Clustered vs Secondary Indexes
- **Clustered Index:** Determines the physical sequential layout of table rows on disk. A table can have strictly **one** clustered index (usually on the primary key). Leaf nodes store the actual complete row data pages.
- **Non-Clustered (Secondary) Index:** A separate structure storing the indexed column value + a row pointer (tuple ID or primary key). Leaf nodes do NOT contain full data rows; querying non-indexed columns requires a secondary **Table Heap Lookup**.

### 6.3 Composite Indexes & The Leftmost Prefix Rule
A composite index defined on `(A, B, C)` can satisfy:
- `WHERE A = 1` (Yes)
- `WHERE A = 1 AND B = 2` (Yes)
- `WHERE A = 1 AND B = 2 AND C = 3` (Yes)
- `WHERE B = 2 AND C = 3` (**NO — violates leftmost prefix rule!** Engine resorts to full table scan).

### 6.4 Query Plan Analysis with EXPLAIN ANALYZE
- **Seq Scan (Table Scan):** Reads every block in the table heap sequentially. Fast for small tables; catastrophic for 10M rows.
- **Index Scan:** Traverses B-Tree to find row pointers, then performs random disk I/O to fetch rows from the table heap.
- **Index Only Scan:** The query's requested columns exist entirely within the index itself (**Covering Index**). Zero table heap I/O required!

---

## Chapter 7: Transactions, ACID Properties & Concurrency Isolation

### 7.1 ACID Properties
- **Atomicity:** All statements in the transaction commit successfully, or all changes are rolled back completely.
- **Consistency:** Transactions move the database from one valid integrity state to another valid state.
- **Isolation:** Concurrent transaction execution yields identical results to serial execution.
- **Durability:** Committed data is guaranteed to survive immediate server power crashes.

### 7.2 Concurrency Anomalies & ANSI Isolation Levels
| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|:---|:---:|:---:|:---:|
| **Read Uncommitted** | Possible | Possible | Possible |
| **Read Committed** | **Prevented** | Possible | Possible |
| **Repeatable Read** | **Prevented** | **Prevented** | Possible |
| **Serializable** | **Prevented** | **Prevented** | **Prevented** |

- **Dirty Read:** Transaction A reads uncommitted modifications made by Transaction B. If B aborts, A read phantom non-existent data.
- **Non-Repeatable Read:** Transaction A reads a row. Transaction B updates that row and commits. Transaction A re-reads the row and observes altered values.
- **Phantom Read:** Transaction A queries rows matching a range predicate (`salary > 50000`). Transaction B inserts a new row satisfying the predicate and commits. Transaction A re-executes the query and sees a new "phantom" row.

---

## Chapter 8: Solved Placement SQL Queries & Technical Coding Challenges

### Challenge 1: N-th Highest Salary (FAANG Classic)
- **Problem:** Write a SQL query to find the $N$-th highest distinct salary from the `Employee` table. If there is no $N$-th highest salary, return `NULL`.
- **Solution (Using DENSE_RANK):**
  ```sql
  CREATE OR REPLACE FUNCTION getNthHighestSalary(N INT) 
  RETURNS TABLE (Salary NUMERIC) AS $$
  BEGIN
      RETURN QUERY (
          WITH RankedSalaries AS (
              SELECT e.salary,
                     DENSE_RANK() OVER (ORDER BY e.salary DESC) AS rnk
              FROM employees e
          )
          SELECT DISTINCT r.salary
          FROM RankedSalaries r
          WHERE r.rnk = N
      );
  END;
  $$ LANGUAGE plpgsql;
  ```

### Challenge 2: Consecutive Login Streaks (Gaps and Islands)
- **Problem (Flipkart / Amazon Interview):** Given a `UserLogins(user_id, login_date)` table, identify all users who logged in for at least 3 consecutive days.
- **Solution:**
  ```sql
  WITH DistinctLogins AS (
      SELECT DISTINCT user_id, CAST(login_date AS DATE) AS log_date
      FROM UserLogins
  ),
  GroupedStreaks AS (
      SELECT user_id, log_date,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY log_date) AS seq,
             log_date - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY log_date) * INTERVAL '1 day') AS grp
      FROM DistinctLogins
  )
  SELECT user_id, MIN(log_date) AS streak_start, MAX(log_date) AS streak_end, COUNT(*) AS consecutive_days
  FROM GroupedStreaks
  GROUP BY user_id, grp
  HAVING COUNT(*) >= 3;
  ```

### Challenge 3: Department Top 3 Earners
- **Problem:** Find all employees who earn in the top 3 unique salaries for their respective department.
- **Solution:**
  ```sql
  WITH DeptRanks AS (
      SELECT 
          d.dept_name,
          e.first_name AS employee,
          e.salary,
          DENSE_RANK() OVER (
              PARTITION BY e.dept_id 
              ORDER BY e.salary DESC
          ) AS salary_rank
      FROM employees e
      JOIN departments d ON e.dept_id = d.dept_id
  )
  SELECT dept_name, employee, salary
  FROM DeptRanks
  WHERE salary_rank <= 3
  ORDER BY dept_name, salary DESC;
  ```

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (WHERE vs HAVING):** Can the `HAVING` clause be used without a `GROUP BY` clause in ANSI SQL?
   - *Solution:* **Yes**. When `HAVING` is used without `GROUP BY`, the entire table is treated as a single aggregate group: `SELECT COUNT(*) FROM employees HAVING COUNT(*) > 10;`.

2. **Exercise 2 (UNION Deduplication):** Why does `UNION ALL` perform faster than `UNION` on datasets with 10 million records?
   - *Solution:* `UNION ALL` simply appends rows from both query streams into the output buffer with zero comparison. Standard `UNION` mandates allocating memory for a hash table or external merge-sort to inspect every tuple for duplicates, introducing $O(N \log N)$ compute and disk spill latency.

3. **Exercise 3 (Composite Index Usage):** An index exists on `(country, state, city)`. Will the query `SELECT * FROM addresses WHERE state = 'California' AND city = 'San Francisco'` utilize the index?
   - *Solution:* **No**. Because the leftmost prefix column `country` is omitted from the predicate, the B-Tree root cannot determine which branch to navigate and must perform a full table scan.

4. **Exercise 4 (EXISTS Short-Circuiting):** Why is `SELECT 1 FROM orders WHERE user_id = e.id` commonly written inside `WHERE EXISTS` instead of selecting table columns?
   - *Solution:* The `EXISTS` predicate cares strictly about the existence of at least one row satisfying the condition. The database query optimizer ignores the `SELECT` list in an `EXISTS` subquery; writing `SELECT 1` or `SELECT *` behaves identically without transmitting column data.

5. **Exercise 5 (Deadlock Resolution):** What mechanism does an enterprise relational database engine employ when two concurrent transactions lock resources in opposing circular order?
   - *Solution:* The engine maintains a **Wait-For Graph (WFG)**. It runs periodic deadlock detection cycles. When a directed cycle is detected ($T_1 \to T_2 \to T_1$), the DBMS automatically selects one transaction as the **Deadlock Victim**, aborts it with an error code, rolls back its uncommitted updates, and releases its locks so the surviving transaction can complete.
"""

SQL_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 2,
        "chapter_title": "SQL Query Execution Order & Deep Filtering Mechanics",
        "subtopic": "WHERE vs HAVING Order",
        "question": "In the standard SQL logical query execution lifecycle, which clause is evaluated immediately after GROUP BY?",
        "options": [
            "HAVING",
            "WHERE",
            "SELECT",
            "ORDER BY"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [SQL Prescribed Textbook — Chapter 2: Query Execution Order]\nThe logical execution order is: FROM -> ON -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT. HAVING evaluates immediately after GROUP BY to filter grouped aggregates.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 5,
        "chapter_title": "Advanced Window Functions & Analytical SQL",
        "subtopic": "RANK vs DENSE_RANK",
        "question": "What is the key difference between the RANK() and DENSE_RANK() window functions when handling tie values?",
        "options": [
            "RANK() skips subsequent rank numbers following a tie, while DENSE_RANK() leaves no gaps in sequential numbering",
            "DENSE_RANK() only works on integer columns",
            "RANK() does not support PARTITION BY",
            "DENSE_RANK() cannot be used with ORDER BY DESC"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [SQL Prescribed Textbook — Chapter 5: Advanced Window Functions]\nWhen two rows share an identical sort value, both functions assign the same rank. However, RANK() skips subsequent numbers (e.g. 1, 2, 2, 4), whereas DENSE_RANK() assigns contiguous sequential integers without gaps (e.g. 1, 2, 2, 3).",
        "difficulty": "easy",
    }
]
'''

with open(os.path.join(TEXTBOOK_DIR, "sql_master.py"), "w", encoding="utf-8") as f:
    f.write(SQL_CODE.strip() + "\n")
ast.parse(SQL_CODE)
print("sql_master.py generated and verified!")

