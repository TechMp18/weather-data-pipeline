# ============================================================================
# etl/transform.py — Data Transformation Module (Data Ko Saaf Karna)
# ============================================================================
#
# 🎯 YEH FILE KYA HAI?
# ETL ka doosra step hai "TRANSFORM" — matlab raw data ko clean, validate,
# aur useful form mein convert karna.
#
# 📚 REAL WORLD MEIN:
# Raw data hamesha "dirty" hota hai:
# - Kuch values missing hoti hain (NULL/None)
# - Kuch values galat type ki hoti hain (string aana chahiye par number aa gaya)
# - Duplicate records hote hain
# - Values out of range hoti hain (temperature 500°C? Impossible!)
#
# Data Engineer ka kaam hai ye sab issues fix karna BEFORE data database mein
# jaaye. Agar dirty data database mein gaya toh reports galat aayengi!
#
# Is file mein hum sikhhenge:
# 1. Data Validation (kya data sahi hai?)
# 2. Data Cleaning (galat data fix karna)
# 3. Data Enrichment (extra useful info add karna)
# 4. Type Safety (sahi data types ensure karna)
# ============================================================================

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_temperature(temp):
    """
    🌡️ Temperature Validation
    
    Check karo ki temperature ek valid number hai aur reasonable range mein hai.
    
    Parameters:
        temp: Temperature value (kuch bhi ho sakta hai — number, string, None)
    
    Returns:
        float: Valid temperature
        None: Agar temperature invalid hai
    
    📚 CONCEPT: Type Checking
    Python mein koi bhi variable kisi bhi type ka ho sakta hai (dynamically typed).
    Isliye humein manually check karna padta hai ki value sahi type ki hai.
    isinstance(value, (int, float)) check karta hai ki value number hai ya nahi.
    """
    
    # Step 1: Check ki temp None toh nahi hai
    if temp is None:
        logger.warning("⚠️ Temperature is None")
        return None
    
    # Step 2: Check ki temp number hai
    # isinstance() check karta hai ki variable kis type ka hai
    if not isinstance(temp, (int, float)):
        try:
            temp = float(temp)  # String ko number mein convert karne ki koshish
        except (ValueError, TypeError):
            logger.warning(f"⚠️ Cannot convert temperature to number: {temp}")
            return None
    
    # Step 3: Check ki temperature realistic range mein hai
    # Duniya ka sabse kam: -89.2°C (Antarctica)
    # Duniya ka sabse zyada: 56.7°C (Death Valley)
    # Hum thoda margin dete hain: -100 to 70
    if not (-100 <= temp <= 70):
        logger.warning(f"⚠️ Temperature {temp}°C is out of realistic range")
        return None
    
    return float(temp)


def validate_humidity(humidity):
    """
    💧 Humidity Validation
    Humidity hamesha 0% se 100% ke beech honi chahiye.
    """
    if humidity is None:
        return None
    
    try:
        humidity = float(humidity)
    except (ValueError, TypeError):
        return None
    
    # Humidity percentage hai — 0 se 100 ke beech
    if not (0 <= humidity <= 100):
        logger.warning(f"⚠️ Humidity {humidity}% is out of range (0-100)")
        return None
    
    return humidity


def validate_string(value, field_name):
    """
    📝 String Validation
    Check ki value ek non-empty string hai.
    
    📚 CONCEPT: Truthy/Falsy Values
    Python mein kuch values "falsy" hoti hain: None, "", 0, [], {}
    Baaki sab "truthy" hoti hain.
    Toh `if not value` se hum None AUR empty string dono pakad lete hain!
    """
    if not value or not isinstance(value, str):
        logger.warning(f"⚠️ Invalid {field_name}: {value}")
        return None
    
    return value.strip()  # .strip() — string ke start aur end se spaces hatata hai


