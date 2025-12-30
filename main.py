from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI(title="Resume Builder API")

DB = {}

class Experience(BaseModel):
    company: str
    role: str
    duration: str
    details: str

class Education(BaseModel):
    degree: str
    year: str
    college: str

class Resume(BaseModel):
    personal: dict
    summary: str
    skills: List[str]
    experience: List[Experience]
    education: List[Education]
    theme: str = "modern"

@app.post("/api/resumes")
def create_resume(resume: Resume):
    resume_id = str(uuid.uuid4())[:8]
    DB[resume_id] = resume
    return {"resume_id": resume_id, "message": "Resume created"}

@app.get("/api/resumes/{resume_id}")
def get_resume(resume_id: str):
    if resume_id not in DB:
        raise HTTPException(404, "Resume not found")
    return DB[resume_id]

@app.get("/api/resumes/{resume_id}/html", response_class=HTMLResponse)
def render_resume(resume_id: str):
    if resume_id not in DB:
        raise HTTPException(404, "Resume not found")

    r = DB[resume_id]
    html = f"""
    <html>
      <body style="font-family:Arial">
        <h1>{r.personal['name']}</h1>
        <h3>{r.personal['title']}</h3>
        <p>{r.summary}</p>
        <h4>Skills</h4>
        <ul>{"".join(f"<li>{s}</li>" for s in r.skills)}</ul>
      </body>
    </html>
    """
    return html

@app.get("/api/themes")
def themes():
    return ["modern", "classic", "minimal", "dark"]
