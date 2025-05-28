# Smart Resume Analyzer

A full-stack application that lets users upload resumes and intelligently parses, analyzes, and visualizes resume content. It identifies skill gaps, compares with job requirements, and gives tailored improvement suggestions using NLP.

---

## 🧰 Tech Stack

- **Frontend**: React.js (or HTML/CSS/JS)
- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL (or MongoDB)
- **Authentication**: OAuth 2.0
- **Containerization**: Docker
- **Orchestration**: Kubernetes (optional via Minikube)
- **Version Control**: Git + GitHub

---

## 🚀 Features

- Upload and parse resumes (PDF/DOCX)
- NLP-driven skill extraction and comparison
- Custom skill gap analysis reports
- User authentication and saved sessions
- Dockerized microservices

---

## 📦 Local Development

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload