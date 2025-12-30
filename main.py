from fastapi import FastAPI, UploadFile, File
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

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(content)

    if file.filename.endswith(".pdf"):
        text = extract_pdf(temp_path)
    elif file.filename.endswith(".docx"):
        text = extract_docx(temp_path)
    else:
        return {"error": "Unsupported file type"}

    lines = text.split("\n")
    parsed = {
        "name": lines[0] if lines else "",
        "title": lines[1] if len(lines) > 1 else "",
        "contact": {},
        "skills": [],
        "experience": [],
        "education": []
    }

    return {"text": text, "parsed_resume": parsed}

def extract_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])
