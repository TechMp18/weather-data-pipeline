# ============================================================================
# tests/test_transform.py — Unit Tests (Code Ko Test Karna)
# ============================================================================
#
# 🎯 YEH FILE KYA HAI?
# Unit Tests likhte hain taaki verify kar sakein ki humara code SAHI kaam kar
# raha hai. SAHI matlab:
# - Sahi input pe sahi output de raha hai ✅
# - Galat input pe gracefully handle kar raha hai ✅
# - Edge cases (extreme situations) mein bhi theek hai ✅
#
# 📚 CONCEPT: Unit Testing
# "Unit" = code ka sabse chhota testable piece (usually ek function)
# "Unit Test" = ek automated check jo verify karta hai ki function sahi kaam karti hai
#
# Companies mein testing MANDATORY hai — bina tests ke code production mein nahi jaata!
# Highspring ki JD mein likha hai: "zero defect code" — tests se hi ensure hota hai.
#
# 📚 CONCEPT: pytest Framework
# pytest Python ka sabse popular testing framework hai.
# Test functions ka naam "test_" se start hona chahiye.
# Run karne ke liye: python -m pytest tests/ -v
# -v = verbose (detail mein output dikhao)
# ============================================================================

import sys
import os

# Project root ko path mein add karo (taaki etl module import ho sake)
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# ☝️ Ye line kya karti hai?
# __file__ = is file ka path (tests/test_transform.py)
# dirname → tests/
# dirname → project root
# sys.path mein add karne se Python ko pata chalega ki modules kahaan dhundne hain

from etl.transform import (
    validate_temperature,
    validate_humidity,
    validate_string,
    add_temperature_category,
    add_comfort_index,
    transform_record,
    transform_weather_data,
)


# ============================================================================
# 🌡️ Temperature Validation Tests
# ============================================================================

class TestValidateTemperature:
    """
    Temperature validation ke tests.
    
    📚 CONCEPT: Test Class
    Related tests ko ek class mein group karte hain.
    Class ka naam "Test" se start hona chahiye (pytest convention).
    """
    
    def test_valid_temperature(self):
        """Normal temperature should pass"""
        assert validate_temperature(25.5) == 25.5
        # ☝️ assert — "yeh TRUE hona chahiye, nahi toh test FAIL"
        # assert 1 + 1 == 2  → PASS ✅
        # assert 1 + 1 == 3  → FAIL ❌
    
    def test_zero_temperature(self):
        """0°C is valid (water freezing point)"""
        assert validate_temperature(0) == 0.0
    
    def test_negative_temperature(self):
        """Negative temperature is valid"""
        assert validate_temperature(-20) == -20.0
    
    def test_extreme_hot(self):
        """56°C is valid (Death Valley record)"""
        assert validate_temperature(56.7) == 56.7
    
    def test_too_hot(self):
        """500°C is impossible — should return None"""
        assert validate_temperature(500) is None
        # ☝️ "is None" check karta hai ki value exactly None hai
        # "== None" bhi kaam karega par "is None" Pythonic (recommended) hai
    
    def test_too_cold(self):
        """-200°C is impossible"""
        assert validate_temperature(-200) is None
    
    def test_none_input(self):
        """None input should return None"""
        assert validate_temperature(None) is None
    
    def test_string_number(self):
        """String number "25.5" should be converted to float"""
        assert validate_temperature("25.5") == 25.5
    
    def test_invalid_string(self):
        """Non-numeric string should return None"""
        assert validate_temperature("hello") is None
    
    def test_integer_input(self):
        """Integer should be converted to float"""
        result = validate_temperature(30)
        assert result == 30.0
        assert isinstance(result, float)
        # ☝️ isinstance() — check karo ki variable float type ka hai


# ============================================================================
# 💧 Humidity Validation Tests
# ============================================================================

class TestValidateHumidity:
    
    def test_valid_humidity(self):
        assert validate_humidity(65) == 65.0
    
    def test_zero_humidity(self):
        assert validate_humidity(0) == 0.0
    
    def test_full_humidity(self):
        assert validate_humidity(100) == 100.0
    
    def test_negative_humidity(self):
        """Humidity can't be negative"""
        assert validate_humidity(-10) is None
    
    def test_over_100(self):
        """Humidity can't be > 100%"""
        assert validate_humidity(150) is None
    
    def test_none(self):
        assert validate_humidity(None) is None


# ============================================================================
# 📝 String Validation Tests
# ============================================================================

class TestValidateString:
    
    def test_valid_string(self):
        assert validate_string("Delhi", "city") == "Delhi"
    
    def test_empty_string(self):
        """Empty string should return None"""
        assert validate_string("", "city") is None
    
    def test_none_input(self):
        assert validate_string(None, "city") is None
    
    def test_whitespace_string(self):
        """String with spaces should be stripped"""
        assert validate_string("  Mumbai  ", "city") == "Mumbai"
    
    def test_number_input(self):
        """Number is not a string"""
        assert validate_string(123, "city") is None


