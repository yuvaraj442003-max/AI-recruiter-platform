"""
book_curriculum_service.py — Service for managing Prescribed Study Textbooks across ALL active learning topics:
- Data Structures & Algorithms (DSA)
- SQL & Database Queries
- Quantitative Aptitude
- Logical Reasoning
- Java
- Python
- JavaScript / TypeScript
- Data Engineering & Big Data
- Artificial Intelligence & Machine Learning (AI / ML)
- Operating Systems (OS)
- Computer Networks (CN)
- DBMS (Database Management Systems)

Provides chapter-by-chapter curriculum from basics to advanced levels,
RAG PDF ingestion and storage, in-app textbook markdown generation,
and enforces that ALL questions generated for exams and practice tests
are strictly grounded in the provided books.
"""
import copy
import json
import logging
import os
import random
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pymupdf
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.student import StudyMaterial
from app.schemas.aptitude_generator import AptitudeQuestionGeneratedItem
from app.services.java_textbook_master_content import (
    JAVA_MASTER_CHAPTERS,
    COMPLETE_JAVA_TEXTBOOK_MARKDOWN,
    JAVA_EXPANDED_BOOK_QUESTIONS,
)
from app.services.textbooks.dsa_master import (
    DSA_MASTER_CHAPTERS,
    DSA_TEXTBOOK_MARKDOWN,
    DSA_EXPANDED_QUESTIONS,
)
from app.services.textbooks.python_master import (
    PYTHON_MASTER_CHAPTERS,
    PYTHON_TEXTBOOK_MARKDOWN,
    PYTHON_EXPANDED_QUESTIONS,
)
from app.services.textbooks.sql_master import (
    SQL_MASTER_CHAPTERS,
    SQL_TEXTBOOK_MARKDOWN,
    SQL_EXPANDED_QUESTIONS,
)
from app.services.textbooks.os_master import (
    OS_MASTER_CHAPTERS,
    OS_TEXTBOOK_MARKDOWN,
    OS_EXPANDED_QUESTIONS,
)
from app.services.textbooks.cn_master import (
    CN_MASTER_CHAPTERS,
    CN_TEXTBOOK_MARKDOWN,
    CN_EXPANDED_QUESTIONS,
)
from app.services.textbooks.dbms_master import (
    DBMS_MASTER_CHAPTERS,
    DBMS_TEXTBOOK_MARKDOWN,
    DBMS_EXPANDED_QUESTIONS,
)
from app.services.textbooks.quant_master import (
    QUANT_MASTER_CHAPTERS,
    QUANT_TEXTBOOK_MARKDOWN,
    QUANT_EXPANDED_QUESTIONS,
)
from app.services.textbooks.logical_master import (
    LOGICAL_MASTER_CHAPTERS,
    LOGICAL_TEXTBOOK_MARKDOWN,
    LOGICAL_EXPANDED_QUESTIONS,
)
from app.services.textbooks.verbal_master import (
    VERBAL_MASTER_CHAPTERS,
    VERBAL_TEXTBOOK_MARKDOWN,
    VERBAL_EXPANDED_QUESTIONS,
)
from app.services.textbooks.javascript_master import (
    JAVASCRIPT_MASTER_CHAPTERS,
    JAVASCRIPT_TEXTBOOK_MARKDOWN,
    JAVASCRIPT_EXPANDED_QUESTIONS,
)
from app.services.textbooks.data_eng_master import (
    DATA_ENG_MASTER_CHAPTERS,
    DATA_ENG_TEXTBOOK_MARKDOWN,
    DATA_ENG_EXPANDED_QUESTIONS,
)
from app.services.textbooks.ai_ml_master import (
    AI_ML_MASTER_CHAPTERS,
    AI_ML_TEXTBOOK_MARKDOWN,
    AI_ML_EXPANDED_QUESTIONS,
)


from app.services.comprehensive_curriculum.formatter import assemble_full_textbook_markdown
from app.services.comprehensive_curriculum.curriculum_dsa import DSA_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_sql import SQL_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_java import JAVA_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_python import PYTHON_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_javascript import JAVASCRIPT_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_os import OS_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_cn import CN_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_dbms import DBMS_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_quant import QUANT_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_logical import LOGICAL_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_verbal import VERBAL_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_data_eng import DATA_ENG_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_ai_ml import AI_ML_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_c import C_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_cpp import CPP_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_go import GOLANG_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_rust import RUST_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_cloud_computing import CLOUD_COMPUTING_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_aws import AWS_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_cybersecurity import CYBERSECURITY_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_devops import DEVOPS_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_gen_ai import GEN_AI_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_deep_learning import DEEP_LEARNING_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_software_testing import SOFTWARE_TESTING_CHAPTERS
from app.services.comprehensive_curriculum.curriculum_data_science import DATA_SCIENCE_CHAPTERS

logger = logging.getLogger("ai_recruiter.book_curriculum")

# Base search paths for books
DATASET_BOOKS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "dataset" / "books"
UPLOADS_BOOKS_DIR = Path(__file__).resolve().parent.parent.parent / "uploads" / "books"

DATASET_BOOKS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_BOOKS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 1. PRESCRIBED TEXTBOOK DEFINITIONS (BASICS TO ADVANCED ACROSS ALL TOPICS)
# =============================================================================

# =============================================================================
# 1. PRESCRIBED TEXTBOOK DEFINITIONS (UNABRIDGED COMPREHENSIVE EDITIONS)
# =============================================================================

DSA_TEXTBOOK = {
    "slug": "dsa-prescribed-textbook",
    "title": "Data Structures & Algorithms: Placement Master Edition (Prescribed Textbook)",
    "subject": "Data Structures & Algorithms (DSA)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Data Structures and Algorithms from foundational "
        "asymptotic complexity to advanced dynamic programming, graphs, tries, DSU, and solved FAANG coding problems. "
        "Every chapter contains core concepts, mathematical proofs, step-by-step solved examples with code, "
        "practice questions with solutions, and technical interview drills."
    ),
    "chapters": DSA_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Data Structures & Algorithms: Placement Master Edition (Prescribed Textbook)",
        "Data Structures & Algorithms (DSA)",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering Data Structures and Algorithms from foundational asymptotic complexity to advanced dynamic programming, graphs, tries, DSU, and solved FAANG coding problems.",
        DSA_CHAPTERS
    ),
}

