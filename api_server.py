# ============================================================================
# api_server.py — Dashboard API Server (Dashboard ke liye Data Serve Karna)
# ============================================================================
#
# 🎯 YEH FILE KYA HAI?
# Yeh ek chhota sa web server hai jo database se data nikal ke dashboard ko
# deta hai. Dashboard (HTML/JS) is server se data maangta hai aur charts banata hai.
#
# 📚 CONCEPT: Flask
# Flask Python ka sabse simple web framework hai.
# Express.js (Node.js) jaisa hai — chhote servers ke liye perfect.
# Sirf kuch lines mein ek API bana sakte ho!
#
# 📚 CONCEPT: REST API
# REST ek pattern hai APIs banane ka:
# GET /api/records → records de do
# GET /api/summary → summary de do
# POST /api/run → pipeline chalao
#
# Is file mein hum sikhhenge:
# 1. Flask se API kaise banate hain
# 2. JSON response kaise bhejte hain
# 3. Static files serve karna (HTML/CSS/JS)
# 4. CORS kya hai
# ============================================================================

import os
import logging
from flask import Flask, jsonify, send_from_directory
from etl.load import get_latest_records, get_city_summary, get_pipeline_stats
from pipeline import run_pipeline, setup_logging

# ---------------------------------------------------------------------------
# 📝 Logging Setup
# ---------------------------------------------------------------------------
setup_logging()
logger = logging.getLogger("api_server")

# ---------------------------------------------------------------------------
# 🏗️ Flask App Banana
# ---------------------------------------------------------------------------

app = Flask(__name__)
# ☝️ Flask(__name__) — ek naya Flask app banata hai
# __name__ se Flask ko pata chalta hai ki files kahaan hain

# Dashboard files ka folder path
DASHBOARD_DIR = os.path.join(os.path.dirname(__file__), "dashboard")
# ☝️ Dashboard ke HTML/CSS/JS files "dashboard" folder mein hain

# ---------------------------------------------------------------------------
# 🌐 Routes (URLs) Define Karna
# ---------------------------------------------------------------------------
# Route kya hai? Jaise GPS mein route hota hai, waise yahan URL ka path hai.
# Jab koi /api/records pe jaayega toh us URL ka function chalega.
# ---------------------------------------------------------------------------


@app.route("/")
def serve_dashboard():
    """
    🏠 Home Page — Dashboard HTML serve karo
    
    Jab koi http://localhost:5050/ open kare toh dashboard dikhe.
    
    📚 CONCEPT: Static File Serving
    Flask "static files" (HTML, CSS, JS) serve kar sakta hai.
    send_from_directory() — ek folder se specific file bhejta hai.
    """
    return send_from_directory(DASHBOARD_DIR, "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    """
    📁 Static Files — CSS, JS files serve karo
    
    <path:filename> ek "variable route" hai:
    /style.css → filename = "style.css"
    /app.js → filename = "app.js"
    """
    return send_from_directory(DASHBOARD_DIR, filename)


@app.route("/api/records")
def api_records():
    """
    📊 API: Latest Weather Records
    
    URL: GET http://localhost:5050/api/records
    
    Returns: JSON array of latest 100 weather records
    
    📚 CONCEPT: JSON Response
    jsonify() Python dict/list ko JSON string mein convert karta hai
    aur sahi headers set karta hai (Content-Type: application/json).
    """
    records = get_latest_records(limit=100)
    return jsonify(records)
    # ☝️ jsonify() — Python object → JSON response
    # Browser ko milega: [{"city": "Delhi", "temperature": 35.2, ...}, ...]


@app.route("/api/summary")
def api_summary():
    """
    📈 API: City-wise Summary
    
    URL: GET http://localhost:5050/api/summary
    
    Returns: JSON with city summaries (avg temp, min, max, count)
    """
    summary = get_city_summary()
    return jsonify(summary)


@app.route("/api/stats")
def api_stats():
    """
    📉 API: Pipeline Statistics
    
    URL: GET http://localhost:5050/api/stats
    
    Returns: JSON with overall pipeline stats
    """
    stats = get_pipeline_stats()
    return jsonify(stats)


@app.route("/api/run", methods=["POST"])
def api_run_pipeline():
    """
    🚀 API: Pipeline Manually Chalao
    
    URL: POST http://localhost:5050/api/run
    
    Dashboard pe "Run Pipeline" button click karoge toh ye chalega.
    
    📚 CONCEPT: POST vs GET
    GET = data MAANGNA (padna)
    POST = data BHEEJNA (kuch karna)
    Pipeline chalana ek "action" hai, isliye POST use kar rahe hain.
    """
    logger.info("🚀 Pipeline triggered from dashboard!")
    
    try:
        result = run_pipeline(demo_mode=True)
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        logger.error(f"❌ Pipeline run failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
        # ☝️ 500 = HTTP status code for Internal Server Error


# ============================================================================
# 🚀 Server Start
# ============================================================================

if __name__ == "__main__":
    # Render.com PORT environment variable use karta hai
    port = int(os.environ.get("PORT", 5050))
    
    print("\n" + "=" * 50)
    print("Weather Pipeline Dashboard Server")
    print("=" * 50)
    print(f"Open in browser: http://localhost:{port}")
    print(f"API endpoints:")
    print(f"   GET  /api/records  — Latest weather data")
    print(f"   GET  /api/summary  — City summaries")
    print(f"   GET  /api/stats    — Pipeline statistics")
    print(f"   POST /api/run      — Run pipeline manually")
    print("=" * 50 + "\n")
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG", "true").lower() == "true"
        # Production mein FLASK_DEBUG set nahi hoga, toh debug=False rahega
    )

