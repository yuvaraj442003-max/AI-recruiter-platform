"""
company_intelligence_service.py — Comprehensive Campus Placement Intelligence,
Company Exam Patterns, Aptitude Question Trends, and Preparation Strategies.

Covers top mass recruiters and product tech leaders:
1. TCS (Tata Consultancy Services - NQT Ninja, Digital, Prime)
2. Infosys (InfyTQ, Systems Engineer, Specialist Programmer)
3. Cognizant (GenC, GenC Next / Elevate)
4. Accenture (Cognitive & Technical Assessment)
5. Wipro (Elite National Talent Hunt & Turbo)
6. Amazon (SDE-1 / WOW Campus Assessment)
7. Capgemini (Exceller Tech Challenge)
8. Deloitte (Deloitte USI Placement Drive)
9. Goldman Sachs (Engineering Campus Hiring Program)
10. Zoho (Software Developer & Problem Solving Drive)
11. Google (STEP & University Grad SDE)
12. Microsoft (Campus SDE & Codess)
"""
from typing import Any, Dict, List, Optional

TOP_COMPANIES_INTELLIGENCE: Dict[str, Dict[str, Any]] = {
    "tcs": {
        "slug": "tcs",
        "name": "Tata Consultancy Services (TCS)",
        "badge_text": "TCS NQT 2026",
        "icon": "🏢",
        "accent_color": "#1e3a8a",
        "gradient": "linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)",
        "tagline": "India's largest IT recruiter hiring across Ninja, Digital, and Prime bands via National Qualifier Test (NQT).",
        "overall_difficulty": "Moderate",
        "hiring_roles": [
            {"title": "Ninja Cadre", "package": "₹3.36 LPA", "focus": "Foundational Aptitude & Basic Coding"},
            {"title": "Digital Cadre", "package": "₹7.00 LPA", "focus": "Advanced Coding, System Thinking & High Aptitude"},
            {"title": "Prime Cadre", "package": "₹9.00 LPA", "focus": "Competitive Programming, AI/Cloud & Complex DSA"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Foundation Section", "details": "Numerical Ability (20 Qs), Verbal Ability (25 Qs), Reasoning Ability (20 Qs) — 75 mins total."},
            {"round": "Round 2: Advanced Section", "details": "Advanced Quantitative & Reasoning (15 Qs) + Advanced Coding (2 problems in C/C++/Java/Python) — 90 mins total."},
            {"round": "Round 3: Technical Interview", "details": "OOPs, Project architecture, SQL queries, DSA basics, and resume defense."},
            {"round": "Round 4: HR / Managerial", "details": "Relocation willingness, shift flexibility, communication, and behavioral scenarios."},
        ],
        "exam_pattern": [
            {"section": "Numerical Ability", "questions": 20, "time_mins": 25, "marking": "1 mark per Q, No Negative", "cutoff": "65%"},
            {"section": "Verbal Ability", "questions": 25, "time_mins": 25, "marking": "1 mark per Q, No Negative", "cutoff": "60%"},
            {"section": "Reasoning Ability", "questions": 20, "time_mins": 25, "marking": "1 mark per Q, No Negative", "cutoff": "65%"},
            {"section": "Advanced Quant & Reasoning", "questions": 15, "time_mins": 25, "marking": "2 marks per Q, No Negative", "cutoff": "70% (For Digital/Prime)"},
            {"section": "Advanced Coding (2 Problems)", "questions": 2, "time_mins": 65, "marking": "Automated Testcases", "cutoff": "1.5 to 2 Problems Solved"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Number Systems & Divisibility", "weight": "25%", "freq": "Very High", "tips": "Focus on remainder theorems, unit digits, LCM/HCF model questions."},
                {"topic": "Time & Work / Pipes", "weight": "20%", "freq": "High", "tips": "Master the LCM efficiency method; practice alternating workers."},
                {"topic": "Speed, Time & Distance", "weight": "15%", "freq": "High", "tips": "Trains crossing moving objects and relative speed formulas are mandatory."},
                {"topic": "Permutations, Combinations & Probability", "weight": "15%", "freq": "High", "tips": "Coin tossing, dice, and committee formation problems repeat every year."},
                {"topic": "Percentages & Profit-Loss", "weight": "15%", "freq": "Medium", "tips": "Successive discounts and dishonest dealer weight formulas."},
                {"topic": "Geometry & Mensuration", "weight": "10%", "freq": "Medium", "tips": "Area/perimeter ratios of circles, cylinders, and cones."},
            ],
            "reasoning_trends": [
                {"topic": "Data Sufficiency", "weight": "25%", "freq": "Very High", "tips": "TCS heavily tests if statement 1, 2, or both are sufficient. Don't calculate fully; verify sufficiency."},
                {"topic": "Coding-Decoding & Series", "weight": "20%", "freq": "High", "tips": "Letter-to-number position values and alternating arithmetic series."},
                {"topic": "Blood Relations & Directions", "weight": "20%", "freq": "High", "tips": "Family tree mapping and Pythagoras theorem for final shortest distance."},
                {"topic": "Syllogisms & Venn Diagrams", "weight": "20%", "freq": "High", "tips": "Complementary pairs (Either-Or) are favourite traps in TCS NQT."},
                {"topic": "Seating Arrangements", "weight": "15%", "freq": "Medium", "tips": "Circular seating facing inward/outward with 6-8 people."},
            ],
            "verbal_trends": [
                {"topic": "Reading Comprehension", "weight": "30%", "freq": "High", "tips": "Inference-based questions from short 250-word business or scientific passages."},
                {"topic": "Sentence Correction & Cloze Test", "weight": "35%", "freq": "Very High", "tips": "Subject-verb agreement, prepositions, and parallel structures."},
                {"topic": "Para Jumbles", "weight": "20%", "freq": "High", "tips": "Identify opening independent statement and noun-pronoun transitional links."},
                {"topic": "Vocabulary in Context", "weight": "15%", "freq": "Medium", "tips": "Synonyms/antonyms determined by sentence meaning."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Master speed-math tables (squares up to 30, cubes up to 20, fraction-to-percentage conversions). Solve 40 daily aptitude questions.",
            "Week 2: Focus on TCS-specific recurring types: Remainder theorems, Cryptarithmetic basics, and Venn diagrams.",
            "Week 3: Daily timed practice of 2 coding problems (Strings & Array transformations) in Java or Python.",
            "Week 4: Take full-length TCS NQT mock tests under strict 30s-per-question and overall sectional countdown.",
        ],
        "sample_questions": [
            {
                "question": "A number when divided by 280 leaves a remainder of 73. When the same number is divided by 35, what is the remainder?",
                "options": ["3", "7", "8", "13"],
                "correct_option_index": 0,
                "explanation": "Since 280 is a multiple of 35 (280 = 35 × 8), we simply divide the remainder 73 by 35. 73 ÷ 35 = 2 with remainder 3. Shortcut: Remainder = 73 mod 35 = 3.",
                "difficulty": "medium",
                "tag": "TCS NQT Quant",
            },
            {
                "question": "Six persons P, Q, R, S, T, and U are sitting in a circle facing the center. P is opposite to S. Q is between P and T. U is between S and R. Who is sitting to the immediate right of S?",
                "options": ["P", "Q", "T", "U"],
                "correct_option_index": 3,
                "explanation": "Facing the center: S is at the bottom, P is at top. Q is between P and T on one side, U is between S and R on the other. Moving counter-clockwise from S to center gives U on the immediate right of S.",
                "difficulty": "medium",
                "tag": "TCS NQT Reasoning",
            },
            {
                "question": "If 12 men or 18 women can reap a field in 14 days, then in how many days can 8 men and 16 women reap the same field?",
                "options": ["7 days", "9 days", "10 days", "12 days"],
                "correct_option_index": 1,
                "explanation": "12 Men = 18 Women => 1 Man = 1.5 Women. So 8 Men = 8 × 1.5 = 12 Women. Total workforce = 12 + 16 = 28 Women. Days = (18 Women × 14 days) / 28 Women = 252 / 28 = 9 days.",
                "difficulty": "medium",
                "tag": "TCS NQT Quant",
            },
        ],
        "mock_test_title": "TCS NQT National Placement Mock Test 1",
        "mock_test_id": "tcs-nqt-national-placement-mock-test-1",
    },
    "infosys": {
        "slug": "infosys",
        "name": "Infosys",
        "badge_text": "Infosys InfyTQ & SP",
        "icon": "💎",
        "accent_color": "#0284c7",
        "gradient": "linear-gradient(135deg, #0369a1 0%, #0284c7 100%)",
        "tagline": "Global consulting and IT services leader with dedicated tracks: Systems Engineer (SE) and Specialist Programmer (SP).",
        "overall_difficulty": "Moderate to High",
        "hiring_roles": [
            {"title": "Systems Engineer (SE)", "package": "₹3.60 LPA", "focus": "Mathematical Ability, Reasoning, Verbal & Pseudocode"},
            {"title": "Digital Specialist Engineer (DSE)", "package": "₹6.25 LPA", "focus": "Algorithms, Data Structures & System Optimization"},
            {"title": "Specialist Programmer (SP)", "package": "₹9.50 LPA", "focus": "Hard Dynamic Programming, Advanced Graphs & Math"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Online Aptitude Assessment", "details": "Reasoning Ability (15 Qs, 25m), Mathematical Ability (10 Qs, 35m), Verbal Ability (20 Qs, 20m), Pseudocode (5 Qs, 10m), Puzzle Solving (4 Qs, 10m)."},
            {"round": "Round 2: Technical Interview", "details": "Deep questions on Cryptarithmetic logic, Recursion, Database Normalization, and Project architecture."},
            {"round": "Round 3: HR Round", "details": "Verification of academic background, communication, problem-solving mindset, and teamwork."},
        ],
        "exam_pattern": [
            {"section": "Reasoning Ability", "questions": 15, "time_mins": 25, "marking": "+1, No Negative", "cutoff": "70%"},
            {"section": "Mathematical Ability", "questions": 10, "time_mins": 35, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Verbal Ability", "questions": 20, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "60%"},
            {"section": "Pseudocode", "questions": 5, "time_mins": 10, "marking": "+1, No Negative", "cutoff": "60%"},
            {"section": "Numerical Puzzle Solving", "questions": 4, "time_mins": 10, "marking": "+1, No Negative", "cutoff": "75%"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Cryptarithmetic Addition & Multiplication", "weight": "30%", "freq": "Signature", "tips": "Infosys is famous for Cryptarithmetic (e.g. SEND + MORE = MONEY). Practice finding carry digits (M=1) and parity."},
                {"topic": "Permutations & Combinations", "weight": "20%", "freq": "Very High", "tips": "Focus on word formation with vowels together, seating arrangements with constraints."},
                {"topic": "Probability", "weight": "15%", "freq": "High", "tips": "Conditional probability, dice sums, and defective item selections."},
                {"topic": "Time, Speed & Distance", "weight": "15%", "freq": "High", "tips": "Boats and streams with current speed, circular track races."},
                {"topic": "Algebra & Series Progressions", "weight": "20%", "freq": "High", "tips": "AP/GP harmonic progressions and quadratic roots."},
            ],
            "reasoning_trends": [
                {"topic": "Data Sufficiency", "weight": "30%", "freq": "Very High", "tips": "Infosys tests high-level 3-statement data sufficiency. Focus on whether a unique solution exists."},
                {"topic": "Visual Reasoning & Shape Folding", "weight": "25%", "freq": "High", "tips": "Cube nets folding, paper cutting, and rotating patterns."},
                {"topic": "Critical Reasoning (Statement & Assumption)", "weight": "25%", "freq": "High", "tips": "Read carefully for implicit assumptions vs factual conclusions."},
                {"topic": "Syllogisms & Analytical Puzzles", "weight": "20%", "freq": "High", "tips": "Floor-based puzzles with 8 people and 2 variables (color/car)."},
            ],
            "verbal_trends": [
                {"topic": "Sentence Completion & Fill in the Blanks", "weight": "35%", "freq": "High", "tips": "Idiomatic expressions, conditional clauses (If + had + would have)."},
                {"topic": "Error Correction", "weight": "35%", "freq": "High", "tips": "Subject-verb agreement and modifier placement."},
                {"topic": "Reading Comprehension", "weight": "30%", "freq": "Medium", "tips": "Short passages requiring rapid factual extraction."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Master Cryptarithmetic rules (Carry digit is always 1; sum of two single digits <= 19; even/odd parity).",
            "Week 2: Deep dive into Data Sufficiency. Practice 20 questions daily without computing final answers.",
            "Week 3: Solve Pseudocode questions tracing bitwise operations (`&`, `|`, `^`, `<<`, `>>`) and recursive calls.",
            "Week 4: Attempt timed Infosys mock assessments with strict section timer limits.",
        ],
        "sample_questions": [
            {
                "question": "In the cryptarithmetic addition: SEND + MORE = MONEY, what is the unique digit value of the letter M?",
                "options": ["0", "1", "2", "9"],
                "correct_option_index": 1,
                "explanation": "In cryptarithmetic addition of two 4-digit numbers yielding a 5-digit sum, the leading carry digit (M) can only ever be 1 because the maximum sum of two 4-digit numbers is 9999 + 9999 = 19998.",
                "difficulty": "medium",
                "tag": "Infosys Cryptarithmetic",
            },
            {
                "question": "What is the output of the following pseudocode? \nInteger a, b, c\nSet a = 4, b = 6, c = 2\nb = (b ^ c) + a\na = a + b + c\nPrint a",
                "options": ["14", "16", "18", "20"],
                "correct_option_index": 0,
                "explanation": "b ^ c = 6 ^ 2 = (110 ^ 010)_2 = (100)_2 = 4. Then b = 4 + 4 = 8. Then a = 4 + 8 + 2 = 14. Hence a = 14.",
                "difficulty": "medium",
                "tag": "Infosys Pseudocode",
            },
        ],
        "mock_test_title": "Infosys Special Program Aptitude Booster",
        "mock_test_id": "infosys-special-program-aptitude-booster",
    },
    "cognizant": {
        "slug": "cognizant",
        "name": "Cognizant (CTS)",
        "badge_text": "Cognizant GenC & Next",
        "icon": "⚡",
        "accent_color": "#0d9488",
        "gradient": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)",
        "tagline": "Leading US multinational technology company recruiting across GenC, GenC Elevate, and GenC Next.",
        "overall_difficulty": "Moderate",
        "hiring_roles": [
            {"title": "GenC", "package": "₹4.00 LPA", "focus": "Quantitative, Analytical, Verbal & Automata Fix"},
            {"title": "GenC Elevate", "package": "₹4.75 LPA", "focus": "Intermediate Problem Solving & Full-Stack Basics"},
            {"title": "GenC Next", "package": "₹6.75 - ₹9.00 LPA", "focus": "Advanced DSA, System Architecture & Cloud Tech"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Aptitude & Communication", "details": "Numerical Ability (25 Qs), Analytical Reasoning (25 Qs), Verbal English (20 Qs) — 80 mins."},
            {"round": "Round 2: Automata Fix (Code Debugging)", "details": "7 buggy code snippets in C/C++/Java to fix syntax and logical bugs in 20 minutes."},
            {"round": "Round 3: Technical Interview", "details": "Coding, OOPs, DBMS queries, basic networking, and academic project review."},
            {"round": "Round 4: HR Discussion", "details": "Career goals, adaptability, team dynamics, and shift readiness."},
        ],
        "exam_pattern": [
            {"section": "Quantitative Ability", "questions": 25, "time_mins": 35, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Analytical Reasoning", "questions": 25, "time_mins": 30, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Verbal English", "questions": 20, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "60%"},
            {"section": "Automata Fix (Debugging)", "questions": 7, "time_mins": 20, "marking": "Testcases passed", "cutoff": "5 of 7 fixed"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Profit, Loss & Discounts", "weight": "25%", "freq": "Very High", "tips": "Successive discounts and marked price problems appear in every GenC exam."},
                {"topic": "Time & Distance / Boats", "weight": "20%", "freq": "High", "tips": "Upstream/downstream speed ratio problems."},
                {"topic": "Percentages & Mixtures", "weight": "20%", "freq": "High", "tips": "Rule of Alligation for mixing liquids of different purities."},
                {"topic": "Simple & Compound Interest", "weight": "20%", "freq": "High", "tips": "Difference between CI and SI for 2 and 3 years: $D = P(R/100)^2$."},
                {"topic": "Number Properties", "weight": "15%", "freq": "Medium", "tips": "Divisibility rules of 7, 11, 13, and prime factorization."},
            ],
            "reasoning_trends": [
                {"topic": "Coding-Decoding & Analogies", "weight": "30%", "freq": "Very High", "tips": "Matrix coding and letter shifting based on alphabetical order."},
                {"topic": "Statement & Conclusions", "weight": "25%", "freq": "High", "tips": "Strict logical deductions without assuming unstated real-world facts."},
                {"topic": "Direction Sense & Angles", "weight": "25%", "freq": "High", "tips": "Turning 45°, 90°, 135° clockwise/anticlockwise."},
                {"topic": "Blood Relations", "weight": "20%", "freq": "High", "tips": "Pointing to a photograph / coded relations (A + B means A is father of B)."},
            ],
            "verbal_trends": [
                {"topic": "Grammar & Spotting Errors", "weight": "40%", "freq": "Very High", "tips": "Tenses, subject-verb agreement, and correct usage of conjunctions."},
                {"topic": "Sentence Improvement", "weight": "30%", "freq": "High", "tips": "Replacing underlined phrases with concise, correct alternatives."},
                {"topic": "Reading Comprehension", "weight": "30%", "freq": "High", "tips": "Direct factual questions with clear answers in the text."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Practice 25 Automata Fix debugging questions (look for off-by-one loop errors, missing base cases in recursion, and pointer mistakes).",
            "Week 2: Focus heavily on Profit/Loss, Alligations, and Direction Sense.",
            "Week 3: Daily English grammar drills on Subject-Verb agreement and Pronoun antecedent matching.",
            "Week 4: Take Cognizant GenC full-length mock tests on this platform.",
        ],
        "sample_questions": [
            {
                "question": "The difference between the Compound Interest and Simple Interest on a sum of money for 2 years at 10% per annum is ₹65. What is the sum?",
                "options": ["₹5,500", "₹6,000", "₹6,500", "₹7,000"],
                "correct_option_index": 2,
                "explanation": "Shortcut for 2 years: Difference = P × (R / 100)^2. Here, 65 = P × (10 / 100)^2 = P × (1/100). Therefore, P = 65 × 100 = ₹6,500.",
                "difficulty": "medium",
                "tag": "Cognizant Quant",
            },
        ],
        "mock_test_title": "Cognizant GenC Analytical & Placement Mock",
        "mock_test_id": "cognizant-genc-analytical-placement-mock",
    },
    "accenture": {
        "slug": "accenture",
        "name": "Accenture",
        "badge_text": "Accenture ASE & FSE",
        "icon": "⚡",
        "accent_color": "#7c3aed",
        "gradient": "linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%)",
        "tagline": "Global professional services giant hiring for Associate Software Engineer (ASE) and Full Stack Engineer (FSE).",
        "overall_difficulty": "Moderate",
        "hiring_roles": [
            {"title": "Associate Software Engineer (ASE)", "package": "₹4.50 LPA", "focus": "Cognitive Ability, Technical Assessment & Coding"},
            {"title": "Advanced / Full Stack Engineer (FSE)", "package": "₹6.50 - ₹11.00 LPA", "focus": "System Design, Microservices & Advanced Coding"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Cognitive & Technical Assessment", "details": "English Ability (17 Qs), Critical Reasoning (18 Qs), Abstract Reasoning (15 Qs), Common Apps & MS Office (12 Qs), Pseudocode (18 Qs), Networking & Cloud (10 Qs) — 90 mins total."},
            {"round": "Round 2: Coding Assessment", "details": "2 Coding problems (Strings, Arrays, Mathematical logic) in 45 mins. Mandatory cutoff."},
            {"round": "Round 3: Communication Assessment", "details": "AI-proctored speech test evaluating pronunciation, fluency, listening, and grammar."},
            {"round": "Round 4: Technical & HR Interview", "details": "Combined interview discussing project, teamwork, leadership, and problem-solving."},
        ],
        "exam_pattern": [
            {"section": "English Ability", "questions": 17, "time_mins": 15, "marking": "+1, No Negative", "cutoff": "60%"},
            {"section": "Critical & Problem Solving", "questions": 18, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Abstract Reasoning", "questions": 15, "time_mins": 15, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Common Tech & MS Office", "questions": 12, "time_mins": 10, "marking": "+1, No Negative", "cutoff": "60%"},
            {"section": "Pseudocode", "questions": 18, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Network Security & Cloud", "questions": 10, "time_mins": 10, "marking": "+1, No Negative", "cutoff": "60%"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Critical Reasoning & Abstract Math", "weight": "35%", "freq": "Signature", "tips": "Accenture uniquely tests Critical Reasoning (Statement-Argument, Flowcharts, Data Arrangements) rather than traditional pure quant."},
                {"topic": "Pseudocode Tracing", "weight": "35%", "freq": "Very High", "tips": "Heavy testing on bitwise operators (`AND`, `OR`, `XOR`, left/right shift) and nested loops."},
                {"topic": "Abstract Reasoning", "weight": "30%", "freq": "High", "tips": "Shape matrices, visual analog patterns, and sequence continuation."},
            ],
            "reasoning_trends": [
                {"topic": "Critical Thinking & Assumptions", "weight": "40%", "freq": "Very High", "tips": "Determine if arguments are strong or weak based on facts, not emotions."},
                {"topic": "Data Arrangements & Matrix Logic", "weight": "30%", "freq": "High", "tips": "Tabular puzzles matching employees to projects and cities."},
                {"topic": "Visual & Spatial Reasoning", "weight": "30%", "freq": "High", "tips": "Clockwise shape rotations and geometric pattern additions."},
            ],
            "verbal_trends": [
                {"topic": "Vocabulary & Synonyms", "weight": "30%", "freq": "High", "tips": "Advanced academic vocabulary and idioms."},
                {"topic": "Grammar & Prepositions", "weight": "40%", "freq": "Very High", "tips": "Active vs passive voice, indirect speech conversions."},
                {"topic": "Reading Comprehension", "weight": "30%", "freq": "High", "tips": "Direct questions with straightforward inferences."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Master bitwise operators (`XOR`, `AND`, `OR`, `NOT`) in C/Java pseudocode. Practice dry-running recursive loops.",
            "Week 2: Solve 50 Abstract Reasoning visual matrices.",
            "Week 3: Revise Computer Fundamentals: MS Excel formulas (VLOOKUP, IF), Cloud types (IaaS/PaaS/SaaS), and OSI Model.",
            "Week 4: Take Accenture mock assessments and practice speaking clearly for the AI Communication Assessment.",
        ],
        "sample_questions": [
            {
                "question": "What is the output of the following pseudocode?\nInteger a, b, c\nSet a = 2, b = 3, c = 4\na = (b ^ c) + (a & b)\nPrint a",
                "options": ["7", "9", "11", "13"],
                "correct_option_index": 1,
                "explanation": "b ^ c = 3 ^ 4 = (011 ^ 100)_2 = (111)_2 = 7. a & b = 2 & 3 = (010 & 011)_2 = (010)_2 = 2. a = 7 + 2 = 9.",
                "difficulty": "medium",
                "tag": "Accenture Pseudocode",
            },
        ],
        "mock_test_title": "Accenture Cognitive & Technical Mock Test",
        "mock_test_id": "accenture-cognitive-technical-mock-test",
    },
    "wipro": {
        "slug": "wipro",
        "name": "Wipro",
        "badge_text": "Wipro Elite NTH",
        "icon": "🌐",
        "accent_color": "#d97706",
        "gradient": "linear-gradient(135deg, #b45309 0%, #f59e0b 100%)",
        "tagline": "Global information technology corporation hiring engineering graduates through Elite National Talent Hunt (NTH).",
        "overall_difficulty": "Moderate",
        "hiring_roles": [
            {"title": "Project Engineer (Elite)", "package": "₹3.50 LPA", "focus": "Quantitative, Logical, Verbal, Essay Writing & Coding"},
            {"title": "Turbo Cadre", "package": "₹6.50 LPA", "focus": "Advanced Algorithmic Coding & Core Architecture"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Online Assessment", "details": "Quantitative (16 Qs, 16m), Logical (14 Qs, 14m), Verbal (22 Qs, 18m), Essay Writing (1 topic, 20m), Coding (2 Qs, 60m)."},
            {"round": "Round 2: Technical Interview", "details": "C/C++/Java/Python basics, OOPs, DBMS concepts, and final year project."},
            {"round": "Round 3: HR Interview", "details": "Behavioral questions, career aspirations, and relocation readiness."},
        ],
        "exam_pattern": [
            {"section": "Quantitative Ability", "questions": 16, "time_mins": 16, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Logical Ability", "questions": 14, "time_mins": 14, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Verbal Ability", "questions": 22, "time_mins": 18, "marking": "+1, No Negative", "cutoff": "60%"},
            {"section": "Written Communication (Essay)", "questions": 1, "time_mins": 20, "marking": "AI Evaluation", "cutoff": "Pass (Grammar, Structure)"},
            {"section": "Coding (2 Questions)", "questions": 2, "time_mins": 60, "marking": "Automated Testcases", "cutoff": "1+ problem solved"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "HCF, LCM & Divisibility", "weight": "25%", "freq": "Very High", "tips": "Highest common factor word problems and prime factorization."},
                {"topic": "Time & Work / Pipes", "weight": "25%", "freq": "Very High", "tips": "Work rate and inlet/outlet tank filling times."},
                {"topic": "Averages & Mixtures", "weight": "25%", "freq": "High", "tips": "Batting averages, age averages, and alligation ratios."},
                {"topic": "Percentages & Ratios", "weight": "25%", "freq": "High", "tips": "Simple direct calculations with minimal trickery."},
            ],
            "reasoning_trends": [
                {"topic": "Deductive Reasoning & Syllogisms", "weight": "35%", "freq": "Very High", "tips": "Standard two-premise syllogisms with clear Venn relationships."},
                {"topic": "Blood Relations", "weight": "35%", "freq": "Very High", "tips": "Linear generation diagrams."},
                {"topic": "Number & Alphabet Series", "weight": "30%", "freq": "High", "tips": "Differences of squares and alternating primes."},
            ],
            "verbal_trends": [
                {"topic": "Synonyms & Antonyms", "weight": "35%", "freq": "High", "tips": "Standard GRE/GMAT basic word list."},
                {"topic": "Sentence Completion", "weight": "35%", "freq": "High", "tips": "Fill in the blank with suitable prepositions/tenses."},
                {"topic": "Reading Comprehension", "weight": "30%", "freq": "Medium", "tips": "Direct factual extraction from short paragraphs."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Practice speed: Wipro gives exactly 1 minute per question (16 Qs in 16 mins). Never spend > 45s on one math problem.",
            "Week 2: Essay writing practice: Write 300 words on current tech topics (AI ethics, remote work, renewable energy). Keep spelling and punctuation perfect.",
            "Week 3: Practice basic array/string coding problems in C or Java (palindrome, frequency count, second largest element).",
            "Week 4: Full-length Wipro mock exam on this platform.",
        ],
        "sample_questions": [
            {
                "question": "The HCF of two numbers is 11 and their LCM is 7700. If one of the numbers is 275, find the other number.",
                "options": ["279", "283", "308", "318"],
                "correct_option_index": 2,
                "explanation": "Formula: Product of two numbers = HCF × LCM. Therefore, Other Number = (11 × 7700) / 275 = 84700 / 275 = 308.",
                "difficulty": "easy",
                "tag": "Wipro Quant",
            },
        ],
        "mock_test_title": "Wipro Elite NTH Placement Mock Test",
        "mock_test_id": "wipro-elite-nth-placement-mock-test",
    },
    "amazon": {
        "slug": "amazon",
        "name": "Amazon",
        "badge_text": "Amazon SDE-1 / WOW",
        "icon": "📦",
        "accent_color": "#ea580c",
        "gradient": "linear-gradient(135deg, #c2410c 0%, #f97316 100%)",
        "tagline": "Global e-commerce and cloud (AWS) titan hiring university graduates for Software Development Engineer (SDE-1).",
        "overall_difficulty": "High to Very High",
        "hiring_roles": [
            {"title": "Software Development Engineer (SDE-1)", "package": "₹28.00 - ₹45.00 LPA", "focus": "Algorithms, Dynamic Programming, Trees/Graphs & Leadership Principles"},
            {"title": "Quality Assurance Engineer (QAE)", "package": "₹16.00 - ₹24.00 LPA", "focus": "Test Automation, Scripting & Code Quality"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Online Assessment 1 (Code Debugging & DSA)", "details": "7 Debugging questions (20m) + 2 Algorithmic Coding problems (70m)."},
            {"round": "Round 2: Online Assessment 2 (Work Style & Behavioral)", "details": "Work Simulation (acting as SDE addressing tickets, prioritizing deadlines) + Amazon 16 Leadership Principles survey (90m)."},
            {"round": "Round 3: Technical Interview 1", "details": "Live coding: Trees, Graphs, HashMaps, Sliding Window + 2 Leadership questions."},
            {"round": "Round 4: Technical Interview 2", "details": "Dynamic Programming, Recursion, Object-Oriented Design (OOD) + 2 Leadership questions."},
            {"round": "Round 5: Bar Raiser Interview", "details": "Senior external leader evaluating long-term engineering rigor and culture fit."},
        ],
        "exam_pattern": [
            {"section": "Code Debugging", "questions": 7, "time_mins": 20, "marking": "Testcases", "cutoff": "6 of 7"},
            {"section": "Coding Problems (2 DSA)", "questions": 2, "time_mins": 70, "marking": "All Testcases & Complexity", "cutoff": "Both Solved (Optimal O(N) or O(N log N))"},
            {"section": "Work Simulation (SDE Scenarios)", "questions": 15, "time_mins": 60, "marking": "Leadership Alignment", "cutoff": "High Fit"},
            {"section": "Leadership Principles Survey", "questions": 45, "time_mins": 30, "marking": "Consistency Score", "cutoff": "Pass"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Algorithmic Math & Complexity", "weight": "40%", "freq": "Very High", "tips": "Amazon focuses on Big-O space/time optimization rather than pure arithmetic speed."},
                {"topic": "Combinatorics & Graph Math", "weight": "35%", "freq": "Very High", "tips": "Paths on a grid, topological ordering math, and binary tree height calculations."},
                {"topic": "Bit Manipulation", "weight": "25%", "freq": "High", "tips": "Bitmasking, single non-repeating number, and counting set bits in $O(1)$."},
            ],
            "reasoning_trends": [
                {"topic": "Amazon 16 Leadership Principles", "weight": "60%", "freq": "Crucial Gate", "tips": "Every candidate MUST know: Customer Obsession, Ownership, Bias for Action, Dive Deep, Earn Trust, Deliver Results."},
                {"topic": "Work Style Simulation", "weight": "40%", "freq": "Very High", "tips": "Always prioritize customer safety, data integrity, and root cause analysis over quick hacks."},
            ],
            "verbal_trends": [
                {"topic": "Professional Technical Writing", "weight": "50%", "freq": "High", "tips": "Clarity, concise PR descriptions, and professional email etiquette."},
                {"topic": "STAR Method Responses", "weight": "50%", "freq": "Crucial", "tips": "Situation, Task, Action, Result with quantifiable metrics."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Master DSA patterns: Two Pointers, Sliding Window, Fast/Slow Pointers, Top-K elements (Heap).",
            "Week 2: Deep dive into Trees and Graphs (DFS, BFS, Dijkstra, Cycle Detection in Directed/Undirected graphs).",
            "Week 3: Write down 2 concrete real-life stories for each of the top 6 Amazon Leadership Principles using the STAR framework.",
            "Week 4: Practice mock live coding interviews while narrating your thought process out loud.",
        ],
        "sample_questions": [
            {
                "question": "Which Amazon Leadership Principle emphasizes that leaders look for root causes, stay connected to details, and audit frequently?",
                "options": ["Customer Obsession", "Dive Deep", "Bias for Action", "Think Big"],
                "correct_option_index": 1,
                "explanation": "'Dive Deep': Leaders operate at all levels, stay connected to the details, audit frequently, and are skeptical when metrics and anecdote differ. No task is beneath them.",
                "difficulty": "medium",
                "tag": "Amazon Leadership Principles",
            },
        ],
        "mock_test_title": "Amazon SDE-1 Technical Aptitude & Coding Foundations Mock",
        "mock_test_id": "amazon-sde-1-technical-aptitude-mock",
    },
    "deloitte": {
        "slug": "deloitte",
        "name": "Deloitte (USI)",
        "badge_text": "Deloitte USI Placement",
        "icon": "🟢",
        "accent_color": "#15803d",
        "gradient": "linear-gradient(135deg, #166534 0%, #22c55e 100%)",
        "tagline": "Top global professional services and consulting firm hiring Analyst and Associate Analyst roles.",
        "overall_difficulty": "Moderate",
        "hiring_roles": [
            {"title": "Associate Analyst", "package": "₹4.50 - ₹5.00 LPA", "focus": "Quantitative, Logical, Verbal & Computer Fundamentals"},
            {"title": "Technology Analyst", "package": "₹7.60 - ₹8.50 LPA", "focus": "SQL, Web Technologies, Cloud & Solution Architecture"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Online Aptitude Assessment", "details": "Quantitative (25 Qs), Logical (25 Qs), Verbal English (25 Qs) — 75 mins total."},
            {"round": "Round 2: Computer Fundamentals & Technical MCQ", "details": "C/Java fundamentals, DBMS/SQL, OOPs, Computer Networks (30 Qs, 30 mins)."},
            {"round": "Round 3: Group Discussion / Case Study", "details": "Discussion on contemporary business or technology scenarios with 8-10 candidates."},
            {"round": "Round 4: Technical & HR Interview", "details": "Resume projects, business scenario solving, leadership in college clubs, and communication."},
        ],
        "exam_pattern": [
            {"section": "Quantitative Ability", "questions": 25, "time_mins": 25, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Logical Reasoning", "questions": 25, "time_mins": 25, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Verbal Ability", "questions": 25, "time_mins": 25, "marking": "+1, No Negative", "cutoff": "60%"},
            {"section": "Computer Fundamentals", "questions": 30, "time_mins": 30, "marking": "+1, No Negative", "cutoff": "65%"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Data Interpretation (Charts & Tables)", "weight": "30%", "freq": "Signature", "tips": "Deloitte is a consulting firm: heavy testing of Bar Charts, Pie Charts, and multi-variable Data Interpretation tables."},
                {"topic": "Profit, Loss & Commercial Math", "weight": "25%", "freq": "Very High", "tips": "Compound Interest, discounts, and partnership profit shares."},
                {"topic": "Ratios & Mixtures", "weight": "25%", "freq": "High", "tips": "Replacement of milk and water in containers."},
                {"topic": "Time & Work", "weight": "20%", "freq": "High", "tips": "Men, women and children combined efficiency rates."},
            ],
            "reasoning_trends": [
                {"topic": "Logical Deductions & Syllogisms", "weight": "35%", "freq": "Very High", "tips": "Three-statement syllogisms with 'Definitely True' conclusions."},
                {"topic": "Seating Arrangement", "weight": "35%", "freq": "Very High", "tips": "Linear row facing North/South and rectangular table seating."},
                {"topic": "Blood Relations & Directions", "weight": "30%", "freq": "High", "tips": "Coded family trees and multi-step directional journeys."},
            ],
            "verbal_trends": [
                {"topic": "Reading Comprehension", "weight": "40%", "freq": "Very High", "tips": "Lengthy business consulting case passages (400 words) with tone and central idea questions."},
                {"topic": "Sentence Correction & Grammar", "weight": "35%", "freq": "High", "tips": "Parallelism, modifier errors, and idiom usage."},
                {"topic": "Para Jumbles", "weight": "25%", "freq": "High", "tips": "Logical narrative sequencing."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Practice Data Interpretation daily: calculate percentage growth and ratio comparisons from complex tables in < 60 seconds.",
            "Week 2: Revise Computer Fundamentals: SQL JOINs, Normalization, ACID, and OOP concepts.",
            "Week 3: Participate in mock Group Discussions: practice structured opening, polite interventions, and concise summaries.",
            "Week 4: Attempt timed Deloitte placement mock tests on this platform.",
        ],
        "sample_questions": [
            {
                "question": "A container contains 60 litres of pure milk. 6 litres are withdrawn and replaced with water. This process is repeated once more. How much milk is left in the container?",
                "options": ["48.6 litres", "49.2 litres", "50.4 litres", "51.2 litres"],
                "correct_option_index": 0,
                "explanation": "Formula: Remaining liquid = Initial × [1 - (x / V)]^n. Remaining Milk = 60 × [1 - (6/60)]^2 = 60 × (0.9)^2 = 60 × 0.81 = 48.6 litres.",
                "difficulty": "medium",
                "tag": "Deloitte Quant",
            },
        ],
        "mock_test_title": "Deloitte USI Placement Aptitude Mock Test",
        "mock_test_id": "deloitte-usi-placement-aptitude-mock-test",
    },
    "capgemini": {
        "slug": "capgemini",
        "name": "Capgemini",
        "badge_text": "Capgemini Exceller",
        "icon": "🔷",
        "accent_color": "#0284c7",
        "gradient": "linear-gradient(135deg, #0369a1 0%, #38bdf8 100%)",
        "tagline": "French multinational information technology services and consulting company hiring via Exceller drive.",
        "overall_difficulty": "Moderate",
        "hiring_roles": [
            {"title": "Software Analyst", "package": "₹4.00 - ₹4.25 LPA", "focus": "Pseudocode, Technical MCQ, English & Game Aptitude"},
            {"title": "Senior Software Analyst", "package": "₹5.75 - ₹7.50 LPA", "focus": "Advanced Coding, Cloud & DSA Optimization"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Technical Assessment", "details": "Pseudocode (30 Qs, 30m) + English Communication (30 Qs, 30m)."},
            {"round": "Round 2: Game-Based Aptitude", "details": "4 interactive mini-games (Grid Challenge, Motion Challenge, Deductive-logical game) testing cognitive agility in 24 mins."},
            {"round": "Round 3: Behavioral Profiling", "details": "100 personality trait questions with no right/wrong answers."},
            {"round": "Round 4: Technical & HR Interview", "details": "Resume deep dive, basic C/Java logic, SQL queries, and situational questions."},
        ],
        "exam_pattern": [
            {"section": "Pseudocode", "questions": 30, "time_mins": 30, "marking": "+1, No Negative", "cutoff": "70%"},
            {"section": "English Communication", "questions": 30, "time_mins": 30, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Game-Based Aptitude", "questions": 4, "time_mins": 24, "marking": "Cognitive score", "cutoff": "High percentile"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Data Structures in Pseudocode", "weight": "40%", "freq": "Signature", "tips": "Capgemini heavily uses pseudocode syntax to test arrays, stacks, and recursion."},
                {"topic": "Bitwise Operations & Math Logic", "weight": "35%", "freq": "Very High", "tips": "Bitwise shifts, modulo arithmetic, and nested loops."},
                {"topic": "Game-Based Numerical Challenges", "weight": "25%", "freq": "High", "tips": "Quick mental arithmetic while tracking moving objects on screen."},
            ],
            "reasoning_trends": [
                {"topic": "Deductive & Inductive Logic Games", "weight": "50%", "freq": "High", "tips": "Identify rules governing geometric shifts across 3x3 grids."},
                {"topic": "Spatial Reasoning", "weight": "50%", "freq": "High", "tips": "Mental rotation of 3D objects and ball-drop trajectory predictions."},
            ],
            "verbal_trends": [
                {"topic": "Spelling, Grammar & Vocabulary", "weight": "50%", "freq": "Very High", "tips": "Identify misspelled words, correct tense shifts, and prepositions."},
                {"topic": "Reading Comprehension", "weight": "50%", "freq": "High", "tips": "Short passages with direct factual questions."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Solve 100 Capgemini pseudocode questions. Focus on while loop break conditions and bitwise masking.",
            "Week 2: Practice game-based cognitive aptitude apps (grid memory, mental math speed).",
            "Week 3: Revise core English grammar (Subject-Verb agreement, Active-Passive, Direct-Indirect speech).",
            "Week 4: Attempt timed Capgemini mock test on this platform.",
        ],
        "sample_questions": [
            {
                "question": "What will be the output of the following pseudocode?\nInteger a, b, c\nSet a = 1, b = 2, c = 3\nif (a + b > c && c - b < a)\n    a = a + b + c\nelse\n    a = a * b * c\nend if\nPrint a",
                "options": ["6", "0", "12", "5"],
                "correct_option_index": 0,
                "explanation": "Condition check: a + b = 1 + 2 = 3. Is 3 > 3? False! Because the first condition of && is false, the else branch executes: a = 1 * 2 * 3 = 6.",
                "difficulty": "medium",
                "tag": "Capgemini Pseudocode",
            },
        ],
        "mock_test_title": "Capgemini Pseudo-Code & Technical Aptitude Mock Test",
        "mock_test_id": "capgemini-pseudocode-technical-mock-test",
    },
    "goldman_sachs": {
        "slug": "goldman_sachs",
        "name": "Goldman Sachs",
        "badge_text": "Goldman Sachs ECHP",
        "icon": "🏛️",
        "accent_color": "#1e293b",
        "gradient": "linear-gradient(135deg, #0f172a 0%, #334155 100%)",
        "tagline": "Top global investment bank hiring engineers via the Engineering Campus Hiring Program (ECHP).",
        "overall_difficulty": "Very High",
        "hiring_roles": [
            {"title": "Summer Analyst / Full-Time Analyst", "package": "₹22.00 - ₹34.00 LPA", "focus": "Higher Math, Complex DSA, Algorithms, OS, DBMS & Financial Acumen"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Aptitude & Technical Assessment", "details": "Numerical Computation (8 Qs), Numerical Reasoning (6 Qs), Reasoning (12 Qs), Advanced Math (8 Qs), Programming (2 coding Qs, 45m), CS Subject MCQs (7 Qs) — 135 mins total."},
            {"round": "Round 2: Technical Interview 1", "details": "Advanced Data Structures, Probability puzzles, and algorithmic optimization."},
            {"round": "Round 3: Technical Interview 2", "details": "Low-level system design, concurrency, memory management, and project deep-dive."},
            {"round": "Round 4: Senior Partner Interview", "details": "Values, high-pressure problem solving, integrity, and cultural fit."},
        ],
        "exam_pattern": [
            {"section": "Numerical Computation & Reasoning", "questions": 14, "time_mins": 25, "marking": "+5, -2 Negative", "cutoff": "70%"},
            {"section": "Abstract & Diagrammatic Reasoning", "questions": 12, "time_mins": 20, "marking": "+5, -2 Negative", "cutoff": "70%"},
            {"section": "Advanced Mathematics", "questions": 8, "time_mins": 20, "marking": "+5, -2 Negative", "cutoff": "65%"},
            {"section": "Programming (2 Coding)", "questions": 2, "time_mins": 45, "marking": "Automated", "cutoff": "Both Solved"},
            {"section": "Core Computer Science", "questions": 7, "time_mins": 15, "marking": "+4, -1 Negative", "cutoff": "70%"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Advanced Probability & Combinatorics", "weight": "40%", "freq": "Signature", "tips": "Bayes' Theorem, expected value of random variables, and poker/dice conditional probability."},
                {"topic": "Linear Algebra & Calculus", "weight": "30%", "freq": "Very High", "tips": "Matrix determinants, eigenvalues, limits, and derivative maxima/minima."},
                {"topic": "Number Theory", "weight": "30%", "freq": "High", "tips": "Modular arithmetic, Euler's totient function, and prime factorizations."},
            ],
            "reasoning_trends": [
                {"topic": "Mathematical Puzzles", "weight": "50%", "freq": "Very High", "tips": "Classic brainteasers: River crossing, burning ropes, measuring water with jugs, and coin weighing."},
                {"topic": "Logical Deductions & Truth-Tellers", "weight": "50%", "freq": "High", "tips": "Knights and Knaves logic puzzles."},
            ],
            "verbal_trends": [
                {"topic": "Critical Analysis", "weight": "100%", "freq": "High", "tips": "Evaluate mathematical validity of financial/logical arguments."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Practice Advanced Probability: Expected values, coin tossing until streak of heads, Bayes' theorem.",
            "Week 2: Solve the Top 50 Interview Puzzles (available in our Study Materials section).",
            "Week 3: Practice Hard DSA: Dynamic Programming on Trees, Segment Trees, and Disjoint Set Union (DSU).",
            "Week 4: Take Goldman Sachs timed mock assessment under negative marking simulation (+5 / -2).",
        ],
        "sample_questions": [
            {
                "question": "You have a 3-litre jug and a 5-litre jug with unlimited water. How can you measure exactly 4 litres of water?",
                "options": [
                    "Fill 3L, pour into 5L; fill 3L again, top up 5L (leaving 1L in 3L jug); empty 5L, pour 1L into 5L, fill 3L and add to 5L = 4L",
                    "Fill 5L, pour into 3L, leaving 2L; pour out 3L, add 2L, fill 5L = 4L",
                    "Fill 5L halfway",
                    "Cannot be done"
                ],
                "correct_option_index": 0,
                "explanation": "Step 1: Fill 3L jug completely. Step 2: Pour into 5L jug (5L has 3L). Step 3: Fill 3L jug again. Step 4: Pour into 5L until full (transfers 2L; 1L remains in 3L jug). Step 5: Empty 5L jug. Step 6: Pour the 1L from 3L jug into 5L jug. Step 7: Fill 3L jug completely and pour into 5L jug. Total in 5L jug = 1L + 3L = 4L.",
                "difficulty": "hard",
                "tag": "Goldman Sachs Puzzle",
            },
        ],
        "mock_test_title": "Goldman Sachs Aptitude & Advanced Math Mock Test",
        "mock_test_id": "goldman-sachs-aptitude-math-mock-test",
    },
    "zoho": {
        "slug": "zoho",
        "name": "Zoho",
        "badge_text": "Zoho Software Developer",
        "icon": "🔴",
        "accent_color": "#dc2626",
        "gradient": "linear-gradient(135deg, #b91c1c 0%, #ef4444 100%)",
        "tagline": "Privately-held SaaS giant known for intensive logic building, C/Java pointer puzzles, and zero reliance on frameworks.",
        "overall_difficulty": "High",
        "hiring_roles": [
            {"title": "Software Developer", "package": "₹5.50 - ₹8.50 LPA", "focus": "Pure Logic Building, Pointers, Recursion & Application Design"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Written General Aptitude & C/Java Output", "details": "Aptitude (20 Qs) + Output Prediction in C/Java (20 Qs with heavy pointers, bitwise, precedence) — 90 mins."},
            {"round": "Round 2: Basic Programming Round", "details": "5 coding problems (Patterns, Matrix operations, String manipulation) with NO built-in library functions allowed."},
            {"round": "Round 3: Advanced Programming Round (Application Design)", "details": "Build a real-world console application (e.g. Railway Reservation, Snake Game, Splitwise, Taxi Booking System) in 3 hours."},
            {"round": "Round 4: Technical Interview", "details": "Walk through your console app architecture, handle edge cases, and solve whiteboard puzzles."},
            {"round": "Round 5: HR Interview", "details": "Company culture, long-term commitment, humility, and passions."},
        ],
        "exam_pattern": [
            {"section": "General Aptitude", "questions": 20, "time_mins": 45, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "C / Java Output Prediction", "questions": 20, "time_mins": 45, "marking": "+1, No Negative", "cutoff": "70%"},
            {"section": "Basic Programming (5 Problems)", "questions": 5, "time_mins": 120, "marking": "Manual Code Review", "cutoff": "4 of 5 solved"},
            {"section": "Advanced App Design", "questions": 1, "time_mins": 180, "marking": "Architecture & Logic", "cutoff": "Complete working model"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Time & Work, Pipes", "weight": "30%", "freq": "High", "tips": "Direct word problems testing basic mathematical rigor."},
                {"topic": "Speed & Distance, Clocks", "weight": "35%", "freq": "Very High", "tips": "Clock angle between hour and minute hand, faulty clocks."},
                {"topic": "Profit, Loss & Ratio", "weight": "35%", "freq": "High", "tips": "Standard commercial math."},
            ],
            "reasoning_trends": [
                {"topic": "C Pointers & Operator Precedence", "weight": "50%", "freq": "Signature", "tips": "Pre/post increment `++i + i++`, pointer arithmetic `*p++ vs (*p)++`, and static variable scopes."},
                {"topic": "Recursion Output", "weight": "50%", "freq": "Signature", "tips": "Traced return stacks for tricky recursive functions."},
            ],
            "verbal_trends": [
                {"topic": "Basic English", "weight": "100%", "freq": "Low", "tips": "Zoho does not heavily filter on verbal; focus is 90% on logic."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Master C pointer mechanics: pointers to pointers (`**ptr`), array of pointers, string manipulation using `while(*str++)`.",
            "Week 2: Practice matrix manipulations (spiral print, 90 degree rotation, snake pattern) without any external libraries.",
            "Week 3: Implement 3 full console projects: Railway Reservation System, ATM Banking System, and Snake & Ladder game.",
            "Week 4: Take Zoho logic assessment on this platform.",
        ],
        "sample_questions": [
            {
                "question": "What is the angle between the hour hand and minute hand of a clock at 3:40 PM?",
                "options": ["120°", "130°", "140°", "150°"],
                "correct_option_index": 1,
                "explanation": "Formula: Angle = |30H - 5.5M| where H=3, M=40. Angle = |30(3) - 5.5(40)| = |90 - 220| = |-130| = 130°.",
                "difficulty": "medium",
                "tag": "Zoho Clock Math",
            },
        ],
        "mock_test_title": "Zoho Analytical & C/Java Output Mock Test",
        "mock_test_id": "zoho-analytical-c-java-mock-test",
    },
    "google": {
        "slug": "google",
        "name": "Google",
        "badge_text": "Google University Grad & STEP",
        "icon": "🌐",
        "accent_color": "#4285f4",
        "gradient": "linear-gradient(135deg, #1a73e8 0%, #4285f4 100%)",
        "tagline": "Global pioneer in search, distributed systems, and AI hiring through Google Online Challenge (GOC) and technical interview loops.",
        "overall_difficulty": "Very High",
        "hiring_roles": [
            {"title": "Software Engineering Intern (STEP)", "package": "₹1.10 Lakhs/month", "focus": "Data Structures, Recursion, Trees & Problem Solving"},
            {"title": "Software Engineer (L3 University Grad)", "package": "₹32.00 - ₹45.00 LPA", "focus": "Advanced Graph Theory, Dynamic Programming, Scalability & Googleyness"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Google Online Challenge (GOC)", "details": "2 algorithmic problems on HackerEarth/custom platform (60 mins) testing edge-case handling and optimal time complexity."},
            {"round": "Round 2: Technical Phone Screen", "details": "45 mins live coding in Google Docs/internal IDE with Google engineer on Tree traversals or string algorithms."},
            {"round": "Round 3: Onsite / Virtual Coding Loop (3-4 Rounds)", "details": "Deep DSA, Dynamic Programming on Trees/DAGs, Big-O proof, and code clarity."},
            {"round": "Round 4: Googleyness & Leadership", "details": "Behavioral evaluation on intellectual humility, bias for action, navigating ambiguity, and ethical collaboration."},
        ],
        "exam_pattern": [
            {"section": "Algorithmic Problem 1 (Arrays/Trees/Graphs)", "questions": 1, "time_mins": 30, "marking": "Automated Hidden Testcases", "cutoff": "100% Correctness"},
            {"section": "Algorithmic Problem 2 (DP/Shortest Path/Geometry)", "questions": 1, "time_mins": 30, "marking": "Automated Hidden Testcases", "cutoff": "100% Correctness"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Combinatorics & Discrete Mathematics", "weight": "40%", "freq": "Signature", "tips": "Pigeonhole principle, Catalan numbers, inclusion-exclusion principle, modular inverse."},
                {"topic": "Probability & Expected Value", "weight": "35%", "freq": "High", "tips": "Linearity of Expectation, Markov chains, random walks, and geometric distribution."},
                {"topic": "Number Theory & Bitwise Math", "weight": "25%", "freq": "High", "tips": "Bitwise XOR tricks, GCD Euclidean algorithm, and prime sieve up to 10^7."},
            ],
            "reasoning_trends": [
                {"topic": "Graph Topologies & DAGs", "weight": "40%", "freq": "Very High", "tips": "Recognizing state transitions as directed graphs; finding strongly connected components."},
                {"topic": "Binary Search on Answer Space", "weight": "35%", "freq": "Very High", "tips": "Recognizing monotonic feasibility functions: if f(mid) is feasible, search half range."},
                {"topic": "Game Theory & Minimax", "weight": "25%", "freq": "High", "tips": "Nim sum with XOR, optimal play strategies, and state reduction."},
            ],
            "verbal_trends": [
                {"topic": "Technical Articulation & Thought Communication", "weight": "50%", "freq": "High", "tips": "Google interviewers judge your ability to 'think out loud' and explain trade-offs before writing a single line of code."},
                {"topic": "STAR Behavioral Scenarios", "weight": "50%", "freq": "High", "tips": "Structuring responses with Situation, Task, Action, Result for Googleyness questions."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Master foundational patterns: Two Pointers, Monotonic Queue, Binary Search on Answer space, and Prefix sums.",
            "Week 2: Deep dive into Graphs (DFS/BFS, Dijkstra, Topological Sort, Union-Find with Rank and Path Compression).",
            "Week 3: Dynamic Programming masterclass: Multi-dimensional DP, Bitmask DP, and Knapsack optimization.",
            "Week 4: Mock interview practice: solve problems on a blank whiteboard/doc without syntax highlighting while explaining logic aloud.",
        ],
        "sample_questions": [
            {
                "question": "What is the expected number of fair 6-sided dice rolls required to obtain all 6 faces at least once (Coupon Collector's Problem)?",
                "options": ["14.7 rolls", "12.0 rolls", "18.3 rolls", "21.6 rolls"],
                "correct_option_index": 0,
                "explanation": "By Linearity of Expectation: E[Total] = sum_{i=1}^6 (6 / i) = 6 × (1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6) = 6 × (147/60) = 14.7 rolls.",
                "difficulty": "hard",
                "tag": "Google Quant & Math",
            },
            {
                "question": "Given a directed acyclic graph (DAG) with N nodes, what is the maximum number of directed edges it can have without introducing a cycle?",
                "options": ["N * (N - 1) / 2", "N * (N - 1)", "N * log(N)", "N^2 - 1"],
                "correct_option_index": 0,
                "explanation": "In any topological ordering of N nodes, directed edges can only flow forward from node i to node j (where i < j). The number of such pairs is C(N, 2) = N*(N - 1)/2.",
                "difficulty": "medium",
                "tag": "Google Logic & Graphs",
            },
        ],
        "mock_test_title": "Google Campus Algorithmic & Problem Solving Mock",
        "mock_test_id": "google-campus-algorithmic-mock",
    },
    "microsoft": {
        "slug": "microsoft",
        "name": "Microsoft",
        "badge_text": "Microsoft University Hire & Codess",
        "icon": "🪟",
        "accent_color": "#00a4ef",
        "gradient": "linear-gradient(135deg, #0078d4 0%, #00a4ef 100%)",
        "tagline": "Global cloud and productivity giant hiring campus software engineers through Microsoft Codess, Future Ready, and Campus Onsite Drives.",
        "overall_difficulty": "High",
        "hiring_roles": [
            {"title": "Software Engineering Intern", "package": "₹1.25 Lakhs/month", "focus": "DSA, Clean Code, OOPs, Problem Solving"},
            {"title": "Software Engineer (SDE-1)", "package": "₹16.00 - ₹24.00 LPA", "focus": "Trees, Linked Lists, System Concurrency, Low-Level Design & Quality"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Online Assessment (OA)", "details": "3 coding challenges (90 mins) on Codility or Mettl covering String manipulation, Arrays, and Trees with strict memory limits."},
            {"round": "Round 2: Technical Interview 1", "details": "DSA problem solving, recursion trees, memory leak analysis, and testing corner cases."},
            {"round": "Round 3: Technical Interview 2 (System & OOPs)", "details": "Object-oriented design (e.g. Parking Lot, Elevator), Thread synchronization, and OS memory concepts."},
            {"round": "Round 4: AA (As-Appropriate / Hiring Manager)", "details": "Growth mindset evaluation, past engineering projects, culture fit, and behavioral scenarios."},
        ],
        "exam_pattern": [
            {"section": "Coding Problem 1 (String / Array)", "questions": 1, "time_mins": 30, "marking": "Correctness & Complexity", "cutoff": "100%"},
            {"section": "Coding Problem 2 (Linked List / Tree)", "questions": 1, "time_mins": 30, "marking": "Correctness & Complexity", "cutoff": "100%"},
            {"section": "Coding Problem 3 (DP / Greedy / Matrix)", "questions": 1, "time_mins": 30, "marking": "Correctness & Complexity", "cutoff": "Passes 80%+ tests"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Bit Manipulation & Arithmetic", "weight": "35%", "freq": "Signature", "tips": "Microsoft loves bitwise tricks (single number in duplicate array, power of 2 check: `n & (n-1) == 0`, counting set bits)."},
                {"topic": "Time & Work / Ratios", "weight": "35%", "freq": "High", "tips": "Standard rate equations and proportion balancing in engineering settings."},
                {"topic": "Permutations & Matrix Paths", "weight": "30%", "freq": "High", "tips": "Unique paths in a grid with obstacles and combinatoric formulas."},
            ],
            "reasoning_trends": [
                {"topic": "Tree & Pointer Transformations", "weight": "40%", "freq": "Signature", "tips": "In-place linked list manipulations, tree serialization, and boundary traversals."},
                {"topic": "Low-Level Design Logic", "weight": "35%", "freq": "High", "tips": "SOLID principles, designing clean extensible interfaces without code duplication."},
                {"topic": "Deadlock & Concurrency Tracing", "weight": "25%", "freq": "High", "tips": "Resource allocation graphs, identifying circular wait conditions."},
            ],
            "verbal_trends": [
                {"topic": "Clarity of Thought & Edge-Case Explanation", "weight": "50%", "freq": "High", "tips": "Clearly articulate code modularity, variable naming, and validation of null pointers/bounds."},
                {"topic": "Growth Mindset Scenarios", "weight": "50%", "freq": "High", "tips": "Microsoft values the 'Learn-it-all' over the 'Know-it-all' mindset."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Master Linked Lists and Trees: reversal, cycle detection, lowest common ancestor, and zig-zag level order.",
            "Week 2: Deep dive into Bit Manipulation and String parsing without built-in library shortcuts.",
            "Week 3: Study Low-Level Design (LLD): OOPs design patterns (Singleton, Factory, Observer, Strategy).",
            "Week 4: Practice writing test cases: for every function, write 5 edge-case inputs (null, empty, single element, duplicates, max integers).",
        ],
        "sample_questions": [
            {
                "question": "What does the expression `(x & (x - 1)) == 0` check for any positive integer x?",
                "options": ["Whether x is a power of 2", "Whether x is an even number", "Whether x is a prime number", "Whether x is a multiple of 4"],
                "correct_option_index": 0,
                "explanation": "Subtracting 1 from a power of 2 flips all bits from the lowest set bit downward. Performing a bitwise AND clears that bit; if x is a power of 2 (has exactly one set bit), the result is strictly 0.",
                "difficulty": "medium",
                "tag": "Microsoft Bitwise Math",
            },
            {
                "question": "In an LRU (Least Recently Used) Cache of capacity K, which pair of data structures guarantees both O(1) get and O(1) put operations?",
                "options": ["Doubly Linked List + Hash Map", "Singly Linked List + Binary Search Tree", "Array + Stack", "Min-Heap + Queue"],
                "correct_option_index": 0,
                "explanation": "A Doubly Linked List enables O(1) removal and insertion of nodes at head/tail, and a Hash Map maps keys directly to linked list node pointers for O(1) lookups.",
                "difficulty": "medium",
                "tag": "Microsoft Core Design",
            },
        ],
        "mock_test_title": "Microsoft SDE-1 Campus Technical & Analytical Mock",
        "mock_test_id": "microsoft-sde1-campus-technical-mock",
    },
    "vgen": {
        "slug": "vgen",
        "name": "VGen Software Solutions",
        "badge_text": "🔥 Recently Hired 5 Candidates",
        "icon": "⚡",
        "accent_color": "#2563eb",
        "gradient": "linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)",
        "tagline": "Fast-growing product & engineering firm with active hiring drives for Frontend, Backend, and Software Developers.",
        "overall_difficulty": "Moderate to High",
        "hiring_roles": [
            {"title": "Frontend Developer", "package": "₹6.00 - ₹9.50 LPA", "focus": "HTML/CSS, JavaScript, React, State Management & Responsive UI"},
            {"title": "Backend Developer", "package": "₹7.50 - ₹12.00 LPA", "focus": "Python, SQL, Java, REST APIs & Distributed Systems"},
            {"title": "Software Developer", "package": "₹6.50 - ₹10.00 LPA", "focus": "Core Algorithms, MySQL, OOPs & Data Structures"},
        ],
        "selection_rounds": [
            {"round": "Round 1: AI Pre-Screening & Technical Profile", "details": "WhatsApp & Voice AI screening verifying hands-on stack skills, experience, and domain proficiency."},
            {"round": "Round 2: Aptitude & Technical Challenge", "details": "Quantitative problem solving (15 Qs), Logical analysis (15 Qs), and Technical core MCQs (15 Qs) in 60 mins."},
            {"round": "Round 3: Live Engineering Interview", "details": "Architecture discussion, live coding / debugging, SQL query optimization, and project defense."},
            {"round": "Round 4: HR & Offer Rollout", "details": "Compensation discussion, joining timelines, and team alignment."},
        ],
        "exam_pattern": [
            {"section": "Quantitative Problem Solving", "questions": 15, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "65%"},
            {"section": "Logical & Code Output Reasoning", "questions": 15, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "70%"},
            {"section": "Frontend & Web Architecture", "questions": 15, "time_mins": 15, "marking": "+1, No Negative", "cutoff": "75%"},
            {"section": "Backend, Python & SQL Systems", "questions": 15, "time_mins": 15, "marking": "+1, No Negative", "cutoff": "70%"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Algorithmic Time Complexity", "weight": "35%", "freq": "Very High", "tips": "Focus on Big-O space-time tradeoffs, heap streaming, and tree traversal costs."},
                {"topic": "Time & Work / Sprint Allocation", "weight": "35%", "freq": "High", "tips": "Combined resource efficiency formulas and multi-worker completion timelines."},
                {"topic": "Proportions & Network Speed", "weight": "30%", "freq": "High", "tips": "Relative speed, throughput ratios, and latency calculation problems."},
            ],
            "reasoning_trends": [
                {"topic": "JavaScript Event Loop Tracing", "weight": "40%", "freq": "Signature", "tips": "Execution order of synchronous call stack, microtask queue (Promises), and macrotasks (setTimeout)."},
                {"topic": "Trie & String Search Logic", "weight": "35%", "freq": "Very High", "tips": "Prefix lookups, pattern matching, and dictionary optimizations."},
                {"topic": "Condition & Loop Logic Tracing", "weight": "25%", "freq": "High", "tips": "Nested loops, recursion unwinding, and bitwise logic."},
            ],
            "verbal_trends": [
                {"topic": "Engineering Communication", "weight": "50%", "freq": "High", "tips": "Technical articulation of system trade-offs and concise documentation."},
                {"topic": "Code Review & Error Spotting", "weight": "50%", "freq": "Very High", "tips": "Identifying subtle bug patterns and security pitfalls."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Practice Frontend basics: JavaScript Event Loop, closures, Promises, React rendering cycles, and CSS layout algorithms.",
            "Week 2: Master Backend fundamentals: Database indexing (B-Tree vs Hash), SQL JOINs, Python memory/GC, and REST status codes.",
            "Week 3: Daily timed practice of 20 Quantitative and Logical aptitude questions under strict 45-second timers.",
            "Week 4: Attempt full VGen recruiter mock tests and review questions asked to recently hired candidates.",
        ],
        "sample_questions": [],
        "mock_test_title": "VGen Software Developer Aptitude & Technical Mock Exam",
        "mock_test_id": "vgen-software-developer-aptitude-mock",
    },
    "vaarg": {
        "slug": "vaarg",
        "name": "Vaarg Technologies",
        "badge_text": "🔥 Recently Hired 5 Candidates",
        "icon": "🤖",
        "accent_color": "#7c3aed",
        "gradient": "linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%)",
        "tagline": "Next-generation AI and intelligent recruiting platform actively hiring AI Developers, Frontend Engineers, and Talent Partners.",
        "overall_difficulty": "High",
        "hiring_roles": [
            {"title": "AI Developer", "package": "₹8.00 - ₹15.00 LPA", "focus": "PyTorch, Vector Embeddings, LLM Prompting, Python & Deep Learning"},
            {"title": "Frontend Developer", "package": "₹6.00 - ₹10.00 LPA", "focus": "Modern JavaScript, Debouncing, React Performance & Responsive UI"},
            {"title": "Senior Recruiter", "package": "₹6.50 - ₹11.00 LPA", "focus": "STAR Methodology, Talent Sourcing, Candidate Screening & Analytics"},
        ],
        "selection_rounds": [
            {"round": "Round 1: Automated AI Screening", "details": "Multimodal candidate screening evaluating core experience, stack alignment, and salary expectations."},
            {"round": "Round 2: Cognitive Aptitude & AI Fundamentals", "details": "Bayesian probability (10 Qs), Linear algebra & vectors (10 Qs), AI/ML mechanics (15 Qs), and Deductive logic (15 Qs)."},
            {"round": "Round 3: Technical Deep-Dive / Portfolio Review", "details": "Hands-on coding, model evaluation metrics, vector search latency optimization, and architecture defense."},
            {"round": "Round 4: Strategic & Leadership Round", "details": "Real-world scenario problem solving, high-ambiguity delivery, and cultural fit."},
        ],
        "exam_pattern": [
            {"section": "Bayesian Math & Probability", "questions": 12, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "70%"},
            {"section": "Logical & Deductive Reasoning", "questions": 15, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "70%"},
            {"section": "AI, ML & Transformer Mechanics", "questions": 15, "time_mins": 20, "marking": "+1, No Negative", "cutoff": "75%"},
            {"section": "Frontend & Talent Evaluation", "questions": 12, "time_mins": 15, "marking": "+1, No Negative", "cutoff": "65%"},
        ],
        "aptitude_analysis": {
            "quantitative_trends": [
                {"topic": "Bayes' Theorem & Screening Statistics", "weight": "40%", "freq": "Signature", "tips": "Conditional probabilities, false positive/negative calculations in automated screening."},
                {"topic": "Vector Math & Cosine Distance", "weight": "35%", "freq": "Very High", "tips": "Dot product of normalized vectors, high-dimensional cosine similarity, and Euclidean bounds."},
                {"topic": "Permutations & Committee Combinations", "weight": "25%", "freq": "High", "tips": "Evaluation panel formations and constrained combinations."},
            ],
            "reasoning_trends": [
                {"topic": "Transformer Attention Mechanics", "weight": "40%", "freq": "Signature", "tips": "Scaled Dot-Product Attention $O(N^2 D)$ complexity and multi-head projection dimensions."},
                {"topic": "Syllogistic & Deductive Logic", "weight": "35%", "freq": "Very High", "tips": "Three-statement syllogisms evaluating guaranteed truth versus uncertain overlap."},
                {"topic": "Web Performance Logic", "weight": "25%", "freq": "High", "tips": "Debounce vs Throttle mechanisms for high-frequency input streams."},
            ],
            "verbal_trends": [
                {"topic": "STAR Behavioral Framework", "weight": "50%", "freq": "Very High", "tips": "Structuring responses into Situation, Task, Action, and Quantifiable Result."},
                {"topic": "Talent Communication & Rubrics", "weight": "50%", "freq": "High", "tips": "Objective candidate assessment and structured feedback formulation."},
            ],
        },
        "preparation_strategy": [
            "Week 1: Master Vector Math and Bayes' Theorem: practice calculating posterior probabilities and embedding cosine distances.",
            "Week 2: Deep dive into Transformer Self-Attention, PyTorch training dynamics, Dropout regularization, and loss functions.",
            "Week 3: Study Modern Frontend performance: Debouncing, Event delegation, and Virtual DOM rendering optimizations.",
            "Week 4: Take the Vaarg AI & Technical recruiter placement mock exam and review questions asked in recent hiring loops.",
        ],
        "sample_questions": [],
        "mock_test_title": "Vaarg Technologies AI & Full-Stack Placement Mock Test",
        "mock_test_id": "vaarg-ai-fullstack-placement-mock",
    },
}


import json
from sqlalchemy.orm import Session
from app.services.company_intelligence_questions import COMPANY_RECENT_QUESTIONS


def _derive_question_section(subtopic: str, topic_name: str) -> str:
    """Derives section name for standard aptitude filtering."""
    combined = f"{subtopic or ''} {topic_name or ''}".lower()
    if any(k in combined for k in ["quant", "math", "work", "time", "speed", "distance", "profit", "loss", "ratio", "number", "interest", "probability", "permutation", "combination", "geometry", "percentage", "clock", "calendar", "mixture", "allegation"]):
        return "Quantitative Ability"
    if any(k in combined for k in ["reason", "deduction", "family", "blood", "direction", "coding", "decoding", "series", "seating", "syllogism", "puzzle", "analogy", "pattern"]):
        return "Logical Reasoning"
    if any(k in combined for k in ["verbal", "english", "grammar", "comprehension", "synonym", "antonym", "error", "sentence", "cloze", "para", "idiom"]):
        return "Verbal Ability"
    return "Technical Pseudocode & Puzzles"


def get_all_companies_intelligence(db: Optional[Session] = None) -> List[Dict[str, Any]]:
    """
    Returns summarized list of company intelligence for top placement recruiters and
    companies actively hiring on the platform. Dynamic database statistics and candidate
    selections are reflected automatically.
    """
    # 1. Discover hiring companies from DB if db session is available
    hiring_companies_stats: Dict[str, Dict[str, Any]] = {}
    db_company_question_counts: Dict[str, int] = {}

    if db:
        try:
            from app.models.application import Application, ApplicationStatus
            from app.models.job import Job
            from app.models.recruiter import RecruiterProfile
            from app.models.student import AptitudeQuestion

            # Find all applications that were selected/hired or shortlisted
            selected_apps = (
                db.query(Application)
                .filter(Application.status.in_([ApplicationStatus.selected, ApplicationStatus.shortlisted]))
                .all()
            )
            for a in selected_apps:
                job = db.query(Job).filter(Job.id == a.job_id).first()
                if not job:
                    continue
                cname = job.company_name
                if not cname:
                    recruiter = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == job.recruiter_id).first()
                    cname = recruiter.company_name if recruiter else "Direct Employer"
                slug = cname.lower().strip().replace(" ", "_").replace("-", "_")
                if slug not in hiring_companies_stats:
                    hiring_companies_stats[slug] = {
                        "name": cname,
                        "hired_count": 0,
                        "shortlisted_count": 0,
                        "roles": set(),
                    }
                if a.status == ApplicationStatus.selected:
                    hiring_companies_stats[slug]["hired_count"] += 1
                else:
                    hiring_companies_stats[slug]["shortlisted_count"] += 1
                if job.title:
                    hiring_companies_stats[slug]["roles"].add(job.title)

            # Query question counts per company tag in aptitude_questions
            tagged_questions = db.query(AptitudeQuestion.company_tag).filter(AptitudeQuestion.company_tag.isnot(None)).all()
            for row in tagged_questions:
                if row[0]:
                    tag_norm = row[0].lower().strip().replace(" ", "_").replace("-", "_")
                    db_company_question_counts[tag_norm] = db_company_question_counts.get(tag_norm, 0) + 1
        except Exception as e:
            # Fallback gracefully if database query encounters an issue
            pass

    result = []
    for slug, c in TOP_COMPANIES_INTELLIGENCE.items():
        base_qs = COMPANY_RECENT_QUESTIONS.get(c["slug"], c.get("sample_questions", []))
        total_qs_count = len(base_qs)

        # Merge DB question count if available
        for tag_norm, count in db_company_question_counts.items():
            if tag_norm == slug or slug in tag_norm or tag_norm in slug:
                # Add unique DB questions count
                total_qs_count = max(total_qs_count, count + len(base_qs) // 2)

        # Check if company conducted recent hiring on the platform
        hiring_stat = hiring_companies_stats.get(slug)
        is_recent_hiring = hiring_stat is not None and (hiring_stat["hired_count"] > 0 or hiring_stat["shortlisted_count"] > 0)

        badge_text = c["badge_text"]
        recent_hiring_process = c.get("badge_text", "Campus Placement 2026")
        hired_count = 0
        hired_roles_list = []

        if is_recent_hiring:
            hired_count = hiring_stat["hired_count"]
            roles_str = ", ".join(list(hiring_stat["roles"])[:2]) if hiring_stat["roles"] else "Tech Roles"
            badge_text = f"🔥 Recently Hired {hired_count} Candidates"
            recent_hiring_process = f"Recent Hiring Process ({roles_str})"
            hired_roles_list = list(hiring_stat["roles"])

        result.append({
            "slug": c["slug"],
            "name": c["name"],
            "badge_text": badge_text,
            "icon": c["icon"],
            "accent_color": c["accent_color"],
            "gradient": c["gradient"],
            "tagline": c["tagline"],
            "overall_difficulty": c["overall_difficulty"],
            "hiring_roles_count": len(c["hiring_roles"]),
            "hiring_roles": c["hiring_roles"],
            "mock_test_title": c["mock_test_title"],
            "mock_test_id": c["mock_test_id"],
            "selection_rounds_count": len(c["selection_rounds"]),
            "questions_count": total_qs_count,
            "recent_hiring_process": recent_hiring_process,
            "is_recent_hiring": is_recent_hiring,
            "hired_candidates_count": hired_count,
            "hired_roles": hired_roles_list,
        })

    # Sort companies so that active hiring companies appear first, followed by top tech recruiters
    result.sort(key=lambda x: (not x.get("is_recent_hiring", False), x["slug"]))
    return result


def get_company_intelligence_detail(slug: str, db: Optional[Session] = None) -> Optional[Dict[str, Any]]:
    """
    Returns full deep-dive intelligence, patterns, questions, and strategies for a specific company.
    Dynamically loads and merges verified recruitment questions from PostgreSQL `aptitude_questions`
    and recent candidate screening rounds.
    """
    norm = slug.lower().strip().replace(" ", "_").replace("-", "_")
    target_company = None
    target_key = None

    for k, v in TOP_COMPANIES_INTELLIGENCE.items():
        if k == norm or norm in k or k in norm:
            target_company = v
            target_key = k
            break

    if not target_company:
        return None

    detail = dict(target_company)
    company_name = detail["name"]

    # 1. Base curated sample questions
    sample_questions: List[Dict[str, Any]] = list(
        COMPANY_RECENT_QUESTIONS.get(detail.get("slug", norm), detail.get("sample_questions", []))
    )
    seen_questions = {q["question"].strip().lower() for q in sample_questions}

    # 2. Dynamically merge live aptitude questions from PostgreSQL
    if db:
        try:
            from app.models.student import AptitudeQuestion
            from app.models.application import Application, ApplicationStatus
            from app.models.job import Job
            from app.models.recruiter import RecruiterProfile
            from app.models.screening import ScreeningSession, ScreeningQuestion

            # Query aptitude_questions tagged with company name or slug
            db_questions = (
                db.query(AptitudeQuestion)
                .filter(
                    (AptitudeQuestion.company_tag.ilike(f"%{norm}%")) |
                    (AptitudeQuestion.company_tag.ilike(f"%{company_name}%"))
                )
                .all()
            )

            for dq in db_questions:
                q_text = dq.question.strip()
                if q_text.lower() in seen_questions:
                    continue
                seen_questions.add(q_text.lower())

                opts = json.loads(dq.options_json) if isinstance(dq.options_json, str) else (dq.options_json or [])
                section = _derive_question_section(dq.subtopic, dq.topic_name)
                sample_questions.append({
                    "id": f"db-{dq.id}",
                    "question": q_text,
                    "options": opts,
                    "correct_option_index": dq.correct_option_index,
                    "section": section,
                    "topic": dq.subtopic or dq.topic_name or "Aptitude",
                    "tag": f"{dq.company_tag} (Recent Hiring)",
                    "difficulty": dq.difficulty or "medium",
                    "explanation": dq.explanation or "Refer to verified corporate exam derivation.",
                })

            # Check if this company hired candidates on the platform
            selected_apps = (
                db.query(Application)
                .filter(Application.status.in_([ApplicationStatus.selected, ApplicationStatus.shortlisted]))
                .all()
            )
            comp_hired_count = 0
            comp_hired_roles = set()
            for a in selected_apps:
                job = db.query(Job).filter(Job.id == a.job_id).first()
                if not job:
                    continue
                cname = job.company_name
                if not cname:
                    recruiter = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == job.recruiter_id).first()
                    cname = recruiter.company_name if recruiter else ""
                if norm in cname.lower() or cname.lower() in norm:
                    if a.status == ApplicationStatus.selected:
                        comp_hired_count += 1
                    if job.title:
                        comp_hired_roles.add(job.title)

            if comp_hired_count > 0:
                detail["hired_candidates_count"] = comp_hired_count
                detail["hired_roles"] = list(comp_hired_roles)
                roles_label = ", ".join(list(comp_hired_roles)[:3])
                detail["badge_text"] = f"🔥 Recently Hired {comp_hired_count} Candidates"
                detail["recent_hiring_process"] = f"Recent Hiring Drive — {roles_label} ({comp_hired_count} Hired)"

            # Check screening questions asked in real sessions for this company
            screening_qs = (
                db.query(ScreeningQuestion)
                .join(ScreeningSession, ScreeningQuestion.screening_session_id == ScreeningSession.id)
                .join(Job, ScreeningSession.job_id == Job.id)
                .filter(
                    (Job.company_name.ilike(f"%{norm}%")) |
                    (Job.title.ilike(f"%{norm}%"))
                )
                .all()
            )
            for sq in screening_qs:
                sq_text = sq.question.strip()
                if sq_text.lower() in seen_questions:
                    continue
                seen_questions.add(sq_text.lower())
                # Format into a question
                exp = sq.expected_answer or "Demonstrate verified production experience and clear technical articulation."
                sample_questions.append({
                    "id": f"screening-{sq.id}",
                    "question": f"[Screening Interview Round] {sq_text}",
                    "options": [
                        exp,
                        "Theoretical understanding without hands-on implementation",
                        "Beginner / academic knowledge only",
                        "No direct experience in this technology",
                    ],
                    "correct_option_index": 0,
                    "section": "Technical Pseudocode & Puzzles" if sq.question_type == "technical" else "Verbal Ability",
                    "topic": f"Screening: {sq.question_type.title()}",
                    "tag": f"{detail['name']} Screening",
                    "difficulty": "medium",
                    "explanation": f"Evaluation Criterion asked during recent hiring: {exp}",
                })
        except Exception as e:
            # Continue with base questions if database lookup encounters any transient exception
            pass

    detail["sample_questions"] = sample_questions
    detail["recent_hiring_process"] = detail.get("recent_hiring_process") or detail.get("badge_text", "Campus Placement 2026")
    detail["questions_count"] = len(sample_questions)
    return detail
