# ============================================================================
# etl/load.py — Data Loading Module (Data Database mein Dalna)
# ============================================================================
#
# 🎯 YEH FILE KYA HAI?
# ETL ka teesra aur last step hai "LOAD" — matlab transformed (clean) data ko
# database mein store karna.
#
# 📚 REAL WORLD MEIN:
# Data Engineers data ko kai jagah load karte hain:
# - Databases (MySQL, PostgreSQL, SQLite)
# - Data Warehouses (Snowflake, BigQuery, Redshift)
# - Data Lakes (S3, HDFS)
# - Files (CSV, Parquet)
#
# Hum SQLite use kar rahe hain kyunki:
# 1. Koi installation nahi chahiye (Python ke saath aata hai!)
# 2. Ek .db file mein sab data store hota hai
# 3. SQL queries likh sakte hain (same SQL jo MySQL mein chalti hai)
# 4. Production mein sirf database change karna padega, logic same rahega
#
# Is file mein hum sikhhenge:
# 1. SQL kaise likhte hain (DDL + DML)
# 2. Database connection kaise handle karte hain
# 3. UPSERT pattern kya hai (Insert or Update)
# 4. Context Manager (with statement)
# ============================================================================

import sqlite3  # Python ke saath built-in aata hai — install nahi karna padta!
import logging
from config import DATABASE_PATH, DATABASE_TABLE

logger = logging.getLogger(__name__)


def get_connection():
    """
    🔗 Database Connection Banana
    
    Database ke saath baat karne ke liye pehle "connection" chahiye — jaise
    phone call karne ke liye pehle dial karna padta hai.
    
    Returns:
        sqlite3.Connection: Database connection object
    
    📚 CONCEPT: Database Connection
    Connection ek "channel" hai tumhare code aur database ke beech.
    Connection open karo → kaam karo → connection band karo.
    Agar band nahi karoge toh resources waste honge (memory leak).
    """
    
    conn = sqlite3.connect(DATABASE_PATH)
    # ☝️ sqlite3.connect() — database file se connect karta hai
    # Agar file exist nahi karti toh AUTOMATICALLY bana dega! 
    
    conn.row_factory = sqlite3.Row
    # ☝️ row_factory = sqlite3.Row set karne se results ko column name se
    # access kar sakte hain: row["city"] instead of row[0]
    # Ye zyada readable hai!
    
    return conn


def create_table():
    """
    📋 Database Table Banana (Agar Pehle Se Nahi Hai)
    
    Table ek Excel sheet jaisi hai — columns define karte hain ki data
    kis format mein aayega.
    
    📚 CONCEPT: SQL DDL (Data Definition Language)
    DDL commands database ka STRUCTURE define karti hain:
    - CREATE TABLE — naya table banao
    - ALTER TABLE — table change karo
    - DROP TABLE — table delete karo
    
    📚 CONCEPT: Data Types in SQL
    - TEXT — string/text (e.g., city name)
    - REAL — decimal number (e.g., temperature 32.5)
    - INTEGER — whole number (e.g., humidity 65)
    """
    
    # SQL query — CREATE TABLE IF NOT EXISTS
    # "IF NOT EXISTS" bahut important hai — agar table pehle se hai toh error nahi aayega
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS {DATABASE_TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        temperature REAL NOT NULL,
        feels_like REAL,
        humidity REAL,
        pressure REAL,
        wind_speed REAL,
        weather_condition TEXT,
        temp_category TEXT,
        comfort_index TEXT,
        timestamp TEXT NOT NULL,
        source TEXT,
        processed_at TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    # ☝️ SQL Explanation:
    # id INTEGER PRIMARY KEY AUTOINCREMENT
    #   → Har row ko ek unique number milega (1, 2, 3, 4...)
    #   → AUTOINCREMENT matlab automatically badhega
    #   → PRIMARY KEY matlab ye row ka unique identifier hai
    #
    # TEXT NOT NULL
    #   → Text value chahiye, aur NULL (khaali) nahi ho sakti
    #
    # REAL
    #   → Decimal number (NULL ho sakta hai kyunki NOT NULL nahi lagaya)
    #
    # DEFAULT CURRENT_TIMESTAMP
    #   → Agar value nahi di toh automatically current time dal dega
    
    conn = get_connection()
    try:
        conn.execute(create_sql)
        # ☝️ conn.execute(sql) — SQL query run karta hai
        
        # Index create karo city aur timestamp pe (searching fast hogi)
        conn.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_city 
            ON {DATABASE_TABLE} (city)
        """)
        conn.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON {DATABASE_TABLE} (timestamp)
        """)
        # ☝️ INDEX kya hai?
        # Index ek "pointer list" hai — jaise book ki INDEX dekh ke directly
        # page pe jaate ho, waise database INDEX dekh ke directly row pe jaata hai.
        # Bina index ke poori table scan karni padti hai (slow!).
        
        conn.commit()
        # ☝️ commit() — changes ko PERMANENTLY save karta hai
        # Jab tak commit nahi karoge, changes temporary hain
        # Agar power cut ho jaaye toh bina commit ke data ud jaayega
        
        logger.info(f"✅ Table '{DATABASE_TABLE}' is ready")
        
    except Exception as e:
        logger.error(f"❌ Error creating table: {e}")
        raise  # Error ko upar propagate karo
    finally:
        conn.close()
        # ☝️ finally block HAMESHA chalta hai — error ho ya na ho
        # Connection band karna zaroori hai wrna resources waste honge