def add_temperature_category(temp):
    """
    🏷️ Temperature Category Add Karna
    
    Yeh "Data Enrichment" hai — existing data ke upar aur useful info add karna.
    Raw temperature se hum ek readable category bana rahe hain.
    
    Parameters:
        temp (float): Temperature in Celsius
    
    Returns:
        str: Category like "Cold", "Pleasant", "Hot", "Very Hot"
    
    📚 CONCEPT: Data Enrichment
    Companies mein raw data ke saath "derived fields" add karte hain.
    Example: Salary → "Low/Medium/High" band, Age → "Youth/Adult/Senior"
    Isse reports aur analytics easy ho jaati hai.
    """
    if temp is None:
        return "Unknown"
    
    if temp < 10:
        return "Cold"
    elif temp < 20:
        return "Cool"
    elif temp < 30:
        return "Pleasant"
    elif temp < 38:
        return "Hot"
    else:
        return "Very Hot"


def add_comfort_index(temp, humidity):
    """
    📊 Comfort Index Calculate Karna
    
    Temperature + Humidity combine karke ek "comfort score" banaate hain.
    Yeh bhi Data Enrichment hai — do existing fields se ek naya field ban gaya!
    
    Formula (simplified Heat Index):
    - High temperature + High humidity = Uncomfortable (low score)
    - Low temperature + Low humidity = Comfortable (high score)
    
    Returns:
        str: "Comfortable", "Moderate", or "Uncomfortable"
    """
    if temp is None or humidity is None:
        return "Unknown"
    
    # Simple comfort calculation
    # Ideal: temp 20-28°C, humidity 30-60%
    temp_score = max(0, 100 - abs(temp - 24) * 5)       # 24°C is ideal
    humidity_score = max(0, 100 - abs(humidity - 45) * 2) # 45% is ideal
    
    comfort = (temp_score + humidity_score) / 2
    
    if comfort >= 60:
        return "Comfortable"
    elif comfort >= 35:
        return "Moderate"
    else:
        return "Uncomfortable"


def transform_record(record):
    """
    🔄 EK RECORD KO TRANSFORM KARNA
    
    Yeh function ek single weather record ko validate, clean, aur enrich karta hai.
    
    Parameters:
        record (dict): Raw weather data from extract phase
    
    Returns:
        dict: Cleaned & enriched record (agar valid hai)
        None: Agar record invalid hai (skip kar denge)
    
    📚 CONCEPT: Data Pipeline Pattern
    Ye ek common pattern hai:
    1. Validate (check karo)
    2. Clean (fix karo)
    3. Enrich (extra info add karo)
    4. Return (aage bhejo ya reject karo)
    """
    
    # Step 1: Check ki record ek dictionary hai
    if not isinstance(record, dict):
        logger.error(f"❌ Record is not a dictionary: {type(record)}")
        return None
    
    # Step 2: City name validate karo
    city = validate_string(record.get("city"), "city")
    # ☝️ dict.get("key") — agar key nahi hai toh None deta hai (error nahi)
    # dict["key"] se safer hai kyunki wo KeyError dega agar key na mile
    
    if city is None:
        logger.error("❌ Record skipped — invalid city name")
        return None
    
    # Step 3: Temperature validate karo
    temperature = validate_temperature(record.get("temperature"))
    if temperature is None:
        logger.error(f"❌ Record skipped for {city} — invalid temperature")
        return None
    
    # Step 4: Humidity validate karo
    humidity = validate_humidity(record.get("humidity"))
    # Humidity None ho sakti hai — hum record reject nahi karenge, bus None rakhenge
    
    # Step 5: Baaki fields validate karo
    feels_like = validate_temperature(record.get("feels_like"))
    weather_condition = validate_string(record.get("weather_condition"), "weather_condition")
    
    # Step 6: Pressure validate karo (simple range check)
    pressure = record.get("pressure")
    try:
        pressure = float(pressure) if pressure is not None else None
        if pressure is not None and not (800 <= pressure <= 1200):
            logger.warning(f"⚠️ Unusual pressure for {city}: {pressure}")
            pressure = None
    except (ValueError, TypeError):
        pressure = None
    
    # Step 7: Wind speed validate karo
    wind_speed = record.get("wind_speed")
    try:
        wind_speed = float(wind_speed) if wind_speed is not None else None
        if wind_speed is not None and not (0 <= wind_speed <= 200):
            wind_speed = None
    except (ValueError, TypeError):
        wind_speed = None
    
    # Step 8: Timestamp validate karo
    timestamp = record.get("timestamp")
    if timestamp is None:
        timestamp = datetime.now().isoformat()  # Agar nahi hai toh current time use karo
    
    # Step 9: Data Enrichment — extra useful fields add karo!
    temp_category = add_temperature_category(temperature)
    comfort = add_comfort_index(temperature, humidity)
    
    # Step 10: Clean, validated, enriched record return karo ✨
    transformed_record = {
        "city": city.title(),  # .title() — first letter capital: "delhi" → "Delhi"
        "temperature": temperature,
        "feels_like": feels_like,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "weather_condition": weather_condition or "Unknown",
        "temp_category": temp_category,          # 🆕 Enriched field!
        "comfort_index": comfort,                # 🆕 Enriched field!
        "timestamp": timestamp,
        "source": record.get("source", "unknown"),
        "processed_at": datetime.now().isoformat(),  # 🆕 Kab process hua
    }
    
    return transformed_record


