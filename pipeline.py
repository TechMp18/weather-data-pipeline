# ============================================================================
# pipeline.py — Pipeline Orchestrator (Sab kuch ek saath chalane wala)
# ============================================================================
#
# 🎯 YEH FILE KYA HAI?
# Yeh file "conductor" hai — jaise orchestra mein conductor sab musicians ko
# coordinate karta hai, waise ye file Extract, Transform, aur Load ko ek
# sequence mein chalata hai.
#
# Flow: Extract → Transform → Load (E → T → L)
#
# 📚 CONCEPT: Pipeline Orchestration
# Real companies mein pipelines ko tools se orchestrate karte hain:
# - Apache Airflow (sabse popular)
# - Luigi
# - Prefect
# Hum simple Python se kar rahe hain, par concept same hai!
#
# Is file mein hum sikhhenge:
# 1. Pipeline pattern (steps ko sequence mein chalana)
# 2. Logging setup (file + console mein logs likhna)
# 3. Command line arguments (--demo flag)
# 4. Error handling at pipeline level
# 5. Execution time tracking
# ============================================================================

import sys       # System functions (command line args, exit)
import io        # Input/Output streams (encoding fix ke liye)
import logging   # Logging framework
import time      # Time tracking
from datetime import datetime

# Apne ETL modules import karo
from etl.extract import fetch_weather_data
from etl.transform import transform_weather_data
from etl.load import load_to_database
from config import LOG_FILE, DEMO_MODE