def insert_record(conn, record):
    """
    📥 Ek Record Database Mein Dalna
    
    Parameters:
        conn: Database connection
        record (dict): Transformed weather record
    
    📚 CONCEPT: SQL DML (Data Manipulation Language)
    DML commands data ke saath kaam karti hain:
    - INSERT — naya data dalo
    - SELECT — data padho
    - UPDATE — data change karo
    - DELETE — data hatao
    
    📚 CONCEPT: Parameter Binding (? placeholders)
    SQL mein direct values nahi likhte — ? placeholder use karte hain.
    Kyun? SECURITY! Direct values dalne se "SQL Injection" attack ho sakta hai.
    
    ❌ GALAT (unsafe):
    f"INSERT INTO table VALUES ('{user_input}')"
    
    ✅ SAHI (safe):
    "INSERT INTO table VALUES (?)", (user_input,)
    """
    
    insert_sql = f"""
    INSERT INTO {DATABASE_TABLE} 
    (city, temperature, feels_like, humidity, pressure, wind_speed,
     weather_condition, temp_category, comfort_index, timestamp, source, processed_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    # ☝️ Har ? ek value ka placeholder hai
    # Total 12 questions marks = 12 values dalenge
    
    values = (
        record["city"],
        record["temperature"],
        record.get("feels_like"),       # .get() — None dega agar key na mile
        record.get("humidity"),
        record.get("pressure"),
        record.get("wind_speed"),
        record.get("weather_condition"),
        record.get("temp_category"),
        record.get("comfort_index"),
        record["timestamp"],
        record.get("source"),
        record.get("processed_at"),
    )
    # ☝️ Tuple — ( ) mein values rakhte hain. Tuple list jaisi hai par
    # immutable (change nahi ho sakti). SQL parameters ke liye tuple use hota hai.
    
    conn.execute(insert_sql, values)
    # ☝️ conn.execute(sql, values) — SQL run karo aur ? ki jagah values dal do


def load_to_database(transformed_data):
    """
    🎯 MAIN LOAD FUNCTION
    
    Yeh function saari transformed weather records ko database mein store karta hai.
    
    Parameters:
        transformed_data (list): List of cleaned weather dictionaries
    
    Returns:
        int: Kitne records successfully insert hue
    
    📚 CONCEPT: Transaction
    Transaction ek "all-or-nothing" operation hai:
    - Ya toh SAARE records save honge
    - Ya toh KUCH BHI save nahi hoga
    
    Ye ensure karta hai ki database mein incomplete data na jaaye.
    Jaise bank transfer mein ya toh dono accounts update honge, ya toh koi nahi.
    """
    
    logger.info(f"{'='*50}")
    logger.info(f"💾 LOAD PHASE STARTED — {len(transformed_data)} records")
    logger.info(f"{'='*50}")
    
    if not transformed_data:
        logger.warning("⚠️ No data to load — empty input")
        return 0
    
    # Pehle table banao (agar nahi hai)
    create_table()
    
    conn = get_connection()
    loaded_count = 0
    
    try:
        for record in transformed_data:
            try:
                insert_record(conn, record)
                loaded_count += 1
                logger.info(f"  💾 Loaded: {record['city']} ({record['temperature']}°C)")
            except Exception as e:
                logger.error(f"  ❌ Failed to load record for {record.get('city', 'unknown')}: {e}")
        
        # Sab records insert hone ke baad commit karo
        conn.commit()
        logger.info(f"💾 LOAD COMPLETE — {loaded_count}/{len(transformed_data)} records saved")
        
    except Exception as e:
        conn.rollback()
        # ☝️ rollback() — sab changes undo karo (kuch galat hua)
        logger.error(f"❌ Transaction failed, rolled back: {e}")
        loaded_count = 0
        
    finally:
        conn.close()
    
    return loaded_count


def get_latest_records(limit=50):
    """
    📊 Latest Records Padhna (Dashboard ke liye)
    
    Database se sabse recent weather records nikaalte hain.
    Dashboard ko data dikhane ke liye ye function use hoga.
    
    Parameters:
        limit (int): Kitne records chahiye (default 50)
    
    Returns:
        list: List of dictionaries
    """
    
    conn = get_connection()
    try:
        cursor = conn.execute(
            f"SELECT * FROM {DATABASE_TABLE} ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        # ☝️ ORDER BY created_at DESC — newest records pehle
        # LIMIT ? — sirf itne records do
        
        rows = cursor.fetchall()
        # ☝️ fetchall() — saare results ek list mein de do
        
        # sqlite3.Row ko normal dictionary mein convert karo
        result = [dict(row) for row in rows]
        # ☝️ List Comprehension! Har row ko dict() se convert karke list mein dal diya
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error reading records: {e}")
        return []
    finally:
        conn.close()


def get_city_summary():
    """
    📈 City-wise Summary (Dashboard ke liye)
    
    Har city ka average temperature, min, max, aur total records.
    
    Returns:
        list: List of city summary dictionaries
    
    📚 CONCEPT: SQL Aggregation
    SQL mein GROUP BY + aggregate functions (AVG, MIN, MAX, COUNT) se
    data ka summary nikal sakte hain. Ye bahut powerful hai!
    """
    
    conn = get_connection()
    try:
        cursor = conn.execute(f"""
            SELECT 
                city,
                ROUND(AVG(temperature), 1) as avg_temp,
                ROUND(MIN(temperature), 1) as min_temp,
                ROUND(MAX(temperature), 1) as max_temp,
                ROUND(AVG(humidity), 0) as avg_humidity,
                COUNT(*) as record_count
            FROM {DATABASE_TABLE}
            GROUP BY city
            ORDER BY avg_temp DESC
        """)
        # ☝️ SQL Explanation:
        # SELECT city, AVG(temperature) — har city ka average temperature
        # GROUP BY city — city ke hisaab se group karo
        # ORDER BY avg_temp DESC — sabse garmi wali city pehle
        # ROUND(..., 1) — 1 decimal tak round karo
        # COUNT(*) — har city ke kitne records hain
        
        return [dict(row) for row in cursor.fetchall()]
        
    except Exception as e:
        logger.error(f"❌ Error getting city summary: {e}")
        return []
    finally:
        conn.close()


def get_pipeline_stats():
    """
    📉 Pipeline Statistics (Dashboard ke liye)
    
    Overall stats: total records, latest run, cities covered, etc.
    """
    
    conn = get_connection()
    try:
        cursor = conn.execute(f"""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT city) as total_cities,
                MIN(created_at) as first_run,
                MAX(created_at) as last_run,
                ROUND(AVG(temperature), 1) as overall_avg_temp
            FROM {DATABASE_TABLE}
        """)
        # ☝️ COUNT(DISTINCT city) — unique cities count karo
        # MIN(created_at) — sabse purana record kab ka hai
        # MAX(created_at) — sabse naya record kab ka hai
        
        row = cursor.fetchone()
        # ☝️ fetchone() — sirf ek row do (kyunki aggregate query ek hi row deti hai)
        
        return dict(row) if row else {}
        
    except Exception as e:
        logger.error(f"❌ Error getting pipeline stats: {e}")
        return {}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 🧪 QUICK TEST
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    
    from datetime import datetime
    
    # Test data
    test_records = [
        {
            "city": "Delhi", "temperature": 35.2, "feels_like": 37.0,
            "humidity": 60, "pressure": 1012, "wind_speed": 4.5,
            "weather_condition": "Clear", "temp_category": "Hot",
            "comfort_index": "Moderate", "timestamp": datetime.now().isoformat(),
            "source": "test", "processed_at": datetime.now().isoformat(),
        },
        {
            "city": "Mumbai", "temperature": 29.8, "feels_like": 31.0,
            "humidity": 80, "pressure": 1010, "wind_speed": 3.0,
            "weather_condition": "Clouds", "temp_category": "Pleasant",
            "comfort_index": "Moderate", "timestamp": datetime.now().isoformat(),
            "source": "test", "processed_at": datetime.now().isoformat(),
        },
    ]
    
    print("\n💾 Testing Load Module...\n")
    count = load_to_database(test_records)
    print(f"\n✅ Loaded {count} records")
    
    print("\n📊 Latest Records:")
    for r in get_latest_records(5):
        print(f"  {r['city']}: {r['temperature']}°C")
    
    print("\n📈 City Summary:")
    for s in get_city_summary():
        print(f"  {s['city']}: avg {s['avg_temp']}°C ({s['record_count']} records)")
