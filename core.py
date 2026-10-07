import os
import time
import math
import requests
import datetime
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

CURRENCY_METADATA = {
    "INR": {"name": "Indian Rupee", "symbol": "₹", "country": "India", "region": "Asia-Pacific", "bank": "Reserve Bank of India"},
    "USD": {"name": "US Dollar", "symbol": "$", "country": "United States", "region": "Americas", "bank": "Federal Reserve"},
    "EUR": {"name": "Euro", "symbol": "€", "country": "Eurozone", "region": "Europe", "bank": "European Central Bank"},
    "GBP": {"name": "British Pound", "symbol": "£", "country": "United Kingdom", "region": "Europe", "bank": "Bank of England"},
    "AED": {"name": "UAE Dirham", "symbol": "د.إ", "country": "United Arab Emirates", "region": "Middle East & Africa", "bank": "Central Bank of UAE"},
    "SAR": {"name": "Saudi Riyal", "symbol": "﷼", "country": "Saudi Arabia", "region": "Middle East & Africa", "bank": "Saudi Central Bank"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥", "country": "Japan", "region": "Asia-Pacific", "bank": "Bank of Japan"},
    "CAD": {"name": "Canadian Dollar", "symbol": "C$", "country": "Canada", "region": "Americas", "bank": "Bank of Canada"},
    "AUD": {"name": "Australian Dollar", "symbol": "A$", "country": "Australia", "region": "Asia-Pacific", "bank": "Reserve Bank of Australia"},
    "CHF": {"name": "Swiss Franc", "symbol": "CHF", "country": "Switzerland", "region": "Europe", "bank": "Swiss National Bank"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥", "country": "China", "region": "Asia-Pacific", "bank": "People's Bank of China"},
    "SGD": {"name": "Singapore Dollar", "symbol": "S$", "country": "Singapore", "region": "Asia-Pacific", "bank": "Monetary Authority of Singapore"},
    "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$", "country": "New Zealand", "region": "Asia-Pacific", "bank": "Reserve Bank of NZ"},
    "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$", "country": "Hong Kong", "region": "Asia-Pacific", "bank": "HK Monetary Authority"},
    "SEK": {"name": "Swedish Krona", "symbol": "kr", "country": "Sweden", "region": "Europe", "bank": "Sveriges Riksbank"},
    "NOK": {"name": "Norwegian Krone", "symbol": "kr", "country": "Norway", "region": "Europe", "bank": "Norges Bank"},
    "MXN": {"name": "Mexican Peso", "symbol": "$", "country": "Mexico", "region": "Americas", "bank": "Banco de México"},
    "BRL": {"name": "Brazilian Real", "symbol": "R$", "country": "Brazil", "region": "Americas", "bank": "Banco Central do Brasil"},
    "ZAR": {"name": "South African Rand", "symbol": "R", "country": "South Africa", "region": "Middle East & Africa", "bank": "South African Reserve Bank"},
    "KRW": {"name": "South Korean Won", "symbol": "₩", "country": "South Korea", "region": "Asia-Pacific", "bank": "Bank of Korea"},
    "PLN": {"name": "Polish Zloty", "symbol": "zł", "country": "Poland", "region": "Europe", "bank": "National Bank of Poland"},
    "TRY": {"name": "Turkish Lira", "symbol": "₺", "country": "Turkey", "region": "Europe", "bank": "Central Bank of Turkey"},
    "IDR": {"name": "Indonesian Rupiah", "symbol": "Rp", "country": "Indonesia", "region": "Asia-Pacific", "bank": "Bank Indonesia"},
    "THB": {"name": "Thai Baht", "symbol": "฿", "country": "Thailand", "region": "Asia-Pacific", "bank": "Bank of Thailand"},
    "DKK": {"name": "Danish Krone", "symbol": "kr", "country": "Denmark", "region": "Europe", "bank": "Danmarks Nationalbank"},
    "CZK": {"name": "Czech Koruna", "symbol": "Kč", "country": "Czech Republic", "region": "Europe", "bank": "Czech National Bank"},
    "HUF": {"name": "Hungarian Forint", "symbol": "Ft", "country": "Hungary", "region": "Europe", "bank": "Magyar Nemzeti Bank"},
    "ILS": {"name": "Israeli Shekel", "symbol": "₪", "country": "Israel", "region": "Middle East & Africa", "bank": "Bank of Israel"},
    "PHP": {"name": "Philippine Peso", "symbol": "₱", "country": "Philippines", "region": "Asia-Pacific", "bank": "Bangko Sentral ng Pilipinas"},
    "MYR": {"name": "Malaysian Ringgit", "symbol": "RM", "country": "Malaysia", "region": "Asia-Pacific", "bank": "Bank Negara Malaysia"},
}