SQL_TEXTBOOK = {
    "slug": "sql-prescribed-textbook",
    "title": "SQL & Relational Databases: Placement Master Edition (Prescribed Textbook)",
    "subject": "SQL & Database Queries",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete enterprise textbook on SQL and relational database engineering covering relational algebra, "
        "normalization, query execution order, advanced window functions, indexing, transactions, and solved technical queries."
    ),
    "chapters": SQL_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "SQL & Relational Databases: Placement Master Edition (Prescribed Textbook)",
        "SQL & Database Queries",
        "2026 Campus Placement Edition",
        "Complete enterprise textbook on SQL and relational database engineering covering relational algebra, normalization, query execution order, advanced window functions, indexing, transactions, and solved technical queries.",
        SQL_CHAPTERS
    ),
}

QUANT_TEXTBOOK = {
    "slug": "quantitative-aptitude-prescribed-textbook",
    "title": "Quantitative Aptitude: Corporate Recruitment Master Edition (Prescribed Textbook)",
    "subject": "Quantitative Aptitude",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering corporate numerical aptitude, speed mathematics, "
        "percentages, ratios, profit & loss, mixtures & alligations, speed distance, time & work, permutations, probability, and data interpretation."
    ),
    "chapters": QUANT_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Quantitative Aptitude: Corporate Recruitment Master Edition (Prescribed Textbook)",
        "Quantitative Aptitude",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering corporate numerical aptitude, speed mathematics, percentages, ratios, profit & loss, mixtures & alligations, speed distance, time & work, permutations, probability, and data interpretation.",
        QUANT_CHAPTERS
    ),
}

LOGICAL_TEXTBOOK = {
    "slug": "logical-reasoning-prescribed-textbook",
    "title": "Logical Reasoning & Analytical Ability (Prescribed Textbook)",
    "subject": "Logical Reasoning",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering corporate analytical reasoning, syllogisms, "
        "blood relations, linear/circular seating arrangements, direction tests, coding-decoding, clocks/calendars, critical reasoning, and multi-variable puzzles."
    ),
    "chapters": LOGICAL_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Logical Reasoning & Analytical Ability (Prescribed Textbook)",
        "Logical Reasoning",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering corporate analytical reasoning, syllogisms, blood relations, linear/circular seating arrangements, direction tests, coding-decoding, clocks/calendars, critical reasoning, and multi-variable puzzles.",
        LOGICAL_CHAPTERS
    ),
}

JAVA_TEXTBOOK = {
    "slug": "java-prescribed-textbook",
    "title": "Core Java Programming & Placement Foundations (Prescribed Master Textbook)",
    "subject": "Java",
    "edition": "2026 Comprehensive Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete, authoritative campus placement master textbook covering all Java programming language topics: "
        "JVM Internals, Memory Model, OOP Architecture, Strings & Memory Pooling, Collections, Generics, Concurrency, "
        "Stream API & Lambdas, I/O, Modern Java (Java 9 to 21 LTS), and Placement Puzzles."
    ),
    "chapters": JAVA_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Core Java Programming & Placement Foundations (Prescribed Master Textbook)",
        "Java",
        "2026 Comprehensive Campus Placement Edition",
        "Complete, authoritative campus placement master textbook covering all Java programming language topics: JVM Internals, Memory Model, OOP Architecture, Strings & Memory Pooling, Collections, Generics, Concurrency, Stream API & Lambdas, I/O, Modern Java, and Placement Puzzles.",
        JAVA_CHAPTERS
    ),
}

PYTHON_TEXTBOOK = {
    "slug": "python-prescribed-textbook",
    "title": "Python Programming & Interview Foundations (Prescribed Master Textbook)",
    "subject": "Python",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete campus placement master textbook covering Python execution architecture, memory model, "
        "built-in data structures, scoping, OOP & dunder methods, decorators, generators, asyncio, and placement coding interview problems."
    ),
    "chapters": PYTHON_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Python Programming & Interview Foundations (Prescribed Master Textbook)",
        "Python",
        "2026 Campus Placement Edition",
        "Complete campus placement master textbook covering Python execution architecture, memory model, built-in data structures, scoping, OOP & dunder methods, decorators, generators, asyncio, and placement coding interview problems.",
        PYTHON_CHAPTERS
    ),
}

JAVASCRIPT_TEXTBOOK = {
    "slug": "javascript-prescribed-textbook",
    "title": "Modern JavaScript & TypeScript: Full-Stack Placement Edition (Prescribed Textbook)",
    "subject": "JavaScript / TypeScript",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete textbook on JavaScript runtime engine architecture, V8 microtask queue, "
        "closures, prototypal inheritance, ES6+, TypeScript static typing, DOM event loop, and polyfills."
    ),
    "chapters": JAVASCRIPT_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Modern JavaScript & TypeScript: Full-Stack Placement Edition (Prescribed Textbook)",
        "JavaScript / TypeScript",
        "2026 Campus Placement Edition",
        "Complete textbook on JavaScript runtime engine architecture, V8 microtask queue, closures, prototypal inheritance, ES6+, TypeScript static typing, DOM event loop, and polyfills.",
        JAVASCRIPT_CHAPTERS
    ),
}

DATA_ENG_TEXTBOOK = {
    "slug": "data-engineering-prescribed-textbook",
    "title": "Data Engineering & Big Data Systems (Prescribed Textbook)",
    "subject": "Data Engineering & Big Data",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Comprehensive campus placement textbook covering distributed computing (Hadoop/Spark), data lakehouses (Delta/Parquet), "
        "stream processing (Kafka), workflow orchestration (Airflow), NoSQL, database sharding, and architecture case studies."
    ),
    "chapters": DATA_ENG_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Data Engineering & Big Data Systems (Prescribed Textbook)",
        "Data Engineering & Big Data",
        "2026 Campus Placement Edition",
        "Comprehensive campus placement textbook covering distributed computing (Hadoop/Spark), data lakehouses (Delta/Parquet), stream processing (Kafka), workflow orchestration (Airflow), NoSQL, database sharding, and architecture case studies.",
        DATA_ENG_CHAPTERS
    ),
}

AI_ML_TEXTBOOK = {
    "slug": "ai-machine-learning-prescribed-textbook",
    "title": "Artificial Intelligence & Machine Learning: Campus Master Edition (Prescribed Textbook)",
    "subject": "Artificial Intelligence & Machine Learning (AI / ML)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Artificial Intelligence and Machine Learning from mathematical foundations "
        "(gradient descent, loss functions) to supervised/unsupervised learning, Deep Learning, CNNs, Transformers, LLMs, and MLOps."
    ),
    "chapters": AI_ML_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Artificial Intelligence & Machine Learning: Campus Master Edition (Prescribed Textbook)",
        "Artificial Intelligence & Machine Learning (AI / ML)",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering Artificial Intelligence and Machine Learning from mathematical foundations (gradient descent, loss functions) to supervised/unsupervised learning, Deep Learning, CNNs, Transformers, LLMs, and MLOps.",
        AI_ML_CHAPTERS
    ),
}

