import streamlit as st
from resume_parser import extract_text_from_pdf
from job_matcher import analyze_match
from ai_suggestions import generate_suggestions
from report_utils import build_report

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & Job Matcher")
st.caption("Compare a resume with a job description, identify matching skills, and get practical improvement tips.")
st.info("Free version: runs locally with Python. No paid API key or external AI service is required.")

with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. Upload a PDF resume or paste resume text.\\n"
        "2. Paste the target job description.\\n"
        "3. Click **Analyze Resume**.\\n"
        "4. Review the match score, skills gap, and suggestions."
    )
    st.caption("Your resume is processed locally by this app and is not uploaded to an AI service.")

left, right = st.columns(2)
with left:
    st.subheader("1. Your resume")
    uploaded_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
    resume_text_input = st.text_area(
        "Or paste your resume text",
        height=260,
        placeholder="Paste your resume content here..."
    )
with right:
    st.subheader("2. Target job")
    job_description = st.text_area(
        "Paste the complete job description",
        height=340,
        placeholder="Paste the job title, responsibilities, required skills, qualifications, and experience..."
    )

if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
    resume_text = resume_text_input.strip()
    if uploaded_file is not None:
        try:
            pdf_text = extract_text_from_pdf(uploaded_file)
            if pdf_text.strip():
                resume_text = pdf_text
            elif not resume_text:
                st.error("No readable text was found in this PDF. It may be scanned. Try copying the text into the box.")
        except Exception as exc:
            st.error(f"Could not read the PDF: {exc}")

    if not resume_text:
        st.error("Please upload a readable PDF or paste your resume text.")
    elif not job_description.strip():
        st.error("Please paste the target job description.")
    else:
        result = analyze_match(resume_text, job_description)
        suggestions = generate_suggestions(result, resume_text, job_description)
        st.session_state["analysis"] = {
            "result": result,
            "suggestions": suggestions,
            "resume_text": resume_text,
            "job_description": job_description,
        }

if "analysis" in st.session_state:
    data = st.session_state["analysis"]
    result = data["result"]
    suggestions = data["suggestions"]

    st.divider()
    st.header("3. Analysis results")
    score_col, skill_col, missing_col = st.columns(3)
    score_col.metric("Overall match", f'{result["match_score"]}%')
    skill_col.metric("Matched skills", len(result["matched_skills"]))
    missing_col.metric("Skills to develop", len(result["missing_skills"]))

    st.progress(result["match_score"] / 100)
    if result["match_score"] >= 75:
        st.success("Strong keyword and content overlap. Review the recommendations before applying.")
    elif result["match_score"] >= 45:
        st.warning("Moderate overlap. Tailor your resume to the role's most relevant requirements.")
    else:
        st.error("Low overlap. Review the role requirements and consider whether this position fits your experience.")

    a, b = st.columns(2)
    with a:
        st.subheader("✅ Skills found in both")
        if result["matched_skills"]:
            st.write(", ".join(result["matched_skills"]))
        else:
            st.write("No skills from the built-in skill list were found in both texts.")
    with b:
        st.subheader("🎯 Skills in job description, not detected in CV")
        if result["missing_skills"]:
            st.write(", ".join(result["missing_skills"]))
        else:
            st.write("No missing skills detected from the built-in skill list.")

    with st.expander("View skills detected in your resume"):
        st.write(", ".join(result["resume_skills"]) or "No listed skills detected.")
    with st.expander("View skills detected in the job description"):
        st.write(", ".join(result["job_skills"]) or "No listed skills detected.")

    st.subheader("💡 Practical improvement suggestions")
    for item in suggestions:
        st.markdown(f"- {item}")

    st.subheader("🧾 Keyword overlap")
    st.caption("This is a simple TF-IDF similarity measure, not a hiring decision or a guarantee of interview selection.")
    st.write(f'Text similarity: **{result["text_similarity"]}%**')

    report = build_report(result, suggestions)
    st.download_button(
        "⬇️ Download analysis report (.txt)",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.divider()
st.caption("Note: Match scores are estimates based on text similarity and a built-in skill dictionary. Always verify that your resume accurately represents your real qualifications.")
