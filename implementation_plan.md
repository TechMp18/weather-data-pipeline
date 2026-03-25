# Resume Tailoring + Data Engineering Portfolio Project

## Goal

Two deliverables for the Highspring India — Associate Data Engineer campus placement:

1. **Tailored Resume** (HTML → PDF) — Highlighting existing projects and skills mapped to the JD
2. **Data Engineering Portfolio Project** — A real ETL data pipeline built in the `Data Engineer` workspace folder

---

## Part 1: Resume (Tailored HTML Resume)

We'll create a clean, ATS-friendly HTML resume that the user can open in the browser and print to PDF.

### Skills & Projects Mapping to JD

| JD Requirement | User's Evidence |
|---|---|
| Python | AI Resume Analyser backend (FastAPI), CCFD fraud detection, FresherTechJobs scraper, 6G simulation |
| Data pipelines / ETL | **New portfolio project** (below) |
| Unix/Linux | Will list as skill |
| HTML/CSS/JavaScript | React frontends (Resume Analyser, FresherTechJobs), reminder-app |
| Analytical & debugging | CCFD data exploration, 6G DQN simulation |
| Communication & documentation | Project walkthroughs, README docs |
| Zero-defect / production code | GitHub projects |

### File

#### [NEW] [resume.html](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/resume.html)

A clean, single-file HTML resume with:
- Professional dark/light theme, ATS-friendly formatting
- Sections: Summary, Education, Skills, Projects, Certifications
- Projects described with **action verbs** and **quantified impact**
- Skills grouped by category matching Highspring's requirements

> [!IMPORTANT]
> The user needs to fill in personal details (name, email, phone, college, GPA, graduation year). I'll use placeholder markers like `[YOUR NAME]` etc.

---

## Part 2: Data Engineering Portfolio Project

A complete, interview-ready ETL pipeline project that directly demonstrates the skills Highspring is hiring for.

### Project: **Real-Time Weather Data Pipeline**

**Why this project?** It covers every major JD requirement:
- ✅ Python-based ETL/ELT pipeline
- ✅ Data extraction from external APIs (free OpenWeatherMap API)
- ✅ Data transformation and cleaning
- ✅ Data loading into SQLite database
- ✅ Automated scheduling & error handling
- ✅ Monitoring dashboard (HTML/CSS/JS)
- ✅ Logging, documentation, and resilient design
- ✅ Can run on Unix/Linux

### Architecture

```
[Weather API] → [Extract (Python)] → [Transform (Python)] → [Load (SQLite)]
                                                                    ↓
                                                        [Dashboard (HTML/JS)]
```

### Files to Create

#### [NEW] [README.md](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/README.md)
Project overview, setup instructions, architecture diagram, tech stack

#### [NEW] [requirements.txt](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/requirements.txt)
Python dependencies: `requests`, `schedule`, `sqlite3` (built-in)

#### [NEW] [config.py](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/config.py)
Configuration: API key, database path, cities list, schedule interval

#### [NEW] [etl/extract.py](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/etl/extract.py)
Fetches weather data from OpenWeatherMap API with error handling & retries

#### [NEW] [etl/transform.py](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/etl/transform.py)
Cleans, normalizes, and validates raw API data; handles missing values

#### [NEW] [etl/load.py](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/etl/load.py)
Creates SQLite tables and inserts transformed data with upsert logic

#### [NEW] [pipeline.py](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/pipeline.py)
Main orchestrator — runs Extract → Transform → Load with logging and error handling

#### [NEW] [scheduler.py](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/scheduler.py)
Schedules the pipeline to run at configurable intervals using the `schedule` library

#### [NEW] [dashboard/index.html](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/dashboard/index.html)
Interactive monitoring dashboard showing pipeline status, data stats, and weather charts

#### [NEW] [dashboard/app.js](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/dashboard/app.js)
JavaScript to fetch data from a lightweight API endpoint and render charts

#### [NEW] [dashboard/style.css](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/dashboard/style.css)
Dark-themed, professional dashboard styling

#### [NEW] [api_server.py](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/api_server.py)
Lightweight Flask/HTTP server to serve dashboard data from SQLite

#### [NEW] [tests/test_transform.py](file:///c:/Users/mukul/Downloads/Projects/Data%20Engineer/tests/test_transform.py)
Unit tests for the transform module

---

## User Review Required

> [!IMPORTANT]
> **Personal Details**: The resume will use placeholders (`[YOUR NAME]`, `[YOUR EMAIL]`, etc.) that you'll need to replace with your real information.

> [!IMPORTANT]
> **API Key**: The weather pipeline uses the free [OpenWeatherMap API](https://openweathermap.org/api). You'll need to sign up (free) and paste your API key into `config.py`. I can also make the project work with a mock/demo mode if you prefer.

> [!WARNING]
> **Education & GPA**: Please share your degree name, college, and expected graduation year so I can include accurate info in the resume — or you can edit the placeholders after.

---

## Verification Plan

### Automated Tests
1. **Unit tests for transform module:**
   ```bash
   cd c:\Users\mukul\Downloads\Projects\Data Engineer
   python -m pytest tests/test_transform.py -v
   ```

2. **Pipeline dry run (with mock data):**
   ```bash
   python pipeline.py --demo
   ```
   This will use sample data instead of the API, confirming the full E→T→L flow works.

### Manual Verification
1. **Resume**: Open `resume.html` in the browser and verify it renders correctly, then print to PDF
2. **Dashboard**: Run `python api_server.py` and open `http://localhost:5050` — check that charts and data render
3. **Pipeline**: Run `python pipeline.py` and verify data appears in the SQLite database