OS_TEXTBOOK = {
    "slug": "operating-systems-prescribed-textbook",
    "title": "Operating Systems & Concurrency Architecture: Placement Master Edition (Prescribed Textbook)",
    "subject": "Operating Systems (OS)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Operating Systems kernel architecture, "
        "process scheduling, synchronization primitives, deadlocks, virtual memory management, paging, and file systems."
    ),
    "chapters": OS_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Operating Systems & Concurrency Architecture: Placement Master Edition (Prescribed Textbook)",
        "Operating Systems (OS)",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering Operating Systems kernel architecture, process scheduling, synchronization primitives, deadlocks, virtual memory management, paging, and file systems.",
        OS_CHAPTERS
    ),
}

CN_TEXTBOOK = {
    "slug": "computer-networks-prescribed-textbook",
    "title": "Computer Networks & Internet Protocols: Campus Master Edition (Prescribed Textbook)",
    "subject": "Computer Networks (CN)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Comprehensive campus placement textbook covering OSI 7-layer model, TCP/IP stack, "
        "CIDR subnetting, transport layer reliability, routing protocols (OSPF/BGP), application protocols (HTTP/2/3, DNS), network security, and socket programming."
    ),
    "chapters": CN_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Computer Networks & Internet Protocols: Campus Master Edition (Prescribed Textbook)",
        "Computer Networks (CN)",
        "2026 Campus Placement Edition",
        "Comprehensive campus placement textbook covering OSI 7-layer model, TCP/IP stack, CIDR subnetting, transport layer reliability, routing protocols (OSPF/BGP), application protocols (HTTP/2/3, DNS), network security, and socket programming.",
        CN_CHAPTERS
    ),
}

DBMS_TEXTBOOK = {
    "slug": "dbms-system-design-prescribed-textbook",
    "title": "Database Management Systems & System Architecture: Placement Master Edition (Prescribed Textbook)",
    "subject": "DBMS & Database Design",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Database Management Systems architecture, "
        "Entity-Relationship modeling, Relational Algebra, Normalization (1NF through 5NF), B+ Trees, 2PL, ACID transaction management, CAP theorem, and System Design."
    ),
    "chapters": DBMS_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Database Management Systems & System Architecture: Placement Master Edition (Prescribed Textbook)",
        "DBMS & Database Design",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering Database Management Systems architecture, Entity-Relationship modeling, Relational Algebra, Normalization (1NF through 5NF), B+ Trees, 2PL, ACID transaction management, CAP theorem, and System Design.",
        DBMS_CHAPTERS
    ),
}

VERBAL_TEXTBOOK = {
    "slug": "verbal-ability-prescribed-textbook",
    "title": "Verbal Ability & Corporate English: Placement Master Edition (Prescribed Textbook)",
    "subject": "Verbal Ability & English",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering corporate English grammar rules, root-word vocabulary, "
        "reading comprehension strategies, para jumbles, cloze test, idioms, verbal deductive logic, and HR interview communication."
    ),
    "chapters": VERBAL_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Verbal Ability & Corporate English: Placement Master Edition (Prescribed Textbook)",
        "Verbal Ability & English",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering corporate English grammar rules, root-word vocabulary, reading comprehension strategies, para jumbles, cloze test, idioms, verbal deductive logic, and HR interview communication.",
        VERBAL_CHAPTERS
    ),
}


C_TEXTBOOK = {
    "slug": "c-programming-prescribed-textbook",
    "title": "C Programming Language: Systems & Placement Foundations (Prescribed Master Textbook)",
    "subject": "C Programming",
    "edition": "2026 Comprehensive Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete, authoritative campus placement master textbook covering C compilation pipeline, memory layout, "
        "pointer arithmetic, dynamic memory allocation, memory leaks, structures, bit-fields, bitwise mechanics, and placement coding traps."
    ),
    "chapters": C_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "C Programming Language: Systems & Placement Foundations (Prescribed Master Textbook)",
        "C Programming",
        "2026 Comprehensive Campus Placement Edition",
        "Complete, authoritative campus placement master textbook covering C compilation pipeline, memory layout, pointer arithmetic, dynamic memory allocation, memory leaks, structures, bit-fields, bitwise mechanics, and placement coding traps.",
        C_CHAPTERS
    ),
}

CPP_TEXTBOOK = {
    "slug": "cpp-programming-prescribed-textbook",
    "title": "Modern C++ Programming & STL Architecture (Prescribed Master Textbook)",
    "subject": "C++ Programming & STL",
    "edition": "2026 Comprehensive Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete, authoritative campus placement master textbook covering Modern C++ (C++11 to C++20), RAII, "
        "Smart Pointers, V-Table internals, Templates, STL Sequence & Associative Containers, Lambdas, and Solved FAANG Competitive Coding Drills."
    ),
    "chapters": CPP_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Modern C++ Programming & STL Architecture (Prescribed Master Textbook)",
        "C++ Programming & STL",
        "2026 Comprehensive Campus Placement Edition",
        "Complete, authoritative campus placement master textbook covering Modern C++ (C++11 to C++20), RAII, Smart Pointers, V-Table internals, Templates, STL Sequence & Associative Containers, Lambdas, and Solved FAANG Competitive Coding Drills.",
        CPP_CHAPTERS
    ),
}

GOLANG_TEXTBOOK = {
    "slug": "golang-programming-prescribed-textbook",
    "title": "Go (Golang) Cloud Systems & Concurrency Architecture (Prescribed Master Textbook)",
    "subject": "Go / Golang Systems Programming",
    "edition": "2026 Comprehensive Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete, authoritative campus placement master textbook covering Go language runtime, escape analysis, "
        "slices/maps memory internals, interfaces, goroutines, CSP channel concurrency, sync primitives, context cancellation, and cloud microservices."
    ),
    "chapters": GOLANG_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Go (Golang) Cloud Systems & Concurrency Architecture (Prescribed Master Textbook)",
        "Go / Golang Systems Programming",
        "2026 Comprehensive Campus Placement Edition",
        "Complete, authoritative campus placement master textbook covering Go language runtime, escape analysis, slices/maps memory internals, interfaces, goroutines, CSP channel concurrency, sync primitives, context cancellation, and cloud microservices.",
        GOLANG_CHAPTERS
    ),
}

