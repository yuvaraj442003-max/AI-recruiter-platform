"""
formatter.py - Formatter for assembling comprehensive chapter-by-chapter placement textbooks.
Transforms structured chapter data into unabridged placement markdown with:
1. Core Concepts & In-Depth Explanation
2. Key Formulas, Rules & Complexity Classes
3. Step-by-Step Solved Examples
4. Practice Questions with Answers & Explanations
5. Real Company Technical Interview Questions & Answers
"""
from typing import Dict, List, Any

def format_chapter_to_markdown(ch: Dict[str, Any], subject: str = "") -> str:
    num = ch.get("chapter_num", 1)
    title = ch.get("title", f"Chapter {num}")
    takeaway = ch.get("key_takeaways", "")
    topics = ch.get("topics", [])
    sections = ch.get("sections", {})

    concept = sections.get("concept", "").strip()
    formulas = sections.get("formulas", "").strip()
    solved_examples = sections.get("solved_examples", [])
    practice_questions = sections.get("practice_questions", [])
    interview_questions = sections.get("interview_questions", [])

    lines = [
        f"## Chapter {num}: {title}",
        "",
        f"> **Key Principle / Exam Takeaway:** {takeaway}",
        "",
        "**Core Curriculum Topics Covered in this Chapter:**",
    ]
    for top in topics:
        lines.append(f"- {top}")
    lines.append("")

    # 1. Core Concepts
    lines.extend([
        "### 📘 1. Core Concepts & In-Depth Explanation",
        "",
        concept,
        "",
    ])

    # 2. Key Formulas & Mechanics
    if formulas:
        lines.extend([
            "### 📐 2. Key Formulas, Rules & Complexity Classes",
            "",
            formulas,
            "",
        ])

    # 3. Step-by-Step Solved Examples
    lines.extend([
        "### 💡 3. Step-by-Step Solved Examples",
        "",
    ])
    if solved_examples:
        for idx, ex in enumerate(solved_examples, 1):
            ex_title = ex.get("title", f"Solved Problem {idx}")
            diff = ex.get("difficulty", "Placement Standard")
            prob = ex.get("problem", "")
            steps = ex.get("step_by_step", [])
            code = ex.get("code_or_math", "").strip()
            exp = ex.get("explanation", "").strip()

            lines.extend([
                f"#### Example {num}.{idx}: {ex_title}",
                f"- **Difficulty / Target Companies:** `{diff}`",
                f"- **Problem Statement:** {prob}",
                "",
                "**Step-by-Step Walkthrough & Logic:**",
            ])
            for st in steps:
                lines.append(f"  - {st}")
            lines.append("")

            if code:
                # Detect language
                lang = "python"
                if "SELECT " in code.upper() or "FROM " in code.upper():
                    lang = "sql"
                elif "package main" in code or "func " in code:
                    lang = "go"
                elif "fn main" in code or "let mut " in code or "impl " in code:
                    lang = "rust"
                elif "public class " in code or "System.out" in code:
                    lang = "java"
                elif "const " in code or "function " in code or "let " in code:
                    lang = "javascript"
                elif "#include" in code:
                    lang = "cpp"
                
                lines.extend([
                    "**Complete Solved Code / Calculation:**",
                    f"```{lang}",
                    code,
                    "```",
                    "",
                ])

            if exp:
                lines.extend([
                    f"- **Line-by-Line Breakdown & Complexity Analysis:** {exp}",
                    "",
                ])
    else:
        lines.extend([
            "_Comprehensive step-by-step solved drills detailed throughout syllabus._",
            "",
        ])

    # 4. Practice Questions with Answers & Explanations
    lines.extend([
        "### 📝 4. Practice Questions with Answers & Explanations",
        "",
    ])
    if practice_questions:
        for idx, pq in enumerate(practice_questions, 1):
            q_text = pq.get("question", "")
            opts = pq.get("options", [])
            ans = pq.get("correct_answer", "")
            sol = pq.get("detailed_solution") or pq.get("explanation", "")

            lines.extend([
                f"#### Practice Question {num}.{idx}",
                f"**Question:** {q_text}",
                "",
            ])
            if opts:
                lines.append("**Options:**")
                for o in opts:
                    lines.append(f"- {o}")
                lines.append("")

            lines.extend([
                f"> **Answer:** **{ans}**  ",
                f"> **Detailed Solution & Reasoning:** {sol}",
                "",
            ])
    else:
        lines.extend([
            "_Review milestone assessments and chapter quizzes to evaluate mastery._",
            "",
        ])

    # 5. Real Company Technical Interview Questions & Answers
    lines.extend([
        "### 💼 5. Real Company Technical Interview Questions & Answers",
        "",
    ])
    if interview_questions:
        for idx, iq in enumerate(interview_questions, 1):
            comp = iq.get("company") or iq.get("company_tag") or "Top Placement Recruiter"
            q_text = iq.get("question", "")
            model_ans = iq.get("model_answer") or iq.get("answer", "")
            tip = iq.get("interviewer_tip") or iq.get("pitfalls", "")

            lines.extend([
                f"#### Interview Question {num}.{idx} ({comp})",
                f"- **Interview Question:** _{q_text}_",
                f"- **Model High-Scoring Answer:** {model_ans}",
            ])
            if tip:
                lines.append(f"- **Interviewer Follow-Up & Pro Tip:** 💡 {tip}")
            lines.append("")
    else:
        lines.extend([
            "_Real interview questions and evaluation rubrics integrated with AI mock interview room._",
            "",
        ])

    lines.extend([
        "---",
        "",
    ])

    return "\n".join(lines)


def assemble_full_textbook_markdown(
    book_title: str,
    subject: str,
    edition: str,
    description: str,
    chapters: List[Dict[str, Any]]
) -> str:
    """Assembles the unabridged full textbook markdown."""
    toc_lines = []
    for ch in chapters:
        num = ch.get("chapter_num", 1)
        title = ch.get("title", f"Chapter {num}")
        anchor = f"chapter-{num}-{title.lower().replace(' ', '-').replace('&', '').replace(',', '').replace(':', '')}"
        toc_lines.append(f"- [Chapter {num}: {title}](#chapter-{num})")

    header = [
        f"# {book_title}",
        "",
        f"**Edition:** {edition}  ",
        f"**Subject:** {subject}  ",
        f"**Courseware Board:** Prescribed Placement Architectural Board  ",
        f"**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)",
        "",
        "> **🔒 EXAM GROUNDING POLICY:** All campus placement technical assessments, coding lab challenges, and technical interview evaluations are strictly grounded in the concepts, algorithms, formulas, step-by-step solved examples, practice questions, and interview questions detailed in this textbook.",
        "",
        "## 📖 Course Overview & Curriculum Scope",
        description,
        "",
        "---",
        "",
        "## 📑 Complete Table of Contents (Chapter-by-Chapter)",
        "",
    ]
    header.extend(toc_lines)
    header.extend(["", "---", ""])

    body_chapters = []
    for ch in chapters:
        body_chapters.append(format_chapter_to_markdown(ch, subject))

    footer = [
        "## 🎓 Campus Placement Certification & Final Exam Policy",
        "To earn Placement-Ready Master status, students must complete all chapter practice questions, review all solved examples, and score at least 80% on the comprehensive subject assessment.",
        "",
    ]

    return "\n".join(header) + "\n" + "\n".join(body_chapters) + "\n" + "\n".join(footer)