# ---------------------------------------------------------------------------
# 🔧 WINDOWS ENCODING FIX
# ---------------------------------------------------------------------------
# Windows ka default console encoding "cp1252" hai jo emojis support nahi karta.
# Hum stdout ko UTF-8 mein wrap kar rahe hain taaki emojis crash na karein.
# errors="replace" matlab — agar koi character print nahi ho sakta toh "?" daal do
# (crash mat karo). Ye production mein bhi best practice hai!
# ---------------------------------------------------------------------------
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def setup_logging():
    """
    Logging Setup
    
    Logs do jagah jaayenge:
    1. Console (terminal pe dikhenge) — developer ke liye
    2. File (pipeline.log mein save honge) — baad mein dekhne ke liye
    
    CONCEPT: Log Handlers
    Handler batata hai ki log kahaan jaaye.
    - StreamHandler -> Console (terminal)
    - FileHandler -> File mein save
    Hum DONO use kar rahe hain — same log dono jagah jaayega!
    """
    
    # Root logger set karo
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # INFO level matlab INFO + WARNING + ERROR + CRITICAL sab record honge
    # DEBUG nahi hoga (kyunki DEBUG < INFO)
    
    # Agar logger ke paas pehle se handlers hain toh duplicate na banao
    if logger.handlers:
        return logger
    
    # Log message ka format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # %(asctime)s — date-time
    # %(levelname)-8s — level naam (INFO, ERROR) 8 characters mein
    # %(name)s — konsa module hai (etl.extract, etl.load)
    # %(message)s — actual message
    
    # Handler 1: Console (UTF-8 wrapped stdout use karenge)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler 2: File
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def run_pipeline(demo_mode=None):
    """
    🚀 MAIN PIPELINE FUNCTION
    
    Yeh function poora ETL pipeline chalata hai:
    Step 1: Extract (data nikalo)
    Step 2: Transform (data saaf karo)
    Step 3: Load (database mein dalo)
    
    Parameters:
        demo_mode (bool): True = fake data use karo, None = config se decide karo
    
    Returns:
        dict: Pipeline run ka summary
    
    📚 CONCEPT: Pipeline Summary/Report
    Production mein har pipeline run ke baad ek summary generate hota hai:
    - Kitne records extract hue?
    - Kitne transform pass hue?
    - Kitne database mein gaye?
    - Koi errors aayi?
    Ye "observability" kehlaata hai — pipeline ka health check!
    """
    
    pipeline_start = time.time()
    # ☝️ time.time() — current time seconds mein deta hai (epoch timestamp)
    # Baad mein end_time - start_time se total time nikal lenge
    
    logger = logging.getLogger("pipeline")
    
    logger.info("=" * 60)
    logger.info("🚀 WEATHER DATA PIPELINE — RUN STARTED")
    logger.info(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🧪 Mode: {'DEMO' if (demo_mode or DEMO_MODE) else 'LIVE'}")
    logger.info("=" * 60)
    
    summary = {
        "status": "started",
        "start_time": datetime.now().isoformat(),
        "extracted": 0,
        "transformed": 0,
        "loaded": 0,
        "errors": [],
    }
    
    try:
        # ═══════════════════════════════════════════════════════════
        # STEP 1: EXTRACT 📡
        # ═══════════════════════════════════════════════════════════
        logger.info("\n📡 STEP 1/3: EXTRACT")
        logger.info("-" * 40)
        
        raw_data = fetch_weather_data()
        summary["extracted"] = len(raw_data)
        
        if not raw_data:
            logger.error("❌ No data extracted! Pipeline stopping.")
            summary["status"] = "failed"
            summary["errors"].append("No data extracted")
            return summary
        
        logger.info(f"✅ Step 1 Complete: {len(raw_data)} records extracted\n")
        
        # ═══════════════════════════════════════════════════════════
        # STEP 2: TRANSFORM 🔄
        # ═══════════════════════════════════════════════════════════
        logger.info("🔄 STEP 2/3: TRANSFORM")
        logger.info("-" * 40)
        
        clean_data = transform_weather_data(raw_data)
        summary["transformed"] = len(clean_data)
        
        if not clean_data:
            logger.error("❌ All records rejected after transform! Pipeline stopping.")
            summary["status"] = "failed"
            summary["errors"].append("All records failed validation")
            return summary
        
        logger.info(f"✅ Step 2 Complete: {len(clean_data)} records validated\n")
        
        # ═══════════════════════════════════════════════════════════
        # STEP 3: LOAD 💾
        # ═══════════════════════════════════════════════════════════
        logger.info("💾 STEP 3/3: LOAD")
        logger.info("-" * 40)
        
        loaded_count = load_to_database(clean_data)
        summary["loaded"] = loaded_count
        
        logger.info(f"✅ Step 3 Complete: {loaded_count} records saved to database\n")
        
        # ═══════════════════════════════════════════════════════════
        # PIPELINE COMPLETE! 🎉
        # ═══════════════════════════════════════════════════════════
        pipeline_end = time.time()
        duration = round(pipeline_end - pipeline_start, 2)
        
        summary["status"] = "success"
        summary["duration_seconds"] = duration
        summary["end_time"] = datetime.now().isoformat()
        
        logger.info("=" * 60)
        logger.info("🎉 PIPELINE RUN COMPLETE!")
        logger.info(f"   📡 Extracted:   {summary['extracted']} records")
        logger.info(f"   🔄 Transformed: {summary['transformed']} records")
        logger.info(f"   💾 Loaded:      {summary['loaded']} records")
        logger.info(f"   ⏱️  Duration:    {duration} seconds")
        logger.info("=" * 60)
        
    except Exception as e:
        # Koi unexpected error aayi — poora pipeline fail
        logger.error(f"💥 PIPELINE CRASHED: {e}")
        summary["status"] = "crashed"
        summary["errors"].append(str(e))
        
        import traceback
        logger.error(traceback.format_exc())
        # ☝️ traceback — full error details print karta hai (debugging ke liye)
    
    return summary


# ============================================================================
# 🚀 ENTRY POINT — Jab tum "python pipeline.py" run karo
# ============================================================================
#
# 📚 CONCEPT: if __name__ == "__main__"
# Ye Python ka standard pattern hai:
# - Agar tum seedha "python pipeline.py" run karo → ye code chalega
# - Agar koi aur file "import pipeline" kare → ye code NAHI chalega
#
# 📚 CONCEPT: Command Line Arguments (sys.argv)
# Terminal mein: python pipeline.py --demo
# sys.argv = ["pipeline.py", "--demo"]
# sys.argv[0] = file name, baaki = arguments
# --demo flag se program ko batate hain ki demo mode use karo
# ============================================================================

if __name__ == "__main__":
    # Logging setup karo
    setup_logging()
    
    # Check if --demo flag diya hai
    demo_flag = "--demo" in sys.argv
    # ☝️ sys.argv mein command line ke saare arguments hote hain
    # "python pipeline.py --demo" mein sys.argv = ["pipeline.py", "--demo"]
    # "--demo" in sys.argv → True/False
    
    if demo_flag:
        # Force demo mode ON
        import config
        config.DEMO_MODE = True
        config.API_KEY = "demo"
    
    # Pipeline chalao!
    result = run_pipeline(demo_mode=demo_flag)
    
    # Exit code set karo
    if result["status"] == "success":
        print("\n✅ Pipeline finished successfully!")
        sys.exit(0)   # 0 = success (Unix convention)
    else:
        print(f"\n❌ Pipeline failed: {result.get('errors', [])}")
        sys.exit(1)   # 1 = failure