RUST_TEXTBOOK = {
    "slug": "rust-programming-prescribed-textbook",
    "title": "Rust Systems & Memory-Safe Architecture (Prescribed Master Textbook)",
    "subject": "Rust Systems Programming",
    "edition": "2026 Comprehensive Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete, authoritative campus placement master textbook covering Rust affine ownership, move semantics, "
        "borrow checker, lifetime annotations, algebraic enums, traits, smart pointers (Box, Rc, Arc, RefCell), fearless concurrency, and unsafe systems programming."
    ),
    "chapters": RUST_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Rust Systems & Memory-Safe Architecture (Prescribed Master Textbook)",
        "Rust Systems Programming",
        "2026 Comprehensive Campus Placement Edition",
        "Complete, authoritative campus placement master textbook covering Rust affine ownership, move semantics, borrow checker, lifetime annotations, algebraic enums, traits, smart pointers (Box, Rc, Arc, RefCell), fearless concurrency, and unsafe systems programming.",
        RUST_CHAPTERS
    ),
}


CLOUD_COMPUTING_TEXTBOOK = {
    "slug": "cloud-computing-prescribed-textbook",
    "title": "Cloud Computing: Architecture, Virtualization & Multi-Cloud Systems (Prescribed Textbook)",
    "subject": "Cloud Computing",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Cloud Computing from hypervisors and service models (IaaS/PaaS/SaaS) "
        "to object/block storage, multi-tier VPC networking, autoscaling, serverless FaaS, IAM/KMS security, and multi-cloud migration."
    ),
    "chapters": CLOUD_COMPUTING_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Cloud Computing: Architecture, Virtualization & Multi-Cloud Systems (Prescribed Textbook)",
        "Cloud Computing",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering Cloud Computing from hypervisors and service models (IaaS/PaaS/SaaS) to object/block storage, multi-tier VPC networking, autoscaling, serverless FaaS, IAM/KMS security, and multi-cloud migration.",
        CLOUD_COMPUTING_CHAPTERS
    ),
}

AWS_TEXTBOOK = {
    "slug": "aws-cloud-prescribed-textbook",
    "title": "AWS Cloud Mastery: Solutions Architect & Serverless Systems (Prescribed Textbook)",
    "subject": "AWS (Amazon Web Services)",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Comprehensive campus placement textbook covering Amazon Web Services (AWS) from global infrastructure, EC2, and S3 "
        "to VPC networking, Aurora/DynamoDB databases, Lambda serverless, IAM/WAF security, and CloudFormation/CDK IaC."
    ),
    "chapters": AWS_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "AWS Cloud Mastery: Solutions Architect & Serverless Systems (Prescribed Textbook)",
        "AWS (Amazon Web Services)",
        "2026 Campus Placement Edition",
        "Comprehensive campus placement textbook covering Amazon Web Services (AWS) from global infrastructure, EC2, and S3 to VPC networking, Aurora/DynamoDB databases, Lambda serverless, IAM/WAF security, and CloudFormation/CDK IaC.",
        AWS_CHAPTERS
    ),
}

CYBERSECURITY_TEXTBOOK = {
    "slug": "cybersecurity-prescribed-textbook",
    "title": "Cybersecurity & Ethical Hacking: Network Defense & SOC (Prescribed Textbook)",
    "subject": "Cybersecurity",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Cybersecurity foundations, the CIA Triad, network security, firewalls, "
        "applied cryptography, OWASP Top 10 web vulnerabilities, OAuth 2.0 / Zero Trust, SIEM/SOC incident response, and penetration testing."
    ),
    "chapters": CYBERSECURITY_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Cybersecurity & Ethical Hacking: Network Defense & SOC (Prescribed Textbook)",
        "Cybersecurity",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering Cybersecurity foundations, the CIA Triad, network security, firewalls, applied cryptography, OWASP Top 10 web vulnerabilities, OAuth 2.0 / Zero Trust, SIEM/SOC incident response, and penetration testing.",
        CYBERSECURITY_CHAPTERS
    ),
}

DEVOPS_TEXTBOOK = {
    "slug": "devops-prescribed-textbook",
    "title": "DevOps & SRE: CI/CD, Docker, Kubernetes & Terraform (Prescribed Textbook)",
    "subject": "DevOps",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Complete campus placement textbook covering DevOps culture, DORA metrics, CI/CD pipelines (GitHub Actions, Jenkins), "
        "Docker containerization, Kubernetes cluster orchestration, Terraform IaC, Ansible automation, Prometheus observability, and SRE."
    ),
    "chapters": DEVOPS_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "DevOps & SRE: CI/CD, Docker, Kubernetes & Terraform (Prescribed Textbook)",
        "DevOps",
        "2026 Campus Placement Edition",
        "Complete campus placement textbook covering DevOps culture, DORA metrics, CI/CD pipelines (GitHub Actions, Jenkins), Docker containerization, Kubernetes cluster orchestration, Terraform IaC, Ansible automation, Prometheus observability, and SRE.",
        DEVOPS_CHAPTERS
    ),
}

GEN_AI_TEXTBOOK = {
    "slug": "generative-ai-prescribed-textbook",
    "title": "Generative AI & LLMs: Prompt Engineering, RAG & Agents (Prescribed Textbook)",
    "subject": "Generative AI",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering Generative AI from the Transformer architecture and self-attention "
        "to LLM tokenization, advanced prompt engineering, RAG vector retrieval, PEFT/LoRA fine-tuning, autonomous agents, and multimodal AI."
    ),
    "chapters": GEN_AI_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Generative AI & LLMs: Prompt Engineering, RAG & Agents (Prescribed Textbook)",
        "Generative AI",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering Generative AI from the Transformer architecture and self-attention to LLM tokenization, advanced prompt engineering, RAG vector retrieval, PEFT/LoRA fine-tuning, autonomous agents, and multimodal AI.",
        GEN_AI_CHAPTERS
    ),
}

DEEP_LEARNING_TEXTBOOK = {
    "slug": "deep-learning-prescribed-textbook",
    "title": "Deep Learning: Neural Networks, PyTorch & Transformers (Prescribed Textbook)",
    "subject": "Deep Learning",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Comprehensive campus placement textbook covering Deep Neural Networks from perceptrons and backpropagation "
        "to optimizers (AdamW), PyTorch pipelines, CNN backbones, RNNs/LSTMs, Vision Transformers (ViT), VAEs/GANs, and distributed DDP training."
    ),
    "chapters": DEEP_LEARNING_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Deep Learning: Neural Networks, PyTorch & Transformers (Prescribed Textbook)",
        "Deep Learning",
        "2026 Campus Placement Edition",
        "Comprehensive campus placement textbook covering Deep Neural Networks from perceptrons and backpropagation to optimizers (AdamW), PyTorch pipelines, CNN backbones, RNNs/LSTMs, Vision Transformers (ViT), VAEs/GANs, and distributed DDP training.",
        DEEP_LEARNING_CHAPTERS
    ),
}

