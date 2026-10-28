"""
logical_master.py — Prescribed Master Textbook for Logical Reasoning & Analytical Ability.
Comprehensive unabridged campus placement textbook covering Aristotelian syllogisms,
Euler diagrams, blood relations, family trees, direction sense vectors, circular and linear
seating arrangements, coding-decoding, EJOTY indexing, clock angle math, calendar odd days,
and placement analytical reasoning puzzles.
"""

LOGICAL_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Deductive Logic, Syllogisms & Euler / Venn Diagrams",
        "topics": [
            "The 4 Aristotelian categorical propositions: A (Universal Affirmative), E (Universal Negative), I (Particular Affirmative), O (Particular Negative)",
            "Rules of immediate inference: Conversion, Obversion, and Contraposition",
            "Venn / Euler diagram cross-intersection techniques for 2 and 3 statements",
            "Either-Or Conditions (Complementary Pairs): A-O, I-E, I-O pairs with identical subject/predicate",
            "Possibility cases vs definite conclusions in modern banking & IT placement syllogisms"
        ],
        "key_takeaways": "A conclusion is valid if and only if it holds across every possible Venn diagram representation. An 'Either-Or' condition requires: both conclusions independently false, same subjects/predicates, and forming a complementary pair."
    },
    {
        "chapter_num": 2,
        "title": "Blood Relations & Generational Family Trees",
        "topics": [
            "Relationship taxonomy: Paternal vs maternal relations, direct vs collateral lines, in-law designations",
            "Standard Family Tree diagramming symbols: Circles (Females), Squares (Males), Double lines (Spouses), Vertical branches (Generations)",
            "Decoded / Coded Blood Relations: Resolving algebraic operator trees (P + Q means P is father of Q)",
            "Pointing / Portrait statements: Reverse backtracking method from 'My' / 'Mine'"
        ],
        "key_takeaways": "Never assume gender based on a person's name alone; gender must be explicitly stated or deduced through an unambiguous relationship (e.g. father, mother, sister)."
    },
    {
        "chapter_num": 3,
        "title": "Direction Sense & Vector Displacement",
        "topics": [
            "The 8 Cardinal and Intercardinal Directions: North, South, East, West, NE, NW, SE, SW",
            "Rotations: Clockwise (+90, +180) vs Counter-Clockwise (-90, -180)",
            "Shadow phenomena: At Sunrise (shadow falls West), at Sunset (shadow falls East), at Noon (no shadow)",
            "Shortest direct displacement calculation via Pythagorean Theorem: d = sqrt(delta_x^2 + delta_y^2)"
        ],
        "key_takeaways": "Represent movements as 2D coordinate vectors (North = +y, South = -y, East = +x, West = -x). The shortest straight-line distance is sqrt(x^2 + y^2)."
    },
    {
        "chapter_num": 4,
        "title": "Seating Arrangements & Complex Analytical Puzzles",
        "topics": [
            "Linear Seating: Single row facing North, South, or mixed directions",
            "Parallel Row Seating: Two opposing rows facing each other",
            "Circular Seating: Facing the center (Left is Clockwise, Right is Counter-Clockwise) vs Facing outward (Left is Counter-Clockwise, Right is Clockwise)",
            "Rectangular and square arrangement constraints",
            "Grid elimination matrices for multi-attribute matching puzzles (Person + City + Car + Color)"
        ],
        "key_takeaways": "In circular arrangements facing inward, moving to a person's Right means moving Counter-Clockwise; moving to their Left means moving Clockwise. Facing outward reverses these completely."
    },
    {
        "chapter_num": 5,
        "title": "Coding-Decoding, Letter Series & Analytical Analogies",
        "topics": [
            "Positional indexing: The EJOTY system (E=5, J=10, O=15, T=20, Y=25)",
            "Reverse positional indexing: Formula (27 - forward position)",
            "Opposite letter pairs: AZ, BY, CX, DW, EV, FU, GT, HS, IR, JQ, KP, LO, MN",
            "Shift ciphers (+3, -2), alternating shifts, and reverse sequence transpositions",
            "Fictitious language / symbol substitution coding (e.g., 'nik pit sod' means 'bring cold water')"
        ],
        "key_takeaways": "The sum of positions of any letter and its opposite letter in the alphabet is always exactly 27 (e.g., A=1, Z=26 -> 1 + 26 = 27; B=2, Y=25 -> 2 + 25 = 27)."
    },
    {
        "chapter_num": 6,
        "title": "Clocks, Calendars & Mathematical Reasoning",
        "topics": [
            "Clock speed rates: Minute hand moves 6 deg/min; Hour hand moves 0.5 deg/min; Relative speed = 5.5 deg/min",
            "Clock angle formula: theta = |30H - 5.5M|",
            "Special positions: Coincide (0 deg) 11 times in 12h, Opposite (180 deg) 11 times in 12h, Right angles (90 deg) 22 times in 12h",
            "Calendar Odd Days concept: Ordinary year = 1 odd day; Leap year = 2 odd days",
            "Century odd days: 100 years = 5 odd days; 200 years = 3; 300 years = 1; 400 years = 0 odd days"
        ],
        "key_takeaways": "Between 11:00 and 1:00, clock hands coincide only once (at exactly 12:00), which is why coincidence occurs 11 times in 12 hours (22 times in 24 hours), not 24."
    },
    {
        "chapter_num": 7,
        "title": "Solved Placement Logical Tests & Analytical Puzzles",
        "topics": [
            "8-Person circular seating arrangement step-by-step trace",
            "Complex blood relation reverse deduction walkthrough",
            "Clock angle calculation with fractional minutes",
            "Calendar day determination for historical dates",
            "Self-assessment practice drills with verified solutions"
        ],
        "key_takeaways": "Mastering the EJOTY mapping, clock relative speed (5.5 deg/min), and family tree symbols guarantees top speed and accuracy in reasoning tests for TCS, Infosys, and Cognizant."
    }
]

