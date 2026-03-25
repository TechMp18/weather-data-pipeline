# ============================================================================
# config.py — Configuration File (Settings ka File)
# ============================================================================
#
# 🎯 YEH FILE KYA HAI?
# Yeh file project ki "settings" store karti hai — jaise API key, database ka
# path, aur kin cities ka weather chahiye. Isko alag file mein rakhne ka fayda
# yeh hai ki settings change karne ke liye sirf yahi file edit karni padti hai,
# baaki code ko chhoona nahi padta.
#
# 📚 CONCEPT: Configuration Management
# Real companies mein bhi settings ko code se alag rakhte hain. Isse "Separation
# of Concerns" kehte hain — har file ka ek hi kaam hona chahiye.
# ============================================================================

import os  # os module — operating system se baat karne ke liye (file paths etc.)

# ---------------------------------------------------------------------------
# 🔑 API Configuration (API ka Setup)
# ---------------------------------------------------------------------------
# API kya hai? API ek "waiter" hai jo tumhare order (request) kitchen (server)
# tak le jaata hai aur khana (data) wapas laata hai.
#
# OpenWeatherMap ek FREE weather service hai. Tumhe unke website pe signup karke
# ek "API Key" milega — yeh ek password jaisa hai jo prove karta hai ki tum
# authorized ho data lene ke liye.
#
# Agar tumhare paas API key nahi hai, chinta mat karo! Hum DEMO_MODE use karenge
# jo fake (sample) data dega — project phir bhi chalega!
# ---------------------------------------------------------------------------

API_KEY = os.environ.get("WEATHER_API_KEY", "demo")
# ☝️ Ye line kya kar rahi hai?
# 1. Pehle check karti hai ki "WEATHER_API_KEY" naam ka environment variable set hai ya nahi
# 2. Agar set hai → uski value use karegi
# 3. Agar nahi hai → "demo" use karegi (matlab demo mode chalega)
#
# Environment variable kya hai? Ye computer ke andar stored settings hain
# jo programs ke saath share hoti hain. Password/keys aise hi store karte hain
# taaki yeh code mein directly na likhi jaayein (security ke liye).

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# ☝️ Yeh URL hai jahaan se hum weather data fetch karenge
# Jaise tum browser mein google.com type karte ho, waise yeh program is URL pe
# jaake data maangega

# ---------------------------------------------------------------------------
# 🏙️ Cities List (Kin cities ka weather chahiye?)
# ---------------------------------------------------------------------------
# Yeh list hai un cities ki jinka weather data hum collect karenge.
# Tum isme aur cities add/remove kar sakte ho!
# ---------------------------------------------------------------------------

CITIES = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Jaipur",
]

# ---------------------------------------------------------------------------
# 💾 Database Configuration (Database ka Setup)
# ---------------------------------------------------------------------------
# SQLite kya hai? Ye ek chhota sa database hai jo EK FILE mein data store
# karta hai. MySQL/PostgreSQL jaise bade databases ko alag server chahiye,
# par SQLite ko kuch nahi chahiye — bus ek .db file bana deta hai!
# Beginners ke liye perfect hai.
# ---------------------------------------------------------------------------

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "weather_data.db")
# ☝️ Ye line kya karti hai?
# os.path.dirname(__file__) → is file (config.py) ka folder path deta hai
# os.path.join(..., "weather_data.db") → us folder mein "weather_data.db" naam
# ki file ka full path banata hai
# Result: "c:\Users\mukul\Downloads\Projects\Data Engineer\weather_data.db"

DATABASE_TABLE = "weather_records"
# ☝️ Table ka naam — database ke andar data is naam ki table mein store hoga
# Table kya hai? Excel sheet jaisi samjho — rows aur columns mein data hota hai

# ---------------------------------------------------------------------------
# ⏰ Pipeline Configuration (Pipeline ke Settings)
# ---------------------------------------------------------------------------
# Pipeline kya hai? Ek assembly line jaisi — data ek step se dusre step mein
# jaata hai: Extract → Transform → Load
# ---------------------------------------------------------------------------

PIPELINE_INTERVAL_MINUTES = 30
# ☝️ Pipeline har 30 minute mein chalegi (fresh data layegi)

LOG_FILE = os.path.join(os.path.dirname(__file__), "pipeline.log")
# ☝️ Log file — pipeline ka "diary" — kya hua, kab hua, koi error aayi?
# Production mein log files bahut important hain — agar kuch galat ho jaaye
# toh log file padh ke pata lagaate hain ki kya hua tha

# ---------------------------------------------------------------------------
# 🧪 Demo Mode (Bina API key ke chalana)
# ---------------------------------------------------------------------------

DEMO_MODE = (API_KEY == "demo")
# ☝️ Agar API_KEY "demo" hai toh DEMO_MODE = True ho jayega
# Demo mode mein hum fake/sample data generate karenge
# Isse project API key ke bina bhi chal sakta hai!

# ---------------------------------------------------------------------------
# 🌡️ Units Configuration
# ---------------------------------------------------------------------------

UNITS = "metric"
# ☝️ Temperature Celsius mein chahiye (metric),
# "imperial" dete toh Fahrenheit mein aata