SOFTWARE_TESTING_TEXTBOOK = {
    "slug": "software-testing-prescribed-textbook",
    "title": "Software Testing & QA: Automation, Selenium & API Testing (Prescribed Textbook)",
    "subject": "Software Testing & QA",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Authoritative campus placement textbook covering the Software Testing Life Cycle (STLC), black-box/white-box test design, "
        "Selenium WebDriver with Page Object Model, REST API automation with REST Assured, PyTest frameworks, JMeter load testing, and Playwright."
    ),
    "chapters": SOFTWARE_TESTING_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Software Testing & QA: Automation, Selenium & API Testing (Prescribed Textbook)",
        "Software Testing & QA",
        "2026 Campus Placement Edition",
        "Authoritative campus placement textbook covering the Software Testing Life Cycle (STLC), black-box/white-box test design, Selenium WebDriver with Page Object Model, REST API automation with REST Assured, PyTest frameworks, JMeter load testing, and Playwright.",
        SOFTWARE_TESTING_CHAPTERS
    ),
}

DATA_SCIENCE_TEXTBOOK = {
    "slug": "data-science-prescribed-textbook",
    "title": "Data Science & Analytics: Python, Statistics, ML & Big Data (Prescribed Textbook)",
    "subject": "Data Science",
    "edition": "2026 Campus Placement Edition",
    "author": "Prescribed Courseware Architectural Board",
    "description": (
        "Comprehensive campus placement textbook covering the Data Science lifecycle (CRISP-DM), NumPy/Pandas manipulation, "
        "EDA and outlier capping, hypothesis testing (P-values, t-tests, ANOVA), Scikit-Learn pipelines, XGBoost, clustering, and SHAP explainability."
    ),
    "chapters": DATA_SCIENCE_CHAPTERS,
    "full_textbook_markdown": assemble_full_textbook_markdown(
        "Data Science & Analytics: Python, Statistics, ML & Big Data (Prescribed Textbook)",
        "Data Science",
        "2026 Campus Placement Edition",
        "Comprehensive campus placement textbook covering the Data Science lifecycle (CRISP-DM), NumPy/Pandas manipulation, EDA and outlier capping, hypothesis testing (P-values, t-tests, ANOVA), Scikit-Learn pipelines, XGBoost, clustering, and SHAP explainability.",
        DATA_SCIENCE_CHAPTERS
    ),
}

ALL_PRESCRIBED_TEXTBOOKS = [
    JAVA_TEXTBOOK,
    PYTHON_TEXTBOOK,
    DSA_TEXTBOOK,
    JAVASCRIPT_TEXTBOOK,
    AI_ML_TEXTBOOK,
    DATA_SCIENCE_TEXTBOOK,
    CLOUD_COMPUTING_TEXTBOOK,
    AWS_TEXTBOOK,
    CYBERSECURITY_TEXTBOOK,
    DEVOPS_TEXTBOOK,
    SQL_TEXTBOOK,
    GEN_AI_TEXTBOOK,
    DEEP_LEARNING_TEXTBOOK,
    SOFTWARE_TESTING_TEXTBOOK,
    DATA_ENG_TEXTBOOK,
    OS_TEXTBOOK,
    CN_TEXTBOOK,
    DBMS_TEXTBOOK,
    QUANT_TEXTBOOK,
    LOGICAL_TEXTBOOK,
    VERBAL_TEXTBOOK,
    C_TEXTBOOK,
    CPP_TEXTBOOK,
    GOLANG_TEXTBOOK,
    RUST_TEXTBOOK,
]

SUBJECT_TO_TEXTBOOK: Dict[str, Dict[str, Any]] = {
    "data structures & algorithms (dsa)": DSA_TEXTBOOK,
    "dsa": DSA_TEXTBOOK,
    "data structures": DSA_TEXTBOOK,
    "algorithms": DSA_TEXTBOOK,
    "sql & database queries": SQL_TEXTBOOK,
    "sql": SQL_TEXTBOOK,
    "database": SQL_TEXTBOOK,
    "quantitative aptitude": QUANT_TEXTBOOK,
    "quant": QUANT_TEXTBOOK,
    "aptitude": QUANT_TEXTBOOK,
    "logical reasoning": LOGICAL_TEXTBOOK,
    "logical": LOGICAL_TEXTBOOK,
    "reasoning": LOGICAL_TEXTBOOK,
    "java": JAVA_TEXTBOOK,
    "python": PYTHON_TEXTBOOK,
    "javascript / typescript": JAVASCRIPT_TEXTBOOK,
    "javascript": JAVASCRIPT_TEXTBOOK,
    "typescript": JAVASCRIPT_TEXTBOOK,
    "js": JAVASCRIPT_TEXTBOOK,
    "operating systems (os)": OS_TEXTBOOK,
    "operating systems": OS_TEXTBOOK,
    "os": OS_TEXTBOOK,
    "computer networks (cn)": CN_TEXTBOOK,
    "computer networks": CN_TEXTBOOK,
    "cn": CN_TEXTBOOK,
    "networks": CN_TEXTBOOK,
    "dbms & database design": DBMS_TEXTBOOK,
    "dbms": DBMS_TEXTBOOK,
    "database management systems": DBMS_TEXTBOOK,
    "system design": DBMS_TEXTBOOK,
    "verbal ability & english": VERBAL_TEXTBOOK,
    "verbal ability": VERBAL_TEXTBOOK,
    "verbal": VERBAL_TEXTBOOK,
    "english": VERBAL_TEXTBOOK,
    "data engineering & big data": DATA_ENG_TEXTBOOK,
    "data engineering": DATA_ENG_TEXTBOOK,
    "big data": DATA_ENG_TEXTBOOK,
    "artificial intelligence & machine learning (ai / ml)": AI_ML_TEXTBOOK,
    "ai_ml": AI_ML_TEXTBOOK,
    "ai and machine learning": AI_ML_TEXTBOOK,
    "sql_db": SQL_TEXTBOOK,
    "sql & database management": SQL_TEXTBOOK,
    "ai / ml": AI_ML_TEXTBOOK,
    "machine learning": AI_ML_TEXTBOOK,
    "ai": AI_ML_TEXTBOOK,
    "c programming": C_TEXTBOOK,
    "c": C_TEXTBOOK,
    "c language": C_TEXTBOOK,
    "c++ programming & stl": CPP_TEXTBOOK,
    "c++ programming": CPP_TEXTBOOK,
    "c++": CPP_TEXTBOOK,
    "cpp": CPP_TEXTBOOK,
    "stl": CPP_TEXTBOOK,
    "go / golang systems programming": GOLANG_TEXTBOOK,
    "go": GOLANG_TEXTBOOK,
    "golang": GOLANG_TEXTBOOK,
    "go programming": GOLANG_TEXTBOOK,
    "rust systems programming": RUST_TEXTBOOK,
    "rust": RUST_TEXTBOOK,
    "rust programming": RUST_TEXTBOOK,
    # Cloud Computing
    "cloud computing": CLOUD_COMPUTING_TEXTBOOK,
    "cloud": CLOUD_COMPUTING_TEXTBOOK,
    "cloud_computing": CLOUD_COMPUTING_TEXTBOOK,
    "cloud-computing-prescribed-textbook": CLOUD_COMPUTING_TEXTBOOK,
    # AWS
    "aws (amazon web services)": AWS_TEXTBOOK,
    "aws": AWS_TEXTBOOK,
    "amazon web services": AWS_TEXTBOOK,
    "aws-cloud-prescribed-textbook": AWS_TEXTBOOK,
    # Cybersecurity
    "cybersecurity": CYBERSECURITY_TEXTBOOK,
    "security": CYBERSECURITY_TEXTBOOK,
    "cyber": CYBERSECURITY_TEXTBOOK,
    "cybersecurity-prescribed-textbook": CYBERSECURITY_TEXTBOOK,
    # DevOps
    "devops": DEVOPS_TEXTBOOK,
    "sre": DEVOPS_TEXTBOOK,
    "ci/cd": DEVOPS_TEXTBOOK,
    "devops-prescribed-textbook": DEVOPS_TEXTBOOK,
    # Generative AI
    "generative ai": GEN_AI_TEXTBOOK,
    "gen ai": GEN_AI_TEXTBOOK,
    "gen_ai": GEN_AI_TEXTBOOK,
    "generative-ai-prescribed-textbook": GEN_AI_TEXTBOOK,
    # Deep Learning
    "deep learning": DEEP_LEARNING_TEXTBOOK,
    "deep_learning": DEEP_LEARNING_TEXTBOOK,
    "deep-learning-prescribed-textbook": DEEP_LEARNING_TEXTBOOK,
    # Software Testing
    "software testing & qa": SOFTWARE_TESTING_TEXTBOOK,
    "software testing": SOFTWARE_TESTING_TEXTBOOK,
    "software_testing": SOFTWARE_TESTING_TEXTBOOK,
    "testing": SOFTWARE_TESTING_TEXTBOOK,
    "qa": SOFTWARE_TESTING_TEXTBOOK,
    "sdet": SOFTWARE_TESTING_TEXTBOOK,
    "software-testing-prescribed-textbook": SOFTWARE_TESTING_TEXTBOOK,
    # Data Science
    "data science": DATA_SCIENCE_TEXTBOOK,
    "data_science": DATA_SCIENCE_TEXTBOOK,
    "data-science-prescribed-textbook": DATA_SCIENCE_TEXTBOOK,
    # Full-Stack Web Dev aliases
    "full-stack web dev": JAVASCRIPT_TEXTBOOK,
    "web dev": JAVASCRIPT_TEXTBOOK,
    "web_dev": JAVASCRIPT_TEXTBOOK,
    "full-stack": JAVASCRIPT_TEXTBOOK,
}


