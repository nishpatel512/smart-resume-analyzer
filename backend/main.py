from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import get_connection
from datetime import datetime
import os
from pyresparser import ResumeParser
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

UPLOAD_FOLDER = 'uploaded_resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    filename = f'{uuid.uuid4()}_{file.filename}'

    # 1. Save uploaded file
    file_loc = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_loc, "wb") as f:
        f.write(await file.read())

    # 2. Extract data using parser
    try:
        data = ResumeParser(file_loc).get_extracted_data()
    except Exception as e:
        os.remove(file_loc)
        return {"error": f"Failed to parse resume: {str(e)}"}
    
    # 3. Extract data from resume
    name = data.get("name")
    email = data.get("email")
    mobile = data.get("mobile_number")
    skills = ", ".join(data.get("skills", [])) if data.get("skills") else None
    education = ", ".join(data.get("education", [])) if data.get("education") else None

    with open(file_loc, "rb") as f:
        file_data = f.read()

    # 4. Insert into DB
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO resumes (filename, uploaded_at, file_data, name, email, mobile_number, skills, education)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (filename, datetime.now(), file_data, name, email, mobile, skills, education))
    resume_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    os.remove(file_loc)
    return {
        "message": f"{filename} uploaded and parsed successfully",
        "resume_id": resume_id,
        "parsed_data": {
            "name": name,
            "email": email,
            "mobile": mobile,
            "skills": skills,
            "education": education
        }
    }

@app.get("/match-jobs/{resume_id}")
def match_jobs(resume_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT skills FROM resumes WHERE id = %s", (resume_id,))
    result = cur.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume_skills = result[0]
    if not resume_skills:
        raise HTTPException(status_code=400, detail="No skills found in resume")
    
    resume_skill_set = set([skill.strip().lower() for skill in resume_skills.split(',')])

    cur.execute("SELECT id, title, company, description, required_skills FROM jobs")
    jobs = cur.fetchall()

    matched_jobs = []
    for job in jobs:
        job_id, title, company, description, required_skills = job
        job_skill_set = set([skill.strip().lower() for skill in required_skills.split(',')])
        matched_skills = resume_skill_set.intersection(job_skill_set)
        match_percent = (len(matched_skills) / len(job_skill_set)) * 100 if job_skill_set else 0
        matched_jobs.append({
            "job_id": job_id,
            "title": title,
            "company": company,
            "description": description,
            "required_skills": list(job_skill_set),
            "match_percent": round(match_percent, 2),
            "matched_skills": list(matched_skills)
        })

    # Sort by match percent descending
    matched_jobs.sort(key=lambda x: x["match_percent"], reverse=True)

    cur.close()
    conn.close()

    return {"matched_jobs": matched_jobs}



