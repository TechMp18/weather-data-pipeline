# ============================================================================
# etl/extract.py — Data Extraction Module (Data Nikalna)
# ============================================================================
#
# 🎯 YEH FILE KYA HAI?
# ETL ka pehla step hai "EXTRACT" — matlab data ko source se nikalna.
# Humara source hai OpenWeatherMap API (ya Demo mode mein fake data).
#
# 📚 REAL WORLD MEIN:
# Data Engineers ko data bahut jagahon se extract karna padta hai:
# - APIs (jaise hum kar rahe hain)
# - Databases (MySQL, PostgreSQL se data pull karna)
# - Files (CSV, JSON, Excel files padhna)
# - Web Scraping (websites se data nikalna)
#
# Is file mein hum sikhhenge:
# 1. API se data kaise fetch karte hain (requests library)
# 2. Error handling kaise karte hain (try/except)
# 3. Retry logic kya hoti hai (agar fail ho toh dobara try karo)
# 4. Logging kya hai (diary maintain karna)
# ============================================================================

import requests  # HTTP requests bhejne ke liye (API se data maangna)
import logging   # Logging ke liye — kya hua kab hua record karna
import random    # Random numbers generate karne ke liye (demo data mein use hoga)
import time      # Time related functions (retry mein wait karne ke liye)
from datetime import datetime  # Date aur time handle karne ke liye
from config import API_KEY, API_BASE_URL, CITIES, DEMO_MODE, UNITS

# ---------------------------------------------------------------------------
# 📝 Logger Setup (Diary Setup)
# ---------------------------------------------------------------------------
# Logger kya hai? Ye ek "diary writer" hai jo record karta hai ki program mein
# kya kya hua. Jab kuch galat hota hai, toh log file padhke pata lagaate hain.
#
# Levels of logging (severity ke hisaab se):
# DEBUG → INFO → WARNING → ERROR → CRITICAL
# DEBUG = sab kuch record karo (debugging ke liye)
# INFO = important milestones (e.g., "Data fetch hua")
# WARNING = kuch theek nahi hai par chalega
# ERROR = kuch galat hua par program chal raha hai
# CRITICAL = program crash hone wala hai
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)
# ☝️ __name__ is file ka naam deta hai ("etl.extract")
# Isse log mein pata chalta hai ki konsi file se log aaya


def generate_demo_data(city):
    """
    🧪 DEMO DATA GENERATOR
    
    Jab API key nahi hai, toh yeh function FAKE (par realistic) weather data
    banata hai. Isse project bina API key ke bhi chalega!
    
    Parameters:
        city (str): City ka naam, e.g. "Delhi"
    
    Returns:
        dict: Ek dictionary with weather info
    
    📚 CONCEPT: Dictionary (dict)
    Dictionary ek key-value pair storage hai — jaise ek real dictionary mein
    word → meaning hota hai, waise dict mein key → value hota hai.
    Example: {"name": "Mukul", "age": 22}
    """
    
    # Har city ke liye thoda alag temperature range (realistic banane ke liye)
    # fmt: off
    city_temp_ranges = {
        "Delhi":     (15, 45),   # Delhi: garmi mein 45°C tak
        "Mumbai":    (22, 38),   # Mumbai: moderate
        "Bangalore": (18, 35),   # Bangalore: pleasant weather
        "Hyderabad": (20, 42),   # Hyderabad: garmi zyada
        "Chennai":   (24, 40),   # Chennai: humid & hot
        "Kolkata":   (15, 40),   # Kolkata: diverse
        "Pune":      (18, 38),   # Pune: pleasant
        "Jaipur":    (10, 46),   # Jaipur: extreme temperatures
    }
    # fmt: on

    # City ka range nikalo, agar nahi mila toh default (20, 40) use karo
    temp_min, temp_max = city_temp_ranges.get(city, (20, 40))
    # ☝️ dict.get(key, default) — agar key nahi mili toh default value deta hai
    # Ye safer hai dict[key] se kyunki dict[key] ERROR deta hai agar key na mile

    # Random temperature generate karo range ke andar
    temperature = round(random.uniform(temp_min, temp_max), 1)
    # ☝️ random.uniform(a, b) — a aur b ke beech ek random decimal number deta hai
    # round(..., 1) — ek decimal place tak round karta hai (e.g., 32.7)

    # Weather conditions ki list — randomly ek choose karenge
    conditions = ["Clear", "Clouds", "Rain", "Haze", "Mist", "Drizzle", "Thunderstorm"]

    demo_record = {
        "city": city,
        "temperature": temperature,
        "feels_like": round(temperature + random.uniform(-3, 3), 1),
        "humidity": random.randint(30, 95),       # 30% se 95% ke beech
        "pressure": random.randint(990, 1030),    # hPa mein
        "wind_speed": round(random.uniform(0, 15), 1),  # m/s mein
        "weather_condition": random.choice(conditions),  # Random condition
        "timestamp": datetime.now().isoformat(),  # Current date-time
        "source": "demo",                         # Ye demo data hai
    }

    return demo_record