# =============================================================================
# 2. VERIFIED QUESTION BANKS (100% GROUNDED IN BOOK CHAPTERS)
# =============================================================================

JAVA_BOOK_QUESTIONS = JAVA_EXPANDED_BOOK_QUESTIONS
PYTHON_BOOK_QUESTIONS = PYTHON_EXPANDED_QUESTIONS
DSA_BOOK_QUESTIONS = DSA_EXPANDED_QUESTIONS
SQL_BOOK_QUESTIONS = SQL_EXPANDED_QUESTIONS
QUANT_BOOK_QUESTIONS = QUANT_EXPANDED_QUESTIONS
LOGICAL_BOOK_QUESTIONS = LOGICAL_EXPANDED_QUESTIONS
JAVASCRIPT_BOOK_QUESTIONS = JAVASCRIPT_EXPANDED_QUESTIONS
DATA_ENG_BOOK_QUESTIONS = DATA_ENG_EXPANDED_QUESTIONS
AI_ML_BOOK_QUESTIONS = AI_ML_EXPANDED_QUESTIONS
OS_BOOK_QUESTIONS = OS_EXPANDED_QUESTIONS
CN_BOOK_QUESTIONS = CN_EXPANDED_QUESTIONS
DBMS_BOOK_QUESTIONS = DBMS_EXPANDED_QUESTIONS
VERBAL_BOOK_QUESTIONS = VERBAL_EXPANDED_QUESTIONS

def extract_book_questions_from_chapters(chapters: List[Dict[str, Any]], textbook_name: str) -> List[Dict[str, Any]]:
    questions = []
    for ch in chapters:
        c_num = ch.get("chapter_num", 1)
        c_title = ch.get("title", f"Chapter {c_num}")
        pqs = ch.get("sections", {}).get("practice_questions", [])
        for pq in pqs:
            opts = pq.get("options", [])
            corr = pq.get("correct_answer", "")
            corr_idx = 0
            for idx, opt in enumerate(opts):
                if opt.strip().startswith(corr.strip()[:2]) or corr.strip() in opt:
                    corr_idx = idx
                    break
            questions.append({
                "chapter_num": c_num,
                "chapter_title": c_title,
                "subtopic": c_title,
                "question": pq.get("question", ""),
                "options": opts,
                "correct_option_index": corr_idx,
                "explanation": f"📖 [{textbook_name} — Chapter {c_num}: {c_title}]\n" + (pq.get("detailed_solution") or pq.get("explanation", "")),
                "difficulty": "medium",
            })
    return questions

C_BOOK_QUESTIONS = extract_book_questions_from_chapters(C_CHAPTERS, "C Programming Language Master Textbook")
CPP_BOOK_QUESTIONS = extract_book_questions_from_chapters(CPP_CHAPTERS, "Modern C++ & STL Master Textbook")
GOLANG_BOOK_QUESTIONS = extract_book_questions_from_chapters(GOLANG_CHAPTERS, "Go Cloud Systems Master Textbook")
RUST_BOOK_QUESTIONS = extract_book_questions_from_chapters(RUST_CHAPTERS, "Rust Systems Architecture Master Textbook")

