# AI Campus Placement Agent

An AI-powered multi-agent web application that helps students prepare for campus placements. It analyzes resumes, compares them with job descriptions, identifies skill gaps, creates personalized learning roadmaps, and conducts AI-powered mock interviews.

Built as a capstone project for the **Kaggle AI Agents Intensive Course**.

---

## The Problem

Students preparing for placements often switch between multiple tools for resume reviews, ATS checks, interview preparation, and learning resources. This makes the preparation process fragmented and time-consuming.

AI Campus Placement Agent brings these tasks together into one intelligent assistant.

---

## Why This Is an AI Agent System

Instead of behaving like a traditional chatbot, the application uses a multi-agent architecture.

A central **Coordinator Agent** manages the workflow and delegates tasks to specialized agents.

- **Resume Agent** – Reviews resumes, calculates ATS score, and provides suggestions.
- **Job Match Agent** – Compares resumes with job descriptions and calculates compatibility.
- **Skill Gap Agent** – Identifies missing skills and recommends what to learn next.
- **Roadmap Agent** – Creates a personalized 6-week placement preparation plan.
- **Interview Agent** – Generates mock interview questions and evaluates user responses.

The Coordinator combines the outputs of these agents into a single placement report.

---

## System Workflow

```text
Student

↓

Upload Resume
+ Job Description
+ Select Company

↓

Coordinator Agent

↓

Single Gemini API Request

↓

Structured JSON Response

↓

Resume Agent
Job Match Agent
Skill Gap Agent
Roadmap Agent
Interview Agent

↓

Dashboard + Placement Report
```

---

## Features

- Resume analysis with ATS score
- Job description matching
- Skill gap analysis
- Personalized 6-week learning roadmap
- AI-powered mock interview
- Company-specific interview preparation
- Downloadable placement report (PDF)

---

## Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap 5

### Backend

- Python
- Flask
- SQLite

### AI

- Google Gemini API
- Google Gen AI SDK (`google-genai`)

### Libraries

- PyPDF2
- ReportLab
- python-dotenv

---

## Project Structure

```text
AI-Campus-Placement-Agent/

│── app.py
│── config.py
│── prompts.py
│── requirements.txt
│── README.md

├── agents/
│   ├── coordinator.py
│   ├── resume_agent.py
│   ├── job_match_agent.py
│   ├── skill_gap_agent.py
│   ├── roadmap_agent.py
│   └── interview_agent.py

├── data/
│   └── companies.json

├── templates/

├── static/

├── utils/

├── uploads/

└── reports/
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/deepikagandla7456/ai-campus-placement-agent.git

cd ai-campus-placement-agent
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

macOS/Linux

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
FLASK_SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_gemini_api_key
```

### Run the application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## Demo

1. Upload your resume.
2. Paste a job description (optional).
3. Select a target company.
4. Click **Analyze**.
5. Review ATS score, job match, skill gaps, and roadmap.
6. Start the mock interview.
7. Download the final placement report.

---

## Future Improvements

- GitHub profile analysis
- LinkedIn profile review
- Voice-based mock interviews
- LeetCode progress tracking
- Resume version comparison
- Google Calendar integration
- Internship recommendations
- Recruiter email generation

---

## License

This project is licensed under the MIT License.



