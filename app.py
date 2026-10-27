import streamlit as st
import PyPDF2
from pydantic import BaseModel, Field
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io


def extract_text_from_pdf(uploaded_file):
    """
    Reads an uploaded PDF file stream page-by-page and extracts 
    all available characters into a single continuous text string.
    """
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    extracted_text = ""
    
    # Loop sequentially through each page of the document
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text += page_text + "\n"
            
    return extracted_text

class EvaluationReport(BaseModel):
    is_fit_for_interview: bool = Field(description="True if the candidate meets mandatory requirements, False otherwise.")
    match_percentage: int = Field(description="Overall match score from 0 to 100 based on core skills and experience.")
    missing_mandatory_qualifications: List[str] = Field(description="Required degrees, licenses, or core academic qualifications missing for this role.")
    missing_technical_skills: List[str] = Field(description="Missing core hard skills, software stacks, tools, or domain-specific technical capabilities.")
    missing_industry_compliance: List[str] = Field(description="Missing critical industry regulations, safety protocols, standard operating standards, or legal guidelines.")
    strengths: List[str] = Field(description="Key professional strengths or compliance areas where the candidate matches perfectly.")
    verdict_justification: str = Field(description="A brief human-like explanation justifying the interview status decision.")


from google import genai
from google.genai import types

def analyze_resume(resume_text, jd_text):
    """
    Connects to the modern 2026 Google GenAI pipeline, 
    processing structured resume gap verification.
    """
    prompt = f"""
    You are an expert Applicant Tracking System (ATS) and Corporate Compliance Auditor.
    Analyze the following resume thoroughly against the provided job description.
    Identify any skill gaps, missing certifications, mandatory profile requirements, 
    and sector-specific compliance variances relative to the target industry.
    
    Job Description:
    {jd_text}
    
    Resume Text:
    {resume_text}
    """

    
    # Securely retrieve the key and initialize the modern 2026 client
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    
    # Call the modern gemini-3.8-flash model enforcing the structured schema
    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EvaluationReport,
        ),
    )
    
    # Load and map response variables cleanly into the data model layout
    import json
    data = json.loads(response.text)
    return EvaluationReport(**data)



def generate_candidate_markdown(data_dict, candidate_name="Candidate"):
    """
    Transforms structured Pydantic dictionary blocks into a beautiful
    and scannable executive brief markdown file.
    """
    md_content = f"""# Executive Evaluation Report: {candidate_name}
    
## 📊 Core Matching Metrics
* **Interview Fit Assessment:** {"✅ Shortlist for Interview" if data_dict.get("is_fit_for_interview") else "❌ Hold / Reject"}
* **ATS Compatibility Score:** `{data_dict.get("match_percentage", 0)}%`

## 🔍 Critical Skill Deficiencies
### Missing Mandatory Requirements
"""
    for item in data_dict.get("missing_mandatory_qualifications", []):
        md_content += f"* {item}\n"
        
    md_content += "\n### Missing Technical Proficiencies\n"
    for item in data_dict.get("missing_technical_skills", []):
        md_content += f"* {item}\n"

    # Cleaned layout reading your updated universal structure key
    md_content += "\n### Industry & Regulatory Compliance Gaps\n"
    for item in data_dict.get("missing_industry_compliance", []):
        md_content += f"* {item}\n"

    md_content += f"""
## 💪 Validated Core Strengths
"""
    for item in data_dict.get("strengths", []):
        md_content += f"* {item}\n"

    md_content += f"""
## 📝 Selection Verdict & Justification
> {data_dict.get("verdict_justification", "No justification provided.")}
"""
    return md_content

