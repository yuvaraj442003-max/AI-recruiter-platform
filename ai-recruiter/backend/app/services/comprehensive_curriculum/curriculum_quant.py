"""
curriculum_quant.py - 8 Comprehensive Chapters for Quantitative Aptitude & Numerical Ability.
"""
from typing import List, Dict, Any

QUANT_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Number Systems, Divisibility Rules & Remainder Theorems",
        "key_takeaways": "Master unit digit cycles, divisibility tests (2-19), Euler's Totient function, Fermat's Little Theorem, and Chinese Remainder Theorem.",
        "topics": [
            "Classification of numbers: Natural, Whole, Integers, Rational, Prime, Co-prime",
            "Divisibility rules for composite numbers (Coprime factorization: 6, 12, 72, 88, 99)",
            "Unit digit calculation and cyclicity (Powers of 2, 3, 7, 8 have cyclicity 4)",
            "Remainder Theorems: Remainder of sum/product, Fermat's Little Theorem, Euler's Theorem",
            "Trailing zeroes calculation in factorials via Legendre's Formula"
        ],
        "sections": {
            "concept": """Number Systems form the foundation of corporate aptitude exams (TCS NQT, Infosys, Cognizant, Wipro, Accenture).

**Cyclicity of Unit Digits:**
When positive integers are raised to powers, their unit digits repeat periodically:
- Numbers ending in 0, 1, 5, 6 maintain identical unit digits for all powers (cyclicity 1).
- Numbers ending in 4, 9 repeat every 2 powers (cyclicity 2).
- Numbers ending in 2, 3, 7, 8 repeat every 4 powers (cyclicity 4). To find the unit digit of $x^n$, compute $n \\pmod 4$.

**Trailing Zeroes in Factorials:**
A trailing zero is formed by the product of $2 \\times 5$. In any factorial $n!$, prime factor 2 occurs far more frequently than 5. Hence, the number of trailing zeroes equals the exponent of prime factor 5 in $n!$, calculated via **Legendre's Formula**:
$$E_5(n!) = \\lfloor n/5 \\rfloor + \\lfloor n/25 \\rfloor + \\lfloor n/125 \\rfloor + \\dots$$""",
            "formulas": """1. **Fermat's Little Theorem:**
   $$\\text{If } p \\text{ is prime and } \\gcd(a, p) = 1 \implies a^{p-1} \\equiv 1 \\pmod p$$
2. **Euler's Totient Theorem:**
   $$a^{\\phi(m)} \\equiv 1 \\pmod m \\quad \\text{where } \\phi(m) = m \\prod_{p|m} \\left(1 - \\frac{1}{p}\\right)$$
3. **Legendre's Trailing Zeroes Formula:**
   $$Z(n!) = \\sum_{k=1}^\infty \\left\\lfloor \\frac{n}{5^k} \\right\\rfloor$$""",
            "solved_examples": [
                {
                    "title": "Finding Trailing Zeroes in 100! (Legendre's Formula)",
                    "difficulty": "Easy | TCS NQT, Infosys, Wipro",
                    "problem": "Calculate the exact number of trailing zeroes in 100!.",
                    "step_by_step": [
                        "Step 1: Divide 100 by successive powers of 5: 5, 25, 125...",
                        "Step 2: $\\lfloor 100 / 5 \\rfloor = 20$.",
                        "Step 3: $\\lfloor 100 / 25 \\rfloor = 4$.",
                        "Step 4: $\\lfloor 100 / 125 \\rfloor = 0$.",
                        "Step 5: Total trailing zeroes $= 20 + 4 = 24$ zeroes."
                    ],
                    "code_or_math": """# Python verification of Legendre's Formula
def trailing_zeroes(n):
    count = 0
    power_of_5 = 5
    while n >= power_of_5:
        count += n // power_of_5
        power_of_5 *= 5
    return count

print(trailing_zeroes(100)) # Output: 24""",
                    "explanation": "Every multiple of 5 contributes one factor of 5; multiples of 25 contribute a second factor of 5. Summing gives exactly 24 zeroes."
                },
                {
                    "title": "Finding the Remainder of 7^100 divided by 101",
                    "difficulty": "Medium | Cognizant, Accenture",
                    "problem": "Find the remainder when $7^{100}$ is divided by 101.",
                    "step_by_step": [
                        "Step 1: Check if divisor 101 is prime: 101 is prime.",
                        "Step 2: Check if $\\gcd(7, 101) = 1$: Yes, 7 and 101 are coprime.",
                        "Step 3: Apply Fermat's Little Theorem: $a^{p-1} \\equiv 1 \\pmod p$ for prime $p$.",
                        "Step 4: Here $a = 7, p = 101 \implies 7^{101 - 1} = 7^{100} \\equiv 1 \\pmod{101}$.",
                        "Step 5: Remainder $= 1$."
                    ],
                    "code_or_math": """# Python pow(base, exp, mod) verification:
print(pow(7, 100, 101)) # Output: 1""",
                    "explanation": "Fermat's Little Theorem solves high-exponent prime modulo queries in seconds without heavy arithmetic."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the unit digit of $3^{65} \\times 6^{59} \\times 7^{71}$?",
                    "options": ["A) 1", "B) 2", "C) 4", "D) 6"],
                    "correct_answer": "C) 4",
                    "detailed_solution": "Unit digit of $3^{65} = 3^{65 \\pmod 4} = 3^1 = 3$. Unit digit of $6^{59} = 6$. Unit digit of $7^{71} = 7^{71 \\pmod 4} = 7^3 = 343 \implies 3$. Product of unit digits $= 3 \\times 6 \\times 3 = 54 \implies 4$."
                }
            ],
            "interview_questions": [
                {
                    "company": "TCS Digital",
                    "question": "How do you test if a very large number is divisible by 72 without performing long division?",
                    "model_answer": "Factorize 72 into its coprime factors: $72 = 8 \\times 9$ (since $\\gcd(8, 9) = 1$). A number is divisible by 72 if and only if it is simultaneously divisible by both 8 and 9. 1) Test for 8: The last three digits of the number must be divisible by 8. 2) Test for 9: The sum of all digits must be divisible by 9.",
                    "interviewer_tip": "Always decompose composite divisors into coprime factors."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Percentages, Profit, Loss & Discount",
        "key_takeaways": "Master fraction-percentage equivalents, multiplying factors, successive percentage changes, and marked price discount formulas.",
        "topics": [
            "Fraction to percentage conversion table (1/2 through 1/16)",
            "Percentage increase/decrease and Multiplying Factors (MF)",
            "Successive percentage change formula: a + b + (ab/100)",
            "Profit, Loss, Cost Price (CP), Selling Price (SP), Marked Price (MP), and Discount",
            "Dishonest dealer / false weights problems"
        ],
        "sections": {
            "concept": """Percentages express numbers as fractions of 100. Rapid mental conversion between fractions and percentages is the single most valuable speed tool in corporate placement tests:
- $1/2 = 50\\%$, $1/3 = 33.33\\%$, $1/4 = 25\\%$, $1/5 = 20\\%$, $1/6 = 16.67\\%$, $1/7 = 14.28\\%$, $1/8 = 12.5\\%$, $1/9 = 11.11\\%$, $1/11 = 9.09\\%$, $1/12 = 8.33\\%$.

**Multiplying Factor (MF):**
- A $20\\%$ increase means $MF = 1 + 0.20 = 1.20$.
- A $15\\%$ decrease means $MF = 1 - 0.15 = 0.85$.
New Value $= \\text{Old Value} \\times MF$.

**Profit & Loss Framework:**
- Profit $\% = \\frac{SP - CP}{CP} \\times 100$. (Profit/Loss is always calculated on CP unless stated otherwise).
- Discount $\% = \\frac{MP - SP}{MP} \\times 100$. (Discount is always calculated on Marked Price).""",
            "formulas": """1. **Successive Percentage Change:**
   $$\\text{Net Change}\\% = a + b + \\frac{a \\times b}{100}$$
2. **Profit & Discount Relationship:**
   $$\\frac{MP}{CP} = \\frac{100 + \\text{Profit}\\%}{100 - \\text{Discount}\\%}$$""",
            "solved_examples": [
                {
                    "title": "Calculating Net Discount from Successive Discounts",
                    "difficulty": "Easy | Infosys, TCS, Wipro",
                    "problem": "An item is offered with successive discounts of 20% and 10%. Find the single equivalent discount.",
                    "step_by_step": [
                        "Step 1: Discounts are negative percentage changes: $a = -20, b = -10$.",
                        "Step 2: Apply formula: $\\text{Net} = (-20) + (-10) + \\frac{(-20)(-10)}{100}$.",
                        "Step 3: $\\text{Net} = -30 + \\frac{200}{100} = -30 + 2 = -28\\%$.",
                        "Step 4: Equivalent single discount is 28%."
                    ],
                    "code_or_math": """// Successive Discount Formula:
// Net Discount = 20 + 10 - (20 * 10) / 100 = 28%""",
                    "explanation": "Demonstrates why successive discounts cannot simply be added together ($20 + 10 \ne 30$)."
                }
            ],
            "practice_questions": [
                {
                    "question": "A trader marks goods 40% above Cost Price and allows a 20% discount. What is his profit percentage?",
                    "options": ["A) 12%", "B) 15%", "C) 20%", "D) 8%"],
                    "correct_answer": "A) 12%",
                    "detailed_solution": "Using successive changes $a = +40, b = -20$: $\\text{Profit}\\% = 40 - 20 + \\frac{40(-20)}{100} = 20 - 8 = 12\\%$."
                }
            ],
            "interview_questions": [
                {
                    "company": "Accenture",
                    "question": "A dishonest grocer sells rice at cost price, but uses a false weight of 900g instead of 1kg. What is his profit percentage?",
                    "model_answer": "Profit occurs because the dealer charges for 1000g while delivering only 900g of goods. The cost to the dealer is 900g, while his revenue corresponds to 1000g. $\\text{Profit}\\% = \\frac{\\text{True Weight} - \\text{False Weight}}{\\text{False Weight}} \\times 100 = \\frac{1000 - 900}{900} \\times 100 = \\frac{100}{900} \\times 100 = \\frac{1}{9} \\times 100 = 11.11\\%$.",
                    "interviewer_tip": "Remember that the denominator is the actual weight dispensed (900g), not the claimed weight."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Simple & Compound Interest",
        "key_takeaways": "Master Simple Interest, Compound Interest, semi-annual compounding, difference between CI and SI for 2 and 3 years, and rule of 72.",
        "topics": [
            "Simple Interest (SI) formula: SI = (P * R * T) / 100",
            "Compound Interest (CI) compounding frequencies: Annual, Semi-annual, Quarterly",
            "Difference between CI and SI for 2 years: P * (R/100)^2",
            "Difference between CI and SI for 3 years: P * (R/100)^2 * (3 + R/100)",
            "Rule of 72 for estimating investment doubling time"
        ],
        "sections": {
            "concept": """Interest is the charge for borrowing capital:
- **Simple Interest (SI):** Calculated strictly on the initial principal $P$ across all periods. Interest earned each year remains constant.
- **Compound Interest (CI):** Interest earned in each period is added to the principal, earning interest on interest in subsequent periods ('exponential growth').
- **Compounding Frequency:** If interest compounds semi-annually, rate becomes $R/2$ and time periods double ($2T$). If quarterly, rate becomes $R/4$ and periods become $4T$.""",
            "formulas": """1. **Compound Interest Amount:**
   $$A = P \\left(1 + \\frac{R}{100}\\right)^T, \\quad CI = A - P$$
2. **Difference between CI and SI for 2 Years:**
   $$D_2 = CI_2 - SI_2 = P \\left(\\frac{R}{100}\\right)^2$$
3. **Difference between CI and SI for 3 Years:**
   $$D_3 = CI_3 - SI_3 = P \\left(\\frac{R}{100}\\right)^2 \\left(3 + \\frac{R}{100}\\right)$$""",
            "solved_examples": [
                {
                    "title": "Finding Principal from CI - SI Difference for 2 Years",
                    "difficulty": "Easy | TCS, Cognizant, Wipro",
                    "problem": "The difference between CI and SI on a sum of money for 2 years at 10% per annum is $45. Find the principal.",
                    "step_by_step": [
                        "Step 1: Formula for 2-year difference: $D_2 = P \\times (R / 100)^2$.",
                        "Step 2: $45 = P \\times (10 / 100)^2 = P \\times (1 / 10)^2 = P \\times (1 / 100)$.",
                        "Step 3: $P = 45 \\times 100 = \\$4500$."
                    ],
                    "code_or_math": """// Calculation:
// P = D2 / (R/100)^2 = 45 / (0.10)^2 = 45 / 0.01 = $4500""",
                    "explanation": "Direct application of the 2-year CI-SI difference formula avoids computing both interests independently."
                }
            ],
            "practice_questions": [
                {
                    "question": "A sum of money doubles itself in 5 years at simple interest. In how many years will it become 4 times itself?",
                    "options": ["A) 10 years", "B) 15 years", "C) 20 years", "D) 12 years"],
                    "correct_answer": "B) 15 years",
                    "detailed_solution": "Doubling means SI = $P$ in 5 years. Becoming 4 times means SI = $3P$. Since SI grows linearly, time required $= 3 \\times 5 = 15$ years."
                }
            ],
            "interview_questions": [
                {
                    "company": "Goldman Sachs",
                    "question": "What is the Rule of 72 and how accurate is it?",
                    "model_answer": "The Rule of 72 is a mental shortcut to estimate the number of years required for an investment to double at a constant annual compound interest rate $R$: $\\text{Years to Double} \\approx 72 / R$. For example, at an $8\\%$ interest rate, money doubles in approx $72 / 8 = 9$ years. It derives from the natural logarithm $\\ln(2) \\approx 0.693$, adjusted upwards to 72 because 72 has numerous small divisors (2, 3, 4, 6, 8, 9, 12). It is highly accurate for interest rates between $4\\%$ and $12\\%$.",
                    "interviewer_tip": "Connect 72 to $\\ln(2) \\approx 0.693$."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Ratio, Proportion & Mixtures / Alligations",
        "key_takeaways": "Master compound ratios, mean proportional, Rule of Alligation, and repeated replacement formula for liquids.",
        "topics": [
            "Ratio properties: Invertendo, Alternando, Componendo and Dividendo",
            "Mean proportional, third proportional, and fourth proportional",
            "Rule of Alligation: Cross-method for determining mixing ratios",
            "Removal and replacement of liquids formula: Residual = Initial * (1 - x/V)^n",
            "Partnership profit sharing based on Capital * Time investment"
        ],
        "sections": {
            "concept": """Ratios compare relative magnitudes of quantities of identical dimension.

**Rule of Alligation:**
A graphical cross-method to find the ratio in which two ingredients of differing prices (Cheaper $C$ and Dearer $D$) must be mixed to produce a mixture of intermediate mean price $M$:
$$\\frac{\\text{Quantity of Cheaper}}{\\text{Quantity of Dearer}} = \\frac{D - M}{M - C}$$

**Repeated Replacement Formula:**
A vessel contains $V$ units of pure liquid. If $x$ units are withdrawn and replaced with water $n$ times repeatedly, the quantity of pure liquid remaining is:
$$\\text{Residual Liquid} = V \\left(1 - \\frac{x}{V}\\right)^n$$""",
            "formulas": """1. **Rule of Alligation Cross Ratio:**
   $$\\frac{Q_C}{Q_D} = \\frac{\\text{Price}_D - \\text{Price}_M}{\\text{Price}_M - \\text{Price}_C}$$
2. **Liquid Replacement Formula:**
   $$Q_{\\text{final}} = Q_{\\text{initial}} \\left(1 - \\frac{x}{V}\\right)^n$$""",
            "solved_examples": [
                {
                    "title": "Applying Alligation to Find Mixing Ratio",
                    "difficulty": "Easy | TCS, Infosys, Cognizant",
                    "problem": "In what ratio must tea costing $60/kg be mixed with tea costing $75/kg so that the resulting mixture is worth $65/kg?",
                    "step_by_step": [
                        "Step 1: Cheaper price $C = 60$, Dearer price $D = 75$, Mean price $M = 65$.",
                        "Step 2: $D - M = 75 - 65 = 10$.",
                        "Step 3: $M - C = 65 - 60 = 5$.",
                        "Step 4: Ratio of Cheaper to Dearer $= (D - M) / (M - C) = 10 / 5 = 2 : 1$."
                    ],
                    "code_or_math": """// Alligation Cross-Subtraction:
// Cheaper (60)         Dearer (75)
//              Mean (65)
// (75 - 65) = 10       (65 - 60) = 5
// Ratio = 10 : 5 = 2 : 1""",
                    "explanation": "Mixing 2 parts of $60 tea with 1 part of $75 tea produces an exact blend value of $65."
                }
            ],
            "practice_questions": [
                {
                    "question": "A container has 40 litres of milk. 4 litres are drawn out and replaced by water. This process is repeated 2 more times. How much milk remains?",
                    "options": ["A) 29.16 litres", "B) 30.5 litres", "C) 28.0 litres", "D) 32.4 litres"],
                    "correct_answer": "A) 29.16 litres",
                    "detailed_solution": "Total operations $n = 3$. Remaining $= 40 \\times (1 - 4/40)^3 = 40 \\times (9/10)^3 = 40 \\times (729 / 1000) = 29.16$ litres."
                }
            ],
            "interview_questions": [
                {
                    "company": "Infosys",
                    "question": "A and B invest in a business in ratio 3:2. If 5% of total profit goes to charity and A's share is $855, find total profit.",
                    "model_answer": "Let total profit be $P$. Charity takes 5%, so remaining profit $= 0.95P$. A's share is $3/5$ of remaining profit: $\\frac{3}{5} \\times 0.95P = 855 \implies 0.57P = 855 \implies P = 855 / 0.57 = \\$1500$.",
                    "interviewer_tip": "Multiply investment ratios by operational duration."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Time, Speed, Distance & Relative Motion",
        "key_takeaways": "Master km/h to m/s conversion, Average Speed harmonic mean, Relative Speed in same vs opposite directions, Trains, and Boats & Streams.",
        "topics": [
            "Unit conversion factor: 1 km/h = 5/18 m/s, 1 m/s = 18/5 km/h",
            "Average Speed for equal distances: 2xy / (x + y)",
            "Relative Speed: (u - v) in same direction, (u + v) in opposite directions",
            "Problems on Trains: Crossing a stationary point vs crossing a platform/bridge of length L",
            "Boats and Streams: Upstream (u - v) vs Downstream (u + v) and still water speed"
        ],
        "sections": {
            "concept": """Time, Speed, and Distance relates physical motion: $\\text{Distance} = \\text{Speed} \\times \\text{Time}$.

**Average Speed:**
If an object covers equal distances at speeds $x$ and $y$, the average speed is NOT the arithmetic mean $(x + y)/2$; it is the **Harmonic Mean**:
$$\\text{Average Speed} = \\frac{2xy}{x + y}$$

**Relative Speed:**
When two objects move simultaneously:
- **Opposite Directions (Towards or Away):** Relative Speed $= u + v$ (velocities add).
- **Same Direction:** Relative Speed $= |u - v|$ (velocities subtract).

**Boats and Streams:**
Let speed of boat in still water $= u$, and speed of stream $= v$:
- Downstream Speed $S_d = u + v$.
- Upstream Speed $S_u = u - v$.
- Still water speed $u = \\frac{S_d + S_u}{2}$, Stream speed $v = \\frac{S_d - S_u}{2}$.""",
            "formulas": """1. **Harmonic Mean Average Speed:**
   $$\\text{Avg Speed} = \\frac{2xy}{x + y} \\quad \\text{(for equal distance traveled at } x \\text{ and } y)$$
2. **Train Crossing Platform:**
   $$T = \\frac{\\text{Length}_{\\text{train}} + \\text{Length}_{\\text{platform}}}{\\text{Speed}_{\\text{train}}}$$""",
            "solved_examples": [
                {
                    "title": "Train Crossing a Platform",
                    "difficulty": "Easy | TCS, Wipro, Infosys",
                    "problem": "A train 150m long moving at 54 km/h crosses a platform in 20 seconds. Find the length of the platform.",
                    "step_by_step": [
                        "Step 1: Convert speed to m/s: $54 \\times (5/18) = 15$ m/s.",
                        "Step 2: Total distance covered $= \\text{Speed} \\times \\text{Time} = 15 \\times 20 = 300$ meters.",
                        "Step 3: Distance $= \\text{Length}_{\\text{train}} + \\text{Length}_{\\text{platform}}$.",
                        "Step 4: $300 = 150 + L_{\\text{platform}} \implies L_{\\text{platform}} = 150$ meters."
                    ],
                    "code_or_math": """// Calculation:
// Speed = 54 * (5/18) = 15 m/s
// Total Distance = 15 * 20 = 300 m
// Platform Length = 300 - 150 = 150 m""",
                    "explanation": "When crossing an object with physical dimension, the train must cover its own length plus the object's length."
                }
            ],
            "practice_questions": [
                {
                    "question": "A man travels from home to office at 30 km/h and returns at 20 km/h. What is his average speed for the whole journey?",
                    "options": ["A) 25 km/h", "B) 24 km/h", "C) 22.5 km/h", "D) 26 km/h"],
                    "correct_answer": "B) 24 km/h",
                    "detailed_solution": "Using Harmonic Mean: $2 \\times 30 \\times 20 / (30 + 20) = 1200 / 50 = 24$ km/h."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "A boat travels 24 km upstream and 28 km downstream in 6 hours total. In 14 hours it can travel 30 km upstream and 21 km downstream. Find the speed of the boat in still water.",
                    "model_answer": "Let $1/u = x$ and $1/v = y$ where $u = \\text{upstream}$ and $v = \\text{downstream}$. $24x + 28y = 6$ and $30x + 21y = 14$ (or similar system). Solving gives Upstream speed $S_u = 6$ km/h and Downstream speed $S_d = 14$ km/h. Boat speed in still water $= (S_d + S_u) / 2 = (14 + 6) / 2 = 10$ km/h.",
                    "interviewer_tip": "Substitute $1/S_u$ and $1/S_d$ with variables $x$ and $y$ to solve as linear equations."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Time and Work, Pipes & Cisterns",
        "key_takeaways": "Master individual work rates, the LCM Method for total work units, efficiency ratios, and inlet/outlet pipe calculations.",
        "topics": [
            "Unitary method: If A does work in n days, 1 day work = 1/n",
            "The LCM Method: Defining Total Work as LCM of given times",
            "Efficiency ratios: Inverse relationship between Time and Efficiency",
            "Alternate days work patterns and work with leaving/joining workers",
            "Pipes and Cisterns: Inlets (positive work) vs Outlets/Leaks (negative work)"
        ],
        "sections": {
            "concept": """Time and Work problems are solved using two primary methods:
1. **Fractional / Unitary Method:** If worker A finishes a job in $n$ days, A's 1-day work rate is $\\frac{1}{n}$.
2. **LCM Method (Faster for Placement Tests):**
   Assume total work is the Least Common Multiple (LCM) of all individual days.
   $$\\text{Efficiency (Units/Day)} = \\frac{\\text{Total Work Units}}{\\text{Days Taken}}$$
   Summing efficiencies gives combined daily output.

**Pipes and Cisterns:**
Analogous to work problems, with the addition of **Negative Work**:
- Inlet pipes perform positive work ($+E$).
- Outlet pipes or leaks drain water and perform negative work ($-E$).""",
            "formulas": """1. **Work Invariant:**
   $$\\text{Total Work} = \\text{Efficiency} \\times \\text{Time}$$
2. **Pipes and Cisterns Net Efficiency:**
   $$E_{\\text{net}} = E_{\\text{inlet}} - E_{\\text{leak}}$$""",
            "solved_examples": [
                {
                    "title": "Solving Combined Work via the LCM Method",
                    "difficulty": "Easy | TCS, Infosys, Cognizant",
                    "problem": "A can finish a task in 12 days and B in 15 days. They work together for 4 days, then A leaves. In how many more days will B finish the remaining work?",
                    "step_by_step": [
                        "Step 1: Find Total Work = $\\text{LCM}(12, 15) = 60$ units.",
                        "Step 2: Calculate daily efficiencies: A does $60/12 = 5$ units/day; B does $60/15 = 4$ units/day.",
                        "Step 3: Together they do $5 + 4 = 9$ units/day. In 4 days they complete $4 \\times 9 = 36$ units.",
                        "Step 4: Remaining work $= 60 - 36 = 24$ units.",
                        "Step 5: B completes remaining work at 4 units/day: $24 / 4 = 6$ days."
                    ],
                    "code_or_math": """// LCM Method:
// Total Work = 60 units
// Eff(A) = 5, Eff(B) = 4
// 4 days * 9 units = 36 units completed
// Remaining = 24 units -> Time for B = 24 / 4 = 6 days""",
                    "explanation": "Using integer units via LCM eliminates messy fraction additions."
                }
            ],
            "practice_questions": [
                {
                    "question": "Pipe A fills a tank in 6 hours, while Pipe B empties it in 8 hours. If both are opened together, in how many hours will the tank fill?",
                    "options": ["A) 24 hours", "B) 14 hours", "C) 12 hours", "D) 48 hours"],
                    "correct_answer": "A) 24 hours",
                    "detailed_solution": "LCM(6, 8) = 24 units. A fills +4 units/hr, B empties -3 units/hr. Net filling = +1 unit/hr. Time = 24 / 1 = 24 hours."
                }
            ],
            "interview_questions": [
                {
                    "company": "Cognizant",
                    "question": "A is twice as efficient as B and takes 30 days less than B to complete a job. In how many days can they finish it together?",
                    "model_answer": "Efficiency ratio $E_A : E_B = 2 : 1$. Since time is inversely proportional to efficiency, Time ratio $T_A : T_B = 1 : 2$. Difference in time $= 2x - 1x = x = 30$ days. Hence, A takes 30 days and B takes 60 days. Total work $= \\text{LCM}(30, 60) = 60$ units. Combined efficiency $= 2 + 1 = 3$ units/day. Time working together $= 60 / 3 = 20$ days.",
                    "interviewer_tip": "Invert efficiency ratios to find time ratios."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Permutations, Combinations & Probability",
        "key_takeaways": "Master Fundamental Principles of Counting, nPr vs nCr, circular permutations, probability axioms, and Bayes' Theorem.",
        "topics": [
            "Fundamental Principle of Multiplication (AND) and Addition (OR)",
            "Permutations (Arrangements: nPr) vs Combinations (Selections: nCr)",
            "Permutations with identical items: n! / (p! * q! * r!)",
            "Circular permutations: (n - 1)! for distinct objects, (n - 1)! / 2 for necklaces",
            "Probability: Independent events, Conditional probability P(A|B), and Bayes' Theorem"
        ],
        "sections": {
            "concept": """Combinatorics and Probability quantify counting and chance:
- **Permutation ($^nP_r$):** Order matters (e.g., arrangements, rankings, codes).
- **Combination ($^nC_r$):** Order does NOT matter (e.g., committees, team selections).
- **Conditional Probability:** The likelihood of event $A$ occurring given that event $B$ has already occurred:
  $$P(A|B) = \\frac{P(A \\cap B)}{P(B)}$$
- **Bayes' Theorem:** Calculates updated posterior probability given new observed evidence.""",
            "formulas": """1. **Permutation & Combination:**
   $$^nP_r = \\frac{n!}{(n - r)!}, \\quad ^nC_r = \\frac{n!}{r!(n - r)!}$$
2. **Bayes' Theorem:**
   $$P(A_i|B) = \\frac{P(A_i) \\cdot P(B|A_i)}{\\sum_{j} P(A_j) \\cdot P(B|A_j)}$$""",
            "solved_examples": [
                {
                    "title": "Forming Committees with Combinations",
                    "difficulty": "Easy | Amazon, TCS, Infosys",
                    "problem": "In how many ways can a team of 4 members be selected from 6 men and 4 women such that the team contains at least 2 women?",
                    "step_by_step": [
                        "Step 1: Case 1 (2 women, 2 men): $^4C_2 \\times ^6C_2 = 6 \\times 15 = 90$.",
                        "Step 2: Case 2 (3 women, 1 man): $^4C_3 \\times ^6C_1 = 4 \\times 6 = 24$.",
                        "Step 3: Case 3 (4 women, 0 men): $^4C_4 \\times ^6C_0 = 1 \\times 1 = 1$.",
                        "Step 4: Total ways $= 90 + 24 + 1 = 115$ ways."
                    ],
                    "code_or_math": """import math

# Combination helper
def nCr(n, r):
    return math.comb(n, r)

total = nCr(4,2)*nCr(6,2) + nCr(4,3)*nCr(6,1) + nCr(4,4)*nCr(6,0)
print(total) # 115""",
                    "explanation": "Partitioning 'at least' conditions into disjoint cases guarantees exhaustive and mutually exclusive counting."
                }
            ],
            "practice_questions": [
                {
                    "question": "In how many distinct ways can the letters of the word 'MATHEMATICS' be arranged?",
                    "options": [
                        "A) 11!",
                        "B) 11! / (2! * 2! * 2!)",
                        "C) 11! / 2!",
                        "D) 10!"
                    ],
                    "correct_answer": "B) 11! / (2! * 2! * 2!)",
                    "detailed_solution": "Total 11 letters with repeats: M occurs 2 times, A occurs 2 times, T occurs 2 times. Formula $= 11! / (2! \\times 2! \\times 2!) = 4,989,600$."
                }
            ],
            "interview_questions": [
                {
                    "company": "Goldman Sachs",
                    "question": "You roll two fair six-sided dice. What is the probability that the sum of the dice is 7 given that at least one die shows a 2?",
                    "model_answer": "Total sample space with two dice $= 36$ outcomes. Let event $B$ = 'at least one die shows a 2'. Outcomes in $B$: $(2,1), (2,2), \dots, (2,6)$ (6 outcomes) and $(1,2), (3,2), \dots, (6,2)$ (5 more outcomes), so $|B| = 11$. Event $A$ = 'sum is 7'. The outcomes having sum 7 that also contain a 2 are: $(2, 5)$ and $(5, 2)$ ($2$ outcomes). Therefore, $P(A|B) = \\frac{|A \\cap B|}{|B|} = \\frac{2}{11}$.",
                    "interviewer_tip": "Remember to eliminate duplicate counts like $(2,2)$ when calculating condition $|B|$."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Mensuration, Geometry & Data Interpretation",
        "key_takeaways": "Master 2D areas/perimeters, 3D volumes/surface areas, circle sector properties, and Data Interpretation (Tables, Bar graphs, Pie charts).",
        "topics": [
            "2D Mensuration: Triangle (Heron's), Quadrilaterals, Rhombus, Trapezium, Circles",
            "3D Mensuration: Cubes, Cylinders, Cones, Spheres, Hemispheres (Surface area & Volume)",
            "Similar triangles and Pythagoras theorem applications",
            "Data Interpretation: Tables, Bar Charts, Line Graphs, Pie Charts",
            "Speed calculation tricks: Percentage increases and ratio approximations in DI"
        ],
        "sections": {
            "concept": """Mensuration and Geometry quantify spatial properties of shapes:
- **Circle:** Area $= \\pi r^2$, Circumference $= 2\\pi r$.
- **Cylinder:** Curved Surface Area $= 2\\pi rh$, Total Surface Area $= 2\\pi r(r + h)$, Volume $= \\pi r^2 h$.
- **Cone:** Slant height $l = \\sqrt{r^2 + h^2}$, CSA $= \\pi r l$, Volume $= \\frac{1}{3}\\pi r^2 h$.
- **Sphere:** Surface Area $= 4\\pi r^2$, Volume $= \\frac{4}{3}\\pi r^3$.

**Data Interpretation (DI):**
DI evaluates the candidate's speed in interpreting business data across Bar Graphs, Pie Charts, and Tables. Critical placement DI speed tip: **in a Pie Chart, $100\\% = 360^\\circ$**, so $1\\% = 3.6^\\circ$.""",
            "formulas": """1. **Heron's Formula:**
   $$\\text{Area} = \\sqrt{s(s - a)(s - b)(s - c)} \\quad \\text{where } s = \\frac{a + b + c}{2}$$
2. **Pie Chart Degree-to-Percentage Conversion:**
   $$\\text{Percentage}\\% = \\frac{\\text{Degrees}}{360^\\circ} \\times 100$$""",
            "solved_examples": [
                {
                    "title": "Sphere Melted and Recast into Cones",
                    "difficulty": "Easy | TCS, Infosys, Wipro",
                    "problem": "A solid metallic sphere of radius 6cm is melted and recast into small cones each of radius 2cm and height 3cm. Find the number of cones formed.",
                    "step_by_step": [
                        "Step 1: Volume remains conserved: $\\text{Volume}_{\\text{sphere}} = n \\times \\text{Volume}_{\\text{cone}}$.",
                        "Step 2: $\\text{Vol}_{\\text{sphere}} = \\frac{4}{3} \\pi (6)^3 = \\frac{4}{3} \\pi (216) = 288\\pi$.",
                        "Step 3: $\\text{Vol}_{\\text{cone}} = \\frac{1}{3} \\pi (2)^2 (3) = 4\\pi$.",
                        "Step 4: Number of cones $n = 288\\pi / 4\\pi = 72$ cones."
                    ],
                    "code_or_math": """// Volume conservation:
// n = Vol(Sphere) / Vol(Cone)
// n = ((4/3) * pi * 6^3) / ((1/3) * pi * 2^2 * 3) = 288 / 4 = 72""",
                    "explanation": "Because mass is conserved during melting, equating volumes directly determines object counts."
                }
            ],
            "practice_questions": [
                {
                    "question": "If the radius of a cylinder is doubled and height is halved, what happens to its volume?",
                    "options": ["A) Halved", "B) Doubled", "C) Remains unchanged", "D) Quadrupled"],
                    "correct_answer": "B) Doubled",
                    "detailed_solution": "Original volume $= \\pi r^2 h$. New volume $= \\pi (2r)^2 (h/2) = \\pi (4r^2) (h/2) = 2\\pi r^2 h$, which is double the original."
                }
            ],
            "interview_questions": [
                {
                    "company": "TCS Digital",
                    "question": "How do you rapidly calculate the percentage contribution of a sector in a Pie Chart without using a calculator?",
                    "model_answer": "Use standard anchor degree equivalents: $36^\\circ = 10\\%$, $18^\\circ = 5\\%$, $3.6^\\circ = 1\\%$, and $72^\\circ = 20\\%$. For any given angle, decompose it into these anchor blocks (e.g., $54^\\circ = 36^\\circ + 18^\\circ = 10\\% + 5\\% = 15\\%$). This delivers instant mental calculations during speed tests.",
                    "interviewer_tip": "Demonstrate the $36^\\circ = 10\\%$ anchor rule."
                }
            ]
        }
    }
]
