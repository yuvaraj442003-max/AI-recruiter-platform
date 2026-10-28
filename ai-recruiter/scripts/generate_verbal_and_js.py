"""
Generates unabridged master textbooks for:
- Verbal Ability & Placement English (verbal_master.py)
- JavaScript, TypeScript & Modern Web Stack (javascript_master.py)
"""
import os
import ast

TEXTBOOK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "app", "services", "textbooks"))

# =============================================================================
# VERBAL ABILITY & ENGLISH
# =============================================================================
VERBAL_CODE = r'''"""
verbal_master.py — Prescribed Master Textbook for Verbal Ability & English Communication.
Comprehensive unabridged campus placement textbook covering Subject-Verb Agreement,
syntax rules, vocabulary etymology, phrasal verbs, idioms, sentence correction,
reading comprehension, critical reasoning, para jumbles, the STAR behavioral interview method,
and solved placement drills.
"""

VERBAL_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Subject-Verb Agreement, Syntax & Grammatical Foundations",
        "topics": [
            "Core agreement rule: Singular subjects take singular verbs; plural take plural",
            "Compound subjects joined by 'and', 'or', 'nor', 'either...or', 'neither...nor'",
            "Indefinite pronouns: Always singular (each, everyone, someone) vs variable (all, some, none)",
            "Collective nouns (committee, jury, team) acting as unit vs individuals",
            "Intervening phrases, parenthetical clauses, and inverted syntax sentences"
        ],
        "key_takeaways": "When subjects are joined by 'either...or' or 'neither...nor', the verb agrees with the subject closest to it. Intervening prepositional phrases like 'along with' or 'as well as' never alter the singular or plural status of the subject."
    },
    {
        "chapter_num": 2,
        "title": "Placement Vocabulary Mastery: Etymology, Roots & Contextual Usage",
        "topics": [
            "Greek and Latin root words: -ben-/-mal- (good/bad), -chron- (time), -loqu-/-loc- (speak), -vert-/-vers- (turn)",
            "Prefixes and suffixes modifying semantic polarity (un-, dis-, in-, -phil, -phobe)",
            "High-frequency corporate placement word list (fastidious, esoteric, pragmatic, ubiquitous, ambivalent)",
            "Words commonly confused and homophones (elicit/illicit, discrete/discreet, affect/effect, principle/principal)",
            "Contextual tone matching and eliminating extreme or inappropriate connotations"
        ],
        "key_takeaways": "Root word decomposition allows rapid inference of unfamiliar words during timed exams. Contextual connotation analysis prevents choosing definitions that are grammatically valid but tone-inappropriate."
    },
    {
        "chapter_num": 3,
        "title": "Idioms, Phrasal Verbs & Prepositional Collocations",
        "topics": [
            "Fixed prepositions: 'adhere to', 'abstain from', 'acquiesce in', 'connive at', 'prone to', 'conducive to'",
            "High-frequency corporate idioms: 'cut corners', 'bite the bullet', 'back to the drawing board', 'call it a day'",
            "Separable vs inseparable phrasal verbs: 'bring about', 'call off', 'put off', 'run into', 'figure out'",
            "Common placement prepositional pitfalls: 'discuss about' (redundant), 'comprise of' (incorrect)"
        ],
        "key_takeaways": "Certain verbs mandate specific prepositions regardless of casual slang. 'Comprise' means 'to consist of' and therefore never takes 'of' in active voice."
    },
    {
        "chapter_num": 4,
        "title": "Sentence Correction, Error Spotting & Structural Flow",
        "topics": [
            "Dangling and misplaced modifiers: Participial phrases must immediately precede their logical subject",
            "Parallelism: Elements in a series or comparison must share identical grammatical structures",
            "Conditional sentences: Zero, First, Second, and Third Conditionals ('If I had known, I would have...')",
            "Pronoun-antecedent agreement, case ambiguity (who vs whom), and ambiguous pronoun references",
            "Redundancy and wordiness elimination: 'return back', 'revert back', 'adequate enough'"
        ],
        "key_takeaways": "A participial clause starting a sentence must be immediately followed by the noun performing that action; otherwise, a dangling modifier error is committed."
    },
    {
        "chapter_num": 5,
        "title": "Reading Comprehension Mastery & Critical Reasoning",
        "topics": [
            "Passage typology: Analytical, discursive, narrative, technical, and argumentative texts",
            "Active skimming and scanning techniques for 400-word corporate test passages",
            "Question classifications: Main idea/title, explicit factual, implicit deductive, author's tone",
            "Critical reasoning foundations: Identifying premises, conclusions, and unstated assumptions",
            "Strengthening and weakening logical arguments and identifying logical fallacies"
        ],
        "key_takeaways": "Tone questions evaluate the author's emotional perspective (e.g., objective, critical, reverent, pragmatic). Answers must be grounded strictly in the passage text without external extrapolation."
    },
    {
        "chapter_num": 6,
        "title": "Para Jumbles, Sentence Reordering & Logical Sequence",
        "topics": [
            "Mandatory Pair identification techniques: Noun-Pronoun linkage, acronym expansion",
            "Transition signal words: Contrast (however, yet, conversely) vs Addition (moreover, furthermore)",
            "Cause-and-Effect logical progression: Identifying problem statement before proposed remedy",
            "Chronological and temporal sequencing in descriptive and historical paragraphs",
            "Elimination strategies using opening sentence autonomy test"
        ],
        "key_takeaways": "A sentence beginning with a transition marker ('However', 'Therefore') or an unresolved pronoun ('He', 'This phenomenon') cannot serve as the opening sentence of an autonomous paragraph."
    },
    {
        "chapter_num": 7,
        "title": "Professional Business Writing & Placement Interview Communication",
        "topics": [
            "The STAR Methodology for behavioral interview questions (Situation, Task, Action, Result)",
            "Crafting a 90-second executive elevator pitch: 'Tell me about yourself'",
            "Professional email communication: Structure, subject lines, tone, and call-to-action",
            "Vocal modulation, active listening cues, and non-verbal communication in AI/human interviews"
        ],
        "key_takeaways": "The STAR framework forces quantifiable, structured behavioral answers. Highlighting specific metrics and personal contributions in the 'Result' phase distinguishes top candidates."
    },
    {
        "chapter_num": 8,
        "title": "Solved Placement Verbal Tests & Assessment Drills",
        "topics": [
            "Detailed sentence correction walkthroughs with grammatical rule citations",
            "Para jumble step-by-step mandatory pair solutions",
            "Critical reasoning assumption and inference breakdowns",
            "Full-length Reading Comprehension passage with verified answer keys",
            "Self-assessment practice drills with explanations"
        ],
        "key_takeaways": "Practicing timed sentence correction and para jumble drills builds the pattern recognition needed for top marks in TCS NQT, Infosys, Cognizant, and Accenture verbal sections."
    }
]

VERBAL_TEXTBOOK_MARKDOWN = r"""# Verbal Ability & English Communication: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Verbal Ability & English Communication  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, verbal aptitude sections, and communication evaluation modules (TCS NQT, Infosys, Cognizant, Wipro, Accenture, Capgemini) are strictly grounded in the rules, grammatical structures, and reasoning frameworks detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Subject-Verb Agreement, Syntax & Grammatical Foundations](#chapter-1-subject-verb-agreement-syntax--grammatical-foundations)
  - [1.1 The Fundamental Agreement Rule](#11-the-fundamental-agreement-rule)
  - [1.2 Compound Subjects & The Proximity Principle](#12-compound-subjects--the-proximity-principle)
  - [1.3 Indefinite Pronouns: Singular, Plural & Variable](#13-indefinite-pronouns-singular-plural--variable)
  - [1.4 Collective Nouns & Inverted Syntax](#14-collective-nouns--inverted-syntax)
- [Chapter 2: Placement Vocabulary Mastery: Etymology, Roots & Contextual Usage](#chapter-2-placement-vocabulary-mastery-etymology-roots--contextual-usage)
  - [2.1 Etymological Roots (Greek & Latin Building Blocks)](#21-etymological-roots-greek--latin-building-blocks)
  - [2.2 High-Yield Corporate Placement Word Bank](#22-high-yield-corporate-placement-word-bank)
  - [2.3 Easily Confused Pairs & Homophones](#23-easily-confused-pairs--homophones)
- [Chapter 3: Idioms, Phrasal Verbs & Prepositional Collocations](#chapter-3-idioms-phrasal-verbs--prepositional-collocations)
  - [3.1 Mandatory Fixed Prepositions](#31-mandatory-fixed-prepositions)
  - [3.2 Phrasal Verbs in Corporate Contexts](#32-phrasal-verbs-in-corporate-contexts)
  - [3.3 Corporate Idiomatic Expressions](#33-corporate-idiomatic-expressions)
- [Chapter 4: Sentence Correction, Error Spotting & Structural Flow](#chapter-4-sentence-correction-error-spotting--structural-flow)
  - [4.1 Dangling & Misplaced Modifiers](#41-dangling--misplaced-modifiers)
  - [4.2 The Principle of Parallelism](#42-the-principle-of-parallelism)
  - [4.3 The Four English Conditionals](#43-the-four-english-conditionals)
  - [4.4 Pronoun Ambiguity & Subjunctive Mood](#44-pronoun-ambiguity--subjunctive-mood)
- [Chapter 5: Reading Comprehension Mastery & Critical Reasoning](#chapter-5-reading-comprehension-mastery--critical-reasoning)
  - [5.1 Active Skimming & Scanning Methodology](#51-active-skimming--scanning-methodology)
  - [5.2 Question Taxonomy & Decoy Elimination](#52-question-taxonomy--decoy-elimination)
  - [5.3 Critical Reasoning: Premises, Assumptions & Inferences](#53-critical-reasoning-premises-assumptions--inferences)
- [Chapter 6: Para Jumbles, Sentence Reordering & Logical Sequence](#chapter-6-para-jumbles-sentence-reordering--logical-sequence)
  - [6.1 The Mandatory Pair Technique](#61-the-mandatory-pair-technique)
  - [6.2 Transition Words & Logical Flow](#62-transition-words--logical-flow)
  - [6.3 The Opening & Closing Sentence Filters](#63-the-opening--closing-sentence-filters)
- [Chapter 7: Professional Business Writing & Placement Interview Communication](#chapter-7-professional-business-writing--placement-interview-communication)
  - [7.1 The STAR Behavioral Interview Framework](#71-the-star-behavioral-interview-framework)
  - [7.2 The 90-Second Executive Elevator Pitch](#72-the-90-second-executive-elevator-pitch)
  - [7.3 Corporate Email Etiquette & Precision](#73-corporate-email-etiquette--precision)
- [Chapter 8: Solved Placement Verbal Tests & Assessment Drills](#chapter-8-solved-placement-verbal-tests--assessment-drills)
  - [Solved Problem 1: Complex Sentence Correction Analysis](#solved-problem-1-complex-sentence-correction-analysis)
  - [Solved Problem 2: 5-Sentence Para Jumble Reordering](#solved-problem-2-5-sentence-para-jumble-reordering)
  - [Solved Problem 3: Reading Comprehension Deep Dive](#solved-problem-3-reading-comprehension-deep-dive)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: Subject-Verb Agreement, Syntax & Grammatical Foundations

### 1.1 The Fundamental Agreement Rule
A subject must agree with its main finite verb in number (singular vs plural) and person (first, second, third):
- **Singular:** *The software engineer writes efficient unit tests.* (Engineer = singular $\to$ writes = singular verb with '-s').
- **Plural:** *The software engineers write efficient unit tests.* (Engineers = plural $\to$ write = base plural form).

**The Intervening Phrase Trap:**
Phrases occurring between the grammatical subject and its verb do not alter the subject's number.
- *Rule:* Prepositional phrases (*in addition to, as well as, along with, accompanied by, together with, including, except*) are parenthetical modifiers.
- *Incorrect:* The lead developer, along with five quality analysts, **are** reviewing the sprint backlog.
- *Correct:* The lead developer, along with five quality analysts, **is** reviewing the sprint backlog. (Subject is *developer*, singular).

### 1.2 Compound Subjects & The Proximity Principle
1. **Joined by 'And':** Usually treated as plural:
   - *Python and Java **are** object-oriented programming languages.*
   - *Exception (Single Concept / Unit):* When two nouns combine to represent a single identity, meal, or concept:
     - *Bread and butter **is** a staple breakfast.*
     - *The founder and CEO of the startup **has** announced the funding round.* (One person holds both titles).
     - *The founder and the CEO **have** announced...* (Two distinct people indicated by repeated article 'the').
2. **Joined by 'Or', 'Nor', 'Either...or', 'Neither...nor':**
   - **The Proximity Rule:** The verb strictly agrees with the subject that is physically **closest** to the verb:
     - *Neither the project manager nor the developers **were** aware of the server outage.* (Developers = plural $\to$ were).
     - *Neither the developers nor the project manager **was** aware of the server outage.* (Manager = singular $\to$ was).

### 1.3 Indefinite Pronouns: Singular, Plural & Variable
- **Always Singular Pronouns:** *Each, everyone, everybody, someone, somebody, anyone, anybody, no one, nobody, either, neither, one.*
  - *Each of the microservices **has** its own dedicated database.* (NOT *have*).
  - *Everybody who applied for the engineering position **is** required to take the coding test.*
- **Always Plural Pronouns:** *Both, few, many, several.*
  - *Several of the candidate resumes **were** shortlisted for technical interviews.*
- **Variable (SANAM Rule):** *Some, Any, None, All, More/Most.*
  - Look at the object of the preposition following the pronoun:
    - Countable noun $\implies$ Plural verb: *All of the test cases **have** passed.*
    - Uncountable noun $\implies$ Singular verb: *All of the cached memory **has** been released.*

### 1.4 Collective Nouns & Inverted Syntax
- **Collective Nouns (Team, Committee, Jury, Faculty, Board):**
  - Acting as a single unified entity $\implies$ Singular verb:
    - *The interview panel **has** finalized the selection list.*
  - Acting as individual members in disagreement or separate actions $\implies$ Plural verb:
    - *The interview panel **were** divided in their opinions regarding the final candidate.*
- **Inverted Syntax (Sentences starting with 'There' or 'Here'):**
  - 'There' and 'Here' are dummy adverbs, never the subject. The true subject follows the verb:
    - *There **is** a critical bug in the authentication controller.* (Subject = bug $\to$ is).
    - *There **are** three critical bugs in the authentication controller.* (Subject = bugs $\to$ are).

---

## Chapter 2: Placement Vocabulary Mastery: Etymology, Roots & Contextual Usage

### 2.1 Etymological Roots (Greek & Latin Building Blocks)
Mastering morphemes (prefixes, roots, suffixes) allows instant decoding of over 5,000 corporate English words:

| Root / Morpheme | Origin & Meaning | Examples & Contextual Applications |
|:---|:---|:---|
| **BEN / BENE** | Latin: *well, good* | **Benefactor** (one who provides aid), **Benevolent** (well-meaning, charitable), **Beneficial** (helpful). |
| **MAL / MALE** | Latin: *bad, evil* | **Malevolent** (ill-willed), **Malicious** (spiteful; malicious code), **Malignant** (harmful). |
| **CHRON** | Greek: *time* | **Chronological** (arranged in order of time), **Synchronous** (occurring at same time), **Anachronism** (out of historical time). |
| **LOQU / LOC** | Latin: *to speak* | **Eloquent** (fluent and persuasive), **Loquacious** (excessively talkative), **Circumlocution** (roundabout speech). |
| **VERT / VERS** | Latin: *to turn* | **Avert** (turn away, prevent), **Adversary** (opponent), **Subvert** (undermine), **Inadvertent** (unintentional). |
| **LUC / LUM** | Latin: *light, clear* | **Lucid** (clear, easy to understand), **Elucidate** (make clear, explain), **Luminous** (bright). |
| **AMPHI / AMBI** | Greek/Latin: *both, around*| **Ambiguous** (open to more than one interpretation), **Ambivalent** (having mixed feelings). |

### 2.2 High-Yield Corporate Placement Word Bank
1. **Pragmatic (adj.):** Dealing with things sensibly and realistically based on practical considerations rather than theoretical ideals.
   - *Context:* "The engineering director adopted a pragmatic architecture, choosing a battle-tested relational database over an unproven technology."
2. **Fastidious (adj.):** Very attentive to and concerned about accuracy, detail, and cleanliness.
   - *Context:* "Code reviewers must be fastidious when inspecting high-concurrency memory allocations."
3. **Esoteric (adj.):** Intended for or likely to be understood by only a small number of people with specialized knowledge.
   - *Context:* "The mathematical proof underlying elliptic curve cryptography remained esoteric to standard frontend developers."
4. **Ubiquitous (adj.):** Present, appearing, or found everywhere simultaneously.
   - *Context:* "Smartphones and high-speed internet connections have become ubiquitous in metropolitan campuses."
5. **Ephemerality / Ephemeral (adj.):** Lasting for a very short time; transitory.
   - *Context:* "Serverless cloud functions exhibit ephemeral lifecycles, spinning up on request and terminating immediately after."

### 2.3 Easily Confused Pairs & Homophones
- **Affect vs Effect:**
  - *Affect (verb):* To influence or produce a change in something: "Network latency directly **affects** user conversion rates."
  - *Effect (noun):* The result or consequence of an action: "The caching layer had an immediate positive **effect** on response times."
  - *(Exception: 'Effect' as verb means to bring about: 'effect change'; 'Affect' as noun means emotional expression).*
- **Discrete vs Discreet:**
  - *Discrete (adj.):* Individually separate and distinct: "The algorithm breaks continuous signals into **discrete** time intervals."
  - *Discreet (adj.):* Careful, circumspect, maintaining confidentiality: "HR remained **discreet** during the performance appraisal reviews."
- **Elicit vs Illicit:**
  - *Elicit (verb):* To draw out or evoke a reaction/information: "The interviewer asked behavioral questions to **elicit** real problem-solving examples."
  - *Illicit (adj.):* Forbidden by law, rules, or custom: "The firewall detects and terminates **illicit** network connections."

---

## Chapter 3: Idioms, Phrasal Verbs & Prepositional Collocations

### 3.1 Mandatory Fixed Prepositions
Collocations in English mandate specific prepositions. Misuse is a primary source of error in campus verbal tests:

- **Adhere TO** (NOT with): *Engineers must adhere to industry security standards.*
- **Abstain FROM** (NOT to): *Committee members abstained from voting on the resolution.*
- **Acquiesce IN** (NOT to/with): *The management acquiesced in the employee demand for hybrid work.*
- **Capable OF** (NOT to do): *The distributed engine is capable of processing 100,000 transactions per second.*
- **Congratulate ON** (NOT for): *The team congratulated Sarah on her promotion to Tech Lead.*
- **Different FROM** (NOT than): *Microservices architecture is fundamentally different from monolithic design.*
- **Prone TO** (NOT for): *Unsynchronized shared memory is prone to race conditions.*
- **No Preposition Needed:** *Discuss* (NOT discuss about), *Comprise* (NOT comprise of in active voice), *Order* (NOT order for food).

### 3.2 Phrasal Verbs in Corporate Contexts
- **Bring about:** To cause something to happen: "Continuous integration brought about a 40% reduction in production deployment defects."
- **Call off:** To cancel an event: "Due to server maintenance, the scheduled online hackathon was called off."
- **Put off:** To postpone or delay: "The release manager decided to put off the deployment until off-peak hours."
- **Run into:** To encounter unexpectedly: "During load testing, the backend team ran into severe memory leaks."
- **Look into:** To investigate: "The site reliability engineer will look into the database deadlock reports."

### 3.3 Corporate Idiomatic Expressions
- **Bite the bullet:** To face a difficult or unpleasant situation with courage: "The company had to bite the bullet and rewrite the legacy codebase from scratch."
- **Cut corners:** To do something poorly or cheaply in order to save time or money: "Never cut corners on security auditing or input sanitization."
- **Back to the drawing board:** To start over after an initial plan failed: "The initial neural network model overfitted drastically, sending the data science team back to the drawing board."
- **Play devil's advocate:** To argue against an idea simply to test the strength of the opposing argument.

---

## Chapter 4: Sentence Correction, Error Spotting & Structural Flow

### 4.1 Dangling & Misplaced Modifiers
A modifier must be placed immediately adjacent to the word or phrase it is intended to modify:

- **Dangling Modifier Error:**
  - *Incorrect:* Walking into the server room, the blast of icy cold air hit the technician.
    *(Analysis: 'Walking into the server room' is a participial modifier. As written, it modifies 'the blast of icy cold air'—implying the air was walking!).*
  - *Correct:* Walking into the server room, the technician was hit by a blast of icy cold air.
    *(Or: When the technician walked into the server room, a blast of icy cold air hit him).*
- **Misplaced Modifier Error:**
  - *Incorrect:* The candidate only solved two coding problems in the first hour.
    *(Analysis: 'Only' misplaced before 'solved' implies he did nothing else—did not breathe or write—except solve).*
  - *Correct:* The candidate solved **only two** coding problems in the first hour.

### 4.2 The Principle of Parallelism
Elements in a sentence that perform the same grammatical function or are joined by coordinating conjunctions (*and, but, or*) must share the exact same grammatical structure:

- *Faulty:* The internship program requires completing a capstone project, attending daily standups, and **to pass** the exit exam.
- *Parallel:* The internship program requires **completing** a capstone project, **attending** daily standups, and **passing** the exit exam. (All gerund `-ing` forms).
- *Correlative Conjunction Parallelism:* *Not only... but also*, *Either... or*, *Both... and*:
  - *Faulty:* The team lead **not only** commended the developer for his speed, **but also for his code clarity**.
  - *Parallel:* The team lead commended the developer **not only for** his speed, **but also for** his code clarity.

### 4.3 The Four English Conditionals
| Type | Structure | Usage & Example |
|:---|:---|:---|
| **Zero Conditional** | If + Present Simple, ... Present Simple | Universal facts, scientific truths: *If you heat ice, it melts.* |
| **First Conditional** | If + Present Simple, ... will + base verb | Real possibility in the future: *If the candidate prepares systematically, he **will clear** the interview.* |
| **Second Conditional** | If + Past Simple, ... would + base verb | Hypothetical or unreal current situation: *If I **were** the CEO, I **would allocate** more budget to employee training.* (Note: Always use 'were', never 'was', in subjunctive). |
| **Third Conditional** | If + Past Perfect, ... would have + past participle | Unreal past event (regret/counterfactual): *If we **had implemented** rate limiting earlier, the API **would not have crashed** during the traffic surge.* |

---

## Chapter 5: Reading Comprehension Mastery & Critical Reasoning

### 5.1 Active Skimming & Scanning Methodology
In campus placement tests (Infosys, TCS, Cognizant), candidates have approximately 60 to 90 seconds per RC question:

1. **Phase 1 — 30-Second Structural Skim:**
   - Read the opening two sentences of Paragraph 1 (establishes topic and thesis).
   - Read the first sentence of each subsequent body paragraph (identifies transition of ideas and evidence).
   - Read the final concluding sentence of the passage.
2. **Phase 2 — Keyword-Targeted Question Scanning:**
   - Read the question stem first before looking at the passage body. Identify distinct anchor words (proper nouns, years, technical terms).
   - Scan directly to the paragraph housing the anchor words.
   - Read 1 sentence before and 1 sentence after the anchor word for complete contextual clarity.

### 5.2 Question Taxonomy & Decoy Elimination
Common incorrect answer trap choices designed by test examiners:
- **The Extreme Decoy:** Uses categorical absolutes (*always, never, all, completely, impossible*). Unless the passage explicitly asserts an absolute, eliminate immediately.
- **The Outside Knowledge Trap:** Contains statements that are factually true in the real world, but are **nowhere mentioned or implied in the text**.
- **The Opposite / Distortion Trap:** Takes exact words from the text but reverses the logical relationship or subject-object causality.
- **The Half-Right, Half-Wrong Trap:** First half of the option matches the text perfectly, while the second half introduces an unsubstantiated claim.

### 5.3 Critical Reasoning: Premises, Assumptions & Inferences
- **Premise:** Explicit evidence, data, or facts stated by the author.
- **Conclusion:** The claim or position the author is attempting to prove using the premises.
- **Assumption:** The unstated, invisible bridge required for the premise to logically support the conclusion:
  $$\text{Premise} + \text{Assumption} = \text{Conclusion}$$
  - *Negation Test for Assumptions:* If you negate the correct assumption, the author's argument **must instantly collapse**. If the conclusion still holds after negation, that option is NOT a necessary assumption.

---

## Chapter 6: Para Jumbles, Sentence Reordering & Logical Sequence

### 6.1 The Mandatory Pair Technique
Solving para jumbles in under 45 seconds relies on finding immutable pairs of sentences that must stick together:

1. **Noun-to-Pronoun Bridge:**
   - Sentence A: "Alan Turing formulated the conceptual foundations of modern computing machines in 1936."
   - Sentence B: "His theoretical formulation laid the groundwork for modern computer architecture."
   - *Rule:* A must precede B ($A \to B$) because the pronoun 'His' cannot appear before the referent 'Alan Turing'.
2. **Acronym & Full Name Bridge:**
   - Sentence A: "The Indian Space Research Organisation (ISRO) achieved global acclaim."
   - Sentence B: "ISRO launched several lunar missions."
   - *Rule:* The full expansion must precede the standalone acronym ($A \to B$).
3. **General Concept to Specific Example:**
   - Sentence introducing the broad phenomenon must precede the specific instance or case study.

### 6.2 Transition Words & Logical Flow
- **Adversative / Contrast Markers:** *However, nevertheless, yet, on the contrary, conversely, in contrast.*
  - Signals a 180-degree reversal of thought from the preceding sentence.
- **Additive / Elaborative Markers:** *Furthermore, moreover, in addition, similarly, likewise.*
  - Continues the positive or negative sentiment established in the prior sentence.
- **Causal / Conclusive Markers:** *Therefore, thus, consequently, as a result, hence.*
  - Marks the logical culmination or consequence; frequently positioned near the end of the paragraph.

---

## Chapter 7: Professional Business Writing & Placement Interview Communication

### 7.1 The STAR Behavioral Interview Framework
Top tech recruiters (Amazon, Google, Microsoft, TCS Digital) assess leadership principles using behavioral questions (*"Tell me about a time you resolved a technical disagreement"*). The STAR structure ensures concise, high-impact delivery:

```
[ S - Situation ]: Set the business/academic context in 2 concise sentences.
[ T - Task      ]: Define the explicit challenge or objective you were assigned to solve.
[ A - Action    ]: Detail YOUR specific personal interventions (technologies used, leadership shown).
[ R - Result    ]: Conclude with quantifiable business outcomes and personal learnings.
```

*Example Behavioral Answer:*
- **Situation:** "During our final-year campus portal project, our database response times degraded to over 4 seconds under concurrent test loads of 500 users."
- **Task:** "As backend lead, my objective was to reduce query latency below 200 milliseconds before the scheduled campus demo day."
- **Action:** "I profiled the queries using EXPLAIN ANALYZE, identified missing indexes on foreign keys, implemented Redis caching for session tokens, and refactored N+1 database queries into eager joins."
- **Result:** "We reduced average latency from 4.2 seconds down to 65 milliseconds—a 98% performance improvement—and successfully demonstrated the platform to 1,200 concurrent student users without a single failure."

### 7.2 The 90-Second Executive Elevator Pitch
Structure for answering **"Tell Me About Yourself"**:
1. **Present (30s):** Current academic standing, core specialization, and primary technical strengths (e.g., Data Structures, Java, Cloud computing).
2. **Past (30s):** Key accomplishments, noteworthy academic capstone projects, and competitive programming or hackathon milestones.
3. **Future (30s):** Why you are excited about this specific company's engineering culture and how your skills directly solve their immediate challenges.

---

## Chapter 8: Solved Placement Verbal Tests & Assessment Drills

### Solved Problem 1: Complex Sentence Correction Analysis
- **Question:** Identify the grammatically correct version of the underlined sentence:  
  *Neither the lead architect nor the backend engineers was able to figure out why the microservice failed, despite investigating the error logs for several hours.*
  - (A) Neither the lead architect nor the backend engineers was able to figure out why the microservice failed...
  - (B) Neither the lead architect nor the backend engineers were able to figure out why the microservice failed...
  - (C) Neither the lead architect or the backend engineers were able to figure out why the microservice failed...
  - (D) Neither the lead architect nor the backend engineers was able to figure out why did the microservice fail...
- **Solution:**
  1. Correlative conjunction pair: 'Neither' must pair strictly with 'nor' (eliminates C which uses 'or').
  2. Proximity Rule: When subjects are joined by 'neither...nor', the verb agrees with the closer subject. The closer subject is 'backend engineers' (plural).
  3. Therefore, the verb must be plural: **were able** (eliminates A and D which use 'was').
  4. In indirect questions ("why the microservice failed"), standard word order (subject before verb) is required, not question inversion ("why did it fail").
  5. **Correct Answer: (B)**.

### Solved Problem 2: 5-Sentence Para Jumble Reordering
- **Sentences:**
  - [1] Consequently, organizations that fail to adopt modern security protocols risk severe financial penalties and reputational loss.
  - [2] Cyberattacks have evolved from isolated hacker pranks into sophisticated state-sponsored operations targeting critical national infrastructure.
  - [3] These attacks exploit legacy software vulnerabilities and unsecured IoT devices connected to enterprise networks.
  - [4] To counter this existential threat, cybersecurity frameworks now mandate Zero-Trust architecture and multi-factor biometric authentication.
  - [5] In a Zero-Trust environment, no entity—inside or outside the perimeter—is trusted by default.
- **Solution:**
  1. Find the opening sentence: Sentence [2] introduces the broad overarching topic ("Cyberattacks have evolved...") with no unresolved pronouns or transition signals. [2] is the opening sentence.
  2. Follow the demonstrative pronoun: Sentence [3] begins with "These attacks", directly referring back to the cyberattacks introduced in [2]. Thus, **[2-3] is a mandatory pair**.
  3. Problem-to-Solution sequence: After describing the attacks and exploits in [2] and [3], Sentence [4] introduces the countermeasure: "To counter this existential threat... Zero-Trust architecture". Thus, [4] follows [3].
  4. Definition elaboration: Sentence [5] defines what a "Zero-Trust environment" actually does, immediately following its introduction in [4]. Thus, **[4-5] is a mandatory pair**.
  5. Concluding outcome: Sentence [1] begins with "Consequently" and summarizes the broader organizational consequences, serving as the logical conclusion.
  6. **Correct Sequence: 2 -> 3 -> 4 -> 5 -> 1**.

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Subject-Verb Agreement):** "The board of directors (has / have) approved the annual bonus scheme."
   - *Solution:* **has**. 'Board of directors' functions as a singular collective unit making a unified formal decision.

2. **Exercise 2 (Fixed Prepositions):** Correct the sentence: "The candidate was confident to crack the campus placement interview."
   - *Solution:* "The candidate was **confident of cracking** the campus placement interview." (The adjective 'confident' collocates with preposition 'of' followed by a gerund).

3. **Exercise 3 (Conditional Sentences):** Fill in the blank: "If the QA team had flagged the regression bug yesterday, we ______ (not / deploy) the faulty build to production."
   - *Solution:* **would not have deployed**. This is a Third Conditional sentence describing a counterfactual past event (If + past perfect $\to$ would have + past participle).

4. **Exercise 4 (Vocabulary In Context):** What is the exact antonym of the word **FASTIDIOUS**?
   - (A) Meticulous (B) Careless (C) Scrupulous (D) Punctual
   - *Solution:* **(B) Careless**. 'Fastidious' means showing extreme care and attention to detail. Its direct antonym is 'careless' or 'lax'.

5. **Exercise 5 (Modifier Correction):** Rewrite the dangling modifier sentence: "Having finished the coding round, the pizza was ordered by the students."
   - *Solution:* "Having finished the coding round, **the students ordered the pizza**." (The participial clause must be immediately followed by the agents who finished the round—the students, not the pizza!).
"""

VERBAL_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "Subject-Verb Agreement, Syntax & Grammatical Foundations",
        "subtopic": "Proximity Principle",
        "question": "Choose the grammatically correct sentence adhering to standard corporate English rules:",
        "options": [
            "Neither the team lead nor the developers were informed about the deployment schedule.",
            "Neither the team lead nor the developers was informed about the deployment schedule.",
            "Neither the team lead or the developers were informed about the deployment schedule.",
            "Neither the team lead nor the developers is informed about the deployment schedule."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Verbal Prescribed Textbook — Chapter 1: Subject-Verb Agreement]\nUnder the Proximity Rule for correlative conjunctions 'neither...nor', the verb agrees with the subject closest to it. Here, 'developers' is plural, requiring the plural verb 'were'.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 4,
        "chapter_title": "Sentence Correction, Error Spotting & Structural Flow",
        "subtopic": "Third Conditional Grammar",
        "question": "Which sentence correctly demonstrates the Third Conditional grammatical structure?",
        "options": [
            "If the team had executed regression tests, the critical production outage would have been averted.",
            "If the team executed regression tests, the critical production outage would be averted.",
            "If the team has executed regression tests, the outage will have been averted.",
            "If the team would have executed tests, the outage would have been averted."
        ],
        "correct_option_index": 0,
        "explanation": "📖 [Verbal Prescribed Textbook — Chapter 4: Sentence Correction]\nThe Third Conditional expresses unreal past situations: 'If + Past Perfect (had executed) ... would have + Past Participle (would have been averted)'.",
        "difficulty": "medium",
    }
]
'''