def transform_weather_data(raw_data):
    """
    🎯 MAIN TRANSFORM FUNCTION
    
    Yeh function saari weather records ko ek saath transform karta hai.
    Invalid records ko filter out kar deta hai.
    
    Parameters:
        raw_data (list): List of raw weather dictionaries from extract phase
    
    Returns:
        list: List of cleaned, validated, enriched dictionaries
    
    📚 CONCEPT: Filter Pattern
    Ye bahut common pattern hai data engineering mein:
    - Input: 100 records
    - Validate each: 5 fail → reject
    - Output: 95 clean records
    - Log: "5 records rejected" (for monitoring)
    """
    
    logger.info(f"{'='*50}")
    logger.info(f"🔄 TRANSFORM PHASE STARTED — {len(raw_data)} records")
    logger.info(f"{'='*50}")
    
    transformed_data = []  # Clean records yahan collect honge
    rejected_count = 0     # Kitne records reject hue
    
    for record in raw_data:
        result = transform_record(record)
        
        if result is not None:
            transformed_data.append(result)
        else:
            rejected_count += 1
    
    # Summary log
    logger.info(f"🔄 TRANSFORM COMPLETE:")
    logger.info(f"   ✅ Accepted: {len(transformed_data)} records")
    logger.info(f"   ❌ Rejected: {rejected_count} records")
    
    return transformed_data


# ---------------------------------------------------------------------------
# 🧪 QUICK TEST
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    
    # Test data — kuch sahi aur kuch galat records
    test_data = [
        {"city": "Delhi", "temperature": 35.2, "humidity": 60, "pressure": 1012, 
         "wind_speed": 4.5, "weather_condition": "Clear", "timestamp": "2024-01-01", "source": "test"},
        {"city": "", "temperature": 28, "humidity": 70, "pressure": 1010,
         "wind_speed": 3, "weather_condition": "Rain", "timestamp": "2024-01-01", "source": "test"},  # ❌ Empty city
        {"city": "Mumbai", "temperature": 500, "humidity": 80, "pressure": 1015,
         "wind_speed": 2, "weather_condition": "Clouds", "timestamp": "2024-01-01", "source": "test"},  # ❌ Impossible temp
        {"city": "Pune", "temperature": 27.5, "humidity": 45, "pressure": 1008,
         "wind_speed": 5, "weather_condition": "Clear", "timestamp": "2024-01-01", "source": "test"},
    ]
    
    print("\n🔄 Testing Transform Module...\n")
    results = transform_weather_data(test_data)
    
    print(f"\n📊 Results ({len(results)} valid records):\n")
    for r in results:
        print(f"  {r['city']}: {r['temperature']}°C [{r['temp_category']}] — {r['comfort_index']}")
