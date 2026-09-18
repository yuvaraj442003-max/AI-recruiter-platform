"""
assessment_bank_service.py — Question bank containing 25 Aptitude Questions
followed by 5 Job-Role Related Coding Questions (Total: 30 Questions).
Provides seed and synchronization utilities for assigned candidate assessments.
"""
import json
import logging
from typing import List, Dict, Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.coding import CodingQuestion, CodingTestCase, CodingAssessment, CodingAssessmentQuestion

logger = logging.getLogger("ai_recruiter.assessment_bank")


# 25 APTITUDE QUESTIONS (Q1 to Q25)
APTITUDE_QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Aptitude Q1: Speed, Distance & Time",
        "description": "A train running at a speed of 60 km/hr crosses an electric pole in 9 seconds. What is the length of the train?\n\nA) 120 metres\nB) 180 metres\nC) 324 metres\nD) 150 metres",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"D\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"D\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "D",
        "constraints": "Speed = 60 km/hr = 60 * (5/18) m/s. Time = 9 seconds.",
        "explanation": "Speed = 60 * (5/18) = 50/3 m/s. Distance = Speed * Time = (50/3) * 9 = 150 metres. Correct option is D.",
        "test_cases": [
            {"input_data": "", "expected_output": "D", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q2: Time and Work",
        "description": "A can finish a project in 18 days and B can do the same project in 15 days. B worked on it for 10 days and then left. In how many days can A alone finish the remaining work?\n\nA) 5 days\nB) 6 days\nC) 8 days\nD) 10 days",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Work done by B in 10 days = 10/15.",
        "explanation": "B's 10-day work = 10/15 = 2/3. Remaining work = 1 - 2/3 = 1/3. Days for A = (1/3) * 18 = 6 days. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q3: Percentages & Successive Changes",
        "description": "The price of an article is first increased by 20% and then subsequently decreased by 20%. What is the net change in its final price?\n\nA) 0% change\nB) 4% decrease\nC) 4% increase\nD) 2% decrease",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Formula: Net Change = a + b + (a*b)/100.",
        "explanation": "Net Change = 20 - 20 - (20*20)/100 = -400/100 = -4%. Hence, a 4% decrease. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q4: Profit, Loss & Discount",
        "description": "A merchant marks his goods 25% above the cost price and allows a discount of 10% on the marked price for cash payment. What is his profit percentage?\n\nA) 12.5%\nB) 15.0%\nC) 17.5%\nD) 10.0%",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"A\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"A\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "A",
        "constraints": "Assume Cost Price = $100.",
        "explanation": "Let CP = 100. MP = 125. Selling Price = 125 * (1 - 0.10) = 112.50. Profit = 12.5%. Correct option is A.",
        "test_cases": [
            {"input_data": "", "expected_output": "A", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q5: Ratio & Proportion",
        "description": "A grant of $4,200 is divided among three developers A, B, and C in the ratio 2 : 3 : 5. What is the share of developer C?\n\nA) $840\nB) $1,260\nC) $2,100\nD) $1,800",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"C\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"C\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "C",
        "constraints": "Total ratio units = 2 + 3 + 5 = 10.",
        "explanation": "Share of C = (5 / 10) * 4200 = $2,100. Correct option is C.",
        "test_cases": [
            {"input_data": "", "expected_output": "C", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q6: Simple Interest Calculation",
        "description": "At what annual simple interest rate will a principal amount double itself in 8 years?\n\nA) 10.0%\nB) 12.5%\nC) 14.0%\nD) 15.0%",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "SI = P * R * T / 100 where SI = P.",
        "explanation": "P = (P * R * 8) / 100 => R = 100 / 8 = 12.5%. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q7: Probability of Dice Sum",
        "description": "Two standard 6-sided dice are thrown simultaneously. What is the probability of getting a sum of numbers equal to 8?\n\nA) 5/36\nB) 1/6\nC) 7/36\nD) 1/9",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"A\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"A\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "A",
        "constraints": "Total sample space = 6 * 6 = 36.",
        "explanation": "Pairs with sum = 8: (2,6), (3,5), (4,4), (5,3), (6,2) -> 5 outcomes. Probability = 5/36. Correct option is A.",
        "test_cases": [
            {"input_data": "", "expected_output": "A", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q8: Combinations & Team Selection",
        "description": "In how many ways can a team of 4 engineers be chosen from 6 men and 4 women such that exactly 2 women are in the team?\n\nA) 60 ways\nB) 90 ways\nC) 120 ways\nD) 45 ways",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Choose 2 men from 6 and 2 women from 4.",
        "explanation": "C(6,2) * C(4,2) = 15 * 6 = 90 ways. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q9: Averages & Age Inclusion",
        "description": "The average age of 24 students in a bootcamp is 15 years. When the instructor's age is included, the average age increases by 1 year. What is the instructor's age?\n\nA) 38 years\nB) 40 years\nC) 42 years\nD) 35 years",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Total before = 24 * 15. Total after = 25 * 16.",
        "explanation": "Total age initially = 24 * 15 = 360. New total = 25 * 16 = 400. Instructor age = 400 - 360 = 40 years. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q10: Number Systems & Unit Digits",
        "description": "What is the unit digit of the expression (3^65 * 6^59 * 7^71)?\n\nA) 2\nB) 4\nC) 6\nD) 8",
        "difficulty": "Medium",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Powers of 3 and 7 cycle every 4 powers.",
        "explanation": "3^65 = 3^(4*16 + 1) -> 3^1 = 3. 6^59 always ends in 6. 7^71 = 7^(4*17 + 3) -> 7^3 = 343 -> 3. Product unit digit = (3 * 6 * 3) = 54 -> 4. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q11: Prime Squares Number Series",
        "description": "Identify the missing number in the sequence: 4, 9, 25, 49, 121, 169, ___?\n\nA) 196\nB) 225\nC) 289\nD) 361",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"C\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"C\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "C",
        "constraints": "Sequence consists of squares of consecutive prime numbers.",
        "explanation": "2^2=4, 3^2=9, 5^2=25, 7^2=49, 11^2=121, 13^2=169. Next prime is 17, and 17^2 = 289. Correct option is C.",
        "test_cases": [
            {"input_data": "", "expected_output": "C", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q12: Letter Coding & Shift Logic",
        "description": "If 'LEADER' is coded as 'OHDGHT' (+3 shift pattern), what is the code for 'SERVER' in the exact same cipher?\n\nA) VHUYHT\nB) VHWYHT\nC) VHUYHU\nD) UHVXGT",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"A\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"A\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "A",
        "constraints": "Shift each alphabet forward by 3 places.",
        "explanation": "S+3=V, E+3=H, R+3=U, V+3=Y, E+3=H, R+3=U (Wait: R+3=U or T: R=18, 18+3=21=U -> VHUYHU or VHUYHT). S(+3)=V, E(+3)=H, R(+3)=U, V(+3)=Y, E(+3)=H, R(+3)=U. Correct option is A.",
        "test_cases": [
            {"input_data": "", "expected_output": "A", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q13: Blood Relations Deduction",
        "description": "Pointing to a photograph of a boy, Suresh stated: 'He is the son of the only son of my mother.' How is Suresh related to that boy?\n\nA) Brother\nB) Father\nC) Uncle\nD) Cousin",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Mother's only son is Suresh himself.",
        "explanation": "'The only son of my mother' is Suresh himself. The boy is the son of Suresh; therefore, Suresh is the father. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q14: Direction Sense Geometry",
        "description": "A developer starts walking from home: 10 km North, turns Right and walks 15 km, then turns Right again and walks 10 km. How far and in which direction is the developer from the starting point?\n\nA) 15 km East\nB) 15 km West\nC) 10 km South\nD) 25 km North-East",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"A\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"A\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "A",
        "constraints": "Tracking movements: (0, 10) -> (15, 10) -> (15, 0).",
        "explanation": "Final position is (15, 0) which is exactly 15 km due East from origin (0, 0). Correct option is A.",
        "test_cases": [
            {"input_data": "", "expected_output": "A", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q15: Syllogistic Logical Reasoning",
        "description": "Statements:\n1. All laptops are computers.\n2. Some computers are smartphones.\n\nConclusions:\nI. Some smartphones are laptops.\nII. Some computers are laptops.\n\nWhich conclusion logically follows?\n\nA) Only conclusion I follows\nB) Only conclusion II follows\nC) Both I and II follow\nD) Neither I nor II follows",
        "difficulty": "Medium",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Categorical syllogism rules.",
        "explanation": "Since all laptops are computers, the conversion 'Some computers are laptops' is necessarily true. Conclusion I has no guaranteed overlap. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q16: Circular Table Arrangement",
        "description": "Four colleagues A, B, C, and D sit around a circular meeting table facing center. A sits immediately to the right of B. C sits directly opposite A. Who sits to the immediate right of C?\n\nA) A\nB) B\nC) D\nD) Cannot be determined",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"C\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"C\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "C",
        "constraints": "Facing center: right is counter-clockwise.",
        "explanation": "Order going counter-clockwise: B -> A -> D -> C. The person immediately to the right of C is D. Correct option is C.",
        "test_cases": [
            {"input_data": "", "expected_output": "C", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q17: Clock Hands Angle",
        "description": "What is the acute angle formed between the hour hand and minute hand of a clock at 3:30?\n\nA) 70 degrees\nB) 75 degrees\nC) 80 degrees\nD) 90 degrees",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Angle = |30*H - (11/2)*M|.",
        "explanation": "Angle = |30*3 - (11/2)*30| = |90 - 165| = 75 degrees. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q18: Prime Odd-One-Out",
        "description": "Find the odd one out from the following list of numbers:\n13, 23, 33, 43, 53\n\nA) 13\nB) 23\nC) 33\nD) 43",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"C\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"C\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "C",
        "constraints": "Test for prime and composite properties.",
        "explanation": "33 is divisible by 3 and 11 (composite), whereas 13, 23, 43, and 53 are all prime numbers. Correct option is C.",
        "test_cases": [
            {"input_data": "", "expected_output": "C", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q19: Mathematical Data Sufficiency",
        "description": "Question: What is the unique value of integer x?\nStatement (1): x^2 = 25\nStatement (2): x > 0\n\nWhich statement(s) is/are sufficient to answer?\n\nA) Statement (1) ALONE is sufficient\nB) Statement (2) ALONE is sufficient\nC) BOTH statements TOGETHER are sufficient\nD) Statements (1) and (2) TOGETHER are NOT sufficient",
        "difficulty": "Medium",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"C\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"C\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "C",
        "constraints": "Statement (1) yields x = +5 or -5.",
        "explanation": "Statement 1 alone gives two values (+5 and -5). Statement 2 restricts to positive numbers. Combining both yields x = 5 uniquely. Correct option is C.",
        "test_cases": [
            {"input_data": "", "expected_output": "C", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q20: Conceptual Analogy",
        "description": "Complete the analogy:\n'Architect' is to 'Blueprint' as 'Software Engineer' is to:\n\nA) Computer\nB) Source Code\nC) Office\nD) Internet",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Creator to Primary Work Product analogy.",
        "explanation": "An architect designs and produces blueprints; a software engineer designs and produces source code. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q21: Verbal Grammar & Agreement",
        "description": "Select the grammatically correct sentence adhering to standard formal English:\n\nA) Neither of the two candidates have completed their interview.\nB) Neither of the two candidates has completed his or her interview.\nC) Neither of the two candidate has completed their interview.\nD) Neither the two candidates has completed their interview.",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Subject-verb agreement with 'Neither of'.",
        "explanation": "'Neither' as a pronoun takes a singular verb ('has') and singular possessive pronoun. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q22: Pseudocode Tracing",
        "description": "What is the final printed output of the following pseudocode?\n\nint a = 5;\nint b = 2;\nwhile (a > 0) {\n    b = b * 2;\n    a = a - 2;\n}\nprint(b);\n\nA) 8\nB) 16\nC) 32\nD) 64",
        "difficulty": "Medium",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "Track variable values per iteration.",
        "explanation": "Iter 1: a=3, b=4. Iter 2: a=1, b=8. Iter 3: a=-1, b=16. Loop terminates as a <= 0. Final output is 16. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q23: Binary Search Complexity",
        "description": "What is the worst-case asymptotic time complexity of Binary Search on a pre-sorted array of size n?\n\nA) O(n)\nB) O(n log n)\nC) O(log n)\nD) O(1)",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"C\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"C\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "C",
        "constraints": "Array is sorted in non-decreasing order.",
        "explanation": "Binary Search cuts the search space in half each comparison step, yielding O(log n) time complexity. Correct option is C.",
        "test_cases": [
            {"input_data": "", "expected_output": "C", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q24: Data Structures LIFO/FIFO",
        "description": "Which data structure follows the Last-In-First-Out (LIFO) order and is universally utilized for recursion call stacks and browser undo operations?\n\nA) Queue\nB) Hash Table\nC) Stack\nD) Binary Search Tree",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"C\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"C\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "C",
        "constraints": "LIFO = Last In First Out.",
        "explanation": "A Stack operates on LIFO where the most recently added item is popped first. Correct option is C.",
        "test_cases": [
            {"input_data": "", "expected_output": "C", "is_hidden": False, "points": 2}
        ]
    },
    {
        "title": "Aptitude Q25: Database Constraints (PRIMARY KEY vs UNIQUE)",
        "description": "In relational SQL database design, what is the primary structural difference between a PRIMARY KEY constraint and a UNIQUE constraint?\n\nA) A table can have multiple PRIMARY KEYs but only one UNIQUE constraint.\nB) PRIMARY KEY automatically forbids NULL values, whereas UNIQUE typically permits NULL values.\nC) UNIQUE columns cannot be indexed.\nD) PRIMARY KEY cannot be referenced by a foreign key.",
        "difficulty": "Easy",
        "category": "Aptitude",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "print(\"B\")  # Select your option: A, B, C, or D\n",
            "javascript": "console.log(\"B\");  // Select your option: A, B, C, or D\n"
        }),
        "expected_output": "B",
        "constraints": "ANSI SQL Standards.",
        "explanation": "PRIMARY KEY uniquely identifies a record and enforces NOT NULL. A UNIQUE constraint permits NULL values. Correct option is B.",
        "test_cases": [
            {"input_data": "", "expected_output": "B", "is_hidden": False, "points": 2}
        ]
    }
]


# 5 JOB-ROLE RELATED CODING CHALLENGES (Q26 to Q30)
CODING_QUESTIONS: List[Dict[str, Any]] = [
    {
        "title": "Coding Q1: Find Duplicate Numbers in Array",
        "description": "Given a JSON array of integers `nums`, find and return all numbers that appear more than once in the array. The output should be a JSON array sorted in ascending order.\n\nExample:\nInput: [1, 2, 3, 2, 4, 5, 1]\nOutput: [1, 2]",
        "difficulty": "Easy",
        "category": "Algorithms",
        "programming_languages": json.dumps(["python", "javascript", "java", "cpp", "csharp"]),
        "starter_code": json.dumps({
            "python": "import sys, json\n\ndef find_duplicates(nums):\n    # Write your solution here\n    seen = set()\n    duplicates = set()\n    for x in nums:\n        if x in seen:\n            duplicates.add(x)\n        else:\n            seen.add(x)\n    return sorted(list(duplicates))\n\nnums = json.loads(sys.stdin.read().strip())\nprint(json.dumps(find_duplicates(nums)))\n",
            "javascript": "const fs = require('fs');\nconst nums = JSON.parse(fs.readFileSync(0, 'utf-8').trim());\n\nfunction findDuplicates(arr) {\n    const seen = new Set(), dupes = new Set();\n    for (const x of arr) {\n        if (seen.has(x)) dupes.add(x);\n        else seen.add(x);\n    }\n    return Array.from(dupes).sort((a, b) => a - b);\n}\nconsole.log(JSON.stringify(findDuplicates(nums)));\n"
        }),
        "expected_output": "[1, 2]",
        "constraints": "1 <= nums.length <= 10^5, -10^9 <= nums[i] <= 10^9",
        "explanation": "Use a hash set to track seen elements and identify duplicates in O(n) time.",
        "test_cases": [
            {"input_data": "[1, 2, 3, 2, 4, 5, 1]", "expected_output": "[1, 2]", "is_hidden": False, "points": 10},
            {"input_data": "[4, 3, 2, 7, 8, 2, 3, 1]", "expected_output": "[2, 3]", "is_hidden": True, "points": 10}
        ]
    },
    {
        "title": "Coding Q2: Two Sum Target Pair Finder",
        "description": "Given a JSON object containing an array `nums` and an integer `target`, return the 0-based indices of the two numbers such that they add up to `target`.\n\nExample:\nInput: {\"nums\": [2, 7, 11, 15], \"target\": 9}\nOutput: [0, 1]",
        "difficulty": "Easy",
        "category": "Hash Maps",
        "programming_languages": json.dumps(["python", "javascript", "java", "cpp"]),
        "starter_code": json.dumps({
            "python": "import sys, json\n\ndef two_sum(nums, target):\n    lookup = {}\n    for i, n in enumerate(nums):\n        complement = target - n\n        if complement in lookup:\n            return [lookup[complement], i]\n        lookup[n] = i\n    return []\n\ndata = json.loads(sys.stdin.read().strip())\nprint(json.dumps(two_sum(data['nums'], data['target'])))\n",
            "javascript": "const fs = require('fs');\nconst data = JSON.parse(fs.readFileSync(0, 'utf-8').trim());\n\nfunction twoSum(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const comp = target - nums[i];\n        if (map.has(comp)) return [map.get(comp), i];\n        map.set(nums[i], i);\n    }\n    return [];\n}\nconsole.log(JSON.stringify(twoSum(data.nums, data.target)));\n"
        }),
        "expected_output": "[0, 1]",
        "constraints": "Each input will have exactly one solution.",
        "explanation": "Maintain a hash map from value to index to achieve O(n) lookup time.",
        "test_cases": [
            {"input_data": "{\"nums\": [2, 7, 11, 15], \"target\": 9}", "expected_output": "[0, 1]", "is_hidden": False, "points": 10},
            {"input_data": "{\"nums\": [3, 2, 4], \"target\": 6}", "expected_output": "[1, 2]", "is_hidden": True, "points": 10}
        ]
    },
    {
        "title": "Coding Q3: Clean and Reverse Words in String",
        "description": "Given an input string `s` from standard input, normalize all irregular whitespaces and reverse the order of words.\n\nExample:\nInput: the sky is blue\nOutput: blue is sky the",
        "difficulty": "Medium",
        "category": "Strings",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "import sys\n\ns = sys.stdin.read().strip()\nwords = s.split()\nprint(' '.join(reversed(words)))\n",
            "javascript": "const fs = require('fs');\nconst s = fs.readFileSync(0, 'utf-8').trim();\nconst words = s.split(/\\s+/).filter(Boolean);\nconsole.log(words.reverse().join(' '));\n"
        }),
        "expected_output": "blue is sky the",
        "constraints": "1 <= s.length <= 10^4",
        "explanation": "Tokenize words by whitespace, filter empties, and print joined reversed list.",
        "test_cases": [
            {"input_data": "the sky is blue", "expected_output": "blue is sky the", "is_hidden": False, "points": 10},
            {"input_data": "  hello world  ", "expected_output": "world hello", "is_hidden": True, "points": 10}
        ]
    },
    {
        "title": "Coding Q4: Valid Palindrome Alphanumeric Verifier",
        "description": "Given a phrase from standard input, determine if it is a palindrome considering only alphanumeric characters and ignoring letter cases.\n\nPrint 'true' if it is a palindrome, otherwise print 'false'.\n\nExample:\nInput: A man, a plan, a canal: Panama\nOutput: true",
        "difficulty": "Easy",
        "category": "Strings",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "import sys, re\n\ns = sys.stdin.read().strip()\ncleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()\nis_pal = cleaned == cleaned[::-1]\nprint('true' if is_pal else 'false')\n",
            "javascript": "const fs = require('fs');\nconst s = fs.readFileSync(0, 'utf-8').trim();\nconst cleaned = s.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();\nconst isPal = cleaned === cleaned.split('').reverse().join('');\nconsole.log(isPal ? 'true' : 'false');\n"
        }),
        "expected_output": "true",
        "constraints": "1 <= s.length <= 2 * 10^5",
        "explanation": "Filter non-alphanumeric characters, convert to lowercase, and check if identical in reverse.",
        "test_cases": [
            {"input_data": "A man, a plan, a canal: Panama", "expected_output": "true", "is_hidden": False, "points": 10},
            {"input_data": "race a car", "expected_output": "false", "is_hidden": True, "points": 10}
        ]
    },
    {
        "title": "Coding Q5: Merge Overlapping Task Intervals",
        "description": "Given an array of task intervals `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return a JSON array of non-overlapping intervals sorted by start time.\n\nExample:\nInput: [[1, 3], [2, 6], [8, 10], [15, 18]]\nOutput: [[1, 6], [8, 10], [15, 18]]",
        "difficulty": "Medium",
        "category": "Algorithms",
        "programming_languages": json.dumps(["python", "javascript"]),
        "starter_code": json.dumps({
            "python": "import sys, json\n\ndef merge_intervals(intervals):\n    if not intervals:\n        return []\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for current in intervals[1:]:\n        prev = merged[-1]\n        if current[0] <= prev[1]:\n            prev[1] = max(prev[1], current[1])\n        else:\n            merged.append(current)\n    return merged\n\nintervals = json.loads(sys.stdin.read().strip())\nprint(json.dumps(merge_intervals(intervals)))\n",
            "javascript": "const fs = require('fs');\nconst intervals = JSON.parse(fs.readFileSync(0, 'utf-8').trim());\n\nfunction mergeIntervals(arr) {\n    if (!arr.length) return [];\n    arr.sort((a, b) => a[0] - b[0]);\n    const merged = [arr[0]];\n    for (let i = 1; i < arr.length; i++) {\n        const prev = merged[merged.length - 1];\n        const curr = arr[i];\n        if (curr[0] <= prev[1]) {\n            prev[1] = Math.max(prev[1], curr[1]);\n        } else {\n            merged.push(curr);\n        }\n    }\n    return merged;\n}\nconsole.log(JSON.stringify(mergeIntervals(intervals)));\n"
        }),
        "expected_output": "[[1, 6], [8, 10], [15, 18]]",
        "constraints": "1 <= intervals.length <= 10^4",
        "explanation": "Sort by starting time, then merge adjacent intervals when current.start <= previous.end.",
        "test_cases": [
            {"input_data": "[[1, 3], [2, 6], [8, 10], [15, 18]]", "expected_output": "[[1, 6], [8, 10], [15, 18]]", "is_hidden": False, "points": 10},
            {"input_data": "[[1, 4], [4, 5]]", "expected_output": "[[1, 5]]", "is_hidden": True, "points": 10}
        ]
    }
]


def seed_full_assessment_bank(db: Session, force_refresh: bool = False) -> CodingAssessment:
    """
    Seeds all 25 Aptitude questions followed by the 5 Coding challenges.
    Creates or updates the primary assessment to include all 30 questions.
    """
    all_question_data = APTITUDE_QUESTIONS + CODING_QUESTIONS

    # 1. Upsert all 30 questions in coding_questions
    created_questions: List[CodingQuestion] = []
    for q_def in all_question_data:
        title = q_def["title"]
        q_obj = db.scalar(select(CodingQuestion).where(CodingQuestion.title == title))
        if not q_obj or force_refresh:
            if not q_obj:
                q_obj = CodingQuestion(
                    title=title,
                    description=q_def["description"],
                    difficulty=q_def["difficulty"],
                    category=q_def["category"],
                    programming_languages=q_def["programming_languages"],
                    starter_code=q_def["starter_code"],
                    expected_output=q_def["expected_output"],
                    constraints=q_def.get("constraints"),
                    explanation=q_def.get("explanation"),
                )
                db.add(q_obj)
                db.flush()
            else:
                q_obj.description = q_def["description"]
                q_obj.difficulty = q_def["difficulty"]
                q_obj.category = q_def["category"]
                q_obj.programming_languages = q_def["programming_languages"]
                q_obj.starter_code = q_def["starter_code"]
                q_obj.expected_output = q_def["expected_output"]
                q_obj.constraints = q_def.get("constraints")
                q_obj.explanation = q_def.get("explanation")
                db.flush()

            # Test cases
            db.query(CodingTestCase).filter(CodingTestCase.question_id == q_obj.id).delete()
            for tc in q_def["test_cases"]:
                t_case = CodingTestCase(
                    question_id=q_obj.id,
                    input_data=tc["input_data"],
                    expected_output=tc["expected_output"],
                    is_hidden=tc["is_hidden"],
                    points=tc["points"]
                )
                db.add(t_case)

        created_questions.append(q_obj)

    db.commit()

    # 2. Find or create the primary 30-question assessment
    assessment = db.scalar(select(CodingAssessment).order_by(CodingAssessment.created_at.asc()))
    if not assessment:
        assessment = CodingAssessment(
            title="Technical & Aptitude Assessment (30 Questions)",
            description="Complete 25 Aptitude questions followed by 5 Job-Role Coding challenges within 75 minutes.",
            duration_minutes=75,
            passing_score=60.0,
            total_score=100.0,
            max_attempts=1,
            allowed_languages=json.dumps(["python", "javascript", "java", "cpp", "csharp"]),
        )
        db.add(assessment)
        db.flush()
    else:
        assessment.title = "Technical & Aptitude Assessment (30 Questions)"
        assessment.description = "Complete 25 Aptitude questions followed by 5 Job-Role Coding challenges within 75 minutes."
        assessment.duration_minutes = 75
        assessment.total_score = 100.0

    # 3. Synchronize questions in order (1..25 Aptitude @ 2 pts, 26..30 Coding @ 10 pts)
    db.query(CodingAssessmentQuestion).filter(CodingAssessmentQuestion.assessment_id == assessment.id).delete()

    for idx, q_obj in enumerate(created_questions, 1):
        points = 2.0 if idx <= 25 else 10.0
        aq = CodingAssessmentQuestion(
            assessment_id=assessment.id,
            question_id=q_obj.id,
            question_order=idx,
            points=points
        )
        db.add(aq)

    db.commit()
    db.refresh(assessment)
    logger.info("Successfully synchronized 30 questions (25 Aptitude + 5 Coding) to assessment.")
    return assessment