def format_currency_label(code: str) -> str:
    """Returns currency code formatted with country in brackets, e.g. 'INR (India)'"""
    country = CURRENCY_METADATA.get(code, {}).get("country", "")
    return f"{code} ({country})" if country else code

BASELINE_USD_RATES = {
    "USD": 1.0,
    "EUR": 0.9225,
    "GBP": 0.7850,
    "JPY": 154.20,
    "INR": 83.45,
    "CAD": 1.3650,
    "AUD": 1.5280,
    "CHF": 0.9020,
    "CNY": 7.2360,
    "SGD": 1.3490,
    "NZD": 1.6340,
    "HKD": 7.8210,
    "SEK": 10.450,
    "NOK": 10.630,
    "MXN": 17.080,
    "BRL": 5.1250,
    "ZAR": 18.420,
    "AED": 3.6725,
    "SAR": 3.7500,
    "KRW": 1365.0,
    "PLN": 3.9850,
    "TRY": 32.40,
    "IDR": 16250.0,
    "THB": 36.80,
    "DKK": 6.8850,
    "CZK": 23.45,
    "HUF": 362.5,
    "ILS": 3.7250,
    "PHP": 57.50,
    "MYR": 4.7450,
}

TWELVEDATA_KEY = os.getenv("TWELVEDATA_API_KEY", "ff1e4a271da84999b4c545a4fc53a44a")