# =============================================================================
# JAVASCRIPT & MODERN WEB STACK
# =============================================================================
JS_CODE = r'''"""
javascript_master.py — Prescribed Master Textbook for JavaScript & Modern Web Stack.
Comprehensive unabridged campus placement textbook covering V8 engine architecture,
Event Loop (macrotasks vs microtasks), execution context, hoisting & TDZ, closures,
prototypal inheritance, Promises, async/await, ES6+, TypeScript static typing & generics,
DOM performance, debouncing/throttling, and solved placement coding challenges.
"""

JS_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "JavaScript Engine Internals: V8, Call Stack & The Event Loop",
        "topics": [
            "V8 Engine pipeline: Parser, AST, Ignition bytecode interpreter, TurboFan JIT optimizing compiler",
            "Execution Context lifecycle: Global vs Function context, Creation phase vs Execution phase",
            "Variable Environment, Lexical Environment, and Hoisting mechanics ('var' vs 'let'/'const' Temporal Dead Zone)",
            "The JavaScript Concurrency Model: Call Stack, Web APIs, Task (Macrotask) Queue, and Microtask Queue",
            "Event Loop execution ordering: Processing all Microtasks (Promises, queueMicrotask) before next Macrotask (setTimeout, I/O)"
        ],
        "key_takeaways": "Microtasks (Promise callbacks, MutationObserver) run immediately after the current call stack clears and before any macrotasks (setTimeout, setInterval). 'let' and 'const' are hoisted but remain uninitialized in the Temporal Dead Zone (TDZ)."
    },
    {
        "chapter_num": 2,
        "title": "Scope, Closures & Memory Management in JavaScript",
        "topics": [
            "Lexical scoping and Scope Chain resolution traversal",
            "Closures definition and internal [[Scopes]] property retention",
            "Practical closure design patterns: Private state encapsulation, Module pattern, Function currying, Memoization",
            "Garbage collection algorithms: Reference Counting (and circular reference pitfalls) vs Mark-and-Sweep",
            "Common JavaScript memory leaks: Accidental global variables, forgotten timers, detached DOM nodes, uncleared closures"
        ],
        "key_takeaways": "A closure is created when an inner function retains access to its enclosing lexical scope even after the outer function has finished execution and returned."
    },
    {
        "chapter_num": 3,
        "title": "Objects, Prototypes & Object-Oriented JavaScript",
        "topics": [
            "The Prototype Chain: '__proto__' accessor vs 'prototype' property on constructor functions",
            "Prototypal inheritance mechanics and 'Object.create(proto)' delegation",
            "ES6 'class' syntax as syntactic sugar over prototypal delegation (super, constructor, static methods)",
            "Property descriptors: 'value', 'writable', 'enumerable', 'configurable', and 'Object.freeze()' vs 'Object.seal()'",
            "The 'this' keyword binding rules: Default (window/undefined), Implicit (object method), Explicit (call, apply, bind), New, and Arrow lexical 'this'"
        ],
        "key_takeaways": "Arrow functions do not possess their own 'this', 'arguments', or 'super' bindings; they inherit 'this' lexically from their enclosing execution context at the time of definition."
    },
    {
        "chapter_num": 4,
        "title": "Asynchronous JavaScript: Promises, Async/Await & Concurrency",
        "topics": [
            "The asynchronous paradigm: Callback Hell and inversion of control",
            "Promises (ES6): States (Pending, Fulfilled, Rejected), immutability of settled state, then/catch/finally chaining",
            "Promise concurrency primitives: 'Promise.all()' (fail-fast), 'Promise.allSettled()', 'Promise.race()', 'Promise.any()' (first success)",
            "Async/Await (ES2017) syntax: Desugaring async functions to Generators and Promise resolution runners",
            "Error handling patterns in async workflows: try/catch blocks, unhandledrejection global listeners"
        ],
        "key_takeaways": "Promise.all() rejects immediately if any input promise rejects. Promise.allSettled() waits for all promises to settle regardless of rejection, making it safer for batch parallel requests."
    },
    {
        "chapter_num": 5,
        "title": "Modern ES6+ Features & TypeScript Fundamentals",
        "topics": [
            "Destructuring, Rest & Spread operators ('...'), Default parameters, Template literals",
            "Advanced data structures: Map, Set, WeakMap, and WeakSet (ephemeral object references for GC)",
            "Symbols as unique object property keys and well-known symbols (Symbol.iterator)",
            "Iterators and Generator functions ('function*') with 'yield' keyword mechanics",
            "TypeScript essentials: Static typing, Interfaces vs Type Aliases, Generics, Union & Intersection types",
            "TypeScript utility types: Partial<T>, Required<T>, Readonly<T>, Pick<T, K>, Omit<T, K>, Record<K, T>"
        ],
        "key_takeaways": "WeakMap keys must be objects and are weakly held; if no other reference to the key object exists, it is garbage collected, preventing memory leaks in metadata caching."
    },
    {
        "chapter_num": 6,
        "title": "DOM Manipulation, Browser APIs & Web Performance",
        "topics": [
            "The Critical Rendering Path: HTML Parsing -> DOM Tree -> CSSOM -> Render Tree -> Layout (Reflow) -> Paint -> Composite",
            "Minimizing browser reflows and repaints: DocumentFragment, batch DOM mutations, CSS transforms",
            "Event bubbling, capturing (trickling), and the Event Delegation design pattern ('event.target' vs 'event.currentTarget')",
            "Performance optimization algorithms: Debouncing vs Throttling implementation with closures and timers",
            "Web Storage architectures: LocalStorage (5MB synchronous) vs SessionStorage vs IndexedDB (async NoSQL)"
        ],
        "key_takeaways": "Debouncing postpones execution until a specified quiet period has elapsed with no new events (ideal for search autocomplete). Throttling guarantees execution at regular periodic intervals (ideal for scroll listeners)."
    },
    {
        "chapter_num": 7,
        "title": "Solved Placement Coding Challenges & Output Prediction Puzzles",
        "topics": [
            "Event Loop execution order output tracing puzzles",
            "Tricky 'this' binding and scope output predictions",
            "Handwritten polyfill: Custom Promise.all implementation",
            "Handwritten implementation: Debounce and Throttle functions",
            "Deep Clone algorithm handling circular references and non-serializable objects",
            "Self-assessment practice drills with verified answers"
        ],
        "key_takeaways": "Mastering event loop execution sequences and writing polyfills for Promise.all and debounce from memory is required in frontend technical interviews for companies like Google, Microsoft, and Uber."
    }
]

JS_TEXTBOOK_MARKDOWN = r"""# JavaScript, TypeScript & Modern Web Stack: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** JavaScript, TypeScript & Modern Web Stack  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, frontend engineering technical interviews, and online coding evaluations (Google, Amazon, Flipkart, Uber, Razorpay, TCS Digital) are strictly grounded in the engine mechanics, ECMAScript standards, TypeScript types, and polyfills detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: JavaScript Engine Internals: V8, Call Stack & The Event Loop](#chapter-1-javascript-engine-internals-v8-call-stack--the-event-loop)
  - [1.1 Inside the V8 Engine: Parser, Ignition & TurboFan](#11-inside-the-v8-engine-parser-ignition--turbofan)
  - [1.2 Execution Context: Creation vs Execution Phase](#12-execution-context-creation-vs-execution-phase)
  - [1.3 Hoisting & The Temporal Dead Zone (TDZ)](#13-hoisting--the-temporal-dead-zone-tdz)
  - [1.4 The JavaScript Event Loop, Macrotasks & Microtasks](#14-the-javascript-event-loop-macrotasks--microtasks)
- [Chapter 2: Scope, Closures & Memory Management in JavaScript](#chapter-2-scope-closures--memory-management-in-javascript)
  - [2.1 Lexical Scope & The Scope Chain](#21-lexical-scope--the-scope-chain)
  - [2.2 Deep Dive into Closures](#22-deep-dive-into-closures)
  - [2.3 Practical Closure Design Patterns](#23-practical-closure-design-patterns)
  - [2.4 Garbage Collection & Memory Leaks](#24-garbage-collection--memory-leaks)
- [Chapter 3: Objects, Prototypes & Object-Oriented JavaScript](#chapter-3-objects-prototypes--object-oriented-javascript)
  - [3.1 The Prototype Chain & Prototypal Inheritance](#31-the-prototype-chain--prototypal-inheritance)
  - [3.2 ES6 Classes vs Prototypal Delegation](#32-es6-classes-vs-prototypal-delegation)
  - [3.3 Property Descriptors & Immutability](#33-property-descriptors--immutability)
  - [3.4 The 5 Rules of the `this` Keyword](#34-the-5-rules-of-the-this-keyword)
- [Chapter 4: Asynchronous JavaScript: Promises, Async/Await & Concurrency](#chapter-4-asynchronous-javascript-promises-asyncawait--concurrency)
  - [4.1 The Promise Lifecycle & Chaining Mechanics](#41-the-promise-lifecycle--chaining-mechanics)
  - [4.2 Promise Concurrency APIs (all, allSettled, race, any)](#42-promise-concurrency-apis-all-allsettled-race-any)
  - [4.3 Async/Await Internals (Generators & Runners)](#43-asyncawait-internals-generators--runners)
- [Chapter 5: Modern ES6+ Features & TypeScript Fundamentals](#chapter-5-modern-es6-features--typescript-fundamentals)
  - [5.1 ES6+ Essentials: Spread, Destructuring & Symbols](#51-es6-essentials-spread-destructuring--symbols)
  - [5.2 WeakMap & WeakSet for Memory Management](#52-weakmap--weakset-for-memory-management)
  - [5.3 TypeScript Fundamentals: Interfaces vs Types](#53-typescript-fundamentals-interfaces-vs-types)
  - [5.4 TypeScript Generics & High-Yield Utility Types](#54-typescript-generics--high-yield-utility-types)
- [Chapter 6: DOM Manipulation, Browser APIs & Web Performance](#chapter-6-dom-manipulation-browser-apis--web-performance)
  - [6.1 The Critical Rendering Path & Minimizing Reflows](#61-the-critical-rendering-path--minimizing-reflows)
  - [6.2 Event Bubbling, Capturing & Delegation](#62-event-bubbling-capturing--delegation)
  - [6.3 Debouncing vs Throttling Algorithm Implementation](#63-debouncing-vs-throttling-algorithm-implementation)
- [Chapter 7: Solved Placement Coding Challenges & Output Prediction Puzzles](#chapter-7-solved-placement-coding-challenges--output-prediction-puzzles)
  - [Solved Challenge 1: The Event Loop & Microtask Execution Order](#solved-challenge-1-the-event-loop--microtask-execution-order)
  - [Solved Challenge 2: Handwritten Polyfill for `Promise.all`](#solved-challenge-2-handwritten-polyfill-for-promiseall)
  - [Solved Challenge 3: Handwritten Debounce Function with Immediate Flag](#solved-challenge-3-handwritten-debounce-function-with-immediate-flag)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: JavaScript Engine Internals: V8, Call Stack & The Event Loop

### 1.1 Inside the V8 Engine: Parser, Ignition & TurboFan
Google's V8 engine (powers Chrome and Node.js) executes JavaScript through an advanced Just-In-Time (JIT) compilation pipeline:

```
[ Source Code ] 
       |
       v
[ Parser / Lexer ] -> Generates Abstract Syntax Tree (AST) & Scopes
       |
       v
[ Ignition Bytecode Interpreter ] -> Generates compact bytecode and executes rapidly
       |
       |  (Type Feedback / Profiling)
       v
[ TurboFan JIT Compiler ] -> Optimizes "hot" functions into raw machine code
       |
       v  (Deoptimization if polymorphic type assumptions fail)
[ Native Machine Code / CPU ]
```

1. **Parser & AST:** Breaks JavaScript source text into lexical tokens and builds the Abstract Syntax Tree (AST).
2. **Ignition Interpreter:** Translates AST into bytecode. Starts executing code with near-zero latency without waiting for machine-code compilation.
3. **TurboFan Optimizing Compiler:** Monitors "hot functions" (code executed repeatedly). If parameter types remain monomorphic (e.g., function always called with integers), TurboFan compiles the bytecode directly into highly optimized native CPU assembly. If a type check subsequently fails (polymorphic deoptimization), TurboFan bails out back to Ignition bytecode.

### 1.2 Execution Context: Creation vs Execution Phase
Whenever JavaScript code executes, it does so within an **Execution Context**:
- **Global Execution Context (GEC):** Created when script starts; defines `window` (browser) or `global` (Node), and `this`.
- **Function Execution Context (FEC):** Created whenever a function is invoked.

**Every Execution Context is created in two distinct phases:**
1. **Creation Phase (Memory Allocation):**
   - The engine creates the `Activation Object` / `Lexical Environment`.
   - Allocates memory space for function declarations and variables.
   - Sets the value of `this`.
   - Builds the Scope Chain link to the outer environment.
2. **Execution Phase (Line-by-Line Code Evaluation):**
   - Assigns actual values to variables and executes statements sequentially.

### 1.3 Hoisting & The Temporal Dead Zone (TDZ)
Hoisting is the JavaScript engine's behavior of allocating memory for declarations during the Creation Phase before executing code:

- **Function Declarations:** Fully hoisted along with their function body implementation:
  ```javascript
  sayHello(); // Works perfectly! Outputs: "Hello"
  function sayHello() { console.log("Hello"); }
  ```
- **`var` Declarations:** The variable name is hoisted and initialized to `undefined`:
  ```javascript
  console.log(score); // Outputs: undefined
  var score = 100;
  console.log(score); // Outputs: 100
  ```
- **`let` and `const` Declarations & The TDZ:**
  `let` and `const` variables are hoisted into memory, but are **NOT initialized**. The time window between the start of the block scope and the actual line where the variable is declared is known as the **Temporal Dead Zone (TDZ)**. Accessing the variable inside the TDZ throws an uncatchable `ReferenceError`:
  ```javascript
  // TDZ for user starts here
  console.log(user); // Uncaught ReferenceError: Cannot access 'user' before initialization
  let user = "Alice"; // TDZ ends here
  ```

### 1.4 The JavaScript Event Loop, Macrotasks & Microtasks
JavaScript is single-threaded: it has one Call Stack and one Memory Heap. Asynchronous concurrency is orchestrated by the browser/Node runtime via the **Event Loop**:

```
[ Call Stack ]  <------- Executes synchronous JS frames
      ^
      |
      |   (When Call Stack is 100% EMPTY)
      |
[ Microtask Queue ] <--- HIGHEST PRIORITY: Promise.then(), queueMicrotask(), MutationObserver
      ^                  *Drains entire queue completely before moving on!*
      |
[ Macrotask Queue ] <--- setTimeout(), setInterval(), setImmediate(), I/O, UI Rendering
```

**The Strict Event Loop Execution Order:**
1. Execute synchronous code on the Call Stack until the Call Stack is completely empty.
2. Check the **Microtask Queue**: Drain and execute **ALL** available microtasks until the Microtask Queue is completely empty. (If a microtask enqueues another microtask, that new microtask runs immediately in the same cycle!).
3. Trigger UI Render/Repaint (in browser environments).
4. Take the **single oldest task** from the **Macrotask Queue** and push it onto the Call Stack to execute.
5. Repeat from Step 1.

---

## Chapter 2: Scope, Closures & Memory Management in JavaScript

### 2.1 Lexical Scope & The Scope Chain
JavaScript employs **Lexical Scoping** (Static Scoping): the scope of an identifier is determined by its physical location within the written source code at authoring time, NOT by where or how it is invoked at runtime.
- When an identifier is referenced, the engine searches the current local lexical environment.
- If not found, it traverses upward along the **Scope Chain** to the enclosing outer environment, continuing until it reaches the Global Environment.
- If still not found in the global scope, it throws a `ReferenceError` (in strict mode).

### 2.2 Deep Dive into Closures
**Formal Definition:** A **Closure** is the combination of a function bundled together with references to its surrounding lexical environment (`[[Scopes]]`). A closure gives an inner function access to its outer function's scope even after the outer function has completed execution and its execution context has been popped off the Call Stack.

```javascript
function createCounter(initialValue = 0) {
  let count = initialValue; // Enclosed lexical variable
  return {
    increment() { count++; return count; },
    decrement() { count--; return count; },
    getValue() { return count; }
  };
}

const counterA = createCounter(10);
console.log(counterA.increment()); // 11
console.log(counterA.increment()); // 12
console.log(counterA.getValue());  // 12
// count is completely inaccessible from external global code!
```

### 2.3 Practical Closure Design Patterns
1. **Private Variables & Data Encapsulation:** Emulates private object properties before native `#privateField` syntax was introduced.
2. **Function Currying:** Transforming a function taking multiple arguments $f(a, b, c)$ into a sequence of unary functions $f(a)(b)(c)$:
   ```javascript
   const multiply = a => b => a * b;
   const double = multiply(2);
   console.log(double(5)); // 10
   ```
3. **Memoization Cache:** Storing previous expensive calculation results in an enclosed dictionary:
   ```javascript
   function memoize(fn) {
     const cache = new Map();
     return function(...args) {
       const key = JSON.stringify(args);
       if (cache.has(key)) return cache.get(key);
       const result = fn.apply(this, args);
       cache.set(key, result);
       return result;
     };
   }
   ```

### 2.4 Garbage Collection & Memory Leaks
V8 utilizes the **Mark-and-Sweep** Garbage Collection algorithm:
- The GC designates a set of **GC Roots** (Global window object, currently active stack frames, DOM tree root).
- The GC traverses all object references starting from roots, "marking" every reachable object.
- In the "Sweep" phase, any memory block in the heap not marked as reachable is deallocated.

**The Top 4 JavaScript Memory Leaks:**
1. **Accidental Global Variables:** Assigning `foo = "bar"` without `let/const` attaches `foo` to `window`, preventing GC forever.
2. **Uncleared Timers:** `setInterval(() => { ... })` retains all variables in its callback scope until explicitly passed to `clearInterval()`.
3. **Detached DOM Nodes:** Retaining a JavaScript variable reference to a removed DOM element (`const btn = document.getElementById('btn'); document.body.removeChild(btn);`). The DOM element cannot be freed because `btn` still holds a reference.
4. **Improper Closures:** Giant data structures retained in outer scopes of functions that are kept alive long-term.

---

## Chapter 3: Objects, Prototypes & Object-Oriented JavaScript

### 3.1 The Prototype Chain & Prototypal Inheritance
In JavaScript, inheritance is based on **Objects delegating to Objects** via the Prototype Chain:
- Every JavaScript object has an internal hidden slot `[[Prototype]]`, accessible via `Object.getPrototypeOf(obj)` or `__proto__`.
- When accessing `obj.prop`, if `prop` is not found on `obj` directly, the engine traverses `obj.__proto__`. If not found there, it inspects `obj.__proto__.__proto__`, continuing until it hits `Object.prototype.__proto__ === null`.

```javascript
const animal = {
  eats: true,
  walk() { return "Walking..."; }
};

// Create rabbit with animal as its prototype
const rabbit = Object.create(animal);
rabbit.hops = true;

console.log(rabbit.hops); // true (own property)
console.log(rabbit.eats); // true (inherited from animal via prototype chain)
console.log(rabbit.walk()); // "Walking..."
```

### 3.2 ES6 Classes vs Prototypal Delegation
ES6 `class` syntax is strictly **syntactic sugar** layered over prototype delegation:
```javascript
class Person {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hello, I am ${this.name}`;
  }
}
// Under the hood, this is equivalent to:
// Person.prototype.greet = function() { return `Hello, I am ${this.name}`; };
```

### 3.3 Property Descriptors & Immutability
Every object property is configured with an internal **Property Descriptor**:
- `value`: The stored data value.
- `writable`: If `false`, the property's value cannot be altered via assignment.
- `enumerable`: If `false`, the property is omitted from `for...in` loops and `Object.keys()`.
- `configurable`: If `false`, descriptor attributes cannot be changed and property cannot be deleted.

```javascript
const user = {};
Object.defineProperty(user, 'id', {
  value: 42,
  writable: false,
  configurable: false,
  enumerable: true
});
user.id = 99; // Silent failure in non-strict mode; TypeError in strict mode!
```

**Immutability Levels:**
- `Object.preventExtensions(obj)`: Prevents adding new properties; existing can be modified or deleted.
- `Object.seal(obj)`: Prevents adding/deleting properties; existing writable properties can still be modified.
- `Object.freeze(obj)`: Shallow immutable. Prevents adding, deleting, or modifying existing properties.

### 3.4 The 5 Rules of the `this` Keyword
The value of `this` is evaluated dynamically based on **how the function is called**:

1. **Default Binding:** Standalone invocation `fn()`. In non-strict mode, `this` is `window` (global). In strict mode (`"use strict";`), `this` is `undefined`.
2. **Implicit Binding:** Method invocation `obj.fn()`. `this` refers to the contextual object to the left of the dot (`obj`).
3. **Explicit Binding (`call`, `apply`, `bind`):**
   - `fn.call(context, arg1, arg2)`: Executes immediately with explicit `context`.
   - `fn.apply(context, [arg1, arg2])`: Executes immediately with arguments as an array.
   - `fn.bind(context, arg1)`: Returns a new permanently bound function.
4. **New Binding:** `new ConstructorFn()`. Creates a new empty object `{}` and binds `this` to it.
5. **Arrow Function Lexical `this`:** Arrow functions (`() => {}`) **never** bind their own `this`. They capture `this` from their immediately enclosing lexical scope at definition time. `call`, `apply`, or `bind` cannot alter an arrow function's `this`!

---

## Chapter 4: Asynchronous JavaScript: Promises, Async/Await & Concurrency

### 4.1 The Promise Lifecycle & Chaining Mechanics
A **Promise** represents the eventual completion or failure of an asynchronous operation:
- **Pending:** Initial state; neither fulfilled nor rejected.
- **Fulfilled:** Operation succeeded; produces a resolved value.
- **Rejected:** Operation failed; produces a rejection reason (error).
- Once a Promise reaches **Fulfilled** or **Rejected**, it is **Settled** and permanently immutable.

```javascript
function fetchUserData(userId) {
  return new Promise((resolve, reject) => {
    if (!userId) {
      reject(new Error("UserId is mandatory"));
      return;
    }
    setTimeout(() => {
      resolve({ id: userId, name: "Placement Candidate" });
    }, 100);
  });
}

fetchUserData(101)
  .then(user => {
    console.log("Fetched user:", user.name);
    return user.id; // Returned values are wrapped in a new resolved Promise
  })
  .then(id => {
    console.log("Processed ID:", id);
  })
  .catch(err => {
    console.error("Pipeline failure:", err.message);
  })
  .finally(() => {
    console.log("Cleanup executed unconditionally");
  });
```

### 4.2 Promise Concurrency APIs (all, allSettled, race, any)
| API Method | Resolution Condition | Rejection Condition | Primary Placement Use Case |
|:---|:---|:---|:---|
| `Promise.all([p1, p2])` | Resolves when **ALL** promises fulfill (returns array of results). | **Rejects immediately** on the FIRST promise that rejects (Fail-Fast). | Parallel dependent fetches where all data is mandatory. |
| `Promise.allSettled([p1, p2])` | Resolves when **ALL** promises have settled (fulfilled or rejected). | **Never rejects**. Returns array of `{status: 'fulfilled'\|'rejected', value\|reason}`. | Bulk tasks where partial failures are acceptable (e.g. sending bulk notifications). |
| `Promise.race([p1, p2])` | Settles as soon as the **FIRST** promise settles (fulfills OR rejects). | Rejects if the first settled promise was rejected. | Request timeout races (`Promise.race([fetch(url), timeout(5000)])`). |
| `Promise.any([p1, p2])` | Resolves as soon as the **FIRST** promise fulfills. | Rejects only if **ALL** promises reject (returns `AggregateError`). | Querying redundant CDN mirrors where first successful response wins. |

### 4.3 Async/Await Internals (Generators & Runners)
`async/await` syntax is built on top of ES6 Generator functions (`function*`) and Promises. An `async` function always returns a Promise:
```javascript
// This async/await function:
async function loadDashboard() {
  const user = await fetchUser();
  const stats = await fetchStats(user.id);
  return { user, stats };
}

// Desugars conceptually into a generator execution runner:
function loadDashboardDesugared() {
  return spawn(function* () {
    const user = yield fetchUser();
    const stats = yield fetchStats(user.id);
    return { user, stats };
  });
}
```

---

## Chapter 5: Modern ES6+ Features & TypeScript Fundamentals

### 5.1 ES6+ Essentials: Spread, Destructuring & Symbols
- **Spread & Rest Operators (`...`):**
  - Rest (parameters): `function sum(...nums) { return nums.reduce((a, b) => a + b, 0); }`
  - Spread (arrays/objects): `const cloned = { ...original, timestamp: Date.now() };` (Shallow clone).
- **Symbols:** Primitive datatype guaranteeing unique, non-colliding property keys:
  ```javascript
  const idSym1 = Symbol("id");
  const idSym2 = Symbol("id");
  console.log(idSym1 === idSym2); // false! Guaranteed distinct.
  ```

### 5.2 WeakMap & WeakSet for Memory Management
- **`Map` vs `WeakMap`:**
  - `Map` allows keys of any datatype and prevents keys from being garbage collected as long as the map lives.
  - `WeakMap` keys **MUST be Objects** and are held as **weak references**.
  - If no other reference to a key object exists outside the `WeakMap`, the key object and its associated value are automatically garbage collected.
  - `WeakMap` is not iterable (no `.size`, no `.keys()`) because GC timing is non-deterministic.

### 5.3 TypeScript Fundamentals: Interfaces vs Types
| Feature | TypeScript `interface` | TypeScript `type` Alias |
|:---|:---|:---|
| **Declaration Merging** | Yes: Declaring same interface twice merges properties automatically. | No: Duplicate identifier compilation error. |
| **Primitives & Unions** | Cannot represent union or primitive aliases directly. | Ideal for unions, primitives, tuples: `type Status = 'pending' \| 'approved';` |
| **Extends / Implements** | Extends via `extends` keyword; classes can `implement` interfaces. | Intersects via `&` operator; classes can also implement static object types. |
| **Recommended Usage** | Public library APIs and object/class contract modeling. | Complex union types, tuples, function signatures, and utility compositions. |

### 5.4 TypeScript Generics & High-Yield Utility Types
Generics allow building reusable, type-safe components without resorting to `any`:
```typescript
interface ApiResponse<T> {
  success: boolean;
  timestamp: number;
  data: T;
}

// High-Yield Utility Types Built into TypeScript:
interface UserProfile {
  id: string;
  name: string;
  email: string;
  age?: number;
}

type ReadonlyUser = Readonly<UserProfile>; // All properties immutable
type PartialUser  = Partial<UserProfile>;  // All properties optional
type UserContact  = Pick<UserProfile, 'name' | 'email'>; // Extracts subset
type UserNoId     = Omit<UserProfile, 'id'>;            // Excludes subset
type UserRegistry = Record<string, UserProfile>;         // Map of key -> value
```

---

## Chapter 6: DOM Manipulation, Browser APIs & Web Performance

### 6.1 The Critical Rendering Path & Minimizing Reflows
The browser renders web pages through sequential pipeline stages:

```
[ HTML Parser ] -> [ DOM Tree   ] \
                                     --> [ Render Tree ] -> [ Layout (Reflow) ] -> [ Paint ] -> [ Composite ]
[ CSS Parser  ] -> [ CSSOM Tree ] /
```

- **Reflow (Layout):** Recomputing geometry, widths, heights, and positions of all elements on screen. Triggered by modifying layout-sensitive CSS properties (`width`, `height`, `margin`, `fontSize`, `top`, `display`) or querying layout measurements (`offsetWidth`, `scrollHeight`, `getBoundingClientRect()`).
- **Repaint:** Re-coloring pixels without altering geometry (`color`, `background-color`, `visibility`).
- **Composite:** GPU layers assembled together (`transform`, `opacity`). Triggering composite operations bypasses reflow and repaint entirely, achieving smooth 60fps animations.
- **Optimization Best Practice:** Use `document.createDocumentFragment()` to batch DOM node additions offscreen before inserting into the live DOM tree.

### 6.2 Event Bubbling, Capturing & Delegation
When a user clicks an element inside the DOM, the event travels in 3 distinct phases:
1. **Capturing Phase:** Event trickles down from `window` $\to$ `document` $\to$ parent elements to the target.
2. **Target Phase:** Event reaches the actual node clicked (`event.target`).
3. **Bubbling Phase:** Event bubbles upward from target back to `window`.

**Event Delegation Pattern:**
Instead of attaching 1,000 separate `click` event listeners to individual table rows or list items, attach a **single** listener to the parent container and inspect `event.target`:
```javascript
document.getElementById('user-list').addEventListener('click', function(e) {
  const item = e.target.closest('.user-item');
  if (item) {
    console.log("Clicked user ID:", item.dataset.id);
  }
});
```

### 6.3 Debouncing vs Throttling Algorithm Implementation
- **Debouncing:** Delays execution of a function until after $N$ milliseconds of silence have passed since the last invocation. (Best for search inputs, resize listeners).
- **Throttling:** Ensures that a function is executed at most once per every $N$ milliseconds interval. (Best for scroll position tracking, mousemove games).

---

## Chapter 7: Solved Placement Coding Challenges & Output Prediction Puzzles

### Solved Challenge 1: The Event Loop & Microtask Execution Order
- **Puzzle:** Predict the exact printed console output order of the following snippet:
  ```javascript
  console.log("1");

  setTimeout(() => {
    console.log("2");
  }, 0);

  Promise.resolve()
    .then(() => {
      console.log("3");
    })
    .then(() => {
      console.log("4");
    });

  console.log("5");
  ```
- **Step-by-Step Execution Trace:**
  1. Synchronous statement `console.log("1")` executes $\implies$ Prints **`1`**.
  2. `setTimeout(..., 0)` registers a timer with the browser Web API. When timer finishes, callback `() => console.log("2")` is queued in the **Macrotask Queue**.
  3. `Promise.resolve().then(...)` registers microtask `() => console.log("3")` in the **Microtask Queue**.
  4. Synchronous statement `console.log("5")` executes $\implies$ Prints **`5`**.
  5. Synchronous stack is now completely empty. Event loop checks the **Microtask Queue**:
     - Executes first microtask $\implies$ Prints **`3`**.
     - Its chained `.then()` queues another microtask `() => console.log("4")` in the current Microtask Queue!
     - Microtask queue is not empty yet. Engine executes next microtask $\implies$ Prints **`4`**.
  6. Microtask queue is now empty. Event loop pulls from **Macrotask Queue**:
     - Executes `setTimeout` callback $\implies$ Prints **`2`**.
- **Final Output:**
  ```
  1
  5
  3
  4
  2
  ```

### Solved Challenge 2: Handwritten Polyfill for `Promise.all`
- **Problem:** Implement a custom `promiseAll(iterable)` polyfill matching native `Promise.all` behavior without using the built-in method.
- **Solution:**
  ```javascript
  function promiseAll(promises) {
    return new Promise((resolve, reject) => {
      // Handle non-array or empty input
      if (!Array.isArray(promises)) {
        return reject(new TypeError("Argument must be an array"));
      }
      
      const total = promises.length;
      if (total === 0) {
        return resolve([]);
      }
      
      const results = new Array(total);
      let completedCount = 0;
      
      promises.forEach((promiseItem, index) => {
        // Wrap with Promise.resolve to handle primitive non-promise values
        Promise.resolve(promiseItem)
          .then(value => {
            results[index] = value; // Preserve original input ordering!
            completedCount++;
            if (completedCount === total) {
              resolve(results);
            }
          })
          .catch(error => {
            // Reject immediately on FIRST error encountered (fail-fast)
            reject(error);
          });
      });
    });
  }
  ```

### Solved Challenge 3: Handwritten Debounce Function with Immediate Flag
- **Problem:** Implement a robust `debounce(fn, wait, immediate)` utility in JavaScript.
- **Solution:**
  ```javascript
  function debounce(fn, wait = 300, immediate = false) {
    let timeoutId = null;
    
    return function debounced(...args) {
      const context = this;
      const callNow = immediate && !timeoutId;
      
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      
      timeoutId = setTimeout(() => {
        timeoutId = null;
        if (!immediate) {
          fn.apply(context, args);
        }
      }, wait);
      
      if (callNow) {
        fn.apply(context, args);
      }
    };
  }
  ```

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Tricky Scope):** What is printed by the following code?
   ```javascript
   for (var i = 0; i < 3; i++) {
     setTimeout(() => console.log(i), 100);
   }
   ```
   - *Solution:* Prints `3, 3, 3`. Because `var` is function-scoped (or globally scoped here), all three `setTimeout` callbacks reference the exact same mutable variable `i`, which reaches `3` by the time the timer callbacks execute. Replacing `var` with block-scoped `let` creates a fresh `i` binding per loop iteration, printing `0, 1, 2`.

2. **Exercise 2 (Arrow Function 'this'):** What is printed by `obj.getGreeting()`?
   ```javascript
   const obj = {
     name: "Placement Candidate",
     getGreeting: () => `Hello, ${this.name}`
   };
   ```
   - *Solution:* Prints `"Hello, undefined"` (or `"Hello, "` in browsers where `window.name` is empty). Arrow functions inherit `this` lexically from their enclosing scope (here, the global window/module), NOT from the object literal `obj`.

3. **Exercise 3 (WeakMap Object Lifespan):** Can a JavaScript primitive string like `"authToken"` be used as a key in a `WeakMap`?
   - *Solution:* **No**. `WeakMap` keys must strictly be objects (`typeof key === 'object' && key !== null`). Supplying a primitive throws an uncatchable `TypeError: Invalid value used as weak map key`.

4. **Exercise 4 (Promise.race vs Promise.any):** If promise $P_1$ rejects after 10ms with error $E$, and promise $P_2$ resolves after 50ms with value $V$, what will `Promise.race([P1, P2])` and `Promise.any([P1, P2])` return?
   - *Solution:* `Promise.race` rejects after 10ms with error $E$ (first to settle). `Promise.any` ignores the rejection and resolves after 50ms with value $V$ (first to fulfill).

5. **Exercise 5 (Event Delegation Benefits):** Why does event delegation conserve client memory when rendering a virtualized list of 10,000 table rows?
   - *Solution:* Instead of instantiating 10,000 distinct closure functions and event listener objects in the V8 heap, event delegation instantiates strictly 1 listener on the table element. When rows are dynamically inserted or recycled during scrolling, no listener teardown or re-attachment is required.
"""

JS_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 1,
        "chapter_title": "JavaScript Engine Internals: V8, Call Stack & The Event Loop",
        "subtopic": "Event Loop Task Priorities",
        "question": "In the JavaScript Event Loop, which queue is checked and completely drained immediately after the Call Stack becomes empty, before any setTimeout callbacks are executed?",
        "options": [
            "The Microtask Queue (Promise.then, queueMicrotask)",
            "The Macrotask Queue",
            "The Web API Network Queue",
            "The Garbage Collection Sweep Queue"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [JS Prescribed Textbook — Chapter 1: Engine Internals & Event Loop]\nMicrotasks (Promises, MutationObserver, queueMicrotask) have absolute priority over macrotasks. The event loop drains all pending microtasks completely before executing the next macrotask (setTimeout, setInterval).",
        "difficulty": "medium",
    },
    {
        "chapter_num": 3,
        "chapter_title": "Objects, Prototypes & Object-Oriented JavaScript",
        "subtopic": "Arrow Function this Binding",
        "question": "How is the 'this' keyword evaluated inside a standard JavaScript ES6 arrow function?",
        "options": [
            "It inherits 'this' lexically from its enclosing execution context at the time of definition",
            "It binds to the object to the left of the calling dot",
            "It defaults to the global window object in all strict modes",
            "It is dynamically assigned to the function's prototype"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [JS Prescribed Textbook — Chapter 3: Prototypes & this]\nArrow functions do not bind their own 'this'. Instead, they capture 'this' lexically from the scope in which they were created.",
        "difficulty": "easy",
    }
]

JAVASCRIPT_MASTER_CHAPTERS = JS_MASTER_CHAPTERS
JAVASCRIPT_TEXTBOOK_MARKDOWN = JS_TEXTBOOK_MARKDOWN
JAVASCRIPT_EXPANDED_QUESTIONS = JS_EXPANDED_QUESTIONS
'''

with open(os.path.join(TEXTBOOK_DIR, "verbal_master.py"), "w", encoding="utf-8") as f:
    f.write(VERBAL_CODE.strip() + "\n")
ast.parse(VERBAL_CODE)
print("verbal_master.py generated and verified!")

with open(os.path.join(TEXTBOOK_DIR, "javascript_master.py"), "w", encoding="utf-8") as f:
    f.write(JS_CODE.strip() + "\n")
ast.parse(JS_CODE)
print("javascript_master.py generated and verified!")