TOPIC_QUESTION_BANKS: Dict[str, List[Dict[str, Any]]] = {
    "c": C_BOOK_QUESTIONS,
    "c-programming": C_BOOK_QUESTIONS,
    "cpp": CPP_BOOK_QUESTIONS,
    "c++": CPP_BOOK_QUESTIONS,
    "go": GOLANG_BOOK_QUESTIONS,
    "golang": GOLANG_BOOK_QUESTIONS,
    "rust": RUST_BOOK_QUESTIONS,
    "java": JAVA_BOOK_QUESTIONS,
    "python": PYTHON_BOOK_QUESTIONS,
    "dsa": DSA_BOOK_QUESTIONS,
    "sql": SQL_BOOK_QUESTIONS,
    "quantitative-aptitude": QUANT_BOOK_QUESTIONS,
    "logical-reasoning": LOGICAL_BOOK_QUESTIONS,
    "javascript": JAVASCRIPT_BOOK_QUESTIONS,
    "operating-systems": OS_BOOK_QUESTIONS,
    "os": OS_BOOK_QUESTIONS,
    "computer-networks": CN_BOOK_QUESTIONS,
    "cn": CN_BOOK_QUESTIONS,
    "dbms": DBMS_BOOK_QUESTIONS,
    "verbal-ability": VERBAL_BOOK_QUESTIONS,
    "verbal": VERBAL_BOOK_QUESTIONS,
    "data-engineering": DATA_ENG_BOOK_QUESTIONS,
    "ai-machine-learning": AI_ML_BOOK_QUESTIONS,
}


# =============================================================================
# 3. BOOK DETECTION & PDF INGESTION UTILITIES
# =============================================================================

def find_prescribed_book_pdf(subject: str) -> Optional[str]:
    """
    Locates an uploaded or dataset PDF for any prescribed subject or slug.
    Checks dataset/books/, dataset/, uploads/books/, and uploads/.
    """
    norm = subject.lower().strip()
    norm_slug = norm.replace(" ", "-")

    # Map common aliases to keywords
    if "data structures" in norm or "dsa" in norm:
        key = "dsa"
    elif "sql" in norm or "database" in norm:
        key = "sql"
    elif "quant" in norm or "aptitude" in norm:
        key = "quant"
    elif "logical" in norm or "reasoning" in norm:
        key = "logical"
    elif "javascript" in norm or "typescript" in norm or "js" in norm:
        key = "javascript"
    elif "data engineering" in norm or "big data" in norm:
        key = "data_engineering"
    elif "ai" in norm or "machine learning" in norm or "ml" in norm:
        key = "ai_ml"
    elif "operating" in norm or "os" in norm:
        key = "os"
    elif "network" in norm or "cn" in norm:
        key = "cn"
    elif "dbms" in norm or "system design" in norm:
        key = "dbms"
    elif "verbal" in norm or "english" in norm:
        key = "verbal"
    elif "python" in norm:
        key = "python"
    elif "c++" in norm or "cpp" in norm:
        key = "cpp"
    elif "golang" in norm or "go" in norm:
        key = "golang"
    elif "rust" in norm:
        key = "rust"
    elif "c programming" in norm or norm == "c":
        key = "c"
    elif "java" in norm:
        key = "java"
    else:
        key = norm.replace(" ", "_")

    candidate_dirs = [
        DATASET_BOOKS_DIR,
        Path(__file__).resolve().parent.parent.parent.parent / "dataset",
        Path(__file__).resolve().parent.parent.parent.parent.parent / "dataset" / "books",
        Path(__file__).resolve().parent.parent.parent.parent.parent / "dataset",
        UPLOADS_BOOKS_DIR,
        Path(__file__).resolve().parent.parent.parent / "uploads",
    ]

    # 1. First priority: exact slug or key match
    for cdir in candidate_dirs:
        if not cdir.exists():
            continue
        exact_slug = cdir / f"{norm_slug}.pdf"
        if exact_slug.is_file():
            return str(exact_slug)
        exact_key = cdir / f"{key}_prescribed_book.pdf"
        if exact_key.is_file():
            return str(exact_key)
        exact_textbook = cdir / f"{key}_prescribed_textbook.pdf"
        if exact_textbook.is_file():
            return str(exact_textbook)

    # 2. Second priority: substring keyword match
    for cdir in candidate_dirs:
        if not cdir.exists():
            continue
        for p in cdir.iterdir():
            if p.is_file() and p.suffix.lower() == ".pdf":
                name = p.name.lower()
                if (key and key in name) or (norm in name) or (norm_slug in name):
                    return str(p)

    return None


