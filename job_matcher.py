import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Extend this list to support more industries and job roles.
SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "html", "css",
    "react", "angular", "node.js", "django", "flask", "streamlit", "machine learning",
    "deep learning", "artificial intelligence", "data analysis", "data science",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "excel", "power bi",
    "tableau", "aws", "azure", "google cloud", "docker", "kubernetes", "git", "github",
    "linux", "cybersecurity", "networking", "communication", "teamwork", "leadership",
    "problem solving", "project management", "time management", "research", "writing",
    "legal research", "contract drafting", "litigation", "case law", "legal writing",
    "client communication", "microsoft word", "microsoft office", "accounting",
    "marketing", "sales", "customer service", "seo", "content writing"
]


def _contains_skill(text: str, skill: str) -> bool:
    # Use word boundaries for short/simple terms; escape punctuation in skill names.
    pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
    return re.search(pattern, text.lower()) is not None


def extract_skills(text: str) -> list[str]:
    found = [skill for skill in SKILL_KEYWORDS if _contains_skill(text, skill)]
    return sorted(found)


def calculate_similarity(resume_text: str, job_description: str) -> float:
    """Calculate cosine similarity between resume and job description using TF-IDF."""
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform([resume_text, job_description])
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return round(float(score) * 100, 1)
    except ValueError:
        return 0.0


def analyze_match(resume_text: str, job_description: str) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))

    # Skill coverage is weighted more heavily than broad text similarity.
    if job_skills:
        skill_coverage = len(matched) / len(job_skills) * 100
        overall = round((skill_coverage * 0.7) + (calculate_similarity(resume_text, job_description) * 0.3))
    else:
        skill_coverage = 0.0
        overall = round(calculate_similarity(resume_text, job_description))

    return {
        "match_score": max(0, min(100, int(overall))),
        "skill_coverage": round(skill_coverage, 1),
        "text_similarity": calculate_similarity(resume_text, job_description),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
    }
