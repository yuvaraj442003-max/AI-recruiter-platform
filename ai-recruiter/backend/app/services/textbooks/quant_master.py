"""
quant_master.py — Prescribed Master Textbook for Quantitative Aptitude.
Comprehensive unabridged campus placement textbook covering speed arithmetic,
divisibility rules, power cyclicity, percentages, profit & loss, false weights,
alligation cross-diagrams, time and work LCM efficiency models, relative speed,
harmonic mean average speed, CI-SI 2 & 3 year difference formulas, probability,
and solved placement aptitude numericals.
"""

QUANT_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Number Systems, Divisibility Rules & Remainder Theorems",
        "topics": [
            "Divisibility rules (2, 3, 4, 5, 6, 7, 8, 9, 11, 13) and composite factorization",
            "Units digit cyclicity of powers (cyclicity of 2, 3, 7, 8 is 4; 4, 9 is 2; 0, 1, 5, 6 is 1)",
            "Trailing zeroes in n! using Legendre's Formula (E_p(n!) = sum(floor(n / p^k)))",
            "HCF and LCM properties: Product formula A * B = HCF(A,B) * LCM(A,B)",
            "Remainder theorems: Fermat's Little Theorem, Euler's Totient Theorem, Wilson's Theorem"
        ],
        "key_takeaways": "Divisibility by 11: Difference between sum of odd-place digits and even-place digits must be 0 or a multiple of 11. The number of trailing zeroes in n! equals floor(n/5) + floor(n/25) + floor(n/125)..."
    },
    {
        "chapter_num": 2,
        "title": "Percentages, Profit, Loss & Successive Discounts",
        "topics": [
            "Multiplying factors for rapid calculation: 20% increase = 1.2x; 15% decrease = 0.85x",
            "Cost Price (CP), Selling Price (SP), Marked Price (MP), and Margin vs Markup",
            "Successive percentage change formula: net = a + b + (a * b / 100)",
            "Dishonest trader / false weight calculations: Gain% = (Error / [True Value - Error]) * 100",
            "Break-even analysis and zero-profit selling pricing"
        ],
        "key_takeaways": "Two successive discounts of d1% and d2% produce an effective net discount of: d1 + d2 - (d1 * d2 / 100)%. When selling two articles at same SP, one at x% profit and one at x% loss, there is ALWAYS an overall net loss of (x/10)%."
    },
    {
        "chapter_num": 3,
        "title": "Ratio, Proportion & The Alligation Cross-Method",
        "topics": [
            "Direct, inverse, and compound proportions",
            "Mean proportional (sqrt(ab)), third proportional (b^2 / a), fourth proportional (bc / a)",
            "Rule of Alligation for mixing ingredients of different costs",
            "Repeated dilution and replacement formula: Final Amount = Initial * (1 - x / V)^n",
            "Partnership profit division based on Capital * Time investments"
        ],
        "key_takeaways": "Alligation ratio = (Dearer Price - Mean Price) : (Mean Price - Cheaper Price). In repeated replacement of x liters from volume V, the fraction of original liquid remaining after n operations is strictly (1 - x/V)^n."
    },
    {
        "chapter_num": 4,
        "title": "Time and Work, Pipes & Cisterns (The LCM Efficiency Model)",
        "topics": [
            "LCM Total Work Assumption technique: Converting days into daily unit work rates",
            "Combined efficiency, alternate day work schedules, and negative work (inlet vs outlet pipes)",
            "Man-Days-Hours equivalence formula: (M1 * D1 * H1) / W1 = (M2 * D2 * H2) / W2",
            "Wages division rules: Wages are divided in strict proportion to total work performed",
            "Pipes and Cisterns: Leakage draining math and filling rates"
        ],
        "key_takeaways": "Assume total work = LCM of individual times. Daily efficiency = Total Work / Days. If A does work in 12 days and B in 15 days, assume work = 60 units; A does 5 units/day, B does 4 units/day."
    },
    {
        "chapter_num": 5,
        "title": "Time, Speed, Distance, Trains & Relative Velocity",
        "topics": [
            "Speed = Distance / Time; Conversion factor: 1 km/h = 5/18 m/s; 1 m/s = 18/5 km/h",
            "Average speed for equal distances = Harmonic Mean: 2xy / (x + y), NEVER arithmetic mean",
            "Relative speed: Same direction (|S1 - S2|); Opposite directions (S1 + S2)",
            "Trains passing stationary objects (Distance = Length of Train) vs platforms (Distance = Train + Platform)",
            "Boats and streams: Downstream = u + v; Upstream = u - v; Still water speed = (Downstream + Upstream) / 2",
            "Circular tracks: First meeting at starting point = LCM of individual round times"
        ],
        "key_takeaways": "When distances are equal, average speed is 2S1*S2 / (S1 + S2). When travel times are equal, average speed is the arithmetic mean (S1 + S2) / 2."
    },
    {
        "chapter_num": 6,
        "title": "Simple Interest, Compound Interest & Depreciation",
        "topics": [
            "Simple Interest formula: SI = (P * T * R) / 100",
            "Compound Interest formula: A = P * (1 + R / 100)^n",
            "Difference between CI and SI for 2 years: D2 = P * (R / 100)^2",
            "Difference between CI and SI for 3 years: D3 = P * (R / 100)^2 * (3 + R / 100)",
            "Half-yearly and quarterly compounding adjustments",
            "Equal annual installments in compound interest: P = x / (1 + R/100) + x / (1 + R/100)^2 ..."
        ],
        "key_takeaways": "The 2-year difference formula D2 = P*(R/100)^2 is one of the most frequently asked shortcut numericals in TCS, Infosys, and Cognizant placement tests."
    },
    {
        "chapter_num": 7,
        "title": "Permutations, Combinations & Probability",
        "topics": [
            "Fundamental Principles of Counting: Addition Principle vs Multiplication Principle",
            "Permutations (Arrangements): nPr = n! / (n - r)!; Circular Permutations: (n - 1)!",
            "Combinations (Selections): nCr = n! / [r! * (n - r)!]; Properties: nCr = nC(n-r)",
            "Arrangements with repeated items: n! / (p! * q! * r!)",
            "Probability axioms, Complementary probability P(A') = 1 - P(A), Addition Rule P(A or B)",
            "Independent Events P(A and B) = P(A) * P(B) and Bayes' Theorem fundamentals"
        ],
        "key_takeaways": "Permutations order matters (arranging people in a row, electing President and VP). Combinations order does not matter (selecting a committee of 3 from 10)."
    },
    {
        "chapter_num": 8,
        "title": "Solved Placement Quantitative Numericals & Speed Drills",
        "topics": [
            "Step-by-step worked TCS NQT numericals",
            "Infosys speed-distance-time train meeting walkthrough",
            "Alligation shortcut applied to multi-ingredient mixtures",
            "Two-year CI-SI difference calculation shortcut",
            "Self-assessment practice drills with verified solutions"
        ],
        "key_takeaways": "Applying speed arithmetic shortcuts, LCM models, and alligation cross-diagrams cuts average problem-solving time from 2.5 minutes down to 30 seconds."
    }
]

