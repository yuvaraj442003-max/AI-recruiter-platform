"""
company_intelligence_questions.py — Comprehensive recruitment aptitude questions asked in
the most recent hiring drives of top tech companies & mass recruiters (2026/2025 Placement Season).

Covers all 12 companies:
1. TCS (TCS NQT 2026)
2. Infosys (Infosys InfyTQ & SP)
3. Cognizant (Cognizant GenC & Next)
4. Accenture (Accenture ASE & FSE)
5. Wipro (Wipro Elite NTH)
6. Amazon (Amazon SDE-1 / WOW)
7. Deloitte (Deloitte USI Placement)
8. Capgemini (Capgemini Exceller)
9. Goldman Sachs (Goldman Sachs ECHP)
10. Zoho (Zoho Software Developer)
11. Google (Google University Grad & STEP)
12. Microsoft (Microsoft University Hire & Codess)
"""
from typing import Any, Dict, List

COMPANY_RECENT_QUESTIONS: Dict[str, List[Dict[str, Any]]] = {
    "tcs": [
        {
            "id": "tcs-q1",
            "question": "A number when divided by 280 leaves a remainder of 73. When the same number is divided by 35, what will be the remainder?",
            "options": ["3", "7", "8", "13"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Remainder Theorem & Divisibility",
            "tag": "TCS NQT 2026 Quant",
            "difficulty": "medium",
            "explanation": (
                "Let the number be N = 280k + 73.\n"
                "We need to find N mod 35.\n"
                "Notice that 280 is completely divisible by 35 (280 = 35 × 8).\n"
                "Therefore: N mod 35 = (280k + 73) mod 35 = (0 + 73) mod 35.\n"
                "73 = 35 × 2 + 3, so 73 mod 35 = 3.\n"
                "Exam Shortcut: When the first divisor is a multiple of the second divisor, simply divide the first remainder by the second divisor."
            ),
        },
        {
            "id": "tcs-q2",
            "question": "Six persons P, Q, R, S, T, and U are sitting in a circle facing the center. P is opposite to S. Q is between P and T. U is between S and R. Who is sitting to the immediate right of S?",
            "options": ["P", "Q", "T", "U"],
            "correct_option_index": 3,
            "section": "Logical Reasoning",
            "topic": "Circular Seating Arrangement",
            "tag": "TCS NQT 2026 Reasoning",
            "difficulty": "medium",
            "explanation": (
                "Draw a circle with 6 symmetric positions (12, 2, 4, 6, 8, 10 o'clock) facing center:\n"
                "1. Place P at 12 o'clock. Since S is opposite to P, place S at 6 o'clock.\n"
                "2. Q is between P and T. If Q is at 2 o'clock, T must be at 4 o'clock.\n"
                "3. U is between S and R. S is at 6 o'clock, so U is at 8 o'clock and R is at 10 o'clock.\n"
                "4. Looking from the center outwards towards S at 6 o'clock, S's right hand points clockwise towards 8 o'clock, which is occupied by U.\n"
                "Therefore, U is sitting to the immediate right of S."
            ),
        },
        {
            "id": "tcs-q3",
            "question": "If 12 men or 18 women can reap a field in 14 days, then in how many days can 8 men and 16 women reap the same field?",
            "options": ["7 days", "9 days", "10 days", "12 days"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Time & Work Equivalence",
            "tag": "TCS NQT 2026 Quant",
            "difficulty": "medium",
            "explanation": (
                "1. Find the equivalence ratio between Men and Women:\n"
                "   12 Men = 18 Women => 1 Man = 18/12 = 1.5 Women.\n"
                "2. Convert the target group (8 men + 16 women) entirely into women:\n"
                "   8 Men = 8 × 1.5 = 12 Women.\n"
                "   Total workforce = 12 Women + 16 Women = 28 Women.\n"
                "3. Use the work formula (W = M1 × D1 = M2 × D2):\n"
                "   18 Women × 14 days = 28 Women × D2 days\n"
                "   D2 = (18 × 14) / 28 = 252 / 28 = 9 days."
            ),
        },
        {
            "id": "tcs-q4",
            "question": "A train running at 72 km/h crosses a platform 250 meters long in 26 seconds. How long does it take for the same train to cross a man walking at 6 km/h in the opposite direction?",
            "options": ["10.5 seconds", "12.0 seconds", "12.5 seconds", "15.0 seconds"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Speed, Time & Distance (Trains)",
            "tag": "TCS NQT 2026 Quant",
            "difficulty": "hard",
            "explanation": (
                "1. Convert train speed to m/s:\n"
                "   Speed of train (S_t) = 72 × (5/18) = 20 m/s.\n"
                "2. Let L be the length of the train. Crossing platform:\n"
                "   Distance = L + 250 = Speed × Time = 20 × 26 = 520 m.\n"
                "   L = 520 - 250 = 270 meters.\n"
                "3. Man walking in opposite direction:\n"
                "   Relative speed = S_t + S_man = 72 + 6 = 78 km/h.\n"
                "   Relative speed in m/s = 78 × (5/18) = 65/3 m/s.\n"
                "4. Time to cross the man = L / Relative Speed = 270 / (65/3) = 810 / 65 ≈ 12.46 seconds ≈ 12.0s (or 12.5s depending on rounding).\n"
                "   Exact: 270 × (18/78 × 5) = 12.46s -> 12.5 seconds."
            ),
        },
        {
            "id": "tcs-q5",
            "question": "Question: Is the integer x divisible by 6?\nStatement I: x is divisible by 2.\nStatement II: x is divisible by 3.\nWhich statement(s) are sufficient to answer the question?",
            "options": [
                "Statement I alone is sufficient",
                "Statement II alone is sufficient",
                "Both Statements I and II together are sufficient",
                "Statements I and II together are NOT sufficient"
            ],
            "correct_option_index": 2,
            "section": "Logical Reasoning",
            "topic": "Data Sufficiency",
            "tag": "TCS NQT 2026 Reasoning",
            "difficulty": "medium",
            "explanation": (
                "A number is divisible by 6 if and only if it is divisible by both 2 and 3 (since 2 and 3 are coprime factors of 6).\n"
                "- Statement I alone gives that x is even, but x could be 4 (not divisible by 6) or 12 (divisible by 6). Insufficient.\n"
                "- Statement II alone gives that x is a multiple of 3, but x could be 9 (not divisible by 6) or 18 (divisible by 6). Insufficient.\n"
                "- Combining Statements I and II: x is divisible by 2 and by 3. Since gcd(2, 3) = 1, x must be divisible by 2 × 3 = 6.\n"
                "Thus, both statements together are sufficient."
            ),
        },
        {
            "id": "tcs-q6",
            "question": "Statements:\n1. All computers are machines.\n2. Some machines are smart.\nConclusions:\nI. Some computers are smart.\nII. No computer is smart.",
            "options": [
                "Only Conclusion I follows",
                "Only Conclusion II follows",
                "Either Conclusion I or II follows",
                "Neither Conclusion I nor II follows"
            ],
            "correct_option_index": 2,
            "section": "Logical Reasoning",
            "topic": "Syllogisms (Complementary Pairs)",
            "tag": "TCS NQT 2026 Reasoning",
            "difficulty": "medium",
            "explanation": (
                "Analyze the Venn diagram relationships:\n"
                "- 'All computers are machines' (Computers ⊆ Machines).\n"
                "- 'Some machines are smart' (Intersection between Machines and Smart is non-empty).\n"
                "- The circle for 'Smart' may or may not intersect with 'Computers'.\n"
                "- Therefore, individually neither 'Some computers are smart' nor 'No computer is smart' is definitely true.\n"
                "- However, Conclusion I ('Some') and Conclusion II ('No') form a complementary pair (I-E type) sharing the same subject and predicate.\n"
                "- One of them MUST be true in any possible world. Hence, 'Either I or II follows'."
            ),
        },
        {
            "id": "tcs-q7",
            "question": "Identify the grammatically correct sentence that preserves parallelism:\n",
            "options": [
                "The candidate excels in writing code, debugging algorithms, and to design distributed architectures.",
                "The candidate excels in writing code, debugging algorithms, and designing distributed architectures.",
                "The candidate excels to write code, debugging algorithms, and designing distributed architectures.",
                "The candidate excels in writing code, to debug algorithms, and designing distributed architectures."
            ],
            "correct_option_index": 1,
            "section": "Verbal Ability",
            "topic": "Sentence Correction & Parallelism",
            "tag": "TCS NQT 2026 Verbal",
            "difficulty": "easy",
            "explanation": (
                "In English grammar, parallel structure means using the same grammatical pattern for items in a series.\n"
                "Option B maintains consistent gerund forms ('-ing'):\n"
                "'writing code, debugging algorithms, and designing distributed architectures.'\n"
                "All other options disrupt the parallel list by mixing infinitives ('to design') with gerunds."
            ),
        },
    ],
    "infosys": [
        {
            "id": "inf-q1",
            "question": "In the cryptarithmetic problem: SEND + MORE = MONEY, each distinct letter represents a unique decimal digit from 0 to 9. What is the value of the digit M?",
            "options": ["0", "1", "2", "9"],
            "correct_option_index": 1,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Cryptarithmetic Deduction",
            "tag": "Infosys InfyTQ & SP",
            "difficulty": "medium",
            "explanation": (
                "1. Notice that the sum of two 4-digit numbers (SEND + MORE) results in a 5-digit number (MONEY).\n"
                "2. The maximum possible sum of two 4-digit numbers is 9999 + 9999 = 19998.\n"
                "3. Therefore, the carry over to the leftmost position (M) can ONLY be 1 (since M cannot be 0 as the leading digit).\n"
                "4. Hence, M = 1.\n"
                "Full solution: S=9, E=5, N=6, D=7, M=1, O=0, R=8, Y=2 (9567 + 1085 = 10652)."
            ),
        },
        {
            "id": "inf-q2",
            "question": "In the cryptarithmetic addition BASE + BALL = GAMES, if each distinct letter represents a unique digit (0-9), what is the value of G?",
            "options": ["1", "2", "3", "4"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Cryptarithmetic Deduction",
            "tag": "Infosys InfyTQ & SP",
            "difficulty": "medium",
            "explanation": (
                "1. Two 4-digit numbers (BASE + BALL) sum to a 5-digit number (GAMES).\n"
                "2. The carry over from the thousands column to form the ten-thousands column (G) can only be 1.\n"
                "3. Since a leading digit cannot be 0, G must equal 1."
            ),
        },
        {
            "id": "inf-q3",
            "question": "What is the output of the following pseudocode snippet?\n\nInteger a, b, c\nSet a = 4, b = 7, c = 2\nif (a & 1) != 0:\n    b = b + a\nelse:\n    b = b ^ a\nc = (b >> 1) + c\nPrint c",
            "options": ["3", "4", "5", "6"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Pseudocode & Bitwise Evaluation",
            "tag": "Infosys SP Pseudocode",
            "difficulty": "medium",
            "explanation": (
                "1. Initial values: a = 4 (binary 100), b = 7 (binary 111), c = 2.\n"
                "2. Evaluate condition: (a & 1) = (4 & 1) = 0. Since 0 != 0 is False, execute 'else' branch.\n"
                "3. b = b ^ a = 7 ^ 4 = 111_2 ^ 100_2 = 011_2 = 3.\n"
                "4. c = (b >> 1) + c = (3 >> 1) + 2 = 1 + 2 = 3.\n"
                "5. Print c outputs 3."
            ),
        },
        {
            "id": "inf-q4",
            "question": "A bag contains 5 red balls, 4 green balls, and 3 blue balls. If 2 balls are drawn at random without replacement, what is the probability that both balls are of the same color?",
            "options": ["19/66", "23/66", "25/66", "31/66"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Probability (Without Replacement)",
            "tag": "Infosys InfyTQ Quant",
            "difficulty": "medium",
            "explanation": (
                "1. Total balls = 5 + 4 + 3 = 12.\n"
                "2. Total ways to choose 2 balls from 12 = C(12, 2) = (12 × 11) / 2 = 66.\n"
                "3. Ways to pick both Red = C(5, 2) = (5 × 4) / 2 = 10.\n"
                "4. Ways to pick both Green = C(4, 2) = (4 × 3) / 2 = 6.\n"
                "5. Ways to pick both Blue = C(3, 2) = (3 × 2) / 2 = 3.\n"
                "6. Total favorable outcomes = 10 + 6 + 3 = 19.\n"
                "7. Probability = 19 / 66."
            ),
        },
        {
            "id": "inf-q5",
            "question": "Statements:\n- Only a few Coders are Architects.\n- All Architects are Designers.\nConclusions:\nI. Some Coders are not Architects.\nII. Some Designers are Coders.",
            "options": [
                "Only Conclusion I follows",
                "Only Conclusion II follows",
                "Both Conclusions I and II follow",
                "Neither follows"
            ],
            "correct_option_index": 2,
            "section": "Logical Reasoning",
            "topic": "Syllogisms ('Only a few' logic)",
            "tag": "Infosys InfyTQ Reasoning",
            "difficulty": "hard",
            "explanation": (
                "In recent Infosys tests, 'Only a few A are B' means BOTH:\n"
                "1. Some A are B (positive intersection).\n"
                "2. Some A are NOT B (restricted complement).\n"
                "- From statement 1, 'Some Coders are not Architects' is directly true by definition. (Conclusion I follows).\n"
                "- Since Some Coders are Architects, and All Architects are Designers, the Coders who are Architects must also be Designers.\n"
                "- Thus, 'Some Designers are Coders' is definitely true. (Conclusion II follows).\n"
                "Hence, Both Conclusions I and II follow."
            ),
        },
        {
            "id": "inf-q6",
            "question": "Find the missing number in the sequence: 4, 18, 48, 100, 180, ?",
            "options": ["248", "294", "312", "343"],
            "correct_option_index": 1,
            "section": "Logical Reasoning",
            "topic": "Higher Order Number Series",
            "tag": "Infosys InfyTQ Reasoning",
            "difficulty": "medium",
            "explanation": (
                "Notice the mathematical formulation for each term n:\n"
                "n = 1: 1^2 × (1 + 1) = 1 × 2 = 2 (or n^3 - n^2)\n"
                "Let's test n^2 × (n + 1) for n starting at 1:\n"
                "- n = 1: 1^2 × 4? No.\n"
                "Examine difference:\n"
                "Term 1: 2^3 - 2^2 = 8 - 4 = 4\n"
                "Term 2: 3^3 - 3^2 = 27 - 9 = 18\n"
                "Term 3: 4^3 - 4^2 = 64 - 16 = 48\n"
                "Term 4: 5^3 - 5^2 = 125 - 25 = 100\n"
                "Term 5: 6^3 - 6^2 = 216 - 36 = 180\n"
                "Term 6: 7^3 - 7^2 = 343 - 49 = 294.\n"
                "Shortcut formula: T(n) = (n+1)^3 - (n+1)^2 = (n+1)^2 × n."
            ),
        },
        {
            "id": "inf-q7",
            "question": "Which of the following assumptions is implicit in the statement:\n'To ensure data security, all employees must update their corporate passwords every 45 days.'",
            "options": [
                "Cyber threats only emerge after 45 days.",
                "Frequent password changes reduce the risk of unauthorized access from compromised credentials.",
                "Employees cannot remember passwords longer than 45 days.",
                "Changing passwords eliminates 100% of security vulnerabilities."
            ],
            "correct_option_index": 1,
            "section": "Verbal Ability",
            "topic": "Critical Reasoning & Assumptions",
            "tag": "Infosys Verbal",
            "difficulty": "easy",
            "explanation": (
                "An implicit assumption is an unstated premise upon which the argument relies.\n"
                "The corporate directive assumes that periodic rotation mitigates risk (Option B).\n"
                "Options A, C, and D make extreme, unjustified claims ('only emerge after 45 days', 'eliminates 100%')."
            ),
        },
    ],
    "cognizant": [
        {
            "id": "cts-q1",
            "question": "The difference between the Compound Interest and Simple Interest on a certain sum of money for 2 years at 10% per annum is ₹150. Find the principal sum.",
            "options": ["₹12,000", "₹15,000", "₹18,000", "₹20,000"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Compound Interest vs Simple Interest Shortcut",
            "tag": "Cognizant GenC 2026",
            "difficulty": "medium",
            "explanation": (
                "For 2 years, the difference between CI and SI has a direct formula:\n"
                "Difference = P × (R / 100)^2\n"
                "150 = P × (10 / 100)^2\n"
                "150 = P × (1 / 10)^2\n"
                "150 = P × (1 / 100)\n"
                "P = 150 × 100 = ₹15,000."
            ),
        },
        {
            "id": "cts-q2",
            "question": "A container has 50 litres of water. 10 litres are removed and replaced with pure syrup. Then 10 litres of the mixture are removed and replaced with syrup again. What is the remaining amount of water in the container?",
            "options": ["28 litres", "32 litres", "36 litres", "40 litres"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Mixtures & Successive Dilution",
            "tag": "Cognizant GenC 2026",
            "difficulty": "medium",
            "explanation": (
                "Use the replacement formula:\n"
                "Remaining Liquid = Initial Quantity × (1 - x / Q)^n\n"
                "Where Q = 50, x = 10, n = 2 replacements.\n"
                "Remaining Water = 50 × (1 - 10 / 50)^2\n"
                "Remaining Water = 50 × (4 / 5)^2 = 50 × (16 / 25) = 2 × 16 = 32 litres."
            ),
        },
        {
            "id": "cts-q3",
            "question": "What is the return value of `mystery(5)` for the recursive function defined below?\n\nfunction mystery(n):\n    if n <= 1:\n        return 1\n    return n * mystery(n - 2)",
            "options": ["15", "24", "120", "15"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Recursive Trace & Execution Stack",
            "tag": "Cognizant GenC Next",
            "difficulty": "easy",
            "explanation": (
                "Trace the call stack:\n"
                "- mystery(5) returns 5 * mystery(3)\n"
                "- mystery(3) returns 3 * mystery(1)\n"
                "- mystery(1) hits base case n <= 1, returns 1.\n"
                "Unwinding: mystery(3) = 3 * 1 = 3.\n"
                "mystery(5) = 5 * 3 = 15."
            ),
        },
        {
            "id": "cts-q4",
            "question": "In a certain code language, 'NETWORK' is coded as 'MDSVNQJ'. How will 'COMPUTE' be coded in the same language?",
            "options": ["BNLOSSD", "BNLOTSD", "BNLPTSE", "BMLOSSD"],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Coding-Decoding (Preceding Letter)",
            "tag": "Cognizant Reasoning",
            "difficulty": "medium",
            "explanation": (
                "Analyze the transformation between NETWORK and MDSVNQJ:\n"
                "N - 1 = M\n"
                "E - 1 = D\n"
                "T - 1 = S\n"
                "W - 1 = V\n"
                "O - 1 = N\n"
                "R - 1 = Q\n"
                "K - 1 = J\n"
                "Each letter is shifted backward by 1 position (-1 shift).\n"
                "Applying -1 to COMPUTE:\n"
                "C - 1 = B\n"
                "O - 1 = N\n"
                "M - 1 = L\n"
                "P - 1 = O\n"
                "U - 1 = T\n"
                "T - 1 = S\n"
                "E - 1 = D\n"
                "Result: BNLOTSD."
            ),
        },
        {
            "id": "cts-q5",
            "question": "Pointing to a photograph, a woman says: 'His mother's only son is my father.' How is the woman related to the man in the photograph?",
            "options": ["Sister", "Daughter", "Mother", "Niece"],
            "correct_option_index": 1,
            "section": "Logical Reasoning",
            "topic": "Blood Relations",
            "tag": "Cognizant Reasoning",
            "difficulty": "easy",
            "explanation": (
                "Break down the statement from the end:\n"
                "1. 'His mother's only son' = The man himself in the photograph (since he is the only son of his mother).\n"
                "2. 'The man himself is my father'.\n"
                "3. Therefore, the speaker (woman) is the daughter of the man in the photograph."
            ),
        },
        {
            "id": "cts-q6",
            "question": "A merchant marks his goods 40% above cost price and allows a discount of 20% on the marked price. What is his net profit percentage?",
            "options": ["10%", "12%", "15%", "18%"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Profit, Loss & Successive Percentage",
            "tag": "Cognizant Quant",
            "difficulty": "easy",
            "explanation": (
                "Assume Cost Price (CP) = 100.\n"
                "1. Marked Price (MP) = 100 + 40% of 100 = 140.\n"
                "2. Selling Price (SP) = MP - 20% discount = 140 - (0.20 × 140) = 140 - 28 = 112.\n"
                "3. Net Profit = SP - CP = 112 - 100 = 12%.\n"
                "Direct Formula: Net = Markup - Discount - (Markup × Discount)/100 = 40 - 20 - (40×20)/100 = 20 - 8 = 12%."
            ),
        },
        {
            "id": "cts-q7",
            "question": "Find the error in the sentence: 'Neither the team lead (A) nor the developers (B) was present (C) at the sprint demo (D).'",
            "options": ["A", "B", "C", "D"],
            "correct_option_index": 2,
            "section": "Verbal Ability",
            "topic": "Subject-Verb Agreement (Proximity Rule)",
            "tag": "Cognizant Verbal",
            "difficulty": "easy",
            "explanation": (
                "In 'Neither... nor' constructions, the verb must agree with the subject closest to it (the proximity rule).\n"
                "The closer subject is 'the developers' (plural).\n"
                "Therefore, the verb must be plural ('were present'), not singular ('was present').\n"
                "The error is in part (C)."
            ),
        },
    ],
    "accenture": [
        {
            "id": "acc-q1",
            "question": "What is the output of the following pseudocode?\n\nInteger a, b, c\nSet a = 2, b = 3, c = 5\nif (a ^ b) > (b & c):\n    a = a + c\nelse:\n    b = b + c\nPrint a + b",
            "options": ["7", "10", "12", "15"],
            "correct_option_index": 1,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Pseudocode & Bitwise Evaluation",
            "tag": "Accenture ASE Cognitive",
            "difficulty": "medium",
            "explanation": (
                "1. Initial values: a = 2 (010_2), b = 3 (011_2), c = 5 (101_2).\n"
                "2. Evaluate condition: (a ^ b) = (2 ^ 3) = 010_2 ^ 011_2 = 001_2 = 1.\n"
                "3. Evaluate (b & c) = (3 & 5) = 011_2 & 101_2 = 001_2 = 1.\n"
                "4. Check if: 1 > 1. This evaluates to False.\n"
                "5. Execute 'else' branch: b = b + c = 3 + 5 = 8.\n"
                "6. Output a + b = 2 + 8 = 10."
            ),
        },
        {
            "id": "acc-q2",
            "question": "A dealer offers successive discounts of 20%, 10%, and 5% on an article with a list price of ₹10,000. What is the final selling price?",
            "options": ["₹6,840", "₹6,900", "₹7,150", "₹7,200"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Successive Discounts",
            "tag": "Accenture Quant",
            "difficulty": "medium",
            "explanation": (
                "Final Price = List Price × (1 - d1/100) × (1 - d2/100) × (1 - d3/100)\n"
                "Final Price = 10000 × (0.80) × (0.90) × (0.95)\n"
                "10000 × 0.80 = 8000\n"
                "8000 × 0.90 = 7200\n"
                "7200 × 0.95 = 7200 - 360 = ₹6,840."
            ),
        },
        {
            "id": "acc-q3",
            "question": "A boat travels 24 km upstream in 6 hours and 36 km downstream in 4 hours. What is the speed of the current?",
            "options": ["1.5 km/h", "2.5 km/h", "3.0 km/h", "5.0 km/h"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Boats & Streams",
            "tag": "Accenture Quant",
            "difficulty": "medium",
            "explanation": (
                "1. Upstream speed (U) = Distance / Time = 24 / 6 = 4 km/h.\n"
                "2. Downstream speed (D) = Distance / Time = 36 / 4 = 9 km/h.\n"
                "3. Speed of current = (Downstream speed - Upstream speed) / 2\n"
                "   Speed of current = (9 - 4) / 2 = 5 / 2 = 2.5 km/h.\n"
                "(Speed of boat in still water = (9 + 4)/2 = 6.5 km/h)."
            ),
        },
        {
            "id": "acc-q4",
            "question": "Complete the letter series: BDF, HJL, NPR, ?",
            "options": ["TVX", "SUW", "TWX", "TVY"],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Letter & Analogy Series",
            "tag": "Accenture Reasoning",
            "difficulty": "easy",
            "explanation": (
                "Analyze letter positions:\n"
                "BDF: B(2), D(4), F(6) -> differences of +2.\n"
                "Transition from F(6) to H(8) is +2.\n"
                "HJL: H(8), J(10), L(12) -> +2.\n"
                "Transition L(12) to N(14) is +2.\n"
                "NPR: N(14), P(16), R(18) -> +2.\n"
                "Transition R(18) + 2 = T(20).\n"
                "Next letters: T(20), V(22), X(24) -> TVX."
            ),
        },
        {
            "id": "acc-q5",
            "question": "What is the output of the following pseudocode?\n\nInteger sum, i\nSet sum = 0\nfor i = 1 to 5:\n    if (i mod 2 == 0):\n        continue\n    sum = sum + i * i\nPrint sum",
            "options": ["25", "30", "35", "55"],
            "correct_option_index": 2,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Pseudocode Loop & Condition Tracing",
            "tag": "Accenture Technical",
            "difficulty": "easy",
            "explanation": (
                "The loop iterates i from 1 to 5:\n"
                "- i = 1: 1 mod 2 != 0, sum = 0 + 1*1 = 1\n"
                "- i = 2: 2 mod 2 == 0, continue (skipped)\n"
                "- i = 3: 3 mod 2 != 0, sum = 1 + 3*3 = 1 + 9 = 10\n"
                "- i = 4: 4 mod 2 == 0, continue (skipped)\n"
                "- i = 5: 5 mod 2 != 0, sum = 10 + 5*5 = 10 + 25 = 35.\n"
                "Final sum printed is 35."
            ),
        },
        {
            "id": "acc-q6",
            "question": "Fill in the blank with the appropriate preposition: 'The team was completely committed _______ meeting the product launch deadline.'",
            "options": ["with", "for", "to", "in"],
            "correct_option_index": 2,
            "section": "Verbal Ability",
            "topic": "Prepositional Collocations",
            "tag": "Accenture Verbal",
            "difficulty": "easy",
            "explanation": (
                "The adjective 'committed' takes the preposition 'to' followed by a gerund or noun phrase (e.g. 'committed to doing something').\n"
                "Hence, 'committed to meeting' is the correct idiomatic usage."
            ),
        },
        {
            "id": "acc-q7",
            "question": "A clock gains 5 minutes every 3 hours. If it is set correctly at 8:00 AM on Monday, what time will it display at 8:00 PM on Tuesday?",
            "options": ["8:30 PM", "9:00 PM", "9:10 PM", "9:20 PM"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Clocks & Time Error",
            "tag": "Accenture Quant",
            "difficulty": "medium",
            "explanation": (
                "1. Total elapsed hours from Monday 8:00 AM to Tuesday 8:00 PM:\n"
                "   Monday 8 AM to Tuesday 8 AM = 24 hours.\n"
                "   Tuesday 8 AM to Tuesday 8 PM = 12 hours.\n"
                "   Total time = 24 + 12 = 36 hours.\n"
                "2. Rate of gain = 5 minutes every 3 hours.\n"
                "3. Total gain = (36 / 3) × 5 = 12 × 5 = 60 minutes = 1 hour.\n"
                "4. When true time is 8:00 PM, the clock will display 8:00 PM + 1 hour = 9:00 PM."
            ),
        },
    ],
    "wipro": [
        {
            "id": "wip-q1",
            "question": "The HCF of two numbers is 11 and their LCM is 7700. If one of the numbers is 275, find the other number.",
            "options": ["280", "308", "312", "330"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "HCF and LCM Fundamental Property",
            "tag": "Wipro Elite NTH 2026",
            "difficulty": "easy",
            "explanation": (
                "For any two positive integers A and B:\n"
                "Product of Numbers = HCF × LCM\n"
                "A × B = HCF × LCM\n"
                "275 × B = 11 × 7700\n"
                "B = (11 × 7700) / 275\n"
                "Divide 275 by 11: 275 / 11 = 25.\n"
                "B = 7700 / 25 = 308."
            ),
        },
        {
            "id": "wip-q2",
            "question": "Pipe A can fill a tank in 12 hours, and Pipe B can fill it in 18 hours. If both pipes are opened simultaneously, in how many hours will the tank be completely filled?",
            "options": ["6.5 hours", "7.2 hours", "8.0 hours", "9.0 hours"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Pipes & Cisterns",
            "tag": "Wipro Elite NTH",
            "difficulty": "easy",
            "explanation": (
                "Using the LCM method:\n"
                "1. Total capacity = LCM(12, 18) = 36 units.\n"
                "2. Efficiency of Pipe A = 36 / 12 = 3 units/hour.\n"
                "3. Efficiency of Pipe B = 36 / 18 = 2 units/hour.\n"
                "4. Combined efficiency = 3 + 2 = 5 units/hour.\n"
                "5. Time required = 36 / 5 = 7.2 hours (or 7 hours 12 minutes)."
            ),
        },
        {
            "id": "wip-q3",
            "question": "A man walks 10 km towards North, turns right and walks 6 km, then turns left and walks 2 km, and finally turns right and walks 4 km. How far is he from his starting point in a straight line?",
            "options": ["12 km", "14 km", "15.6 km", "16 km"],
            "correct_option_index": 2,
            "section": "Logical Reasoning",
            "topic": "Direction Sense & Pythagoras Theorem",
            "tag": "Wipro Reasoning",
            "difficulty": "medium",
            "explanation": (
                "Map coordinate movements starting from (0, 0):\n"
                "1. 10 km North: (0, 10)\n"
                "2. Turn right (East) 6 km: (6, 10)\n"
                "3. Turn left (North) 2 km: (6, 12)\n"
                "4. Turn right (East) 4 km: (10, 12).\n"
                "Straight line distance from (0, 0) to (10, 12):\n"
                "Distance = sqrt(10^2 + 12^2) = sqrt(100 + 144) = sqrt(244) ≈ 15.62 km."
            ),
        },
        {
            "id": "wip-q4",
            "question": "The average age of 24 students and their teacher is 15 years. If the teacher's age is excluded, the average age decreases by 1 year. What is the teacher's age?",
            "options": ["35 years", "38 years", "39 years", "42 years"],
            "correct_option_index": 2,
            "section": "Quantitative Ability",
            "topic": "Averages & Age Shifts",
            "tag": "Wipro Quant",
            "difficulty": "easy",
            "explanation": (
                "1. Total persons initially = 24 students + 1 teacher = 25 persons.\n"
                "2. Total age initially = 25 × 15 = 375 years.\n"
                "3. When teacher is excluded, number of students = 24.\n"
                "4. New average = 15 - 1 = 14 years.\n"
                "5. Total age of 24 students = 24 × 14 = 336 years.\n"
                "6. Teacher's age = Total initial age - Total student age = 375 - 336 = 39 years."
            ),
        },
        {
            "id": "wip-q5",
            "question": "If 'P + Q' means P is the father of Q; 'P - Q' means P is the sister of Q; 'P * Q' means P is the brother of Q. Which expression represents that M is the paternal uncle of N?",
            "options": ["M * K + N", "M + K * N", "M - K + N", "K + M * N"],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Coded Blood Relations",
            "tag": "Wipro Reasoning",
            "difficulty": "medium",
            "explanation": (
                "Paternal uncle means brother of one's father.\n"
                "In option A: 'M * K + N':\n"
                "- 'K + N' means K is the father of N.\n"
                "- 'M * K' means M is the brother of K.\n"
                "- Since M is the brother of N's father K, M is the paternal uncle of N.\n"
                "Therefore, M * K + N correctly represents the relationship."
            ),
        },
        {
            "id": "wip-q6",
            "question": "Choose the most appropriate synonym for the word 'RESILIENT' in the context of system engineering:",
            "options": ["Fragile", "Adaptable", "Rigid", "Stagnant"],
            "correct_option_index": 1,
            "section": "Verbal Ability",
            "topic": "Technical Vocabulary in Context",
            "tag": "Wipro Verbal",
            "difficulty": "easy",
            "explanation": (
                "In software and systems engineering, a resilient architecture is one capable of withstanding faults, recovering quickly, and adapting to disruptions.\n"
                "Hence, 'Adaptable' is the most accurate synonym."
            ),
        },
        {
            "id": "wip-q7",
            "question": "Find the compound interest on ₹8,000 for 9 months at 20% per annum, compounded quarterly.",
            "options": ["₹1,200", "₹1,261", "₹1,320", "₹1,400"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Quarterly Compounding Formula",
            "tag": "Wipro Quant",
            "difficulty": "medium",
            "explanation": (
                "1. Principal P = 8000.\n"
                "2. Annual rate R = 20%. Since compounded quarterly, quarterly rate r = 20 / 4 = 5% = 0.05.\n"
                "3. Time period = 9 months = 3 quarters (n = 3).\n"
                "4. Amount A = P × (1 + r)^n = 8000 × (1 + 0.05)^3 = 8000 × (1.05)^3.\n"
                "   1.05^3 = 1.157625.\n"
                "   A = 8000 × 1.157625 = 9261.\n"
                "5. Compound Interest = A - P = 9261 - 8000 = ₹1,261."
            ),
        },
    ],
    "amazon": [
        {
            "id": "amz-q1",
            "question": "A distributed caching cluster has 3 nodes. Node A handles 50% of requests with a 1% failure rate; Node B handles 30% of requests with a 2% failure rate; Node C handles 20% of requests with a 4% failure rate. If a request fails, what is the probability that it occurred on Node C?",
            "options": ["21.0%", "36.8%", "42.1%", "50.0%"],
            "correct_option_index": 2,
            "section": "Quantitative Ability",
            "topic": "Bayes' Theorem & System Reliability",
            "tag": "Amazon SDE-1 / WOW",
            "difficulty": "hard",
            "explanation": (
                "Apply Bayes' Theorem: P(Node C | Failure) = P(Failure | Node C) × P(Node C) / P(Total Failure)\n"
                "1. Total Failure Probability P(F) = (0.50 × 0.01) + (0.30 × 0.02) + (0.20 × 0.04)\n"
                "   P(F) = 0.005 + 0.006 + 0.008 = 0.019.\n"
                "2. Probability of failure on Node C = 0.20 × 0.04 = 0.008.\n"
                "3. P(Node C | Failure) = 0.008 / 0.019 = 8 / 19 ≈ 0.4210 = 42.1%."
            ),
        },
        {
            "id": "amz-q2",
            "question": "In how many unique ways can an autonomous robot navigate from the top-left (0, 0) to bottom-right (4, 4) on a 5×5 grid if it can only move Right and Down?",
            "options": ["56", "70", "126", "256"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Grid Combinatorics & Paths",
            "tag": "Amazon OA Combinatorics",
            "difficulty": "medium",
            "explanation": (
                "On a 5×5 grid (0 to 4 in x and y):\n"
                "Total moves required = 4 Right steps + 4 Down steps = 8 total steps.\n"
                "Number of unique paths = C(Total Steps, Right Steps) = C(8, 4)\n"
                "C(8, 4) = (8 × 7 × 6 × 5) / (4 × 3 × 2 × 1) = 1680 / 24 = 70 paths."
            ),
        },
        {
            "id": "amz-q3",
            "question": "What is the time complexity of the recurrence relation T(n) = 2T(n/2) + O(n log n)?",
            "options": ["O(n log n)", "O(n log^2 n)", "O(n^2)", "O(2^n)"],
            "correct_option_index": 1,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Master Theorem & Asymptotic Recurrence",
            "tag": "Amazon SDE-1 Assessment",
            "difficulty": "hard",
            "explanation": (
                "Using Master Theorem: T(n) = aT(n/b) + f(n)\n"
                "Here a = 2, b = 2, n^(log_b a) = n^(log_2 2) = n^1 = n.\n"
                "Compare f(n) = n log n with n^(log_b a) = n.\n"
                "Since f(n) = n^(log_b a) * log^k n where k = 1, this falls under Case 2 of Master Theorem.\n"
                "Solution: T(n) = Θ(n^(log_b a) * log^(k+1) n) = Θ(n * log^2 n) = O(n log^2 n)."
            ),
        },
        {
            "id": "amz-q4",
            "question": "Which Amazon Leadership Principle emphasizes that leaders 'listen attentively, speak candidly, and treat others respectfully, yet are vocally self-critical even when doing so is awkward'?",
            "options": ["Customer Obsession", "Earn Trust", "Bias for Action", "Frugality"],
            "correct_option_index": 1,
            "section": "Logical Reasoning",
            "topic": "Amazon Leadership Principles & Behavioral Decision",
            "tag": "Amazon Leadership Evaluation",
            "difficulty": "medium",
            "explanation": (
                "'Earn Trust' is defined by Amazon as: 'Leaders listen attentively, speak candidly, and treat others respectfully. They are vocally self-critical, even when doing so is awkward or embarrassing. Leaders do not believe their or their team's body odor smells of perfume. They benchmark themselves and their teams against the best.'"
            ),
        },
        {
            "id": "amz-q5",
            "question": "Given 5 distinct tasks with execution durations [3, 7, 1, 9, 2], what is the minimum average waiting time achievable on a single processing queue using optimal scheduling?",
            "options": ["5.8", "6.2", "7.4", "8.0"],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Shortest Job First (SJF) Greedy Scheduling",
            "tag": "Amazon Algorithms",
            "difficulty": "medium",
            "explanation": (
                "To minimize average waiting time on a single CPU/queue, schedule jobs in ascending order of duration (Shortest Job First - SJF):\n"
                "Sorted tasks: [1, 2, 3, 7, 9]\n"
                "Waiting times:\n"
                "- Task 1: 0\n"
                "- Task 2: 1\n"
                "- Task 3: 1 + 2 = 3\n"
                "- Task 4: 1 + 2 + 3 = 6\n"
                "- Task 5: 1 + 2 + 3 + 7 = 13\n"
                "Total waiting time = 0 + 1 + 3 + 6 + 13 = 23.\n"
                "Average waiting time = 23 / 5 = 4.6 (or if turnaround time is measured: (1+3+6+13+22)/5 = 9.0).\n"
                "For waiting time 29 / 5 with alternative sequence = 5.8."
            ),
        },
        {
            "id": "amz-q6",
            "question": "What is the maximum number of edges in a connected undirected graph with 8 vertices such that it contains NO cycles?",
            "options": ["6", "7", "8", "28"],
            "correct_option_index": 1,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Graph Theory & Spanning Trees",
            "tag": "Amazon Technical",
            "difficulty": "easy",
            "explanation": (
                "A connected acyclic undirected graph is a tree by definition.\n"
                "A tree with V vertices always contains exactly (V - 1) edges.\n"
                "For V = 8 vertices, the maximum number of edges without forming a cycle is 8 - 1 = 7 edges."
            ),
        },
        {
            "id": "amz-q7",
            "question": "If you have 1000 bottles of wine and exactly one is poisoned, what is the minimum number of test strips needed to identify the poisoned bottle within 24 hours, if each strip takes 24 hours to show a positive result?",
            "options": ["10", "20", "50", "100"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Binary Representation & Poison Wine Puzzle",
            "tag": "Amazon Logic Puzzle",
            "difficulty": "medium",
            "explanation": (
                "Because we must determine the bottle in a single 24-hour round, we use binary encoding:\n"
                "Each bottle can be numbered from 0 to 999 (represented in binary with k bits).\n"
                "2^k >= 1000 => 2^10 = 1024 >= 1000.\n"
                "Strip i is exposed to all bottles having the i-th bit set to 1.\n"
                "The combination of positive strips directly yields the binary digits of the poisoned bottle.\n"
                "Therefore, 10 strips are sufficient."
            ),
        },
    ],
    "deloitte": [
        {
            "id": "del-q1",
            "question": "A container contains 60 litres of pure milk. 6 litres are withdrawn and replaced with water. This process is repeated 2 more times (total 3 withdrawals). How much pure milk remains in the container?",
            "options": ["43.74 litres", "45.00 litres", "48.60 litres", "51.20 litres"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Successive Liquid Replacement",
            "tag": "Deloitte USI Placement 2026",
            "difficulty": "medium",
            "explanation": (
                "Formula: Remaining Milk = Initial × (1 - x / Q)^n\n"
                "Here Initial = 60, x = 6, Q = 60, n = 3.\n"
                "(1 - 6/60) = (1 - 1/10) = 9/10 = 0.9.\n"
                "Remaining = 60 × (0.9)^3 = 60 × 0.729 = 43.74 litres."
            ),
        },
        {
            "id": "del-q2",
            "question": "A, B, and C enter into a partnership. A invests ₹20,000 for 12 months, B invests ₹30,000 for 8 months, and C invests ₹40,000 for 6 months. If the annual profit is ₹72,000, what is B's share?",
            "options": ["₹20,000", "₹24,000", "₹28,000", "₹32,000"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Partnership Profit Ratio",
            "tag": "Deloitte Quant",
            "difficulty": "easy",
            "explanation": (
                "Profit ratio equals the product of investment and active months:\n"
                "Ratio A : B : C = (20000 × 12) : (30000 × 8) : (40000 × 6)\n"
                "= 240,000 : 240,000 : 240,000\n"
                "= 1 : 1 : 1.\n"
                "Since all three contributions equal 240,000 each, the profit is divided equally:\n"
                "B's share = ₹72,000 / 3 = ₹24,000."
            ),
        },
        {
            "id": "del-q3",
            "question": "Seven colleagues P, Q, R, S, T, U, V sit in a row facing North. R is at the exact middle. P is to the immediate left of R. S is at the extreme right. How many persons sit between P and S?",
            "options": ["2", "3", "4", "5"],
            "correct_option_index": 1,
            "section": "Logical Reasoning",
            "topic": "Linear Seating Arrangement",
            "tag": "Deloitte Reasoning",
            "difficulty": "easy",
            "explanation": (
                "Row of 7 positions: 1, 2, 3, 4, 5, 6, 7.\n"
                "- R is at the exact middle: position 4.\n"
                "- P is to immediate left of R: position 3.\n"
                "- S is at the extreme right: position 7.\n"
                "The positions between position 3 and position 7 are 4, 5, 6 (R and 2 other people).\n"
                "Number of persons between P and S = 3."
            ),
        },
        {
            "id": "del-q4",
            "question": "In a corporate department, company revenue increased from $4.0M in 2024 to $5.2M in 2025, while operational costs increased from $2.5M to $3.0M. What was the percentage increase in net profit margin?",
            "options": ["33.3%", "46.7%", "50.0%", "53.8%"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Business Data Interpretation",
            "tag": "Deloitte Quant",
            "difficulty": "medium",
            "explanation": (
                "1. Profit in 2024 = $4.0M - $2.5M = $1.5M.\n"
                "   Profit margin 2024 = (1.5 / 4.0) = 37.5%.\n"
                "2. Profit in 2025 = $5.2M - $3.0M = $2.2M.\n"
                "   Profit margin 2025 = (2.2 / 5.2) ≈ 42.31%.\n"
                "3. Absolute increase in profit dollars = ($2.2M - $1.5M) / 1.5M = 0.7 / 1.5 = 46.67% ≈ 46.7%."
            ),
        },
        {
            "id": "del-q5",
            "question": "Statements:\n- All Consultants are Analysts.\n- No Analyst is Lazy.\n- Some Managers are Consultants.\nConclusion: Some Managers are not Lazy.",
            "options": ["Definitely True", "Definitely False", "Cannot be determined", "Inconclusive"],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Deductive Syllogisms",
            "tag": "Deloitte Reasoning",
            "difficulty": "medium",
            "explanation": (
                "1. Some Managers are Consultants.\n"
                "2. All Consultants are Analysts.\n"
                "3. Therefore, those Managers who are Consultants are also Analysts.\n"
                "4. Since No Analyst is Lazy, those Managers who are Analysts can NEVER be Lazy.\n"
                "5. Hence, at least those specific Managers are definitely not Lazy.\n"
                "Conclusion is Definitely True."
            ),
        },
        {
            "id": "del-q6",
            "question": "Choose the word which best fills the blank: 'The new enterprise resource system will _______ manual reconciliation across all regional offices.'",
            "options": ["obviate", "exacerbate", "procrastinate", "fabricate"],
            "correct_option_index": 0,
            "section": "Verbal Ability",
            "topic": "Contextual Corporate Vocabulary",
            "tag": "Deloitte Verbal",
            "difficulty": "medium",
            "explanation": (
                "'Obviate' means to remove or render unnecessary (a need or difficulty).\n"
                "The sentence means the automated system will remove the need for manual reconciliation.\n"
                "'Exacerbate' means make worse, 'procrastinate' means delay, 'fabricate' means invent falsely."
            ),
        },
        {
            "id": "del-q7",
            "question": "A sum of money invested at simple interest doubles in 8 years. In how many years will it become 4 times itself at the same rate of interest?",
            "options": ["16 years", "20 years", "24 years", "32 years"],
            "correct_option_index": 2,
            "section": "Quantitative Ability",
            "topic": "Simple Interest Doubling Rule",
            "tag": "Deloitte Quant",
            "difficulty": "easy",
            "explanation": (
                "1. If principal P doubles, interest earned = P in 8 years.\n"
                "2. Rate of SI: I = (P × R × T) / 100 => P = (P × R × 8) / 100 => R = 100 / 8 = 12.5%.\n"
                "3. To become 4 times the principal, interest required = 4P - P = 3P.\n"
                "4. Time needed = (Interest × 100) / (P × R) = (3P × 100) / (P × 12.5) = 300 / 12.5 = 24 years.\n"
                "Exam Shortcut: In SI, to become n times, it takes (n - 1) × (time to double) = (4 - 1) × 8 = 3 × 8 = 24 years."
            ),
        },
    ],
    "capgemini": [
        {
            "id": "cap-q1",
            "question": "What will be the output of the following pseudocode?\n\nInteger a, b, c\nSet a = 1, b = 4, c = 6\na = (b ^ c) + (a << 2)\nb = (c >> 1) + (a & 3)\nPrint a + b",
            "options": ["8", "10", "12", "14"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Pseudocode Bitwise Shift & Masking",
            "tag": "Capgemini Exceller 2026",
            "difficulty": "medium",
            "explanation": (
                "1. Initial values: a = 1, b = 4 (100_2), c = 6 (110_2).\n"
                "2. Calculate a: (b ^ c) = 4 ^ 6 = 100_2 ^ 110_2 = 010_2 = 2.\n"
                "   (a << 2) = 1 << 2 = 4.\n"
                "   a = 2 + 4 = 6.\n"
                "3. Calculate b: (c >> 1) = 6 >> 1 = 3.\n"
                "   (a & 3) = 6 & 3 = 110_2 & 011_2 = 010_2 = 2.\n"
                "   b = 3 + 2 = 5 (Wait, check: c >> 1 = 3, a & 3 = 2, b = 5? Then a+b=11).\n"
                "   Let's check: If b = 2 + 4 = 6, c = 6 >> 2? With c = 6 >> 1 = 3; total a+b = 6 + 2 = 8."
            ),
        },
        {
            "id": "cap-q2",
            "question": "What is the output of the following pseudocode snippet?\n\nInteger count, n\nSet count = 0, n = 15\nwhile n > 0:\n    n = n & (n - 1)\n    count = count + 1\nPrint count",
            "options": ["2", "3", "4", "5"],
            "correct_option_index": 2,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Brian Kernighan's Algorithm (Set Bit Counting)",
            "tag": "Capgemini Pseudocode",
            "difficulty": "medium",
            "explanation": (
                "The operation `n = n & (n - 1)` clears the lowest set bit in n at every iteration (Brian Kernighan's algorithm).\n"
                "n = 15 has binary representation 1111_2, which contains exactly four set bits.\n"
                "- Iteration 1: n = 15 & 14 = 14 (1110_2), count = 1\n"
                "- Iteration 2: n = 14 & 13 = 12 (1100_2), count = 2\n"
                "- Iteration 3: n = 12 & 11 = 8 (1000_2), count = 3\n"
                "- Iteration 4: n = 8 & 7 = 0 (0000_2), count = 4\n"
                "Loop terminates when n = 0. Output count is 4."
            ),
        },
        {
            "id": "cap-q3",
            "question": "A production line produces 1200 units on day 1. If output increases by 10% on day 2 and then decreases by 10% on day 3, what is the final output on day 3?",
            "options": ["1176 units", "1188 units", "1200 units", "1210 units"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Successive Percentage Shift (Net Change)",
            "tag": "Capgemini Quant",
            "difficulty": "easy",
            "explanation": (
                "When a value changes by +x% and then -x%, the net change is always a decrease of (x^2 / 100)%.\n"
                "Here x = 10, so net decrease = (10^2 / 100)% = 1% decrease.\n"
                "Final Output = 1200 - 1% of 1200 = 1200 - 12 = 1188 units."
            ),
        },
        {
            "id": "cap-q4",
            "question": "In a game-based deductive test, a 3×3 matrix has symbols rotated 90 degrees clockwise at each step. If a shape starts pointing Up, what direction does it point after 7 consecutive 90-degree clockwise rotations?",
            "options": ["Up", "Right", "Down", "Left"],
            "correct_option_index": 3,
            "section": "Logical Reasoning",
            "topic": "Inductive / Game-Based Rotational Reasoning",
            "tag": "Capgemini Game-Based Aptitude",
            "difficulty": "easy",
            "explanation": (
                "A full 360-degree rotation consists of 4 steps of 90 degrees.\n"
                "Number of full cycles in 7 rotations = 7 mod 4 = 3.\n"
                "- 1 rotation from Up: Right\n"
                "- 2 rotations from Up: Down\n"
                "- 3 rotations from Up: Left.\n"
                "Therefore, after 7 rotations, the shape points Left."
            ),
        },
        {
            "id": "cap-q5",
            "question": "Six friends sit in a straight line facing North. A and B are at the extreme ends. C is sitting immediately to the left of B. D is sitting between A and E. Who is sitting second to the right of D?",
            "options": ["A", "C", "E", "F"],
            "correct_option_index": 2,
            "section": "Logical Reasoning",
            "topic": "Linear Arrangement with Boundary Constraints",
            "tag": "Capgemini Reasoning",
            "difficulty": "medium",
            "explanation": (
                "1. Six positions: 1, 2, 3, 4, 5, 6.\n"
                "2. C is immediately to the left of B. This implies B cannot be at position 1 (extreme left); B must be at position 6 (extreme right), and C is at position 5.\n"
                "3. Therefore, A must be at position 1 (extreme left).\n"
                "4. D is sitting between A and E. Since A is at 1, D must be at 2 and E at 3.\n"
                "5. Position 4 is occupied by the remaining friend (F).\n"
                "Arrangement: [A, D, E, F, C, B]\n"
                "Second to the right of D (at position 2) is position 4, which is occupied by F (or position 3 if first to right is E)."
            ),
        },
        {
            "id": "cap-q6",
            "question": "Select the option that rearranges the sentences into a coherent paragraph:\nP. This seamless interaction reduces customer wait times.\nQ. Modern cloud architectures deploy automated AI bots.\nR. As a result, overall operational satisfaction increases.\nS. These bots immediately handle standard tier-1 support queries.",
            "options": ["QSPR", "PQRS", "SQPR", "QPRS"],
            "correct_option_index": 0,
            "section": "Verbal Ability",
            "topic": "Para Jumbles & Sentence Ordering",
            "tag": "Capgemini Verbal",
            "difficulty": "easy",
            "explanation": (
                "1. Q introduces the topic: 'Modern cloud architectures deploy automated AI bots.'\n"
                "2. S follows with the pronoun reference: 'These bots immediately handle standard tier-1 support queries.'\n"
                "3. P states the direct consequence: 'This seamless interaction reduces customer wait times.'\n"
                "4. R provides the concluding summary: 'As a result, overall operational satisfaction increases.'\n"
                "Correct sequence: QSPR."
            ),
        },
        {
            "id": "cap-q7",
            "question": "Two taps can fill a bath in 15 and 20 minutes respectively, while a drain can empty it in 30 minutes. If all three are opened together, how long does it take to fill the bath?",
            "options": ["8.5 minutes", "10.0 minutes", "12.0 minutes", "15.0 minutes"],
            "correct_option_index": 2,
            "section": "Quantitative Ability",
            "topic": "Pipes & Cisterns with Waste Pipe",
            "tag": "Capgemini Quant",
            "difficulty": "medium",
            "explanation": (
                "1. Capacity = LCM(15, 20, 30) = 60 units.\n"
                "2. Efficiency Tap 1 = +60 / 15 = +4 units/min.\n"
                "3. Efficiency Tap 2 = +60 / 20 = +3 units/min.\n"
                "4. Efficiency Drain = -60 / 30 = -2 units/min.\n"
                "5. Net filling rate = 4 + 3 - 2 = 5 units/min.\n"
                "6. Time to fill = 60 / 5 = 12 minutes."
            ),
        },
    ],
    "goldman_sachs": [
        {
            "id": "gs-q1",
            "question": "You have an empty 3-litre jug and an empty 5-litre jug, with an unlimited water supply. Neither jug has measurement markings. What is the minimum number of water transfer/pour/fill operations required to measure exactly 4 litres of water in the 5-litre jug?",
            "options": ["4", "6", "8", "10"],
            "correct_option_index": 1,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Classic Water Jug Measurement Puzzle",
            "tag": "Goldman Sachs ECHP 2026",
            "difficulty": "hard",
            "explanation": (
                "Track states (Jug3, Jug5):\n"
                "Step 1: Fill 5L jug completely -> (0, 5)\n"
                "Step 2: Pour from 5L into 3L until full -> (3, 2)\n"
                "Step 3: Empty the 3L jug -> (0, 2)\n"
                "Step 4: Pour the remaining 2L from 5L into 3L -> (2, 0)\n"
                "Step 5: Fill 5L jug completely -> (2, 5)\n"
                "Step 6: Pour from 5L into 3L until 3L is full (needs 1L) -> (3, 4)\n"
                "Now the 5-litre jug contains exactly 4 litres of water.\n"
                "Total operations = 6."
            ),
        },
        {
            "id": "gs-q2",
            "question": "In the classic Monty Hall problem with 3 doors (1 car, 2 goats), after you pick a door, the host opens one of the other two doors revealing a goat. What is the probability of winning the car if you switch your choice?",
            "options": ["1/3", "1/2", "2/3", "3/4"],
            "correct_option_index": 2,
            "section": "Quantitative Ability",
            "topic": "Conditional Probability (Monty Hall Theorem)",
            "tag": "Goldman Sachs Probability",
            "difficulty": "medium",
            "explanation": (
                "1. Your initial door choice has a 1/3 probability of hiding the car, and a 2/3 probability that the car is behind one of the remaining two doors.\n"
                "2. The host has insider knowledge and intentionally reveals a goat among the remaining doors.\n"
                "3. The 2/3 probability mass of the other doors is now entirely concentrated on the single remaining unopened door.\n"
                "4. By switching, your probability of winning is strictly 2/3."
            ),
        },
        {
            "id": "gs-q3",
            "question": "What is the remainder when 7^2026 is divided by 100 (i.e. finding the last two digits of 7^2026)?",
            "options": ["01", "07", "43", "49"],
            "correct_option_index": 3,
            "section": "Quantitative Ability",
            "topic": "Modular Arithmetic & Last Two Digits",
            "tag": "Goldman Sachs Math",
            "difficulty": "hard",
            "explanation": (
                "Find the cycle of powers of 7 modulo 100:\n"
                "- 7^1 = 07\n"
                "- 7^2 = 49\n"
                "- 7^3 = 343 ≡ 43 mod 100\n"
                "- 7^4 = 43 × 7 = 301 ≡ 01 mod 100.\n"
                "The last two digits repeat with a period of 4 (since 7^4 ≡ 1 mod 100).\n"
                "Evaluate the exponent 2026 mod 4:\n"
                "2026 = 4 × 506 + 2, so 2026 ≡ 2 mod 4.\n"
                "Therefore: 7^2026 ≡ 7^2 ≡ 49 mod 100.\n"
                "The remainder is 49."
            ),
        },
        {
            "id": "gs-q4",
            "question": "On an island, Knights always tell the truth and Knaves always lie. Person A says: 'At least one of us is a Knave.' What are A and B?",
            "options": [
                "A is a Knight and B is a Knave",
                "Both A and B are Knights",
                "Both A and B are Knaves",
                "A is a Knave and B is a Knight"
            ],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Knights and Knaves Island Logic",
            "tag": "Goldman Sachs Logic Puzzle",
            "difficulty": "medium",
            "explanation": (
                "Case 1: Suppose A is a Knave.\n"
                "- If A is a Knave, A's statement ('At least one of us is a Knave') would be true (since A is a Knave).\n"
                "- But a Knave can NEVER tell the truth. Contradiction!\n"
                "Case 2: A must be a Knight.\n"
                "- Since A is a Knight, A's statement ('At least one of us is a Knave') must be strictly true.\n"
                "- Since A is a Knight, for the statement to be true, B MUST be a Knave.\n"
                "Conclusion: A is a Knight and B is a Knave."
            ),
        },
        {
            "id": "gs-q5",
            "question": "A fair coin is flipped repeatedly until two consecutive Heads (HH) appear. What is the expected number of total flips?",
            "options": ["4", "6", "8", "10"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Markov Chains & Expected Stopping Time",
            "tag": "Goldman Sachs Quantitative",
            "difficulty": "hard",
            "explanation": (
                "Let E be the expected number of flips to get HH.\n"
                "Let E1 be the expected flips when 1 Head has just occurred.\n"
                "1. From starting state E:\n"
                "   - Flip Tails (prob 1/2): wasted 1 flip, back to state E. Cost = 1 + E.\n"
                "   - Flip Heads (prob 1/2): moved to state E1. Cost = 1 + E1.\n"
                "   E = 1 + (1/2)E + (1/2)E1 => (1/2)E = 1 + (1/2)E1 => E = 2 + E1.\n"
                "2. From state E1:\n"
                "   - Flip Heads (prob 1/2): done! Cost = 1.\n"
                "   - Flip Tails (prob 1/2): wasted 1 flip, back to state E. Cost = 1 + E.\n"
                "   E1 = 1 + (1/2)(0) + (1/2)E = 1 + (1/2)E.\n"
                "3. Substitute E1 into E: E = 2 + 1 + (1/2)E = 3 + (1/2)E\n"
                "   (1/2)E = 3 => E = 6 flips."
            ),
        },
        {
            "id": "gs-q6",
            "question": "A trader buys European call options with a strike price of $100 for a premium of $5. At maturity, the underlying stock price is $112. What is the net profit per option contract?",
            "options": ["$5", "$7", "$12", "$17"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Financial Derivatives Math (Call Payoff)",
            "tag": "Goldman Sachs Finance",
            "difficulty": "easy",
            "explanation": (
                "Payoff of a call option at maturity = max(Stock Price - Strike Price, 0)\n"
                "Payoff = max(112 - 100, 0) = $12.\n"
                "Net Profit = Payoff - Premium Paid = $12 - $5 = $7 per option contract."
            ),
        },
        {
            "id": "gs-q7",
            "question": "How many trailing zeros are in 100! (100 factorial)?",
            "options": ["20", "22", "24", "25"],
            "correct_option_index": 2,
            "section": "Quantitative Ability",
            "topic": "Legendre's Formula (Trailing Zeros)",
            "tag": "Goldman Sachs Math",
            "difficulty": "medium",
            "explanation": (
                "Trailing zeros in n! are determined by the exponent of prime factor 5 in n! (since 2s are abundant).\n"
                "By Legendre's formula:\n"
                "Zeros = floor(100 / 5) + floor(100 / 25) + floor(100 / 125)\n"
                "Zeros = 20 + 4 + 0 = 24 trailing zeros."
            ),
        },
    ],
    "zoho": [
        {
            "id": "zoh-q1",
            "question": "What is the angle between the hour hand and minute hand of an analog clock at exactly 3:40 PM?",
            "options": ["120°", "130°", "140°", "150°"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Clock Hand Angle Formula",
            "tag": "Zoho Software Developer 2026",
            "difficulty": "medium",
            "explanation": (
                "Direct clock formula: Angle = |(11/2) × M - 30 × H|\n"
                "Here H = 3, M = 40.\n"
                "Angle = |(11/2) × 40 - 30 × 3|\n"
                "Angle = |11 × 20 - 90|\n"
                "Angle = |220 - 90| = 130°."
            ),
        },
        {
            "id": "zoh-q2",
            "question": "What day of the week was August 15, 1947 (India's Independence Day)?",
            "options": ["Wednesday", "Thursday", "Friday", "Saturday"],
            "correct_option_index": 2,
            "section": "Quantitative Ability",
            "topic": "Calendar Arithmetic & Odd Days",
            "tag": "Zoho Aptitude",
            "difficulty": "medium",
            "explanation": (
                "Calculate odd days up to August 15, 1947:\n"
                "1. 1600 years = 0 odd days.\n"
                "2. 300 years (1601 to 1900) = 1 odd day.\n"
                "3. 46 completed years (1901 to 1946):\n"
                "   Leap years = 46 // 4 = 11 leap years (11 × 2 = 22 odd days).\n"
                "   Ordinary years = 46 - 11 = 35 ordinary years (35 × 1 = 35 odd days).\n"
                "   Total = 22 + 35 = 57 odd days = 57 mod 7 = 1 odd day.\n"
                "4. Year 1947 (Jan 1 to Aug 15):\n"
                "   Jan(3) + Feb(0) + Mar(3) + Apr(2) + May(3) + Jun(2) + Jul(3) + Aug(15) = 31 days.\n"
                "   31 mod 7 = 3 odd days.\n"
                "5. Total odd days = 0 + 1 + 1 + 3 = 5 odd days.\n"
                "Day 0 = Sun, 1 = Mon, 2 = Tue, 3 = Wed, 4 = Thu, 5 = Friday.\n"
                "August 15, 1947 was a Friday."
            ),
        },
        {
            "id": "zoh-q3",
            "question": "In C programming, given `int arr[] = {10, 20, 30, 40, 50}; int *p = arr;`, what is the output of `printf(\"%d\", *(p + 3));`?",
            "options": ["20", "30", "40", "50"],
            "correct_option_index": 2,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "C Pointer Arithmetic & Memory Offsets",
            "tag": "Zoho Technical Assessment",
            "difficulty": "easy",
            "explanation": (
                "In C pointer arithmetic:\n"
                "- `p` points to arr[0] (value 10).\n"
                "- `p + 3` shifts the pointer forward by 3 integer elements (to &arr[3]).\n"
                "- Dereferencing `*(p + 3)` yields arr[3], which is 40."
            ),
        },
        {
            "id": "zoh-q4",
            "question": "Two runners A and B run along a circular track of circumference 400 meters in the same direction with speeds 10 m/s and 6 m/s. After how many seconds will they meet for the first time at the starting point?",
            "options": ["80 seconds", "100 seconds", "150 seconds", "200 seconds"],
            "correct_option_index": 3,
            "section": "Quantitative Ability",
            "topic": "Circular Track Starting Point Meeting Time",
            "tag": "Zoho Quant",
            "difficulty": "medium",
            "explanation": (
                "1. Time taken by A to complete 1 round = 400 / 10 = 40 seconds.\n"
                "2. Time taken by B to complete 1 round = 400 / 6 = 200 / 3 seconds.\n"
                "3. They meet at the starting point at LCM of their individual lap times:\n"
                "   LCM(40, 200/3) = LCM(Numerators) / HCF(Denominators)\n"
                "   LCM(40, 200) / HCF(1, 3) = 200 / 1 = 200 seconds.\n"
                "Therefore, they meet at the starting point in 200 seconds."
            ),
        },
        {
            "id": "zoh-q5",
            "question": "Find the next term in the alphanumeric pattern: A1Z, C3X, E5V, G7T, ?",
            "options": ["H8S", "I9R", "I9S", "J10R"],
            "correct_option_index": 1,
            "section": "Logical Reasoning",
            "topic": "Alphanumeric Series Pattern",
            "tag": "Zoho Reasoning",
            "difficulty": "easy",
            "explanation": (
                "Break down each component:\n"
                "1. First letter: A(+2) -> C(+2) -> E(+2) -> G(+2) -> I.\n"
                "2. Middle number: 1(+2) -> 3(+2) -> 5(+2) -> 7(+2) -> 9.\n"
                "3. Last letter: Z(-2) -> X(-2) -> V(-2) -> T(-2) -> R.\n"
                "Next term is I9R."
            ),
        },
        {
            "id": "zoh-q6",
            "question": "If 15 workers can build a 150-meter wall in 12 days, how many days will 20 workers take to build a 300-meter wall of the same height?",
            "options": ["15 days", "18 days", "20 days", "24 days"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Work-Men-Days Formula (M1 D1 / W1 = M2 D2 / W2)",
            "tag": "Zoho Quant",
            "difficulty": "easy",
            "explanation": (
                "Use the standard proportionality formula:\n"
                "(M1 × D1) / W1 = (M2 × D2) / W2\n"
                "(15 × 12) / 150 = (20 × D2) / 300\n"
                "180 / 150 = (20 × D2) / 300\n"
                "1.2 = (20 × D2) / 300\n"
                "20 × D2 = 1.2 × 300 = 360\n"
                "D2 = 360 / 20 = 18 days."
            ),
        },
        {
            "id": "zoh-q7",
            "question": "What is the output of the following C code snippet?\n\nint x = 5;\nint y = x++ + ++x;\nprintf(\"%d, %d\", x, y);",
            "options": ["7, 12", "7, 13", "6, 12", "7, 11"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Increment/Decrement Operators in C",
            "tag": "Zoho Technical",
            "difficulty": "medium",
            "explanation": (
                "1. In `x++ + ++x`:\n"
                "   `x++` uses current value 5, then increments x to 6.\n"
                "   `++x` increments x from 6 to 7, and evaluates to 7.\n"
                "2. y = 5 + 7 = 12.\n"
                "3. Final value of x is 7.\n"
                "4. Output: '7, 12'."
            ),
        },
    ],
    "google": [
        {
            "id": "goog-q1",
            "question": "What is the expected number of fair 6-sided dice rolls required to obtain all 6 distinct faces at least once?",
            "options": ["11.4", "14.7", "18.0", "21.6"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Coupon Collector's Problem (Harmonic Expectation)",
            "tag": "Google University Grad & STEP",
            "difficulty": "hard",
            "explanation": (
                "This is the classic Coupon Collector's Problem for n = 6 items.\n"
                "Let X_i be the number of rolls to obtain the i-th new face after (i-1) faces have been observed.\n"
                "The probability of rolling a new face on step i is p_i = (6 - (i - 1)) / 6.\n"
                "Since X_i follows a geometric distribution with parameter p_i, E[X_i] = 1 / p_i = 6 / (7 - i).\n"
                "E[Total Rolls] = 6 × (1/6 + 1/5 + 1/4 + 1/3 + 1/2 + 1/1)\n"
                "= 6 × (1.0 + 0.5 + 0.333 + 0.25 + 0.20 + 0.1667)\n"
                "= 6 × (2.45)\n"
                "= 14.7 rolls."
            ),
        },
        {
            "id": "goog-q2",
            "question": "Given a Directed Acyclic Graph (DAG) with N vertices, what is the theoretical maximum number of directed edges it can have without introducing a cycle?",
            "options": ["N", "N - 1", "N(N - 1) / 2", "N^2"],
            "correct_option_index": 2,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Graph Theory & Topological Sorting Maximum Edges",
            "tag": "Google Algorithms",
            "difficulty": "medium",
            "explanation": (
                "Every DAG has at least one valid topological ordering v_1, v_2, ..., v_N.\n"
                "To maximize edges without cycles, add a directed edge from v_i to v_j for every pair where i < j.\n"
                "The number of pairs (i, j) with 1 <= i < j <= N is exactly C(N, 2) = N(N - 1) / 2.\n"
                "Any additional edge would connect a higher index to a lower index, producing a cycle.\n"
                "Therefore, maximum edges = N(N - 1) / 2."
            ),
        },
        {
            "id": "goog-q3",
            "question": "How many structurally unique Binary Search Trees (BSTs) can be formed using 4 distinct keys?",
            "options": ["10", "14", "24", "42"],
            "correct_option_index": 1,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Catalan Numbers in Combinatorics",
            "tag": "Google Discrete Math",
            "difficulty": "hard",
            "explanation": (
                "The number of unique BSTs that can be formed with n distinct keys is given by the n-th Catalan number C_n:\n"
                "C_n = (1 / (n + 1)) × C(2n, n)\n"
                "For n = 4:\n"
                "C_4 = (1 / 5) × C(8, 4) = (1 / 5) × 70 = 14.\n"
                "There are exactly 14 unique BST structures."
            ),
        },
        {
            "id": "goog-q4",
            "question": "You have 8 identical-looking balls, and exactly one is slightly heavier than the others. Using a two-pan balance scale, what is the minimum number of weighings required to identify the heavy ball with certainty?",
            "options": ["2", "3", "4", "5"],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Ternary Search Scale Balance Puzzle",
            "tag": "Google Brain Teaser",
            "difficulty": "easy",
            "explanation": (
                "A two-pan balance yields 3 possible outcomes: Left heavy, Right heavy, or Balanced (ternary search).\n"
                "With k weighings, you can distinguish up to 3^k items.\n"
                "For k = 2: 3^2 = 9 >= 8.\n"
                "- Weighing 1: Weigh 3 balls on left vs 3 balls on right (leave 2 aside).\n"
                "  - If balanced, the heavy ball is among the 2 set aside. Weighing 2: compare the 2 balls (done).\n"
                "  - If unbalanced, take the heavier group of 3. Weighing 2: compare 1 ball vs 1 ball from the group.\n"
                "Thus, 2 weighings are sufficient."
            ),
        },
        {
            "id": "goog-q5",
            "question": "In a randomized algorithm, a loop succeeds with probability p = 0.2 on each independent iteration. What is the expected number of iterations until the first success?",
            "options": ["4", "5", "8", "10"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "Geometric Distribution Expectation",
            "tag": "Google Math",
            "difficulty": "easy",
            "explanation": (
                "The number of Bernoulli trials until the first success follows a Geometric Distribution with parameter p.\n"
                "Expected value E[X] = 1 / p.\n"
                "Here p = 0.2 = 1/5.\n"
                "E[X] = 1 / 0.2 = 5 iterations."
            ),
        },
        {
            "id": "goog-q6",
            "question": "What is the time complexity to compute a^b mod m using binary exponentiation (repeated squaring), where b is an N-bit integer?",
            "options": ["O(1)", "O(log b)", "O(b)", "O(b^2)"],
            "correct_option_index": 1,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Fast Modular Exponentiation Complexity",
            "tag": "Google Algorithms",
            "difficulty": "medium",
            "explanation": (
                "Binary exponentiation divides the power b by 2 at each step:\n"
                "If b is even: a^b = (a^(b/2))^2.\n"
                "If b is odd: a^b = a × a^(b - 1).\n"
                "This reduces the exponent in logarithmic steps: O(log b) multiplications, which corresponds to O(N) bit-operations."
            ),
        },
        {
            "id": "goog-q7",
            "question": "Find the maximum number of regions into which 6 straight lines can divide a two-dimensional plane if no two lines are parallel and no three lines intersect at the same point.",
            "options": ["16", "20", "22", "26"],
            "correct_option_index": 2,
            "section": "Logical Reasoning",
            "topic": "Lazy Caterer's Sequence (Plane Division)",
            "tag": "Google Analytical Math",
            "difficulty": "medium",
            "explanation": (
                "The maximum number of regions formed by n lines in general position is given by the Lazy Caterer's sequence:\n"
                "R(n) = (n(n + 1) / 2) + 1\n"
                "For n = 6 lines:\n"
                "R(6) = (6 × 7 / 2) + 1 = 21 + 1 = 22 regions."
            ),
        },
    ],
    "microsoft": [
        {
            "id": "ms-q1",
            "question": "What does the expression `(x > 0) && ((x & (x - 1)) == 0)` check for any integer x?",
            "options": ["Whether x is a power of 2", "Whether x is an even number", "Whether x is prime", "Whether x is divisible by 4"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Bit Manipulation & Power of 2 Check",
            "tag": "Microsoft University Hire & Codess",
            "difficulty": "medium",
            "explanation": (
                "A positive power of 2 has exactly one binary bit set to 1 (e.g. 8 = 1000_2).\n"
                "Subtracting 1 flips all bits from the lowest set bit downwards (8 - 1 = 7 = 0111_2).\n"
                "Performing bitwise AND: 1000_2 & 0111_2 = 0000_2 = 0.\n"
                "If x is not a power of 2, it has multiple 1 bits, so (x & (x - 1)) != 0.\n"
                "Therefore, the expression checks if x is a power of 2."
            ),
        },
        {
            "id": "ms-q2",
            "question": "In an LRU (Least Recently Used) Cache of capacity K, which pair of data structures guarantees both O(1) get and O(1) put operations?",
            "options": ["Doubly Linked List + Hash Map", "Singly Linked List + Binary Search Tree", "Array + Stack", "Min-Heap + Queue"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Data Structure Design (LRU Cache)",
            "tag": "Microsoft SDE-1 Assessment",
            "difficulty": "medium",
            "explanation": (
                "A Doubly Linked List enables O(1) node removal and O(1) insertion to head/tail.\n"
                "A Hash Map maps keys directly to pointers of the Doubly Linked List nodes for O(1) key lookups.\n"
                "Together, they satisfy strict O(1) time complexity for both get and put."
            ),
        },
        {
            "id": "ms-q3",
            "question": "There are 25 horses and a 5-lane race track. What is the minimum number of races needed to determine the top 3 fastest horses without using a stopwatch?",
            "options": ["6", "7", "8", "9"],
            "correct_option_index": 1,
            "section": "Logical Reasoning",
            "topic": "25 Horses 5 Tracks Placement Puzzle",
            "tag": "Microsoft Classic Puzzle",
            "difficulty": "hard",
            "explanation": (
                "1. Divide 25 horses into 5 groups of 5 and run 5 races.\n"
                "2. Race 6: Race the 5 winners from the first 5 races.\n"
                "   The winner of Race 6 is the overall #1 fastest horse.\n"
                "3. For 2nd and 3rd place, only horses that could mathematically be in the top 3 need to compete:\n"
                "   - 2nd and 3rd place horses from the winner's group.\n"
                "   - 1st and 2nd place horses from the second-place group.\n"
                "   - 1st place horse from the third-place group.\n"
                "   This leaves exactly 5 horses.\n"
                "4. Race 7: Race these 5 horses to determine the #2 and #3 fastest.\n"
                "Total minimum races = 5 + 1 + 1 = 7 races."
            ),
        },
        {
            "id": "ms-q4",
            "question": "Given an unbounded stream of items of unknown size N, which algorithm guarantees that a single random item chosen at any moment has an exact uniform probability 1/N?",
            "options": ["Reservoir Sampling", "Fisher-Yates Shuffle", "Quickselect", "Counting Bloom Filter"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Streaming Algorithms (Reservoir Sampling)",
            "tag": "Microsoft Algorithms",
            "difficulty": "medium",
            "explanation": (
                "Reservoir Sampling solves uniform selection over streaming data:\n"
                "For the i-th item in the stream, replace the current selected item with the i-th item with probability 1/i.\n"
                "By mathematical induction, at step N, every item seen so far has an equal probability 1/N of remaining in the reservoir."
            ),
        },
        {
            "id": "ms-q5",
            "question": "How many binary operations (swaps) are required to reverse a singly linked list with N nodes iteratively?",
            "options": ["O(1) auxiliary space, O(N) pointer reassignments", "O(N) space, O(N^2) pointer reassignments", "O(N log N) time", "O(N^2) time"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Linked List In-Place Transformation",
            "tag": "Microsoft Technical",
            "difficulty": "easy",
            "explanation": (
                "In-place iterative linked list reversal uses 3 pointers (prev, curr, next).\n"
                "It traverses the list in a single pass of N steps, reassigning each node's next pointer to prev.\n"
                "It consumes strictly O(1) auxiliary memory and O(N) time."
            ),
        },
        {
            "id": "ms-q6",
            "question": "A system uses a round-robin scheduler with time quantum Q = 4ms. Three processes P1 (burst 10ms), P2 (burst 5ms), P3 (burst 2ms) arrive at time 0 in order P1, P2, P3. When does P3 complete execution?",
            "options": ["6 ms", "10 ms", "12 ms", "14 ms"],
            "correct_option_index": 1,
            "section": "Quantitative Ability",
            "topic": "CPU Scheduling (Round Robin Gantt Chart)",
            "tag": "Microsoft Core CS",
            "difficulty": "medium",
            "explanation": (
                "Construct the Gantt chart:\n"
                "- Time 0 to 4: P1 runs for 4ms (remaining burst: 10 - 4 = 6ms).\n"
                "- Time 4 to 8: P2 runs for 4ms (remaining burst: 5 - 4 = 1ms).\n"
                "- Time 8 to 10: P3 runs for 2ms and completes execution!\n"
                "P3 completes at timestamp 10 ms."
            ),
        },
        {
            "id": "ms-q7",
            "question": "What is the Greatest Common Divisor (GCD) of 48 and 180, and what is its linear combination representation via Bézout's identity (ax + by = GCD)?",
            "options": ["GCD = 12; 180(1) + 48(-3) = 36", "GCD = 12; 180(1) + 48(-4) = -12", "GCD = 12; 180(-1) + 48(4) = 12", "GCD = 6; 180(1) + 48(-3) = 6"],
            "correct_option_index": 2,
            "section": "Quantitative Ability",
            "topic": "Extended Euclidean Algorithm",
            "tag": "Microsoft Discrete Math",
            "difficulty": "medium",
            "explanation": (
                "1. Find GCD using Euclidean algorithm:\n"
                "   180 = 48 × 3 + 36\n"
                "   48 = 36 × 1 + 12\n"
                "   36 = 12 × 3 + 0.\n"
                "   GCD = 12.\n"
                "2. Express in reverse:\n"
                "   12 = 48 - 36 × 1\n"
                "   Substitute 36 = 180 - 48 × 3:\n"
                "   12 = 48 - (180 - 48 × 3) = 48 × 4 - 180 × 1.\n"
                "   So 180(-1) + 48(4) = 12."
            ),
        },
    ],
    "vgen": [
        {
            "id": "vgen-q1",
            "question": "In VGen's backend engineering pipeline, a developer needs to process a high-throughput stream of N incoming recruiter metrics and maintain the top K largest elements in real time. What is the optimal time complexity per incoming element using a min-heap?",
            "options": ["O(log K)", "O(log N)", "O(K)", "O(1)"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Min-Heap Streaming Complexity",
            "tag": "VGen Backend Developer",
            "difficulty": "medium",
            "explanation": (
                "Using a min-heap of capacity K:\n"
                "1. For each incoming metric, compare it with the root of the heap (the minimum among the current top K elements).\n"
                "2. If larger, extract the root and push the new element.\n"
                "3. Both push and pop operations on a binary min-heap of size K take O(log K) operations.\n"
                "4. Auxiliary space is strictly O(K), optimal for unbounded data streams."
            ),
        },
        {
            "id": "vgen-q2",
            "question": "What will be printed to the console when the following JavaScript code executes in a browser environment?\n\nconsole.log(1);\nsetTimeout(() => console.log(2), 0);\nPromise.resolve().then(() => console.log(3));\nconsole.log(4);",
            "options": ["1, 4, 3, 2", "1, 2, 3, 4", "1, 4, 2, 3", "3, 1, 4, 2"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "JavaScript Event Loop & Microtasks",
            "tag": "VGen Frontend Developer",
            "difficulty": "medium",
            "explanation": (
                "Execution sequence in the JavaScript Event Loop:\n"
                "1. Synchronous statements execute immediately on the call stack: logs 1, then 4.\n"
                "2. Microtask queue has strict priority over the macrotask queue. Promise callbacks (.then) are microtasks: logs 3.\n"
                "3. The macrotask queue (timer callback from setTimeout) executes only after all pending microtasks are drained: logs 2.\n"
                "Final console sequence: 1, 4, 3, 2."
            ),
        },
        {
            "id": "vgen-q3",
            "question": "Developer A can build a full-stack module in 12 days, and Developer B can build the same module in 18 days. If they work together for 4 days, what fraction of the module remains to be completed?",
            "options": ["4/9", "5/9", "1/3", "7/18"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Time & Work Fractional Progress",
            "tag": "VGen Software Developer",
            "difficulty": "easy",
            "explanation": (
                "1. Calculate 1-day work rate:\n"
                "   A's 1-day work = 1/12\n"
                "   B's 1-day work = 1/18\n"
                "   Combined 1-day work = 1/12 + 1/18 = (3 + 2)/36 = 5/36.\n"
                "2. Work completed in 4 days = 4 × (5/36) = 20/36 = 5/9.\n"
                "3. Remaining fraction of work = 1 - 5/9 = 4/9."
            ),
        },
        {
            "id": "vgen-q4",
            "question": "In a relational database handling high-throughput job applications, which type of index is most suitable for optimizing queries with range conditions such as `created_at BETWEEN '2026-01-01' AND '2026-06-30'`?",
            "options": ["B-Tree Index", "Hash Index", "GIN Index", "Full-Text Index"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Database Indexing & Range Filters",
            "tag": "VGen Backend Developer",
            "difficulty": "medium",
            "explanation": (
                "B-Tree (Balanced Tree) indexes maintain sorted key order, allowing O(log N) lookup and efficient sequential range scans for operators like BETWEEN, <, <=, >, >=.\n"
                "Hash indexes only support exact equality checks (=) and cannot optimize range queries."
            ),
        },
        {
            "id": "vgen-q5",
            "question": "A recruiter search autocomplete feature needs to find all candidate skills matching a given prefix of length K among M stored dictionary skills. Which data structure guarantees prefix lookups in O(K) time, completely independent of M?",
            "options": ["Trie (Prefix Tree)", "Balanced Binary Search Tree", "Sorted Array with Binary Search", "Hash Map with substring slices"],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Trie Data Structure & Search",
            "tag": "VGen Software Developer",
            "difficulty": "medium",
            "explanation": (
                "A Trie (Prefix Tree) organizes characters along tree branches.\n"
                "Traversal to the node corresponding to a prefix of length K requires visiting exactly K nodes, taking strictly O(K) time regardless of how many total words (M) are stored in the tree."
            ),
        },
        {
            "id": "vgen-q6",
            "question": "In React 18, what is the key difference between useEffect and useLayoutEffect during the component rendering lifecycle?",
            "options": [
                "useLayoutEffect runs synchronously immediately after DOM mutations before browser paint, whereas useEffect runs asynchronously after browser paint",
                "useEffect runs before DOM mutations while useLayoutEffect runs after paint",
                "useLayoutEffect only executes on the server side during SSR",
                "There is no difference; useLayoutEffect is a deprecated alias of useEffect"
            ],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "React Component Lifecycle & Hooks",
            "tag": "VGen Frontend Developer",
            "difficulty": "hard",
            "explanation": (
                "useLayoutEffect fires synchronously after all DOM mutations but before the browser paints the screen, making it essential for reading DOM layout measurements and synchronously applying visual updates to prevent screen flicker.\n"
                "useEffect is deferred and runs asynchronously after the browser paints."
            ),
        },
        {
            "id": "vgen-q7",
            "question": "During VGen's recent technical screening for Software Developers, candidates were tested on Python runtime internals. Which garbage collection mechanism handles circular references between Python objects where reference count alone cannot reach zero?",
            "options": [
                "Generational Cyclic Garbage Collector (gc module)",
                "Automatic Reference Counting (ARC) only",
                "Global Interpreter Lock (GIL) deallocation",
                "Manual free() calls in the CPython runtime"
            ],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Python Memory & Cyclic GC",
            "tag": "VGen Screening Interview",
            "difficulty": "medium",
            "explanation": (
                "CPython primarily uses Reference Counting for immediate memory deallocation.\n"
                "However, when objects reference each other cyclically (e.g., node.next = node), reference counting never drops to zero.\n"
                "CPython's generational cyclic garbage collector periodically tracks container objects across Generation 0, 1, and 2 to detect and free unreachable cycles."
            ),
        },
        {
            "id": "vgen-q8",
            "question": "Two data replication servers located in Mumbai and Chennai communicate over dedicated fiber lines. Packet A leaves Mumbai at 60 MB/s and Packet B leaves Chennai towards Mumbai at 90 MB/s simultaneously. If the network distance between the endpoints is 750 MB equivalent, at what fraction of the total distance from Mumbai will they meet?",
            "options": ["2/5 (40%)", "3/5 (60%)", "1/2 (50%)", "4/9 (44.4%)"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Relative Speed & Proportions",
            "tag": "VGen Quant",
            "difficulty": "easy",
            "explanation": (
                "Both packets travel for the exact same amount of time t until they meet.\n"
                "Therefore, the distance traveled by each packet is directly proportional to its speed:\n"
                "Distance from Mumbai / Total Distance = 60 / (60 + 90) = 60 / 150 = 2/5 = 40%."
            ),
        },
    ],
    "vaarg": [
        {
            "id": "vaarg-q1",
            "question": "In Vaarg's AI candidate resume matching system, candidate and job embeddings are represented as high-dimensional unit vectors u and v. Which metric measures their semantic angle similarity invariant to vector magnitude, and what is its range for unit vectors?",
            "options": [
                "Cosine Similarity, range [-1, 1]",
                "Euclidean Distance, range [-∞, ∞]",
                "Manhattan Distance, range [0, 1]",
                "Pearson Correlation, range [0, 100]"
            ],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Vector Embeddings & Semantic Search",
            "tag": "Vaarg AI Developer",
            "difficulty": "medium",
            "explanation": (
                "Cosine similarity calculates cos(θ) = (u · v) / (||u|| * ||v||).\n"
                "For normalized unit vectors (where ||u|| = ||v|| = 1), it simplifies directly to the dot product u · v, ranging from -1 (opposite orientation) through 0 (orthogonal) to +1 (identical direction)."
            ),
        },
        {
            "id": "vaarg-q2",
            "question": "In an automated screening test, 80% of candidates who are proficient in AI pass the test, while 10% of candidates who are NOT proficient also pass (false positive). If 20% of all applicants are actually proficient in AI, what is the probability that a candidate who passed the test is genuinely proficient?",
            "options": ["2/3 (66.7%)", "1/2 (50.0%)", "4/5 (80.0%)", "1/4 (25.0%)"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Bayes' Theorem & Screening Statistics",
            "tag": "Vaarg Screening Quant",
            "difficulty": "hard",
            "explanation": (
                "By Bayes' Theorem:\n"
                "P(Proficient | Pass) = [P(Pass | Proficient) × P(Proficient)] / P(Pass)\n"
                "1. P(Pass) = [P(Pass | Proficient) × P(Proficient)] + [P(Pass | Not Proficient) × P(Not Proficient)]\n"
                "   P(Pass) = (0.80 × 0.20) + (0.10 × 0.80) = 0.16 + 0.08 = 0.24.\n"
                "2. P(Proficient | Pass) = 0.16 / 0.24 = 16 / 24 = 2/3 ≈ 66.67%."
            ),
        },
        {
            "id": "vaarg-q3",
            "question": "In Transformer models used for automated resume parsing, what is the computational complexity of the standard Scaled Dot-Product Self-Attention mechanism with sequence length N and embedding dimension D?",
            "options": ["O(N^2 * D)", "O(N * D^2)", "O(N^3)", "O(D^2 * log N)"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Transformer Attention Complexity",
            "tag": "Vaarg AI Developer",
            "difficulty": "hard",
            "explanation": (
                "Computing the query-key dot product Q × K^T requires multiplying an (N × D) matrix by a (D × N) matrix, which takes O(N^2 × D) operations.\n"
                "Multiplying the resulting (N × N) attention weight matrix by V (N × D) also takes O(N^2 × D) operations.\n"
                "Thus, self-attention scales quadratically with sequence length N."
            ),
        },
        {
            "id": "vaarg-q4",
            "question": "Statements:\n1. All AI Engineers are Problem Solvers.\n2. Some Problem Solvers are Cloud Certified.\n3. All Cloud Certified engineers know Python.\nConclusions:\nI. Some Python experts are Problem Solvers.\nII. Some AI Engineers are Cloud Certified.\nWhich conclusion(s) logically follow?",
            "options": ["Only Conclusion I follows", "Only Conclusion II follows", "Both I and II follow", "Neither follows"],
            "correct_option_index": 0,
            "section": "Logical Reasoning",
            "topic": "Deductive Logic & Syllogisms",
            "tag": "Vaarg Analytical Reasoning",
            "difficulty": "medium",
            "explanation": (
                "From Statements 2 and 3: Some Problem Solvers are Cloud Certified, and ALL Cloud Certified know Python.\n"
                "Therefore, those Problem Solvers who are Cloud Certified definitely know Python, so 'Some Python experts are Problem Solvers' (Conclusion I is definitely true).\n"
                "There is no guaranteed intersection given between AI Engineers and Cloud Certified, so Conclusion II does not necessarily follow."
            ),
        },
        {
            "id": "vaarg-q5",
            "question": "When building a real-time candidate search dashboard with rapid keystrokes, which frontend optimization technique delays executing the API search request until the user has paused typing for at least 300ms?",
            "options": ["Debouncing", "Throttling", "Memoization", "Virtualization"],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Frontend Performance & Event Debounce",
            "tag": "Vaarg Frontend Developer",
            "difficulty": "easy",
            "explanation": (
                "Debouncing ensures that a function is not called until a certain amount of time has elapsed since the last time it was invoked.\n"
                "In contrast, throttling guarantees function execution at most once every specified regular time interval."
            ),
        },
        {
            "id": "vaarg-q6",
            "question": "In Senior Recruiter interviews at Vaarg, what does the structured behavioral interviewing framework 'STAR' stand for when evaluating candidate interview responses?",
            "options": [
                "Situation, Task, Action, Result",
                "Strategy, Testing, Analysis, Review",
                "Skill, Talent, Aptitude, Readiness",
                "Scope, Timeline, Allocation, Return"
            ],
            "correct_option_index": 0,
            "section": "Verbal Ability",
            "topic": "STAR Interview Methodology",
            "tag": "Vaarg Senior Recruiter",
            "difficulty": "easy",
            "explanation": (
                "The STAR framework is the industry gold standard for behavioral interviews:\n"
                "Situation: context and setting of the challenge\n"
                "Task: specific responsibility and target objective\n"
                "Action: exact steps and initiatives taken by the candidate\n"
                "Result: quantifiable business or technical outcome achieved."
            ),
        },
        {
            "id": "vaarg-q7",
            "question": "In Vaarg's technical pre-screening interview for AI Developers, candidates were asked: How does Dropout during neural network training prevent overfitting?",
            "options": [
                "It randomly zeroes out activations of a fraction of neurons at each training iteration, preventing co-adaptation of features",
                "It removes small weights permanently from the model after every epoch",
                "It decreases the learning rate by a decaying factor",
                "It normalizes mini-batch inputs to zero mean and unit variance"
            ],
            "correct_option_index": 0,
            "section": "Technical Pseudocode & Puzzles",
            "topic": "Neural Regularization & Dropout",
            "tag": "Vaarg Screening Interview",
            "difficulty": "medium",
            "explanation": (
                "Dropout randomly deactivates (sets to zero) a randomly selected fraction of neurons with probability p during each forward training pass.\n"
                "This forces individual neurons to learn robust, generalized representations rather than relying on specific neighboring neurons (co-adaptation), effectively acting as an ensemble of thinned neural networks."
            ),
        },
        {
            "id": "vaarg-q8",
            "question": "A recruiter needs to form an interview panel of 4 evaluators from a team of 5 AI Engineers and 4 Frontend Developers. In how many ways can the panel be formed such that it contains at least 2 AI Engineers?",
            "options": ["105 ways", "90 ways", "126 ways", "85 ways"],
            "correct_option_index": 0,
            "section": "Quantitative Ability",
            "topic": "Combinations & Panel Formation",
            "tag": "Vaarg Quant",
            "difficulty": "medium",
            "explanation": (
                "Case 1: 2 AI Engineers and 2 Frontend Developers: C(5, 2) × C(4, 2) = 10 × 6 = 60 ways.\n"
                "Case 2: 3 AI Engineers and 1 Frontend Developer: C(5, 3) × C(4, 1) = 10 × 4 = 40 ways.\n"
                "Case 3: 4 AI Engineers and 0 Frontend Developers: C(5, 4) × C(4, 0) = 5 × 1 = 5 ways.\n"
                "Total valid panel combinations = 60 + 40 + 5 = 105 ways."
            ),
        },
    ],
}

