"""
question_bank.py — a small, hand-written bank of technical questions
keyed by skill, plus generic behavioral/problem-solving questions.
Used by question_generator.py as the template fallback when no LLM is
configured, so question generation always returns something usable.
"""

TECHNICAL_QUESTIONS: dict[str, list[dict]] = {
    "Python": [
        {"q": "What is the difference between a list and a tuple in Python?", "difficulty": "easy"},
        {"q": "Explain how Python's GIL affects multi-threaded programs.", "difficulty": "medium"},
        {"q": "How would you optimize a Python function that's running slowly on large datasets?", "difficulty": "hard"},
    ],
    "FastAPI": [
        {"q": "What are FastAPI dependencies used for, and how do you define one?", "difficulty": "easy"},
        {"q": "How would you implement JWT-based authentication in a FastAPI application?", "difficulty": "medium"},
        {"q": "How would you design a scalable REST API using FastAPI for a high-traffic service?", "difficulty": "hard"},
    ],
    "Django": [
        {"q": "What is Django middleware and what is it used for?", "difficulty": "medium"},
        {"q": "Explain Django's ORM and how migrations work.", "difficulty": "easy"},
    ],
    "React": [
        {"q": "What is the difference between state and props in React?", "difficulty": "easy"},
        {"q": "Explain how the useEffect hook works and common pitfalls with it.", "difficulty": "medium"},
    ],
    "PostgreSQL": [
        {"q": "How would you optimize a slow PostgreSQL query?", "difficulty": "hard"},
        {"q": "What's the difference between a LEFT JOIN and an INNER JOIN?", "difficulty": "easy"},
    ],
    "SQL": [
        {"q": "Write a query to find duplicate rows in a table.", "difficulty": "medium"},
    ],
    "Docker": [
        {"q": "What's the difference between an image and a container in Docker?", "difficulty": "easy"},
        {"q": "How would you reduce the size of a Docker image for a Python application?", "difficulty": "medium"},
    ],
    "AWS": [
        {"q": "How would you design a highly available architecture on AWS for a web application?", "difficulty": "hard"},
    ],
    "Machine Learning": [
        {"q": "Explain the difference between supervised and unsupervised learning.", "difficulty": "easy"},
        {"q": "How would you handle an imbalanced dataset in a classification problem?", "difficulty": "medium"},
    ],
}

GENERIC_TECHNICAL_QUESTIONS = [
    {"q": "Walk me through how you would design a scalable REST API for this role.", "difficulty": "hard"},
    {"q": "Describe a technical problem you solved recently and how you approached it.", "difficulty": "medium"},
]

BEHAVIORAL_QUESTIONS = [
    "Tell me about a time you disagreed with a teammate. How did you resolve it?",
    "Describe a project where you had to work under a tight deadline. What did you do?",
    "Tell me about a time you had to learn a new technology quickly for a project.",
    "Describe a situation where you received critical feedback. How did you respond?",
    "Tell me about a time you had to explain a technical concept to a non-technical stakeholder.",
]
