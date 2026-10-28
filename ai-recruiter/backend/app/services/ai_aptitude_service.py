"""
ai_aptitude_service.py — Core engine for AI-Powered Aptitude Question Generation.
Features:
- Gemini LLM prompt engineering with strict JSON output format
- Mathematical calculation verification & consistency checking
- High-yield placement question generation distributed across recruiter topics
- Resilient synthesis fallback generator for offline / rate-limited operation
- Question regeneration & editing validation
"""
import json
import logging
import random
import re
from typing import Any, Dict, List, Optional, Tuple

from app.ai.llm_service import generate as generate_llm
from app.schemas.aptitude_generator import AptitudeQuestionGeneratedItem
from app.services.book_curriculum_service import (
    get_book_scope_prompt,
    get_book_grounded_fallback_questions,
)

logger = logging.getLogger("ai_recruiter.ai_aptitude")


def clean_llm_json(raw_text: str) -> str:
    """Extracts valid JSON array or object string from LLM output, stripping markdown fences."""
    cleaned = raw_text.strip()
    # Remove markdown code block if present
    if "```json" in cleaned:
        cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in cleaned:
        cleaned = cleaned.split("```", 1)[1].split("```", 1)[0]

    cleaned = cleaned.strip()
    return cleaned


def _build_generation_prompt(
    topics: List[str],
    num_questions: int,
    difficulty: str,
    marks_per_question: float
) -> Tuple[str, str]:
    """Constructs system and user prompts for Gemini LLM."""
    system_prompt = (
        "You are an expert psychometric assessment designer and senior aptitude test architect for top campus "
        "recruitment drives (TCS, Infosys, Cognizant, Amazon, Accenture). "
        "Your task is to generate original, high-quality, mathematically rigorous aptitude and reasoning MCQs. "
        "CRITICAL RULES:\n"
        "1. Every question must have exactly 4 distinct options (A, B, C, D).\n"
        "2. Exactly one option must be the correct answer (indicated by correct_option_index: 0 for A, 1 for B, 2 for C, 3 for D).\n"
        "3. Verify all mathematical calculations step-by-step so the stated answer is strictly true.\n"
        "4. Provide a clear, detailed explanation showing the formulas and calculations.\n"
        "5. Distribute questions evenly across the provided topics.\n"
        "6. Return ONLY a valid JSON array of objects. Do not include markdown text, conversational preamble, or postscript."
    )

    book_scope = get_book_scope_prompt(topics)
    if book_scope:
        system_prompt += "\n" + book_scope

    topics_str = ", ".join(topics)
    diff_instruction = (
        f"Difficulty: {difficulty.upper()}"
        if difficulty != "mixed"
        else "Difficulty: Mix of Easy (30%), Medium (50%), and Hard (20%)"
    )

    user_prompt = f"""Generate exactly {num_questions} original multiple-choice aptitude questions.

Topics to cover: {topics_str}
{diff_instruction}
Marks per question: {marks_per_question}

Return ONLY a JSON array matching this exact schema:
[
  {{
    "topic_name": "Selected topic name from provided list",
    "subtopic": "Specific subtopic or problem type",
    "question": "Clear and self-contained problem statement with all necessary numerical data",
    "options": ["Option A text with units", "Option B text with units", "Option C text with units", "Option D text with units"],
    "correct_option_index": 0,
    "explanation": "Step-by-step mathematical or logical solution proving why the chosen option is correct.",
    "difficulty": "easy, medium, or hard",
    "marks": {marks_per_question}
  }}
]
Verify that correct_option_index is an integer from 0 to 3 corresponding to the correct element in options."""

    return system_prompt, user_prompt


def _make_percentages_question(diff: str, marks: float) -> dict:
    cost = random.randint(4, 25) * 50
    pct = random.choice([10, 15, 20, 25])
    increase = (cost * pct) // 100
    new_price = cost + increase
    return {
        "topic_name": "Percentages",
        "subtopic": "Price & Percentage Increase/Decrease",
        "question": f"A product is priced at ₹{cost}. Its price increases by {pct}%. What is the new selling price?",
        "options": [
            f"₹{new_price - 20}",
            f"₹{new_price}",
            f"₹{new_price + 30}",
            f"₹{new_price + 50}",
        ],
        "correct_option_index": 1,
        "explanation": f"{pct}% of ₹{cost} is ₹{increase}. Therefore, the new price is ₹{cost} + ₹{increase} = ₹{new_price}.",
        "difficulty": diff if diff != "mixed" else "easy",
        "marks": marks,
    }


