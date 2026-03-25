# 🌦️ Weather Data Pipeline

A complete **ETL (Extract-Transform-Load) Data Pipeline** built with Python that collects weather data from multiple Indian cities, processes it, stores it in a database, and displays it on an interactive monitoring dashboard.

> Built as a portfolio project for the **Associate Data Engineer** role.

---

## 🏗️ Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   EXTRACT        │     │   TRANSFORM      │     │   LOAD           │
│                  │     │                  │     │                  │
│  Weather API  ───┼────►│  Clean & Validate├────►│  SQLite Database │
│  (or Demo data)  │     │  Normalize Data  │     │  weather_data.db │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                          │
                                                          ▼
                                                  ┌──────────────────┐
                                                  │   DASHBOARD      │
                                                  │                  │
                                                  │  Flask API ──► HTML/JS │
                                                  │  Charts & Stats  │
                                                  └──────────────────┘
```

## ✨ Features

- 📊 **ETL Pipeline** — Automated Extract → Transform → Load workflow
- 🌡️ **Multi-City Monitoring** — Tracks weather for 8 Indian cities
- 📉 **Interactive Dashboard** — Real-time charts and statistics
- 🧪 **Demo Mode** — Works without API key using sample data
- 📝 **Comprehensive Logging** — Pipeline activity tracking
- ⏰ **Auto-Scheduling** — Runs at configurable intervals
- ✅ **Unit Tested** — Automated tests for data validation

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Core programming language |
| **SQLite** | Lightweight database (no server needed) |
| **Flask** | API server for the dashboard |
| **HTML/CSS/JS** | Interactive monitoring dashboard |
| **requests** | HTTP client for API calls |
| **schedule** | Pipeline scheduling |
| **pytest** | Unit testing |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd "Data Engineer"
pip install -r requirements.txt
```

### 2. Run the Pipeline (Demo Mode — No API Key Needed!)
```bash
python pipeline.py --demo
```

### 3. Run with Real Data (Optional)
```bash
# Set your free API key from https://openweathermap.org/api
set WEATHER_API_KEY=your_api_key_here
python pipeline.py
```

### 4. View the Dashboard
```bash
python api_server.py
# Open http://localhost:5050 in your browser
```

### 5. Run Tests
```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
Data Engineer/
├── config.py              # Settings & configuration
├── pipeline.py            # Main pipeline orchestrator
├── api_server.py          # Flask API for dashboard
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
├── etl/                   # ETL modules
│   ├── __init__.py
│   ├── extract.py         # Data extraction (API/demo)
│   ├── transform.py       # Data cleaning & validation
│   └── load.py            # Database operations
│
├── dashboard/             # Frontend dashboard
│   ├── index.html         # Dashboard UI
│   ├── style.css          # Styling
│   └── app.js             # Charts & interactivity
│
├── tests/                 # Unit tests
│   └── test_transform.py  # Transform module tests
│
├── weather_data.db        # SQLite database (auto-created)
└── pipeline.log           # Activity log (auto-created)
```

## 📚 Key Concepts Demonstrated

- **ETL Pipeline Design** — Industry-standard data engineering pattern
- **API Integration** — RESTful API consumption with error handling
- **Data Validation** — Cleaning, null handling, type checking
- **Database Design** — Schema creation, UPSERT operations
- **Error Handling** — Try/except with logging and retry logic
- **Scheduling** — Automated pipeline execution
- **Full-Stack Skills** — Python backend + HTML/CSS/JS frontend
- **Testing** — Unit tests with pytest
- **Configuration Management** — Separated config from code

## 📝 License

This project is for educational and portfolio purposes.