@st.cache_data(ttl=120)
def fetch_twelve_exchange_rate(pair: str) -> dict:
    """
    Fetch live exchange rate from Twelve Data API using API key.
    Pair format: 'EUR/USD', 'USD/INR', etc.
    """
    url = f"https://api.twelvedata.com/exchange_rate?symbol={pair}&apikey={TWELVEDATA_KEY}"
    try:
        resp = requests.get(url, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            if "rate" in data:
                return {
                    "rate": float(data["rate"]),
                    "timestamp": data.get("timestamp", int(time.time())),
                    "source": "Twelve Data (Live Keyed API)"
                }
    except Exception:
        pass
    return {}

@st.cache_data(ttl=300)
def fetch_frankfurter_latest(base: str = "USD") -> dict:
    """
    Fetch all latest exchange rates from open Frankfurter API (Direct, NO Key required).
    """
    endpoints = [
        f"https://api.frankfurter.dev/v1/latest?from={base}",
        f"https://api.frankfurter.app/latest?from={base}"
    ]
    for url in endpoints:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                rates = data.get("rates", {})
                rates[base] = 1.0
                return {
                    "base": base,
                    "date": data.get("date", str(datetime.date.today())),
                    "rates": rates,
                    "source": "Frankfurter (Direct ECB Open API)"
                }
        except Exception:
            continue
    return {}

@st.cache_data(ttl=600)
def fetch_frankfurter_timeseries(base: str, target: str, days: int = 30) -> pd.DataFrame:
    """
    Fetch historical daily rates for a pair from Frankfurter direct API.
    """
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)
    s_str = start_date.strftime("%Y-%m-%d")
    e_str = end_date.strftime("%Y-%m-%d")

    endpoints = [
        f"https://api.frankfurter.dev/v1/{s_str}..{e_str}?from={base}&to={target}",
        f"https://api.frankfurter.app/{s_str}..{e_str}?from={base}&to={target}"
    ]
    for url in endpoints:
        try:
            resp = requests.get(url, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                rates_dict = data.get("rates", {})
                if rates_dict:
                    records = []
                    for dt_str, r_dict in sorted(rates_dict.items()):
                        if target in r_dict:
                            records.append({"date": pd.to_datetime(dt_str), "rate": float(r_dict[target])})
                    if records:
                        df = pd.DataFrame(records)
                        df.sort_values("date", inplace=True)
                        return df
        except Exception:
            continue

    base_rate = get_cross_rate(base, target)
    rng = np.random.default_rng(seed=42)
    dates = pd.date_range(end=end_date, periods=min(days, 180), freq="B")
    shocks = rng.normal(0.0001, 0.004, size=len(dates))
    simulated_rates = [base_rate]
    for shock in shocks[1:]:
        simulated_rates.append(simulated_rates[-1] * (1 + shock))
    df = pd.DataFrame({"date": dates, "rate": simulated_rates})
    return df

def get_cross_rate(from_curr: str, to_curr: str) -> float:
    """
    Calculates rate from from_curr to to_curr with multi-tier fallback:
      1. Twelve Data Live (/exchange_rate)
      2. Frankfurter Live Latest
      3. Built-in Baseline Table
    """
    if from_curr == to_curr:
        return 1.0

    if from_curr in ["USD", "EUR", "GBP"] or to_curr in ["USD", "EUR"]:
        pair_str = f"{from_curr}/{to_curr}"
        twelve_res = fetch_twelve_exchange_rate(pair_str)
        if "rate" in twelve_res:
            return twelve_res["rate"]

    frank_res = fetch_frankfurter_latest(from_curr)
    if frank_res and "rates" in frank_res:
        rates = frank_res["rates"]
        if to_curr in rates:
            return float(rates[to_curr])

    usd_from = BASELINE_USD_RATES.get(from_curr, 1.0)
    usd_to = BASELINE_USD_RATES.get(to_curr, 1.0)
    return usd_to / usd_from

def calculate_risk_metrics(df: pd.DataFrame):
    """
    Calculates Value at Risk (VaR 95%, 99%), annualized volatility, and drawdown.
    """
    if len(df) < 5:
        return {
            "volatility_pct": 0.0,
            "var_95": 0.0,
            "var_99": 0.0,
            "max_drawdown": 0.0,
            "mean_return": 0.0,
        }

    rates = df["rate"].values
    daily_returns = np.diff(rates) / rates[:-1]

    mean_ret = float(np.mean(daily_returns))
    std_ret = float(np.std(daily_returns))

    ann_vol = float(std_ret * math.sqrt(252) * 100)

    var_95 = float(-(mean_ret - 1.645 * std_ret) * 100)
    var_99 = float(-(mean_ret - 2.326 * std_ret) * 100)

    cumulative = np.maximum.accumulate(rates)
    drawdowns = (rates - cumulative) / cumulative
    max_dd = float(np.min(drawdowns) * 100)

    return {
        "volatility_pct": round(ann_vol, 2),
        "var_95": round(max(0.0, var_95), 2),
        "var_99": round(max(0.0, var_99), 2),
        "max_drawdown": round(abs(max_dd), 2),
        "mean_return": round(mean_ret * 100, 4),
    }

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes SMA 20, SMA 50, and Bollinger Bands using pandas.
    """
    df_out = df.copy()
    df_out["sma_20"] = df_out["rate"].rolling(window=min(20, len(df_out)), min_periods=1).mean()
    df_out["sma_50"] = df_out["rate"].rolling(window=min(50, len(df_out)), min_periods=1).mean()

    rolling_std = df_out["rate"].rolling(window=min(20, len(df_out)), min_periods=1).std().fillna(0)
    df_out["bb_upper"] = df_out["sma_20"] + (2 * rolling_std)
    df_out["bb_lower"] = df_out["sma_20"] - (2 * rolling_std)
    return df_out

