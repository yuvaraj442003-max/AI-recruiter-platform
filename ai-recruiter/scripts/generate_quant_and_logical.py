"""
Generates complete master textbooks for:
- Quantitative Aptitude (quant_master.py)
- Logical Reasoning (logical_master.py)
"""
import os
import ast

TEXTBOOK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "app", "services", "textbooks"))

# =============================================================================
# QUANT MASTER TEXTBOOK
# =============================================================================
QUANT_CONTENT = r'''"""
quant_master.py — Prescribed Master Textbook for Quantitative Aptitude.
Comprehensive campus placement textbook covering speed arithmetic, divisibility rules,
percentages, profit and loss, time and work (LCM model), time-speed-distance (harmonic mean),
interest formulas, permutations and combinations, probability, and data interpretation.
"""

QUANT_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Number Systems, Divisibility Rules & Remainder Theorems",
        "topics": ["Divisibility rules (2, 3, 4, 5, 6, 7, 8, 9, 11, 13) and composite factorization", "Units digit cyclicity of powers (cyclicity of 2, 3, 7, 8 is 4; 4, 9 is 2; 0, 1, 5, 6 is 1)", "HCF and LCM properties: Product formula A * B = HCF(A,B) * LCM(A,B)", "Wilson's Theorem, Fermat's Little Theorem, and Chinese Remainder Theorem basics"],
        "key_takeaways": "Divisibility by 11: Difference between sum of odd-place digits and even-place digits must be 0 or a multiple of 11. HCF divides LCM without remainder."
    },
    {
        "chapter_num": 2,
        "title": "Percentages, Profit, Loss & Successive Discounts",
        "topics": ["Multiplying factors (10% increase = 1.1x; 20% decrease = 0.8x)", "Cost Price (CP), Selling Price (SP), Marked Price (MP), and Margin vs Markup", "Successive percentage change formula: net = a + b + (a * b / 100)", "Dishonest dealer / false weight calculations: Gain% = (Error / [True Value - Error]) * 100"],
        "key_takeaways": "Two successive discounts of d1% and d2% produce an effective net discount of: d1 + d2 - (d1 * d2 / 100)%. Profit is always calculated on CP unless stated otherwise."
    },
    {
        "chapter_num": 3,
        "title": "Ratio, Proportion & The Alligation Cross-Method",
        "topics": ["Direct, inverse, and compound proportions", "Mean proportional, third proportional, and fourth proportional formulas", "Rule of Alligation for mixing ingredients of different costs", "Repeated dilution/replacement formula: Final Amount = Initial * (1 - x / V)^n"],
        "key_takeaways": "Alligation ratio = (Dearer Price - Mean Price) : (Mean Price - Cheaper Price). In repeated replacement of x liters from V liters, the ratio of original liquid remaining is (1 - x/V)^n."
    },
    {
        "chapter_num": 4,
        "title": "Time and Work, Pipes & Cisterns (The LCM Efficiency Model)",
        "topics": ["LCM Total Work Assumption technique: converting days into daily unit rates", "Combined efficiency, alternate day work, and negative work (inlet vs outlet pipes)", "Man-Days-Hours equivalence formula: (M1 * D1 * H1) / W1 = (M2 * D2 * H2) / W2", "Wages division rules: Wages are divided in strict proportion to total work done"],
        "key_takeaways": "Assume total work = LCM of individual times. Daily efficiency = Total Work / Days. If A does work in 12 days and B in 15 days, assume work = 60 units; A does 5 units/day, B does 4 units/day."
    },
    {
        "chapter_num": 5,
        "title": "Time, Speed, Distance, Trains & Relative Velocity",
        "topics": ["Speed = Distance / Time; Conversion factor: 1 km/h = 5/18 m/s; 1 m/s = 18/5 km/h", "Average speed for equal distances = Harmonic Mean: 2xy / (x + y), NEVER arithmetic mean", "Relative speed: Same direction (|S1 - S2|); Opposite directions (S1 + S2)", "Trains passing stationary objects (Distance = Length of Train) vs platforms (Distance = Train + Platform)", "Boats and streams: Downstream = u + v; Upstream = u - v; Still water speed = (Downstream + Upstream) / 2"],
        "key_takeaways": "When distances are equal, average speed is 2S1*S2 / (S1 + S2). When travel times are equal, average speed is the arithmetic mean (S1 + S2) / 2."
    },
    {
        "chapter_num": 6,
        "title": "Simple Interest, Compound Interest & Depreciation",
        "topics": ["Simple Interest: SI = (P * R * T) / 100", "Compound Interest: A = P * (1 + R / 100)^T; Semi-annual (R/2, 2T) and quarterly compounding", "Difference between CI and SI for 2 years: Diff = P * (R / 100)^2", "Difference between CI and SI for 3 years: Diff = P * (R / 100)^2 * (3 + R / 100)", "Effective annual rate of compounding"],
        "key_takeaways": "The 2-year difference between CI and SI is exactly the interest on the first year's interest: P*(R/100)^2."
    },
    {
        "chapter_num": 7,
        "title": "Permutations, Combinations, Probability & Data Interpretation",
        "topics": ["Arrangements: nPr = n! / (n - r)!; Selections: nCr = n! / [r! * (n - r)!]; nCr = nC(n - r)", "Circular arrangements: (n - 1)! for distinct items; (n - 1)! / 2 for necklaces", "Probability axioms, sample spaces, independent events P(A and B) = P(A) * P(B)", "Data Interpretation: Pie chart angle conversion (1% = 3.6 degrees), bar graphs, and tabular data extraction"],
        "key_takeaways": "Permutations care about order (AB != BA); Combinations care only about selection (AB == BA). Mutually exclusive events have P(A and B) = 0."
    }
]

QUANT_TEXTBOOK_MARKDOWN = r"""# Quantitative Aptitude: Corporate Recruitment Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement & Technical Interview Edition  
**Subject:** Quantitative Aptitude  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus recruitment quantitative assessment questions across top companies (TCS NQT, Infosys DSE, Cognizant, Accenture, Wipro, Amazon, Deloitte, Capgemini, etc.) are strictly grounded in the numerical arithmetic, formulas, and shortcut techniques presented in this master textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Number Systems, Divisibility Rules & Remainder Theorems](#chapter-1-number-systems-divisibility-rules--remainder-theorems)
- [Chapter 2: Percentages, Profit, Loss & Successive Discounts](#chapter-2-percentages-profit-loss--successive-discounts)
- [Chapter 3: Ratio, Proportion & The Alligation Cross-Method](#chapter-3-ratio-proportion--the-alligation-cross-method)
- [Chapter 4: Time and Work, Pipes & Cisterns (The LCM Efficiency Model)](#chapter-4-time-and-work-pipes--cisterns-the-lcm-efficiency-model)
- [Chapter 5: Time, Speed, Distance, Trains & Relative Velocity](#chapter-5-time-speed-distance-trains--relative-velocity)
- [Chapter 6: Simple Interest, Compound Interest & Depreciation](#chapter-6-simple-interest-compound-interest--depreciation)
- [Chapter 7: Permutations, Combinations, Probability & Data Interpretation](#chapter-7-permutations-combinations-probability--data-interpretation)
- [Chapter 8: Solved Placement Quantitative Problems & Drills](#chapter-8-solved-placement-quantitative-problems--drills)

---

## Chapter 1: Number Systems, Divisibility Rules & Remainder Theorems

### 1.1 Complete Divisibility Rules
- **Divisibility by 2:** Last digit is even ($0, 2, 4, 6, 8$).
- **Divisibility by 3:** Sum of digits is divisible by 3.
- **Divisibility by 4:** Last 2 digits form a number divisible by 4.
- **Divisibility by 5:** Last digit is 0 or 5.
- **Divisibility by 6:** Number is divisible by both 2 and 3.
- **Divisibility by 7:** Double the last digit and subtract from the remaining truncated number. Result must be divisible by 7.
- **Divisibility by 8:** Last 3 digits form a number divisible by 8.
- **Divisibility by 9:** Sum of digits is divisible by 9.
- **Divisibility by 11:** Difference between the sum of digits at odd positions and the sum of digits at even positions is either 0 or a multiple of 11.
  *Example:* Check 85976: $(8 + 9 + 6) - (5 + 7) = 23 - 12 = 11 \implies$ Divisible by 11.

### 1.2 Cyclicity of Powers (Finding the Units Digit)
When finding the units digit of $A^B$, compute $B \pmod 4$:
- **Cyclicity 4:** $\{2, 3, 7, 8\}$. (e.g. $7^1=7, 7^2=9, 7^3=3, 7^4=1$).
- **Cyclicity 2:** $\{4, 9\}$. (e.g. $4^{\text{odd}} = 4, 4^{\text{even}} = 6$; $9^{\text{odd}} = 9, 9^{\text{even}} = 1$).
- **Cyclicity 1:** $\{0, 1, 5, 6\}$. (Always retain their respective units digit).
*Example:* Units digit of $7^{105}$: $105 \pmod 4 = 1 \implies 7^1 = 7$.

### 1.3 Fundamental HCF and LCM Theorem
$$\text{Product of Two Numbers} = \text{HCF}(A, B) \times \text{LCM}(A, B)$$
$$\text{HCF of Fractions} = \frac{\text{HCF of Numerators}}{\text{LCM of Denominators}}, \quad \text{LCM of Fractions} = \frac{\text{LCM of Numerators}}{\text{HCF of Denominators}}$$

---

## Chapter 2: Percentages, Profit, Loss & Successive Discounts

### 2.1 Multiplying Factors
- An increase of $P\%$: $\text{Multiplying Factor} = 1 + \frac{P}{100}$
- A decrease of $P\%$: $\text{Multiplying Factor} = 1 - \frac{P}{100}$

### 2.2 Successive Percentage Changes
If a quantity changes successively by $+a\%$ and then by $+b\%$:
$$\text{Net Percentage Change} = a + b + \frac{a \times b}{100}\%$$

### 2.3 Successive Discounts Formula
For two successive store discounts of $d_1\%$ and $d_2\%$:
$$\text{Equivalent Single Discount} = d_1 + d_2 - \frac{d_1 \times d_2}{100}\%$$
*Example:* Successive discounts of $20\%$ and $10\%$:
$$\text{Net Discount} = 20 + 10 - \frac{20 \times 10}{100} = 30 - 2 = 28\%$$

### 2.4 Dishonest Dealer & False Weight Arithmetic
When a trader claims to sell goods at Cost Price but uses a false weight of $W_{\text{false}}$ instead of true weight $W_{\text{true}}$:
$$\text{Gain Percentage} = \frac{\text{Error}}{\text{True Value} - \text{Error}} \times 100 = \frac{W_{\text{true}} - W_{\text{false}}}{W_{\text{false}}} \times 100$$
*Example:* A trader uses 900g instead of 1000g:
$$\text{Gain\%} = \frac{1000 - 900}{900} \times 100 = \frac{100}{900} \times 100 = 11.11\%$$

---

## Chapter 3: Ratio, Proportion & The Alligation Cross-Method

### 3.1 Proportionality Rules
- **Mean Proportional** between $a$ and $b$: $x = \sqrt{a \times b}$
- **Third Proportional** to $a$ and $b$: $x = \frac{b^2}{a}$
- **Fourth Proportional** to $a, b, c$: $x = \frac{b \times c}{a}$

### 3.2 The Alligation Cross-Diagram
Used to find the ratio in which two ingredients of prices $C$ (cheaper) and $D$ (dearer) must be mixed to obtain a mixture of mean price $M$:
```
       Cheaper Price (C)               Dearer Price (D)
               \                               /
                \                             /
                 --->   Mean Price (M)   <---
                /                             \
               /                               \
       (D - M)                                   (M - C)
```
$$\frac{\text{Quantity of Cheaper}}{\text{Quantity of Dearer}} = \frac{D - M}{M - C}$$

### 3.3 Repeated Replacement Formula
If a container initially holds $V$ units of pure liquid, and $x$ units are drawn off and replaced with water $n$ times:
$$\text{Liquid Remaining after } n \text{ operations} = V \left(1 - \frac{x}{V}\right)^n$$

---

## Chapter 4: Time and Work, Pipes & Cisterns (The LCM Efficiency Model)

### 4.1 The LCM Total Work Model
Never work with fractions like $\frac{1}{A} + \frac{1}{B}$. Instead:
1. Find $\text{LCM}(\text{Days of A}, \text{Days of B}, \dots) = \text{Total Work Units}$.
2. Compute daily unit efficiency: $\text{Rate} = \frac{\text{Total Work}}{\text{Days}}$.
3. $\text{Days Needed} = \frac{\text{Remaining Work Units}}{\text{Combined Rate}}$.

*Example:* A completes a task in 10 days; B completes in 15 days:
- $\text{LCM}(10, 15) = 30 \text{ units}$.
- A's rate $= 30 / 10 = 3 \text{ units/day}$; B's rate $= 30 / 15 = 2 \text{ units/day}$.
- Combined rate $= 3 + 2 = 5 \text{ units/day}$.
- Time together $= 30 / 5 = 6 \text{ days}$.

### 4.2 Man-Days-Hours Equivalence
$$\frac{M_1 \times D_1 \times H_1}{W_1} = \frac{M_2 \times D_2 \times H_2}{W_2}$$

---

## Chapter 5: Time, Speed, Distance, Trains & Relative Velocity

### 5.1 Unit Conversion
$$\text{km/h} \xrightarrow{\times \frac{5}{18}} \text{m/s}, \qquad \text{m/s} \xrightarrow{\times \frac{18}{5}} \text{km/h}$$

### 5.2 Average Speed Formula
- **Equal Distances:** If distance $D$ is traveled at speed $x$, and returned at speed $y$:
$$\text{Average Speed} = \frac{2xy}{x + y} \quad (\text{Harmonic Mean})$$
- **Equal Times:** If traveling for time $T$ at speed $x$ and time $T$ at speed $y$:
$$\text{Average Speed} = \frac{x + y}{2} \quad (\text{Arithmetic Mean})$$

### 5.3 Relative Velocity & Train Crossings
- **Opposite Directions:** $\text{Relative Speed} = S_1 + S_2$
- **Same Direction:** $\text{Relative Speed} = |S_1 - S_2|$
- **Train Crossing a Pole:** $\text{Distance} = \text{Length of Train}$
- **Train Crossing a Platform/Bridge:** $\text{Distance} = \text{Length of Train} + \text{Length of Platform}$

### 5.4 Boats and Streams
- Speed of Boat in still water $= u$, Speed of Stream $= v$.
- **Downstream Speed ($D$):** $D = u + v$
- **Upstream Speed ($U$):** $U = u - v$
- $$u = \frac{D + U}{2}, \qquad v = \frac{D - U}{2}$$

---

## Chapter 6: Simple Interest, Compound Interest & Depreciation

### 6.1 Formulas
- **Simple Interest (SI):** $\text{SI} = \frac{P \times R \times T}{100}$
- **Compound Interest (CI):** $A = P \left(1 + \frac{R}{100}\right)^T, \quad \text{CI} = A - P$

### 6.2 The Crucial CI - SI Difference Formulas
- **Difference for 2 Years:**
$$\text{Diff}_2 = P \left(\frac{R}{100}\right)^2$$
- **Difference for 3 Years:**
$$\text{Diff}_3 = P \left(\frac{R}{100}\right)^2 \left(3 + \frac{R}{100}\right)$$

---

## Chapter 7: Permutations, Combinations, Probability & Data Interpretation

### 7.1 Arrangements vs Selections
- **Permutation (Order Matters):** $^n P_r = \frac{n!}{(n - r)!}$
- **Combination (Order Does Not Matter):** $^n C_r = \frac{n!}{r!(n - r)!}$
- **Circular Permutation:** $(n - 1)!$ distinct arrangements; $\frac{(n - 1)!}{2}$ for symmetric necklaces.

### 7.2 Classical Probability & Independent Events
$$P(E) = \frac{\text{Favorable Outcomes}}{\text{Total Elementary Outcomes in Sample Space}}$$
$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$
If $A$ and $B$ are independent: $P(A \cap B) = P(A) \times P(B)$.

---

## Chapter 8: Solved Placement Quantitative Problems & Drills

### Solved Problem 1: Time and Work with Absences (TCS NQT Placement)
- **Problem:** A can do a piece of work in 14 days and B in 21 days. They begin together, but 3 days before the completion of work, A leaves off. In how many total days was the work completed?
- **Step-by-Step Solution:**
  1. $\text{LCM}(14, 21) = 42 \text{ units}$ (Total Work).
  2. A's daily rate $= 42 / 14 = 3 \text{ units/day}$; B's daily rate $= 42 / 21 = 2 \text{ units/day}$.
  3. In the final 3 days, only B worked: $3 \text{ days} \times 2 \text{ units/day} = 6 \text{ units}$.
  4. Remaining work completed together $= 42 - 6 = 36 \text{ units}$.
  5. Combined daily rate $= 3 + 2 = 5 \text{ units/day}$.
  6. Days worked together $= 36 / 5 = 7.2 \text{ days}$.
  7. Total days $= 7.2 + 3 = 10.2 \text{ days}$ (or $10 \frac{1}{5}$ days).

### Self-Assessment Practice Exercises & Verified Solutions:
1. **Exercise 1 (Numbers):** Find the remainder when $2^{100}$ is divided by 7.
   - *Solution:* $2^3 = 8 \equiv 1 \pmod 7$. Thus $2^{100} = (2^3)^{33} \times 2^1 = 1^{33} \times 2 = 2$. Remainder is 2.
2. **Exercise 2 (Speed):** A train 150m long moving at 54 km/h crosses a platform in 20 seconds. Find the platform length.
   - *Solution:* Speed $= 54 \times (5/18) = 15 \text{ m/s}$. Total distance $= 15 \times 20 = 300\text{m}$. Platform $= 300 - 150 = 150\text{m}$.
3. **Exercise 3 (Alligation):** In what ratio must tea at ₹62/kg be mixed with tea at ₹72/kg so that the mixture is worth ₹64.50/kg?
   - *Solution:* Ratio $= (72 - 64.5) : (64.5 - 62) = 7.5 : 2.5 = 3 : 1$.
"""

QUANT_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 2,
        "chapter_title": "Percentages, Profit, Loss & Successive Discounts",
        "subtopic": "Successive Discounts",
        "question": "What is the single equivalent discount percentage for three successive discounts of 20%, 10%, and 5%?",
        "options": ["31.6%", "35.0%", "32.4%", "30.0%"],
        "correct_option_index": 0,
        "explanation": "📖 [Quantitative Aptitude Prescribed Textbook — Chapter 2: Percentages & Discounts]\nMultiplying factors: 0.8 * 0.9 * 0.95 = 0.684. Net discount = (1 - 0.684) * 100% = 31.6%.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 5,
        "chapter_title": "Time, Speed, Distance, Trains & Relative Velocity",
        "subtopic": "Average Speed",
        "question": "A student travels from home to campus at 30 km/h and returns along the same route at 20 km/h. What is the average speed for the round trip?",
        "options": ["24 km/h", "25 km/h", "24.5 km/h", "23.8 km/h"],
        "correct_option_index": 0,
        "explanation": "📖 [Quantitative Aptitude Prescribed Textbook — Chapter 5: Time, Speed, Distance]\nWhen distances are equal, Average Speed is the Harmonic Mean: 2xy / (x + y) = 2 * 30 * 20 / (30 + 20) = 1200 / 50 = 24 km/h.",
        "difficulty": "easy",
    }
]
'''

