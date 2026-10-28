"""
generate_logical_and_verbal.py - Generates comprehensive curricula for:
1. Logical Reasoning (8 chapters)
2. Verbal Ability (8 chapters)
"""
from pathlib import Path

CURRICULUM_DIR = Path(__file__).resolve().parent.parent / "backend" / "app" / "services" / "comprehensive_curriculum"
CURRICULUM_DIR.mkdir(parents=True, exist_ok=True)

def build_verbal_module():
    content = '''"""
curriculum_verbal.py - 8 Comprehensive Chapters for Verbal Ability & Corporate English.
"""
from typing import List, Dict, Any

VERBAL_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Advanced English Grammar & Sentence Correction",
        "key_takeaways": "Master Subject-Verb Agreement, Dangling Modifiers, Parallelism, Pronoun-Antecedent agreement, and conditional tenses.",
        "topics": [
            "Subject-Verb Agreement: Compound subjects, collective nouns, phrases intervening between subject and verb",
            "Dangling and Misplaced Modifiers: Participial phrases and introductory clauses",
            "Parallelism: Coordinating conjunctions (and, but, or), correlative conjunctions (not only... but also)",
            "Pronoun Ambiguity and Antecedent agreement (each, neither, either as singular)",
            "Tenses and Conditionals: Past Perfect, Present Perfect, Subjunctive mood"
        ],
        "sections": {
            "concept": """Verbal Ability evaluates precision in corporate English:
- **Subject-Verb Agreement:** The verb must agree with the true grammatical subject, not with intervening prepositional phrases (e.g., 'The box of chocolates **is** on the table', NOT 'are').
- **Dangling Modifiers:** A descriptive phrase at the start of a sentence must logically modify the immediate noun following the comma (e.g., 'Walking down the street, the trees looked beautiful' is incorrect because trees cannot walk!).
- **Parallelism:** Elements in a list or joined by correlative conjunctions (`neither...nor`, `not only...but also`) must share identical grammatical form (e.g., 'She likes swimming, running, and to cycle' -> 'swimming, running, and **cycling**').
- **Singular Indefinite Pronouns:** `Everyone`, `everybody`, `each`, `neither`, `either`, `nobody` are strictly singular and take singular verbs ('Everyone **has** finished his or her work').""",
            "formulas": """1. **Intervening Phrase Rule:**
   $$\\\\text{Subject} + [\\\\text{as well as / along with / together with / in addition to}] + \\\\text{Noun} \\\\implies \\\\text{Verb agrees with FIRST Subject!}$$
2. **Correlative Conjunction Agreement:**
   $$\\\\text{Neither } A \\\\text{ nor } B + \\\\text{Verb} \\\\implies \\\\text{Verb agrees with CLOSEST subject } (B)$$""",
            "solved_examples": [
                {
                    "title": "Correcting Dangling Modifier Errors",
                    "difficulty": "Easy | TCS, Infosys, Wipro",
                    "problem": "Correct the error: 'Having finished the assignment, the TV was turned on by John.'",
                    "step_by_step": [
                        "Step 1: Identify introductory participial phrase: 'Having finished the assignment'.",
                        "Step 2: Who finished the assignment? John, not the TV!",
                        "Step 3: In the original sentence, 'the TV' immediately follows the comma, making it a dangling modifier.",
                        "Step 4: Correction: Place 'John' immediately after the comma: 'Having finished the assignment, John turned on the TV.'"
                    ],
                    "code_or_math": """// Grammar Fix:
// Incorrect: Having finished the assignment, the TV was turned on by John.
// Correct:   Having finished the assignment, John turned on the TV.""",
                    "explanation": "Aligns the actor with the introductory modifier phrase."
                }
            ],
            "practice_questions": [
                {
                    "question": "Choose the grammatically correct sentence:",
                    "options": [
                        "A) Neither the manager nor the employees was present.",
                        "B) Neither the manager nor the employees were present.",
                        "C) Neither the manager or the employees were present.",
                        "D) Neither the manager nor employees has been present."
                    ],
                    "correct_answer": "B) Neither the manager nor the employees were present.",
                    "detailed_solution": "With 'neither...nor', the verb agrees with the closer subject ('employees', which is plural, taking 'were')."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is the Subjunctive Mood in English and how does it appear in corporate communications?",
                    "model_answer": "The Subjunctive Mood expresses wishes, hypothetical scenarios, or demands rather than objective facts. Key rules: 1) Hypothetical conditional uses 'were' regardless of subject: 'If I were the team lead...' (not 'was'). 2) Mandative subjunctive verbs (demand, recommend, insist, require) use the base form of the verb without 's' or 'should': 'The committee recommended that he **submit** the report by Friday' (not 'submits').",
                    "interviewer_tip": "Cite mandative subjunctive after verbs of demand/recommendation."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Vocabulary Mastery, Synonyms & Antonyms",
        "key_takeaways": "Master Latin and Greek root words, prefixes/suffixes, contextual word meanings, high-frequency GRE/CAT words, and word associations.",
        "topics": [
            "Etymology and Root words: Bene/Mal, Chron, Dict, Loc/Loq, Path, Phil, Vert/Vers",
            "Prefixes and Suffixes that invert or intensify meanings",
            "Contextual Synonyms and Antonyms in corporate and technical contexts",
            "Homophones and easily confused word pairs (affect vs effect, principal vs principle)",
            "High-frequency placement vocabulary bank (500 essential words)"
        ],
        "sections": {
            "concept": """Building a powerful vocabulary is achieved most effectively through **Etymology (Root Words)** rather than brute-force memorization:
- **`BENE` (Good/Well):** Benefactor (one who gives help), Benevolent (kind), Beneficial.
- **`MAL` (Bad/Evil):** Malevolent (spiteful), Malicious, Malignant.
- **`CHRON` (Time):** Chronological (arranged in order of time), Chronic (persisting over time), Synchronize (occur at same time).
- **`LOQ / LOC` (Speak/Talk):** Loquacious (talkative), Eloquent (fluent speaker), Circumlocution (roundabout talking).
- **`PATH` (Feeling/Disease):** Sympathy (feeling with), Empathy (identifying with feeling), Apathy (lack of feeling), Antipathy (hostility).

**Contextual Nuance:**
In placement exams, multiple choices may seem like synonyms, but tone dictates the correct fit (e.g., 'frugal' has a positive connotation of careful spending, whereas 'miserly' has a negative connotation of hoarding).""",
            "formulas": """1. **Root Word Formula:**
   $$\\\\text{Prefix (Direction/Polarity)} + \\\\text{Root (Core Concept)} + \\\\text{Suffix (Part of Speech)} = \\\\text{Word Meaning}$$""",
            "solved_examples": [
                {
                    "title": "Deducing Word Meaning via Root Words",
                    "difficulty": "Easy | Infosys, TCS, Cognizant",
                    "problem": "Deduce the meaning of 'Magnanimous' from its roots: MAGNA + ANIM.",
                    "step_by_step": [
                        "Step 1: Root `MAGNA` means Large / Great (as in magnitude, magnify).",
                        "Step 2: Root `ANIM` means Soul / Mind / Spirit (as in animal, unanimous, animate).",
                        "Step 3: Combined meaning: Great-souled / Generous and forgiving, especially towards a rival."
                    ],
                    "code_or_math": """// Etymological Breakdown:
// Magna (Great) + Anima (Soul) = Generous, noble-spirited""",
                    "explanation": "Root words allow candidates to decipher unfamiliar vocabulary during exams."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the closest synonym of 'Ephemeral'?",
                    "options": ["A) Eternal", "B) Transient", "C) Fragile", "D) Luminous"],
                    "correct_answer": "B) Transient",
                    "detailed_solution": "Ephemeral means lasting for a very short time; transient is its direct synonym."
                }
            ],
            "interview_questions": [
                {
                    "company": "TCS",
                    "question": "Explain the difference between 'Affect' and 'Effect'.",
                    "model_answer": "In standard usage, **Affect** is almost always a verb meaning to influence or produce a change in something ('The market crash affected his portfolio'). **Effect** is almost always a noun meaning the result or consequence of a change ('The effect of the medication was immediate'). Memory trick: **RAVEN** (Remember: Affect is a Verb, Effect is a Noun).",
                    "interviewer_tip": "Cite the RAVEN mnemonic for instant recall."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Reading Comprehension Mastery",
        "key_takeaways": "Master Skimming & Scanning, Main Idea identification, Tone analysis (Objective, Critical, Cynical, Laudatory), and Inference extraction.",
        "topics": [
            "Speed reading techniques: Skimming for structure, scanning for keywords, eliminating subvocalization",
            "Identifying the Central Thesis and Primary Purpose of a passage",
            "Author Tone Classification: Objective/Informative, Critical, Laudatory/Eulogistic, Cynical, Sarcastic",
            "Direct fact questions vs Deep inference questions",
            "Elimination strategies: Extreme words (always, never, all) vs Balanced nuanced qualifiers"
        ],
        "sections": {
            "concept": """Reading Comprehension (RC) tests the ability to rapidly digest dense, technical, scientific, or socioeconomic prose.

**Strategic Reading Methodology:**
1. **First Pass (Skim - 60 seconds):** Read the first and last sentence of each paragraph. Identify the **Central Thesis** and paragraph structural flow.
2. **Analyze the Question Stem:** Identify whether the question is:
   - **Direct Fact:** Match keywords directly in the text.
   - **Main Idea:** Synthesize the overall purpose of the author.
   - **Inference:** A conclusion that MUST be logically true based on the passage, but is NOT explicitly stated verbatim.
   - **Tone:** The emotional attitude of the author towards the subject matter.

**Elimination Heuristics:**
- Beware of **Extreme Options:** Answers using `completely`, `always`, `never`, `solely` are almost always incorrect in RC passages.
- Prefer **Nuanced Answers:** Answers using `tends to`, `suggests`, `partially`, `indicates` reflect balanced academic reasoning.""",
            "formulas": """1. **RC Question Classification:**
   $$\\\\text{Fact (Verbatim scan)} \\\\iff \\\\text{Inference (Logical deduction)} \\\\iff \\\\text{Tone (Author's sentiment)}$$""",
            "solved_examples": [
                {
                    "title": "Eliminating Traps in Inference Questions",
                    "difficulty": "Easy | TCS Digital, Infosys, Capgemini",
                    "problem": "Passage: 'Electric vehicles have seen adoption growth due to subsidies, but battery raw material scarcity threatens production scales.' Question: What can be inferred?",
                    "step_by_step": [
                        "Step 1: Option A: 'EV production will cease completely.' (Trap: Extreme word 'completely').",
                        "Step 2: Option B: 'Raw material supply chains play a significant role in determining EV manufacturing capacity.' (Balanced, supported by text).",
                        "Step 3: Option B is the valid inference."
                    ],
                    "code_or_math": """// Elimination:
// A) Extreme ("cease completely") -> Eliminate!
// B) Measured & Supported -> Correct!""",
                    "explanation": "Valid inferences remain conservative and strictly supported by passage evidence."
                }
            ],
            "practice_questions": [
                {
                    "question": "If an author describes a new technology by highlighting its benefits while pointing out documented risks without bias, what is the author's tone?",
                    "options": ["A) Cynical", "B) Laudatory", "C) Objective and Analytical", "D) Sarcastic"],
                    "correct_answer": "C) Objective and Analytical",
                    "detailed_solution": "Presenting balanced pros and cons without personal emotional bias defines an objective tone."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "In fast corporate communications, how do you synthesize a multi-page document into an executive summary?",
                    "model_answer": "Extract the **BLUF (Bottom Line Up Front)**: 1) What is the core problem or opportunity? 2) What is the proposed decision or action? 3) What are the measurable impacts and metrics? 4) What are the primary risks and mitigations? Summarize this into 3 concise bullet points before presenting supporting data.",
                    "interviewer_tip": "Use the BLUF (Bottom Line Up Front) framework."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Para Jumbles & Sentence Rearrangement",
        "key_takeaways": "Master Opening Sentences, Mandatory Pairs (Noun -> Pronoun, Acronym -> Full Form), Chronological markers, and Concluding transitions.",
        "topics": [
            "Identifying independent Opening Sentences (Introduces subject, no dangling pronouns)",
            "Mandatory Pair identification techniques: Pronoun references (he, she, they, this, these)",
            "Chronology and Sequence connectors: First, subsequently, meanwhile, finally",
            "Contrast markers (However, on the other hand, nevertheless) and cause-effect links (therefore, consequently)",
            "Acronym rule: Full organizational title precedes abbreviated acronym"
        ],
        "sections": {
            "concept": """Para Jumbles test structural coherence and narrative flow. 

**Core Solving Techniques:**
1. **Find the Opening Sentence:** The opener must be an independent, self-contained thought introducing the central topic. Sentences starting with `However`, `Therefore`, `Moreover`, `This`, `These`, or pronouns (`He`, `It`) cannot be the opening sentence.
2. **Form Mandatory Pairs:**
   - **Noun-Pronoun Pair:** A person's full name or concept is introduced first (e.g., 'Alan Turing'), followed by the pronoun in a subsequent sentence ('He proposed...').
   - **Acronym Pair:** Full expansion occurs first (e.g., 'World Health Organization (WHO)'), followed by the acronym in later sentences.
   - **Contrast Pair:** An idea followed by its contradiction introduced by `However` or `Yet`.
3. **Scan Options for Identified Pairs:** If sentences B and D form a mandatory pair (BD), immediately eliminate all options where B is not followed directly by D.""",
            "formulas": """1. **Mandatory Pairing Rules:**
   $$\\\\text{Full Name} \\\\to \\\\text{Pronoun}; \\\\quad \\\\text{Full Definition} \\\\to \\\\text{Acronym}; \\\\quad \\\\text{Cause} \\\\to \\\\text{Therefore / Consequently}$$""",
            "solved_examples": [
                {
                    "title": "Arranging a 4-Sentence Para Jumble via Mandatory Pairs",
                    "difficulty": "Easy | TCS, Infosys, Wipro",
                    "problem": "Arrange sentences: A. He spent his childhood in South Africa. B. Elon Musk is a prominent technology entrepreneur. C. Later, he moved to Canada and then to the United States. D. These ventures include SpaceX and Tesla.",
                    "step_by_step": [
                        "Step 1: Identify opener: B introduces the full name 'Elon Musk' without dangling pronouns. B is the opener.",
                        "Step 2: A follows B chronologically ('spent his childhood...'). Pair = BA.",
                        "Step 3: C follows A ('Later, he moved...'). Pair = BAC.",
                        "Step 4: D concludes by referencing ventures founded in the US. Final order = B-A-C-D."
                    ],
                    "code_or_math": """// Order:
// B: Introduces person
// A: Early childhood
// C: Later relocation
// D: Current ventures
// Valid sequence: BACD""",
                    "explanation": "Chronological progression from childhood to modern ventures creates a cohesive narrative."
                }
            ],
            "practice_questions": [
                {
                    "question": "Can a sentence beginning with 'Therefore' serve as the opening sentence of a coherent paragraph?",
                    "options": [
                        "A) Yes, always",
                        "B) No, because 'Therefore' denotes a conclusion derived from preceding context",
                        "C) Only in scientific papers",
                        "D) Yes, if it is short"
                    ],
                    "correct_answer": "B) No, because 'Therefore' denotes a conclusion derived from preceding context",
                    "detailed_solution": "Conclusive transition words require antecedent premises and cannot introduce a paragraph."
                }
            ],
            "interview_questions": [
                {
                    "company": "Cognizant",
                    "question": "When solving Para Jumbles with 5 sentences in a timed exam, what is the fastest elimination strategy?",
                    "model_answer": "Never try to arrange all 5 sentences mentally from scratch. First, scan the options to see candidate opening sentences (usually only 2 options differ, e.g., A vs C). Identify the single valid opener to eliminate 50% of choices. Next, find just ONE strong mandatory pair (e.g., a Noun-Pronoun link BD). Look at the remaining options: whichever option places B immediately before D is the correct answer. This solves the question in under 45 seconds.",
                    "interviewer_tip": "Advise using option-driven elimination rather than manual rearrangement."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Fill in the Blanks & Sentence Completion",
        "key_takeaways": "Master Single and Double blanks, positive/negative contextual tone signals, collocations, and transition trigger words.",
        "topics": [
            "Contextual Clues: Identifying tone and sentiment indicators in the sentence",
            "Transition Trigger Words: Agreement (and, moreover) vs Contrast (although, despite, yet)",
            "Collocations: Prepositional pairings (accused of, abstained from, adhere to)",
            "Double-blank strategy: Solving the easier blank first to eliminate options",
            "Vocabulary precision: Selecting words that fit exact syntactic grammar"
        ],
        "sections": {
            "concept": """Sentence Completion evaluates vocabulary precision and contextual reading comprehension:
- **Tone Indicators:** Identify whether the missing word must carry a positive, negative, or neutral charge based on surrounding words.
- **Transition Triggers:**
  - **Continuity Triggers (`and`, `moreover`, `furthermore`, `similarly`):** The second half of the sentence reinforces the sentiment of the first half.
  - **Contrast Triggers (`although`, `despite`, `in spite of`, `however`, `yet`, `nevertheless`):** The second half of the sentence inverts the sentiment of the first half.
- **Prepositional Collocations:** English pairs specific verbs with specific prepositions: `abide by`, `abstain from`, `accede to`, `accused of`, `adhere to`, `concur with`, `prohibit from`.""",
            "formulas": """1. **Sentence Polarity Equation:**
   $$[\\\\text{Positive Clause}] + \\\\text{ALONG WITH} + [\\\\text{Blank}] \\\\implies \\\\text{Blank MUST be POSITIVE}$$
   $$[\\\\text{Positive Clause}] + \\\\text{ALTHOUGH} + [\\\\text{Blank}] \\\\implies \\\\text{Blank MUST be NEGATIVE}$$""",
            "solved_examples": [
                {
                    "title": "Solving Double Blank via Contrast Triggers",
                    "difficulty": "Easy | Infosys, TCS, Wipro",
                    "problem": "Fill blanks: 'Although the team was initially _______ by the technical setbacks, their final presentation was _______ by the judges.'",
                    "step_by_step": [
                        "Step 1: Notice contrast trigger 'Although'.",
                        "Step 2: 'technical setbacks' indicates Blank 1 should be negative (e.g., discouraged, dismayed).",
                        "Step 3: 'Although [negative], ... final presentation was [positive]': Blank 2 must be positive (e.g., praised, lauded).",
                        "Step 4: Match options containing (Negative, Positive) pair: (dismayed, praised)."
                    ],
                    "code_or_math": """// Polarity Mapping:
// Although [Negative: dismayed], presentation was [Positive: praised]""",
                    "explanation": "Contrast trigger 'Although' dictates opposite emotional polarities between blanks."
                }
            ],
            "practice_questions": [
                {
                    "question": "The manager decided to _______ the employee from his duties following the audit findings.",
                    "options": ["A) relieve", "B) dismiss", "C) exonerate", "D) promote"],
                    "correct_answer": "A) relieve",
                    "detailed_solution": "The correct corporate prepositional collocation is 'relieve [someone] from [duties]'."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is a Collocation in English and why are collocations critical in corporate communications?",
                    "model_answer": "A Collocation is a customary juxtaposition or natural combination of words that commonly occur together in native speech (e.g., 'make a decision', NOT 'do a decision'; 'fast food', NOT 'quick food'; 'adhere to guidelines', NOT 'adhere with guidelines'). In corporate communications, using unnatural word combinations sounds unpolished and confuses international clients. Mastering standard collocations ensures clear, professional, authoritative communication.",
                    "interviewer_tip": "Cite 'make a decision' vs 'do a decision' as a clear example."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Idioms, Phrases & Corporate Communication",
        "key_takeaways": "Master common business idioms, phrasal verbs, corporate email etiquette, professional tone, and active vs passive voice.",
        "topics": [
            "High-frequency business idioms (hit the ground running, burn the midnight oil, cut corners)",
            "Phrasal verbs and prepositional nuances (call off, put off, look into, bring about)",
            "Corporate email architecture: Subject lines, salutations, body conciseness, sign-offs",
            "Professional vs Informal tone: Avoiding conversational slang in business writing",
            "Active voice (preferred for clarity) vs Passive voice (used when actor is unknown or to soften blame)"
        ],
        "sections": {
            "concept": """Corporate Communication requires professionalism, clarity, and diplomacy:
- **Business Idioms:** Expressions whose figurative meaning cannot be inferred from the literal definition of individual words (e.g., 'touch base' means briefly make contact; 'ballpark figure' means rough estimate; 'bite the bullet' means face an inevitable difficult situation).
- **Active Voice:** The subject performs the action (`The team completed the project`). Preferred in corporate communications for accountability, conciseness, and directness.
- **Passive Voice:** The subject receives the action (`The project was completed`). Used diplomatically to soften blame ('An error was made' instead of 'You made an error').

**Email Etiquette:**
- Subject lines must be specific and actionable: `[Action Required] Review Q3 Engineering Roadmap by Friday`.
- Keep messages structured with bullet points.
- State the desired action in the first two sentences.""",
            "formulas": """1. **Voice Preference:**
   $$\\\\text{Active Voice (Direct & Accountable)} \\\\gg \\\\text{Passive Voice (Diplomatic / Impersonal)}$$""",
            "solved_examples": [
                {
                    "title": "Rewriting Passive Cluttered Prose into Clean Active Corporate English",
                    "difficulty": "Easy | Amazon, TCS, Infosys",
                    "problem": "Rewrite: 'It was decided by our committee that the deployment of the server will be executed by the DevOps engineer on Tuesday.'",
                    "step_by_step": [
                        "Step 1: Identify the true actors: Committee and DevOps engineer.",
                        "Step 2: Convert passive verbs ('was decided', 'will be executed') to direct active verbs.",
                        "Step 3: Revised: 'The committee decided that the DevOps engineer will deploy the server on Tuesday.'"
                    ],
                    "code_or_math": """// Professional Active Voice:
// Legacy: It was decided by our committee that...
// Clean:  The committee decided that the DevOps engineer will deploy the server on Tuesday.""",
                    "explanation": "Reduces wordiness and clearly establishes ownership of actions."
                }
            ],
            "practice_questions": [
                {
                    "question": "What does the business idiom 'to play devil's advocate' mean?",
                    "options": [
                        "A) To support the competitor",
                        "B) To argue against an idea for the sake of exploring all perspectives and testing robustness",
                        "C) To break the law",
                        "D) To cause confusion"
                    ],
                    "correct_answer": "B) To argue against an idea for the sake of exploring all perspectives and testing robustness",
                    "detailed_solution": "Playing devil's advocate tests the strength of an argument by taking an opposing view during discussions."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "Why does Amazon ban PowerPoint presentations in executive meetings in favor of 6-page structured narrative memos?",
                    "model_answer": "PowerPoint presentations allow presenters to hide weak logic behind flashy bullet points, vocal charisma, and superficial graphics. A 6-page written narrative forces authors to think deeply, structure complete sentences, support arguments with data, and address trade-offs explicitly. In meetings, everyone reads the memo silently for the first 20 minutes before asking deep, rigorous questions, leading to vastly superior decision making.",
                    "interviewer_tip": "Cite the Amazon 6-page narrative memo policy."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Critical Verbal Reasoning & Passage Assumptions",
        "key_takeaways": "Master argument structure (Premise, Assumption, Conclusion), strengthening/weakening arguments, and paradox resolution.",
        "topics": [
            "Argument Anatomy: Premises (facts) + Unstated Assumptions = Conclusion",
            "Weakening an argument: Introducing alternate causes, attacking the assumption",
            "Strengthening an argument: Validating the assumption, ruling out confounding factors",
            "Resolving a Paradox: Identifying a fact that explains seemingly contradictory outcomes",
            "Flaws in reasoning: Ad Hominem, Straw Man, Post Hoc Ergo Propter Hoc"
        ],
        "sections": {
            "concept": """Critical Verbal Reasoning analyzes the logical strength of arguments:
$$\\\\text{Premises (Observable Facts)} + \\\\text{Assumptions (Unstated Bridges)} \\\\implies \\\\text{Conclusion (Author's Claim)}$$

**How to Weaken an Argument:**
1. Identify the Conclusion and the unstated Assumption.
2. Find an option that shows the assumption is false, or introduces an **Alternative Cause** that explains the outcome without the author's proposed factor.

**How to Strengthen an Argument:**
1. Provide additional evidence showing the assumption holds true.
2. Rule out potential alternative causes, proving the author's factor was the sole driver.

**Resolving a Paradox:**
A paradox presents two conflicting facts that seem contradictory. The correct answer provides a missing piece of information that reconciles both facts without rejecting either.""",
            "formulas": """1. **Argument Strengthening/Weakening Dynamics:**
   $$\\\\text{Weaken} \\\\implies \\\\text{Break the Assumption OR Introduce Alternative Cause}$$
   $$\\\\text{Strengthen} \\\\implies \\\\text{Reinforce Assumption OR Eliminate Alternative Cause}$$""",
            "solved_examples": [
                {
                    "title": "Resolving a Business Paradox",
                    "difficulty": "Easy | Infosys, TCS Digital",
                    "problem": "Fact 1: City X reduced public bus fares by 50%. Fact 2: Total fare revenues collected by the bus transit authority increased by 20%. How is this resolved?",
                    "step_by_step": [
                        "Step 1: Formula for revenue: $\\\\text{Revenue} = \\\\text{Fare per rider} \\\\times \\\\text{Ridership}$.",
                        "Step 2: Fare dropped by 50%. For revenue to increase by 20%, ridership must have increased substantially ($> 140\\\\%$ increase).",
                        "Step 3: The paradox is resolved by showing that the lower price attracted a massive surge in new passengers who previously drove cars."
                    ],
                    "code_or_math": """// Revenue = Price * Quantity
// 1.20 = 0.50 * Quantity -> Quantity = 2.40 (140% surge in ridership!)""",
                    "explanation": "Explains how a price cut can increase total revenue through volume elasticity."
                }
            ],
            "practice_questions": [
                {
                    "question": "An argument claims that because ice cream consumption and crime rates both peak in July, ice cream causes crime. What logical fallacy is committed?",
                    "options": [
                        "A) Ad Hominem",
                        "B) Post Hoc Ergo Propter Hoc / Confounding variable fallacy",
                        "C) Straw Man",
                        "D) Circular reasoning"
                    ],
                    "correct_answer": "B) Post Hoc Ergo Propter Hoc / Confounding variable fallacy",
                    "detailed_solution": "Confusing correlation with causation: summer heat causes both higher ice cream consumption and more outdoor activity leading to crime."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "What is the Straw Man fallacy and how do you prevent it during technical architectural debates?",
                    "model_answer": "A Straw Man fallacy occurs when an opponent distorts, exaggerates, or misrepresents someone's argument to make it easier to attack, rather than addressing the actual argument (e.g., 'So you want to use microservices because you want to make our system unnecessarily complex and fail!'). To prevent it: 1) Practice active listening and reflect the opponent's argument back to their satisfaction ('What I hear you proposing is X to achieve Y. Is that accurate?'). 2) Debate the actual trade-offs objectively based on latency, throughput, and operational complexity.",
                    "interviewer_tip": "Demonstrate emotional intelligence and collaborative debate habits."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Corporate Group Discussions, Extempore & HR Verbal Round Preparation",
        "key_takeaways": "Master Group Discussion dynamics (initiation, moderation, conclusion), Extempore frameworks (PREP, PAST-PRESENT-FUTURE), and top HR behavioral interview questions (STAR method).",
        "topics": [
            "Group Discussion (GD) evaluation parameters: Content, articulation, leadership, active listening",
            "How to initiate and summarize a Group Discussion effectively",
            "Extempore frameworks: PREP (Point, Reason, Example, Point) and 3-Pillar structure",
            "HR Behavioral Interviews: The STAR Method (Situation, Task, Action, Result)",
            "Mastering common HR questions: 'Tell me about yourself', 'Greatest weakness', 'Why this company?'"
        ],
        "sections": {
            "concept": """Final campus placement rounds test interpersonal verbal communication and corporate behavioral fit:
- **Group Discussion (GD):** Evaluates teamwork, leadership, and emotional intelligence. Key roles:
  - **Initiator:** Defines the topic scope clearly.
  - **Moderator:** Brings quiet candidates into the conversation diplomatically.
  - **Summarizer:** Summarizes key pros and cons without introducing new ideas.
- **Extempore (Speaking spontaneously for 1-2 minutes):**
  Use the **PREP Framework**:
  1. **Point:** State your core stance in the first sentence.
  2. **Reason:** Explain the underlying rationale.
  3. **Example:** Give a concrete real-world case study or metric.
  4. **Point:** Restate your conclusion firmly.
- **The STAR Method for Behavioral Interviews:**
  - **Situation:** Set the context and challenge.
  - **Task:** Your specific responsibility.
  - **Action:** The concrete steps YOU took (use 'I', not 'we').
  - **Result:** Quantifiable business outcome ('reduced latency by 35%').""",
            "formulas": """1. **The STAR Behavioral Response Structure:**
   $$\\\\text{Situation (20\\\\%)} \\\\to \\\\text{Task (10\\\\%)} \\\\to \\\\text{Action (50\\\\% - Most critical)} \\\\to \\\\text{Result (20\\\\% - Quantified)}$$""",
            "solved_examples": [
                {
                    "title": "Answering 'Tell Me About a Time You Faced a Conflict in a Team' using STAR",
                    "difficulty": "Easy | Amazon, Google, TCS",
                    "problem": "Deliver a model HR response to a team conflict question.",
                    "step_by_step": [
                        "Step 1 (Situation): During our final year capstone project, our 4-person team had a deadline in two weeks.",
                        "Step 2 (Task): Two teammates disagreed strongly on whether to use React or vanilla JavaScript, stalling progress.",
                        "Step 3 (Action): I organized an objective 30-minute evaluation session where both members listed pros and cons against our project requirements (tight deadline and minimal dependencies). I proposed building the MVP in vanilla JS while keeping component structures ready for React.",
                        "Step 4 (Result): The team aligned, unblocked development, and delivered the working portal 2 days ahead of schedule, earning an A grade."
                    ],
                    "code_or_math": """// STAR Framework Checklist:
// [x] Situation clearly stated
// [x] Specific role defined
// [x] Mature, proactive Action taken
// [x] Positive, quantified Result delivered""",
                    "explanation": "Demonstrates conflict resolution, maturity, and focus on team outcomes."
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the recommended response when an HR interviewer asks: 'What is your greatest weakness?'",
                    "options": [
                        "A) 'I have no weaknesses; I am a perfectionist.'",
                        "B) State a genuine professional developmental area, explain what proactive steps you are taking to improve it, and show measurable progress",
                        "C) Mention a personal flaw that disqualifies you from the job",
                        "D) Refuse to answer"
                    ],
                    "correct_answer": "B) State a genuine professional developmental area, explain what proactive steps you are taking to improve it, and show measurable progress",
                    "detailed_solution": "Authentic self-awareness coupled with active self-improvement demonstrates maturity and high coachability."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon",
                    "question": "Why does Amazon evaluate candidates against 16 Leadership Principles (such as Customer Obsession and Bias for Action)?",
                    "model_answer": "Amazon uses Leadership Principles not as inspirational slogans, but as daily decision-making frameworks. They evaluate candidates for cultural fit to ensure that when decentralized engineers face ambiguous decisions without managerial oversight, they will naturally prioritize long-term customer trust over short-term metrics, act with urgency (Bias for Action), and take long-term responsibility (Ownership). In interviews, every behavioral response should map directly to one of these principles using the STAR method.",
                    "interviewer_tip": "Anchor responses directly into Leadership Principles using quantified metrics."
                }
            ]
        }
    }
]
'''
    (CURRICULUM_DIR / "curriculum_verbal.py").write_text(content, encoding="utf-8")
    print("Created curriculum_verbal.py")

build_verbal_module()
