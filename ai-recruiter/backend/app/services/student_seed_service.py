"""
student_seed_service.py — Seeds high-quality aptitude questions, mock tests,
study materials, and learning roadmaps for college students.
"""
import json
import logging
import math
import uuid
from sqlalchemy.orm import Session

from app.models.student import (
    AptitudeTopic,
    AptitudeQuestion,
    AptitudeTest,
    StudyMaterial,
    LearningRoadmap,
)

logger = logging.getLogger(__name__)


def seed_student_ecosystem(db: Session) -> None:
    """Seeds topics, questions, tests, study materials, and roadmaps if not already present."""
    try:
        _seed_aptitude(db)
        _seed_study_materials(db)
        _seed_roadmaps(db)
        from app.services.book_curriculum_service import seed_prescribed_books_to_db
        seed_prescribed_books_to_db(db)
        db.commit()
        logger.info("Successfully verified and seeded Student Placement Ecosystem data.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to seed student ecosystem: {e}")


def _seed_aptitude(db: Session) -> None:
    # Ensure all aptitude tests strictly enforce the 30-seconds-per-question rule
    existing_tests = db.query(AptitudeTest).all()
    if existing_tests:
        for t in existing_tests:
            total_q = t.total_questions if (t.total_questions and t.total_questions > 0) else 10
            expected_mins = max(1, math.ceil(total_q * 30 / 60))
            if t.duration_minutes != expected_mins:
                t.duration_minutes = expected_mins
        db.commit()

    # Check if topics exist
    if db.query(AptitudeTopic).count() > 0:
        return

    topics_data = [
        {
            "name": "Quantitative Aptitude",
            "slug": "quantitative-aptitude",
            "description": "Percentages, Profit & Loss, Time & Work, Speed, Ratios, Probability, Permutations & Combinations.",
            "icon": "📐",
            "order_index": 1,
        },
        {
            "name": "Logical Reasoning",
            "slug": "logical-reasoning",
            "description": "Syllogisms, Coding-Decoding, Blood Relations, Seating Arrangement, Direction Sense, Series.",
            "icon": "🧩",
            "order_index": 2,
        },
        {
            "name": "Verbal Ability & English",
            "slug": "verbal-ability",
            "description": "Reading Comprehension, Sentence Correction, Error Spotting, Synonyms/Antonyms, Para Jumbles.",
            "icon": "📖",
            "order_index": 3,
        },
        {
            "name": "Core CS & Data Interpretation",
            "slug": "data-interpretation-cs",
            "description": "Charts, Tables, OOP Concepts, Database Queries, OS Basics, Computer Networks.",
            "icon": "💻",
            "order_index": 4,
        },
    ]

    topic_objs = {}
    for td in topics_data:
        topic = AptitudeTopic(
            name=td["name"],
            slug=td["slug"],
            description=td["description"],
            icon=td["icon"],
            order_index=td["order_index"],
        )
        db.add(topic)
        topic_objs[td["slug"]] = topic

    db.flush()

    # Seed Questions
    questions_data = [
        # Quantitative Aptitude
        {
            "topic": "quantitative-aptitude",
            "subtopic": "Time and Work",
            "question": "A can finish a project in 12 days and B can finish the same project in 18 days. If they work together, in how many days will the project be completed?",
            "options": ["7.2 days", "8 days", "6 days", "7.5 days"],
            "correct": 0,
            "explanation": "A's 1-day work = 1/12. B's 1-day work = 1/18. Together in 1 day = 1/12 + 1/18 = (3+2)/36 = 5/36. Total days = 36/5 = 7.2 days.",
            "difficulty": "easy",
            "company": "TCS",
        },
        {
            "topic": "quantitative-aptitude",
            "subtopic": "Profit and Loss",
            "question": "A trader sells a laptop at a 15% discount on the marked price and still makes a 20% profit. If the cost price is $800, what is the marked price?",
            "options": ["$1,129.41", "$1,080.00", "$1,150.00", "$1,200.00"],
            "correct": 0,
            "explanation": "Cost Price = 800. Selling Price with 20% profit = 800 * 1.20 = 960. Marked Price * (1 - 0.15) = 960 => MP = 960 / 0.85 ≈ $1,129.41.",
            "difficulty": "medium",
            "company": "Infosys",
        },
        {
            "topic": "quantitative-aptitude",
            "subtopic": "Speed, Time and Distance",
            "question": "A train 180 meters long running at a speed of 72 km/h crosses a platform in 20 seconds. What is the length of the platform?",
            "options": ["220 meters", "200 meters", "240 meters", "180 meters"],
            "correct": 0,
            "explanation": "Speed in m/s = 72 * (5/18) = 20 m/s. Total distance in 20s = 20 * 20 = 400 m. Total distance = Train Length + Platform Length. Platform Length = 400 - 180 = 220 m.",
            "difficulty": "medium",
            "company": "Wipro",
        },
        {
            "topic": "quantitative-aptitude",
            "subtopic": "Probability",
            "question": "Two fair dice are thrown simultaneously. What is the probability of getting a sum greater than 9?",
            "options": ["1/6", "5/36", "1/4", "7/36"],
            "correct": 0,
            "explanation": "Total outcomes = 36. Favorable outcomes with sum > 9: Sum=10: (4,6), (5,5), (6,4) [3]. Sum=11: (5,6), (6,5) [2]. Sum=12: (6,6) [1]. Total favorable = 6. Probability = 6/36 = 1/6.",
            "difficulty": "medium",
            "company": "Amazon",
        },
        {
            "topic": "quantitative-aptitude",
            "subtopic": "Permutations & Combinations",
            "question": "In how many different ways can the letters of the word 'CAMPUS' be arranged so that the vowels always come together?",
            "options": ["240", "120", "360", "720"],
            "correct": 0,
            "explanation": "Vowels in CAMPUS: A, U (2 vowels). Consonants: C, M, P, S (4 consonants). Treat (A, U) as 1 unit. We have 5 units: 5! = 120. The 2 vowels can arrange among themselves in 2! = 2 ways. Total = 120 * 2 = 240.",
            "difficulty": "hard",
            "company": "TCS",
        },

        # Logical Reasoning
        {
            "topic": "logical-reasoning",
            "subtopic": "Syllogisms",
            "question": "Statements: 1. All engineers are problem solvers. 2. Some problem solvers are coders.\nConclusions: I. Some engineers are coders. II. Some coders are problem solvers.",
            "options": ["Only conclusion II follows", "Only conclusion I follows", "Both I and II follow", "Neither I nor II follows"],
            "correct": 0,
            "explanation": "From statement 2, 'Some problem solvers are coders' directly converts to 'Some coders are problem solvers' (Conclusion II is valid). Engineer and coder have no definite overlap given.",
            "difficulty": "medium",
            "company": "Infosys",
        },
        {
            "topic": "logical-reasoning",
            "subtopic": "Coding-Decoding",
            "question": "In a certain code language, 'SYSTEM' is written as 'SYSMET' and 'NEARER' is written as 'AENRER'. How is 'FRACTION' written in that code?",
            "options": ["CARFNOIT", "ARFCNOIT", "CARFNOIT", "CARFTION"],
            "correct": 0,
            "explanation": "The word is divided into two halves and reversed. FRACTION has 8 letters: FRAC and TION. FRAC reversed is CARF. TION reversed is NOIT. Combined: CARFNOIT.",
            "difficulty": "medium",
            "company": "Cognizant",
        },
        {
            "topic": "logical-reasoning",
            "subtopic": "Blood Relations",
            "question": "Pointing to a photograph, Rohit said, 'She is the daughter of my grandfather's only son.' How is the girl in the photograph related to Rohit?",
            "options": ["Sister", "Mother", "Aunt", "Cousin"],
            "correct": 0,
            "explanation": "Rohit's grandfather's only son is Rohit's father. The daughter of Rohit's father is Rohit's sister.",
            "difficulty": "easy",
            "company": "TCS",
        },
        {
            "topic": "logical-reasoning",
            "subtopic": "Number Series",
            "question": "Find the missing number in the series: 2, 6, 12, 20, 30, 42, ?",
            "options": ["56", "54", "58", "60"],
            "correct": 0,
            "explanation": "Pattern: 1*2=2, 2*3=6, 3*4=12, 4*5=20, 5*6=30, 6*7=42, 7*8=56. Next is 56.",
            "difficulty": "easy",
            "company": "Wipro",
        },
        {
            "topic": "logical-reasoning",
            "subtopic": "Direction Sense",
            "question": "A student walks 20 meters North, turns right and walks 30 meters, then turns right again and walks 35 meters. How far and in which direction is the student from the starting point?",
            "options": ["33.54 meters South-East", "25 meters North-East", "30 meters South", "35 meters South-West"],
            "correct": 0,
            "explanation": "North +20, East +30, South -35 => Net Y = -15 (South), Net X = +30 (East). Distance = sqrt(30^2 + 15^2) = sqrt(900 + 225) = sqrt(1125) ≈ 33.54 meters South-East.",
            "difficulty": "hard",
            "company": "Amazon",
        },

        # Verbal Ability
        {
            "topic": "verbal-ability",
            "subtopic": "Sentence Correction",
            "question": "Choose the grammatically correct sentence:",
            "options": [
                "Neither the manager nor the employees were informed about the schedule change.",
                "Neither the manager nor the employees was informed about the schedule change.",
                "Neither the manager or the employees was informed about the schedule change.",
                "Neither the manager nor the employees has been informed about the schedule change.",
            ],
            "correct": 0,
            "explanation": "With 'neither... nor', the verb agrees with the closer subject ('employees' is plural, so 'were informed' is correct).",
            "difficulty": "medium",
            "company": "TCS",
        },
        {
            "topic": "verbal-ability",
            "subtopic": "Vocabulary & Synonyms",
            "question": "What is the closest synonym for 'PRAGMATIC'?",
            "options": ["Practical", "Idealistic", "Theoretical", "Fictional"],
            "correct": 0,
            "explanation": "Pragmatic means dealing with things sensibly and realistically in a way that is based on practical rather than theoretical considerations.",
            "difficulty": "easy",
            "company": "Infosys",
        },
        {
            "topic": "verbal-ability",
            "subtopic": "Error Spotting",
            "question": "Identify the part containing an error: 'He has been studying (A) / for this placement exam (B) / since three months (C) / without taking a break (D).'",
            "options": ["Part (C)", "Part (A)", "Part (B)", "Part (D)"],
            "correct": 0,
            "explanation": "For a duration of time (three months), the preposition 'for' should be used instead of 'since'. Correct phrase: 'for three months'.",
            "difficulty": "easy",
            "company": "Accenture",
        },

        # Core CS & Technical Concepts
        {
            "topic": "data-interpretation-cs",
            "subtopic": "Database & SQL",
            "question": "Which of the following SQL clauses is executed FIRST during query evaluation?",
            "options": ["FROM", "WHERE", "SELECT", "ORDER BY"],
            "correct": 0,
            "explanation": "SQL logical query execution order: 1. FROM & JOINs, 2. WHERE, 3. GROUP BY, 4. HAVING, 5. SELECT, 6. DISTINCT, 7. ORDER BY, 8. LIMIT.",
            "difficulty": "medium",
            "company": "Amazon",
        },
        {
            "topic": "data-interpretation-cs",
            "subtopic": "Data Structures & Complexity",
            "question": "What is the worst-case time complexity of searching for an element in an unbalanced Binary Search Tree (BST)?",
            "options": ["O(N)", "O(log N)", "O(1)", "O(N log N)"],
            "correct": 0,
            "explanation": "In an unbalanced (skewed) BST, elements are arranged linearly like a linked list, degrading search time to O(N). Balanced BSTs (AVL, Red-Black) maintain O(log N).",
            "difficulty": "medium",
            "company": "TCS",
        },
        {
            "topic": "data-interpretation-cs",
            "subtopic": "Operating Systems",
            "question": "Which of the following is NOT one of Coffman's four conditions required for a deadlock to occur?",
            "options": ["Preemption allowed", "Mutual Exclusion", "Hold and Wait", "Circular Wait"],
            "correct": 0,
            "explanation": "Coffman conditions are: 1. Mutual Exclusion, 2. Hold and Wait, 3. No Preemption (preemption is NOT allowed), and 4. Circular Wait.",
            "difficulty": "medium",
            "company": "Infosys",
        },
    ]

    created_questions = []
    for i, qd in enumerate(questions_data):
        topic_obj = topic_objs.get(qd["topic"])
        if not topic_obj:
            continue

        # Distribute correct answers evenly across A (0), B (1), C (2), D (3)
        target_idx = i % 4
        opts = list(qd["options"])
        curr_idx = qd.get("correct", 0)
        if len(opts) == 4 and curr_idx != target_idx:
            opts[curr_idx], opts[target_idx] = opts[target_idx], opts[curr_idx]
            curr_idx = target_idx

        q = AptitudeQuestion(
            topic_id=topic_obj.id,
            subtopic=qd["subtopic"],
            question=qd["question"],
            options_json=json.dumps(opts),
            correct_option_index=curr_idx,
            explanation=qd["explanation"],
            difficulty=qd["difficulty"],
            company_tag=qd["company"],
        )
        db.add(q)
        created_questions.append(q)

    db.flush()

    # Create Pre-packaged Tests (30 seconds per question rule)
    tests_data = [
        {
            "title": "TCS NQT National Placement Mock Test 1",
            "description": "Comprehensive simulation covering Quantitative, Logical Reasoning, and Verbal Ability calibrated to the latest TCS NQT exam pattern.",
            "category": "company_mock",
            "company_name": "TCS",
            "duration_minutes": max(1, math.ceil(len(created_questions) * 30 / 60)),  # 30s per question (8 mins for 16 Qs)
            "total_questions": len(created_questions),
            "passing_percentage": 65.0,
            "q_ids": [str(q.id) for q in created_questions],
        },
        {
            "title": "Daily 5-Minute Aptitude & Reasoning Sprint",
            "description": "Quick daily challenge to keep your analytical reflexes sharp for campus selection tests.",
            "category": "daily_practice",
            "company_name": "General",
            "duration_minutes": max(1, math.ceil(min(10, len(created_questions)) * 30 / 60)),  # 30s per question (5 mins for 10 Qs)
            "total_questions": min(10, len(created_questions)),
            "passing_percentage": 60.0,
            "q_ids": [str(q.id) for q in created_questions[:10]],
        },
        {
            "title": "Infosys Special Program Aptitude Booster",
            "description": "Targeted questions focused on puzzle solving, high-speed arithmetic, and vocabulary.",
            "category": "company_mock",
            "company_name": "Infosys",
            "duration_minutes": max(1, math.ceil(min(8, len(created_questions)) * 30 / 60)),  # 30s per question (4 mins for 8 Qs)
            "total_questions": min(8, len(created_questions)),
            "passing_percentage": 70.0,
            "q_ids": [str(q.id) for q in created_questions if q.company_tag in ["Infosys", "General", "Cognizant"]],
        },
    ]

    for td in tests_data:
        test = AptitudeTest(
            title=td["title"],
            description=td["description"],
            category=td["category"],
            company_name=td["company_name"],
            duration_minutes=td["duration_minutes"],
            total_questions=td["total_questions"],
            passing_percentage=td["passing_percentage"],
            question_ids_json=json.dumps(td["q_ids"]),
            is_active=True,
        )
        db.add(test)

    db.flush()

    # Index seeded aptitude questions into Qdrant vector database
    try:
        from app.services.qdrant_service import upsert_batch, COLLECTION_APTITUDE
        apt_items = []
        for q in created_questions:
            topic_str = q.topic_name or (q.topic.name if q.topic else "")
            if not topic_str:
                for slug, tobj in topic_objs.items():
                    if tobj.id == q.topic_id:
                        topic_str = tobj.name
                        break
            full_text = f"Topic: {topic_str or 'Aptitude'}\nSubtopic: {q.subtopic}\nQuestion: {q.question}"
            apt_items.append({
                "id": str(q.id),
                "text": full_text,
                "metadata": {
                    "question_id": str(q.id),
                    "topic_name": topic_str or "Aptitude",
                    "subtopic": q.subtopic,
                    "difficulty": q.difficulty,
                    "company_tag": q.company_tag,
                },
            })
        if apt_items:
            upsert_batch(COLLECTION_APTITUDE, apt_items)
    except Exception as exc:
        pass