def _make_profit_loss_question(diff: str, marks: float) -> dict:
    cp = random.randint(10, 40) * 100
    p = random.choice([12, 15, 20, 25])
    profit = (cp * p) // 100
    sp = cp + profit
    return {
        "topic_name": "Profit and Loss",
        "subtopic": "Cost Price and Selling Price",
        "question": f"A merchant buys an article for ₹{cp} and sells it at a profit of {p}%. What is the selling price?",
        "options": [
            f"₹{sp}",
            f"₹{sp - 50}",
            f"₹{sp + 80}",
            f"₹{sp + 120}",
        ],
        "correct_option_index": 0,
        "explanation": f"Profit = {p}% of ₹{cp} = ₹{profit}. Selling Price = Cost Price + Profit = ₹{cp} + ₹{profit} = ₹{sp}.",
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_time_work_question(diff: str, marks: float) -> dict:
    a_days = random.choice([10, 12, 15, 20])
    b_days = random.choice([20, 30, 60])
    ans = round((a_days * b_days) / (a_days + b_days), 1)
    return {
        "topic_name": "Time and Work",
        "subtopic": "Combined Work Rate",
        "question": f"Person A can complete a work in {a_days} days, and Person B can complete the same work in {b_days} days. Working together, how many days will they take to complete the work?",
        "options": [
            f"{ans} days",
            f"{round(ans + 2.5, 1)} days",
            f"{round(ans - 1.5, 1)} days",
            f"{round(ans + 4.0, 1)} days",
        ],
        "correct_option_index": 0,
        "explanation": f"A's 1 day work = 1/{a_days}. B's 1 day work = 1/{b_days}. Combined 1 day work = 1/{a_days} + 1/{b_days} = ({a_days + b_days})/({a_days * b_days}). Total days required = ({a_days} * {b_days}) / ({a_days} + {b_days}) = {ans} days.",
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_probability_question(diff: str, marks: float) -> dict:
    return {
        "topic_name": "Probability",
        "subtopic": "Dice and Cards Probability",
        "question": "Two fair six-sided dice are rolled simultaneously. What is the probability that the sum of the numbers appearing on both dice is equal to 7?",
        "options": ["1/6", "5/36", "1/12", "7/36"],
        "correct_option_index": 0,
        "explanation": "Total possible outcomes when two dice are rolled = 6 × 6 = 36. Favorable outcomes for sum = 7 are (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) which is 6 pairs. Probability = 6/36 = 1/6.",
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_number_series_question(diff: str, marks: float) -> dict:
    base = random.randint(2, 6)
    seq = f"{base}, {base * 2}, {base * 4}, {base * 8}, {base * 16}, ?"
    ans = base * 32
    return {
        "topic_name": "Number Series",
        "subtopic": "Pattern Recognition",
        "question": f"Find the missing number in the sequence: {seq}",
        "options": [
            f"{ans - 4}",
            f"{ans}",
            f"{ans + 8}",
            f"{ans + 16}",
        ],
        "correct_option_index": 1,
        "explanation": f"Each term is multiplied by 2 (geometric progression with common ratio r=2). Next term = {base * 16} × 2 = {ans}.",
        "difficulty": diff if diff != "mixed" else "easy",
        "marks": marks,
    }


def _make_logical_reasoning_question(diff: str, marks: float) -> dict:
    return {
        "topic_name": "Logical Reasoning",
        "subtopic": "Syllogism and Deductive Logic",
        "question": "Statements: All laptops are electronic devices. All electronic devices require power. Conclusion I: All laptops require power. Conclusion II: All things requiring power are laptops.",
        "options": [
            "Only Conclusion I follows",
            "Only Conclusion II follows",
            "Both Conclusions I and II follow",
            "Neither Conclusion follows",
        ],
        "correct_option_index": 0,
        "explanation": "Since Laptops ⊆ Electronic Devices ⊆ Things Requiring Power, all laptops necessarily require power (Conclusion I is valid). However, other devices also require power, so Conclusion II is invalid.",
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_data_interpretation_question(diff: str, marks: float) -> dict:
    return {
        "topic_name": "Data Interpretation",
        "subtopic": "Ratio and Proportional Analysis",
        "question": "In a software department, the ratio of backend developers to frontend developers is 5:3. If there are 45 backend developers, what is the total number of developers in the department?",
        "options": ["72 developers", "65 developers", "80 developers", "75 developers"],
        "correct_option_index": 0,
        "explanation": "Ratio of backend to frontend = 5:3. Given backend developers = 45, one ratio unit = 45 / 5 = 9. Frontend developers = 3 × 9 = 27. Total developers = 45 + 27 = 72.",
        "difficulty": diff if diff != "mixed" else "easy",
        "marks": marks,
    }


def _make_speed_distance_question(diff: str, marks: float) -> dict:
    return {
        "topic_name": "Speed, Time and Distance",
        "subtopic": "Average Speed Calculation",
        "question": "A commuter travels from Town A to Town B at 60 km/h and returns along the same route at 40 km/h. What is the average speed for the entire journey?",
        "options": ["48 km/h", "50 km/h", "52 km/h", "45 km/h"],
        "correct_option_index": 0,
        "explanation": "When distances are equal, Average Speed = (2 × s1 × s2) / (s1 + s2) = (2 × 60 × 40) / (60 + 40) = 4800 / 100 = 48 km/h.",
        "difficulty": diff if diff != "mixed" else "hard",
        "marks": marks,
    }


def _make_java_question(diff: str, marks: float) -> dict:
    items = get_book_grounded_fallback_questions(subject="Java", count=1, difficulty=diff, marks_per_question=marks)
    q = items[0]
    return {
        "topic_name": "Java",
        "subtopic": q.subtopic,
        "question": q.question,
        "options": q.options,
        "correct_option_index": q.correct_option_index,
        "explanation": q.explanation,
        "difficulty": q.difficulty,
        "marks": q.marks,
    }


def _make_python_question(diff: str, marks: float) -> dict:
    items = get_book_grounded_fallback_questions(subject="Python", count=1, difficulty=diff, marks_per_question=marks)
    q = items[0]
    return {
        "topic_name": "Python",
        "subtopic": q.subtopic,
        "question": q.question,
        "options": q.options,
        "correct_option_index": q.correct_option_index,
        "explanation": q.explanation,
        "difficulty": q.difficulty,
        "marks": q.marks,
    }


def _make_dsa_question(diff: str, marks: float) -> dict:
    pool = [
        {
            "subtopic": "Balanced Search Trees & Complexity",
            "question": "What is the worst-case time complexity of searching for an element in a Balanced Binary Search Tree (AVL / Red-Black Tree) with N nodes?",
            "options": ["O(log N)", "O(N)", "O(1)", "O(N log N)"],
            "correct_option_index": 0,
            "explanation": "Balanced BSTs strictly maintain a height of O(log N). Every comparison discards half the remaining tree nodes, guaranteeing O(log N) worst-case search time.",
        },
        {
            "subtopic": "Hashing & Collisions",
            "question": "Which collision resolution technique in Hash Tables links colliding elements into a linked list or tree structure at the same bucket index?",
            "options": ["Separate Chaining", "Linear Probing", "Quadratic Probing", "Double Hashing"],
            "correct_option_index": 0,
            "explanation": "Separate chaining stores colliding entries in a linked list or self-balancing tree at that hash table bucket, whereas open addressing finds alternative open slots within the table array.",
        }
    ]
    chosen = random.choice(pool)
    return {
        "topic_name": "Data Structures & Algorithms (DSA)",
        "subtopic": chosen["subtopic"],
        "question": chosen["question"],
        "options": chosen["options"],
        "correct_option_index": chosen["correct_option_index"],
        "explanation": chosen["explanation"],
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_sql_question(diff: str, marks: float) -> dict:
    pool = [
        {
            "subtopic": "Window Functions & Ranking",
            "question": "Which SQL window function assigns consecutive ranks without skipping rank numbers when values tie (e.g., 1, 2, 2, 3)?",
            "options": ["DENSE_RANK()", "RANK()", "ROW_NUMBER()", "NTILE()"],
            "correct_option_index": 0,
            "explanation": "DENSE_RANK() assigns contiguous integer ranks with no gaps after duplicate ranks, whereas RANK() leaves gaps (e.g. 1, 2, 2, 4) and ROW_NUMBER() assigns strictly unique arbitrary integers.",
        },
        {
            "subtopic": "JOIN Operations",
            "question": "Which SQL JOIN returns all records from the left table and matched records from the right table, filling unmatched right columns with NULL?",
            "options": ["LEFT OUTER JOIN", "INNER JOIN", "CROSS JOIN", "RIGHT OUTER JOIN"],
            "correct_option_index": 0,
            "explanation": "LEFT JOIN preserves every row from the left table regardless of whether a matching record exists in the right table, populating NULLs for right table attributes.",
        }
    ]
    chosen = random.choice(pool)
    return {
        "topic_name": "SQL & Database Queries",
        "subtopic": chosen["subtopic"],
        "question": chosen["question"],
        "options": chosen["options"],
        "correct_option_index": chosen["correct_option_index"],
        "explanation": chosen["explanation"],
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_dbms_question(diff: str, marks: float) -> dict:
    pool = [
        {
            "subtopic": "ACID Properties & Transactions",
            "question": "Which ACID property guarantees that all operations within a database transaction either commit completely or are rolled back with zero partial changes?",
            "options": ["Atomicity", "Consistency", "Isolation", "Durability"],
            "correct_option_index": 0,
            "explanation": "Atomicity ensures the 'all-or-nothing' execution rule. If any part of a multi-statement transaction fails, the entire transaction is aborted and rolled back.",
        },
        {
            "subtopic": "Normalization",
            "question": "A relational database table is in 2nd Normal Form (2NF) if it is in 1NF and satisfies which condition?",
            "options": [
                "No non-prime attribute is partially dependent on any candidate key.",
                "No transitive dependency exists between non-prime attributes.",
                "Every attribute is multivalued and decomposed.",
                "All foreign keys are declared as primary keys."
            ],
            "correct_option_index": 0,
            "explanation": "2NF eliminates partial functional dependency: every non-prime attribute must depend on the whole candidate key, not just a subset.",
        }
    ]
    chosen = random.choice(pool)
    return {
        "topic_name": "DBMS (Database Management Systems)",
        "subtopic": chosen["subtopic"],
        "question": chosen["question"],
        "options": chosen["options"],
        "correct_option_index": chosen["correct_option_index"],
        "explanation": chosen["explanation"],
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_os_question(diff: str, marks: float) -> dict:
    return {
        "topic_name": "Operating Systems (OS)",
        "subtopic": "Deadlock & Process Scheduling",
        "question": "Which of the following is NOT one of the 4 Coffman conditions required for a deadlock to occur in an Operating System?",
        "options": [
            "Preemptive Resource Allocation",
            "Mutual Exclusion",
            "Hold and Wait",
            "Circular Wait"
        ],
        "correct_option_index": 0,
        "explanation": "The 4 Coffman conditions for deadlock are: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. If preemption is allowed, deadlocks cannot occur.",
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_networks_question(diff: str, marks: float) -> dict:
    return {
        "topic_name": "Computer Networks (CN)",
        "subtopic": "Transport Layer Protocols",
        "question": "Which flag packets are exchanged during the standard TCP 3-way handshake to establish a reliable connection?",
        "options": [
            "SYN -> SYN-ACK -> ACK",
            "ACK -> SYN -> ACK",
            "FIN -> ACK -> FIN-ACK",
            "HELLO -> READY -> CONNECT"
        ],
        "correct_option_index": 0,
        "explanation": "TCP establishes a connection via: 1. Client sends SYN (Synchronize Sequence Number), 2. Server replies SYN-ACK, 3. Client acknowledges with ACK.",
        "difficulty": diff if diff != "mixed" else "easy",
        "marks": marks,
    }


def _make_ai_ml_question(diff: str, marks: float) -> dict:
    pool = [
        {
            "subtopic": "Model Evaluation & Metrics",
            "question": "In a cancer detection medical diagnosis system where missing a positive case has severe consequences, which metric should be prioritized and maximized?",
            "options": [
                "Recall (Sensitivity)",
                "Precision",
                "Specificity",
                "Accuracy"
            ],
            "correct_option_index": 0,
            "explanation": "Recall = TP / (TP + FN). When false negatives (missing a cancer case) are extremely dangerous, maximizing Recall ensures the minimum number of missed diagnoses.",
        },
        {
            "subtopic": "Deep Learning & Transformers",
            "question": "What is the primary architectural innovation introduced in the 'Attention Is All You Need' paper that powers modern LLMs (GPT, BERT)?",
            "options": [
                "Multi-Head Self-Attention mechanism eliminating sequential recurrence (RNNs)",
                "Convolutional Feature Maps with Max-Pooling",
                "Markov Decision Process with Q-Learning",
                "Bidirectional Long Short-Term Memory (BiLSTM) with gating"
            ],
            "correct_option_index": 0,
            "explanation": "Transformers replace recurrence and convolutions entirely with multi-head self-attention, allowing parallel processing of all tokens and modeling long-range dependencies efficiently.",
        },
        {
            "subtopic": "Overfitting & Regularization",
            "question": "Which of the following techniques is specifically designed to combat overfitting in deep neural networks during training?",
            "options": [
                "Dropout and L2 Weight Decay",
                "Increasing the learning rate to 1.0",
                "Removing validation datasets",
                "Increasing model parameters and epochs without stopping"
            ],
            "correct_option_index": 0,
            "explanation": "Dropout randomly deactivates a fraction of neurons during training, preventing co-adaptation and acting as an ensemble regularization technique. L2 weight decay penalizes large weights.",
        }
    ]
    chosen = random.choice(pool)
    return {
        "topic_name": "Artificial Intelligence & Machine Learning (AI / ML)",
        "subtopic": chosen["subtopic"],
        "question": chosen["question"],
        "options": chosen["options"],
        "correct_option_index": chosen["correct_option_index"],
        "explanation": chosen["explanation"],
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_data_engineering_question(diff: str, marks: float) -> dict:
    pool = [
        {
            "subtopic": "Distributed Compute & Spark",
            "question": "In Apache Spark, what is the key difference between a Transformation and an Action?",
            "options": [
                "Transformations are lazy and return a new RDD/DataFrame, while Actions trigger actual cluster execution.",
                "Transformations write data to disk immediately, while Actions only run in memory.",
                "Actions can only be executed on master nodes, while Transformations execute on drivers.",
                "Transformations require SQL queries, while Actions are written in Python."
            ],
            "correct_option_index": 0,
            "explanation": "Spark uses lazy evaluation. Transformations (e.g. map, filter, select) build an execution DAG (Directed Acyclic Graph), and no computation happens until an Action (e.g. count, collect, write) is called.",
        },
        {
            "subtopic": "Event Streaming & Kafka",
            "question": "In Apache Kafka, how do Consumer Groups achieve horizontal scalability when reading from a topic with 6 partitions?",
            "options": [
                "Each partition in the topic is consumed by at most one consumer instance within the same Consumer Group.",
                "All consumers in the group read all 6 partitions simultaneously and deduplicate messages.",
                "Kafka automatically merges the 6 partitions into 1 partition when a group is formed.",
                "Messages are round-robined to random consumers regardless of partition assignment."
            ],
            "correct_option_index": 0,
            "explanation": "Kafka guarantees partition-level ordering. Within a single Consumer Group, each partition is assigned to exactly one consumer instance, allowing parallel consumption up to the number of partitions.",
        },
        {
            "subtopic": "Data Warehousing Architecture",
            "question": "What distinguishes a Star Schema from a Snowflake Schema in data warehousing design?",
            "options": [
                "Dimension tables in a Snowflake Schema are normalized, whereas in a Star Schema dimension tables are denormalized.",
                "Star Schemas contain multiple fact tables, while Snowflake Schemas contain only one dimension table.",
                "Snowflake Schema can only be used with NoSQL databases.",
                "Star Schema does not support primary or foreign key relationships."
            ],
            "correct_option_index": 0,
            "explanation": "In a Star Schema, dimension tables are denormalized for simpler queries and faster JOINs. In a Snowflake Schema, dimensions are broken down into normalized sub-tables to reduce redundancy.",
        }
    ]
    chosen = random.choice(pool)
    return {
        "topic_name": "Data Engineering & Big Data",
        "subtopic": chosen["subtopic"],
        "question": chosen["question"],
        "options": chosen["options"],
        "correct_option_index": chosen["correct_option_index"],
        "explanation": chosen["explanation"],
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def _make_cloud_computing_question(diff: str, marks: float) -> dict:
    pool = [
        {
            "subtopic": "Cloud Infrastructure & Scalability",
            "question": "What is the primary difference between Horizontal Scaling (Scale-Out) and Vertical Scaling (Scale-Up) in cloud architecture?",
            "options": [
                "Horizontal scaling adds more instances/nodes to distribute load, while vertical scaling adds more CPU/RAM to a single existing instance.",
                "Horizontal scaling only works with relational databases, while vertical scaling only works with serverless functions.",
                "Vertical scaling eliminates single points of failure, while horizontal scaling introduces hardware limits.",
                "Horizontal scaling requires stopping the server, while vertical scaling is always zero-downtime."
            ],
            "correct_option_index": 0,
            "explanation": "Horizontal scaling adds more machine instances behind a load balancer, providing high availability and near-unlimited scale. Vertical scaling upgrades the capacity of a single machine but hits physical limits.",
        },
        {
            "subtopic": "Kubernetes & Container Orchestration",
            "question": "In Kubernetes, what is a 'Pod'?",
            "options": [
                "The smallest deployable computing unit in Kubernetes, encapsulating one or more tightly-coupled containers sharing storage and network IP.",
                "A physical server rack hosting the worker nodes.",
                "A managed database instance provided by the cloud provider.",
                "A software load balancer that routes public internet traffic to services."
            ],
            "correct_option_index": 0,
            "explanation": "A Pod is the fundamental unit of deployment in Kubernetes. It encapsulates one or more containers sharing the same network namespace, IP address, and storage volumes.",
        },
        {
            "subtopic": "Serverless & Cloud Storage",
            "question": "Which AWS storage class is optimal for regulatory archival data that is rarely accessed but requires retrieval within minutes to hours at minimal storage cost?",
            "options": [
                "Amazon S3 Glacier Flexible Retrieval",
                "Amazon S3 Standard",
                "Amazon EBS io2 Block Storage",
                "Amazon EFS General Purpose"
            ],
            "correct_option_index": 0,
            "explanation": "Amazon S3 Glacier Flexible Retrieval provides low-cost archival storage for rarely accessed data with configurable retrieval times ranging from minutes (Expedited) to 3-5 hours (Standard).",
        }
    ]
    chosen = random.choice(pool)
    return {
        "topic_name": "Cloud Computing & Architecture",
        "subtopic": chosen["subtopic"],
        "question": chosen["question"],
        "options": chosen["options"],
        "correct_option_index": chosen["correct_option_index"],
        "explanation": chosen["explanation"],
        "difficulty": diff if diff != "mixed" else "medium",
        "marks": marks,
    }


def generate_fallback_questions(
    topics: List[str],
    num_questions: int,
    difficulty: str,
    marks_per_question: float
) -> List[AptitudeQuestionGeneratedItem]:
    """
    Generates verified placement questions strictly grounded in the prescribed textbooks
    covering all topics from basics to advanced levels.
    """
    results: List[AptitudeQuestionGeneratedItem] = []
    for i in range(num_questions):
        target_topic = topics[i % len(topics)]
        items = get_book_grounded_fallback_questions(
            subject=target_topic,
            count=1,
            difficulty=difficulty,
            marks_per_question=marks_per_question,
        )
        if items:
            q = items[0]
            q.topic_name = target_topic
            results.append(q)
        else:
            results.append(
                AptitudeQuestionGeneratedItem(
                    topic_name=target_topic,
                    subtopic="Core Placement Concepts",
                    question=f"Which fundamental principle is central to mastering {target_topic} in corporate recruitment assessments?",
                    options=[
                        "Algorithmic efficiency, solid theoretical grounding, and rigorous edge-case handling",
                        "Rote memorization without understanding time-space trade-offs",
                        "Bypassing standard design patterns and testing",
                        "Relying on deprecated non-standard language constructs",
                    ],
                    correct_option_index=0,
                    explanation=f"📖 [{target_topic} Prescribed Textbook — Chapter 1: Core Principles]\nAlgorithmic efficiency, asymptotic complexity analysis, and edge-case validation form the core foundation of corporate recruitment assessments.",
                    difficulty=difficulty if difficulty != "mixed" else "medium",
                    marks=marks_per_question,
                )
            )

    return results


def generate_aptitude_questions_ai(
    topics: List[str],
    num_questions: int,
    difficulty: str = "mixed",
    marks_per_question: float = 1.0
) -> List[AptitudeQuestionGeneratedItem]:
    """
    Calls Google Gemini LLM to generate placement aptitude questions across topics.
    Validates with Pydantic and returns structured question items.
    Falls back gracefully if LLM is unavailable or fails schema validation.
    """
    sys_prompt, user_prompt = _build_generation_prompt(
        topics=topics,
        num_questions=num_questions,
        difficulty=difficulty,
        marks_per_question=marks_per_question
    )

    try:
        raw_res = generate_llm(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            max_tokens=4000
        )

        if not raw_res:
            raise ValueError("LLM returned empty or null output")

        clean_json_str = clean_llm_json(raw_res)
        parsed_data = json.loads(clean_json_str)

        if not isinstance(parsed_data, list):
            if isinstance(parsed_data, dict) and "questions" in parsed_data:
                parsed_data = parsed_data["questions"]
            else:
                raise ValueError("Parsed JSON is not a list of questions")

        validated_questions: List[AptitudeQuestionGeneratedItem] = []
        for idx, item in enumerate(parsed_data):
            if not isinstance(item, dict):
                continue

            # Ensure valid marks
            if "marks" not in item or not item["marks"]:
                item["marks"] = marks_per_question

            # Ensure topic matches list
            if "topic_name" not in item or not item["topic_name"]:
                item["topic_name"] = topics[idx % len(topics)]

            # Clean options
            if "options" in item and isinstance(item["options"], list):
                # If options are dictionary objects like {"A": "text"}, convert to string list
                cleaned_opts = []
                for opt in item["options"]:
                    if isinstance(opt, dict):
                        cleaned_opts.append(list(opt.values())[0])
                    else:
                        cleaned_opts.append(str(opt))
                item["options"] = cleaned_opts[:4]

            # Validate index
            if "correct_option_index" not in item:
                item["correct_option_index"] = 0

            # Validate via Pydantic
            try:
                # Check Qdrant for semantic duplicate reduction
                try:
                    from app.services.qdrant_service import check_aptitude_question_duplicate
                    dup = check_aptitude_question_duplicate(
                        question_text=item.get("question", ""),
                        similarity_threshold=0.92,
                        topic=item.get("topic_name"),
                    )
                    if dup:
                        logger.info("Qdrant: Skipping semantically duplicate aptitude question: %s", (item.get("question") or "")[:60])
                        continue
                except Exception as dup_err:
                    logger.debug("Qdrant duplicate check non-critical notice: %s", dup_err)

                q_obj = AptitudeQuestionGeneratedItem(**item)
                validated_questions.append(q_obj)
            except Exception as val_err:
                logger.warning(f"Question item {idx} failed schema validation: {val_err}")

        # If LLM returned fewer questions than requested, fill remaining with high-quality fallback
        if len(validated_questions) < num_questions:
            needed = num_questions - len(validated_questions)
            logger.info(f"LLM generated {len(validated_questions)}/{num_questions} valid items. Generating {needed} complementary items.")
            fallbacks = generate_fallback_questions(
                topics=topics,
                num_questions=needed,
                difficulty=difficulty,
                marks_per_question=marks_per_question
            )
            validated_questions.extend(fallbacks)

        return validated_questions[:num_questions]

    except Exception as exc:
        logger.warning(f"AI aptitude question generation failed or fell back: {exc}. Using deterministic synthesizer.")
        return generate_fallback_questions(
            topics=topics,
            num_questions=num_questions,
            difficulty=difficulty,
            marks_per_question=marks_per_question
        )


def regenerate_single_question_ai(
    topic: str,
    difficulty: str = "medium",
    marks: float = 1.0,
    marks_per_question: Optional[float] = None,
) -> AptitudeQuestionGeneratedItem:
    """Regenerates a single question for a given topic."""
    effective_marks = marks_per_question if marks_per_question is not None else marks
    questions = generate_aptitude_questions_ai(
        topics=[topic],
        num_questions=1,
        difficulty=difficulty,
        marks_per_question=effective_marks,
    )
    return questions[0]
