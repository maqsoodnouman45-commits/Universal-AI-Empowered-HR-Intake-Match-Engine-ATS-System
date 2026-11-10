# AI-Powered HR Intake and Talent Matching Engine 🚀

> A universal, B2B-ready corporate talent acquisition platform that automatically ingests incoming candidate resumes, extracts structured evaluations against any industry job criteria, and vaults data into a persistent repository.

[![Python](https://shields.io)](https://python.org)
[![Streamlit](https://shields.io)](https://streamlit.io)
[![Google GenAI SDK](https://shields.io)](https://google.dev)
[![Database](https://shields.io)](https://www.mongodb.com/)

---

## 📋 Table of Contents
- [🌟 Key Architectural Features](#-key-architectural-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🔧 Installation & Quick Start](#-installation--quick-start)
- [⚙️ Environment Variables](#️-environment-variables)
- [🚀 Execution](#-execution)
- [📊 Data Models & Schema Enforcement](#-data-models--schema-enforcement)

---

## 🌟 Key Architectural Features

- **Universal Industry Processing:** Enforces a rigid, industry-agnostic Pydantic validation schema (`EvaluationReport`) capable of analyzing any candidate background against arbitrary corporate job descriptions.
- **High-Throughput Extraction Engine:** Built entirely around the native 2026 `google-genai` SDK, utilizing the low-latency `gemini-3.5-flash-lite` model for high-speed automated applicant vetting.
- **Automated Resume Ingestion Backend:** Features a multi-tenant corporate web intake listener that captures incoming applications, parses raw metrics, and routes them to the pipeline regardless of the specific job tier selected.
- **Corporate Report Export:** Auto-generates publication-quality, pixel-perfect `.pdf` Executive Briefing Reports utilizing ReportLab for frictionless HR handoffs.
- **Talent Repository Vaulting:** Systematically preserves structured data and applicant profiles inside a persistent local MongoDB database (`universal_ats_database`) to build long-term enterprise talent pools.

---

## 🛠️ Tech Stack

- **Backend Logic:** Python 3.10+
- **Web UI & Dashboard:** Streamlit Framework
- **AI Core:** Google GenAI SDK (`google-genai` / `gemini-3.5-flash-lite`)
- **Document Generation:** ReportLab PDF Library
- **Database Engine:** MongoDB (via PyMongo)

---

## 🔧 Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com
cd Universal-AI-Empowered-HR-Intake-Match-Engine-ATS-System
```

### 2. Configure Your Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Initialization
Ensure your local MongoDB instance is running. You can verify and inspect the data storage pipelines natively using **MongoDB Compass** by connecting to:
```text
mongodb://localhost:27017/
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory of your project to inject required credentials safely:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
MONGO_URI=mongodb://localhost:27017/
```

---

## 🚀 Execution

To spin up the platform client dashboard interface, execute the app via Streamlit:

```bash
streamlit run app.py
```

---

## 📊 Data Models & Schema Enforcement

The parsing framework relies on strict structural matching to eliminate LLM hallucinations. All incoming data structures resolve directly against the following strict object validation layout:

```python
from pydantic import BaseModel, Field
from typing import List

class EvaluationReport(BaseModel):
    candidate_name: str = Field(description="Full legal name of the candidate")
    skills_match_percentage: float = Field(description="Score mapping candidate competencies to the core JD")
    core_strengths: List[str] = Field(description="Key professional advantages highlighted in the intake profile")
    identified_gaps: List[str] = Field(description="Missing critical stack competencies or alignment mismatches")
    interview_suitability: bool = Field(description="Rigid logic flag for automated shortlisting routing")
```

---
💡 *Maintained by [Malik Nouman Maqsood](https://github.com)*