def _seed_study_materials(db: Session) -> None:
    materials_data = [
        {
            "title": "Campus Placement 60-Day Master Sprint Guide",
            "slug": "campus-placement-60-day-sprint",
            "category": "interview_prep",
            "content_type": "guide",
            "description": "The battle-tested 8-week structured roadmap to crack campus aptitude tests, coding rounds, and technical interviews.",
            "company_tag": "General",
            "difficulty": "beginner",
            "estimated_read_time": "12 mins",
            "tags": ["Roadmap", "Placement", "Strategy", "Aptitude", "DSA"],
            "order_index": 1,
            "content": """# Campus Placement 60-Day Master Sprint Guide

Cracking on-campus and off-campus recruitment drives requires a structured, multi-disciplinary approach. Top tech companies and mass recruiters evaluate candidates across four clear gates:

---

## 🎯 The 4-Stage Recruitment Pipeline

1. **Aptitude & Logical Screening**: Eliminates 60–70% of candidates. Focus on speed, shortcuts, and accuracy.
2. **Coding Assessment**: Multi-language programming problems (Arrays, Strings, HashMaps, Trees).
3. **Technical Interview**: Deep dive into your projects, OOPs, DBMS, Operating Systems, and live coding.
4. **HR & Behavioral Round**: Communication skills, cultural fit, willingness to learn, and situational responses.

---

## 📅 The 8-Week Action Plan

### Weeks 1–2: Aptitude Foundations & Basic DSA
* **Daily Quantitative**: 30 mins on Percentages, Profit/Loss, Ratios, Time & Work.
* **Daily Logical**: 30 mins on Syllogisms, Series, Blood Relations.
* **DSA**: Arrays, Two-Pointer technique, Strings, and HashMap fundamentals.

### Weeks 3–4: Intermediate Coding & Core CS
* **DSA Focus**: Recursion, Binary Search, Linked Lists, Stacks & Queues.
* **Core CS**: SQL queries (JOINs, GROUP BY, Aggregates), Normalization, and ACID properties.
* **Project Review**: Clean up GitHub repositories, write clear README files, and deploy live demos.

### Weeks 5–6: Trees, Dynamic Programming & System Design Basics
* **DSA**: Binary Trees, BST traversal, Graph BFS/DFS, basic DP (Knapsack, LCS).
* **Core CS**: OS concepts (Process vs Thread, Deadlocks, Virtual Memory), Networks (TCP/IP, HTTP vs HTTPS).
* **Mock Interviews**: Practice answering STAR method questions out loud.

### Weeks 7–8: Company Mock Tests & Final Polish
* Take full-length timed mock tests daily on this platform.
* Refine your resume using the AI ATS checker to score above 85.
* Practice self-introduction: 90 seconds summarizing education, skills, and proudest project.
""",
        },
        {
            "title": "Data Structures & Algorithms Placement Cheatsheet",
            "slug": "dsa-placement-cheatsheet",
            "category": "dsa",
            "content_type": "cheatsheet",
            "description": "Quick reference for Big-O complexities, common algorithmic patterns, and key data structure templates.",
            "company_tag": "Amazon",
            "difficulty": "intermediate",
            "estimated_read_time": "15 mins",
            "tags": ["DSA", "Big-O", "Algorithms", "Coding Round"],
            "order_index": 2,
            "content": """# Data Structures & Algorithms Placement Cheatsheet

### ⚡ Time & Space Complexity Master Table

| Data Structure | Access | Search | Insertion | Deletion | Space |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Array** | O(1) | O(N) | O(N) | O(N) | O(N) |
| **Hash Table** | N/A | O(1) avg / O(N) | O(1) avg / O(N) | O(1) avg / O(N) | O(N) |
| **Singly Linked List**| O(N) | O(N) | O(1) (head) | O(N) | O(N) |
| **Binary Search Tree**| O(log N) | O(log N) | O(log N) | O(log N) | O(N) |
| **Skewed BST** | O(N) | O(N) | O(N) | O(N) | O(N) |
| **Heap (Min/Max)** | O(1) (top) | O(N) | O(log N) | O(log N) | O(N) |

---

### 🧩 Top 6 Problem-Solving Patterns

1. **Two Pointers**: Used on sorted arrays (e.g., Two Sum II, Trapping Rain Water, Palindrome checks).
2. **Sliding Window**: Subarray/substring optimization (e.g., Longest Substring Without Repeating Characters).
3. **Fast & Slow Pointer (Hare & Tortoise)**: Cycle detection in Linked Lists and finding the middle element.
4. **Binary Search**: Any monotonic search space, finding square root, peak element.
5. **Breadth-First Search (BFS)**: Shortest path in unweighted graphs or level-order tree traversal.
6. **Depth-First Search (DFS)**: Connected components, topological sort, backtracking (Subsets, Permutations).
""",
        },
        {
            "title": "SQL & DBMS Interview Mastery Guide",
            "slug": "sql-dbms-interview-guide",
            "category": "core_cs",
            "content_type": "cheatsheet",
            "description": "Must-know SQL queries, Indexing, ACID transactions, Normalization, and frequently asked interview questions.",
            "company_tag": "TCS",
            "difficulty": "intermediate",
            "estimated_read_time": "10 mins",
            "tags": ["SQL", "DBMS", "Core CS", "Database"],
            "order_index": 3,
            "content": """# SQL & DBMS Interview Mastery Guide

### 📌 Most Asked SQL Query Templates

#### 1. Find the N-th Highest Salary
```sql
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank = 2; -- Change to N
```

#### 2. Find Duplicate Records in a Table
```sql
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

#### 3. Delete Duplicate Records (Keeping Lowest ID)
```sql
DELETE FROM users
WHERE id NOT IN (
    SELECT MIN(id)
    FROM users
    GROUP BY email
);
```

---

### 🔑 Core DBMS Principles for Freshers

* **ACID Properties**:
  * **Atomicity**: All or nothing transaction.
  * **Consistency**: DB remains in a valid state following all constraints.
  * **Isolation**: Concurrent transactions don't interfere with each other.
  * **Durability**: Committed data is persisted even during system crashes.
* **Indexing**: B-Trees/B+ Trees allow O(log N) lookup. Primary indexes are clustered; secondary indexes are non-clustered.
* **Normalization**: 1NF (atomic values) $\to$ 2NF (no partial dependency) $\to$ 3NF (no transitive dependency) $\to$ BCNF.
""",
        },
        {
            "title": "Top 50 Behavioral & HR Interview Questions (STAR Method)",
            "slug": "top-50-hr-behavioral-interview-questions",
            "category": "interview_prep",
            "content_type": "guide",
            "description": "How to answer 'Tell me about yourself', conflict resolution, leadership scenarios, and strengths/weaknesses.",
            "company_tag": "General",
            "difficulty": "beginner",
            "estimated_read_time": "10 mins",
            "tags": ["HR", "Behavioral", "STAR Method", "Interview Tips"],
            "order_index": 4,
            "content": """# Top Behavioral & HR Interview Questions

### ⭐ The STAR Method Framework
When answering behavioral questions, structure your answers in 4 parts:
* **Situation (S)**: Briefly set the scene (course project, hackathon, internship).
* **Task (T)**: What was the specific problem or goal?
* **Action (A)**: What specific steps did YOU take? (Focus on your contribution).
* **Result (R)**: What was the quantifiable outcome? (e.g. improved speed by 30%, delivered on time).

---

### 💬 Top 5 Questions & Winning Responses

#### 1. "Tell me about yourself."
* **Formula**: Past (Degree, college) + Present (Skills, recent capstone project) + Future (Why this company and role). Keep it under 90 seconds!

#### 2. "What are your greatest strengths and weaknesses?"
* **Strength**: Pick a relevant technical/analytical strength with a short example.
* **Weakness**: Pick a real, non-fatal area (e.g., public speaking or saying yes to too many tasks) and explain the active steps you are taking to improve.

#### 3. "Tell me about a time you faced a disagreement in a team project."
* Use STAR: Focus on active listening, data-driven compromise, and delivering the project successfully.

#### 4. "Why should we hire you over other candidates?"
* Focus on your blend of strong fundamental preparation, high adaptability, problem-solving discipline, and enthusiasm to contribute from day one.
""",
        },
        {
            "title": "Java Core & OOPs Placement Master Guide",
            "slug": "java-core-placement-guide",
            "category": "programming",
            "content_type": "guide",
            "description": "Comprehensive reference for Core Java, OOP principles, Collections Framework, Multithreading, and JVM internals.",
            "company_tag": "TCS",
            "difficulty": "intermediate",
            "estimated_read_time": "15 mins",
            "tags": ["Java", "OOP", "Collections", "Multithreading", "Placement"],
            "order_index": 5,
            "content": """# Java Core & OOPs Placement Master Guide

Java remains one of the most widely tested programming languages in college placement exams and technical interviews.

---

### ☕ 1. Four Pillars of OOP in Java

1. **Encapsulation**: Bundling fields and methods within classes and restricting direct access via private fields with public getters/setters.
2. **Inheritance**: Code reusability via the `extends` keyword. Java does *not* support multiple class inheritance to avoid the diamond problem; multiple interface implementation is used instead.
3. **Polymorphism**:
   - **Compile-time (Static)**: Method Overloading (same method name, different parameter types or counts).
   - **Runtime (Dynamic)**: Method Overriding (subclass provides specific implementation of parent method with `@Override`).
4. **Abstraction**: Hiding implementation details using `abstract` classes (can have constructors and state) and `interface` (contracts, default/static methods in Java 8+).

---

### 📦 2. Collections Framework Cheat Sheet

| Interface | Implementations | Key Characteristics |
| :--- | :--- | :--- |
| **List** | `ArrayList`, `LinkedList`, `Vector` | Ordered, allows duplicates. ArrayList is $O(1)$ random access, LinkedList is $O(1)$ head/tail insertion. |
| **Set** | `HashSet`, `LinkedHashSet`, `TreeSet` | Unique elements. `HashSet` uses hashing ($O(1)$), `TreeSet` uses Red-Black Tree (sorted, $O(\\log N)$). |
| **Map** | `HashMap`, `LinkedHashMap`, `TreeMap` | Key-value pairs. `HashMap` allows 1 null key, `ConcurrentHashMap` provides thread-safety without locking the entire map. |
| **Queue** | `PriorityQueue`, `ArrayDeque` | `PriorityQueue` implements a min-heap by default. `ArrayDeque` is faster than `Stack` for LIFO operations. |

#### Internal Working of HashMap:
- Based on an array of Node buckets: `hash(key) & (n - 1)`.
- Collisions handled via LinkedList; when bucket length exceeds threshold 8 and table capacity $\\ge 64$, bucket converts to a balanced Red-Black Tree ($O(\\log N)$).

---

### 🧵 3. Multithreading & Concurrency Essentials

- **Thread Creation**: Extend `Thread` or implement `Runnable` / `Callable<V>`. Implementing `Runnable` is preferred to allow extending other classes.
- **Synchronization**: `synchronized` keyword locks on object monitor. `ReentrantLock` allows fairness policies and timed lock acquisition.
- **Volatile Keyword**: Guarantees visibility of variable modifications across threads without caching in CPU registers, but does not guarantee compound atomicity.
- **ExecutorService**: Thread pooling via `Executors.newFixedThreadPool(n)` avoids overhead of recreating OS threads.

---

### 💡 4. Top 5 Java Placement Interview Questions

1. **Difference between `==` and `.equals()`?**
   - `==` compares reference equality (memory addresses), while `.equals()` compares value content (when overridden).
2. **Why is String immutable in Java?**
   - Security (used in network/DB connections), Thread safety, and Caching in String Constant Pool (SCP).
3. **Final vs Finally vs Finalize?**
   - `final`: keyword for constant variables, non-overridable methods, or non-inheritable classes.
   - `finally`: block following `try-catch` that executes regardless of whether an exception was thrown.
   - `finalize()`: deprecated cleanup method called by Garbage Collector before reclaiming memory.
""",
        },
        {
            "title": "Python for Placements & Coding Rounds Master Guide",
            "slug": "python-placement-master-guide",
            "category": "programming",
            "content_type": "guide",
            "description": "Essential Python idioms, Built-in Data Structures, Memory Management, Generators, Decorators, and Coding interview patterns.",
            "company_tag": "Amazon",
            "difficulty": "intermediate",
            "estimated_read_time": "14 mins",
            "tags": ["Python", "Comprehensions", "OOP", "Placement", "Coding"],
            "order_index": 6,
            "content": """# Python for Placements & Coding Rounds Master Guide

Python is renowned for high developer productivity and concise syntax, making it the top choice for campus coding assessments.

---

### 🐍 1. Built-in Data Structures & Time Complexities

| Type | Mutability | Lookup | Append / Add | Deletion |
| :--- | :--- | :--- | :--- | :--- |
| `list` | Mutable | $O(1)$ index, $O(N)$ search | $O(1)$ amortized append | $O(N)$ pop(0), $O(1)$ pop() |
| `tuple` | Immutable | $O(1)$ index, $O(N)$ search | N/A | N/A |
| `dict` | Mutable | $O(1)$ average | $O(1)$ average | $O(1)$ average |
| `set` | Mutable | $O(1)$ average | $O(1)$ average | $O(1)$ average |
| `deque` | Mutable | $O(N)$ random | $O(1)$ append / appendleft | $O(1)$ pop / popleft |

---

### ⚡ 2. Pythonic Idioms for Timed Coding Rounds

#### List & Dict Comprehensions:
```python
# Filter and transform in one step
even_squares = [x**2 for x in range(20) if x % 2 == 0]

# Frequency counter in dict
freq = {ch: text.count(ch) for ch in set(text)}
```

#### Min & Max Heaps with `heapq`:
```python
import heapq
# By default, heapq is a MIN-HEAP
min_heap = []
heapq.heappush(min_heap, 10)
val = heapq.heappop(min_heap)

# For MAX-HEAP, negate values:
heapq.heappush(min_heap, -val)
```

#### Generators & Yield:
- Generators do not hold the entire dataset in memory; they yield elements lazily on demand, reducing memory overhead to $O(1)$.

---

### 🧠 3. Advanced Python Concepts Tested in Technical Interviews

- **GIL (Global Interpreter Lock)**: A mutex that prevents multiple native threads from executing Python bytecodes simultaneously in CPython. For CPU-bound tasks, use `multiprocessing`; for I/O-bound tasks, use `threading` or `asyncio`.
- **Decorators**: Functions that take another function as argument and extend its behavior without modifying it:
```python
def benchmark(func):
    import time
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter()-t0:.4f}s")
        return res
    return wrapper
```
- **Shallow Copy vs Deep Copy**:
  - `copy.copy()`: Creates a new compound object and inserts references to existing inner objects.
  - `copy.deepcopy()`: Recursively duplicates inner objects as well.
""",
        },
        {
            "title": "Quantitative Aptitude Formulas & Speed Math Guide",
            "slug": "quantitative-aptitude-formulas-guide",
            "category": "aptitude",
            "content_type": "guide",
            "description": "Core shortcut formulas, mental math techniques, percentages, profit-loss, work-time, and speed-distance rules for placement exams.",
            "company_tag": "TCS",
            "difficulty": "beginner",
            "estimated_read_time": "12 mins",
            "tags": ["Quantitative Aptitude", "Aptitude", "Speed Math", "Formulas", "Placement"],
            "order_index": 7,
            "content": """# Quantitative Aptitude Formulas & Speed Math Guide

In 30-second-per-question placement tests, mental math and shortcut formulas are your greatest competitive advantage.

---

### 📐 1. Master Formula Table

#### 1. Percentages & Fractions Equivalents:
- $1/2 = 50\\%, \\quad 1/3 = 33.33\\%, \\quad 1/4 = 25\\%, \\quad 1/5 = 20\\%$
- $1/6 = 16.67\\%, \\quad 1/7 = 14.28\\%, \\quad 1/8 = 12.5\\%, \\quad 1/9 = 11.11\\%$
- **Net Successive Percentage Change**:
  $$\\text{Net Change} = x + y + \\frac{xy}{100}\\%$$

#### 2. Profit and Loss:
- $\\text{Profit} = SP - CP, \\quad \\text{Loss} = CP - SP$
- $\\text{Profit}\\% = \\frac{\\text{Profit}}{CP} \\times 100$
- $SP = CP \\times \\left(1 + \\frac{\\text{Profit}\\%}{100}\\right)$
- $\\text{Discount} = MP - SP, \\quad SP = MP \\times \\left(1 - \\frac{\\text{Discount}\\%}{100}\\right)$

#### 3. Time, Speed and Distance:
- $\\text{Speed} = \\frac{\\text{Distance}}{\\text{Time}}$
- **Conversion**: $1 \\text{ km/h} = \\frac{5}{18} \\text{ m/s}, \\quad 1 \\text{ m/s} = \\frac{18}{5} \\text{ km/h}$
- **Average Speed** for equal distances with speeds $u$ and $v$:
  $$\\text{Average Speed} = \\frac{2uv}{u + v}$$
- **Relative Speed**:
  - Same Direction: $|u - v|$
  - Opposite Direction: $u + v$

#### 4. Time and Work:
- If A completes work in $x$ days, A's 1-day work $= 1/x$.
- Together, A and B finish in:
  $$\\text{Total Days} = \\frac{xy}{x + y}$$
- **LCM Method**: Assume total work is the LCM of individual days, then solve using daily units produced.

#### 5. Probability & Permutations:
- $P(E) = \\frac{\\text{Favorable Outcomes}}{\\text{Total Possible Outcomes}}$
- Permutation (Arrangement matters): $^nP_r = \\frac{n!}{(n - r)!}$
- Combination (Selection only): $^nC_r = \\frac{n!}{r!(n - r)!}$
""",
        },
        {
            "title": "Logical Reasoning & Analytical Puzzles Guide",
            "slug": "logical-reasoning-puzzles-guide",
            "category": "aptitude",
            "content_type": "guide",
            "description": "Step-by-step techniques for Syllogisms, Seating Arrangements, Blood Relations, Direction Sense, and Coding-Decoding.",
            "company_tag": "Infosys",
            "difficulty": "intermediate",
            "estimated_read_time": "12 mins",
            "tags": ["Logical Reasoning", "Reasoning", "Syllogisms", "Puzzles", "Placement"],
            "order_index": 8,
            "content": """# Logical Reasoning & Analytical Puzzles Guide

Logical reasoning tests your deductive ability, structural thinking, and speed under time pressure.

---

### 🧩 1. Syllogisms via Venn Diagrams

Standard Syllogism Propositions:
1. **Universal Affirmative (A)**: *All A are B* $\\implies$ Circle A is completely inside Circle B.
2. **Universal Negative (E)**: *No A are B* $\\implies$ Circle A and Circle B do not touch.
3. **Particular Affirmative (I)**: *Some A are B* $\\implies$ Circle A and Circle B overlap.
4. **Particular Negative (O)**: *Some A are not B* $\\implies$ At least one part of A is outside B.

#### Complementary Pairs (Either-Or Conditions):
Two conclusions form an 'Either I or II follows' pair if:
1. Both individual conclusions are doubtful/false independently.
2. One conclusion is affirmative and one is negative.
3. Both have identical subject and predicate (e.g., Some A are B and No A are B).

---

### 👥 2. Blood Relations Mapping Protocol

Always draw a family tree using clear standard symbols:
- **Male**: $\\square$ or $[+]$
- **Female**: $\\bigcirc$ or $[-]$
- **Marriage**: Double horizontal line ($=$)
- **Siblings**: Single horizontal line ($-$)
- **Generations**: Vertical lines connecting down

---

### 🧭 3. Direction Sense Tricks

- Always orient: **North (Up)**, **South (Down)**, **East (Right)**, **West (Left)**.
- Turning **Right** from North goes East; turning **Left** goes West.
- Shortest distance between starting and ending points uses Pythagoras Theorem:
  $$D = \\sqrt{\\Delta x^2 + \\Delta y^2}$$
- **Shadow Rules**:
  - At **Sunrise**: Sun is in East $\\implies$ Shadow falls in **West**.
  - At **Sunset**: Sun is in West $\\implies$ Shadow falls in **East**.
""",
        },
        {
            "title": "Operating Systems (OS) Core Placement Cheatsheet",
            "slug": "os-concepts-cheatsheet",
            "category": "core_cs",
            "content_type": "cheatsheet",
            "description": "Essential OS interview questions: Processes vs Threads, CPU Scheduling, Deadlocks, Banker's Algorithm, Virtual Memory, and Paging.",
            "company_tag": "Amazon",
            "difficulty": "intermediate",
            "estimated_read_time": "12 mins",
            "tags": ["Operating Systems", "OS", "Processes", "Deadlocks", "Virtual Memory", "Placement"],
            "order_index": 9,
            "content": """# Operating Systems (OS) Core Placement Cheatsheet

---

### ⚙️ 1. Process vs Thread

| Feature | Process | Thread |
| :--- | :--- | :--- |
| **Definition** | Program in execution (heavyweight) | Basic unit of CPU execution (lightweight) |
| **Memory** | Has isolated address space | Shares code, data, and files with peer threads |
| **Context Switch**| Slower, requires flushing cache | Fast, changes program counter and registers only |
| **Communication** | IPC (Pipes, Sockets, Shared Memory) | Directly shares global variables / memory |

---

### 🔒 2. Deadlocks & Banker's Algorithm

#### Coffman's 4 Conditions for Deadlock:
1. **Mutual Exclusion**: At least one resource must be non-shareable.
2. **Hold and Wait**: Process holds one resource while waiting for another.
3. **No Preemption**: Resources cannot be forcibly seized from a process.
4. **Circular Wait**: $P_0$ waits for $P_1$, $P_1$ waits for $P_2$, ..., $P_n$ waits for $P_0$.

#### Deadlock Handling:
- **Prevention**: Invalidate at least one Coffman condition (e.g., resource ordering).
- **Avoidance**: Use **Banker's Algorithm** to verify that state remains safe:
  $$\\text{Need} = \\text{Max} - \\text{Allocation}$$
- **Detection & Recovery**: Terminate deadlocked processes or preempt resources.

---

### 📄 3. Virtual Memory & Paging

- **Page**: Fixed-size block of logical memory.
- **Frame**: Fixed-size block of physical RAM.
- **Page Fault**: Occurs when a program accesses a page not currently in physical RAM, triggering disk I/O.
- **TLB (Translation Lookaside Buffer)**: High-speed hardware cache for page table lookups.
- **Page Replacement Algorithms**:
  - **FIFO**: Suffers from Belady's Anomaly (more frames can lead to more page faults).
  - **LRU (Least Recently Used)**: Optimal approximation, implemented via doubly-linked list & hash map.
  - **Optimal (OPT)**: Replaces page that will not be used for longest time in future (theoretical benchmark).
""",
        },
        {
            "title": "Computer Networks Protocols & Placement Guide",
            "slug": "computer-networks-guide",
            "category": "core_cs",
            "content_type": "guide",
            "description": "OSI 7-Layer Model, TCP vs UDP, IP Addressing, Subnetting, DNS, HTTP vs HTTPS, and Socket programming essentials.",
            "company_tag": "TCS",
            "difficulty": "intermediate",
            "estimated_read_time": "12 mins",
            "tags": ["Computer Networks", "Networks", "TCP/IP", "OSI Model", "HTTP", "Placement"],
            "order_index": 10,
            "content": """# Computer Networks Protocols & Placement Guide

---

### 🌐 1. OSI 7-Layer Model vs TCP/IP

| Layer | Protocol Examples | PDU (Data Unit) | Responsibilities |
| :--- | :--- | :--- | :--- |
| **7. Application** | HTTP, HTTPS, FTP, DNS, SMTP | Data | User interface & network services |
| **6. Presentation**| TLS/SSL, JPEG, ASCII | Data | Encryption, compression, data format |
| **5. Session** | RPC, NetBIOS | Data | Session establishment and termination |
| **4. Transport** | TCP, UDP | Segment | End-to-end reliability, port addressing |
| **3. Network** | IPv4, IPv6, ICMP, ARP | Packet | Logical addressing & IP routing |
| **2. Data Link** | Ethernet, MAC, Wi-Fi | Frame | Physical addressing (MAC), error checking |
| **1. Physical** | Cables, Fiber, Hubs | Bit | Electrical/optical transmission |

---

### ⚡ 2. TCP vs UDP Master Comparison

- **TCP (Transmission Control Protocol)**:
  - Connection-oriented with **3-way handshake** (`SYN` $\\to$ `SYN-ACK` $\\to$ `ACK`).
  - Guarantees ordered, reliable delivery, error checking, flow control (Sliding Window), and congestion control.
  - Used in: Web browsing (HTTP/HTTPS), file transfer (FTP), email (SMTP).
- **UDP (User Datagram Protocol)**:
  - Connectionless, lightweight, low-latency, no retransmission of dropped packets.
  - Used in: Video streaming (VoIP, YouTube live), online gaming, DNS queries.

---

### 🔒 3. What happens when you type `https://google.com` in your browser?

1. **DNS Lookup**: Browser checks cache $\\to$ OS cache $\\to$ Router $\\to$ Recursive Resolver $\\to$ Root/TLD servers to resolve IP.
2. **TCP 3-Way Handshake**: Client sends `SYN`, server responds with `SYN-ACK`, client returns `ACK`.
3. **TLS/SSL Handshake**: Negotiates encryption cipher, verifies server certificate, exchanges session key.
4. **HTTP GET Request**: Browser requests index HTML.
5. **Server Processing & Response**: Server returns `200 OK` with HTML, CSS, and JS bundles.
6. **DOM Rendering**: Browser engine parses HTML, constructs DOM tree, and paints page.
""",
        },
        {
            "title": "Artificial Intelligence & Machine Learning (AI / ML) Placement Guide",
            "slug": "ai-machine-learning-guide",
            "category": "ai_ml",
            "content_type": "guide",
            "description": "Supervised vs Unsupervised ML, Neural Networks, Transformers & LLMs, PyTorch, and Model Evaluation metrics.",
            "company_tag": "Google",
            "difficulty": "intermediate",
            "estimated_read_time": "15 mins",
            "tags": ["Artificial Intelligence", "Machine Learning", "AI", "Deep Learning", "LLMs", "Placement"],
            "order_index": 11,
            "content": """# Artificial Intelligence & Machine Learning (AI / ML) Placement Guide

AI and Machine Learning skills are in massive demand across campus recruitment drives and product engineering roles.

---

### 🤖 1. Supervised vs Unsupervised vs Reinforcement Learning

| Paradigm | Training Data | Core Goal | Classic Algorithms |
| :--- | :--- | :--- | :--- |
| **Supervised** | Labeled $(X, y)$ | Predict target output for unseen inputs | Linear Regression, Logistic Regression, Random Forest, XGBoost |
| **Unsupervised** | Unlabeled $(X)$ | Discover latent structure, clusters, or patterns | K-Means, PCA (Principal Component Analysis), DBSCAN |
| **Reinforcement** | Environment states & rewards | Learn optimal policy via action-reward loops | Q-Learning, PPO, Deep Q-Networks (DQN) |

---

### 📊 2. Model Evaluation Metrics

- **Accuracy**: $\\frac{TP + TN}{TP + TN + FP + FN}$ (Misleading for imbalanced datasets).
- **Precision**: $\\frac{TP}{TP + FP}$ (Cost of false alarm is high, e.g. spam detection).
- **Recall (Sensitivity)**: $\\frac{TP}{TP + FN}$ (Cost of missing a positive is severe, e.g. cancer/fraud detection).
- **F1 Score**: Harmonic mean of Precision & Recall: $2 \\times \\frac{P \\times R}{P + R}$.
- **ROC-AUC**: Evaluates classification threshold trade-offs across TPR vs FPR.

---

### 🧠 3. Neural Networks & Transformer Architecture

- **Backpropagation**: Calculates gradient of loss function with respect to weights using chain rule:
  $$\\frac{\\partial L}{\\partial W^{[l]}} = \\frac{\\partial L}{\\partial A^{[l]}} \\times \\frac{\\partial A^{[l]}}{\\partial Z^{[l]}} \\times \\frac{\\partial Z^{[l]}}{\\partial W^{[l]}}$$
- **Activation Functions**:
  - **ReLU**: $f(x) = \\max(0, x)$ — prevents vanishing gradients in deep networks.
  - **Softmax**: Converts logits into normalized probability distribution: $\\sigma(z)_i = \\frac{e^{z_i}}{\\sum e^{z_j}}$.
- **Transformers & Self-Attention**:
  $$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$
  Powers modern LLMs by computing context-aware token representations in parallel.

---

### 💡 4. Top AI/ML Placement Interview Questions

1. **How do you combat Overfitting?**
   - L1/L2 regularization, Dropout (random neuron deactivation), early stopping, and data augmentation.
2. **What is the difference between Generative vs Discriminative models?**
   - Discriminative models model $P(Y|X)$ (decision boundary), while Generative models model $P(X, Y)$ or $P(X)$ to generate synthetic data.
3. **What is Prompt Engineering & Retrieval-Augmented Generation (RAG)?**
   - RAG combines vector database embeddings (semantic search) with an LLM prompt to ground answers with verified private data without fine-tuning.
""",
        },
        {
            "title": "Data Engineering & Big Data Architecture Placement Guide",
            "slug": "data-engineering-big-data-guide",
            "category": "data_engineering",
            "content_type": "guide",
            "description": "ETL/ELT data pipelines, Apache Spark, Apache Kafka event streaming, Star vs Snowflake Schema, and Data Lakes.",
            "company_tag": "Amazon",
            "difficulty": "intermediate",
            "estimated_read_time": "14 mins",
            "tags": ["Data Engineering", "Big Data", "Spark", "Kafka", "ETL", "Placement"],
            "order_index": 12,
            "content": """# Data Engineering & Big Data Architecture Placement Guide

Data Engineering bridges software engineering and analytics, powering enterprise decision-making at scale.

---

### 🌊 1. Batch vs Stream Processing

- **Batch Processing**: Operates on large, bounded historical datasets (e.g. nightly reports via Apache Spark, Hadoop MapReduce). High throughput, higher latency.
- **Stream Processing**: Operates on unbounded, real-time event streams (e.g. Kafka, Apache Flink, Spark Streaming). Ultra-low latency (milliseconds).

---

### ⚡ 2. Apache Spark Core Architecture

- **Driver & Executors**: The Driver converts code into a Directed Acyclic Graph (DAG) and schedules tasks across worker Executor nodes.
- **Transformations vs Actions**:
  - **Transformations (Lazy)**: `map()`, `filter()`, `select()`, `groupBy()` — return new DataFrame/RDD without computing.
  - **Actions (Eager)**: `count()`, `collect()`, `write()`, `show()` — triggers cluster execution of the DAG.
- **Narrow vs Wide Dependencies**:
  - Narrow: Each parent partition used by at most 1 child partition (no shuffle, e.g. `map()`).
  - Wide: Multiple child partitions depend on data across parent partitions (triggers expensive network **Shuffle**, e.g. `groupByKey()`).

---

### 📬 3. Apache Kafka Event Streaming

- **Topics & Partitions**: A Topic is split into Partitions for parallel writes and reads across broker nodes.
- **Producer / Consumer Groups**: Each partition is read by exactly one consumer within a Consumer Group, guaranteeing horizontal scale with ordered consumption.
- **Retention**: Persistent, disk-backed commit log with configurable retention time or size.

---

### 🏗️ 4. Data Warehousing & Schema Design

- **Star Schema**: Denormalized dimension tables surrounding a central Fact table. Faster queries, fewer JOINs.
- **Snowflake Schema**: Normalized dimension tables. Saves disk space, but requires multi-table JOINs.
- **ETL vs ELT**: Modern cloud data warehouses (Snowflake, BigQuery, Databricks) prefer ELT: extract and load raw data into cloud storage, then transform using warehouse compute power.
""",
        },
        {
            "title": "Cloud Computing & Architecture (AWS / Azure / GCP) Placement Guide",
            "slug": "cloud-computing-architecture-guide",
            "category": "cloud_devops",
            "content_type": "guide",
            "description": "AWS core primitives, Serverless architecture, Kubernetes container orchestration, Microservices, and Terraform IaC.",
            "company_tag": "Microsoft",
            "difficulty": "intermediate",
            "estimated_read_time": "15 mins",
            "tags": ["Cloud Computing", "AWS", "Kubernetes", "DevOps", "Serverless", "Placement"],
            "order_index": 13,
            "content": """# Cloud Computing & Architecture Placement Guide

Modern software runs on the cloud. Tech recruiters test your understanding of distributed infrastructure, serverless, and containers.

---

### ☁️ 1. Cloud Service Models (IaaS vs PaaS vs SaaS)

- **IaaS (Infrastructure as a Service)**: AWS EC2, GCP Compute Engine, Azure VMs. You manage OS, runtime, and app.
- **PaaS (Platform as a Service)**: AWS Elastic Beanstalk, Heroku, Railway, Render. Provider manages OS/runtime; you deploy code.
- **SaaS (Software as a Service)**: Salesforce, Google Workspace, Slack. End-user software.
- **FaaS (Function as a Service / Serverless)**: AWS Lambda, Cloud Functions. Event-driven, pay-per-millisecond, zero idle cost.

---

### 🐳 2. Containers vs Virtual Machines & Kubernetes

- **VM**: Emulates hardware, runs guest OS kernel (heavyweight, minutes to boot).
- **Container (Docker)**: Shares host OS kernel, isolates via Linux cgroups and namespaces (lightweight, megabytes in size, boots in milliseconds).
- **Kubernetes (K8s)**:
  - **Pod**: Smallest deployable unit (1 or more containers).
  - **Deployment**: Declarative replica management with rolling zero-downtime updates.
  - **Service**: Stable virtual IP and load-balancing abstraction in front of ephemeral pods (`ClusterIP`, `NodePort`, `LoadBalancer`).

---

### 🛡️ 3. High Availability, Fault Tolerance & Terraform

- **High Availability (HA)**: Multi-AZ (Availability Zone) deployment with automated Application Load Balancer (ALB) health checks.
- **Auto-Scaling**: Dynamically adjusts instance counts based on CPU utilization or request queue depth.
- **Infrastructure as Code (IaC)**: Tools like **Terraform** enable provisioning reproducible, version-controlled cloud infrastructure across AWS, Azure, and GCP.
""",
        },
    ]

    existing_slugs = {m.slug for m in db.query(StudyMaterial.slug).all()}
    for md in materials_data:
        if md["slug"] in existing_slugs:
            continue
        mat = StudyMaterial(
            title=md["title"],
            slug=md["slug"],
            category=md["category"],
            content_type=md["content_type"],
            description=md["description"],
            content_markdown=md["content"],
            company_tag=md["company_tag"],
            difficulty=md["difficulty"],
            estimated_read_time=md["estimated_read_time"],
            tags_json=json.dumps(md["tags"]),
            order_index=md["order_index"],
        )
        db.add(mat)
    db.flush()


