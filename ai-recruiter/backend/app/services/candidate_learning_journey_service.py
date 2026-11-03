"""
candidate_learning_journey_service.py — Service for Candidate Learning Roadmap,
Stage-Gated Progression (Foundations -> Advanced -> Projects -> Placement Ready),
Dynamic Recommendations, Daily Study Plan, Strengths & Focus Areas Analytics.
Supports choosing a target course (e.g. Java Programming, Python Full Stack, DSA, Web Dev)
with complete step-by-step guidance: study materials, practical coding exercises,
real-world projects, and campus placement training.
"""
from datetime import datetime, timezone, timedelta
import json
import logging
import uuid
import copy
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from app.models.student import (
    StudentLearningPreference,
    CandidateTestAttempt,
    AptitudeTestResult,
    StudentRoadmapProgress,
)
from app.models.candidate import CandidateProfile
from app.models.coding import CandidateCodingAttempt
from app.models.interview import Interview
from app.models.user import User

logger = logging.getLogger("ai_recruiter.learning_journey")


def compute_dynamic_phase_schedules(base_date: Optional[datetime] = None) -> List[str]:
    """
    Computes dynamic, realistic 90-day placement sprint schedules starting from base_date (Day 1):
    - Phase 1: Foundations (Days 1 - 21) -> Weeks 1-3
    - Phase 2: Core Engineering (Days 22 - 50) -> Weeks 4-7
    - Phase 3: Advanced & Projects (Days 51 - 70) -> Weeks 8-10
    - Phase 4: Placement Ready (Days 71 - 90) -> Weeks 11-12
    """
    start_date = base_date or datetime.now()
    p1_start = start_date
    p1_end = start_date + timedelta(days=20)

    p2_start = p1_end + timedelta(days=1)
    p2_end = start_date + timedelta(days=49)

    p3_start = p2_end + timedelta(days=1)
    p3_end = start_date + timedelta(days=69)

    p4_start = p3_end + timedelta(days=1)
    p4_end = start_date + timedelta(days=89)

    def fmt_range(d1: datetime, d2: datetime) -> str:
        return f"{d1.strftime('%b %d')} - {d2.strftime('%b %d')}"

    return [
        fmt_range(p1_start, p1_end),
        fmt_range(p2_start, p2_end),
        fmt_range(p3_start, p3_end),
        fmt_range(p4_start, p4_end),
    ]


PHASE_SCHEDULE_META: List[Dict[str, Any]] = [
    {
        "phase_num": 1,
        "weekly_schedule": "Weeks 1–3 (Days 1–21)",
        "expected_topics_count": 15,
        "stage_title": "Foundations & Syntax Mechanics",
        "focus": "Core Language Syntax, JVM/Runtime Architecture, Data Structures & OOP Foundations",
    },
    {
        "phase_num": 2,
        "weekly_schedule": "Weeks 4–7 (Days 22–50)",
        "expected_topics_count": 15,
        "stage_title": "Core Engineering & Deep Architecture",
        "focus": "Collections Framework, Concurrency, Multithreading, Asynchronous I/O & Databases",
    },
    {
        "phase_num": 3,
        "weekly_schedule": "Weeks 8–10 (Days 51–70)",
        "expected_topics_count": 10,
        "stage_title": "Production Systems & Real-World Projects",
        "focus": "REST Microservices, High-Scale Enterprise Architectures, Cloud Dockerization",
    },
    {
        "phase_num": 4,
        "weekly_schedule": "Weeks 11–12 (Days 71–90)",
        "expected_topics_count": 10,
        "stage_title": "Placement Sprints & Mock Interviews",
        "focus": "Campus Placement Coding Rounds, Speed Tests, AI Proctored Technical & Behavioral Interviews",
    },
]