LOGICAL_TEXTBOOK_MARKDOWN = r"""# Logical Reasoning & Analytical Ability: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Logical Reasoning & Analytical Ability  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement reasoning assessments, analytical ability tests, and logical problem-solving evaluations (TCS NQT, Infosys, Cognizant, Wipro, Accenture, Capgemini, Deloitte) are strictly grounded in the deductive rules, arrangement frameworks, and reasoning formulas detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Deductive Logic, Syllogisms & Euler / Venn Diagrams](#chapter-1-deductive-logic-syllogisms--euler--venn-diagrams)
  - [1.1 Categorical Propositions (A, E, I, O)](#11-categorical-propositions-a-e-i-o)
  - [1.2 Syllogistic Deduction Rules](#12-syllogistic-deduction-rules)
  - [1.3 The Either-Or Complementary Pairs](#13-the-either-or-complementary-pairs)
- [Chapter 2: Blood Relations & Generational Family Trees](#chapter-2-blood-relations--generational-family-trees)
  - [2.1 Generational Hierarchy & Standard Notation](#21-generational-hierarchy--standard-notation)
  - [2.2 Coded Blood Relations](#22-coded-blood-relations)
  - [2.3 Pointing Statements Reverse Method](#23-pointing-statements-reverse-method)
- [Chapter 3: Direction Sense & Vector Displacement](#chapter-3-direction-sense--vector-displacement)
  - [3.1 The 8 Compass Directions & Rotations](#31-the-8-compass-directions--rotations)
  - [3.2 Shadow Rules (Sunrise & Sunset)](#32-shadow-rules-sunrise--sunset)
  - [3.3 Shortest Vector Displacement](#33-shortest-vector-displacement)
- [Chapter 4: Seating Arrangements & Complex Analytical Puzzles](#chapter-4-seating-arrangements--complex-analytical-puzzles)
  - [4.1 Linear Seating Arrangements](#41-linear-seating-arrangements)
  - [4.2 Circular Seating (Inward vs Outward Facing)](#42-circular-seating-inward-vs-outward-facing)
  - [4.3 Multi-Attribute Grid Elimination](#43-multi-attribute-grid-elimination)
- [Chapter 5: Coding-Decoding, Letter Series & Analytical Analogies](#chapter-5-coding-decoding-letter-series--analytical-analogies)
  - [5.1 The EJOTY Positional Indexing System](#51-the-ejoty-positional-indexing-system)
  - [5.2 Reverse Positional Indexing & Opposite Pairs](#52-reverse-positional-indexing--opposite-pairs)
  - [5.3 Substitution & Fictitious Language Coding](#53-substitution--fictitious-language-coding)
- [Chapter 6: Clocks, Calendars & Mathematical Reasoning](#chapter-6-clocks-calendars--mathematical-reasoning)
  - [6.1 Clock Angle Mathematics & Relative Speed](#61-clock-angle-mathematics--relative-speed)
  - [6.2 Coincidence, Opposite & Right Angle Frequencies](#62-coincidence-opposite--right-angle-frequencies)
  - [6.3 Calendar Odd Days Determination](#63-calendar-odd-days-determination)
- [Chapter 7: Solved Placement Logical Tests & Analytical Puzzles](#chapter-7-solved-placement-logical-tests--analytical-puzzles)
  - [Solved Problem 1: 8-Person Circular Seating Puzzle](#solved-problem-1-8-person-circular-seating-puzzle)
  - [Solved Problem 2: Coded Blood Relations Deduction](#solved-problem-2-coded-blood-relations-deduction)
  - [Solved Problem 3: Clock Angle Calculation](#solved-problem-3-clock-angle-calculation)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: Deductive Logic, Syllogisms & Euler / Venn Diagrams

### 1.1 Categorical Propositions (A, E, I, O)
In formal deductive logic, statements are categorized into 4 fundamental Aristotelian propositions:

| Code | Type | Standard Form | Quantity | Quality | Venn Representation |
|:---:|:---|:---|:---:|:---:|:---|
| **A** | Universal Affirmative | **All S are P** | Universal | Affirmative | Circle S is entirely enclosed within Circle P ($S \subseteq P$). |
| **E** | Universal Negative | **No S is P** | Universal | Negative | Circle S and Circle P are completely disjoint ($S \cap P = \emptyset$). |
| **I** | Particular Affirmative | **Some S are P** | Particular | Affirmative | Circle S and Circle P have non-empty intersection ($S \cap P \ne \emptyset$). |
| **O** | Particular Negative | **Some S are not P** | Particular | Negative | At least one element of S lies outside P ($S \setminus P \ne \emptyset$). |

### 1.2 Syllogistic Deduction Rules
1. **Rule of Middle Term:** The middle term (the common term linking both premises) must be distributed (referring to ALL members of its class) in at least one premise.
2. **Two Negative Premises:** If both premises are negative (E or O), **NO definite conclusion** can be drawn!
3. **Two Particular Premises:** If both premises are particular (I or O), **NO definite conclusion** can be drawn!
4. **Negative Premise $\implies$ Negative Conclusion:** If one premise is negative, the valid conclusion must be negative.
5. **Particular Premise $\implies$ Particular Conclusion:** If one premise is particular, the valid conclusion must be particular.

### 1.3 The Either-Or Complementary Pairs
An **"Either I or II follows"** condition holds if and only if all three criteria are satisfied:
1. Both individual conclusions are independently false (not definitely true).
2. Both conclusions share the exact same Subject and Predicate.
3. The two conclusions form one of the **Complementary Pairs**:
   - Pair 1: **I and E** ("Some A are B" and "No A is B")
   - Pair 2: **A and O** ("All A are B" and "Some A are not B")
   - Pair 3: **I and O** ("Some A are B" and "Some A are not B")
   *(Note: A and E ("All A are B" and "No A is B") can both be false simultaneously and do NOT form a complementary pair!).*

---

## Chapter 2: Blood Relations & Generational Family Trees

### 2.1 Generational Hierarchy & Standard Notation
Constructing an unambiguous visual family tree diagram:
- **Horizontal Line ($\leftrightarrow$):** Marriage / Spouse relationship.
- **Horizontal Line ($\mathbf{-}$):** Sibling relationship.
- **Vertical Line ($\downarrow$):** Parent-Child generational descent.
- **Square ($\square$):** Male.
- **Circle ($\bigcirc$):** Female.

```
Generation 1 (Grandparents):   [Grandfather] = (Grandmother)
                                       |
Generation 2 (Parents/Aunts):  [Father] = (Mother) ------ [Uncle] = (Aunt)
                                   |                         |
Generation 3 (Current/Self):   [Brother] - (Sister) - [Self]  [Cousin]
```

### 2.2 Coded Blood Relations
In coded questions, algebraic operators designate relationships:
- $P + Q \implies P$ is the father of $Q$.
- $P - Q \implies P$ is the sister of $Q$.
- $P \times Q \implies P$ is the brother of $Q$.
- $P \div Q \implies P$ is the mother of $Q$.

**Systematic Solving Strategy:**
Start from the rightmost entity and work backward to the left, tracking gender and generational offset:
- Father / Mother $\implies$ Generation $+1$.
- Brother / Sister / Spouse $\implies$ Generation $0$.
- Son / Daughter $\implies$ Generation $-1$.

### 2.3 Pointing Statements Reverse Method
*Example:* "Pointing to a photograph, a woman says: 'He is the only son of the wife of my husband's father.'"
1. Start from 'My' $\implies$ The woman speaking.
2. 'My husband's father' $\implies$ Her father-in-law.
3. 'The wife of my father-in-law' $\implies$ Her mother-in-law.
4. 'The only son of her mother-in-law' $\implies$ **Her Husband**!
5. The photograph is of her husband.

---

## Chapter 3: Direction Sense & Vector Displacement

### 3.1 The 8 Compass Directions & Rotations
```
                 North (N)
                    |
     North-West     |     North-East
         \          |          /
          \         |         /
West (W) ----------+---------- East (E)
          /         |         \
         /          |          \
     South-West     |     South-East
                    |
                 South (S)
```

- Turning **Right** $\implies 90^\circ$ Clockwise rotation.
- Turning **Left** $\implies 90^\circ$ Counter-Clockwise rotation.

### 3.2 Shadow Rules (Sunrise & Sunset)
1. **At Sunrise:** The sun is in the East. All shadows fall strictly toward the **West**.
   - If a person faces North, their shadow falls to their **Left** (West).
   - If a person faces South, their shadow falls to their **Right** (West).
2. **At Sunset:** The sun is in the West. All shadows fall strictly toward the **East**.
   - If a person faces North, their shadow falls to their **Right** (East).
   - If a person faces South, their shadow falls to their **Left** (East).
3. **At 12:00 Noon:** The sun is directly overhead. **Zero shadow** is cast.

### 3.3 Shortest Vector Displacement
When a person walks $x$ meters East/West and $y$ meters North/South, the shortest straight-line distance back to the starting point is given by the hypotenuse:
$$\text{Distance } d = \sqrt{\Delta x^2 + \Delta y^2}$$

---

## Chapter 4: Seating Arrangements & Complex Analytical Puzzles

### 4.1 Circular Seating: Facing Inward vs Outward
- **Facing Inward (Toward Center):**
  - Moving to a person's **Right** $\implies$ **Counter-Clockwise** movement.
  - Moving to a person's **Left** $\implies$ **Clockwise** movement.
- **Facing Outward (Away from Center):**
  - Moving to a person's **Right** $\implies$ **Clockwise** movement.
  - Moving to a person's **Left** $\implies$ **Counter-Clockwise** movement.

*Golden Rule for Circular Seating:* Always place the first person at the bottom of the circle facing North. This makes their Left and Right align naturally with your own left and right hands!

---

## Chapter 5: Coding-Decoding, Letter Series & Analytical Analogies

### 5.1 The EJOTY Positional Indexing System
Memorize the positions of letters at multiples of 5:

$$\mathbf{E}=5, \quad \mathbf{J}=10, \quad \mathbf{O}=15, \quad \mathbf{T}=20, \quad \mathbf{Y}=25$$

### 5.2 Reverse Positional Indexing & Opposite Pairs
$$\text{Reverse Position} = 27 - \text{Forward Position}$$

**Mnemonic Table for Opposite Letter Pairs (Sum = 27):**
- **A - Z:** **A** to **Z**
- **B - Y:** **B**o**Y**
- **C - X:** **C**ru**X** / **C**o**X**
- **D - W:** **D**ew / **D**own
- **E - V:** **EV**ening / **L**o**VE**
- **F - U:** **FU**ll / **F**or **U**
- **G - T:** **G**.**T**. Road
- **H - S:** **H**igh **S**chool
- **I - R:** **I**ndian **R**ailways
- **J - Q:** **J**ungle **Q**ueen
- **K - P:** **K**an**P**ur / **P**K
- **L - O:** **LO**ve
- **M - N:** **M**a**N**

---

## Chapter 6: Clocks, Calendars & Mathematical Reasoning

### 6.1 Clock Angle Mathematics & Relative Speed
- Minute Hand speed $= 360^\circ / 60\text{ min} = \mathbf{6^\circ/\text{min}}$.
- Hour Hand speed $= 360^\circ / 720\text{ min} = \mathbf{0.5^\circ/\text{min}}$.
- Relative speed of Minute Hand over Hour Hand $= 6 - 0.5 = \mathbf{5.5^\circ/\text{min}} = \frac{11}{2}^\circ/\text{min}$.

**The Universal Clock Angle Formula:**
$$\theta = \left| 30 H - \frac{11}{2} M \right|$$
*(If $\theta > 180^\circ$, the reflex angle is $360^\circ - \theta$).*

*Example:* Angle at 3:40:
$$\theta = \left| 30(3) - \frac{11}{2}(40) \right| = |90 - 220| = |-130| = \mathbf{130^\circ}.$$

### 6.2 Coincidence, Opposite & Right Angle Frequencies
| Position | Angle ($\theta$) | In 12 Hours | In 24 Hours |
|:---|:---:|:---:|:---:|
| **Coincide (Together)** | $0^\circ$ | **11 times** | **22 times** |
| **Opposite (Straight Line)** | $180^\circ$ | **11 times** | **22 times** |
| **Right Angles (Perpendicular)** | $90^\circ$ | **22 times** | **44 times** |

### 6.3 Calendar Odd Days Determination
- 1 Ordinary Year $= 365\text{ days} = 52\text{ weeks} + \mathbf{1\text{ odd day}}$.
- 1 Leap Year $= 366\text{ days} = 52\text{ weeks} + \mathbf{2\text{ odd days}}$.
- 100 Years $= 76\text{ ordinary} + 24\text{ leap} = 76(1) + 24(2) = 124\text{ days} = 17\text{ weeks} + \mathbf{5\text{ odd days}}$.
- 200 Years $= 5 \times 2 = 10 \equiv \mathbf{3\text{ odd days}}$.
- 300 Years $= 5 \times 3 = 15 \equiv \mathbf{1\text{ odd day}}$.
- 400 Years $= (5 \times 4 + 1) = 21 \equiv \mathbf{0\text{ odd days}}$.

---

## Chapter 7: Solved Placement Logical Tests & Analytical Puzzles

### Solved Problem 1: 8-Person Circular Seating Puzzle
- **Problem:** Eight persons A, B, C, D, E, F, G, H sit around a circular table facing the center.
  - A sits third to the right of B.
  - C is an immediate neighbor of both A and E.
  - D sits second to the left of G.
  - H sits second to the right of A.
- **Solution Steps:**
  1. Fix B at position 1. Since B faces center, Right is Counter-Clockwise.
  2. A sits 3rd to right of B $\implies$ Position 4.
  3. H sits 2nd to right of A $\implies$ Position 6.
  4. C is neighbor of A and E $\implies$ C must be at Position 3 or 5. Since E must also neighbor C, test C at Position 5, E at Position 6 (occupied by H) $\implies$ Contradiction! Thus, C must be at Position 3, E at Position 2.
  5. Remaining slots: D sits 2nd to left of G. Place G at Position 8, D at Position 7.
  6. Final arrangement: $\mathbf{B, E, C, A, F, H, D, G}$.

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Clock Angle):** Find the angle between the hands of a clock at 8:20.
   - *Solution:* $\theta = |30(8) - 5.5(20)| = |240 - 110| = \mathbf{130^\circ}$.

2. **Exercise 2 (Blood Relations):** Pointing to a man, a woman says: "His mother is the only daughter of my mother." How is the woman related to the man?
   - *Solution:* "Only daughter of my mother" is the woman herself. So the man's mother is the woman. The woman is the man's **Mother**.

3. **Exercise 3 (Direction Displacement):** A person walks 12m North, turns East and walks 5m. What is the shortest distance from the start point?
   - *Solution:* $d = \sqrt{12^2 + 5^2} = \sqrt{144 + 25} = \sqrt{169} = \mathbf{13\text{ meters}}$.

4. **Exercise 4 (Opposite Letter):** What is the opposite letter of 'K' in the English alphabet?
   - *Solution:* $K = 11$. Opposite $= 27 - 11 = 16 \implies \mathbf{P}$.

5. **Exercise 5 (Syllogism Complementary Pair):** If Conclusions are: (I) "Some doctors are lawyers", (II) "No doctor is a lawyer". If both are not definitely true, what is the answer?
   - *Solution:* **Either I or II follows**. Statements form an I-E complementary pair with identical subjects and predicates.
"""

LOGICAL_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 6,
        "chapter_title": "Clocks, Calendars & Mathematical Reasoning",
        "subtopic": "Universal Clock Angle Formula",
        "question": "What is the angle between the hour hand and the minute hand of a clock at 3:40?",
        "options": [
            "130 degrees",
            "140 degrees",
            "120 degrees",
            "110 degrees"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Logical Reasoning Prescribed Textbook — Chapter 6: Clocks]\nUsing the formula theta = |30*H - 5.5*M|: theta = |30*(3) - 5.5*(40)| = |90 - 220| = |-130| = 130 degrees.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 5,
        "chapter_title": "Coding-Decoding, Letter Series & Analytical Analogies",
        "subtopic": "Opposite Letter Pairs",
        "question": "What is the sum of the forward positional indexes of any letter and its opposite reverse letter in the English alphabet?",
        "options": [
            "27",
            "26",
            "28",
            "25"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Logical Reasoning Prescribed Textbook — Chapter 5: Coding-Decoding]\nThe forward position of letter N and its opposite position M always sum up to exactly 27 (e.g. A(1) + Z(26) = 27, K(11) + P(16) = 27).",
        "difficulty": "easy",
    }
]
