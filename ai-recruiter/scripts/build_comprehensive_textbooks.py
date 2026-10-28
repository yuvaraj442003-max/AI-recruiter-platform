"""
build_comprehensive_textbooks.py - Generates and seeds complete, exhaustive,
chapter-by-chapter learning materials for all 13 placement subjects:
1. DSA (10 Chapters)
2. SQL & Relational Databases (8 Chapters)
3. Core Java & OOPs (10 Chapters)
4. Python Programming (8 Chapters)
5. JavaScript & TypeScript (8 Chapters)
6. Operating Systems (8 Chapters)
7. Computer Networks (8 Chapters)
8. DBMS & System Design (8 Chapters)
9. Quantitative Aptitude (8 Chapters)
10. Logical Reasoning (8 Chapters)
11. Verbal Ability (8 Chapters)
12. Data Engineering & Big Data (8 Chapters)
13. Artificial Intelligence & Machine Learning (8 Chapters)

Each chapter strictly includes:
1. Detailed Explanation & Concepts (deep theoretical foundation & internal mechanics)
2. Key Formulas, Rules & Complexity Classes
3. Step-by-Step Solved Examples (Problem, Strategy, Full Working Code/Calculation, Line-by-Line Breakdown)
4. Practice Questions with Answers & Explanations (self-assessment test questions)
5. Placement & Company Technical Interview Questions (FAANG, Tier 1, IT Services interview questions & model answers)
"""
import os
import sys
import json
import sqlite3
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

print("BASE_DIR:", BASE_DIR)
print("BACKEND_DIR:", BACKEND_DIR)