def build_12_week_schedule(
    course_id: str,
    base_date: datetime,
    is_started: bool,
    completed_topics: List[str],
) -> List[Dict[str, Any]]:
    """
    Builds the complete 12-week schedule (90 days) for the candidate's active course track,
    mapping out week-by-week topic allocations, calendar dates, milestones, and progress.
    """
    norm = course_id.lower().strip() if course_id else "java"
    curr = get_course_curriculum_details(norm)
    chapters = curr.get("chapters", [])
    completed_set = set(str(t).lower() for t in completed_topics)

    now = datetime.now()
    days_elapsed = (now - base_date).days if is_started else 0
    current_week_num = min(12, max(1, (days_elapsed // 7) + 1)) if is_started else 1

    weeks = []
    for w in range(1, 13):
        if w <= 10:
            w_start = base_date + timedelta(days=(w - 1) * 7)
            w_end = w_start + timedelta(days=6)
            days_label = f"Days {(w - 1) * 7 + 1}-{w * 7}"
            ch_idx = w - 1
            ch = chapters[ch_idx] if ch_idx < len(chapters) else {}
            week_title = ch.get("title", f"Module {w}: Core Engineering & Implementation")
            phase_num = 1 if w <= 3 else (2 if w <= 7 else 3)
            phase_name = (
                "Phase 1: Foundations" if phase_num == 1 else
                ("Phase 2: Core Engineering" if phase_num == 2 else "Phase 3: Production Systems & Projects")
            )
            raw_topics = ch.get("topics", [])
            topics_list = []
            for t_idx, t_name in enumerate(raw_topics):
                t_id = f"topic-{w}-{t_idx + 1}"
                is_done = is_started and (t_id.lower() in completed_set or str(t_name).lower() in completed_set)
                topics_list.append({
                    "id": t_id,
                    "title": t_name,
                    "is_completed": is_done,
                    "order": t_idx + 1,
                })
            real_world_app = ch.get("real_world_app", "")
        elif w == 11:
            w_start = base_date + timedelta(days=70)
            w_end = base_date + timedelta(days=79)
            days_label = "Days 71-80"
            week_title = "Placement Sprint 1: Company Technical Assessments & Problem Solving Drills"
            phase_num = 4
            phase_name = "Phase 4: Placement Ready"
            real_world_app = "Amazon, Google, Microsoft, TCS, Infosys technical screening round drills"
            topics_list = [
                {"id": "topic-11-1", "title": "High-Frequency Company Coding Challenges & LeetCode Sprints", "is_completed": False, "order": 1},
                {"id": "topic-11-2", "title": "Data Structures & Algorithm Optimization Speed Tests", "is_completed": False, "order": 2},
                {"id": "topic-11-3", "title": "System Design & Enterprise Architecture Walkthroughs", "is_completed": False, "order": 3},
                {"id": "topic-11-4", "title": "Live Timed Technical Coding Assessment Drills", "is_completed": False, "order": 4},
            ]
        else:
            w_start = base_date + timedelta(days=80)
            w_end = base_date + timedelta(days=89)
            days_label = "Days 81-90"
            week_title = "Placement Sprint 2: AI Proctored Mock Interviews & Final Readiness Verification"
            phase_num = 4
            phase_name = "Phase 4: Placement Ready"
            real_world_app = "Full placement sign-off, live AI proctored interview, portfolio & resume audit"
            topics_list = [
                {"id": "topic-12-1", "title": "AI Proctored Technical Mock Interview with Live Audio/Video", "is_completed": False, "order": 1},
                {"id": "topic-12-2", "title": "HR Behavioral Interview & STAR Method Response Mastery", "is_completed": False, "order": 2},
                {"id": "topic-12-3", "title": "ATS Resume Score Optimization & Production Portfolio Review", "is_completed": False, "order": 3},
                {"id": "topic-12-4", "title": "Final Placement Readiness Audit & Direct Job Application Dispatch", "is_completed": False, "order": 4},
            ]

        done_cnt = sum(1 for t in topics_list if t.get("is_completed"))
        total_cnt = len(topics_list)
        pct = round((done_cnt / max(1, total_cnt)) * 100.0, 1) if is_started else 0.0

        if not is_started:
            status = "Ready to Start" if w == 1 else "Locked"
        elif pct >= 100.0:
            status = "Completed"
        elif w == current_week_num:
            status = "In Progress"
        elif w < current_week_num:
            status = "In Progress"
        else:
            status = "Upcoming"

        weeks.append({
            "week_num": w,
            "days_label": days_label,
            "phase_num": phase_num,
            "phase_name": phase_name,
            "title": week_title,
            "date_range": f"{w_start.strftime('%b %d')} - {w_end.strftime('%b %d')}",
            "target_completion_date": w_end.strftime("%b %d, %Y"),
            "topics": topics_list,
            "topics_count": total_cnt,
            "completed_topics_count": done_cnt,
            "progress_percent": pct,
            "status": status,
            "is_current_week": (w == current_week_num) if is_started else (w == 1),
            "real_world_app": real_world_app,
        })

    return weeks


COURSE_TRACKS: Dict[str, Dict[str, Any]] = {
    "java": {
        "id": "java",
        "name": "Java Programming",
        "title": "Java Programming: Beginner to Placement Ready",
        "icon": "☕",
        "badge": "Most Popular for Placements",
        "target_role": "Java Backend Developer / SDE-1 / Enterprise Engineer",
        "description": "Complete step-by-step guidance from Java basics and JVM memory management to Collections, Concurrency, Spring Boot REST microservices, real-world projects, and campus placement interviews.",
        "phases": [
            {
                "id": "phase-1",
                "phase_num": 1,
                "name": "Phase 1: Foundations",
                "subtitle": "Master Java syntax, JVM runtime & core OOP principles",
                "progress_percent": 0.0,
                "status": "In Progress",
                "is_locked": False,
                "icon": "layers",
                "badge_color": "success",
                "level": "Beginner Level",
                "topics_covered": ["Java Syntax & Primitive Data Types", "JVM Architecture & Memory (Heap vs Stack)", "Flow Control, Loops & Arrays", "OOP Principles: Classes, Encapsulation & Inheritance"],
                "courses": [
                    {"id": "java-101", "name": "Java Syntax & Variables Mechanics", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "java-102", "name": "JVM Architecture & Heap vs Stack", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "java-103", "name": "Algorithmic Logic & Loops in Java", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "java-104", "name": "Core OOP: Classes, Encapsulation & Polymorphism", "progress_percent": 0.0, "status": "Not Started"},
                ],
                "action_url": "study-materials.html?subject=java",
                "action_text": "Study Java Foundations",
            },
            {
                "id": "phase-2",
                "phase_num": 2,
                "name": "Phase 2: Core Skills",
                "subtitle": "Collections Framework, Concurrency & Modern Streams API",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "code",
                "badge_color": "primary",
                "level": "Advanced Level",
                "topics_covered": ["Java Collections (ArrayList, HashMap, PriorityQueue)", "Exception Handling & Robust Architecture", "Multithreading, Concurrency & ExecutorService", "Java 8+ Streams API, Lambdas & JDBC"],
                "courses": [
                    {"id": "java-201", "name": "Java Collections Deep Dive & HashMap Internals", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-202", "name": "Multithreading, Locks & Thread Safety", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-203", "name": "Java 8+ Streams & Functional Programming", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-204", "name": "JDBC, SQL Queries & Database Transactions", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "coding-assessment.html?lang=java",
                "action_text": "Core Java Coding Lab",
            },
            {
                "id": "phase-3",
                "phase_num": 3,
                "name": "Phase 3: Advanced & Projects",
                "subtitle": "Build production enterprise applications with Spring Boot",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "briefcase",
                "badge_color": "warning",
                "level": "Practical Projects",
                "topics_covered": ["Spring Boot 3 RESTful Microservices", "Spring Data JPA & Hibernate ORM", "Distributed Caching with Redis", "High-Throughput Kafka Event Pipelines"],
                "courses": [
                    {"id": "java-301", "name": "Spring Boot RESTful Microservice Architecture", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-302", "name": "High-Throughput Kafka Message Pipeline", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-303", "name": "Distributed In-Memory Cache with Redis", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-304", "name": "Full-Stack AI Recruitment Portal in Java", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "coding-assessment.html?mode=projects&lang=java",
                "action_text": "Build Java Projects",
            },
            {
                "id": "phase-4",
                "phase_num": 4,
                "name": "Phase 4: Placement Ready",
                "subtitle": "Company Java technical interview questions & AI mock interviews",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "trophy",
                "badge_color": "info",
                "level": "Placement Ready",
                "topics_covered": ["Top 50 Java Technical Interview Q&A (TCS, Infosys, Amazon)", "Java Concurrency & JVM Tuning Scenarios", "Speed Quantitative & Reasoning Drills", "Live AI Java Technical Mock Interview"],
                "courses": [
                    {"id": "java-401", "name": "Top 12 Company Java Technical Interview Questions", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-402", "name": "AI Proctored Live Java Mock Interview Simulator", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-403", "name": "HR Behavioral & STAR Scenario Practice", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "java-404", "name": "Company Speed Aptitude & Reasoning Drills", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "interview.html?track=java",
                "action_text": "Take Java Mock Interview",
            },
        ],
        "recommendations": [
            {
                "id": "rec-j1",
                "title": "Java Masterclass: Core to OOP",
                "provider": "Curriculum • Beginner",
                "icon": "graduation-cap",
                "type": "course",
                "category": "Beginner Level Course",
                "progress_percent": 0.0,
                "action_url": "study-materials.html?subject=java",
                "description": "Master Java variables, JVM memory model, heap vs stack, and object-oriented principles.",
                "stage": "Phase 1: Foundations",
            },
            {
                "id": "rec-j2",
                "title": "Spring Boot RESTful Microservice",
                "provider": "Project • Intermediate",
                "icon": "code",
                "type": "project",
                "category": "Practical Project",
                "progress_percent": 0.0,
                "action_url": "coding-assessment.html?mode=project&lang=java",
                "description": "Build an end-to-end e-commerce order management microservice with PostgreSQL and JWT auth.",
                "stage": "Phase 3: Projects",
            },
            {
                "id": "rec-j3",
                "title": "Java Collections & Concurrency",
                "provider": "Course • Important",
                "icon": "zap",
                "type": "core",
                "category": "Placement Essential",
                "progress_percent": 0.0,
                "action_url": "study-materials.html?subject=java",
                "description": "HashMap internal hashing, LinkedList, PriorityQueue, ReentrantLocks, and thread synchronization.",
                "stage": "Phase 2: Core Skills",
            },
            {
                "id": "rec-j4",
                "title": "Java Low-Level System Design",
                "provider": "Course • Advanced",
                "icon": "cpu",
                "type": "advanced",
                "category": "Advanced Level",
                "progress_percent": 0.0,
                "action_url": "study-materials.html?subject=java",
                "description": "Design patterns (Factory, Singleton, Observer, Strategy) and scalable enterprise architecture.",
                "stage": "Phase 2: Core Skills",
            },
        ],
        "today_plan": [
            {
                "id": "task-j1",
                "title": "Watch: JVM Memory Architecture (Heap vs Stack)",
                "duration": "30 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "watch",
                "subject": "Java Core",
                "action_url": "study-materials.html?subject=java",
            },
            {
                "id": "task-j2",
                "title": "Practice: Java Arrays & Two-Pointer Mechanics",
                "duration": "45 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "practice",
                "subject": "Java Coding",
                "action_url": "coding-assessment.html?lang=java",
            },
            {
                "id": "task-j3",
                "title": "Read: OOP Principles & Encapsulation in Java",
                "duration": "20 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "read",
                "subject": "Java OOP",
                "action_url": "study-materials.html?subject=java",
            },
        ],
        "focus_areas": ["Java OOP", "Collections Framework", "Spring Boot", "JVM Concurrency"],
        "practical_exercises": [
            {
                "id": "java-ex-1",
                "title": "Reverse an Array & Two-Pointer Mechanics",
                "difficulty": "Easy | TCS, Infosys, Wipro",
                "phase": 1,
                "description": "Write a Java method to reverse an integer array in-place with O(1) auxiliary space using two pointers.",
                "starter_code": "public class Solution {\n    public static void reverseArray(int[] arr) {\n        int left = 0, right = arr.length - 1;\n        while (left < right) {\n            int temp = arr[left];\n            arr[left++] = arr[right];\n            arr[right--] = temp;\n        }\n    }\n}",
                "expected_time": "15 mins",
                "action_url": "coding-assessment.html?lang=java&problem=reverse-array",
            },
            {
                "id": "java-ex-2",
                "title": "Encapsulation & Banking Account System",
                "difficulty": "Medium | Cognizant, Accenture, Capgemini",
                "phase": 1,
                "description": "Design an OOP BankAccount class enforcing balance validation, transaction logs, and immutable account numbers.",
                "starter_code": "public class BankAccount {\n    private final String accountNumber;\n    private double balance;\n    public BankAccount(String accNo, double initBalance) {\n        this.accountNumber = accNo;\n        this.balance = Math.max(0.0, initBalance);\n    }\n    public synchronized void deposit(double amount) {\n        if (amount > 0) balance += amount;\n    }\n}",
                "expected_time": "25 mins",
                "action_url": "coding-assessment.html?lang=java&problem=banking-oop",
            },
            {
                "id": "java-ex-3",
                "title": "Implement LRU Cache using LinkedHashMap",
                "difficulty": "Hard | Amazon, Microsoft, Goldman Sachs",
                "phase": 2,
                "description": "Design an LRU Cache supporting O(1) get and put operations by subclassing Java LinkedHashMap with removeEldestEntry.",
                "starter_code": "import java.util.*;\n\npublic class LRUCache<K, V> extends LinkedHashMap<K, V> {\n    private final int capacity;\n    public LRUCache(int cap) {\n        super(cap, 0.75f, true);\n        this.capacity = cap;\n    }\n    @Override\n    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {\n        return size() > capacity;\n    }\n}",
                "expected_time": "35 mins",
                "action_url": "coding-assessment.html?lang=java&problem=lru-cache",
            },
            {
                "id": "java-ex-4",
                "title": "Thread-Safe Producer-Consumer with BlockingQueue",
                "difficulty": "Hard | Amazon, Oracle, Deloitte",
                "phase": 2,
                "description": "Implement a multi-threaded Producer-Consumer pipeline in Java using java.util.concurrent.ArrayBlockingQueue with graceful shutdown.",
                "starter_code": "import java.util.concurrent.*;\n\npublic class ProducerConsumerDemo {\n    public static void main(String[] args) throws InterruptedException {\n        BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(10);\n        // Implement producer and consumer worker runnables\n    }\n}",
                "expected_time": "30 mins",
                "action_url": "coding-assessment.html?lang=java&problem=producer-consumer",
            },
            {
                "id": "java-ex-5",
                "title": "Java Streams API: Employee Data Aggregation",
                "difficulty": "Medium | TCS Digital, Infosys SP",
                "phase": 2,
                "description": "Use Java 8 Streams to filter employees by department, group by designation, and calculate average salary without imperative loops.",
                "starter_code": "import java.util.*;\nimport java.util.stream.*;\n\npublic class StreamAnalytics {\n    public static Map<String, Double> averageSalaryByDept(List<Employee> list) {\n        return list.stream()\n            .collect(Collectors.groupingBy(Employee::getDepartment,\n                     Collectors.averagingDouble(Employee::getSalary)));\n    }\n}",
                "expected_time": "20 mins",
                "action_url": "coding-assessment.html?lang=java&problem=streams-aggregation",
            },
        ],
        "real_world_projects": [
            {
                "id": "proj-java-1",
                "title": "Spring Boot E-Commerce REST API & Payment Gateway",
                "difficulty": "Production Microservice",
                "phase": 3,
                "badge": "Portfolio Essential",
                "tech_stack": ["Java 17/21", "Spring Boot 3", "PostgreSQL", "Hibernate JPA", "Stripe API", "Docker"],
                "description": "Construct a full-featured e-commerce backend microservice with product catalogs, shopping cart sessions, inventory reservation, and payment processing.",
                "architecture": "3-Tier Controller-Service-Repository architecture with Spring Security, JWT stateless tokens, and transaction management.",
                "key_features": [
                    "Stateless JWT Authentication & Role-Based Access Control (Admin vs Customer)",
                    "Optimistic locking on inventory quantities to prevent overselling race conditions",
                    "Idempotent payment webhook handling and automated invoice generation",
                    "Swagger / OpenAPI 3.0 interactive documentation & JUnit 5 / Mockito unit tests",
                ],
                "action_url": "study-materials.html?project=spring-ecommerce",
            },
            {
                "id": "proj-java-2",
                "title": "High-Throughput Kafka Event Notification Engine",
                "difficulty": "Distributed System",
                "phase": 3,
                "badge": "Advanced Enterprise",
                "tech_stack": ["Spring Boot 3", "Apache Kafka", "Docker", "PostgreSQL", "Java Concurrency"],
                "description": "Build an asynchronous event-driven notification hub processing 10,000+ placement alerts, interview schedules, and transactional emails per minute.",
                "architecture": "Producer-Consumer message broker architecture with Kafka consumer groups, dead-letter topics (DLQ), and retry exponential backoff.",
                "key_features": [
                    "Partition-keyed event streaming guaranteeing ordered delivery for candidate updates",
                    "Dead Letter Queue (DLQ) pattern for handling corrupted or malformed payloads",
                    "Consumer group scaling across containerized workers",
                    "Prometheus & Micrometer metrics instrumentation for throughput monitoring",
                ],
                "action_url": "study-materials.html?project=kafka-notification",
            },
            {
                "id": "proj-java-3",
                "title": "Distributed In-Memory Cache with Spring Cache & Redis",
                "difficulty": "System Design",
                "phase": 3,
                "badge": "High Concurrency",
                "tech_stack": ["Java 21", "Spring Data Redis", "Cache-Aside Pattern", "Jedis/Lettuce"],
                "description": "Design a high-performance distributed caching layer reducing database latency from 80ms to <2ms for high-frequency hiring catalog queries.",
                "architecture": "Cache-Aside pattern with TTL expiration, cache invalidation listeners, and multi-tier local Caffeine + distributed Redis cache.",
                "key_features": [
                    "Cache stampede mitigation using distributed Redis locks",
                    "Automated cache invalidation on database mutations via Spring Events",
                    "Serializing JSON with Jackson JavaTimeModule and custom polymorphic type validators",
                ],
                "action_url": "study-materials.html?project=redis-cache",
            },
            {
                "id": "proj-java-4",
                "title": "AI-Powered Proctored Recruitment & Candidate Evaluation API",
                "difficulty": "Full-Stack AI Project",
                "phase": 3,
                "badge": "Placement Capstone",
                "tech_stack": ["Spring Boot", "OpenAI / Gemini LLM API", "PostgreSQL", "WebSocket", "WebRTC"],
                "description": "Develop the backend for an AI proctored interview platform evaluating audio transcripts, coding submissions, and applicant fit scores.",
                "architecture": "REST & WebSocket gateway communicating with LLM inference endpoints and recording proctoring violation timestamps.",
                "key_features": [
                    "Real-time WebSocket streaming for question-by-question candidate interview answers",
                    "Automated prompt-engineered evaluation rubric scoring clarity, correctness, and confidence",
                    "Exportable PDF candidate evaluation report generated server-side",
                ],
                "action_url": "interview.html",
            },
        ],
        "placement_training": {
            "title": "Campus Placement Training & Job Readiness",
            "target_companies": ["TCS NQT", "Infosys InfyTQ / SP", "Cognizant GenC Next", "Accenture", "Amazon SDE-1", "Capgemini", "Wipro Turbo"],
            "top_interview_questions": [
                {
                    "q": "Why is String immutable in Java, and what is String Constant Pool?",
                    "company": "TCS & Infosys SP",
                    "a": "Strings are immutable for security (network connections/database credentials), caching in String Constant Pool (saving heap memory), synchronization (thread-safe without locks), and HashCode caching in HashMaps.",
                },
                {
                    "q": "How does HashMap work internally in Java 8?",
                    "company": "Amazon & Capgemini",
                    "a": "HashMap uses an array of Node buckets. Keys are hashed with hashCode() and indexed via hash & (n-1). When collisions occur, entries form a linked list. In Java 8, if bucket length exceeds TREEIFY_THRESHOLD (8) and capacity >= 64, the list converts into a balanced Red-Black Tree (TreeNode) reducing search time from O(n) to O(log n).",
                },
                {
                    "q": "Difference between volatile and synchronized in Java multithreading?",
                    "company": "Cognizant & Goldman Sachs",
                    "a": "volatile ensures variable visibility across threads by reading and writing directly to main memory (preventing CPU thread cache staleness) and prevents instruction reordering. synchronized provides both visibility and mutual exclusion (atomicity) by acquiring an object monitor lock.",
                },
                {
                    "q": "What is the difference between fail-fast and fail-safe iterators?",
                    "company": "Accenture & Wipro",
                    "a": "Fail-fast iterators (e.g. ArrayList, HashMap) operate directly on collection memory and throw ConcurrentModificationException if modified structurally while iterating via the modCount flag. Fail-safe iterators (e.g. CopyOnWriteArrayList, ConcurrentHashMap) operate on a clone or snapshot without throwing exceptions.",
                },
                {
                    "q": "What are Java 8 Functional Interfaces and Default Methods in interfaces?",
                    "company": "TCS Digital & Amazon",
                    "a": "A Functional Interface has exactly one abstract method (annotated with @FunctionalInterface), e.g., Predicate, Function, Consumer, Supplier. Default methods allow adding new method implementations to interfaces without breaking existing implementing classes, enabling backward compatibility.",
                },
            ],
            "speed_aptitude_drills": [
                {"title": "Quantitative Aptitude for Java Developers", "topics": "Permutations, Time & Work, Speed & Distance", "questions_count": 25, "action_url": "study-materials.html?topic=aptitude"},
                {"title": "Logical Reasoning & Coding Deduction", "topics": "Data Sufficiency, Syllogisms, Code Debugging", "questions_count": 20, "action_url": "study-materials.html?topic=reasoning"},
            ],
            "mock_interview_action": {
                "title": "Start AI Proctored Java Mock Interview",
                "description": "Simulate a live 30-minute technical campus placement round with AI voice feedback, coding questions, and performance scorecards.",
                "action_url": "interview.html?track=java",
                "button_text": "Launch Java Mock Interview →",
            },
        },
    },
    "python": {
        "id": "python",
        "name": "Python Full-Stack",
        "title": "Python Programming: Beginner to Placement Ready",
        "icon": "🐍",
        "badge": "AI & Fast-Track",
        "target_role": "Python Backend Engineer / AI Developer",
        "description": "Complete Python journey from fundamental syntax and data structures to FastAPI microservices, asynchronous programming, AI agent architecture, and technical interviews.",
        "phases": [
            {
                "id": "phase-1",
                "phase_num": 1,
                "name": "Phase 1: Foundations",
                "subtitle": "Master Python syntax, memory model & functional basics",
                "progress_percent": 0.0,
                "status": "In Progress",
                "is_locked": False,
                "icon": "layers",
                "badge_color": "success",
                "level": "Beginner Level",
                "topics_covered": ["Python Syntax, Dynamic Typing & Memory", "List Comprehensions & Dictionaries", "Functions, Closures & Decorators", "Object-Oriented Python (Dunder Methods)"],
                "courses": [
                    {"id": "py-101", "name": "Python Syntax, Data Types & Scope", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "py-102", "name": "List Comprehensions, Tuples & Sets", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "py-103", "name": "Functions, Lambda & Decorators", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "py-104", "name": "Object-Oriented Python & Magic Methods", "progress_percent": 0.0, "status": "Not Started"},
                ],
                "action_url": "study-materials.html?subject=python",
                "action_text": "Study Python Foundations",
            },
            {
                "id": "phase-2",
                "phase_num": 2,
                "name": "Phase 2: Core Skills",
                "subtitle": "Advanced Data Structures, Asyncio & FastAPI",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "code",
                "badge_color": "primary",
                "level": "Advanced Level",
                "topics_covered": ["Python Generators & Memory Profiling", "Asyncio & High-Concurrency I/O", "FastAPI & Pydantic REST APIs", "SQLAlchemy ORM & Database Indexing"],
                "courses": [
                    {"id": "py-201", "name": "Advanced Python Data Structures & Algorithmic Patterns", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-202", "name": "Asynchronous Programming with Asyncio", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-203", "name": "FastAPI Production REST Architectures", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-204", "name": "PostgreSQL & SQLAlchemy Asynchronous Session", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "coding-assessment.html?lang=python",
                "action_text": "Core Python Lab",
            },
            {
                "id": "phase-3",
                "phase_num": 3,
                "name": "Phase 3: Advanced & Projects",
                "subtitle": "Build production AI agents and distributed backends",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "briefcase",
                "badge_color": "warning",
                "level": "Practical Projects",
                "topics_covered": ["Build a Chatbot with LLM (RAG)", "High-Throughput Celery Redis Pipeline", "Real-Time WebSocket Analytics Engine", "Autonomous AI Agent Workflow"],
                "courses": [
                    {"id": "py-301", "name": "Production RAG Chatbot with Vector DB", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-302", "name": "Celery & Redis Distributed Task Queue", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-303", "name": "FastAPI WebSockets High-Frequency Engine", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-304", "name": "Autonomous Multi-Agent Recruitment Pipeline", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "coding-assessment.html?mode=projects&lang=python",
                "action_text": "Build Python Projects",
            },
            {
                "id": "phase-4",
                "phase_num": 4,
                "name": "Phase 4: Placement Ready",
                "subtitle": "Python company interview rounds & mock assessments",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "trophy",
                "badge_color": "info",
                "level": "Placement Ready",
                "topics_covered": ["Top Python Coding & Technical Interview Qs", "AI Proctored Live Mock Interview", "Speed Aptitude Placement Drills", "System Design & HR Interview Practice"],
                "courses": [
                    {"id": "py-401", "name": "Top Python Interview Questions & Pitfalls", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-402", "name": "AI Proctored Live Python Mock Interview", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-403", "name": "HR STAR Behavioral Scenarios", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "py-404", "name": "Speed Aptitude Drills for Python Developers", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "interview.html?track=python",
                "action_text": "Take Python Mock Interview",
            },
        ],
        "recommendations": [
            {
                "id": "rec-p1",
                "title": "Python Architecture & Clean Code",
                "provider": "Curriculum • Beginner",
                "icon": "graduation-cap",
                "type": "course",
                "category": "Beginner Level Course",
                "progress_percent": 0.0,
                "action_url": "study-materials.html?subject=python",
                "description": "Master memory references, mutability, closures, and object-oriented Python design.",
                "stage": "Phase 1: Foundations",
            },
            {
                "id": "rec-p2",
                "title": "Build a Chatbot with LLM (RAG)",
                "provider": "Project • Intermediate",
                "icon": "code",
                "type": "project",
                "category": "Practical Project",
                "progress_percent": 0.0,
                "action_url": "coding-assessment.html?mode=project&lang=python",
                "description": "Build an enterprise document assistant with LangChain, ChromaDB, and OpenAI APIs.",
                "stage": "Phase 3: Projects",
            },
            {
                "id": "rec-p3",
                "title": "Asyncio & FastAPI Microservices",
                "provider": "Course • Important",
                "icon": "zap",
                "type": "core",
                "category": "Placement Essential",
                "progress_percent": 0.0,
                "action_url": "study-materials.html?subject=python",
                "description": "Event loops, coroutines, non-blocking network calls, and high-performance APIs.",
                "stage": "Phase 2: Core Skills",
            },
            {
                "id": "rec-p4",
                "title": "Python Low-Level Design & Concurrency",
                "provider": "Course • Advanced",
                "icon": "cpu",
                "type": "advanced",
                "category": "Advanced Level",
                "progress_percent": 0.0,
                "action_url": "study-materials.html?subject=python",
                "description": "Global Interpreter Lock (GIL), multiprocessing, threading, and distributed caching.",
                "stage": "Phase 2: Core Skills",
            },
        ],
        "today_plan": [
            {
                "id": "task-p1",
                "title": "Watch: Python Memory Allocation & Reference Counting",
                "duration": "30 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "watch",
                "subject": "Python Core",
                "action_url": "study-materials.html?subject=python",
            },
            {
                "id": "task-p2",
                "title": "Practice: Dictionary & Two-Sum in Python",
                "duration": "45 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "practice",
                "subject": "Python Coding",
                "action_url": "coding-assessment.html?lang=python",
            },
            {
                "id": "task-p3",
                "title": "Read: Python Decorators & Generator Pipelines",
                "duration": "20 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "read",
                "subject": "Python Advanced",
                "action_url": "study-materials.html?subject=python",
            },
        ],
        "focus_areas": ["Python OOP", "FastAPI", "Asyncio", "Data Structures"],
    },
    "dsa": {
        "id": "dsa",
        "name": "DSA Placement Mastery",
        "title": "Data Structures & Algorithms: Campus Placement Mastery",
        "icon": "⚡",
        "badge": "Placement Essential",
        "target_role": "Core Software Development Engineer (SDE-1)",
        "description": "Intensive 90-day DSA bootcamp covering all placement patterns: Sliding Window, Two Pointers, Trees, Graphs, Dynamic Programming, and company coding assessments.",
        "phases": [
            {
                "id": "phase-1",
                "phase_num": 1,
                "name": "Phase 1: Foundations",
                "subtitle": "Arrays, Strings, Two Pointers & Big-O Analysis",
                "progress_percent": 0.0,
                "status": "In Progress",
                "is_locked": False,
                "icon": "layers",
                "badge_color": "success",
                "level": "Beginner Level",
                "topics_covered": ["Time & Space Complexity (Big-O)", "Arrays, Sliding Window & Two Pointers", "String Pattern Matching & Hashing", "Basic Recursion & Backtracking"],
                "courses": [
                    {"id": "dsa-101", "name": "Asymptotic Complexity & Math Basics", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "dsa-102", "name": "Two-Pointer & Sliding Window Techniques", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "dsa-103", "name": "String Manipulations & Hashing", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "dsa-104", "name": "Recursion Trees & Mathematical Induction", "progress_percent": 0.0, "status": "Not Started"},
                ],
                "action_url": "coding-assessment.html?category=dsa",
                "action_text": "Study DSA Foundations",
            },
            {
                "id": "phase-2",
                "phase_num": 2,
                "name": "Phase 2: Core Skills",
                "subtitle": "Linked Lists, Stacks, Queues, Binary Trees & BSTs",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "code",
                "badge_color": "primary",
                "level": "Advanced Level",
                "topics_covered": ["Linked Lists (Fast & Slow Pointers)", "Monotonic Stacks & Queues", "Binary Trees (Traversals & LCA)", "Binary Search Trees & Heaps"],
                "courses": [
                    {"id": "dsa-201", "name": "Linked List Cycle Detection & Reversals", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-202", "name": "Monotonic Stack Problems (Next Greater Element)", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-203", "name": "Binary Tree DFS/BFS & Lowest Common Ancestor", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-204", "name": "Priority Queues & Top-K Elements Pattern", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "coding-assessment.html?category=dsa",
                "action_text": "Core DSA Lab",
            },
            {
                "id": "phase-3",
                "phase_num": 3,
                "name": "Phase 3: Advanced & Projects",
                "subtitle": "Graphs, Dynamic Programming & Trie Structures",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "briefcase",
                "badge_color": "warning",
                "level": "Practical Projects",
                "topics_covered": ["Graph Algorithms (BFS/DFS, Dijkstra, Topological Sort)", "Dynamic Programming (1D & 2D Knapsack)", "Disjoint Set Union (DSU) & Minimum Spanning Tree", "Trie Data Structures & Autocomplete System"],
                "courses": [
                    {"id": "dsa-301", "name": "Graph BFS/DFS & Shortest Path Dijkstra", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-302", "name": "1D & 2D Dynamic Programming Patterns", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-303", "name": "Disjoint Set Union & Kruskal Algorithm", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-304", "name": "Design Autocomplete System using Trie", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "coding-assessment.html?mode=projects&category=dsa",
                "action_text": "Build DSA Systems",
            },
            {
                "id": "phase-4",
                "phase_num": 4,
                "name": "Phase 4: Placement Ready",
                "subtitle": "Company LeetCode patterns & live coding mock rounds",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "trophy",
                "badge_color": "info",
                "level": "Placement Ready",
                "topics_covered": ["Amazon, Google & Microsoft SDE Coding Rounds", "Timed Speed Coding Assessments", "Company Technical Problem Solving", "System Design & Low-Level Architecture"],
                "courses": [
                    {"id": "dsa-401", "name": "Top 50 SDE LeetCode Medium/Hard Patterns", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-402", "name": "AI Proctored Live Coding Interview Simulator", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-403", "name": "Behavioral & Communication in Tech Rounds", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "dsa-404", "name": "Speed Aptitude Placement Drills", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "interview.html?track=dsa",
                "action_text": "Take Coding Interview",
            },
        ],
        "recommendations": [
            {
                "id": "rec-d1",
                "title": "Sliding Window & Two Pointer Masterclass",
                "provider": "Curriculum • Important",
                "icon": "zap",
                "type": "core",
                "category": "Placement Essential",
                "progress_percent": 0.0,
                "action_url": "coding-assessment.html",
                "description": "Master subarray problems, longest substrings, and maximum sum windows.",
                "stage": "Phase 1: Foundations",
            },
            {
                "id": "rec-d2",
                "title": "Binary Tree & Graph Mastery",
                "provider": "Curriculum • Advanced",
                "icon": "code",
                "type": "core",
                "category": "Advanced Level",
                "progress_percent": 0.0,
                "action_url": "coding-assessment.html",
                "description": "Recursive traversals, tree paths, cycle detection, and topological sorting.",
                "stage": "Phase 2: Core Skills",
            },
            {
                "id": "rec-d3",
                "title": "Dynamic Programming Master Patterns",
                "provider": "Curriculum • Advanced",
                "icon": "cpu",
                "type": "advanced",
                "category": "Advanced Level",
                "progress_percent": 0.0,
                "action_url": "coding-assessment.html",
                "description": "0/1 Knapsack, Longest Common Subsequence, and Coin Change state transitions.",
                "stage": "Phase 3: Projects",
            },
            {
                "id": "rec-d4",
                "title": "Design a Distributed Trie Autocomplete",
                "provider": "Project • Intermediate",
                "icon": "briefcase",
                "type": "project",
                "category": "Practical Project",
                "progress_percent": 0.0,
                "action_url": "coding-assessment.html?mode=project",
                "description": "Construct high-performance prefix search with frequency weighting in O(k) time.",
                "stage": "Phase 3: Projects",
            },
        ],
        "today_plan": [
            {
                "id": "task-d1",
                "title": "Watch: Sliding Window Technique & Complexity",
                "duration": "30 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "watch",
                "subject": "DSA Foundations",
                "action_url": "study-materials.html?topic=dsa",
            },
            {
                "id": "task-d2",
                "title": "Practice: Longest Substring Without Repeating Characters",
                "duration": "45 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "practice",
                "subject": "DSA Coding",
                "action_url": "coding-assessment.html?problem=longest-substring",
            },
            {
                "id": "task-d3",
                "title": "Read: Monotonic Stack Mechanics & Next Greater Element",
                "duration": "20 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "read",
                "subject": "DSA Theory",
                "action_url": "study-materials.html?topic=dsa",
            },
        ],
        "focus_areas": ["Dynamic Programming", "Graphs", "Trees", "Sliding Window"],
    },
    "web_dev": {
        "id": "web_dev",
        "name": "Full-Stack Web Dev",
        "title": "Full-Stack Web Development: React, Node.js & Cloud",
        "icon": "🌐",
        "badge": "High Demand",
        "target_role": "Full-Stack Software Engineer / Frontend Engineer",
        "description": "Comprehensive web development track covering modern JavaScript (ES6+), React.js, Node.js/Express REST APIs, WebSockets, PostgreSQL, and scalable deployments.",
        "phases": [
            {
                "id": "phase-1",
                "phase_num": 1,
                "name": "Phase 1: Foundations",
                "subtitle": "HTML5, Modern CSS, ES6+ JavaScript & DOM APIs",
                "progress_percent": 0.0,
                "status": "In Progress",
                "is_locked": False,
                "icon": "layers",
                "badge_color": "success",
                "level": "Beginner Level",
                "topics_covered": ["Semantic HTML5 & Responsive CSS3 Flexbox/Grid", "Modern JavaScript (Promises, Async/Await, Closures)", "DOM Manipulation & Event Propagation", "REST API Consumption with Fetch"],
                "courses": [
                    {"id": "web-101", "name": "Semantic HTML5 & Modern Responsive CSS", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "web-102", "name": "ES6+ JavaScript Mechanics & Event Loop", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "web-103", "name": "DOM Event Bubbling & Dynamic Rendering", "progress_percent": 0.0, "status": "Not Started"},
                    {"id": "web-104", "name": "REST API Integration & Async/Await", "progress_percent": 0.0, "status": "Not Started"},
                ],
                "action_url": "study-materials.html?subject=javascript",
                "action_text": "Study Web Foundations",
            },
            {
                "id": "phase-2",
                "phase_num": 2,
                "name": "Phase 2: Core Skills",
                "subtitle": "TypeScript, React.js Hooks, Node.js & Express",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "code",
                "badge_color": "primary",
                "level": "Advanced Level",
                "topics_covered": ["TypeScript Type Systems & Generics", "React.js State, Hooks (useMemo, useCallback)", "Node.js Architecture & Express REST APIs", "JWT Authentication & Secure Cookies"],
                "courses": [
                    {"id": "web-201", "name": "TypeScript Deep Dive for Enterprise Web", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-202", "name": "React Component Architecture & Custom Hooks", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-203", "name": "Node.js Non-Blocking I/O & Express Gateway", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-204", "name": "Database Modeling with Prisma & PostgreSQL", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "coding-assessment.html?lang=javascript",
                "action_text": "Full-Stack Lab",
            },
            {
                "id": "phase-3",
                "phase_num": 3,
                "name": "Phase 3: Advanced & Projects",
                "subtitle": "Build real-world full-stack SaaS & collaboration apps",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "briefcase",
                "badge_color": "warning",
                "level": "Practical Projects",
                "topics_covered": ["Real-Time Collaborative Whiteboard (WebSockets)", "AI-Powered SaaS Dashboard with Next.js", "Full-Stack Recruitment Portal", "Micro-Frontend Cloud Architecture"],
                "courses": [
                    {"id": "web-301", "name": "Real-Time WebSocket Collaboration System", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-302", "name": "Next.js Full-Stack SaaS with Stripe Billing", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-303", "name": "Docker & CI/CD Cloud Deployment Pipeline", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-304", "name": "Full-Stack AI Recruitment Workspace", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "coding-assessment.html?mode=projects&lang=javascript",
                "action_text": "Build Web Projects",
            },
            {
                "id": "phase-4",
                "phase_num": 4,
                "name": "Phase 4: Placement Ready",
                "subtitle": "Frontend System Design, Web interview rounds & mock tests",
                "progress_percent": 0.0,
                "status": "Upcoming",
                "is_locked": True,
                "icon": "trophy",
                "badge_color": "info",
                "level": "Placement Ready",
                "topics_covered": ["Frontend Performance (Lighthouse, Virtual DOM)", "Full-Stack Technical Interview Questions", "Live AI Technical Mock Interview", "Speed Aptitude & Problem Solving"],
                "courses": [
                    {"id": "web-401", "name": "Top Full-Stack & React Technical Interview Questions", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-402", "name": "AI Proctored Live Mock Interview Simulator", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-403", "name": "HR Behavioral & STAR Scenario Practice", "progress_percent": 0.0, "status": "Upcoming"},
                    {"id": "web-404", "name": "Speed Aptitude Placement Assessments", "progress_percent": 0.0, "status": "Upcoming"},
                ],
                "action_url": "interview.html?track=web_dev",
                "action_text": "Take Web Mock Interview",
            },
        ],
        "recommendations": [
            {
                "id": "rec-w1",
                "title": "React & TypeScript Architecture",
                "provider": "Curriculum • Important",
                "icon": "code",
                "type": "core",
                "category": "Placement Essential",
                "progress_percent": 0.0,
                "action_url": "study-materials.html?subject=javascript",
                "description": "Component lifecycle, memoization, state machines, and type-safe props.",
                "stage": "Phase 2: Core Skills",
            },
            {
                "id": "rec-w2",
                "title": "Full-Stack SaaS Application",
                "provider": "Project • Intermediate",
                "icon": "briefcase",
                "type": "project",
                "category": "Practical Project",
                "progress_percent": 0.0,
                "action_url": "coding-assessment.html?mode=project",
                "description": "Construct multi-tenant application with Next.js, Tailwind, and Prisma ORM.",
                "stage": "Phase 3: Projects",
            },
            {
                "id": "rec-w3",
                "title": "Web Performance & Core Vitals",
                "provider": "Course • Advanced",
                "icon": "zap",
                "type": "advanced",
                "category": "Advanced Level",
                "progress_percent": 0.0,
                "action_url": "study-materials.html",
                "description": "Code splitting, lazy loading, debouncing, and browser rendering critical path.",
                "stage": "Phase 2: Core Skills",
            },
            {
                "id": "rec-w4",
                "title": "Frontend System Design",
                "provider": "Course • Advanced",
                "icon": "cpu",
                "type": "advanced",
                "category": "Placement Essential",
                "progress_percent": 0.0,
                "action_url": "study-materials.html",
                "description": "Design an infinite scroll feed, notification tray, and client-side caching.",
                "stage": "Phase 4: Placement Ready",
            },
        ],
        "today_plan": [
            {
                "id": "task-w1",
                "title": "Watch: JavaScript Event Loop & Microtasks",
                "duration": "30 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "watch",
                "subject": "JS Core",
                "action_url": "study-materials.html?subject=javascript",
            },
            {
                "id": "task-w2",
                "title": "Practice: Debounce & Throttle Implementation",
                "duration": "45 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "practice",
                "subject": "JS Coding",
                "action_url": "coding-assessment.html?lang=javascript",
            },
            {
                "id": "task-w3",
                "title": "Read: React Fiber Architecture & Reconciliation",
                "duration": "20 min",
                "status": "Pending",
                "progress_percent": 0.0,
                "type": "read",
                "subject": "React Deep Dive",
                "action_url": "study-materials.html?subject=javascript",
            },
        ],
        "focus_areas": ["React.js", "TypeScript", "Node.js", "WebSockets"],
    },
}

# Alias default references for backward compatibility
try:
    from app.services.learning_journey_tracks import ADDITIONAL_COURSE_TRACKS
    COURSE_TRACKS.update(ADDITIONAL_COURSE_TRACKS)
except Exception as e:
    logger.warning("Could not load additional learning journey tracks: %s", e)

DEFAULT_PHASES = COURSE_TRACKS["java"]["phases"]
DEFAULT_RECOMMENDATIONS = COURSE_TRACKS["java"]["recommendations"]
DEFAULT_TODAYS_PLAN = COURSE_TRACKS["java"]["today_plan"]

DEFAULT_RECENT_PROGRESS = {
    "courses_completed": 0,
    "courses_delta": "0 completed",
    "projects_built": 0,
    "projects_delta": "0 built",
    "hours_learned": 0.0,
    "hours_delta": "Start today",
    "streak_days": 1,
}

DEFAULT_STRENGTHS = ["Logical Reasoning", "Problem Solving", "Basic Coding"]
DEFAULT_FOCUS_AREAS = ["Java OOP", "Collections Framework", "Spring Boot", "JVM Concurrency"]


def create_course_journey_state(
    course_id: str = "java",
    user_rec: Optional[User] = None,
    cand_prof: Optional[CandidateProfile] = None,
) -> Dict[str, Any]:
    """Generates an independent, completely fresh 0% learning journey state for a chosen course."""
    norm_id = course_id.lower().strip() if course_id else "java"
    track = COURSE_TRACKS.get(norm_id, COURSE_TRACKS["java"])

    phases = copy.deepcopy(track["phases"])
    for p in phases:
        p["date_range"] = ""
        p["progress_percent"] = 0.0
        if p.get("phase_num") == 1:
            p["status"] = "Not Started"
        else:
            p["status"] = "Locked"
            p["is_locked"] = True

    strengths = copy.deepcopy(DEFAULT_STRENGTHS)
    if cand_prof and hasattr(cand_prof, "skills") and cand_prof.skills:
        try:
            if isinstance(cand_prof.skills, str):
                parsed = [s.strip() for s in cand_prof.skills.split(",") if s.strip()]
            elif isinstance(cand_prof.skills, (list, set)):
                parsed = [str(getattr(s, "name", s)) for s in cand_prof.skills]
            else:
                parsed = []
            if parsed:
                strengths = parsed[:3]
        except Exception:
            pass

    return {
        "selected_course": track["id"],
        "phases": phases,
        "recommendations": copy.deepcopy(track["recommendations"]),
        "today_plan": copy.deepcopy(track["today_plan"]),
        "recent_progress": copy.deepcopy(DEFAULT_RECENT_PROGRESS),
        "strengths": strengths,
        "focus_areas": copy.deepcopy(track.get("focus_areas", DEFAULT_FOCUS_AREAS)),
        "completed_topics": [],
        "course_started_at": None,
        "is_started": False,
    }


def create_fresh_journey_state(user_rec: Optional[User] = None, cand_prof: Optional[CandidateProfile] = None) -> Dict[str, Any]:
    return create_course_journey_state("java", user_rec, cand_prof)


def get_candidate_learning_journey(db: Session, user_id: Any) -> Dict[str, Any]:
    """
    Fetches candidate's learning roadmap, course progress percentage, recommendations,
    daily study plan, recent progress, strengths, and focus areas.
    All percentages are dynamically calculated from candidate's actual learning activities.
    Every new candidate account starts strictly fresh with their own independent data.
    """
    user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id
    user_rec = db.query(User).filter(User.id == user_uuid).first()
    cand_prof = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_uuid).first()

    # 1. Fetch or initialize StudentLearningPreference for this specific user
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
    if not pref:
        pref = StudentLearningPreference(
            user_id=user_uuid,
            selected_topics_json=json.dumps(["Java", "Python", "DSA", "SQL"]),
            daily_streak=1,
        )
        db.add(pref)
        db.flush()

    # 2. Parse or initialize journey state
    state = {}
    if pref.journey_state_json:
        try:
            state = json.loads(pref.journey_state_json)
        except Exception:
            state = {}

    selected_course = state.get("selected_course", "java") if state else "java"
    if selected_course not in COURSE_TRACKS:
        selected_course = "java"
    active_track = COURSE_TRACKS[selected_course]

    # Check for legacy mock template injection:
    is_legacy_mock = False
    if state and "phases" in state:
        first_phase = state["phases"][0] if state["phases"] else {}
        if first_phase.get("progress_percent") == 60.0 or state.get("recent_progress", {}).get("hours_learned") == 18.5:
            cand_id = cand_prof.id if cand_prof else None
            has_tests = db.query(CandidateTestAttempt).filter(CandidateTestAttempt.user_id == user_uuid).count() > 0
            has_coding = (cand_id and db.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.candidate_id == cand_id).count() > 0)
            has_interview = (cand_id and db.query(Interview).filter(Interview.candidate_id == cand_id).count() > 0)
            if not has_tests and not has_coding and not has_interview:
                is_legacy_mock = True

    if not state or is_legacy_mock or "phases" not in state or not state["phases"]:
        fresh_state = create_course_journey_state(selected_course, user_rec, cand_prof)
        phases = fresh_state["phases"]
        recommendations = fresh_state["recommendations"]
        today_plan = fresh_state["today_plan"]
        recent_progress = fresh_state["recent_progress"]
        strengths = fresh_state["strengths"]
        focus_areas = fresh_state["focus_areas"]
        completed_topics = fresh_state.get("completed_topics", [])
    else:
        phases = state.get("phases", copy.deepcopy(active_track["phases"]))
        recommendations = state.get("recommendations", copy.deepcopy(active_track["recommendations"]))
        today_plan = state.get("today_plan", copy.deepcopy(active_track["today_plan"]))
        recent_progress = state.get("recent_progress", copy.deepcopy(DEFAULT_RECENT_PROGRESS))
        strengths = state.get("strengths", copy.deepcopy(DEFAULT_STRENGTHS))
        focus_areas = state.get("focus_areas", copy.deepcopy(active_track.get("focus_areas", DEFAULT_FOCUS_AREAS)))
        completed_topics = state.get("completed_topics", [])

    # Validate phase track consistency: Ensure loaded phases match currently selected course
    track_mismatch = False
    if phases and phases[0].get("courses") and phases[0]["courses"]:
        first_c_id = phases[0]["courses"][0].get("id", "")
        if selected_course == "python" and not first_c_id.startswith("py-"):
            track_mismatch = True
        elif selected_course == "java" and not first_c_id.startswith("java-"):
            track_mismatch = True
        elif selected_course == "dsa" and not first_c_id.startswith("dsa-"):
            track_mismatch = True
    elif phases and phases[0].get("subtitle"):
        sub = phases[0]["subtitle"].lower()
        if selected_course == "python" and "java" in sub:
            track_mismatch = True

    if track_mismatch:
        phases = copy.deepcopy(active_track["phases"])
        recommendations = copy.deepcopy(active_track["recommendations"])
        today_plan = copy.deepcopy(active_track["today_plan"])
        focus_areas = copy.deepcopy(active_track.get("focus_areas", DEFAULT_FOCUS_AREAS))

    # 3. Synchronize with candidate's actual assessment history & interview scores
    _sync_live_candidate_performance(
        db, user_uuid, phases, recommendations, today_plan, strengths, focus_areas, recent_progress, completed_topics
    )

    # 4. Enforce strict stage-gate logic
    p1 = phases[0]
    p2 = phases[1]
    p3 = phases[2]
    p4 = phases[3]

    if p1["progress_percent"] >= 100.0:
        p1["status"] = "Completed"
        p1["progress_percent"] = 100.0
        p2["is_locked"] = False
        if p2["status"] == "Upcoming" and p2["progress_percent"] == 0.0:
            p2["status"] = "In Progress"
    else:
        p1["status"] = "In Progress"
        p2["is_locked"] = True
        p2["status"] = "Upcoming"
        p3["is_locked"] = True
        p3["status"] = "Upcoming"
        p4["is_locked"] = True
        p4["status"] = "Upcoming"

    if p2["progress_percent"] >= 100.0:
        p2["status"] = "Completed"
        p2["progress_percent"] = 100.0
        p3["is_locked"] = False
        if p3["status"] == "Upcoming" and p3["progress_percent"] == 0.0:
            p3["status"] = "In Progress"

    if p3["progress_percent"] >= 100.0:
        p3["status"] = "Completed"
        p3["progress_percent"] = 100.0
        p4["is_locked"] = False
        if p4["status"] == "Upcoming" and p4["progress_percent"] == 0.0:
            p4["status"] = "In Progress"

    # 5. Dynamically calculate overall roadmap completion percentage
    total_prog = sum(float(p["progress_percent"]) for p in phases) / len(phases)
    overall_roadmap_pct = round(total_prog, 1)

    # 6. Dynamically calculate recommendations progress percentage
    rec_prog_sum = sum(float(r.get("progress_percent", 0.0)) for r in recommendations)
    recommendations_overall_pct = round(rec_prog_sum / max(1, len(recommendations)), 1)

    # 7. Dynamically calculate daily study plan completion percentage
    task_prog_sum = 0.0
    for t in today_plan:
        if t.get("status") == "Completed":
            t["progress_percent"] = 100.0
            task_prog_sum += 100.0
        elif t.get("status") == "In Progress":
            t["progress_percent"] = 50.0
            task_prog_sum += 50.0
        else:
            t["progress_percent"] = 0.0
            task_prog_sum += 0.0
    today_plan_pct = round(task_prog_sum / max(1, len(today_plan)), 1)

    # Identify currently active phase & guidance
    p1_pct = round(float(p1.get("progress_percent", 0.0)), 1)
    if p1_pct < 100.0:
        active_phase = p1
        tid = active_track.get("id", "").lower()
        if "python" in tid:
            topic_desc = "syntax, dynamic typing, variables, and core data structures"
        elif "dsa" in tid:
            topic_desc = "algorithmic complexity, asymptotic Big-O bounds, and fundamental arrays"
        elif "web" in tid:
            topic_desc = "HTML5, CSS3 layout, DOM manipulation, and modern JavaScript"
        elif "ai" in tid or "machine" in tid:
            topic_desc = "linear algebra, probability, Python numerical libraries, and ML algorithms"
        elif "data" in tid:
            topic_desc = "data manipulation, Pandas, SQL data querying, and exploratory data analysis"
        elif "cloud" in tid or "aws" in tid:
            topic_desc = "cloud architecture models, compute instances, storage, and networking"
        elif "cyber" in tid:
            topic_desc = "network protocols, threat surfaces, encryption, and security essentials"
        elif "devops" in tid:
            topic_desc = "Linux command line, Git workflows, CI/CD pipelines, and containerization"
        elif "sql" in tid:
            topic_desc = "relational schema design, SELECT queries, JOINs, and aggregation functions"
        elif "gen" in tid:
            topic_desc = "prompt engineering, LLM tokenization, embeddings, and API integrations"
        elif "deep" in tid:
            topic_desc = "neural network forward/backpropagation, activation functions, and PyTorch tensors"
        elif "testing" in tid:
            topic_desc = "software test lifecycle, test case design, unit testing, and automation fundamentals"
        else:
            topic_desc = "syntax, variables, JVM memory model, and object-oriented principles"

        if p1_pct == 0.0:
            next_step_action = {
                "title": f"Phase 1: Foundations (0% Completed)",
                "guidance": f"Welcome to {active_track['name']}! Begin with beginner core concepts, {topic_desc} to build strong foundational competence.",
                "target_phase": 1,
                "action_url": f"course-learning.html?course={selected_course}",
                "action_label": "Start Course →",
            }
        else:
            next_step_action = {
                "title": f"Complete Phase 1: Foundations ({int(p1_pct)}% completed)",
                "guidance": f"Keep going! Finish foundational topics and practice drills in {active_track['name']} to unlock Phase 2: Core Skills.",
                "target_phase": 1,
                "action_url": f"course-learning.html?course={selected_course}",
                "action_label": "Continue Learning →",
            }
    elif p2["progress_percent"] < 100.0:
        active_phase = p2
        next_step_action = {
            "title": f"Advance Phase 2: Core Skills ({int(p2['progress_percent'])}% completed)",
            "guidance": f"Foundations cleared! Advance to deep {active_track['name']} core skills, data structures, and multithreading before project development.",
            "target_phase": 2,
            "action_url": p2.get("action_url", "coding-assessment.html"),
            "action_label": "Start Advanced Core Skills →",
        }
    elif p3["progress_percent"] < 100.0:
        active_phase = p3
        next_step_action = {
            "title": f"Build Phase 3: Practical Projects ({int(p3['progress_percent'])}% completed)",
            "guidance": f"Core skills mastered! Now construct real-world production projects in {active_track['name']} to showcase applied engineering competence.",
            "target_phase": 3,
            "action_url": p3.get("action_url", "coding-assessment.html?mode=projects"),
            "action_label": "Build Practical Projects →",
        }
    else:
        active_phase = p4
        next_step_action = {
            "title": f"Phase 4: Placement Ready & Interview Prep ({int(p4['progress_percent'])}% completed)",
            "guidance": f"Projects cleared! You are now qualified for company campus placement drives, technical interview drills, and AI proctored mock interviews.",
            "target_phase": 4,
            "action_url": p4.get("action_url", "interview.html"),
            "action_label": "Start AI Mock Interview →",
        }

    # Format today's date and dynamic 90-day phase timeline anchored to actual course start date
    now = datetime.now()
    formatted_date = now.strftime("%b %d, %Y")

    course_start_dt = None
    is_course_started = bool(state and state.get("is_started"))
    if is_course_started and state.get("course_started_at"):
        try:
            course_start_dt = datetime.fromisoformat(state["course_started_at"])
        except Exception:
            course_start_dt = None

    start_dt = course_start_dt if (is_course_started and course_start_dt) else now
    expected_completion_dt = start_dt + timedelta(days=90)
    days_elapsed = (now - start_dt).days if (is_course_started and course_start_dt) else 0
    days_remaining = max(0, 90 - days_elapsed) if is_course_started else 90
    current_week = min(12, max(1, (days_elapsed // 7) + 1)) if is_course_started else 1

    dynamic_schedules = compute_dynamic_phase_schedules(start_dt)
    for idx, p in enumerate(phases):
        meta = PHASE_SCHEDULE_META[idx] if idx < len(PHASE_SCHEDULE_META) else {}
        p["weekly_schedule"] = meta.get("weekly_schedule", f"Phase {idx+1}")
        p["expected_topics_count"] = meta.get("expected_topics_count", 10)
        p["stage_title"] = meta.get("stage_title", p.get("name", ""))
        p["focus_areas"] = meta.get("focus", "")
        if idx < len(dynamic_schedules):
            p["date_range"] = dynamic_schedules[idx]

    if not is_course_started:
        # Candidate has not started course yet:
        # Phase 1 is Ready to Start, Phases 2-4 are Locked.
        # Overall progress remains 0.0% until they begin learning, but the 12-week schedule,
        # weekly milestones, and expected completion date are clearly visible.
        for p in phases:
            p["progress_percent"] = 0.0
            if p.get("phase_num") == 1:
                p["status"] = "Ready to Start"
                p["is_locked"] = False
                for c in p.get("courses", []):
                    c["status"] = "Ready to Start"
                    c["progress_percent"] = 0.0
            else:
                p["status"] = "Upcoming (Locked)"
                p["is_locked"] = True
                for c in p.get("courses", []):
                    c["status"] = "Locked"
                    c["progress_percent"] = 0.0
        overall_roadmap_pct = 0.0
        recommendations_overall_pct = 0.0
        today_plan_pct = 0.0

    weekly_schedule = build_12_week_schedule(
        selected_course,
        start_dt,
        is_course_started,
        completed_topics,
    )

    schedule_overview = {
        "is_started": is_course_started,
        "status_label": "In Progress" if is_course_started else "Not Started (Ready to Start)",
        "start_date": course_start_dt.strftime("%b %d, %Y") if (is_course_started and course_start_dt) else "Ready Today (Day 1 on Click)",
        "start_date_iso": course_start_dt.isoformat() if (is_course_started and course_start_dt) else None,
        "start_date_human": f"Started on {course_start_dt.strftime('%b %d, %Y')}" if (is_course_started and course_start_dt) else "Starts immediately when you click Start Course",
        "expected_completion_date": expected_completion_dt.strftime("%b %d, %Y"),
        "expected_completion_iso": expected_completion_dt.isoformat(),
        "total_days": 90,
        "total_weeks": 12,
        "days_elapsed": days_elapsed,
        "days_remaining": days_remaining,
        "current_week": current_week,
        "total_topics": 50,
        "completed_topics_count": len(completed_topics) if is_course_started else 0,
        "overall_progress_percent": overall_roadmap_pct if is_course_started else 0.0,
        "target_pace": "4–5 Topics / Week (approx. 1 hour / day)",
    }

    # Available courses list for UI selection dropdown
    available_courses = [
        {
            "id": c_id,
            "name": tr["name"],
            "title": tr["title"],
            "icon": tr["icon"],
            "badge": tr["badge"],
            "target_role": tr["target_role"],
            "description": tr["description"],
            "is_selected": (c_id == selected_course),
        }
        for c_id, tr in COURSE_TRACKS.items()
    ]

    result = {
        "roadmap_title": f"Your 90-Day Roadmap — {active_track['name']}",
        "target_track": active_track["title"],
        "selected_course": selected_course,
        "course_track": {
            "id": active_track["id"],
            "name": active_track["name"],
            "title": active_track["title"],
            "icon": active_track["icon"],
            "badge": active_track["badge"],
            "target_role": active_track["target_role"],
            "description": active_track["description"],
        },
        "available_courses": available_courses,
        "overall_progress_percent": overall_roadmap_pct,
        "active_phase_num": active_phase["phase_num"],
        "active_phase_name": active_phase["name"],
        "phases": phases,
        "schedule_overview": schedule_overview,
        "weekly_schedule": weekly_schedule,
        "expected_completion_date": expected_completion_dt.strftime("%b %d, %Y"),
        "start_date": course_start_dt.strftime("%b %d, %Y") if (is_course_started and course_start_dt) else "Ready Today (Day 1 on Click)",
        "recommendations": recommendations,
        "recommendations_progress_percent": recommendations_overall_pct,
        "today_plan": today_plan,
        "today_plan_progress_percent": today_plan_pct,
        "today_date": formatted_date,
        "recent_progress": recent_progress,
        "strengths": strengths,
        "focus_areas": focus_areas,
        "completed_topics": completed_topics,
        "is_started": is_course_started,
        "course_started_at": course_start_dt.isoformat() if course_start_dt else None,
        "next_step": next_step_action,
        "stage_gate_policy": {
            "rule": "Strict Stage-Gate: Foundations (Beginner) -> Core Skills (Advanced) -> Practical Projects -> Placement Ready (Interviews & Tests)",
            "phase_1_unlocked": True,
            "phase_2_unlocked": not p2["is_locked"],
            "phase_3_unlocked": not p3["is_locked"],
            "phase_4_unlocked": not p4["is_locked"],
        },
        "practical_exercises": active_track.get("practical_exercises", []),
        "real_world_projects": active_track.get("real_world_projects", []),
        "placement_training": active_track.get("placement_training", {}),
    }

    # Save state back
    state["selected_course"] = selected_course
    state["phases"] = phases
    state["recommendations"] = recommendations
    state["today_plan"] = today_plan
    state["recent_progress"] = recent_progress
    state["strengths"] = strengths
    state["focus_areas"] = focus_areas
    state["completed_topics"] = completed_topics
    state["is_started"] = is_course_started
    state["course_started_at"] = course_start_dt.isoformat() if course_start_dt else None
    pref.journey_state_json = json.dumps(state)
    try:
        db.commit()
    except Exception:
        db.rollback()

    return result


def select_candidate_course(db: Session, user_id: Any, course_id: str) -> Dict[str, Any]:
    """Switches the candidate's active learning track to the chosen course (e.g. Java, Python, DSA)."""
    user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
    if not pref:
        pref = StudentLearningPreference(user_id=user_uuid, daily_streak=1)
        db.add(pref)
        db.flush()

    norm_id = course_id.lower().strip() if course_id else "java"
    if norm_id not in COURSE_TRACKS:
        norm_id = "java"

    user_rec = db.query(User).filter(User.id == user_uuid).first()
    cand_prof = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_uuid).first()

    # Create fresh state for this chosen course
    state = create_course_journey_state(norm_id, user_rec, cand_prof)
    pref.journey_state_json = json.dumps(state)
    db.commit()

    return get_candidate_learning_journey(db, user_uuid)


def start_course_journey(db: Session, user_id: Any, course_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Activates and begins the chosen course track for the student, advancing initial progress
    from 0% and marking Phase 1: Foundations as active 'In Progress', so the student can
    immediately learn topics step by step.
    """
    user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
    if not pref:
        get_candidate_learning_journey(db, user_uuid)
        pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()

    state = json.loads(pref.journey_state_json) if pref.journey_state_json else {}

    # If course_id is passed, ensure it is selected
    if course_id:
        norm_id = course_id.lower().strip() if course_id else "java"
        if norm_id not in COURSE_TRACKS:
            norm_id = "java"
        if state.get("selected_course") != norm_id:
            select_candidate_course(db, user_uuid, norm_id)
            pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
            state = json.loads(pref.journey_state_json) if pref.journey_state_json else {}

    phases = state.get("phases", [])
    if phases:
        p1 = phases[0]
        p1["status"] = "In Progress"
        for c in p1.get("courses", []):
            if c.get("status") == "Not Started":
                c["status"] = "In Progress"

    now = datetime.now()
    state["is_started"] = True
    state["course_started_at"] = now.isoformat()
    dynamic_schedules = compute_dynamic_phase_schedules(now)
    for idx, p in enumerate(phases):
        if idx < len(dynamic_schedules):
            p["date_range"] = dynamic_schedules[idx]
    state["phases"] = phases
    pref.journey_state_json = json.dumps(state)
    db.commit()

    return get_candidate_learning_journey(db, user_uuid)


def complete_course_topic(db: Session, user_id: Any, topic_id: str, phase_num: int = 1) -> Dict[str, Any]:
    """
    Marks a specific course topic or exercise as completed, dynamically advancing
    the phase and overall roadmap progress percentage.
    """
    user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
    if not pref:
        get_candidate_learning_journey(db, user_uuid)
        pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()

    state = json.loads(pref.journey_state_json) if pref.journey_state_json else {}
    completed = set(state.get("completed_topics", []))

    is_already_done = topic_id in completed
    if is_already_done:
        completed.remove(topic_id)
        delta_pct = -25.0
        delta_hours = -0.5
    else:
        completed.add(topic_id)
        delta_pct = 25.0
        delta_hours = 0.5

    state["completed_topics"] = list(completed)

    # Find the target phase and advance its progress
    phases = state.get("phases", [])
    for p in phases:
        if p.get("phase_num") == phase_num:
            cur_pct = p.get("progress_percent", 0.0)
            p["progress_percent"] = max(0.0, min(100.0, round(cur_pct + delta_pct, 1)))
            if p["progress_percent"] >= 100.0:
                p["status"] = "Completed"
                # unlock next phase
                if phase_num < len(phases):
                    phases[phase_num]["is_locked"] = False
                    if phases[phase_num]["status"] == "Upcoming":
                        phases[phase_num]["status"] = "In Progress"
            elif p["progress_percent"] > 0:
                p["status"] = "In Progress"

            for c in p.get("courses", []):
                if p["progress_percent"] >= 100.0:
                    c["progress_percent"] = 100.0
                    c["status"] = "Completed"
                elif p["progress_percent"] > 0:
                    c["progress_percent"] = min(100.0, round(p["progress_percent"] * (0.8 + 0.05 * (hash(c.get("name", "")) % 4)), 1))
                    c["status"] = "In Progress"
            break

    recent = state.get("recent_progress", {})
    recent["hours_learned"] = max(0.0, round(float(recent.get("hours_learned", 0.0)) + delta_hours, 1))
    recent["hours_delta"] = f"+{recent['hours_learned']}h this week" if recent["hours_learned"] > 0 else "Start today"
    state["recent_progress"] = recent

    pref.journey_state_json = json.dumps(state)
    db.commit()

    return {
        "success": True,
        "message": f"Topic {'unmarked' if is_already_done else 'completed successfully'}. Progress updated!",
        "topic_id": topic_id,
        "is_completed": not is_already_done,
        "all_journey": get_candidate_learning_journey(db, user_uuid),
    }


def get_course_curriculum_details(course_id: str) -> Dict[str, Any]:
    """Returns complete 10-chapter curriculum, practical coding exercises, projects, and interview preparation."""
    norm = course_id.lower().strip() if course_id else "java"
    track = COURSE_TRACKS.get(norm, COURSE_TRACKS["java"])

    chapters = []
    try:
        if norm == "java":
            from app.services.comprehensive_curriculum.curriculum_java import JAVA_CHAPTERS
            chapters = JAVA_CHAPTERS
        elif norm == "python":
            from app.services.comprehensive_curriculum.curriculum_python import PYTHON_CHAPTERS
            chapters = PYTHON_CHAPTERS
        elif norm == "dsa":
            from app.services.comprehensive_curriculum.curriculum_dsa import DSA_CHAPTERS
            chapters = DSA_CHAPTERS
        elif norm == "web_dev":
            from app.services.comprehensive_curriculum.curriculum_javascript import JAVASCRIPT_CHAPTERS
            chapters = JAVASCRIPT_CHAPTERS
        elif norm == "ai_ml":
            from app.services.comprehensive_curriculum.curriculum_ai_ml import AI_ML_CHAPTERS
            chapters = AI_ML_CHAPTERS
        elif norm == "data_science":
            from app.services.comprehensive_curriculum.curriculum_data_science import DATA_SCIENCE_CHAPTERS
            chapters = DATA_SCIENCE_CHAPTERS
        elif norm == "cloud_computing":
            from app.services.comprehensive_curriculum.curriculum_cloud_computing import CLOUD_COMPUTING_CHAPTERS
            chapters = CLOUD_COMPUTING_CHAPTERS
        elif norm == "aws":
            from app.services.comprehensive_curriculum.curriculum_aws import AWS_CHAPTERS
            chapters = AWS_CHAPTERS
        elif norm == "cybersecurity":
            from app.services.comprehensive_curriculum.curriculum_cybersecurity import CYBERSECURITY_CHAPTERS
            chapters = CYBERSECURITY_CHAPTERS
        elif norm == "devops":
            from app.services.comprehensive_curriculum.curriculum_devops import DEVOPS_CHAPTERS
            chapters = DEVOPS_CHAPTERS
        elif norm == "sql_db":
            from app.services.comprehensive_curriculum.curriculum_sql import SQL_CHAPTERS
            chapters = SQL_CHAPTERS
        elif norm == "gen_ai":
            from app.services.comprehensive_curriculum.curriculum_gen_ai import GEN_AI_CHAPTERS
            chapters = GEN_AI_CHAPTERS
        elif norm == "deep_learning":
            from app.services.comprehensive_curriculum.curriculum_deep_learning import DEEP_LEARNING_CHAPTERS
            chapters = DEEP_LEARNING_CHAPTERS
        elif norm == "software_testing":
            from app.services.comprehensive_curriculum.curriculum_software_testing import SOFTWARE_TESTING_CHAPTERS
            chapters = SOFTWARE_TESTING_CHAPTERS
        else:
            from app.services.comprehensive_curriculum.curriculum_java import JAVA_CHAPTERS
            chapters = JAVA_CHAPTERS
    except Exception as err:
        logger.warning(f"Could not load full chapter curriculum for {norm}: {err}")
        chapters = []

    practical_exercises = list(track.get("practical_exercises", []))
    real_world_projects = list(track.get("real_world_projects", []))
    placement_training = dict(track.get("placement_training", {}))

    # Synthesize practical exercises from curriculum solved examples if empty
    if not practical_exercises:
        for ch_idx, ch in enumerate(chapters):
            sec = ch.get("sections", {})
            for ex_idx, ex in enumerate(sec.get("solved_examples", [])):
                practical_exercises.append({
                    "id": f"{norm}-ex-{len(practical_exercises)+1}",
                    "title": ex.get("title", f"Hands-on Lab: {ch.get('title')}"),
                    "difficulty": ex.get("difficulty", "Medium | Placement Prep"),
                    "phase": 1 if len(practical_exercises) < 3 else 2,
                    "description": ex.get("problem", f"Practical implementation exercise covering {ch.get('title')}."),
                    "starter_code": ex.get("code_or_math", "// Implement solution here"),
                    "expected_time": "20 mins",
                    "action_url": f"coding-assessment.html?lang={norm}&problem={len(practical_exercises)+1}",
                })
                if len(practical_exercises) >= 5:
                    break
            if len(practical_exercises) >= 5:
                break

    # Synthesize real-world production projects if empty
    if not real_world_projects:
        course_name = track["name"]
        real_world_projects = [
            {
                "id": f"proj-{norm}-1",
                "title": f"Enterprise {course_name} Microservice & API Engine",
                "difficulty": "Production Microservice",
                "phase": 3,
                "badge": "Portfolio Essential",
                "tech_stack": [course_name, "REST APIs", "PostgreSQL", "Docker", "Authentication"],
                "description": f"Architect and build an end-to-end production microservice applying {course_name} core design patterns, database modeling, and secure API gateways.",
                "architecture": "3-Tier Controller-Service-Repository architecture with stateless JWT security, PostgreSQL persistence, and containerized deployment.",
                "key_features": [
                    f"Full CRUD lifecycle and business validation logic implemented with {course_name}",
                    "Role-based access control, request sanitization, and structured audit logs",
                    "Automated integration tests and Docker container deployment workflow"
                ],
                "action_url": f"study-materials.html?project={norm}-api"
            },
            {
                "id": f"proj-{norm}-2",
                "title": f"High-Throughput Distributed {course_name} Processing System",
                "difficulty": "Scalable Cloud Architecture",
                "phase": 3,
                "badge": "Industry Capstone",
                "tech_stack": [course_name, "Redis", "Asynchronous Queues", "Metrics & Monitoring"],
                "description": f"Build a resilient, high-concurrency event-driven pipeline processing asynchronous tasks, background analytics, and distributed state management.",
                "architecture": "Event-driven publisher-subscriber architecture with worker queues, Redis caching, and health-check monitoring.",
                "key_features": [
                    "Dead-letter queues and automated retry mechanics for fault tolerance",
                    "Optimized cache-aside strategy reducing backend response times under heavy load",
                    "Configurable alert thresholds and structured JSON logging"
                ],
                "action_url": f"study-materials.html?project={norm}-distributed"
            },
            {
                "id": f"proj-{norm}-3",
                "title": f"Production-Grade {course_name} CI/CD & Cloud Deployment Capstone",
                "difficulty": "Full-Stack Deployment",
                "phase": 3,
                "badge": "Placement Accelerator",
                "tech_stack": [course_name, "Docker", "GitHub Actions", "Cloud Infrastructure", "Kubernetes"],
                "description": f"Package, automate testing, and deploy the entire {course_name} workload to cloud environments with automated zero-downtime rollouts.",
                "architecture": "Infrastructure as Code and automated GitOps CI/CD delivery pipeline connected to production cloud clusters.",
                "key_features": [
                    "Automated linting, security vulnerability scanning, and code coverage gates",
                    "Multi-stage Docker builds creating minimal, hardened container images",
                    "Automated canary / blue-green release simulation with rollback triggers"
                ],
                "action_url": f"study-materials.html?project={norm}-capstone"
            }
        ]

    # Synthesize placement training questions & drills if empty
    if not placement_training or not placement_training.get("top_interview_questions"):
        questions = []
        for ch in chapters:
            sec = ch.get("sections", {})
            for iq in sec.get("interview_questions", []):
                questions.append({
                    "q": iq.get("question") or iq.get("q", ""),
                    "company": iq.get("company", "Top Product / MNC Recruiter"),
                    "a": iq.get("model_answer") or iq.get("answer") or iq.get("a", ""),
                    "tip": iq.get("interviewer_tip", "Explain the concept, edge cases, and real-world trade-offs.")
                })
                if len(questions) >= 6:
                    break
            if len(questions) >= 6:
                break

        placement_training = {
            "title": f"Campus Placement Training & Job Readiness ({track['name']})",
            "target_companies": [
                "TCS NQT", "Infosys SP", "Cognizant GenC Next", "Accenture", "Amazon", "Microsoft", "Capgemini", "Wipro Turbo"
            ],
            "top_interview_questions": questions,
            "speed_aptitude_drills": [
                {
                    "title": f"Technical Aptitude & Problem Solving for {track['name']}",
                    "topics": "Core Fundamentals, Code Debugging, Output Prediction, Complexity Analysis",
                    "questions_count": 25,
                    "action_url": "study-materials.html?topic=aptitude"
                },
                {
                    "title": "Logical Reasoning & Deductive Logic Drills",
                    "topics": "Data Interpretation, Pattern Analysis, Algorithmic Thinking",
                    "questions_count": 20,
                    "action_url": "study-materials.html?topic=reasoning"
                }
            ],
            "mock_interview_action": {
                "title": f"Start AI Proctored {track['name']} Mock Interview",
                "description": f"Simulate a live 30-minute technical interview for {track['name']} with real-time feedback, coding challenges, and readiness scoring.",
                "action_url": f"interview.html?track={norm}",
                "button_text": f"Launch {track['name']} Mock Interview →"
            }
        }

    from app.services.course_real_world_pedagogy import get_chapter_pedagogy, get_course_progression_overview

    enriched_chapters = []
    for ch in chapters:
        ch_copy = dict(ch)
        num = ch_copy.get("chapter_num", 1)
        title = ch_copy.get("title", "")
        ped = get_chapter_pedagogy(norm, num, title, len(chapters))
        ch_copy["progression_stage"] = ped.get("stage_num", 1)
        ch_copy["stage_title"] = ped.get("stage_title", "Foundations")
        ch_copy["stage_badge"] = ped.get("stage_badge", "Fundamentals")
        ch_copy["stage_color"] = ped.get("stage_color", "success")
        ch_copy["stage_guidance"] = ped.get("guidance", "")
        ch_copy["real_world_application"] = ped.get("real_world_application", {})
        enriched_chapters.append(ch_copy)

    progression_overview = get_course_progression_overview(norm, track["name"], len(chapters))

    return {
        "course_id": track["id"],
        "course_name": track["name"],
        "course_title": track["title"],
        "icon": track["icon"],
        "badge": track["badge"],
        "target_role": track["target_role"],
        "description": track["description"],
        "chapters_count": len(chapters),
        "progression_overview": progression_overview,
        "chapters": enriched_chapters,
        "practical_exercises": practical_exercises,
        "real_world_projects": real_world_projects,
        "placement_training": placement_training,
    }


def advance_candidate_phase(
    db: Session,
    user_id: Any,
    phase_num: int,
    delta_percent: float = 20.0,
    set_exact_percent: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Advances candidate progress in a given phase and updates individual course percentages.
    Enforces stage gates: cannot advance Phase 2 if Phase 1 is not 100%, etc.
    """
    user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
    if not pref:
        get_candidate_learning_journey(db, user_uuid)
        pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()

    state = json.loads(pref.journey_state_json) if pref.journey_state_json else {}
    selected_course = state.get("selected_course", "java")
    track = COURSE_TRACKS.get(selected_course, COURSE_TRACKS["java"])
    phases = state.get("phases", copy.deepcopy(track["phases"]))

    # Validate prerequisite stage gates
    if phase_num == 2 and phases[0]["progress_percent"] < 100.0:
        return {
            "success": False,
            "message": "Stage Gate Enforced: You must complete Phase 1 (Foundations) to 100% before starting Phase 2 (Core Skills & Advanced Level).",
            "current_phase": 1,
            "phase_1_progress": phases[0]["progress_percent"],
        }
    if phase_num == 3 and phases[1]["progress_percent"] < 100.0:
        return {
            "success": False,
            "message": "Stage Gate Enforced: You must complete Phase 2 (Core Skills & Advanced Level) to 100% before starting Phase 3 (Practical Projects).",
            "current_phase": 2,
            "phase_2_progress": phases[1]["progress_percent"],
        }
    if phase_num == 4 and phases[2]["progress_percent"] < 100.0:
        return {
            "success": False,
            "message": "Stage Gate Enforced: You must complete your Practical Projects in Phase 3 before unlocking Phase 4 (Placement Interview Preparation).",
            "current_phase": 3,
            "phase_3_progress": phases[2]["progress_percent"],
        }

    target_p = None
    for p in phases:
        if p["phase_num"] == phase_num:
            target_p = p
            break

    if not target_p:
        return {"success": False, "message": f"Phase {phase_num} not found."}

    if set_exact_percent is not None:
        target_p["progress_percent"] = max(0.0, min(100.0, float(set_exact_percent)))
    else:
        target_p["progress_percent"] = max(0.0, min(100.0, target_p["progress_percent"] + delta_percent))

    new_p_pct = target_p["progress_percent"]

    courses = target_p.get("courses", [])
    for c in courses:
        if new_p_pct >= 100.0:
            c["progress_percent"] = 100.0
            c["status"] = "Completed"
        elif new_p_pct > 0.0:
            c["progress_percent"] = min(100.0, round(new_p_pct * (0.8 + 0.1 * (hash(c.get("name", "")) % 3)), 1))
            c["status"] = "In Progress"
        else:
            c["progress_percent"] = 0.0
            c["status"] = "Not Started" if phase_num == 1 else "Upcoming"

    if new_p_pct >= 100.0:
        target_p["status"] = "Completed"
        target_p["progress_percent"] = 100.0
        # Unlock next phase
        next_idx = phase_num
        if next_idx < len(phases):
            phases[next_idx]["is_locked"] = False
            phases[next_idx]["status"] = "In Progress"
    else:
        target_p["status"] = "In Progress"

    state["phases"] = phases
    pref.journey_state_json = json.dumps(state)
    db.commit()

    return {
        "success": True,
        "message": f"Successfully updated Phase {phase_num} progress to {target_p['progress_percent']}%",
        "phase": target_p,
        "all_journey": get_candidate_learning_journey(db, user_uuid),
    }


def toggle_daily_task(db: Session, user_id: Any, task_id: str) -> Dict[str, Any]:
    """Toggles a daily plan task status between Pending -> In Progress -> Completed -> Pending."""
    user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id
    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
    if not pref:
        get_candidate_learning_journey(db, user_uuid)
        pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()

    state = json.loads(pref.journey_state_json) if pref.journey_state_json else {}
    selected_course = state.get("selected_course", "java")
    track = COURSE_TRACKS.get(selected_course, COURSE_TRACKS["java"])
    tasks = state.get("today_plan", copy.deepcopy(track["today_plan"]))
    recent = state.get("recent_progress", copy.deepcopy(DEFAULT_RECENT_PROGRESS))

    target_task = None
    for t in tasks:
        if t["id"] == task_id:
            target_task = t
            break

    if not target_task:
        return {"success": False, "message": f"Task '{task_id}' not found."}

    cur_status = target_task.get("status", "Pending")
    if cur_status == "Completed":
        target_task["status"] = "Pending"
        target_task["progress_percent"] = 0.0
        recent["hours_learned"] = max(0.0, round(float(recent.get("hours_learned", 0.0)) - 0.5, 1))
    elif cur_status == "In Progress":
        target_task["status"] = "Completed"
        target_task["progress_percent"] = 100.0
        recent["hours_learned"] = round(float(recent.get("hours_learned", 0.0)) + 0.5, 1)
    else:
        target_task["status"] = "In Progress"
        target_task["progress_percent"] = 50.0

    state["today_plan"] = tasks
    state["recent_progress"] = recent
    pref.journey_state_json = json.dumps(state)
    db.commit()

    return {
        "success": True,
        "message": f"Task '{target_task['title']}' updated to {target_task['status']}",
        "task": target_task,
        "all_journey": get_candidate_learning_journey(db, user_uuid),
    }


def reset_to_reference_dashboard(db: Session, user_id: Any) -> Dict[str, Any]:
    """Resets the candidate's learning dashboard state to a fresh, clean 0% starting state."""
    user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id
    user_rec = db.query(User).filter(User.id == user_uuid).first()
    cand_prof = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_uuid).first()

    pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
    if not pref:
        pref = StudentLearningPreference(user_id=user_uuid, daily_streak=1)
        db.add(pref)

    cur_state = {}
    if pref.journey_state_json:
        try:
            cur_state = json.loads(pref.journey_state_json)
        except Exception:
            cur_state = {}
    selected_course = cur_state.get("selected_course", "java") if cur_state else "java"
    state = create_course_journey_state(selected_course, user_rec, cand_prof)
    state["course_started_at"] = None
    state["is_started"] = False
    pref.journey_state_json = json.dumps(state)
    pref.daily_streak = 1
    db.commit()
    return get_candidate_learning_journey(db, user_uuid)


def _sync_live_candidate_performance(
    db: Session,
    user_uuid: uuid.UUID,
    phases: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]],
    today_plan: List[Dict[str, Any]],
    strengths: List[str],
    focus_areas: List[str],
    recent_progress: Dict[str, Any],
    completed_topics: Optional[List[str]] = None,
) -> None:
    """
    Dynamically recalculates all progress percentages, strengths, focus areas,
    courses completed, and projects built from actual candidate records in PostgreSQL.
    """
    try:
        # 1. Check Aptitude test attempts
        attempts = db.query(CandidateTestAttempt).filter(CandidateTestAttempt.user_id == user_uuid).all()
        topic_scores: Dict[str, List[float]] = {}
        total_test_pct = 0.0
        for att in attempts:
            pct = float(att.percentage or 0.0)
            total_test_pct += pct
            if att.test and att.test.topics_json:
                try:
                    tops = json.loads(att.test.topics_json)
                    for top in tops:
                        topic_scores.setdefault(top, []).append(pct)
                except Exception:
                    pass

        # Adjust strengths and focus areas dynamically based on candidate's real scores
        for top, scores in topic_scores.items():
            avg_score = sum(scores) / len(scores)
            if avg_score >= 75.0 and top not in strengths:
                strengths.append(top)
                if top in focus_areas:
                    focus_areas.remove(top)
            elif avg_score < 60.0 and top not in focus_areas:
                focus_areas.append(top)
                if top in strengths:
                    strengths.remove(top)

        # 2. Check CandidateProfile skills
        prof = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_uuid).first()
        cand_id = prof.id if prof else None
        if prof and hasattr(prof, "skills") and prof.skills:
            try:
                if isinstance(prof.skills, str):
                    cand_skills = [s.strip() for s in prof.skills.split(",") if s.strip()]
                elif isinstance(prof.skills, (list, set)):
                    cand_skills = [str(getattr(s, "name", s)) for s in prof.skills]
                else:
                    cand_skills = []
                for cs in cand_skills[:3]:
                    if cs not in strengths:
                        strengths.append(cs)
            except Exception:
                pass

        # 3. Check Coding attempts & project submissions
        coding_attempts_count = 0
        coding_avg_pct = 0.0
        projects_passed_count = 0
        if cand_id:
            coding_attempts = db.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.candidate_id == cand_id).all()
            coding_attempts_count = len(coding_attempts)
            if coding_attempts:
                coding_avg_pct = sum(float(ca.percentage or 0.0) for ca in coding_attempts) / len(coding_attempts)
                projects_passed_count = sum(1 for ca in coding_attempts if float(ca.percentage or 0.0) >= 60.0)

        # 4. Check Interviews conducted
        interview_count = 0
        interview_avg_score = 0.0
        if cand_id:
            interviews = db.query(Interview).filter(Interview.candidate_id == cand_id).all()
            interview_count = len(interviews)
            if interviews:
                scores = [float(iv.overall_score or 0.0) for iv in interviews if iv.overall_score is not None]
                if scores:
                    interview_avg_score = sum(scores) / len(scores)

        # 5. Dynamically calibrate Phase and Course Progress ONLY if actual candidate activity exists
        if attempts:
            avg_apt_pct = total_test_pct / len(attempts)
            p1 = phases[0]
            if p1["progress_percent"] < 100.0:
                test_contribution = min(60.0, len(attempts) * 15.0)
                score_contribution = (avg_apt_pct / 100.0) * 40.0
                calc_p1 = min(99.0, test_contribution + score_contribution)
                p1["progress_percent"] = max(p1["progress_percent"], round(calc_p1, 1))
                for idx, c in enumerate(p1.get("courses", [])):
                    course_calc = min(100.0, round(avg_apt_pct * (0.8 + 0.05 * (idx % 4)), 1))
                    c["progress_percent"] = max(c.get("progress_percent", 0.0), course_calc)
                    if c["progress_percent"] >= 100.0:
                        c["status"] = "Completed"
                    elif c["progress_percent"] > 0:
                        c["status"] = "In Progress"

        if coding_attempts_count > 0:
            for r in recommendations:
                if any(k in r.get("title", "") for k in ["Collections", "Data Structures", "Spring Boot"]):
                    r["progress_percent"] = min(100.0, round(coding_avg_pct, 1))
            p2 = phases[1]
            if not p2.get("is_locked", True) and p2["progress_percent"] < 100.0:
                p2["progress_percent"] = max(p2["progress_percent"], round(min(90.0, coding_avg_pct), 1))

        if interview_count > 0:
            p4 = phases[3]
            if not p4.get("is_locked", True):
                p4["progress_percent"] = max(p4["progress_percent"], round(min(100.0, interview_avg_score), 1))

        # 6. Dynamically update Recent Progress metrics
        completed_courses = 0
        for p in phases:
            if p.get("progress_percent", 0.0) >= 100.0:
                completed_courses += len(p.get("courses", []))
            else:
                completed_courses += sum(1 for c in p.get("courses", []) if c.get("progress_percent", 0.0) >= 100.0)

        completed_tasks_count = sum(1 for t in today_plan if t.get("status") == "Completed")
        completed_topics_count = len(completed_topics or [])

        recent_progress["courses_completed"] = completed_courses
        recent_progress["courses_delta"] = f"+{completed_courses} this week" if completed_courses > 0 else "0 completed"

        recent_progress["projects_built"] = projects_passed_count
        recent_progress["projects_delta"] = f"+{projects_passed_count} this week" if projects_passed_count > 0 else "0 built"

        calculated_hours = (completed_topics_count * 0.5) + (completed_tasks_count * 0.5) + (len(attempts) * 0.3) + (coding_attempts_count * 0.5) + (interview_count * 0.75)
        recent_progress["hours_learned"] = round(calculated_hours, 1)
        recent_progress["hours_delta"] = f"+{recent_progress['hours_learned']}h this week" if recent_progress["hours_learned"] > 0 else "Start today"

        pref = db.query(StudentLearningPreference).filter(StudentLearningPreference.user_id == user_uuid).first()
        recent_progress["streak_days"] = pref.daily_streak if (pref and pref.daily_streak) else 1

    except Exception as err:
        logger.warning(f"Could not sync live candidate performance: {err}")