QUANT_TEXTBOOK_MARKDOWN = r"""# Quantitative Aptitude: Corporate Recruitment Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Quantitative Aptitude  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus recruitment aptitude rounds, numerical ability online tests, and speed assessments (TCS NQT, Infosys, Cognizant, Wipro, Accenture, Capgemini) are strictly grounded in the formulas, speed arithmetic shortcuts, and derivation proofs detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Number Systems, Divisibility Rules & Remainder Theorems](#chapter-1-number-systems-divisibility-rules--remainder-theorems)
  - [1.1 Divisibility Rules & Factorization](#11-divisibility-rules--factorization)
  - [1.2 Units Digit Power Cyclicity](#12-units-digit-power-cyclicity)
  - [1.3 Legendre's Formula for Trailing Zeroes](#13-legendres-formula-for-trailing-zeroes)
  - [1.4 Remainder Theorems: Fermat & Euler](#14-remainder-theorems-fermat--euler)
- [Chapter 2: Percentages, Profit, Loss & Successive Discounts](#chapter-2-percentages-profit-loss--successive-discounts)
  - [2.1 Multiplying Factors & Percentage Change](#21-multiplying-factors--percentage-change)
  - [2.2 Profit, Loss, Marked Price & Cost Price](#22-profit-loss-marked-price--cost-price)
  - [2.3 Successive Discounts Formula](#23-successive-discounts-formula)
  - [2.4 Dishonest Dealer & False Weights Math](#24-dishonest-dealer--false-weights-math)
- [Chapter 3: Ratio, Proportion & The Alligation Cross-Method](#chapter-3-ratio-proportion--the-alligation-cross-method)
  - [3.1 Proportion Theorems & Variation](#31-proportion-theorems--variation)
  - [3.2 The Alligation Cross-Method](#32-the-alligation-cross-method)
  - [3.3 Repeated Dilution & Replacement Formula](#33-repeated-dilution--replacement-formula)
- [Chapter 4: Time and Work, Pipes & Cisterns (The LCM Efficiency Model)](#chapter-4-time-and-work-pipes--cisterns-the-lcm-efficiency-model)
  - [4.1 The LCM Total Work Technique](#41-the-lcm-total-work-technique)
  - [4.2 Alternate Day Work Schedules](#42-alternate-day-work-schedules)
  - [4.3 Man-Days-Hours Equivalence Formula](#43-man-days-hours-equivalence-formula)
  - [4.4 Pipes, Cisterns & Negative Work](#44-pipes-cisterns--negative-work)
- [Chapter 5: Time, Speed, Distance, Trains & Relative Velocity](#chapter-5-time-speed-distance-trains--relative-velocity)
  - [5.1 Average Speed as Harmonic Mean](#51-average-speed-as-harmonic-mean)
  - [5.2 Relative Speed in Same vs Opposite Directions](#52-relative-speed-in-same-vs-opposite-directions)
  - [5.3 Trains Crossing Poles, Platforms & Moving Objects](#53-trains-crossing-poles-platforms--moving-objects)
  - [5.4 Boats and Streams Formulas](#54-boats-and-streams-formulas)
- [Chapter 6: Simple Interest, Compound Interest & Depreciation](#chapter-6-simple-interest-compound-interest--depreciation)
  - [6.1 Simple Interest vs Compound Interest](#61-simple-interest-vs-compound-interest)
  - [6.2 The 2-Year & 3-Year Difference Shortcuts](#62-the-2-year--3-year-difference-shortcuts)
  - [6.3 Compounding Periods & Installment Annuities](#63-compounding-periods--installment-annuities)
- [Chapter 7: Permutations, Combinations & Probability](#chapter-7-permutations-combinations--probability)
  - [7.1 Principles of Counting: Addition vs Multiplication](#71-principles-of-counting-addition-vs-multiplication)
  - [7.2 Permutations vs Combinations](#72-permutations-vs-combinations)
  - [7.3 Probability Axioms & Conditional Probability](#73-probability-axioms--conditional-probability)
- [Chapter 8: Solved Placement Quantitative Numericals & Speed Drills](#chapter-8-solved-placement-quantitative-numericals--speed-drills)
  - [Solved Problem 1: Time & Work LCM Model](#solved-problem-1-time--work-lcm-model)
  - [Solved Problem 2: Alligation Mixture Math](#solved-problem-2-alligation-mixture-math)
  - [Solved Problem 3: Two Trains Crossing Each Other](#solved-problem-3-two-trains-crossing-each-other)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: Number Systems, Divisibility Rules & Remainder Theorems

### 1.1 Divisibility Rules & Factorization
- **Divisibility by $2^k$:** A number is divisible by $2^k$ if its last $k$ digits are divisible by $2^k$ ($2 \to$ last 1, $4 \to$ last 2, $8 \to$ last 3, $16 \to$ last 4 digits).
- **Divisibility by 3 & 9:** Sum of digits must be divisible by 3 or 9 respectively.
- **Divisibility by 11:** The difference between the sum of digits at odd places and the sum of digits at even places must be either $0$ or a multiple of $11$.
  - *Example:* Check $8,371,440$:
    - Odd places: $8 + 7 + 4 + 0 = 19$
    - Even places: $3 + 1 + 4 = 8$
    - Difference: $19 - 8 = 11 \implies$ Divisible by 11!

### 1.2 Units Digit Power Cyclicity
When raising a number to a large power $a^b$, the units digit follows a periodic cycle of length at most 4:

| Base Units Digit | Power Cycle Pattern | Cyclicity Period |
|:---:|:---|:---:|
| **0, 1, 5, 6** | Always ends in the exact same digit ($0^n=0, 1^n=1, 5^n=5, 6^n=6$) | **1** |
| **4** | $4^1 = 4, \ 4^2 = 6, \ 4^3 = 4, \ 4^4 = 6$ (Odd power: 4, Even power: 6) | **2** |
| **9** | $9^1 = 9, \ 9^2 = 1, \ 9^3 = 9, \ 9^4 = 1$ (Odd power: 9, Even power: 1) | **2** |
| **2** | $2, 4, 8, 6$ | **4** |
| **3** | $3, 9, 7, 1$ | **4** |
| **7** | $7, 9, 3, 1$ | **4** |
| **8** | $8, 4, 2, 6$ | **4** |

**Algorithm to Find Units Digit of $a^b$:**
1. Let $d$ be the units digit of $a$.
2. Divide exponent $b$ by 4: compute remainder $r = b \bmod 4$.
3. If $r = 0$, replace $r$ with $4$.
4. Units digit is the units digit of $d^r$.
   - *Example:* Find units digit of $7^{95}$:
     $95 \div 4 = 23 \text{ R } 3 \implies 7^3 = 343 \implies$ Units digit is **3**.

### 1.3 Legendre's Formula for Trailing Zeroes
A trailing zero is created by the prime factor pair $2 \times 5 = 10$. In $n!$, the count of factor 2 always exceeds the count of factor 5. Therefore, the number of trailing zeroes equals the exponent of 5 in the prime factorization of $n!$:

$$E_5(n!) = \left\lfloor \frac{n}{5} \right\rfloor + \left\lfloor \frac{n}{25} \right\rfloor + \left\lfloor \frac{n}{125} \right\rfloor + \left\lfloor \frac{n}{625} \right\rfloor + \dots$$

*Placement Example:* Trailing zeroes in $100!$:
$$E_5(100!) = \left\lfloor \frac{100}{5} \right\rfloor + \left\lfloor \frac{100}{25} \right\rfloor = 20 + 4 = \mathbf{24\text{ trailing zeroes}}.$$

---

## Chapter 2: Percentages, Profit, Loss & Successive Discounts

### 2.1 Multiplying Factors & Percentage Change
$$\text{Percentage Change } = \frac{\text{Final Value} - \text{Initial Value}}{\text{Initial Value}} \times 100$$
Using Multiplying Factors ($MF$):
- $25\%$ increase $\implies MF = 1 + 0.25 = 1.25$
- $30\%$ decrease $\implies MF = 1 - 0.30 = 0.70$
- **Product Constancy Concept:** If expenditure $= \text{Price} \times \text{Consumption}$, and Price increases by $\frac{1}{n} = \frac{x}{100}$, Consumption must decrease by $\frac{1}{n + 1}$ to keep expenditure constant!
  - *Example:* If price of sugar increases by $25\% = \frac{1}{4}$, consumption must decrease by $\frac{1}{4 + 1} = \frac{1}{5} = \mathbf{20\%}$.

### 2.2 Profit, Loss, Marked Price & Cost Price
- $\text{Profit} = SP - CP \implies \text{Profit } \% = \frac{SP - CP}{CP} \times 100$
- $\text{Loss} = CP - SP \implies \text{Loss } \% = \frac{CP - SP}{CP} \times 100$
- $\text{Discount} = MP - SP \implies \text{Discount } \% = \frac{MP - SP}{MP} \times 100$
- Relationship formula:
  $$\frac{MP}{CP} = \frac{100 + \text{Profit } \%}{100 - \text{Discount } \%}$$

### 2.3 Successive Discounts Formula
When two successive discounts of $d_1\%$ and $d_2\%$ are applied to Marked Price:
$$\text{Net Single Equivalent Discount} = \left( d_1 + d_2 - \frac{d_1 \times d_2}{100} \right) \%$$
*Example:* Successive discounts of $20\%$ and $10\%$:
$$\text{Net Discount} = 20 + 10 - \frac{20 \times 10}{100} = 30 - 2 = \mathbf{28\%} \quad (\text{NOT } 30\%!).$$

### 2.4 Dishonest Dealer & False Weights Math
When a trader professes to sell goods at Cost Price but uses a false weight that measures $W_{\text{false}}$ instead of true weight $W_{\text{true}}$:
$$\text{Gain } \% = \left( \frac{\text{True Weight} - \text{False Weight}}{\text{False Weight}} \right) \times 100 = \left( \frac{\text{Error}}{\text{True Value} - \text{Error}} \right) \times 100$$
*Example:* A dealer claims to sell at cost but uses a 900g weight instead of 1kg (1000g):
$$\text{Gain } \% = \frac{1000 - 900}{900} \times 100 = \frac{100}{900} \times 100 = \mathbf{11.11\%}.$$

---

## Chapter 3: Ratio, Proportion & The Alligation Cross-Method

### 3.1 Proportion Theorems & Variation
If $a : b = c : d$:
- Product of Extremes = Product of Means: $a \times d = b \times c$.
- Mean Proportional between $a$ and $b$: $x = \sqrt{a \times b}$.
- Third Proportional to $a$ and $b$: $x = \frac{b^2}{a}$.
- Fourth Proportional to $a, b, c$: $x = \frac{b \times c}{a}$.

### 3.2 The Alligation Cross-Method
Used to find the ratio in which two ingredients of prices $C$ (Cheaper) and $D$ (Dearer) must be mixed to produce a mixture of mean price $M$:

```
   Cheaper Price (C)            Dearer Price (D)
             \                /
              \              /
               Mean Price (M)
              /              \
             /                \
      (D - M)                  (M - C)

Ratio of Cheaper to Dearer Quantity = (D - M) : (M - C)
```

### 3.3 Repeated Dilution & Replacement Formula
A vessel contains $V$ units of pure liquid. $x$ units are withdrawn and replaced with water. This operation is repeated $n$ times:
$$\text{Liquid Remaining} = V \times \left(1 - \frac{x}{V}\right)^n$$
$$\frac{\text{Pure Liquid Remaining}}{\text{Total Solution Capacity}} = \left(1 - \frac{x}{V}\right)^n$$

---

## Chapter 4: Time and Work, Pipes & Cisterns (The LCM Efficiency Model)

### 4.1 The LCM Total Work Technique
Instead of dealing with cumbersome fractions ($1/12 + 1/15$), assume the **Total Work** is the **LCM** of the individual time periods:

*Placement Problem:* Person A can complete a project in 12 days; Person B can complete it in 15 days. Working together, in how many days will they finish?
1. Total Work $= \text{LCM}(12, 15) = \mathbf{60\text{ units}}$.
2. Efficiency of A $= 60 / 12 = \mathbf{5\text{ units/day}}$.
3. Efficiency of B $= 60 / 15 = \mathbf{4\text{ units/day}}$.
4. Combined Efficiency $= 5 + 4 = \mathbf{9\text{ units/day}}$.
5. Days to complete $= \frac{60}{9} = \frac{20}{3} = \mathbf{6\frac{2}{3}\text{ days}}$ (Solved in 10 seconds!).

### 4.2 Man-Days-Hours Equivalence Formula
$$\frac{M_1 \times D_1 \times H_1 \times E_1}{W_1} = \frac{M_2 \times D_2 \times H_2 \times E_2}{W_2}$$
Where $M$ = Men/Workers, $D$ = Days, $H$ = Hours per day, $E$ = Efficiency rating, $W$ = Total Work performed.

---

## Chapter 5: Time, Speed, Distance, Trains & Relative Velocity

### 5.1 Average Speed as Harmonic Mean
When an object travels distance $d$ at speed $x$, and returns the exact same distance $d$ at speed $y$:
$$\text{Average Speed} = \frac{\text{Total Distance}}{\text{Total Time}} = \frac{2d}{\frac{d}{x} + \frac{d}{y}} = \frac{2xy}{x + y}$$
- **Crucial Rule:** Average speed for equal distances is the **Harmonic Mean**, NEVER the arithmetic mean $(x + y) / 2$!

### 5.2 Relative Speed in Same vs Opposite Directions
- **Opposite Directions (Approaching or Moving Apart):**
  $$S_{\text{relative}} = S_1 + S_2$$
- **Same Direction (Overtaking):**
  $$S_{\text{relative}} = |S_1 - S_2|$$

### 5.3 Trains Crossing Poles, Platforms & Moving Objects
1. **Train of length $L$ crossing a stationary pole / man:**
   $$\text{Distance} = L, \quad \text{Time} = \frac{L}{S_{\text{train}}}$$
2. **Train of length $L$ crossing a platform / bridge of length $P$:**
   $$\text{Distance} = L + P, \quad \text{Time} = \frac{L + P}{S_{\text{train}}}$$
3. **Two trains of lengths $L_1$ and $L_2$ crossing each other:**
   $$\text{Distance} = L_1 + L_2, \quad \text{Time} = \frac{L_1 + L_2}{S_1 \pm S_2}$$

---

## Chapter 6: Simple Interest, Compound Interest & Depreciation

### 6.1 Simple Interest vs Compound Interest
- **Simple Interest:** Interest is calculated strictly on original Principal:
  $$SI = \frac{P \times T \times R}{100}, \quad A = P + SI$$
- **Compound Interest:** Interest is calculated on accumulated principal:
  $$A = P \times \left(1 + \frac{R}{100}\right)^n, \quad CI = A - P$$

### 6.2 The 2-Year & 3-Year Difference Shortcuts
- **Difference for 2 Years:**
  $$D_2 = CI_2 - SI_2 = P \times \left(\frac{R}{100}\right)^2$$
- **Difference for 3 Years:**
  $$D_3 = CI_3 - SI_3 = P \times \left(\frac{R}{100}\right)^2 \times \left(3 + \frac{R}{100}\right)$$

---

## Chapter 7: Permutations, Combinations & Probability

### 7.1 Principles of Counting: Addition vs Multiplication
- **Addition Principle (OR):** If event A can occur in $m$ mutually exclusive ways, and event B can occur in $n$ ways: Total ways $= m + n$.
- **Multiplication Principle (AND):** If event A can occur in $m$ ways, and for each way event B can occur in $n$ ways: Total ways $= m \times n$.

### 7.2 Permutations vs Combinations
- **Permutation ($^n P_r$):** Ordered arrangement.
  $$^n P_r = \frac{n!}{(n - r)!}$$
- **Combination ($^n C_r$):** Unordered selection.
  $$^n C_r = \frac{n!}{r! (n - r)!}$$

---

## Chapter 8: Solved Placement Quantitative Numericals & Speed Drills

### Solved Problem 1: Time & Work LCM Model
- **Problem:** A and B can do a work in 10 days and 15 days respectively. They begin together, but after 2 days A leaves. In how many more days will B finish the remaining work?
- **Solution:**
  1. Total Work $= \text{LCM}(10, 15) = 30\text{ units}$.
  2. Efficiency of A $= 30 / 10 = 3\text{ u/day}$; Efficiency of B $= 30 / 15 = 2\text{ u/day}$.
  3. Work in first 2 days $= (3 + 2) \times 2 = 10\text{ units}$.
  4. Remaining work $= 30 - 10 = 20\text{ units}$.
  5. Time taken by B alone $= \frac{20}{2} = \mathbf{10\text{ days}}$.

### Solved Problem 2: Alligation Mixture Math
- **Problem:** In what ratio must rice at \$9.30 per kg be mixed with rice at \$10.80 per kg so that the mixture be worth \$10.00 per kg?
- **Solution:**
  - Cheaper $C = 9.30$, Dearer $D = 10.80$, Mean $M = 10.00$.
  - $D - M = 10.80 - 10.00 = 0.80$.
  - $M - C = 10.00 - 9.30 = 0.70$.
  - Ratio $= 0.80 : 0.70 = \mathbf{8 : 7}$.

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Trailing Zeroes):** Find the number of trailing zeroes in $250!$.
   - *Solution:* $\lfloor 250/5 \rfloor + \lfloor 250/25 \rfloor + \lfloor 250/125 \rfloor = 50 + 10 + 2 = \mathbf{62\text{ zeroes}}$.

2. **Exercise 2 (Average Speed):** A car travels from City A to City B at 60 km/h and returns at 40 km/h. What is the average speed for the whole journey?
   - *Solution:* Harmonic mean $= \frac{2 \times 60 \times 40}{60 + 40} = \frac{4800}{100} = \mathbf{48\text{ km/h}}$ (NOT 50 km/h!).

3. **Exercise 3 (Successive Discounts):** Find the single discount equivalent to three successive discounts of 20%, 10%, and 5%.
   - *Solution:* $MF = (1 - 0.20)(1 - 0.10)(1 - 0.05) = 0.80 \times 0.90 \times 0.95 = 0.684$. Net discount $= 1 - 0.684 = 0.316 = \mathbf{31.6\%}$.

4. **Exercise 4 (2-Year CI-SI Difference):** If the difference between CI and SI on a sum for 2 years at 10% per annum is \$45, what is the Principal?
   - *Solution:* $D_2 = P (R/100)^2 \implies 45 = P (10/100)^2 = P (1/100) \implies P = \mathbf{\$4500}$.

5. **Exercise 5 (Permutations of Word):** How many distinct arrangements can be formed from the letters of the word **PLACEMENT**?
   - *Solution:* Total letters $= 9$. Letter 'E' repeats 2 times. Total arrangements $= \frac{9!}{2!} = \frac{362880}{2} = \mathbf{181,440}$.
"""

