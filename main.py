from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from docx import Document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def extract_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(content)
    
    if file.filename.endswith(".pdf"):
        text = extract_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_docx(file_path)
    else:
        return {"error": "Unsupported file type"}

    # Simple parsing logic (can improve later)
    lines = text.split("\n")
    resume_json = {
        "name": lines[0] if lines else "",
        "title": lines[1] if len(lines) > 1 else "",
        "contact": {"Email": "", "Phone": ""},
        "skills": [],
        "experience": [],
        "education": []
    }

    # You can add NLP later to detect sections automatically

    return {"text": text, "parsed_resume": resume_json}
