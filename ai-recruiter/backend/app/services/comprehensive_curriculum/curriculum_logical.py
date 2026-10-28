"""
curriculum_logical.py - 8 Comprehensive Chapters for Logical Reasoning & Analytical Puzzles.
"""
from typing import List, Dict, Any

LOGICAL_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Syllogisms & Deductive Logic",
        "key_takeaways": "Master Venn diagram representations, A/E/I/O categorical propositions, rules of deduction, and 'Either-Or' complementary pairs.",
        "topics": [
            "Categorical Propositions: Universal Affirmative (All A are B), Universal Negative (No A is B), Particular Affirmative (Some A are B), Particular Negative (Some A are not B)",
            "Venn diagram methods: Minimal overlap vs maximal overlap testing",
            "Rules of Syllogism deduction without diagrams",
            "Complementary Pairs for 'Either-Or' conditions (Some + No, Some + Some not)",
            "Possibility cases vs definite conclusion verification"
        ],
        "sections": {
            "concept": """Syllogisms evaluate deductive logical validity. In placement tests (TCS, Infosys, Cognizant, Capgemini), candidates are given statements that must be accepted as 100% true, regardless of real-world facts, and must determine which conclusions logically follow.

**Categorical Propositions (A, E, I, O):**
1. **A (All $A$ are $B$):** Universal Affirmative. Venn: Circle $A$ lies entirely inside circle $B$.
2. **E (No $A$ is $B$):** Universal Negative. Venn: Circle $A$ and circle $B$ are completely disjoint.
3. **I (Some $A$ are $B$):** Particular Affirmative. Venn: Circles $A$ and $B$ overlap in at least one point.
4. **O (Some $A$ are not $B$):** Particular Negative.

**Complementary Pairs ('Either-Or'):**
An 'Either Conclusion I or II follows' answer requires three strict conditions:
1. Both conclusions share the exact same subject and predicate.
2. Both individual conclusions are independently false / uncertain.
3. The pair forms one of two valid complementary relationships:
   - **Some + No** (e.g., 'Some pens are books' and 'No pens are books')
   - **All + Some not** (e.g., 'All cats are dogs' and 'Some cats are not dogs').""",
            "formulas": """1. **Complementary Pair Invariants:**
   $$\\text{Either-Or} \\iff \\text{Same Elements} \\land \\text{Both Uncertain} \\land \\text{(Some + No OR All + Some Not)}$$""",
            "solved_examples": [
                {
                    "title": "Evaluating Statements with Possibility Conclusions",
                    "difficulty": "Medium | Infosys, TCS NQT, Wipro",
                    "problem": "Statements: 1) All mangoes are apples. 2) Some apples are oranges. Conclusions: I. Some mangoes being oranges is a possibility. II. Some apples are mangoes.",
                    "step_by_step": [
                        "Step 1: Check Conclusion II: Since All mangoes are apples, naturally Some apples must be mangoes (Definite True).",
                        "Step 2: Check Conclusion I: There is no negative restriction between mangoes and oranges. A Venn diagram can be drawn where the orange circle expands to touch mangoes without violating either statement.",
                        "Step 3: Since it can be true without violating statements, Conclusion I is a valid possibility (True).",
                        "Step 4: Both Conclusion I and II follow."
                    ],
                    "code_or_math": """// Syllogism Deduction:
// All M are A, Some A are O
// Conclusion I (Possibility M -> O): VALID
// Conclusion II (Definite A -> M): VALID
// Answer: Both I and II follow.""",
                    "explanation": "Possibility conclusions are valid if at least one compliant Venn diagram can represent the scenario."
                }
            ],
            "practice_questions": [
                {
                    "question": "Statements: No cat is dog. No dog is lion. Conclusion: No cat is lion. Does the conclusion follow?",
                    "options": [
                        "A) Follows definitely",
                        "B) Does not follow (Cat and lion could overlap)",
                        "C) Either follows or not",
                        "D) Invalid statement"
                    ],
                    "correct_answer": "B) Does not follow (Cat and lion could overlap)",
                    "detailed_solution": "Two negative premises yield no definite conclusion. Cats and lions have no stated restriction between them, so they could overlap."
                }
            ],
            "interview_questions": [
                {
                    "company": "TCS Digital",
                    "question": "What is the difference between 'Some A are B' and 'Only a few A are B'?",
                    "model_answer": "In standard logic, 'Some A are B' means at least one A is B, and it leaves open the possibility that *All* A could be B. In contrast, 'Only a few A are B' is a dual statement containing two simultaneous components: 1) A positive part: 'Some A are B'. 2) A negative part: 'Some A are NOT B'. Thus, under 'Only a few A are B', the conclusion 'All A being B is a possibility' is strictly FALSE.",
                    "interviewer_tip": "Highlight the dual positive + negative nature of 'Only a few'."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Seating Arrangements & Spatial Placement",
        "key_takeaways": "Master Linear single/parallel rows, Circular arrangements facing center vs facing outward, and position deduction tables.",
        "topics": [
            "Linear arrangements: Facing North (left/right aligns with candidate) vs Facing South",
            "Parallel row arrangements: Row 1 facing South, Row 2 facing North",
            "Circular arrangements: Facing Center (Left = Clockwise, Right = Counter-clockwise)",
            "Circular arrangements: Facing Outward (Left = Counter-clockwise, Right = Clockwise)",
            "Mixed facing directions circular puzzles and rectangular/square table arrangements"
        ],
        "sections": {
            "concept": """Seating Arrangement puzzles test spatial orientation and constraint propagation:
- **Linear Row Facing North:** Left is towards your left hand; Right is towards your right hand.
- **Linear Row Facing South:** Left is towards your right hand; Right is towards your left hand.
- **Circular Arrangement Facing Center:**
  - Turning **Right** = Moving **Counter-Clockwise**.
  - Turning **Left** = Moving **Clockwise**.
- **Circular Arrangement Facing Outward:**
  - Turning **Right** = Moving **Clockwise**.
  - Turning **Left** = Moving **Counter-Clockwise**.

**Standard Solving Strategy:**
1. Identify definite anchor clues (e.g., 'A sits at the extreme right end' or 'B sits opposite C').
2. Maintain two parallel branch sketches if a clue has two ambiguous possibilities.
3. Cross-reference remaining negative constraints ('D does not sit adjacent to E') to eliminate false branches.""",
            "formulas": """1. **Circular Clockwise/Counter-Clockwise Rules:**
   $$\\text{Facing Inside: } \\text{Immediate Right} = \\text{Counter-Clockwise}, \\quad \\text{Immediate Left} = \\text{Clockwise}$$
   $$\\text{Facing Outside: } \\text{Immediate Right} = \\text{Clockwise}, \\quad \\text{Immediate Left} = \\text{Counter-Clockwise}$$""",
            "solved_examples": [
                {
                    "title": "6 Persons Sitting Around a Circular Table Facing Center",
                    "difficulty": "Easy | Infosys, TCS, Cognizant",
                    "problem": "6 friends (A, B, C, D, E, F) sit in a circle facing the center. A is opposite D. B is to the immediate right of A. C is between A and E. Where is F sitting?",
                    "step_by_step": [
                        "Step 1: Place A at bottom (6 o'clock). D sits opposite A at top (12 o'clock).",
                        "Step 2: Facing center, immediate right of A (counter-clockwise) is B at 4 o'clock.",
                        "Step 3: C is between A and E: C must sit to the immediate left of A (clockwise) at 8 o'clock, placing E at 10 o'clock.",
                        "Step 4: The only remaining position is 2 o'clock, which must be occupied by F.",
                        "Step 5: F sits between D and B (or opposite C)."
                    ],
                    "code_or_math": """// Clock positions (Facing Center):
// 12 o'clock: D
//  2 o'clock: F
//  4 o'clock: B
//  6 o'clock: A
//  8 o'clock: C
// 10 o'clock: E""",
                    "explanation": "Placing A and D first grounds the coordinate circle, allowing deterministic counter-clockwise placement."
                }
            ],
            "practice_questions": [
                {
                    "question": "In a line of 7 people facing North, P sits exactly in the middle. How many people sit to the left of P?",
                    "options": ["A) 2", "B) 3", "C) 4", "D) 1"],
                    "correct_answer": "B) 3",
                    "detailed_solution": "For 7 people, positions are 1, 2, 3, 4, 5, 6, 7. The middle is position 4. To the left of position 4 are 3 people (positions 1, 2, 3)."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is the recommended approach to solve complex 8-person circular seating puzzles with mixed inward and outward facing directions?",
                    "model_answer": "Draw a circle with 8 radial spokes and directional arrows at each node. Start with clues that fix both position and facing direction (e.g., 'A faces inside and sits third to the right of B'). If an entity's direction is unknown, fork into two lightweight pencil diagrams (Case 1: Inward, Case 2: Outward). Fill in relative constraints. Invariably, one case will hit a direct contradiction within 2-3 clues, leaving the unique correct configuration.",
                    "interviewer_tip": "Emphasize maintaining at most two parallel hypotheses to prevent cognitive overload."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Blood Relations & Family Tree Analysis",
        "key_takeaways": "Master family tree generational diagrams, gender symbols (+/-), sibling vs spouse links, and coded blood relation decoding.",
        "topics": [
            "Generational leveling: Grandparents (+2), Parents (+1), Self/Siblings (0), Children (-1)",
            "Gender notation: [+] for Male, [-] for Female",
            "Relationship symbols: Horizontal double line (=) for Spouses, single horizontal line (-) for Siblings, vertical line (|) for Parent-Child",
            "Deciphering conversational pointers ('Pointing to a photograph, a woman said...')",
            "Coded blood relations: Decoding expressions like A + B * C - D"
        ],
        "sections": {
            "concept": """Blood Relations test logical deduction of kinship structures.

**Standard Tree Representation:**
- **Male:** Box $[+]$ or $+$.
- **Female:** Circle $(-)$ or $-$.
- **Married Couple:** Connected by horizontal double-line ($A = B$).
- **Siblings:** Connected by horizontal single line ($A - B$).
- **Generational Shift:** Connected by vertical line downward.

**Conversational Pointers Technique:**
For statements like 'He is the only son of my father's father':
1. Break down the sentence from the end ('my father's father' = paternal grandfather).
2. 'Only son of paternal grandfather' = my father.
3. 'He is the son of my father' = my brother (or myself).""",
            "formulas": """1. **Kinship Shorthand:**
   $$\\text{Paternal} = \\text{Father's side}, \\quad \\text{Maternal} = \\text{Mother's side}$$
   $$\\text{Nephew/Niece} = \\text{Sibling's son/daughter}, \\quad \\text{Cousin} = \\text{Uncle/Aunt's child}$$""",
            "solved_examples": [
                {
                    "title": "Deciphering Pointing to a Photograph Problem",
                    "difficulty": "Easy | TCS, Cognizant, Wipro",
                    "problem": "Pointing to a man, a woman says: 'His mother is the only daughter of my mother.' How is the woman related to the man?",
                    "step_by_step": [
                        "Step 1: Analyze 'the only daughter of my mother': For the woman speaking, the only daughter of her mother must be the woman herself!",
                        "Step 2: Substitute back into sentence: 'His mother is [myself]'.",
                        "Step 3: Therefore, the woman is the man's Mother."
                    ],
                    "code_or_math": """// Backward Substitution:
// 'my mother's only daughter' = the woman herself
// 'His mother is [myself]'
// Woman = Mother of the man""",
                    "explanation": "Deconstructing relational phrases from the possessive end resolves conversational puzzles cleanly."
                }
            ],
            "practice_questions": [
                {
                    "question": "A is B's brother. C is A's father. D is C's father. E is D's mother. How is A related to D?",
                    "options": ["A) Grandfather", "B) Grandson", "C) Son", "D) Great-grandson"],
                    "correct_answer": "B) Grandson",
                    "detailed_solution": "D is C's father, and C is A's father. Hence D is A's grandfather, meaning A is D's grandson."
                }
            ],
            "interview_questions": [
                {
                    "company": "Infosys",
                    "question": "In coded blood relations where A + B means A is father of B, A - B means A is sister of B, and A * B means A is brother of B, which expression means P is aunt of Q?",
                    "model_answer": "For P to be an aunt of Q: 1) P must be female (-). 2) P must be the sister of Q's parent. Consider expression `P - R + Q`: `P - R` means P is sister of R. `R + Q` means R is father of Q. Since P is the sister of Q's father R, P is strictly the paternal aunt of Q.",
                    "interviewer_tip": "Check the gender of the target person first to eliminate invalid answer choices instantly."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Direction Sense & Path Traversal",
        "key_takeaways": "Master cardinal directions (N, S, E, W), ordinal directions (NE, NW, SE, SW), right/left 90-degree rotations, Pythagoras shortest distance, and shadow problems.",
        "topics": [
            "Cardinal and Ordinal coordinate planes (NESW clockwise compass order)",
            "Turn mechanics: Left turn (-90 deg), Right turn (+90 deg), U-turn (180 deg)",
            "Shortest displacement calculation using Pythagoras theorem (sqrt(x^2 + y^2))",
            "Shadow problems at Sunrise (shadow points West) and Sunset (shadow points East)",
            "Angle rotations: Clockwise vs Counter-Clockwise angular additions"
        ],
        "sections": {
            "concept": """Direction Sense evaluates 2D spatial navigation:
- **Clockwise Compass Sequence:** North -> East -> South -> West (mnemonic: **NESW**).
- A **Right turn** always advances $90^\\circ$ clockwise.
- A **Left turn** always advances $90^\\circ$ counter-clockwise.

**Displacement & Pythagoras Theorem:**
To find the shortest straight-line distance from starting point $(0,0)$ to ending point $(x,y)$:
$$\\text{Shortest Distance} = \\sqrt{(\\Delta x)^2 + (\\Delta y)^2}$$

**Shadow Rules:**
- **At Sunrise (Sun in East):** All shadows fall towards the **West**. If a person faces North, their shadow is on their Left.
- **At Sunset (Sun in West):** All shadows fall towards the **East**. If a person faces North, their shadow is on their Right.
- **At Noon (12:00 PM):** The sun is directly overhead; shadows are negligibly small (no direction).""",
            "formulas": """1. **Pythagoras Displacement:**
   $$d = \\sqrt{(\\Delta x)^2 + (\\Delta y)^2}$$
2. **Shadow Orientation:**
   $$\\text{Sunrise} \\implies \\text{Shadow West}; \\quad \\text{Sunset} \\implies \\text{Shadow East}$$""",
            "solved_examples": [
                {
                    "title": "Finding Final Displacement and Direction",
                    "difficulty": "Easy | TCS, Infosys, Wipro",
                    "problem": "A person walks 4km North, turns right and walks 3km. Find their straight-line distance and direction from the start.",
                    "step_by_step": [
                        "Step 1: North is along $+y$ axis: $(0, 4)$.",
                        "Step 2: Right turn from North is East ($+x$ axis): $(3, 4)$.",
                        "Step 3: Distance $= \\sqrt{3^2 + 4^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5$km.",
                        "Step 4: Vector $(+3, +4)$ points North-East.",
                        "Step 5: Person is 5km North-East from start."
                    ],
                    "code_or_math": """// Vector Coordinates:
// Start = (0, 0)
// North 4km = (0, 4)
// Turn Right (East) 3km = (3, 4)
// Distance = sqrt(3^2 + 4^2) = 5 km North-East""",
                    "explanation": "Standard 3-4-5 Pythagorean triplet calculation."
                }
            ],
            "practice_questions": [
                {
                    "question": "One morning after sunrise, Suresh was standing facing a pole. The shadow of the pole fell exactly to his right. Which direction was Suresh facing?",
                    "options": ["A) East", "B) South", "C) West", "D) North"],
                    "correct_answer": "B) South",
                    "detailed_solution": "At sunrise, sun is in East, so all shadows fall West. If the shadow is to Suresh's right, his right hand points West. If your right hand points West, you must be facing South."
                }
            ],
            "interview_questions": [
                {
                    "company": "Cognizant",
                    "question": "A person faces North, turns 135 degrees clockwise, and then 180 degrees counter-clockwise. Which direction are they facing now?",
                    "model_answer": "Track net angular rotation: $+135^\\circ$ (clockwise) $- 180^\\circ$ (counter-clockwise) $= -45^\\circ$ (net $45^\\circ$ counter-clockwise). Turning $45^\\circ$ counter-clockwise from North points directly to **North-West**.",
                    "interviewer_tip": "Sum signed angles rather than rotating iteratively."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Coding-Decoding, Series & Analogy",
        "key_takeaways": "Master English alphabet position values (A=1 to Z=26), EJOTY mnemonic, letter shifts, number series differences, and matrix coding.",
        "topics": [
            "Alphabet positioning: Forward (A=1, Z=26) and Backward reverse pairs (A-Z, B-Y via sum=27 rule)",
            "The EJOTY mnemonic (5, 10, 15, 20, 25) for instant letter indexing",
            "Letter shifting, reversal, and cross-pairing cipher patterns",
            "Number Series: Arithmetic, Geometric, Prime, Fibonacci, Alternating differences",
            "Alphanumeric Symbol series and matrix coding"
        ],
        "sections": {
            "concept": """Coding-Decoding and Series evaluate pattern recognition and rule extraction:
- **Alphabet Indexing (EJOTY):** $E=5, J=10, O=15, T=20, Y=25$.
- **Reverse Letter Pairs (Sum = 27):**
  $A(1) + Z(26) = 27$, $B(2) + Y(25) = 27$, $C(3) + X(24) = 27$, $M(13) + N(14) = 27$.
  To find the opposite letter of any letter with rank $R$, compute $27 - R$.

**Series Decomposition:**
1. Check difference between consecutive numbers ($\\Delta$). If second differences ($\\Delta^2$) are constant, it is a quadratic sequence.
2. Check multiplicative ratios (geometric series).
3. Check primes or cubes/squares ($n^2 \\pm 1$, $n^3 \\pm 1$).""",
            "formulas": """1. **Reverse Letter Rule:**
   $$\\text{Reverse Rank} = 27 - \\text{Forward Rank}$$""",
            "solved_examples": [
                {
                    "title": "Solving Number Series via Second Differences",
                    "difficulty": "Easy | Infosys, TCS, Wipro",
                    "problem": "Find the missing number in the series: 2, 5, 10, 17, 26, ?.",
                    "step_by_step": [
                        "Step 1: Compute first differences: $5-2=3, 10-5=5, 17-10=7, 26-17=9$.",
                        "Step 2: Notice differences are consecutive odd numbers: 3, 5, 7, 9, 11...",
                        "Step 3: Alternatively, notice $n^2 + 1$: $1^2+1=2, 2^2+1=5, 3^2+1=10, 4^2+1=17, 5^2+1=26$.",
                        "Step 4: Next number $= 6^2 + 1 = 37$ (or $26 + 11 = 37$)."
                    ],
                    "code_or_math": """// Series Pattern:
// 1^2 + 1 = 2
// 2^2 + 1 = 5
// 3^2 + 1 = 10
// 4^2 + 1 = 17
// 5^2 + 1 = 26
// 6^2 + 1 = 37""",
                    "explanation": "Recognizing $n^2 + 1$ patterns provides instant solutions."
                }
            ],
            "practice_questions": [
                {
                    "question": "If 'EARTH' is coded as 'GCTVJ', how is 'GLOBE' coded in that language?",
                    "options": ["A) INQDG", "B) HMNCD", "C) INQDH", "D) JNQDG"],
                    "correct_answer": "A) INQDG",
                    "detailed_solution": "Each letter is shifted forward by +2 positions: E(+2)=G, A(+2)=C, R(+2)=T, T(+2)=V, H(+2)=J. Applying to GLOBE: G(+2)=I, L(+2)=N, O(+2)=Q, B(+2)=D, E(+2)=G -> INQDG."
                }
            ],
            "interview_questions": [
                {
                    "company": "TCS Digital",
                    "question": "How do you identify whether a coding problem uses a direct letter substitution cipher or an arithmetic shift cipher?",
                    "model_answer": "Count the number of distinct characters in the given word and compare them to the code. If multiple words are provided in the problem and identical letters across words map to identical coded letters regardless of position (e.g., 'E' is always '7'), it is a Direct Substitution Cipher. If the mapping changes based on character position or maintains a constant alphabetical offset across letters (e.g., $+2, -1, +2$), it is an Arithmetic Shift Cipher.",
                    "interviewer_tip": "Cross-check common letters between sample words."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Clocks, Calendars & Binary Logic",
        "key_takeaways": "Master angle between clock hands, clock speed gains/losses, leap year rules, odd days calculation, and Truth-Teller / Liar puzzles.",
        "topics": [
            "Clock face geometry: Minute hand speeds (6 deg/min) vs Hour hand speeds (0.5 deg/min)",
            "Angle between hands formula: theta = |30H - (11/2)M|",
            "Coincidence (0 deg), Right angle (90 deg), and Opposite (180 deg) frequencies",
            "Calendar mechanics: Ordinary years (1 odd day) vs Leap years (2 odd days)",
            "Binary Logic: Knights and Knaves (Truth-Tellers, Liars, and Alternators)"
        ],
        "sections": {
            "concept": """Clocks and Calendars evaluate modular arithmetic:
- **Clock Mechanics:**
  - Minute hand moves $360^\\circ / 60 = 6^\\circ$ per minute.
  - Hour hand moves $360^\\circ / (12 \\times 60) = 0.5^\\circ$ per minute.
  - Relative speed of minute hand over hour hand $= 6 - 0.5 = 5.5^\\circ = \\frac{11}{2}^\\circ$ per minute.

**Calendar Odd Days:**
An 'Odd Day' is the remainder when total days are divided by 7:
- Ordinary year (365 days) $= 52 \\text{ weeks} + 1 \\text{ odd day}$.
- Leap year (366 days) $= 52 \\text{ weeks} + 2 \\text{ odd days}$.
- Century leap rule: A century year (e.g., 1900, 2000) is a leap year if and only if it is divisible by **400** (2000 is a leap year; 1900 is NOT).

**Binary Logic (Knights and Knaves):**
Solve by contradiction: Assume Person A is a Truth-Teller. If their statement implies a logical impossibility, the assumption is false and Person A is a Liar.""",
            "formulas": """1. **Clock Angle Formula:**
   $$\\theta = \\left|30H - \\frac{11}{2}M\\right|$$
2. **Odd Days per Century:**
   $$\\text{100 years} = 5 \\text{ odd days}; \\quad \\text{200 years} = 3; \\quad \\text{300 years} = 1; \\quad \\text{400 years} = 0$$""",
            "solved_examples": [
                {
                    "title": "Finding the Angle Between Clock Hands at 3:40",
                    "difficulty": "Easy | TCS, Infosys, Cognizant",
                    "problem": "Find the angle between the hour hand and the minute hand of a clock at 3:40.",
                    "step_by_step": [
                        "Step 1: Here $H = 3, M = 40$.",
                        "Step 2: Apply formula: $\\theta = |30(3) - \\frac{11}{2}(40)|$.",
                        "Step 3: $\\theta = |90 - 220| = |-130| = 130^\\circ$.",
                        "Step 4: Angle is $130^\\circ$ (reflex angle is $360 - 130 = 230^\\circ$)."
                    ],
                    "code_or_math": """// Calculation:
// Angle = |30 * 3 - 5.5 * 40| = |90 - 220| = 130 degrees""",
                    "explanation": "Direct application of the clock angle formula gives exact degrees instantly."
                }
            ],
            "practice_questions": [
                {
                    "question": "What day of the week was 15th August 1947?",
                    "options": ["A) Thursday", "B) Friday", "C) Saturday", "D) Wednesday"],
                    "correct_answer": "B) Friday",
                    "detailed_solution": "1600 years = 0 odd days. 300 years = 1 odd day. 46 years (11 leap, 35 ordinary) = $22 + 35 = 57 / 7 = 1$ odd day. Jan-July 1947 odd days = $3+0+3+2+3+2+3 = 16 / 7 = 2$. Aug 15 = $15 / 7 = 1$ odd day. Total odd days $= 0 + 1 + 1 + 2 + 1 = 5$. Day 5 corresponds to Friday."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google",
                    "question": "How many times do the hands of a clock overlap (coincide) in a 24-hour day?",
                    "model_answer": "The hands overlap **22 times** in 24 hours (not 24 times). In every 12-hour period, the hands overlap 11 times because the overlap between 11:00 and 1:00 occurs exactly once at 12:00. Over 24 hours, $11 \\times 2 = 22$ overlaps.",
                    "interviewer_tip": "Cite the 11:00 to 1:00 single-overlap exception at 12:00."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Critical Reasoning & Statement-Assumptions",
        "key_takeaways": "Master Statement & Assumptions, Statement & Conclusions, Course of Action, Cause & Effect, and Strong vs Weak Arguments.",
        "topics": [
            "Statement & Assumptions: Unstated premises taken for granted by the speaker",
            "Statement & Conclusions: Necessary logical deductions based strictly on provided text",
            "Course of Action: Pragmatic, proportional, and non-extreme corrective measures",
            "Cause and Effect: Direct causes, common causes, and coincidental correlation",
            "Strong vs Weak Arguments: Fact-based vs opinion/emotional arguments"
        ],
        "sections": {
            "concept": """Critical Reasoning evaluates business decision-making and cognitive bias resistance:
- **Assumption:** An unstated premise that the author took for granted when formulating the statement. An assumption is valid if negating it destroys the statement's logical validity (**Negation Test**).
- **Conclusion:** A deduction that MUST be true if the statement is true. Avoid assumptions or real-world external knowledge when evaluating conclusions.
- **Course of Action:** A realistic administrative action to resolve a problem. Must be proportional: severe extreme measures (e.g., immediately firing an entire department) are invalid courses of action.""",
            "formulas": """1. **The Negation Test for Assumptions:**
   $$\\text{Negate Assumption} \\implies \\text{Does the author's argument collapse? If YES } \\implies \\text{VALID ASSUMPTION}$$""",
            "solved_examples": [
                {
                    "title": "Applying the Negation Test to Statement & Assumptions",
                    "difficulty": "Easy | Infosys, TCS, Capgemini",
                    "problem": "Statement: 'The company has decided to launch a new mobile application to increase customer engagement.' Assumption: Customers prefer mobile applications over physical visits.",
                    "step_by_step": [
                        "Step 1: Apply Negation Test: Assume customers DO NOT prefer mobile applications.",
                        "Step 2: If customers reject mobile apps, launching an app would NOT increase engagement.",
                        "Step 3: The company's decision depends entirely on this premise.",
                        "Step 4: The assumption is implicitly made and is VALID."
                    ],
                    "code_or_math": """// Negation Test:
// 'Customers do not prefer apps' -> Company action becomes illogical
// Therefore, the assumption is implicitly necessary (Implicit).""",
                    "explanation": "Valid assumptions are foundational premises upon which statements depend."
                }
            ],
            "practice_questions": [
                {
                    "question": "Statement: 'Smoking in public places is banned.' Course of Action: I. Violators should be fined. II. All tobacco factories should be permanently bulldozed.",
                    "options": [
                        "A) Both follow",
                        "B) Only I follows",
                        "C) Only II follows",
                        "D) Neither follows"
                    ],
                    "correct_answer": "B) Only I follows",
                    "detailed_solution": "Action I is proportional and directly enforces the ban. Action II is disproportionately extreme and harms the broader economy."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is the difference between Correlation and Causation in data reasoning?",
                    "model_answer": "Correlation means two variables display a statistical relationship or trend together (e.g., ice cream sales and drowning rates both increase in summer). Causation means a change in one variable directly causes a change in the other. In the example, ice cream does not cause drowning; both are caused by a third confounding variable: warm summer temperatures. Confusing correlation with causation leads to flawed business strategies.",
                    "interviewer_tip": "Cite confounding variables in business decision making."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Complex Analytical Puzzles & Floor/Grid Arrangements",
        "key_takeaways": "Master Multi-variable matrix puzzles, Floor/Building puzzles with lift/color attributes, and grid scheduling.",
        "topics": [
            "Matrix puzzles with 3+ variables (Person, Profession, City, Car)",
            "Floor puzzles: Top-to-bottom numbering, odd/even floors, adjacent floor constraints",
            "Box stacking puzzles with relative distance constraints",
            "Tabular deduction grids (Tick/Cross elimination tables)",
            "Placement assessment time-management strategy for complex analytical puzzles"
        ],
        "sections": {
            "concept": """Complex Analytical Puzzles synthesize multiple logical constraints across 3 to 4 independent variables (e.g., 7 people living on 7 different floors, working in 7 different companies, driving 7 different color cars).

**Solving Methodology:**
1. **Choose the Anchor Axis:** Pick the most fixed, immutable variable as the table backbone (e.g., Floor Numbers $7, 6, 5, 4, 3, 2, 1$ or Days of the Week Monday-Sunday).
2. **Direct Mapping:** Fill in definite positive clues immediately.
3. **Negative Clue Stacking:** Write negative clues on the margin (e.g., 'A does not live on Floor 3').
4. **Link Chaining:** Look for clues connecting the same person across multiple attributes to unlock multiple cells simultaneously.""",
            "formulas": """1. **Anchor Selection Priority:**
   $$\\text{Floors (1-7)} \\gg \\text{Days of Week (Mon-Sun)} \\gg \\text{Arbitrary Person Names}$$""",
            "solved_examples": [
                {
                    "title": "Solving a 7-Story Building Floor Puzzle",
                    "difficulty": "Medium | Infosys, TCS Digital, Wipro",
                    "problem": "7 people (A-G) live on floors 1-7. Top floor is 7. A lives on an odd floor. Only 3 people live between A and B. B lives on a floor immediately above C. Determine B and C's floors.",
                    "step_by_step": [
                        "Step 1: A is on an odd floor (1, 3, 5, 7). Exactly 3 people between A and B.",
                        "Step 2: If A = 1, B must be on floor $1 + 3 + 1 = 5$. Then C is on floor 4 (immediately below B). Valid!",
                        "Step 3: If A = 7, B must be on floor $7 - 3 - 1 = 3$. Then C is on floor 2. Valid!",
                        "Step 4: Use subsequent problem constraints to lock in Case 1 or 2."
                    ],
                    "code_or_math": """// Floor Skeleton:
// 7: 
// 6: 
// 5: B
// 4: C
// 3: 
// 2: 
// 1: A (Gap of 3 floors between A and B!)""",
                    "explanation": "Floor indices provide a natural vertical coordinate system that narrows possibilities."
                }
            ],
            "practice_questions": [
                {
                    "question": "In a 6-floor building, if X lives on an even-numbered floor and there are 2 floors between X and Y, what floor can Y live on if X is on floor 2?",
                    "options": ["A) Floor 4", "B) Floor 5", "C) Floor 6", "D) Floor 3"],
                    "correct_answer": "B) Floor 5",
                    "detailed_solution": "Between floor 2 and floor 5 are floors 3 and 4 (exactly 2 floors)."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "When solving an analytical puzzle in a timed assessment, when should you abandon a puzzle and move on?",
                    "model_answer": "Follow the **3-Minute Rule**: If within 3 minutes of reading the puzzle, you cannot construct a clear skeleton table or eliminate at least 50% of ambiguities, immediately flag the puzzle, guess conservatively if there is no negative marking, and move on. Complex puzzles can consume 15+ minutes with zero return, sacrificing easier questions later in the section.",
                    "interviewer_tip": "Demonstrate strategic exam time management."
                }
            ]
        }
    }
]