# ============================================================================
# 🏷️ Temperature Category Tests
# ============================================================================

class TestTemperatureCategory:
    
    def test_cold(self):
        assert add_temperature_category(5) == "Cold"
    
    def test_cool(self):
        assert add_temperature_category(15) == "Cool"
    
    def test_pleasant(self):
        assert add_temperature_category(25) == "Pleasant"
    
    def test_hot(self):
        assert add_temperature_category(35) == "Hot"
    
    def test_very_hot(self):
        assert add_temperature_category(42) == "Very Hot"
    
    def test_none(self):
        assert add_temperature_category(None) == "Unknown"
    
    def test_boundary_cold_cool(self):
        """Exactly 10°C should be Cool (not Cold)"""
        assert add_temperature_category(10) == "Cool"
        # ☝️ Boundary testing — exact boundary values pe test karo
        # Bahut common interview question hai!


# ============================================================================
# 📊 Comfort Index Tests
# ============================================================================

class TestComfortIndex:
    
    def test_comfortable(self):
        """24°C, 45% humidity — ideal conditions"""
        result = add_comfort_index(24, 45)
        assert result == "Comfortable"
    
    def test_uncomfortable(self):
        """45°C, 95% humidity — very uncomfortable"""
        result = add_comfort_index(45, 95)
        assert result == "Uncomfortable"
    
    def test_none_temp(self):
        assert add_comfort_index(None, 50) == "Unknown"
    
    def test_none_humidity(self):
        assert add_comfort_index(25, None) == "Unknown"


# ============================================================================
# 🔄 Transform Record Tests
# ============================================================================

class TestTransformRecord:
    """Transform record ke integration tests"""
    
    def test_valid_record(self):
        """Complete valid record should transform successfully"""
        record = {
            "city": "Delhi",
            "temperature": 35.2,
            "feels_like": 37.0,
            "humidity": 60,
            "pressure": 1012,
            "wind_speed": 4.5,
            "weather_condition": "Clear",
            "timestamp": "2024-01-01T12:00:00",
            "source": "test"
        }
        
        result = transform_record(record)
        
        assert result is not None
        assert result["city"] == "Delhi"
        assert result["temperature"] == 35.2
        assert result["temp_category"] == "Hot"
        assert result["comfort_index"] in ["Comfortable", "Moderate", "Uncomfortable"]
        assert "processed_at" in result  # Enriched field should exist
    
    def test_missing_city(self):
        """Record without city should be rejected"""
        record = {"temperature": 25, "humidity": 50}
        assert transform_record(record) is None
    
    def test_missing_temperature(self):
        """Record without temperature should be rejected"""
        record = {"city": "Delhi", "humidity": 50}
        assert transform_record(record) is None
    
    def test_invalid_temperature(self):
        """Record with impossible temperature should be rejected"""
        record = {"city": "Delhi", "temperature": 500, "humidity": 50}
        assert transform_record(record) is None
    
    def test_not_a_dict(self):
        """Non-dict input should return None"""
        assert transform_record("not a dict") is None
        assert transform_record(None) is None
        assert transform_record(42) is None
    
    def test_city_title_case(self):
        """City name should be title-cased"""
        record = {
            "city": "delhi",
            "temperature": 30,
            "timestamp": "2024-01-01",
        }
        result = transform_record(record)
        assert result["city"] == "Delhi"  # "delhi" → "Delhi"


# ============================================================================
# 🎯 Transform Weather Data (Full Pipeline Transform) Tests
# ============================================================================

class TestTransformWeatherData:
    
    def test_mixed_data(self):
        """Some valid, some invalid — only valid should pass"""
        data = [
            {"city": "Delhi", "temperature": 35, "timestamp": "2024-01-01"},
            {"city": "", "temperature": 28, "timestamp": "2024-01-01"},      # Invalid: empty city
            {"city": "Mumbai", "temperature": 500, "timestamp": "2024-01-01"},  # Invalid: impossible temp
            {"city": "Pune", "temperature": 27, "timestamp": "2024-01-01"},
        ]
        
        results = transform_weather_data(data)
        
        assert len(results) == 2  # Only Delhi and Pune should pass
        cities = [r["city"] for r in results]
        assert "Delhi" in cities
        assert "Pune" in cities
    
    def test_empty_input(self):
        """Empty list should return empty list"""
        assert transform_weather_data([]) == []
    
    def test_all_invalid(self):
        """All invalid records should return empty list"""
        data = [
            {"city": "", "temperature": 28},
            {"city": "X", "temperature": 999},
        ]
        assert len(transform_weather_data(data)) == 0


# ============================================================================
# 🧪 Run Tests
# ============================================================================
# Terminal mein ye command run karo:
#   python -m pytest tests/test_transform.py -v
#
# Output kuch aisa aayega:
#   tests/test_transform.py::TestValidateTemperature::test_valid_temperature PASSED
#   tests/test_transform.py::TestValidateTemperature::test_none_input PASSED
#   ... and so on
#
# Sab PASSED dikhna chahiye! ✅
# ============================================================================
