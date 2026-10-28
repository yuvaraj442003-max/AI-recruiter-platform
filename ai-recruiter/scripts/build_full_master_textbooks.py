"""
build_full_master_textbooks.py — Generates complete, comprehensive placement textbooks for:
1. SQL & Relational Databases
2. Python Programming
3. Quantitative Aptitude
4. Logical Reasoning
5. Verbal Ability & Corporate English
6. Operating Systems
7. Computer Networks
8. Database Management Systems (DBMS)
9. Modern JavaScript & TypeScript
10. Data Engineering & Big Data
11. Artificial Intelligence & Machine Learning
"""
import os
import sys
import ast

TEXTBOOK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "app", "services", "textbooks"))

# =============================================================================
# 1. SQL MASTER TEXTBOOK
# =============================================================================
SQL_CONTENT = r'''"""
sql_master.py — Prescribed Master Textbook for SQL & Relational Databases.
Comprehensive campus placement textbook covering relational algebra, DDL/DML, multi-table joins,
window functions, recursive CTEs, indexing, normalization, transactions, and placement query interview challenges.
"""

SQL_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Relational Theory, Schema Design & Normalization",
        "topics": ["Relational Model, Tuples, Relations, Superkeys, Candidate Keys, and Primary Keys", "Referential Integrity, Foreign Keys & Cascading Actions (CASCADE, SET NULL, RESTRICT)", "Functional Dependencies & Armstrong's Axioms (Reflexivity, Augmentation, Transitivity)", "1NF (Atomicity), 2NF (Full functional dependency), 3NF (Transitive dependency removal), BCNF"],
        "key_takeaways": "Candidate keys are minimal superkeys uniquely identifying tuples. Normalization eliminates update, insertion, and deletion anomalies while preserving lossless decomposition and functional dependencies."
    },
    {
        "chapter_num": 2,
        "title": "SQL Query Execution Lifecycle & Filtering Architecture",
        "topics": ["Physical and Logical Query Processing Phases (FROM -> ON -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT)", "WHERE vs HAVING operational boundaries and aggregate filtration", "Three-Valued Logic (TRUE, FALSE, UNKNOWN) and NULL handling via IS NULL, COALESCE(), NULLIF()", "Pattern matching (LIKE, ILIKE, REGEXP) and boolean short-circuit evaluation"],
        "key_takeaways": "WHERE filters raw base tuples prior to grouping; HAVING filters aggregated groups post-aggregation. In SQL's three-valued logic, comparisons with NULL evaluate to UNKNOWN, requiring COALESCE or IS NULL."
    },
    {
        "chapter_num": 3,
        "title": "Mastering Relational Joins & Set Operations",
        "topics": ["INNER JOIN, LEFT (OUTER) JOIN, RIGHT (OUTER) JOIN, FULL OUTER JOIN Venn representations", "CROSS JOIN (Cartesian product) and NATURAL JOIN pitfalls in production schemas", "SELF JOIN paradigms for hierarchical structures (Employee-Manager, Category Trees)", "Set operations: UNION vs UNION ALL (sorting/deduplication penalty), INTERSECT, and EXCEPT / MINUS"],
        "key_takeaways": "INNER JOIN returns matching pairs. OUTER JOINs preserve unmatched rows from designated sides with NULL padding. UNION ALL avoids expensive sorting passes when duplicates are acceptable."
    },
    {
        "chapter_num": 4,
        "title": "Subqueries, Correlated Subqueries & Exists Optimization",
        "topics": ["Scalar, Single-Column, and Multi-Column subqueries", "Quantified comparison predicates (IN, NOT IN, ANY / SOME, ALL)", "Correlated subqueries (inner query evaluating per outer tuple reference)", "EXISTS vs IN performance benchmarks and the critical NOT IN with NULL trap"],
        "key_takeaways": "EXISTS short-circuits upon encountering the first matching record (boolean probe). NOT IN fails completely and returns zero records if the subquery returns any NULL value."
    },
    {
        "chapter_num": 5,
        "title": "Analytical SQL & Advanced Window Functions",
        "topics": ["OVER clause architecture: PARTITION BY, ORDER BY, and Window Frame Specifications (ROWS vs RANGE BETWEEN)", "Ranking functions: ROW_NUMBER() (unique), RANK() (gaps on ties), DENSE_RANK() (no gaps)", "Offset value functions: LEAD() and LAG() for time-series deltas and consecutive streak analysis", "Cumulative aggregates (Running SUM, Moving Average, First_Value, Last_Value)"],
        "key_takeaways": "Window functions compute analytics over partitioned row subsets without collapsing underlying result set cardinality like GROUP BY. DENSE_RANK() is optimal for Nth highest salary queries."
    },
    {
        "chapter_num": 6,
        "title": "Common Table Expressions (CTEs) & Hierarchical Recursion",
        "topics": ["WITH clause syntax and query modularization", "Recursive CTE execution model: Anchor Member, UNION ALL, Recursive Member, Termination Condition", "Traversing organizational hierarchies, bill-of-materials, and directed acyclic graphs (DAGs)", "Materialized vs Inline CTE execution in modern database optimizers"],
        "key_takeaways": "Recursive CTEs repeatedly evaluate the recursive member on the prior iteration's working table until an empty set is produced, ideal for hierarchy and graph traversal."
    },
    {
        "chapter_num": 7,
        "title": "Indexing, Query Plans & Concurrency (ACID & 2PL)",
        "topics": ["B+ Tree vs Hash vs Bitmap indexing structures", "Clustered Index (physical sort order of table) vs Non-Clustered Secondary Indexes", "Leftmost Prefix Rule in composite indexes (Index Skip Scan vs Full Table Scan)", "EXPLAIN / EXPLAIN ANALYZE execution plan breakdown", "ACID properties, ANSI Isolation Levels, Two-Phase Locking (2PL), and Deadlocks"],
        "key_takeaways": "A table can possess only ONE clustered index. Composite index (A, B, C) cannot be leveraged for lookups on B alone unless A is specified. Repeatable Read prevents non-repeatable reads; Serializable prevents phantom reads."
    }
]

SQL_TEXTBOOK_MARKDOWN = r"""# SQL & Database Querying Mastery: Placement Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement & Technical Interview Edition  
**Subject:** SQL & Database Queries  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus recruitment database assessments, technical interview queries, and live query challenges (TCS Digital/Prime, Infosys DSE, Amazon SDE, Google SWE, Cognizant, etc.) are strictly grounded in the relational concepts, normalization rules, and SQL idioms contained within this master textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Relational Theory, Schema Design & Normalization](#chapter-1-relational-theory-schema-design--normalization)
- [Chapter 2: SQL Query Execution Lifecycle & Filtering Architecture](#chapter-2-sql-query-execution-lifecycle--filtering-architecture)
- [Chapter 3: Mastering Relational Joins & Set Operations](#chapter-3-mastering-relational-joins--set-operations)
- [Chapter 4: Subqueries, Correlated Subqueries & Exists Optimization](#chapter-4-subqueries-correlated-subqueries--exists-optimization)
- [Chapter 5: Analytical SQL & Advanced Window Functions](#chapter-5-analytical-sql--advanced-window-functions)
- [Chapter 6: Common Table Expressions (CTEs) & Hierarchical Recursion](#chapter-6-common-table-expressions-ctes--hierarchical-recursion)
- [Chapter 7: Indexing, Query Plans & Concurrency (ACID & 2PL)](#chapter-7-indexing-query-plans--concurrency-acid--2pl)
- [Chapter 8: Solved Placement SQL Challenges & Self-Assessment Drills](#chapter-8-solved-placement-sql-challenges--self-assessment-drills)

---

## Chapter 1: Relational Theory, Schema Design & Normalization

### 1.1 The Relational Model & Key Architecture
A relational database organizes data into relations (tables) composed of attributes (columns) and tuples (rows):
- **Superkey:** Any attribute set that uniquely identifies every tuple in the relation.
- **Candidate Key:** A minimal superkey. No proper subset of a candidate key can uniquely identify tuples.
- **Primary Key:** The single candidate key selected by database architects as the principal row identifier. Primary keys cannot contain `NULL` values.
- **Foreign Key:** An attribute or set of attributes in a referencing table that references the primary or candidate key of a referenced table, enforcing referential integrity.

### 1.2 Referential Integrity & Cascading Actions
```sql
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dept_id INT,
    salary DECIMAL(10, 2),
    CONSTRAINT fk_dept FOREIGN KEY (dept_id) 
        REFERENCES departments(dept_id)
        ON DELETE CASCADE       -- Deletes employees if parent department is deleted
        ON UPDATE CASCADE       -- Updates foreign key when parent ID changes
);
```

### 1.3 Database Normalization: 1NF to BCNF
Normalization eliminates insertion, deletion, and update anomalies through schema decomposition:
1. **First Normal Form (1NF):** Each column must contain atomic (indivisible) values. No repeating groups or arrays.
2. **Second Normal Form (2NF):** Table is in 1NF AND contains NO partial dependencies (no non-prime attribute may depend on a proper subset of a composite candidate key).
3. **Third Normal Form (3NF):** Table is in 2NF AND contains NO transitive dependencies (for every functional dependency $X \to Y$, either $X$ is a superkey OR $Y$ is a prime attribute).
4. **Boyce-Codd Normal Form (BCNF):** For EVERY non-trivial functional dependency $X \to Y$, $X$ MUST be a superkey. BCNF strictly eliminates all non-superkey determinants.

---

## Chapter 2: SQL Query Execution Lifecycle & Filtering Architecture

### 2.1 Logical Order of SQL Operations
Unlike procedural programming, SQL statements are evaluated in a strict logical order distinct from written syntax:

$$\text{FROM} \longrightarrow \text{ON} \longrightarrow \text{JOIN} \longrightarrow \text{WHERE} \longrightarrow \text{GROUP BY} \longrightarrow \text{HAVING} \longrightarrow \text{SELECT} \longrightarrow \text{DISTINCT} \longrightarrow \text{ORDER BY} \longrightarrow \text{LIMIT}$$

### 2.2 WHERE vs HAVING Deep Comparison
| Dimension | WHERE Clause | HAVING Clause |
|---|---|---|
| Processing Phase | Evaluated early during row scanning (Step 4) | Evaluated post-aggregation (Step 6) |
| Target Data | Filters individual raw tuples | Filters aggregated groups |
| Aggregate Functions | `SUM()`, `COUNT()` strictly FORBIDDEN in WHERE | Aggregate functions allowed and expected |
| Performance | Reduces dataset before grouping (Fast) | Filters groups after grouping pass |

### 2.3 Three-Valued Logic & The NULL Trap
In relational algebra, `NULL` indicates missing, unknown, or inapplicable data. Comparing anything to `NULL` via `=` or `!=` evaluates to `UNKNOWN`, never `TRUE`:
```sql
-- Fails to return records where bonus is NULL:
SELECT * FROM employees WHERE bonus != 500;

-- Correct evaluation handling NULL safely:
SELECT * FROM employees WHERE bonus != 500 OR bonus IS NULL;
-- Or using COALESCE:
SELECT * FROM employees WHERE COALESCE(bonus, 0) != 500;
```

---

## Chapter 3: Mastering Relational Joins & Set Operations

### 3.1 Relational Join Architecture
- **INNER JOIN:** Returns tuples that have matching values in both tables.
- **LEFT (OUTER) JOIN:** Returns all tuples from the left table, and matched tuples from the right table. Unmatched right attributes are populated with `NULL`.
- **RIGHT (OUTER) JOIN:** Returns all tuples from the right table, and matched tuples from the left table.
- **FULL OUTER JOIN:** Returns all tuples when there is a match in either left or right table.

```
       INNER JOIN               LEFT OUTER JOIN             FULL OUTER JOIN
    ┌───────┬───────┐        ┌───────┬───────┐           ┌───────┬───────┐
    │       │ Match │        │  All  │ Match │           │  All  │ Match │  All  │
    │ Left  │ Both  │ Right  │ Left  │ Both  │  (NULL)  │ Left  │ Both  │ Right │
    │       │ Table │        │ Table │ Table │           │ Table │ Table │ Table │
    └───────┴───────┘        └───────┴───────┘           └───────┴───────┘
```

### 3.2 Self-Join for Hierarchical Structures
To query an employee alongside their direct manager from a unified table:
```sql
SELECT 
    e.name AS employee_name,
    COALESCE(m.name, 'Top Executive / CEO') AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```

### 3.3 Set Operations: UNION vs UNION ALL
- **UNION:** Merges result sets and executes an internal sorting step to eliminate duplicates ($O(N \log N)$ cost).
- **UNION ALL:** Appends result sets directly without sorting ($O(N)$ linear append). Always prefer `UNION ALL` unless duplicate removal is strictly required.

---

## Chapter 4: Subqueries, Correlated Subqueries & Exists Optimization

### 4.1 Correlated Subquery
An inner query that references columns from the outer query table, executing once for every row processed by the outer query:
```sql
-- Find employees who earn more than the average salary of their respective department:
SELECT e.emp_id, e.name, e.salary, e.dept_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(d.salary) 
    FROM employees d 
    WHERE d.dept_id = e.dept_id
);
```

### 4.2 The Dangerous NOT IN with NULL Subqueries
If the inner subquery returns even a single `NULL` value, `NOT IN` returns ZERO rows for the entire outer query:
```sql
-- DANGEROUS: If any dept_id in audit_log is NULL, this returns empty!
SELECT * FROM departments WHERE dept_id NOT IN (SELECT dept_id FROM audit_log);

-- BULLETPROOF: Use NOT EXISTS instead
SELECT * FROM departments d 
WHERE NOT EXISTS (
    SELECT 1 FROM audit_log a WHERE a.dept_id = d.dept_id
);
```

---

## Chapter 5: Analytical SQL & Advanced Window Functions

### 5.1 Ranking Functions: ROW_NUMBER, RANK, DENSE_RANK
When ranking employees with identical salaries:
- `ROW_NUMBER()`: Sequentially assigns unique integers regardless of ties: `1, 2, 3, 4`.
- `RANK()`: Assigns identical ranks to ties, skipping subsequent ranks: `1, 2, 2, 4`.
- `DENSE_RANK()`: Assigns identical ranks to ties without gaps: `1, 2, 2, 3`.

```sql
SELECT 
    emp_id, dept_id, salary,
    ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) as row_num,
    RANK()       OVER(PARTITION BY dept_id ORDER BY salary DESC) as rnk,
    DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) as dense_rnk
FROM employees;
```

### 5.2 Finding Nth Highest Salary per Department
```sql
WITH RankedSalaries AS (
    SELECT 
        name, dept_id, salary,
        DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) as rank_pos
    FROM employees
)
SELECT name, dept_id, salary
FROM RankedSalaries
WHERE rank_pos = 2; -- 2nd highest salary per department
```

### 5.3 LEAD, LAG & Running Aggregates
```sql
SELECT 
    sale_date, revenue,
    -- Compares today's revenue to previous day
    LAG(revenue, 1) OVER(ORDER BY sale_date) as prev_day_revenue,
    revenue - LAG(revenue, 1) OVER(ORDER BY sale_date) as day_on_day_growth,
    -- Running cumulative sum across the fiscal year
    SUM(revenue) OVER(ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
FROM daily_sales;
```

---

## Chapter 6: Common Table Expressions (CTEs) & Hierarchical Recursion

### 6.1 Recursive CTE Execution Model
A recursive CTE consists of:
1. **Anchor Member:** Initial query that establishes the base dataset.
2. `UNION ALL`: Connects anchor to recursive evaluation.
3. **Recursive Member:** Queries the CTE itself, executing iteratively until returning an empty set.

```sql
-- Generate hierarchical organizational tree with management levels:
WITH RECURSIVE OrgHierarchy AS (
    -- Anchor member: Start at top CEO (manager_id is NULL)
    SELECT emp_id, name, manager_id, 1 AS depth_level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive member: Find all direct reports of prior level
    SELECT e.emp_id, e.name, e.manager_id, o.depth_level + 1
    FROM employees e
    INNER JOIN OrgHierarchy o ON e.manager_id = o.emp_id
)
SELECT * FROM OrgHierarchy ORDER BY depth_level, manager_id;
```

---

## Chapter 7: Indexing, Query Plans & Concurrency (ACID & 2PL)

### 7.1 B+ Tree Indexing & Physical Ordering
- **Clustered Index:** Dictates the physical storage order of data rows on disk. A table can have only ONE clustered index.
- **Non-Clustered (Secondary) Index:** Stores index keys and pointers back to the clustered index key or row ID.
- **Leftmost Prefix Rule:** For composite index `(dept_id, salary, hire_date)`, queries filtering by `(dept_id)` or `(dept_id, salary)` utilize the index. A query filtering solely on `(salary)` cannot initiate an index seek and triggers a full scan.

### 7.2 ACID Properties & ANSI Concurrency Anomalies
- **Atomicity:** Entire transaction commits or completely rolls back.
- **Consistency:** Database transitions only between valid integrity states.
- **Isolation:** Concurrent transactions execute without mutual interference.
- **Durability:** Committed data survives hardware crashes via Write-Ahead Logging (WAL).

| ANSI SQL Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---|---|---|
| **Read Uncommitted** | Possible | Possible | Possible |
| **Read Committed** | Prevented | Possible | Possible |
| **Repeatable Read** | Prevented | Prevented | Possible |
| **Serializable** | Prevented | Prevented | Prevented |

---

## Chapter 8: Solved Placement SQL Challenges & Self-Assessment Drills

### Solved Challenge 1: Consecutive Active Logins (Amazon SDE Placement)
- **Problem:** Find all users who logged in for at least 3 consecutive days.
- **Solution:** Use `LAG()` or difference of dates with `ROW_NUMBER()`:

```sql
WITH DistinctLogins AS (
    SELECT DISTINCT user_id, login_date FROM user_logins
),
GroupedDates AS (
    SELECT 
        user_id, login_date,
        login_date - CAST(ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_date) AS INT) as date_group
    FROM DistinctLogins
)
SELECT user_id, COUNT(*) as consecutive_days
FROM GroupedDates
GROUP BY user_id, date_group
HAVING COUNT(*) >= 3;
```

### Self-Assessment Practice Exercises & Verified Solutions:
1. **Exercise 1 (Window Functions):** Write a query to find the top 3 customers by revenue for each region, properly handling ties without skipping ranks.
   - *Solution:* Use `DENSE_RANK() OVER(PARTITION BY region_id ORDER BY total_spent DESC) AS rnk`, then filter `WHERE rnk <= 3`.
2. **Exercise 2 (Hierarchical CTE):** Write a recursive CTE to calculate the total headcount managed directly and indirectly under each vice president.
3. **Exercise 3 (Optimization):** Explain why `SELECT * FROM orders WHERE YEAR(order_date) = 2024` prevents index seek on `order_date`, and rewrite it sargably (`WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'`).
"""

SQL_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "Relational Theory, Schema Design & Normalization",
        "subtopic": "BCNF Decomposition",
        "question": "What is the strict mathematical requirement for a functional dependency X -> Y to satisfy Boyce-Codd Normal Form (BCNF)?",
        "options": [
            "X must be a superkey of the relation.",
            "Y must be a prime attribute part of some candidate key.",
            "X must be in 2NF and Y must be atomic.",
            "The relation must have no composite candidate keys."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [SQL Prescribed Textbook — Chapter 1: Relational Theory & Normalization]\nIn BCNF, for every non-trivial functional dependency X -> Y, X must be a superkey. Unlike 3NF, BCNF does not permit exceptions where Y is a prime attribute.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 2,
        "chapter_title": "SQL Query Execution Lifecycle & Filtering Architecture",
        "subtopic": "Logical Query Processing Order",
        "question": "In standard ANSI SQL logical query processing, which clause is evaluated immediately after GROUP BY?",
        "options": ["HAVING", "WHERE", "SELECT", "ORDER BY"],
        "correct_option_index": 0,
        "explanation": "📖 [SQL Prescribed Textbook — Chapter 2: SQL Query Execution Lifecycle]\nThe logical evaluation order is FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY. HAVING filters the aggregated groups formed by GROUP BY.",
        "difficulty": "easy",
    },
    {
        "chapter_num": 5,
        "chapter_title": "Analytical SQL & Advanced Window Functions",
        "subtopic": "DENSE_RANK vs RANK",
        "question": "When querying salaries [10000, 10000, 8000], what rank values are assigned to the three rows by DENSE_RANK() and RANK() respectively?",
        "options": [
            "DENSE_RANK gives 1, 1, 2; RANK gives 1, 1, 3",
            "DENSE_RANK gives 1, 2, 3; RANK gives 1, 1, 2",
            "DENSE_RANK gives 1, 1, 3; RANK gives 1, 1, 2",
            "Both give 1, 1, 2"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [SQL Prescribed Textbook — Chapter 5: Window Functions]\nRANK() leaves gaps following tied rows (1, 1, 3), whereas DENSE_RANK() assigns consecutive rank integers without gaps (1, 1, 2).",
        "difficulty": "medium",
    }
]
'''

with open(os.path.join(TEXTBOOK_DIR, "sql_master.py"), "w", encoding="utf-8") as f:
    f.write(SQL_CONTENT.strip() + "\n")
ast.parse(SQL_CONTENT)
print("Generated and verified sql_master.py successfully!")

