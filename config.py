import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# API Settings
try:
    API_KEY = st.secrets.get("TWELVEDATA_API_KEY", os.getenv("TWELVEDATA_API_KEY"))
except FileNotFoundError:
    API_KEY = os.getenv("TWELVEDATA_API_KEY")

TWELVEDATA_BASE_URL = "https://api.twelvedata.com"

# Application Settings
APP_NAME = "CurrencyGuard"
APP_SUBTITLE = "Real-Time Currency Exchange & Financial Risk Monitor"

# Supported Currencies
DEFAULT_CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "CHF", "SGD", "AED"]
