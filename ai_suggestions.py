def generate_suggestions(result: dict, resume_text: str, job_description: str) -> list[str]:
    """Generate rule-based recommendations without an external paid AI API."""
    suggestions = []
    missing = result["missing_skills"]

    if missing:
        suggestions.append(
            "Review these job-description skills and add any that you genuinely have: "
            + ", ".join(missing[:10]) + ". Do not claim skills you do not possess."
        )
    else:
        suggestions.append("No gaps were detected in the built-in skill list. Check the full job description for role-specific requirements.")

    lower_resume = resume_text.lower()
    if not any(term in lower_resume for term in ["%", "increased", "reduced", "improved", "saved", "achieved"]):
        suggestions.append("Add measurable achievements where possible, such as percentage improvements, money saved, clients served, or projects completed.")

    if "summary" not in lower_resume and "profile" not in lower_resume and "objective" not in lower_resume:
        suggestions.append("Consider adding a short professional summary tailored to this job.")

    if not any(term in lower_resume for term in ["education", "degree", "university", "college"]):
        suggestions.append("Make sure your education and relevant qualifications are clearly listed.")

    if len(resume_text.split()) < 100:
        suggestions.append("Your resume text appears brief. Include relevant projects, responsibilities, education, experience, and accomplishments.")

    if result["match_score"] < 50:
        suggestions.append("Prioritize the essential requirements in the vacancy. Reorder your resume so the most relevant experience and projects appear near the top.")
    else:
        suggestions.append("Use wording from the vacancy naturally when it accurately describes your experience. Keep the resume concise and easy to scan.")

    suggestions.append("Proofread dates, contact details, spelling, and formatting before submitting.")
    return suggestions