def _seed_roadmaps(db: Session) -> None:
    roadmaps_data = [
        {
            "title": "Campus Placement 60-Day Sprint (Comprehensive)",
            "slug": "campus-60-day-sprint",
            "role_target": "Software Engineer / Technical Consultant / SDE-1",
            "description": "Complete 12-week end-to-end curriculum covering Quantitative Aptitude, Logical Reasoning, Verbal Ability, Coding (DSA), SQL, DBMS, Operating Systems, Computer Networks, OOP, and Company Mock Drives.",
            "icon": "🚀",
            "estimated_weeks": 12,
            "milestones": [
                {
                    "id": "m1",
                    "week": 1,
                    "title": "Week 1: Quantitative Aptitude Essentials",
                    "subject": "Quantitative Aptitude",
                    "icon": "📊",
                    "description": "Master foundational numerical aptitude required for corporate placement exams.",
                    "topics": ["Percentages", "Profit and Loss", "Ratios and Proportions", "Averages"],
                    "subtopics": [
                        "Percentage Calculations & Successive Percentage Changes",
                        "Cost Price, Selling Price & Marked Price Discounts",
                        "Ratios, Proportions & Partnership Distributions",
                        "Weighted Averages & Mixture Alligations",
                        "Shortcuts for Campus Placement Aptitude Tests"
                    ],
                    "practice_questions": [
                        {
                            "id": "m1-q1",
                            "question": "A product costs ₹800. Its price increases by 15%. What is the new selling price?",
                            "options": ["₹880", "₹900", "₹920", "₹940"],
                            "correct_option_index": 2,
                            "explanation": "15% of ₹800 = (15/100) × 800 = ₹120. New price = ₹800 + ₹120 = ₹920.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m1-q2",
                            "question": "A merchant buys an article for ₹1,200 and sells it at a profit of 20%. What is the selling price?",
                            "options": ["₹1,440", "₹1,400", "₹1,380", "₹1,500"],
                            "correct_option_index": 0,
                            "explanation": "Profit = 20% of ₹1,200 = ₹240. Selling Price = ₹1,200 + ₹240 = ₹1,440.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m1-q3",
                            "question": "Divide ₹7,200 among A, B, and C in the ratio 5:3:1. What is A's share?",
                            "options": ["₹3,600", "₹4,000", "₹4,200", "₹4,500"],
                            "correct_option_index": 1,
                            "explanation": "Total ratio units = 5 + 3 + 1 = 9. Value of 1 unit = ₹7,200 / 9 = ₹800. A's share = 5 × ₹800 = ₹4,000.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m1-q4",
                            "question": "The average of 5 numbers is 28. If a new number 40 is included, what is the new average of the 6 numbers?",
                            "options": ["29", "30", "31", "32"],
                            "correct_option_index": 1,
                            "explanation": "Sum of 5 numbers = 5 × 28 = 140. New sum with 40 = 140 + 40 = 180. New average = 180 / 6 = 30.",
                            "difficulty": "medium",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "quantitative-aptitude",
                    "estimated_hours": 10
                },
                {
                    "id": "m2",
                    "week": 2,
                    "title": "Week 2: Advanced Quantitative Aptitude",
                    "subject": "Quantitative Aptitude",
                    "icon": "⏱️",
                    "description": "Crack rate, speed, interest, and combinatorics problems tested in top tier tech assessments.",
                    "topics": ["Time and Work", "Speed, Time and Distance", "Simple and Compound Interest", "Probability"],
                    "subtopics": [
                        "Work Rate Formula, Alternating Workers & Efficiency Ratios",
                        "Pipes and Cisterns (Inlet vs Drain rates)",
                        "Relative Speed, Train Crossing Stationary & Moving Objects",
                        "Compound Interest Compounded Annually vs Semi-Annually",
                        "Dice, Cards and Urn Probability Problems"
                    ],
                    "practice_questions": [
                        {
                            "id": "m2-q1",
                            "question": "Person A completes a work in 12 days and Person B in 24 days. Working together, how many days will they take?",
                            "options": ["6 days", "8 days", "9 days", "10 days"],
                            "correct_option_index": 1,
                            "explanation": "Combined work rate = 1/12 + 1/24 = 3/24 = 1/8 work per day. Total time = 8 days.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m2-q2",
                            "question": "A train 150 meters long traveling at 54 km/h passes a telegraph pole. How many seconds does it take?",
                            "options": ["8 seconds", "10 seconds", "12 seconds", "15 seconds"],
                            "correct_option_index": 1,
                            "explanation": "Speed = 54 × (5/18) = 15 m/s. Time to cross pole = Distance / Speed = 150 / 15 = 10 seconds.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m2-q3",
                            "question": "What is the Compound Interest on ₹5,000 for 2 years at 10% per annum compounded annually?",
                            "options": ["₹1,000", "₹1,050", "₹1,100", "₹1,150"],
                            "correct_option_index": 1,
                            "explanation": "Amount = 5,000 × (1.10)^2 = 5,000 × 1.21 = ₹6,050. CI = ₹6,050 - ₹5,000 = ₹1,050.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m2-q4",
                            "question": "Two fair dice are rolled simultaneously. What is the probability that the sum of the numbers is 8?",
                            "options": ["1/6", "5/36", "7/36", "1/9"],
                            "correct_option_index": 1,
                            "explanation": "Total outcomes = 36. Favorable outcomes for sum=8: (2,6), (3,5), (4,4), (5,3), (6,2) -> 5 outcomes. Probability = 5/36.",
                            "difficulty": "hard",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "quantitative-aptitude",
                    "estimated_hours": 12
                },
                {
                    "id": "m3",
                    "week": 3,
                    "title": "Week 3: Logical Reasoning & Analytical Deduction",
                    "subject": "Logical Reasoning",
                    "icon": "🧩",
                    "description": "Master sequence identification, coding patterns, family trees, and spatial orientation.",
                    "topics": ["Number Series", "Coding-Decoding", "Blood Relations", "Direction Sense"],
                    "subtopics": [
                        "Arithmetic, Geometric & Multi-step Pattern Sequences",
                        "Letter Shifting, Reverse Alphabet & Matrix Coding",
                        "Generation Trees & Coded Blood Relations (A+B, A-B)",
                        "Direction Sense with Compass Angles & Pythagoras Distance",
                        "Clocks & Calendars Angle & Day Calculation"
                    ],
                    "practice_questions": [
                        {
                            "id": "m3-q1",
                            "question": "Find the missing number in the sequence: 4, 9, 19, 39, 79, ?",
                            "options": ["149", "159", "169", "179"],
                            "correct_option_index": 1,
                            "explanation": "The pattern is (x × 2) + 1. 4×2+1=9, 9×2+1=19, 19×2+1=39, 39×2+1=79, 79×2+1 = 159.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m3-q2",
                            "question": "If CLOUD is coded as ENQWF (+2 to each letter), how is RAIN coded in the same system?",
                            "options": ["TCKP", "SBJO", "SZHM", "TBKP"],
                            "correct_option_index": 0,
                            "explanation": "R(+2) = T, A(+2) = C, I(+2) = K, N(+2) = P. Code is TCKP.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m3-q3",
                            "question": "Pointing to a photograph, Amit said: 'She is the only daughter of my paternal grandfather's only son.' Who is she to Amit?",
                            "options": ["Mother", "Sister", "Cousin", "Aunt"],
                            "correct_option_index": 1,
                            "explanation": "Amit's paternal grandfather's only son is Amit's father. The only daughter of Amit's father is Amit's sister.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m3-q4",
                            "question": "Rahul walks 20m North, turns right and walks 15m, then turns right and walks 20m. How far is he from his starting point?",
                            "options": ["10m East", "15m East", "20m West", "15m West"],
                            "correct_option_index": 1,
                            "explanation": "Walking 20m North and 20m South cancels the vertical movement. He is 15 meters East of his origin.",
                            "difficulty": "easy",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "logical-reasoning",
                    "estimated_hours": 10
                },
                {
                    "id": "m4",
                    "week": 4,
                    "title": "Week 4: Advanced Reasoning, Syllogisms & Seating Puzzles",
                    "subject": "Logical Reasoning",
                    "icon": "🧠",
                    "description": "Solve high-difficulty placement puzzles, Venn deduction, and multi-variable arrangements.",
                    "topics": ["Syllogisms", "Seating Arrangement", "Puzzles", "Statement & Assumptions"],
                    "subtopics": [
                        "Venn Diagram Syllogisms (Some, All, No, At Least)",
                        "Linear Single & Double Row Facing Arrangements",
                        "Circular Inward & Outward Seating Arrangements",
                        "Multi-Floor & Day-Color Association Puzzles",
                        "Critical Reasoning: Implicit Assumptions & Inferences"
                    ],
                    "practice_questions": [
                        {
                            "id": "m4-q1",
                            "question": "Statements: All dogs are mammals. All mammals are animals. Conclusion I: All dogs are animals. Conclusion II: All animals are dogs.",
                            "options": ["Only Conclusion I follows", "Only Conclusion II follows", "Both follow", "Neither follows"],
                            "correct_option_index": 0,
                            "explanation": "Dogs ⊆ Mammals ⊆ Animals. Thus all dogs are animals (I is valid). But other animals exist, so all animals are dogs is invalid.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m4-q2",
                            "question": "Six friends A, B, C, D, E, F sit in a circle facing the center. A is opposite D. B is to the immediate right of A. E is opposite B. Who is opposite B?",
                            "options": ["C", "D", "E", "F"],
                            "correct_option_index": 2,
                            "explanation": "By definition in the premise, E is positioned directly opposite B.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m4-q3",
                            "question": "Statement: 'Fasten seatbelts while driving to ensure safety.' Assumption I: Seatbelts prevent severe crash injuries. Assumption II: People follow safety advice.",
                            "options": ["Only I is implicit", "Only II is implicit", "Both I and II are implicit", "Neither is implicit"],
                            "correct_option_index": 2,
                            "explanation": "The notice assumes both that the mechanism works (I) and that drivers will heed the directive (II).",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m4-q4",
                            "question": "At what time between 3:00 and 4:00 will the hour hand and minute hand of a clock coincide?",
                            "options": ["3:15", "3:16 4/11", "3:18 2/11", "3:20"],
                            "correct_option_index": 1,
                            "explanation": "Formula: M = (2/11) × (30 × H) = (2/11) × 90 = 180/11 = 16 4/11 minutes. Time is 3:16 4/11.",
                            "difficulty": "hard",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "logical-reasoning",
                    "estimated_hours": 12
                },
                {
                    "id": "m5",
                    "week": 5,
                    "title": "Week 5: Verbal Ability & Reading Comprehension",
                    "subject": "Verbal Ability",
                    "icon": "📖",
                    "description": "Master English vocabulary, sentence structure, para-jumbles, and reading comprehension passages.",
                    "topics": ["Reading Comprehension", "Sentence Correction", "Synonyms & Antonyms", "Para Jumbles"],
                    "subtopics": [
                        "Main Idea Extraction, Tone Detection & Inference Questions",
                        "Subject-Verb Agreement, Parallelism & Modifier Placement",
                        "High-Yield Placement Vocabulary & Contextual Synonyms",
                        "Para Jumble Opening Sentence Identification & Transition Cues",
                        "Idiomatic Expressions & Common Phrasal Verbs"
                    ],
                    "practice_questions": [
                        {
                            "id": "m5-q1",
                            "question": "Choose the grammatically correct sentence:",
                            "options": [
                                "Neither of the candidates have submitted their portfolio.",
                                "Neither of the candidates has submitted their portfolio.",
                                "Neither of the candidates has submitted his or her portfolio.",
                                "Neither of the candidates have submitted his or her portfolio."
                            ],
                            "correct_option_index": 2,
                            "explanation": "'Neither' is a singular indefinite pronoun requiring the singular verb 'has' and singular pronoun 'his or her'.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m5-q2",
                            "question": "What is the closest synonym for the word 'METICULOUS'?",
                            "options": ["Careless", "Thorough & Precise", "Aggressive", "Indifferent"],
                            "correct_option_index": 1,
                            "explanation": "'Meticulous' means showing great attention to detail, very careful and thorough.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m5-q3",
                            "question": "What is the antonym of the word 'CANDID'?",
                            "options": ["Frank", "Truthful", "Deceptive & Guarded", "Sincere"],
                            "correct_option_index": 2,
                            "explanation": "'Candid' means open, honest, and straightforward. Its opposite is secretive, deceptive, or guarded.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m5-q4",
                            "question": "Reorder the sentences: P: It revolutionized personal computing. Q: In 1984, Apple introduced the Macintosh. R: Setting a new industry benchmark. S: With an intuitive graphical user interface.",
                            "options": ["Q - S - P - R", "P - Q - R - S", "Q - P - R - S", "S - Q - P - R"],
                            "correct_option_index": 0,
                            "explanation": "Q introduces the event (Macintosh launch), S details the feature (graphical UI), P states the impact (revolutionized computing), R concludes with benchmark.",
                            "difficulty": "medium",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "verbal-ability",
                    "estimated_hours": 10
                },
                {
                    "id": "m6",
                    "week": 6,
                    "title": "Week 6: Core Data Structures & Algorithmic Patterns",
                    "subject": "Coding & Data Structures",
                    "icon": "💻",
                    "description": "Master essential algorithmic techniques: two-pointers, sliding window, and hash tables.",
                    "topics": ["Arrays", "Strings", "HashMaps", "Two-Pointers", "Sliding Window"],
                    "subtopics": [
                        "Two-Pointer Technique on Sorted Arrays & In-Place Partitioning",
                        "Sliding Window (Fixed vs Variable Size Subarrays)",
                        "Hash Table Implementation, Collision Resolution & O(1) Lookups",
                        "Frequency Counting, Anagram Detection & Prefix Sums",
                        "Time & Space Complexity Big-O Analysis for Campus Technical Rounds"
                    ],
                    "practice_questions": [
                        {
                            "id": "m6-q1",
                            "question": "What is the optimal time complexity to determine if two elements in a sorted array sum to target K?",
                            "options": ["O(N^2)", "O(N log N)", "O(N)", "O(1)"],
                            "correct_option_index": 2,
                            "explanation": "Using the two-pointer technique (one pointer at start, one at end), the sorted array is processed in a single O(N) pass.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m6-q2",
                            "question": "What is the average time complexity for insertion and search operations in a well-balanced Hash Table?",
                            "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                            "correct_option_index": 0,
                            "explanation": "Under simple uniform hashing, average lookup, insertion, and deletion are O(1) constant time.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m6-q3",
                            "question": "What is the time complexity of the Sliding Window technique for finding maximum sum of subarray of size K?",
                            "options": ["O(N × K)", "O(N)", "O(N^2)", "O(K log N)"],
                            "correct_option_index": 1,
                            "explanation": "By subtracting the exiting element and adding the entering element, each step is O(1), leading to an overall O(N) time.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m6-q4",
                            "question": "Which algorithm is best suited to detect whether a singly linked list contains a cycle in O(1) extra space?",
                            "options": ["Breadth-First Search", "Floyd's Tortoise and Hare (Slow/Fast Pointers)", "Dijkstra's Algorithm", "Hash Set Cache"],
                            "correct_option_index": 1,
                            "explanation": "Floyd's Cycle-Finding Algorithm uses two pointers moving at speeds 1 and 2, detecting loops in O(N) time and O(1) memory.",
                            "difficulty": "medium",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "coding",
                    "estimated_hours": 14
                },
                {
                    "id": "m7",
                    "week": 7,
                    "title": "Week 7: Advanced Data Structures & Algorithms",
                    "subject": "Coding & Data Structures",
                    "icon": "🌲",
                    "description": "Master tree data structures, recursion, binary search, and dynamic programming paradigms.",
                    "topics": ["Binary Trees", "BST", "Recursion", "Dynamic Programming", "Sorting"],
                    "subtopics": [
                        "Inorder, Preorder, Postorder & Level-Order Tree Traversals",
                        "Binary Search Tree Property, Insertion, Deletion & LCA",
                        "Divide & Conquer: Merge Sort vs Quick Sort Stability & Complexity",
                        "Memoization & Tabulation for 0/1 Knapsack & Fibonacci",
                        "Backtracking Principles for N-Queens & Subsets Generation"
                    ],
                    "practice_questions": [
                        {
                            "id": "m7-q1",
                            "question": "Which tree traversal of a Binary Search Tree produces elements in strictly ascending sorted order?",
                            "options": ["Preorder Traversal", "Inorder Traversal", "Postorder Traversal", "Level-order Traversal"],
                            "correct_option_index": 1,
                            "explanation": "Inorder traversal visits Left subtree -> Root -> Right subtree, which naturally extracts BST keys in ascending order.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m7-q2",
                            "question": "What is the maximum number of nodes at level L in a binary tree (where root is level 0)?",
                            "options": ["2^L", "2^(L+1) - 1", "2L", "L^2"],
                            "correct_option_index": 0,
                            "explanation": "Level 0 has 1 (2^0), level 1 has 2 (2^1), level 2 has 4 (2^2), so level L has 2^L nodes.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m7-q3",
                            "question": "What is the time complexity of the 0/1 Knapsack problem with N items and capacity W using Dynamic Programming?",
                            "options": ["O(2^N)", "O(N × W)", "O(N + W)", "O(W^2)"],
                            "correct_option_index": 1,
                            "explanation": "The DP table has dimensions (N+1) × (W+1), requiring O(N × W) time and pseudo-polynomial space.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m7-q4",
                            "question": "Which sorting algorithm guarantees O(N log N) time complexity in the worst case and is stable?",
                            "options": ["Quick Sort", "Heap Sort", "Merge Sort", "Selection Sort"],
                            "correct_option_index": 2,
                            "explanation": "Merge Sort always runs in O(N log N) worst-case time and preserves relative order of equal elements (stable).",
                            "difficulty": "medium",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "coding",
                    "estimated_hours": 14
                },
                {
                    "id": "m8",
                    "week": 8,
                    "title": "Week 8: SQL Mastery & Relational Queries",
                    "subject": "SQL",
                    "icon": "🗄️",
                    "description": "Write advanced SQL queries, joins, aggregates, subqueries, and window functions.",
                    "topics": ["SQL Queries", "Joins", "Aggregate Functions", "Subqueries", "Window Functions"],
                    "subtopics": [
                        "DDL vs DML (CREATE, ALTER, DROP vs INSERT, UPDATE, DELETE)",
                        "INNER, LEFT, RIGHT, FULL OUTER & CROSS JOIN mechanics",
                        "GROUP BY, HAVING vs WHERE clause filter execution order",
                        "Subqueries, Correlated Subqueries & Common Table Expressions (WITH)",
                        "Window Functions: ROW_NUMBER(), RANK(), DENSE_RANK(), and PARTITION BY"
                    ],
                    "practice_questions": [
                        {
                            "id": "m8-q1",
                            "question": "Which SQL JOIN returns all rows from the left table, and matched rows from the right table (with NULL for non-matches)?",
                            "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"],
                            "correct_option_index": 1,
                            "explanation": "LEFT JOIN (or LEFT OUTER JOIN) preserves all rows from the left table, placing NULL values where right table matches are absent.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m8-q2",
                            "question": "In SQL, which clause filters groups of rows AFTER aggregate functions (e.g. COUNT, SUM) are computed?",
                            "options": ["WHERE", "HAVING", "ORDER BY", "GROUP BY"],
                            "correct_option_index": 1,
                            "explanation": "WHERE filters rows before aggregation; HAVING filters groups after aggregation.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m8-q3",
                            "question": "Which window function assigns sequential rank integers without skipping any numbers when ties occur (e.g., 1, 2, 2, 3)?",
                            "options": ["ROW_NUMBER()", "RANK()", "DENSE_RANK()", "LEAD()"],
                            "correct_option_index": 2,
                            "explanation": "DENSE_RANK() assigns consecutive rank integers without gaps. RANK() would skip to 4 after two ties.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m8-q4",
                            "question": "What is true about a Correlated Subquery in SQL?",
                            "options": [
                                "It executes once for the entire query before the outer query.",
                                "It references columns from the outer query and executes once for each candidate row.",
                                "It cannot contain WHERE clauses.",
                                "It only works with SQLite."
                            ],
                            "correct_option_index": 1,
                            "explanation": "A correlated subquery references values from the outer query row and is evaluated repeatedly for each row.",
                            "difficulty": "medium",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "sql",
                    "estimated_hours": 10
                },
                {
                    "id": "m9",
                    "week": 9,
                    "title": "Week 9: DBMS Architecture, Normalization & ACID Transactions",
                    "subject": "DBMS",
                    "icon": "💾",
                    "description": "Master relational database architecture, normal forms, transaction ACID properties, and concurrency control.",
                    "topics": ["Relational Model", "Normalization", "ACID Transactions", "Concurrency Control", "Indexing"],
                    "subtopics": [
                        "Entity-Relationship (ER) Modeling, Primary Keys & Foreign Keys",
                        "Normalization: 1NF, 2NF (Full Functional Dependency), 3NF, BCNF",
                        "ACID Properties: Atomicity, Consistency, Isolation, Durability",
                        "Concurrency Control: Dirty Reads, Phantom Reads, Two-Phase Locking (2PL)",
                        "B-Tree and B+ Tree Index Architecture & Disk Page I/O"
                    ],
                    "practice_questions": [
                        {
                            "id": "m9-q1",
                            "question": "A table where every non-key attribute is fully functionally dependent on the primary key (no partial dependency) is in:",
                            "options": ["1NF", "2NF", "3NF", "BCNF"],
                            "correct_option_index": 1,
                            "explanation": "2NF requires 1NF compliance plus the removal of partial dependencies on any candidate key.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m9-q2",
                            "question": "Which ACID property guarantees that once a transaction commits, its modifications are permanently recorded even in power failure?",
                            "options": ["Atomicity", "Consistency", "Isolation", "Durability"],
                            "correct_option_index": 3,
                            "explanation": "Durability guarantees that committed data persists in non-volatile storage despite sudden system crashes.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m9-q3",
                            "question": "What concurrency anomaly describes a transaction reading uncommitted data written by a concurrent transaction that later rolls back?",
                            "options": ["Dirty Read", "Non-repeatable Read", "Phantom Read", "Lost Update"],
                            "correct_option_index": 0,
                            "explanation": "A Dirty Read occurs when Transaction A reads data modified by Transaction B before B has committed or aborted.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m9-q4",
                            "question": "Why are B+ Trees predominantly preferred over standard Binary Search Trees for database indexes?",
                            "options": [
                                "B+ Trees have fewer nodes than binary trees.",
                                "B+ Trees have high fan-out, minimizing disk block read I/O operations.",
                                "B+ Trees do not support range queries.",
                                "Binary trees cannot store strings."
                            ],
                            "correct_option_index": 1,
                            "explanation": "B+ Trees have high branching factors (fan-out) which keeps the tree shallow (3-4 levels) and reduces expensive disk seeks.",
                            "difficulty": "hard",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "dbms",
                    "estimated_hours": 10
                },
                {
                    "id": "m10",
                    "week": 10,
                    "title": "Week 10: Operating Systems & System Architecture",
                    "subject": "Operating Systems",
                    "icon": "⚙️",
                    "description": "Understand process management, CPU scheduling, deadlocks, and virtual memory.",
                    "topics": ["Processes and Threads", "CPU Scheduling", "Deadlocks", "Memory Management", "Virtual Memory"],
                    "subtopics": [
                        "Process States, PCB, Context Switching & Thread Synchronization",
                        "CPU Scheduling: FCFS, Shortest Job First (SJF), Round Robin",
                        "Deadlock: 4 Necessary Conditions, Prevention & Banker's Algorithm",
                        "Paging, Page Tables, TLB (Translation Lookaside Buffer) & Inverted Pages",
                        "Virtual Memory, Page Faults & Page Replacement Algorithms (FIFO, LRU, Optimal)"
                    ],
                    "practice_questions": [
                        {
                            "id": "m10-q1",
                            "question": "What system resources are shared between multiple threads belonging to the same process?",
                            "options": [
                                "Stack and CPU registers",
                                "Code segment, data segment, and open files (Heap)",
                                "Program Counter",
                                "Thread Local Storage"
                            ],
                            "correct_option_index": 1,
                            "explanation": "Threads in the same process share code, global data, open files, and the heap, but have independent stacks and registers.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m10-q2",
                            "question": "Which of the following is NOT one of the four Coffman conditions necessary for a Deadlock to occur?",
                            "options": ["Mutual Exclusion", "Hold and Wait", "Preemption", "Circular Wait"],
                            "correct_option_index": 2,
                            "explanation": "No-Preemption (Non-preemption) is the required condition. Preemption actually prevents deadlocks.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m10-q3",
                            "question": "What is the phenomenon called when an OS spends more time handling page faults and swapping than executing user instructions?",
                            "options": ["Belady's Anomaly", "Thrashing", "Starvation", "Deadlock"],
                            "correct_option_index": 1,
                            "explanation": "Thrashing occurs when total memory allocated to active processes is insufficient, causing continuous page faults.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m10-q4",
                            "question": "Which page replacement algorithm suffers from Belady's Anomaly (where increasing page frames increases page faults)?",
                            "options": ["LRU (Least Recently Used)", "Optimal Algorithm", "FIFO (First In First Out)", "LFU (Least Frequently Used)"],
                            "correct_option_index": 2,
                            "explanation": "FIFO page replacement can exhibit Belady's Anomaly because it is not a stack algorithm.",
                            "difficulty": "hard",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "os",
                    "estimated_hours": 12
                },
                {
                    "id": "m11",
                    "week": 11,
                    "title": "Week 11: Computer Networks & Web Protocols",
                    "subject": "Computer Networks",
                    "icon": "🌐",
                    "description": "Understand network protocol layers, IP addressing, TCP/UDP transport, and web security.",
                    "topics": ["OSI and TCP/IP Models", "IP Addressing", "TCP vs UDP", "DNS & HTTP/HTTPS", "Network Security"],
                    "subtopics": [
                        "OSI 7 Layers vs TCP/IP 4 Layers & Encapsulation Headers",
                        "IPv4 Classless Addressing (CIDR) & Subnet Mask Calculations",
                        "TCP 3-Way Handshake, Flow Control (Sliding Window) & Congestion Control",
                        "UDP Connectionless Transport (VoIP, Video Streaming, Gaming)",
                        "DNS Resolution Workflow, HTTP/1.1 vs HTTP/2 vs HTTP/3 & TLS Handshake"
                    ],
                    "practice_questions": [
                        {
                            "id": "m11-q1",
                            "question": "At which layer of the OSI model does a Router operate to route packets between networks?",
                            "options": ["Data Link Layer (Layer 2)", "Network Layer (Layer 3)", "Transport Layer (Layer 4)", "Application Layer (Layer 7)"],
                            "correct_option_index": 1,
                            "explanation": "Routers inspect IP addresses to make routing decisions, which is the function of Network Layer 3.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m11-q2",
                            "question": "What sequence of TCP control packets is exchanged during the standard 3-way handshake?",
                            "options": ["ACK -> SYN -> FIN", "SYN -> SYN-ACK -> ACK", "SYN -> ACK -> DATA", "RST -> SYN -> ACK"],
                            "correct_option_index": 1,
                            "explanation": "Client sends SYN; Server responds with SYN-ACK; Client confirms with ACK, establishing the TCP socket.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m11-q3",
                            "question": "How many usable host IP addresses are available in a subnet with a /26 mask (255.255.255.192)?",
                            "options": ["30", "62", "64", "126"],
                            "correct_option_index": 1,
                            "explanation": "32 - 26 = 6 host bits. Total IPs = 2^6 = 64. Subtract network ID and broadcast IP -> 64 - 2 = 62 usable hosts.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m11-q4",
                            "question": "Which protocol provides reliable, connection-oriented data delivery with congestion control?",
                            "options": ["UDP", "IP", "TCP", "ICMP"],
                            "correct_option_index": 2,
                            "explanation": "TCP provides guaranteed delivery, retransmission of lost segments, in-order reassembly, and congestion control.",
                            "difficulty": "easy",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "cn",
                    "estimated_hours": 12
                },
                {
                    "id": "m12",
                    "week": 12,
                    "title": "Week 12: Company Mock Exams, OOP & AI Interview Prep",
                    "subject": "Company Mocks & Interviews",
                    "icon": "🏢",
                    "description": "Simulate campus exams (TCS, Infosys, Cognizant), revise OOP principles, and master STAR interview delivery.",
                    "topics": ["Company Exam Simulations", "OOPs Principles", "SOLID Design", "STAR Interview Framework"],
                    "subtopics": [
                        "TCS NQT Foundation (Numerical, Verbal, Reasoning) & Advanced Sections",
                        "Infosys Pseudocode, Reasoning Ability & Technical MCQ Formats",
                        "Cognizant GenC Quantitative & Automata Fix Analysis",
                        "OOP Pillars: Encapsulation, Abstraction, Inheritance, Polymorphism",
                        "STAR Behavioral Interview Responses (Situation, Task, Action, Result)"
                    ],
                    "practice_questions": [
                        {
                            "id": "m12-q1",
                            "question": "Which Object-Oriented Programming principle is demonstrated by restricting direct access to object attributes via private fields and getters/setters?",
                            "options": ["Polymorphism", "Inheritance", "Encapsulation", "Compilation"],
                            "correct_option_index": 2,
                            "explanation": "Encapsulation bundles data and methods together while hiding internal implementation details from external direct access.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m12-q2",
                            "question": "In the SOLID object-oriented design principles, what does the 'L' stand for?",
                            "options": ["Linear Inheritance Principle", "Liskov Substitution Principle", "Lazy Initialization Principle", "Late Binding Principle"],
                            "correct_option_index": 1,
                            "explanation": "Liskov Substitution Principle states that subtypes must be substitutable for their base types without altering program correctness.",
                            "difficulty": "medium",
                            "marks": 1.0
                        },
                        {
                            "id": "m12-q3",
                            "question": "In the STAR technique used in behavioral and HR placement interviews, what does the acronym stand for?",
                            "options": [
                                "Skill, Training, Ability, Result",
                                "Situation, Task, Action, Result",
                                "Strategy, Technique, Analysis, Review",
                                "Strength, Talent, Ambition, Responsibility"
                            ],
                            "correct_option_index": 1,
                            "explanation": "STAR stands for Situation, Task, Action, and Result — the recommended framework for answering competency-based interview questions.",
                            "difficulty": "easy",
                            "marks": 1.0
                        },
                        {
                            "id": "m12-q4",
                            "question": "What is the primary purpose of an Applicant Tracking System (ATS) resume checker in campus placements?",
                            "options": [
                                "To verify social media activity",
                                "To score keyword match between student skills and job requisition descriptions",
                                "To compile Python source code",
                                "To send automated WhatsApp messages"
                            ],
                            "correct_option_index": 1,
                            "explanation": "ATS parsers scan candidate resumes for relevant technical keywords, skills, and experience matching job requirements.",
                            "difficulty": "easy",
                            "marks": 1.0
                        }
                    ],
                    "quiz_category": "interview_prep",
                    "estimated_hours": 14
                }
            ]
        },
        {
            "title": "Full-Stack Web Developer Career Track",
            "slug": "full-stack-web-developer",
            "role_target": "Full-Stack Engineer (MERN / Python-FastAPI)",
            "description": "Comprehensive roadmap from HTML/CSS/JS fundamentals to REST APIs, databases, authentication, and cloud deployment.",
            "icon": "💻",
            "estimated_weeks": 10,
            "milestones": [
                {
                    "id": "fs1",
                    "week": 1,
                    "title": "Milestone 1: Modern JavaScript & Frontend Architecture",
                    "subject": "Web Development",
                    "description": "ES6+, Async/Await, DOM Manipulation, Fetch API, and Component state.",
                    "topics": ["JavaScript", "DOM", "Async JS"],
                    "subtopics": ["Arrow functions & Destructuring", "Promises & async/await", "Event bubbling & delegation", "Fetch API & JSON handling"],
                    "practice_questions": [
                        {
                            "id": "fs1-q1",
                            "question": "Which array method returns a new array with elements that satisfy a predicate test function?",
                            "options": ["map()", "filter()", "forEach()", "reduce()"],
                            "correct_option_index": 1,
                            "explanation": "filter() creates a shallow copy of a portion of a given array filtered down to just the elements passing the test.",
                            "difficulty": "easy",
                            "marks": 1.0
                        }
                    ]
                },
                {
                    "id": "fs2",
                    "week": 2,
                    "title": "Milestone 2: Backend REST APIs & Authentication",
                    "subject": "Web Development",
                    "description": "FastAPI or Express, JWT authentication, Request validation, and Middleware.",
                    "topics": ["REST APIs", "JWT", "Security"],
                    "subtopics": ["RESTful design principles", "Stateless JWT tokens", "Password hashing with bcrypt", "CORS & Security headers"],
                    "practice_questions": [
                        {
                            "id": "fs2-q1",
                            "question": "Which HTTP status code signifies that a client must authenticate itself to get the requested response?",
                            "options": ["400 Bad Request", "401 Unauthorized", "403 Forbidden", "404 Not Found"],
                            "correct_option_index": 1,
                            "explanation": "401 Unauthorized indicates that the request lacks valid authentication credentials.",
                            "difficulty": "easy",
                            "marks": 1.0
                        }
                    ]
                },
                {
                    "id": "fs3",
                    "week": 3,
                    "title": "Milestone 3: Database Design & ORM Modeling",
                    "subject": "Web Development",
                    "description": "PostgreSQL / SQLite, SQLAlchemy ORM, Schema Migrations, and Indexing.",
                    "topics": ["SQLAlchemy", "PostgreSQL", "Database Design"],
                    "subtopics": ["Declarative Base models", "One-to-Many & Many-to-Many relationships", "Alembic migrations", "Session management & connection pooling"],
                    "practice_questions": [
                        {
                            "id": "fs3-q1",
                            "question": "What is the purpose of Alembic in a SQLAlchemy-based Python application?",
                            "options": ["Web server routing", "Database schema migration tool", "Template rendering engine", "JWT token generator"],
                            "correct_option_index": 1,
                            "explanation": "Alembic manages schema migrations, tracking alterations and table creations over time.",
                            "difficulty": "easy",
                            "marks": 1.0
                        }
                    ]
                },
                {
                    "id": "fs4",
                    "week": 4,
                    "title": "Milestone 4: Full-Stack Capstone Project & Deployment",
                    "subject": "Web Development",
                    "description": "Deploy to Railway/Render, implement Docker containers, and build a live portfolio demo.",
                    "topics": ["Docker", "Deployment", "CI/CD"],
                    "subtopics": ["Dockerfile containerization", "Environment variable security", "Reverse proxy & Nginx configuration", "Cloud deployment on Railway"],
                    "practice_questions": [
                        {
                            "id": "fs4-q1",
                            "question": "What is the main advantage of containerizing an application with Docker?",
                            "options": [
                                "Eliminates need for source code",
                                "Ensures application runs consistently across any environment",
                                "Increases CPU clock frequency",
                                "Replaces relational databases"
                            ],
                            "correct_option_index": 1,
                            "explanation": "Docker packages code and dependencies together, eliminating the 'works on my machine' issue across environments.",
                            "difficulty": "easy",
                            "marks": 1.0
                        }
                    ]
                }
            ]
        }
    ]

    for rd in roadmaps_data:
        existing = db.query(LearningRoadmap).filter(LearningRoadmap.slug == rd["slug"]).first()
        if existing:
            existing.title = rd["title"]
            existing.description = rd["description"]
            existing.estimated_weeks = rd["estimated_weeks"]
            existing.icon = rd["icon"]
            existing.milestones_json = json.dumps(rd["milestones"])
        else:
            roadmap = LearningRoadmap(
                title=rd["title"],
                slug=rd["slug"],
                role_target=rd["role_target"],
                description=rd["description"],
                icon=rd["icon"],
                estimated_weeks=rd["estimated_weeks"],
                milestones_json=json.dumps(rd["milestones"]),
            )
            db.add(roadmap)

    db.commit()