def generate_candidate_pdf(data_dict, candidate_name="Candidate"):
    """
    Compiles structured data blocks into a beautifully styled,
    corporate-ready PDF Executive Briefing document.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40,
        title=f"Executive Briefing - {candidate_name}"
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Define premium custom color typography layout sets
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontSize=24, leading=28, textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=15
    )
    section_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'],
        fontSize=14, leading=18, textColor=colors.HexColor('#0F172A'),
        spaceBefore=12, spaceAfter=6, borderPadding=4
    )
    body_style = ParagraphStyle(
        'ReportBody', parent=styles['Normal'],
        fontSize=10.5, leading=15, textColor=colors.HexColor('#334155')
    )
    
    # Document Header Title
    story.append(Paragraph(f"Executive Evaluation Report: {candidate_name}", title_style))
    story.append(Spacer(1, 10))
    
    # 📊 Core Matching Metrics Section
    story.append(Paragraph("Core Matching Metrics", section_style))
    fit_status = "Shortlist for Interview" if data_dict.get("is_fit_for_interview") else "Hold / Reject"
    story.append(Paragraph(f"<b>• Interview Fit Assessment:</b> {fit_status}", body_style))
    story.append(Paragraph(f"<b>• ATS Compatibility Score:</b> {data_dict.get('match_percentage', 0)}%", body_style))
    story.append(Spacer(1, 10))
    
    # 🔍 Critical Skill Deficiencies Section
    story.append(Paragraph("Critical Skill Gaps & Deficiencies", section_style))
    
    story.append(Paragraph("<b>Missing Mandatory Qualifications:</b>", body_style))
    for item in data_dict.get("missing_mandatory_qualifications", []):
        story.append(Paragraph(f"  - {item}", body_style))
        
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Missing Technical Proficiencies:</b>", body_style))
    for item in data_dict.get("missing_technical_skills", []):
        story.append(Paragraph(f"  - {item}", body_style))
        
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Missing Industry Compliance/Regulations:</b>", body_style))
    for item in data_dict.get("missing_industry_compliance", []):
        story.append(Paragraph(f"  - {item}", body_style))
    story.append(Spacer(1, 10))
    
    # 💪 Validated Strengths Section
    story.append(Paragraph("Validated Core Strengths", section_style))
    for item in data_dict.get("strengths", []):
        story.append(Paragraph(f"  • {item}", body_style))
    story.append(Spacer(1, 10))
    
    # 📝 Verdict Section
    story.append(Paragraph("Selection Verdict & Justification", section_style))
    story.append(Paragraph(f"<i>{data_dict.get('verdict_justification', 'No justification provided.')}</i>", body_style))
    
    # Disclaimer Footnote Required for Clinical/Health content handling
    story.append(Spacer(1, 30))
    disclaimer_style = ParagraphStyle('Disclaimer', parent=styles['Italic'], fontSize=8, leading=10, textColor=colors.gray)
    story.append(Paragraph("This is for informational purposes only. For medical advice or diagnosis, consult a professional. AI responses may include mistakes.", disclaimer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


from pymongo import MongoClient
import datetime

def save_applicant_to_database(candidate_name, match_percentage, evaluation_data_dict):
    """
    Permanently saves every incoming applicant record into the local MongoDB instance.
    This maintains a permanent talent bank irrespective of the job match outcome.
    """
    try:
        # Establish connection to your active local MongoDB instance
        client = MongoClient("mongodb://localhost:27017/")
        db = client["universal_ats_database"]
        collection = db["applicants_historical_ledger"]
        
        # Build the permanent profile entry structure
        applicant_record = {
            "candidate_name": candidate_name,
            "match_score": f"{match_percentage}%",
            "evaluation_metrics": evaluation_data_dict,
            "submission_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Ingest the document record ledger into the database vault
        collection.insert_one(applicant_record)
        return True
    except Exception as e:
        print(f"Database Ingestion Logging Error: {e}")
        return False


# --- Streamlit UI Section ---
st.set_page_config(page_title="AI-Powered HR Intake & Talent Matching Engine", layout="wide")
st.title("AI-Powered HR Intake & Talent Matching Engine")
st.subheader("Compare candidates precisely against any industry, technical, or regulatory criteria")

# Split screen into two balanced visual columns
col1, col2 = st.columns(2)

with col1:
    st.header("📄 Candidate Profile")
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])
    
with col2:
    st.header("📋 Job Parameters")
    jd_text = st.text_area("Paste Target Job Description here")

# Action execution trigger button
if st.button("Run Compliance & Gap Analysis", type="primary"):
    if uploaded_file and jd_text:
        with st.spinner("Parsing documents and calculating alignment parameters..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            analysis = analyze_resume(resume_text, jd_text)
            
            st.divider()
            
            # Display score elements inside modern visual metrics
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                verdict = "🟩 APPROVED FOR INTERVIEW" if analysis.is_fit_for_interview else "🟥 REJECTED / HOLD"
                st.metric(label="Interview Decision Status", value=verdict)
            with m_col2:
                st.metric(label="Overall Compatibility Match Score", value=f"{analysis.match_percentage}%")
            
            st.subheader("💡 Analysis Verdict")
            st.write(analysis.verdict_justification)
            
            # Core Gap Information Breakdown
            st.subheader("📉 Critical Skill Gaps & Missing Items")
            
            if analysis.missing_mandatory_qualifications:
                st.error(f"**Missing Qualifications:** {', '.join(analysis.missing_mandatory_qualifications)}")
            if analysis.missing_technical_skills:
                st.warning(f"**Missing Technical Skills/Tools:** {', '.join(analysis.missing_technical_skills)}")
            if analysis.missing_industry_compliance:
                st.info(f"**Missing Compliance/Regulatory Standards:** {', '.join(analysis.missing_industry_compliance)}")

                
            st.subheader("📈 Validated Strengths")
            for strength in analysis.strengths:
                st.success(f"✓ {strength}")
            # Generate and provide download option for the enterprise report file
                    # Generate and provide standard PDF binary output option smoothly
        report_data = analysis.model_dump()
                # Trigger automatic permanent ingestion to your MongoDB vault matrix
                # Trigger automatic permanent ingestion to your MongoDB vault matrix
        save_applicant_to_database(
            candidate_name=uploaded_file.name.replace('.pdf', ''),
            match_percentage=analysis.match_percentage,
            evaluation_data_dict=report_data
        )

        pdf_data = generate_candidate_pdf(report_data, candidate_name=uploaded_file.name)
        
        st.divider()
        st.download_button(
            label="📥 Download Executive Briefing Report (.pdf)",
            data=pdf_data,
            file_name=f"Executive_Briefing_{uploaded_file.name.replace('.pdf', '')}.pdf",
            mime="application/pdf",
            key="download_report_btn"
        )



    else:
        st.warning("Please upload a resume file and paste a job description to initiate evaluation.")