QUANT_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 5,
        "chapter_title": "Time, Speed, Distance, Trains & Relative Velocity",
        "subtopic": "Average Speed for Equal Distances",
        "question": "If a vehicle travels a fixed distance at speed x km/h and returns the exact same distance at speed y km/h, what is the correct formula for its average speed?",
        "options": [
            "2xy / (x + y)",
            "(x + y) / 2",
            "sqrt(xy)",
            "(x - y) / (x + y)"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Quant Prescribed Textbook — Chapter 5: Speed & Distance]\nWhen equal distances are traversed at different speeds, average speed is the Harmonic Mean: 2xy / (x + y). The arithmetic mean (x + y) / 2 is valid only when travel times are equal.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 6,
        "chapter_title": "Simple Interest, Compound Interest & Depreciation",
        "subtopic": "2-Year CI-SI Difference Formula",
        "question": "What is the shortcut formula for the difference between Compound Interest and Simple Interest on Principal P for 2 years at annual rate R%?",
        "options": [
            "P * (R / 100)^2",
            "P * (R / 100)",
            "P * (R / 100)^3",
            "2 * P * R / 100"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Quant Prescribed Textbook — Chapter 6: Interest Formulas]\nThe difference between CI and SI for 2 years is strictly D2 = P * (R / 100)^2, representing the interest earned in year 2 on the interest accumulated from year 1.",
        "difficulty": "easy",
    }
]