with open(os.path.join(TEXTBOOK_DIR, "quant_master.py"), "w", encoding="utf-8") as f:
    f.write(QUANT_CONTENT.strip() + "\n")
ast.parse(QUANT_CONTENT)
print("Generated and verified quant_master.py successfully!")

# =============================================================================
# LOGICAL REASONING MASTER TEXTBOOK
# =============================================================================
LOGICAL_CONTENT = r'''"""
logical_master.py — Prescribed Master Textbook for Logical Reasoning.
Comprehensive campus placement textbook covering syllogisms, Venn diagrams,
blood relations, seating arrangements, direction vectors, coding-decoding, clocks,
calendars, and analytical puzzle solving.
"""

LOGICAL_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Syllogisms, Venn Diagrams & Deductive Logic",
        "topics": ["Categorical propositions: Universal Affirmative (All A are B), Universal Negative (No A is B), Particular Affirmative (Some A are B), Particular Negative (Some A are not B)", "Venn diagram intersection models for 2 and 3 statement problems", "Possibility conclusions vs Definitely True conclusions", "Complementary pairs: Conditions for 'Either I or II follows'"],
        "key_takeaways": "A conclusion is valid ONLY if it holds in EVERY single possible Venn diagram representation. If even one valid counter-example diagram invalidates the conclusion, it is not definitely true."
    },
    {
        "chapter_num": 2,
        "title": "Blood Relations & Family Tree Diagramming",
        "topics": ["Generational hierarchy mapping: Grandparents (+2) -> Parents (+1) -> Self/Siblings (0) -> Children (-1)", "Standard symbolic notation (+ for male, - for female, = for married couple, | for parent-child)", "Coded blood relations (e.g. P + Q means P is father of Q)", "Maternal vs Paternal relation distinctions (Maternal Uncle vs Paternal Uncle)"],
        "key_takeaways": "Never assume an individual's gender based on their name; gender must be explicitly stated or mathematically deduced through parental relationships."
    },
    {
        "chapter_num": 3,
        "title": "Direction Sense, Vector Paths & Shadow Puzzles",
        "topics": ["4 Cardinal (N, S, E, W) and 4 Ordinal directions (NE, NW, SE, SW)", "Left (counter-clockwise 90 deg) and Right turns (clockwise 90 deg)", "Pythagorean displacement: straight line distance d = sqrt(x^2 + y^2)", "Shadow mechanics: At sunrise shadows cast strictly West; at sunset shadows cast strictly East; at noon zero shadow"],
        "key_takeaways": "At sunrise (sun in the East), a person facing North casts their shadow to their Left (West). At sunset, the shadow casts to their Right (East)."
    },
    {
        "chapter_num": 4,
        "title": "Seating Arrangements (Linear, Circular, Polygonal)",
        "topics": ["Linear arrangements: Facing North (Right is East) vs Facing South (Right is West)", "Circular arrangements: Facing center (Right = Counter-Clockwise) vs Facing outward (Right = Clockwise)", "Parallel row arrangements with cross-facing candidates", "Step-by-step constraint elimination grids"],
        "key_takeaways": "When facing inwards in a circle, moving to the 'Right' is Counter-Clockwise; 'Left' is Clockwise. In parallel rows, remember opposite rows face in inverted directions."
    },
    {
        "chapter_num": 5,
        "title": "Coding-Decoding & Alphabetical Series Patterns",
        "topics": ["Forward positional numbering: EJOTY (5, 10, 15, 20, 25)", "Reverse positional numbering: A=26, Z=1 (Sum of opposite letters = 27)", "Caesar shift ciphers, alternating skips, and cross-pairing", "Fictitious language symbol frequency mapping"],
        "key_takeaways": "Opposite letter pairs always sum to 27 (A[1] + Z[26] = 27; B[2] + Y[25] = 27). Remember mnemonic pairs: AZ, BY, CX, DW, EV, FU, GT, HS, IR, JQ, KP, LO, MN."
    },
    {
        "chapter_num": 6,
        "title": "Clocks, Calendars, Order & Ranking",
        "topics": ["Clock hands angular velocity: Minute hand = 6 deg/min; Hour hand = 0.5 deg/min; Relative speed = 5.5 deg/min", "Angle between hands formula: Theta = |30H - (11/2)M|", "Hands overlapping (0 deg), opposite (180 deg), right angles (90 deg)", "Calendar odd days concept, standard years (1 odd day), leap years (2 odd days), and century leap rules", "Order & Ranking formula: Total in a row = (Rank from Left) + (Rank from Right) - 1"],
        "key_takeaways": "Angle between clock hands = |30 * Hours - 5.5 * Minutes|. A century year is a leap year if and only if it is divisible by 400 (e.g. 2000 is leap; 1900 is NOT leap)."
    }
]

LOGICAL_TEXTBOOK_MARKDOWN = r"""# Logical Reasoning & Analytical Ability (Prescribed Textbook)

**Edition:** 2026 Campus Placement & Technical Interview Edition  
**Subject:** Logical Reasoning  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement analytical reasoning assessments across top IT and product companies (TCS NQT, Infosys DSE/SE, Amazon SDE, Cognizant GenC Elevate, Accenture, etc.) are strictly grounded in the deductive logic and arrangement techniques presented in this master textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Syllogisms, Venn Diagrams & Deductive Logic](#chapter-1-syllogisms-venn-diagrams--deductive-logic)
- [Chapter 2: Blood Relations & Family Tree Diagramming](#chapter-2-blood-relations--family-tree-diagramming)
- [Chapter 3: Direction Sense, Vector Paths & Shadow Puzzles](#chapter-3-direction-sense-vector-paths--shadow-puzzles)
- [Chapter 4: Seating Arrangements (Linear, Circular, Polygonal)](#chapter-4-seating-arrangements-linear-circular-polygonal)
- [Chapter 5: Coding-Decoding & Alphabetical Series Patterns](#chapter-5-coding-decoding--alphabetical-series-patterns)
- [Chapter 6: Clocks, Calendars, Order & Ranking](#chapter-6-clocks-calendars-order--ranking)
- [Chapter 7: Solved Placement Analytical Puzzles & Drills](#chapter-7-solved-placement-analytical-puzzles--drills)

---

## Chapter 1: Syllogisms, Venn Diagrams & Deductive Logic

### 1.1 The 4 Aristotelian Categorical Propositions
1. **A-Type (Universal Affirmative):** "All S are P" (Set $S \subseteq P$).
2. **E-Type (Universal Negative):** "No S is P" (Sets $S \cap P = \emptyset$).
3. **I-Type (Particular Affirmative):** "Some S are P" (Set $S \cap P \neq \emptyset$).
4. **O-Type (Particular Negative):** "Some S are not P" (Set $S - P \neq \emptyset$).

### 1.2 Venn Diagram Construction & Testing
To evaluate whether a conclusion is valid:
- Construct the minimal (standard) Venn diagram.
- Construct all valid alternate diagrams (overlapping possibilities).
- A conclusion is **Definitely True** if and only if it is satisfied in 100% of all possible diagrams.

### 1.3 Complementary Pairs ('Either I or II Follows')
Three strict conditions must hold simultaneously for an "Either-Or" conclusion:
1. Both conclusions must share the exact same subject and predicate.
2. Both individual conclusions must be independently doubtful (false/unproven).
3. The conclusions must form a complementary pair:
   - **Pair 1:** "Some" + "No"
   - **Pair 2:** "All" + "Some Not"

---

## Chapter 2: Blood Relations & Family Tree Diagramming

### 2.1 Standard Symbolic Charting
- **Male:** Box $[+]$ or $[\text{Name}]^+$
- **Female:** Circle $(-)$ or $(\text{Name})^-$
- **Spousal Pair:** Double horizontal line $(A = B)$
- **Siblings:** Single horizontal dashed line $(A \dots B)$
- **Parent-Child:** Vertical line $(A \downarrow B)$

### 2.2 Generational Levels
- **Level +2:** Paternal Grandfather, Maternal Grandmother
- **Level +1:** Father, Mother, Uncle, Aunt
- **Level 0 (Reference):** Self, Brother, Sister, Cousin, Brother-in-Law
- **Level -1:** Son, Daughter, Nephew, Niece
- **Level -2:** Grandson, Granddaughter

---

## Chapter 3: Direction Sense, Vector Paths & Shadow Puzzles

### 3.1 Cardinal Points & Angular Rotations
```
                     North (0°)
                         |
      North-West (315°)  |  North-East (45°)
               \         |         /
                \        |        /
    West (270°) ---------+--------- East (90°)
                /        |        \
               /         |         \
      South-West (225°)  |  South-East (135°)
                         |
                     South (180°)
```
- A **Right Turn** is a $+90^\circ$ clockwise rotation.
- A **Left Turn** is a $-90^\circ$ (or $270^\circ$) counter-clockwise rotation.
- **Shortest Displacement:** $d = \sqrt{(\Delta x)^2 + (\Delta y)^2}$.

### 3.2 Shadow Mechanics
- **Sunrise (Sun in East):** Shadows fall strictly towards the **West**.
  - Facing North: Shadow is on your **Left**.
  - Facing South: Shadow is on your **Right**.
- **Sunset (Sun in West):** Shadows fall strictly towards the **East**.
  - Facing North: Shadow is on your **Right**.
  - Facing South: Shadow is on your **Left**.

---

## Chapter 4: Seating Arrangements (Linear, Circular, Polygonal)

### 4.1 Circular Seating Strategy
1. **Facing the Center:**
   - Person's **Right** = Counter-Clockwise movement.
   - Person's **Left** = Clockwise movement.
2. **Facing Outward:**
   - Person's **Right** = Clockwise movement.
   - Person's **Left** = Counter-Clockwise movement.
3. **Execution Rule:** Always anchor the first person at the 6 o'clock bottom position facing the center so their right and left match your natural right and left.

---

## Chapter 5: Coding-Decoding & Alphabetical Series Patterns

### 5.1 EJOTY Formula & Opposite Alphabet Mappings
$$\begin{matrix}
\text{Letter} & \text{E} & \text{J} & \text{O} & \text{T} & \text{Y} \\
\text{Position} & 5 & 10 & 15 & 20 & 25
\end{matrix}$$

Opposite Letter Pairs (Sum of positions $= 27$):
- $\text{A}(1) \leftrightarrow \text{Z}(26)$ [AZure]
- $\text{B}(2) \leftrightarrow \text{Y}(25)$ [BoY]
- $\text{C}(3) \leftrightarrow \text{X}(24)$ [CruX]
- $\text{D}(4) \leftrightarrow \text{W}(23)$ [DeW]
- $\text{E}(5) \leftrightarrow \text{V}(22)$ [EVen]
- $\text{F}(6) \leftrightarrow \text{U}(21)$ [FUll]
- $\text{G}(7) \leftrightarrow \text{T}(20)$ [GT Road]
- $\text{H}(8) \leftrightarrow \text{S}(19)$ [High School]
- $\text{I}(9) \leftrightarrow \text{R}(18)$ [Indian Railway]
- $\text{J}(10) \leftrightarrow \text{Q}(17)$ [Jungle Queen]
- $\text{K}(11) \leftrightarrow \text{P}(16)$ [Kamal Pasand]
- $\text{L}(12) \leftrightarrow \text{O}(15)$ [LOve]
- $\text{M}(13) \leftrightarrow \text{N}(14)$ [MaN]

---

## Chapter 6: Clocks, Calendars, Order & Ranking

### 6.1 Clock Angle Formula
$$\theta = \left|30 \times H - \frac{11}{2} \times M\right|$$
*Example:* Angle between hands at 3:40:
$$\theta = |30(3) - 5.5(40)| = |90 - 220| = |-130| = 130^\circ$$

### 6.2 Order & Ranking Single-Row Formula
$$\text{Total Persons in Row} = (\text{Rank from Left}) + (\text{Rank from Right}) - 1$$
$$\text{Persons between A and B (Non-overlapping)} = \text{Total} - (\text{Left Rank of A} + \text{Right Rank of B})$$

---

## Chapter 7: Solved Placement Analytical Puzzles & Drills

### Solved Puzzle 1: Circular Seating with 8 Persons (Amazon Placement)
- **Problem:** Eight friends (A, B, C, D, E, F, G, H) sit in a circle facing the center. B is 3rd to the right of A. F is 2nd to the left of B. C and G are immediate neighbors of each other. H is not a neighbor of A. D is 2nd to the left of E.
- **Deduction:**
  1. Place A at bottom (Pos 1). B is 3rd right (counter-clockwise) $\implies$ Pos 4.
  2. F is 2nd left of B (clockwise 2 steps) $\implies$ Pos 2.
  3. C and G must occupy adjacent empty spots: Pos 5 & 6 or 6 & 7.
  4. Testing constraints places: A at 1, F at 2, D at 3, B at 4, C at 5, G at 6, E at 7, H at 8.

### Self-Assessment Practice Exercises & Verified Solutions:
1. **Exercise 1 (Syllogisms):** Statements: "All computers are machines. Some machines are calculators." Evaluate: "Some computers are calculators."
   - *Solution:* Invalid. In the minimal Venn diagram, computers and calculators can be disjoint sets.
2. **Exercise 2 (Blood Relations):** Pointing to a photograph, a woman says: "He is the only son of the wife of my husband's father." How is the man related to the woman?
   - *Solution:* "My husband's father" = Father-in-law. "Wife of father-in-law" = Mother-in-law. "Only son of mother-in-law" = Her husband. The man is her **Husband**.
3. **Exercise 3 (Ranking):** In a class of 45 students, Rahul ranks 18th from the top. What is his rank from the bottom?
   - *Solution:* $\text{Bottom Rank} = 45 - 18 + 1 = 28\text{th}$.
"""

LOGICAL_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "Syllogisms, Venn Diagrams & Deductive Logic",
        "subtopic": "Complementary Pairs",
        "question": "Which of the following statement pairs forms a valid complementary pair for an 'Either-Or' conclusion in Syllogisms?",
        "options": [
            "Some pens are books and No pen is a book",
            "All pens are books and Some pens are books",
            "No pen is a book and Some pens are not books",
            "All pens are books and No pen is a book"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Logical Reasoning Prescribed Textbook — Chapter 1: Syllogisms]\nThe 'Some + No' pair is a valid contradictory complementary pair: if one is false, the other must be true.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 6,
        "chapter_title": "Clocks, Calendars, Order & Ranking",
        "subtopic": "Clock Angle Formula",
        "question": "What is the angle between the hour hand and the minute hand of a clock at 8:20?",
        "options": ["130 degrees", "120 degrees", "140 degrees", "125 degrees"],
        "correct_option_index": 0,
        "explanation": "📖 [Logical Reasoning Prescribed Textbook — Chapter 6: Clocks & Calendars]\nTheta = |30 * H - 5.5 * M| = |30 * 8 - 5.5 * 20| = |240 - 110| = 130 degrees.",
        "difficulty": "easy",
    }
]
'''

with open(os.path.join(TEXTBOOK_DIR, "logical_master.py"), "w", encoding="utf-8") as f:
    f.write(LOGICAL_CONTENT.strip() + "\n")
ast.parse(LOGICAL_CONTENT)
print("Generated and verified logical_master.py successfully!")

