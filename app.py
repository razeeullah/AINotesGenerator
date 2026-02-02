import streamlit as st
from docx import Document
from io import BytesIO
from google import genai

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Lecture to Exam Notes AI", layout="centered")

st.title("📘 Lecture to Exam Notes AI")
st.write("Turn lectures into **exam-ready notes** in seconds.")

# ---------------------------
# PROMPTS
# ---------------------------

SYSTEM_PROMPT = """You are an experienced university professor and examiner.

Your task is to convert lecture content into HIGH-SCORING, EXAM-ORIENTED NOTES.

Focus on:
- Frequently asked exam topics
- Clear definitions
- Short and long questions
- Important headings
- Simple language for average students

Ignore unnecessary stories, jokes, repetition, and filler content.

The output must be clean, structured, and easy to revise before exams.

"""

TEXT_PROMPT = """
Convert the following lecture content into EXAM-ORIENTED NOTES.

Rules:
1. Use clear headings and subheadings
2. Highlight important terms and definitions
3. Focus on what is most likely to be asked in exams
4. Keep explanations concise but complete
5. Use bullet points where possible
6. Do NOT add information not present in the lecture

Output Format:

Title: <Topic Name>

1. Important Concepts
- …

2. Key Definitions
- Term: Definition

3. Exam-Important Points
- …

4. Short Questions (2–3 marks)
- …

5. Long Questions (5–10 marks)
- …

Lecture Content:
{content}

"""

AUDIO_PROMPT = """The following text is a transcript of a university lecture.

Convert it into clean, structured, EXAM-READY NOTES.

Instructions:
- Remove spoken fillers (uh, um, repetition)
- Organize content logically
- Emphasize exam-important ideas
- Use simple student-friendly language

Output Format:

Title: <Lecture Topic>

1. Core Topics Explained
- …

2. Definitions & Terminology
- …

3. Important Exam Notes
- …

4. Short Questions
- …

5. Long Questions
- …

Lecture Transcript:
{content}

"""

MCQ_PROMPT = """Based ONLY on the lecture content below, generate EXAM-STYLE MCQs.

Rules:
- Each MCQ must have 4 options
- Clearly mark the correct answer
- Questions should match university exam difficulty
- Do NOT add information outside the content

Output Format:

Q1. Question?
A)
B)
C)
D)
Correct Answer: X

Lecture Content:
{content}

"""

REVISION_PROMPT = """Create LAST-DAY REVISION NOTES from the content below.

Rules:
- Extremely concise
- Bullet points only
- No explanation longer than 1–2 lines
- Focus only on high-yield exam points

Output Format:

🔹 Key Points
- …

🔹 Definitions
- …

🔹 Formulas / Facts
- …

🔹 Common Exam Questions
- …

Content:
{content}

"""

CS_SUBJECT_PROMPT = """
Explain concepts with technical accuracy but simple language.
Use examples only when they improve understanding.
Avoid unnecessary theory.

"""

THEORY_SUBJECT_PROMPT = """Focus on definitions, structured explanations, and answers suitable for written exams.
Use formal academic tone.
.
"""

# ---------------------------
# UI INPUTS
# ---------------------------

uploaded_file = st.file_uploader(
    "Upload Lecture File (PDF / TXT / MP3)",
    type=["txt", "pdf", "mp3"]
)

subject = st.selectbox("Select Subject", ["Computer Science", "Theory"])

output_type = st.multiselect(
    "Select Output",
    ["Exam Notes", "MCQs", "Last-Day Revision"]
)

generate_btn = st.button("🚀 Generate")

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def create_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Gemini Configuration
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please add GEMINI_API_KEY to your Streamlit secrets.")
    client = None

def call_gemini(system_prompt, user_prompt):
    if client is None:
        return "Error: Gemini API Key not found."
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{system_prompt}\n\n{user_prompt}"
        )
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

# ---------------------------
# MAIN LOGIC
# ---------------------------

if generate_btn and uploaded_file:
    content = uploaded_file.read().decode("utf-8", errors="ignore")

    # 1️⃣ Subject Control Prompt
    subject_prompt = CS_SUBJECT_PROMPT if subject == "Computer Science" else THEORY_SUBJECT_PROMPT

    final_output = ""

    # 2️⃣ Exam Notes Prompt
    if "Exam Notes" in output_type:
        user_prompt = TEXT_PROMPT.format(content=content) + subject_prompt
        final_output += call_gemini(SYSTEM_PROMPT, user_prompt) + "\n\n"

    # 3️⃣ MCQs Prompt
    if "MCQs" in output_type:
        user_prompt = MCQ_PROMPT.format(content=content)
        final_output += call_gemini(SYSTEM_PROMPT, user_prompt) + "\n\n"

    # 4️⃣ Revision Prompt
    if "Last-Day Revision" in output_type:
        user_prompt = REVISION_PROMPT.format(content=content)
        final_output += call_gemini(SYSTEM_PROMPT, user_prompt)

    # ---------------------------
    # OUTPUT
    # ---------------------------
    st.subheader("📄 Generated Output")
    st.text_area("Result", final_output, height=300)

    docx_file = create_docx(final_output)

    st.download_button(
        "⬇ Download as DOCX",
        data=docx_file,
        file_name="exam_notes.docx"
    )
