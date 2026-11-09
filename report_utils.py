from datetime import datetime


def build_report(result: dict, suggestions: list[str]) -> str:
    lines = [
        "AI RESUME ANALYZER - MATCH REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Overall match score: {result['match_score']}%",
        f"Skill coverage: {result['skill_coverage']}%",
        f"Text similarity: {result['text_similarity']}%",
        "",
        "MATCHED SKILLS:",
        ", ".join(result["matched_skills"]) or "None detected",
        "",
        "SKILLS TO DEVELOP / NOT DETECTED:",
        ", ".join(result["missing_skills"]) or "None detected",
        "",
        "SKILLS DETECTED IN RESUME:",
        ", ".join(result["resume_skills"]) or "None detected",
        "",
        "SKILLS DETECTED IN JOB DESCRIPTION:",
        ", ".join(result["job_skills"]) or "None detected",
        "",
        "RECOMMENDATIONS:",
    ]
    lines.extend(f"- {suggestion}" for suggestion in suggestions)
    lines += [
        "",
        "DISCLAIMER:",
        "This report is an automated estimate based on TF-IDF text similarity and a built-in skill keyword list.",
        "It is not a hiring decision, professional assessment, or guarantee of interview selection.",
        "Missing means not detected in the supplied resume text; it does not prove the applicant lacks the skill.",
    ]
    return "\n".join(lines)