def fetch_from_api(city):
    """
    🌐 REAL API SE DATA FETCH KARNA
    
    Yeh function OpenWeatherMap API se REAL weather data laata hai.
    
    Parameters:
        city (str): City ka naam
    
    Returns:
        dict: Weather data dictionary (agar successful)
        None: Agar koi error aayi
    
    📚 CONCEPT: HTTP Request
    Jab tum browser mein koi website open karte ho, toh browser ek "GET request"
    bhejta hai server ko. Yahan hum same kaam code se kar rahe hain!
    
    API response kuch aisa dikhta hai:
    {
        "main": {"temp": 32.5, "humidity": 65, "pressure": 1012},
        "wind": {"speed": 4.2},
        "weather": [{"main": "Clear"}],
        "name": "Delhi"
    }
    """
    
    # API ke liye parameters (query string)
    # URL banega: https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid=KEY&units=metric
    params = {
        "q": city,           # q = query = konsi city chahiye
        "appid": API_KEY,    # appid = API key (authentication)
        "units": UNITS,      # units = metric matlab Celsius
    }

    # ---------------------------------------------------------------------------
    # 🔄 RETRY LOGIC (Dobara Try Karna)
    # ---------------------------------------------------------------------------
    # Internet pe requests fail ho sakti hain — network slow ho, server busy ho.
    # Isliye hum 3 baar try karenge. Har baar fail hone pe thoda wait karenge.
    # Isko "Exponential Backoff" kehte hain — pehli baar 1 sec wait, phir 2 sec,
    # phir 4 sec. Companies mein ye bahut common pattern hai!
    # ---------------------------------------------------------------------------

    max_retries = 3  # Kitni baar try karenge

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"🌐 Fetching weather for {city} (attempt {attempt}/{max_retries})")
            
            # API ko request bhejo
            response = requests.get(API_BASE_URL, params=params, timeout=10)
            # ☝️ requests.get() — GET request bhejta hai
            # timeout=10 — agar 10 seconds mein response na aaye toh error do
            
            # Response ka status check karo
            response.raise_for_status()
            # ☝️ raise_for_status() — agar response mein error hai (404, 500 etc.)
            # toh ye ek Exception raise kar deta hai, jo except block pakad lega
            
            # JSON data parse karo
            data = response.json()
            # ☝️ .json() — response ke text ko Python dictionary mein convert karta hai
            # API data JSON format mein bhejte hain (JavaScript Object Notation)
            
            # API ke raw data se humein jo chahiye wo nikalo
            weather_record = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "weather_condition": data["weather"][0]["main"],
                "timestamp": datetime.now().isoformat(),
                "source": "api",
            }
            # ☝️ Nested dictionary access:
            # data["main"]["temp"] matlab:
            # Step 1: data["main"] → {"temp": 32, "humidity": 65, ...}
            # Step 2: uske andar se ["temp"] → 32
            
            logger.info(f"✅ Successfully fetched data for {city}: {weather_record['temperature']}°C")
            return weather_record

        except requests.exceptions.Timeout:
            # Server se response nahi aaya time pe
            logger.warning(f"⏱️ Timeout for {city}, attempt {attempt}")
            
        except requests.exceptions.ConnectionError:
            # Internet connection problem
            logger.warning(f"🔌 Connection error for {city}, attempt {attempt}")
            
        except requests.exceptions.HTTPError as e:
            # Server ne error bheja (404, 401, 500, etc.)
            logger.error(f"❌ HTTP error for {city}: {e}")
            return None  # HTTP error pe retry nahi karenge (city name galat ho sakta hai)
            
        except Exception as e:
            # Koi aur unexpected error
            logger.error(f"💥 Unexpected error for {city}: {e}")
        
        # Retry se pehle wait karo (Exponential Backoff)
        if attempt < max_retries:
            wait_time = 2 ** attempt  # 2, 4, 8 seconds
            logger.info(f"⏳ Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
    
    # Sab retries fail ho gayi
    logger.error(f"❌ All {max_retries} attempts failed for {city}")
    return None


def fetch_weather_data(cities=None):
    """
    🎯 MAIN EXTRACT FUNCTION
    
    Yeh function sab cities ka weather data ek saath collect karta hai.
    Demo mode mein fake data deta hai, otherwise real API se laata hai.
    
    Parameters:
        cities (list): Cities ki list. None doge toh config se le lega.
    
    Returns:
        list: Dictionaries ki list, har dictionary ek city ka weather data
    
    📚 CONCEPT: Function Parameters with Defaults
    cities=None matlab agar koi cities list nahi di, toh None ho jayega.
    Phir hum config.py se default list use karenge.
    """
    
    if cities is None:
        cities = CITIES  # Config se default cities list use karo
    
    all_weather_data = []  # Sab cities ka data yahan collect hoga
    
    logger.info(f"{'='*50}")
    logger.info(f"📡 EXTRACT PHASE STARTED — {len(cities)} cities")
    logger.info(f"📡 Mode: {'DEMO' if DEMO_MODE else 'LIVE API'}")
    logger.info(f"{'='*50}")
    
    for city in cities:
        if DEMO_MODE:
            # Demo mode — fake data generate karo
            record = generate_demo_data(city)
            logger.info(f"🧪 Generated demo data for {city}: {record['temperature']}°C")
        else:
            # Real mode — API se data fetch karo
            record = fetch_from_api(city)
        
        if record is not None:
            all_weather_data.append(record)
            # ☝️ .append() — list ke end mein ek item add karta hai
            # all_weather_data ab thoda bada ho gaya
        else:
            logger.warning(f"⚠️ Skipping {city} — no data received")
    
    logger.info(f"📡 EXTRACT COMPLETE — Got data for {len(all_weather_data)}/{len(cities)} cities")
    
    return all_weather_data


# ---------------------------------------------------------------------------
# 🧪 QUICK TEST (ye file directly run karo toh ye chalega)
# ---------------------------------------------------------------------------
# Python mein __name__ == "__main__" ka matlab hai:
# "Yeh code sirf tab chalega jab TUM is file ko seedha run karo"
# Agar koi aur file import kare toh ye nahi chalega.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Logging setup (console pe dikhane ke liye)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    
    print("\n🌦️ Testing Extract Module...\n")
    data = fetch_weather_data()
    
    print(f"\n📊 Extracted {len(data)} records:\n")
    for record in data:
        print(f"  {record['city']}: {record['temperature']}°C, {record['weather_condition']}")
