# 📘 Lecture to Exam Notes AI

Turn university lectures into high-scoring, exam-oriented notes, MCQs, and revision guides in seconds using AI.

## ✨ Features

- **Multi-format Support**: Upload lectures as text (.txt), documents (.pdf), or audio recordings (.mp3).
- **Exam-Ready Notes**: Automatically extracts key concepts, definitions, and important questions.
- **Auto-Generated MCQs**: Creates university-standard multiple-choice questions for practice.
- **Last-Day Revision**: Generates ultra-concise bullet points for quick review.
- **Export to Word**: Download your generated notes as a professional .docx file.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key

### 2. Setup

1. **Clone or download** this repository.
2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure API Key**:
   Create a `.streamlit/secrets.toml` file (or add to your Streamlit cloud secrets) with:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

### 3. Running the App

Always ensure your virtual environment is active before running:
```bash
source .venv/bin/activate
streamlit run app.py
```

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Engine**: [Google Gemini 2.0 Flash](https://ai.google.dev/)
- **Document Handling**: [python-docx](https://python-docx.readthedocs.io/)
- **Backend API**: [google-genai](https://pypi.org/project/google-genai/)

---
*Created for students to study smarter, not harder.*
