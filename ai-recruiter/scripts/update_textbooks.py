"""
Script to wire master textbooks into book_curriculum_service.py and seed them into PostgreSQL database.
"""
import ast
import os
import sys

TARGET_PATH = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "services", "book_curriculum_service.py")
TARGET_PATH = os.path.abspath(TARGET_PATH)

with open(TARGET_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Part 1: Replace from 'DSA_TEXTBOOK = {' up to 'JAVA_TEXTBOOK = {'
sec1_start = content.index("DSA_TEXTBOOK = {")
sec1_end = content.index("JAVA_TEXTBOOK = {")

part1_replacement = """DSA_TEXTBOOK = {
    "slug": "dsa-prescribed-textbook",
    "title": "Data Structures & Algorithms: Placement Master Edition (Prescribed Textbook)",
    "subject": "Data Structures & Algorithms (DSA)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Data Structures and Algorithms from foundational "
        "asymptotic complexity to advanced dynamic programming and graph theory. All DSA exam and practice "
        "questions are strictly derived only from the topics in these chapters."
    ),
    "chapters": DSA_MASTER_CHAPTERS,
    "full_textbook_markdown": DSA_TEXTBOOK_MARKDOWN,
}

SQL_TEXTBOOK = {
    "slug": "sql-prescribed-textbook",
    "title": "SQL & Relational Databases: Placement Master Edition (Prescribed Textbook)",
    "subject": "SQL & Database Queries",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete enterprise textbook on SQL and relational database engineering covering basic queries, "
        "relational joins, window functions, query execution plans, and transaction concurrency. "
        "All SQL exam questions are strictly grounded in these chapters."
    ),
    "chapters": SQL_MASTER_CHAPTERS,
    "full_textbook_markdown": SQL_TEXTBOOK_MARKDOWN,
}

QUANT_TEXTBOOK = {
    "slug": "quantitative-aptitude-prescribed-textbook",
    "title": "Quantitative Aptitude: Corporate Recruitment Master Edition (Prescribed Textbook)",
    "subject": "Quantitative Aptitude",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering corporate numerical aptitude, speed mathematics, "
        "percentages, ratios, profit & loss, time and work, speed distance, permutations, probability, and data interpretation."
    ),
    "chapters": QUANT_MASTER_CHAPTERS,
    "full_textbook_markdown": QUANT_TEXTBOOK_MARKDOWN,
}

LOGICAL_TEXTBOOK = {
    "slug": "logical-reasoning-prescribed-textbook",
    "title": "Logical Reasoning & Analytical Ability (Prescribed Textbook)",
    "subject": "Logical Reasoning",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering corporate analytical reasoning, syllogisms, "
        "blood relations, linear/circular seating arrangements, direction tests, coding-decoding, and multi-variable puzzles."
    ),
    "chapters": LOGICAL_MASTER_CHAPTERS,
    "full_textbook_markdown": LOGICAL_TEXTBOOK_MARKDOWN,
}

"""

content = content[:sec1_start] + part1_replacement + content[sec1_end:]

# Part 2: Replace from 'PYTHON_TEXTBOOK = {' up to 'ALL_PRESCRIBED_TEXTBOOKS = ['
sec2_start = content.index("PYTHON_TEXTBOOK = {")
sec2_end = content.index("ALL_PRESCRIBED_TEXTBOOKS = [")

part2_replacement = """PYTHON_TEXTBOOK = {
    "slug": "python-prescribed-textbook",
    "title": "Python Programming & Interview Foundations (Prescribed Master Textbook)",
    "subject": "Python",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete campus placement master textbook covering Python execution architecture, "
        "Built-in Data Structures & Mutability, Comprehensions, Functions & LEGB Scoping, "
        "OOP & Dunder Methods, Iterators & Generators, Decorators, Context Managers, and Standard Libraries. "
        "All Python exam questions are strictly derived from these chapters."
    ),
    "chapters": PYTHON_MASTER_CHAPTERS,
    "full_textbook_markdown": PYTHON_TEXTBOOK_MARKDOWN,
}

JAVASCRIPT_TEXTBOOK = {
    "slug": "javascript-prescribed-textbook",
    "title": "Modern JavaScript & TypeScript: Full-Stack Placement Edition (Prescribed Textbook)",
    "subject": "JavaScript / TypeScript",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete textbook on JavaScript runtime engine architecture, V8 microtask queue, "
        "closures, prototypal inheritance, ES6+ idioms, and TypeScript static typing."
    ),
    "chapters": JAVASCRIPT_MASTER_CHAPTERS,
    "full_textbook_markdown": JAVASCRIPT_TEXTBOOK_MARKDOWN,
}

DATA_ENG_TEXTBOOK = {
    "slug": "data-engineering-prescribed-textbook",
    "title": "Data Engineering & Big Data Systems (Prescribed Textbook)",
    "subject": "Data Engineering & Big Data",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Comprehensive campus placement textbook covering modern data engineering, "
        "distributed computing (Hadoop/Spark), data pipelines, streaming architectures (Kafka), "
        "columnar data formats (Parquet), and Cloud Data Warehousing."
    ),
    "chapters": DATA_ENG_MASTER_CHAPTERS,
    "full_textbook_markdown": DATA_ENG_TEXTBOOK_MARKDOWN,
}

AI_ML_TEXTBOOK = {
    "slug": "ai-machine-learning-prescribed-textbook",
    "title": "Artificial Intelligence & Machine Learning: Campus Master Edition (Prescribed Textbook)",
    "subject": "Artificial Intelligence & Machine Learning (AI / ML)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Artificial Intelligence and Machine Learning from mathematical foundations "
        "to Deep Learning architectures, Transformer LLMs, Loss functions, and evaluation metrics."
    ),
    "chapters": AI_ML_MASTER_CHAPTERS,
    "full_textbook_markdown": AI_ML_TEXTBOOK_MARKDOWN,
}

OS_TEXTBOOK = {
    "slug": "operating-systems-prescribed-textbook",
    "title": "Operating Systems & Concurrency Architecture: Placement Master Edition (Prescribed Textbook)",
    "subject": "Operating Systems (OS)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Operating Systems kernel architecture, "
        "process scheduling, synchronization primitives, deadlocks, virtual memory management, and file systems."
    ),
    "chapters": OS_MASTER_CHAPTERS,
    "full_textbook_markdown": OS_TEXTBOOK_MARKDOWN,
}

CN_TEXTBOOK = {
    "slug": "computer-networks-prescribed-textbook",
    "title": "Computer Networks & Internet Protocols: Campus Master Edition (Prescribed Textbook)",
    "subject": "Computer Networks (CN)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Comprehensive campus placement textbook covering OSI 7-layer model, TCP/IP stack, "
        "IPv4/IPv6 CIDR subnetting, transport layer reliability, routing protocols, application protocols, and network security."
    ),
    "chapters": CN_MASTER_CHAPTERS,
    "full_textbook_markdown": CN_TEXTBOOK_MARKDOWN,
}

DBMS_TEXTBOOK = {
    "slug": "dbms-system-design-prescribed-textbook",
    "title": "Database Management Systems & System Architecture: Placement Master Edition (Prescribed Textbook)",
    "subject": "DBMS & Database Design",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Database Management Systems architecture, "
        "Entity-Relationship modeling, Relational Algebra, Normalization (1NF through BCNF), ACID transaction management, "
        "concurrency protocols, and storage indexing."
    ),
    "chapters": DBMS_MASTER_CHAPTERS,
    "full_textbook_markdown": DBMS_TEXTBOOK_MARKDOWN,
}

VERBAL_TEXTBOOK = {
    "slug": "verbal-ability-prescribed-textbook",
    "title": "Verbal Ability & Corporate English: Placement Master Edition (Prescribed Textbook)",
    "subject": "Verbal Ability & English",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering corporate English grammar, sentence correction, "
        "vocabulary building, para jumbles, reading comprehension strategies, and HR interview articulation."
    ),
    "chapters": VERBAL_MASTER_CHAPTERS,
    "full_textbook_markdown": VERBAL_TEXTBOOK_MARKDOWN,
}

"""

content = content[:sec2_start] + part2_replacement + content[sec2_end:]

# Part 3: Replace Question Banks
q_start = content.index("# Include existing Java and Python questions")
q_end = content.index("TOPIC_QUESTION_BANKS: Dict[str, List[Dict[str, Any]]] = {")

part3_replacement = """JAVA_BOOK_QUESTIONS = JAVA_EXPANDED_BOOK_QUESTIONS
PYTHON_BOOK_QUESTIONS = PYTHON_EXPANDED_QUESTIONS
DSA_BOOK_QUESTIONS = DSA_EXPANDED_QUESTIONS
SQL_BOOK_QUESTIONS = SQL_EXPANDED_QUESTIONS
QUANT_BOOK_QUESTIONS = QUANT_EXPANDED_QUESTIONS
LOGICAL_BOOK_QUESTIONS = LOGICAL_EXPANDED_QUESTIONS
JAVASCRIPT_BOOK_QUESTIONS = JAVASCRIPT_EXPANDED_QUESTIONS
DATA_ENG_BOOK_QUESTIONS = DATA_ENG_EXPANDED_QUESTIONS
AI_ML_BOOK_QUESTIONS = AI_ML_EXPANDED_QUESTIONS
OS_BOOK_QUESTIONS = OS_EXPANDED_QUESTIONS
CN_BOOK_QUESTIONS = CN_EXPANDED_QUESTIONS
DBMS_BOOK_QUESTIONS = DBMS_EXPANDED_QUESTIONS
VERBAL_BOOK_QUESTIONS = VERBAL_EXPANDED_QUESTIONS

"""

content = content[:q_start] + part3_replacement + content[q_end:]

# Validate AST
ast.parse(content)

with open(TARGET_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Validated and updated book_curriculum_service.py successfully!")

