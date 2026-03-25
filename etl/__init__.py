# ============================================================================
# etl/__init__.py — Package Initializer
# ============================================================================
#
# 🎯 YEH FILE KYA HAI?
# Python mein jab tum ek folder ko "package" (module ka group) banana chahte ho
# toh us folder mein ek __init__.py file honi chahiye. Ye file Python ko batati
# hai: "Hey, yeh ek normal folder nahi hai, yeh ek Python package hai!"
#
# Is file ka kaam bas itna hai ki Python ko bataye ki "etl" folder se tum
# extract, transform, load modules import kar sakte ho.
#
# Example:
#   from etl.extract import fetch_weather_data
#   from etl.transform import transform_weather_data
#   from etl.load import load_to_database
# ============================================================================

from etl.extract import fetch_weather_data
from etl.transform import transform_weather_data
from etl.load import load_to_database