def get_prescribed_books_status(filter_topic: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns overview of prescribed textbooks, chapters count, and detected PDF status."""
    books = ALL_PRESCRIBED_TEXTBOOKS
    if filter_topic and isinstance(filter_topic, str) and filter_topic.lower() != "all":
        norm = filter_topic.lower().strip()
        matched = []
        for b in books:
            if norm in b["subject"].lower() or norm in b["slug"].lower() or b["subject"].lower() in norm:
                matched.append(b)
        if matched:
            books = matched

    result = []
    for b in books:
        pdf_path = find_prescribed_book_pdf(b["slug"]) or find_prescribed_book_pdf(b["subject"])
        result.append({
            "subject": b["subject"],
            "slug": b["slug"],
            "title": b["title"],
            "edition": b["edition"],
            "author": b["author"],
            "description": b["description"],
            "chapters_count": len(b["chapters"]),
            "chapters": b["chapters"],
            "has_physical_pdf": pdf_path is not None,
            "pdf_filename": Path(pdf_path).name if pdf_path else None,
            "pdf_download_url": f"/api/study-materials/books/{b['slug']}/download-pdf",
            "exam_grounding_policy": "Strict: 100% of questions are derived exclusively from these chapters.",
        })
    return result


def ingest_book_pdf(file_path: str, subject: str) -> Dict[str, Any]:
    """
    Extracts chapters and pages from an uploaded PDF book using PyMuPDF.
    Updates the chapter structure and indices.
    """
    path = Path(file_path)
    if not path.exists():
        return {"success": False, "error": f"File '{file_path}' does not exist"}

    try:
        doc = pymupdf.open(str(path))
        page_count = len(doc)
        toc = doc.get_toc()

        extracted_chapters = []
        if toc:
            for item in toc:
                lvl, title, page = item[0], item[1], item[2]
                if lvl == 1:
                    extracted_chapters.append({
                        "chapter_num": len(extracted_chapters) + 1,
                        "title": title.strip(),
                        "page": page,
                    })

        return {
            "success": True,
            "filename": path.name,
            "page_count": page_count,
            "extracted_chapters": extracted_chapters,
            "has_table_of_contents": len(extracted_chapters) > 0,
        }
    except Exception as e:
        logger.error(f"Error parsing PDF '{file_path}': {e}")
        return {"success": False, "error": str(e)}


# =============================================================================
# 4. TEXTBOOK MARKDOWN CONTENT GENERATOR & DB SEEDER
# =============================================================================

def build_textbook_markdown(book: Dict[str, Any]) -> str:
    """Renders complete comprehensive textbook markdown with all chapters and takeaways."""
    if book.get("full_textbook_markdown"):
        return book["full_textbook_markdown"]

    md = [
        f"# {book['title']}",
        f"**Edition:** {book['edition']}  ",
        f"**Subject:** {book['subject']}  ",
        f"**Author:** {book['author']}  ",
        "",
        "> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, practice quizzes, and milestone tests "
        f"for **{book['subject']}** are strictly grounded exclusively in the concepts, algorithms, and models "
        "defined within this textbook. Master these chapters to guarantee 100% test preparedness.",
        "",
        "## Overview & Course Objectives",
        book["description"],
        "",
        "---",
        "",
        "## Complete Chapter Curriculum & Detailed Syllabus",
        "",
    ]

    for ch in book["chapters"]:
        md.append(f"### Chapter {ch['chapter_num']}: {ch['title']}")
        md.append("")
        md.append(f"> **Key Principle / Exam Takeaway:** {ch['key_takeaways']}")
        md.append("")
        md.append("**Syllabus Topics Covered:**")
        for top in ch["topics"]:
            md.append(f"- ✓ {top}")
        md.append("")
        md.append("---")
        md.append("")

    md.extend([
        "## 💡 Placement Exam Preparation Strategy",
        "1. Study each chapter systematically, focusing on core conceptual trade-offs and mathematical proofs.",
        "2. Review the chapter key principles and ensure understanding of core real-world architecture.",
        "3. Every practice exam question cites the exact chapter in its step-by-step verified solution.",
    ])

    return "\n".join(md)


def seed_prescribed_books_to_db(db: Session) -> None:
    """Inserts or updates all prescribed textbooks in the study_materials table."""
    books = ALL_PRESCRIBED_TEXTBOOKS

    for idx, b in enumerate(books):
        mat = db.query(StudyMaterial).filter(StudyMaterial.slug == b["slug"]).first()
        md_content = build_textbook_markdown(b)
        tags = [b["subject"], "Textbook", "Prescribed Curriculum", "Placement Exam Syllabus", "Core Guide"]

        if not mat:
            mat = StudyMaterial(
                title=b["title"],
                slug=b["slug"],
                category="textbook",
                content_type="textbook",
                description=b["description"],
                content_markdown=md_content,
                company_tag="Prescribed Curriculum",
                difficulty="intermediate",
                estimated_read_time="60 mins",
                tags_json=json.dumps(tags),
                order_index=idx + 1,
            )
            db.add(mat)
            logger.info(f"Seeded Prescribed Textbook: {b['title']}")
        else:
            mat.title = b["title"]
            mat.description = b["description"]
            mat.content_markdown = md_content
            mat.content_type = "textbook"
            mat.company_tag = "Prescribed Curriculum"
            mat.tags_json = json.dumps(tags)
            mat.order_index = idx + 1

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to commit prescribed books: {e}")


# =============================================================================
# 5. STRICT BOOK-GROUNDED QUESTION GENERATION ENGINE (ALL TOPICS)
# =============================================================================

def get_book_scope_prompt(topics: List[str]) -> str:
    """
    Returns strict LLM prompt instructions restricting questions
    exclusively to topics covered in each corresponding prescribed textbook.
    """
    if not topics:
        return ""

    instructions = [
        "\nCRITICAL REQUIREMENT — PRESCRIBED TEXTBOOK GROUNDING:",
        "All questions for each topic MUST BE DERIVED STRICTLY AND ONLY from the chapters and topics in the provided prescribed textbooks.",
        "Do NOT ask questions on external unverified third-party libraries, obscure syntax, or unlisted technologies.",
        "Each question's 'explanation' MUST start with: '📖 [Book Reference: Chapter X - Topic Name]' followed by the solution.",
        "Scope constraints by subject:",
    ]

    has_any = False
    for t in topics:
        norm = t.lower().strip()
        matched_book = None
        for k, b in SUBJECT_TO_TEXTBOOK.items():
            if k in norm or norm in k:
                matched_book = b
                break

        if matched_book:
            has_any = True
            ch_summary = ", ".join([f"Ch {c['chapter_num']}: {c['title']}" for c in matched_book["chapters"][:6]])
            instructions.append(f"- {matched_book['subject']} Prescribed Scope: {ch_summary} (and related advanced chapters).")

    if not has_any:
        return ""

    return "\n".join(instructions)


def get_book_grounded_fallback_questions(
    subject: str,
    count: int = 1,
    difficulty: str = "medium",
    marks_per_question: float = 1.0,
) -> List[AptitudeQuestionGeneratedItem]:
    """
    Generates verified questions directly modeled on the prescribed textbook chapters
    for ANY subject (DSA, SQL, Quant, Logical, Java, Python, JavaScript, Data Eng, AI/ML).
    Balances option letters across A, B, C, D (0, 1, 2, 3) and attaches the chapter reference.
    """
    norm = subject.lower().strip()
    
    # Identify pool
    pool = None
    topic_display = subject
    for k, questions in TOPIC_QUESTION_BANKS.items():
        if k in norm or norm in k:
            pool = questions
            # Set topic display
            for sub_key, b in SUBJECT_TO_TEXTBOOK.items():
                if sub_key in norm or norm in sub_key:
                    topic_display = b["subject"]
                    break
            break

    if not pool:
        # Fallback to general DSA or Java
        pool = DSA_BOOK_QUESTIONS if "dsa" in norm or "algorithm" in norm else JAVA_BOOK_QUESTIONS
        topic_display = subject

    results = []
    shuffled_pool = list(pool)
    random.shuffle(shuffled_pool)

    for i in range(count):
        raw = copy.deepcopy(shuffled_pool[i % len(shuffled_pool)])

        # Option balancing
        target_idx = i % 4
        orig_idx = raw["correct_option_index"]
        if orig_idx != target_idx:
            options = raw["options"]
            correct_val = options[orig_idx]
            other_vals = [opt for idx, opt in enumerate(options) if idx != orig_idx]
            new_options = []
            other_pointer = 0
            for slot in range(4):
                if slot == target_idx:
                    new_options.append(correct_val)
                else:
                    new_options.append(other_vals[other_pointer])
                    other_pointer += 1
            raw["options"] = new_options
            raw["correct_option_index"] = target_idx

        results.append(
            AptitudeQuestionGeneratedItem(
                topic_name=topic_display,
                subtopic=f"Chapter {raw['chapter_num']}: {raw['chapter_title']} ({raw['subtopic']})",
                question=raw["question"],
                options=raw["options"],
                correct_option_index=raw["correct_option_index"],
                explanation=raw["explanation"],
                difficulty=raw["difficulty"] if difficulty == "mixed" else difficulty,
                marks=marks_per_question,
            )
        )

    return results
