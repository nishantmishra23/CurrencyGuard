<div align="center">

# 💱 CurrencyGuard

### Real-Time Currency Exchange & Financial Risk Monitor

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A fintech-style dashboard for real-time currency exchange rates, historical trend visualization, and algorithmic financial risk analysis — built as a college mini-project for Advanced & Core Python Programming.**

</div>

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Live Features](#-live-features)
- [Tech Stack & Tools](#-tech-stack--tools)
- [API Used](#-api-used)
- [Project Architecture](#-project-architecture)
- [Python Concepts Demonstrated](#-python-concepts-demonstrated)
- [Custom Exception Hierarchy](#-custom-exception-hierarchy)
- [Technical Indicators Engine](#-technical-indicators-engine)
- [Supported Currencies](#-supported-currencies)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [Running the App](#-running-the-app)
- [Dependencies](#-dependencies-requirementstxt)
- [Disclaimer](#-disclaimer)

---

## 🌐 Project Overview

**CurrencyGuard** is a full-featured, production-style Python web application built to demonstrate mastery of **Chapter 4 – Exception Handling and Packages** from the Advanced & Core Python Programming curriculum.

It simulates a real fintech dashboard where users can:
- View **live currency exchange rates** across 10+ major global currencies
- **Convert** any amount between supported currency pairs with live rates
- Analyze **30-day historical price trends** with interactive charts
- Run an algorithmic **risk scoring engine** that evaluates volatility and price momentum
- Receive **financial alerts** when market conditions are unusual (high volatility, sudden moves)

Every layer of the app — from API calls to data transformation — is protected by structured, multi-level exception handling using both built-in and custom exceptions.

---

## 🚀 Live Features

| Feature | Description |
|---|---|
| 📊 **Real-Time Dashboard** | Fetches live exchange rates for all major currency pairs using the Twelve Data API |
| 🔁 **Currency Converter** | Convert any amount between 10 supported currencies with live rates |
| 📈 **Market Trends** | Interactive Plotly charts showing 30-day historical price series |
| 🧮 **Technical Indicators** | Locally computed RSI (14-day), SMA-20, SMA-50, MACD (12, 26) |
| 🔥 **Risk Analysis Engine** | Algorithmic risk scoring based on volatility and % price change |
| 🔔 **Financial Alerts** | Scans all pairs and flags high-volatility or sudden-movement events |
| 📉 **Market Metrics** | High, Low, Average, Current rate, % Change, and Std-Dev Volatility |

---

## 🛠️ Tech Stack & Tools

### Core Language

| Tool | Version | Purpose |
|---|---|---|
| **Python** | 3.11+ | Core application language |

### UI & Web Framework

| Tool | Version | Purpose |
|---|---|---|
| **Streamlit** | Latest | Powers the entire interactive web UI — tabs, sidebar, charts, alerts, and forms |

> Streamlit converts plain Python scripts into interactive web apps with zero frontend (HTML/CSS/JS) code required. Every widget — sliders, selectboxes, buttons, metric cards — is a native Streamlit component rendered directly from Python.

### Data Processing

| Tool | Version | Purpose |
|---|---|---|
| **Pandas** | 2.x | DataFrames for storing and processing time-series exchange rate data |
| **NumPy** | 1.x | Numerical computations for RSI, SMA, MACD, and volatility calculations |

> Pandas is used to parse the API's JSON response into typed DataFrames, handle datetime indexing, compute rolling window statistics, and feed clean data into the visualization layer.

### Visualization

| Tool | Version | Purpose |
|---|---|---|
| **Plotly** | 5.x | Interactive, animated charts for historical rate trends |
| **Matplotlib** | 3.x | Supplementary static chart rendering |

> Plotly is the primary charting library. It renders fully interactive line charts with hover tooltips, zoom/pan controls, and range sliders directly inside the Streamlit application.

### API & Networking

| Tool | Version | Purpose |
|---|---|---|
| **Requests** | 2.x | Makes authenticated HTTP GET calls to the Twelve Data REST API |

### Configuration & Security

| Tool | Version | Purpose |
|---|---|---|
| **python-dotenv** | 1.x | Loads the `TWELVEDATA_API_KEY` securely from the `.env` file at runtime |

---

## 🌍 API Used

### [Twelve Data API](https://twelvedata.com)

CurrencyGuard is powered by the **Twelve Data** financial data API — a professional-grade REST API providing real-time and historical data for forex, stocks, ETFs, and crypto.

**Base URL:** `https://api.twelvedata.com`

| Endpoint | Method | Description | Used For |
|---|---|---|---|
| `/quote` | GET | Latest close price & metadata for a forex pair | Real-time rates, currency converter |
| `/time_series` | GET | Historical OHLCV data at 1-day interval | 30-day trend charts, indicator computations |

**Key API Features Used:**
- **Symbol Batching** — Comma-separated symbols (e.g., `USD/EUR,USD/GBP,USD/INR`) fetch all dashboard rates in a **single API call**, minimising latency and API quota usage
- **Authentication** — API key is passed as a query parameter (`?apikey=...`) and loaded securely from environment variables via `python-dotenv`
- **Response Format** — JSON; the app validates the `status` field and raises `APIRequestError` if the API returns an error

**Free Tier Limits:** 8 API calls/minute · 800 calls/day — the architecture minimises redundant calls by batching.

---

## 🏗️ Project Architecture

```
CurrencyGuard/
│
├── app.py                    ← Main Streamlit application (UI + page logic)
├── config.py                 ← Centralised settings: API URL, app name, default currencies
├── requirements.txt          ← All Python package dependencies
├── .env                      ← Secret API key (NOT committed to Git)
├── .gitignore                ← Excludes .env, __pycache__, venv, etc.
│
├── api/
│   ├── __init__.py
│   └── currency_api.py       ← TwelveDataAPI class — raw HTTP client layer
│
├── services/
│   ├── __init__.py
│   ├── currency_service.py   ← CurrencyService — business logic & DataFrame processing
│   ├── risk_analyzer.py      ← RiskAnalyzer — algorithmic risk scoring engine
│   └── alert_service.py      ← AlertService — scans pairs for alert conditions
│
├── utils/
│   ├── __init__.py
│   ├── formatters.py         ← Currency formatting helpers (e.g., ₹1,23,456.78)
│   ├── helpers.py            ← Miscellaneous utility/helper functions
│   └── validators.py         ← Input validation (currency codes, amounts)
│
└── exceptions/
    ├── __init__.py
    └── custom_exceptions.py  ← Full custom exception hierarchy (4 exception types)
```

### Data Flow / Layer Separation

```
┌─────────────────────────────────────┐
│        Streamlit UI  (app.py)       │  ← User-facing pages, widgets, charts
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│     Service Layer  (services/)      │  ← Business logic, DataFrame transforms
│  CurrencyService · RiskAnalyzer     │
│  AlertService                       │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│       API Layer  (api/)             │  ← Raw HTTP requests, JSON parsing
│       TwelveDataAPI                 │
└──────────────────┬──────────────────┘
                   ↓
        Twelve Data REST API          ← External financial data source
```

---

## 🐍 Python Concepts Demonstrated

This project was explicitly designed to showcase **Chapter 4** concepts in depth:

### 1. Structured Exception Handling (`try` / `except` / `else` / `finally`)

Every API call is wrapped in structured, multi-level exception handling:

```python
try:
    response = requests.get(url, params=params, timeout=self.timeout)
    response.raise_for_status()
except requests.exceptions.Timeout as e:
    raise APIRequestError("Request timed out while connecting to the API.") from e
except requests.exceptions.ConnectionError as e:
    raise APIRequestError("Network connection error. Check your internet connection.") from e
except requests.exceptions.RequestException as e:
    raise APIRequestError(f"API Error occurred: {str(e)}") from e
```

### 2. Exception Chaining (`raise ... from e`)

Original low-level exceptions are chained using `raise NewException(...) from e` to preserve the **full traceback** while surfacing a user-friendly error message. This is a real-world best practice.

### 3. Custom Exception Hierarchy

A 4-level custom exception tree is defined in `exceptions/custom_exceptions.py`. See [below](#-custom-exception-hierarchy).

### 4. Packages & Modules

The project is split into **4 Python packages** (`api`, `services`, `utils`, `exceptions`), each with their own `__init__.py`, demonstrating real-world modular package design and relative imports.

### 5. Object-Oriented Programming — Classes

- `TwelveDataAPI` — Encapsulates the raw HTTP client with authentication
- `CurrencyService` — Service singleton wrapping business logic, holds a `TwelveDataAPI` instance
- `RiskAnalyzer` — Stateless analysis class
- `AlertService` — Scans and reports market events

### 6. Static Methods (`@staticmethod`)

`calculate_technical_indicators()` and `calculate_market_metrics()` are `@staticmethod` methods — they perform pure computation on passed data without needing instance state.

### 7. External Packages in Practice

Real-world usage of `pandas`, `numpy`, `requests`, `plotly`, `streamlit`, and `python-dotenv` — demonstrating how to install, import, and use third-party packages professionally.

---

## 🔴 Custom Exception Hierarchy

```
Exception  (Python built-in)
└── CurrencyAppError              ← Base for all CurrencyGuard errors
    ├── APIRequestError           ← API call fails (network, timeout, HTTP error, bad key)
    ├── InvalidCurrencyError      ← Unsupported or unknown currency code used
    ├── InvalidAmountError        ← Negative, zero, or non-numeric amount provided
    └── DataProcessingError       ← JSON parse failure or unexpected data structure
```

All four exception classes inherit from `CurrencyAppError`, which itself inherits from Python's built-in `Exception`. This hierarchy allows the app to catch all app-specific errors with a single `except CurrencyAppError` clause, or handle each type individually for finer control.

---

## 📐 Technical Indicators Engine

All technical indicators are computed **locally** using Pandas/NumPy on the historical DataFrame fetched from the API — no additional API calls are needed:

| Indicator | Full Name | Formula / Method | Window |
|---|---|---|---|
| **RSI** | Relative Strength Index | `100 - (100 / (1 + avg_gain / avg_loss))` | 14-day rolling |
| **SMA-20** | Simple Moving Average | `rolling(20).mean()` | 20-day |
| **SMA-50** | Simple Moving Average | `rolling(50).mean()` | 50-day |
| **MACD** | Moving Avg Convergence Divergence | `EMA(12) - EMA(26)` | 12 & 26 period EWM |
| **Volatility** | Daily Std-Dev (%) | `pct_change().std() * 100` | Full 30-day series |

**RSI Signal Interpretation:**

| RSI Value | Signal | Meaning |
|---|---|---|
| > 70 | 🔴 Overbought | Pair may be overvalued; potential reversal |
| < 30 | 🟢 Oversold | Pair may be undervalued; potential recovery |
| 30 – 70 | ⚪ Neutral | Normal trading range |

---

## 💱 Supported Currencies

| Code | Flag | Currency Name |
|---|---|---|
| USD | 🇺🇸 | US Dollar |
| EUR | 🇪🇺 | Euro |
| GBP | 🇬🇧 | British Pound Sterling |
| INR | 🇮🇳 | Indian Rupee |
| JPY | 🇯🇵 | Japanese Yen |
| AUD | 🇦🇺 | Australian Dollar |
| CAD | 🇨🇦 | Canadian Dollar |
| CHF | 🇨🇭 | Swiss Franc |
| SGD | 🇸🇬 | Singapore Dollar |
| AED | 🇦🇪 | UAE Dirham |

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.11** or higher installed
- A free API key from [Twelve Data](https://twelvedata.com/pricing) (free tier is available — no credit card required)

### Step-by-Step

**1. Clone the repository:**
```bash
git clone https://github.com/nishantmishra23/CurrencyGuard.git
cd CurrencyGuard
```

**2. (Recommended) Create a virtual environment:**
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

**3. Install all dependencies:**
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a file named `.env` in the project root directory (same folder as `app.py`) with the following content:

```env
TWELVEDATA_API_KEY=your_api_key_here
```

> ⚠️ **Never commit your `.env` file to GitHub.** It is already excluded via `.gitignore`. Exposing API keys publicly can lead to quota abuse or account bans.

**How to get a free Twelve Data API key:**
1. Visit [https://twelvedata.com](https://twelvedata.com)
2. Click **"Get your free API key"**
3. Create a free account (email only, no credit card)
4. Copy the API key from your dashboard and paste it into `.env`

---

## ▶️ Running the App

```bash
streamlit run app.py
```

The application will automatically open in your default browser at:

```
http://localhost:8501
```

---

## 📦 Dependencies (`requirements.txt`)

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework — renders the entire dashboard |
| `requests` | HTTP client — makes REST API calls to Twelve Data |
| `pandas` | DataFrame library — processes and transforms time-series data |
| `numpy` | Numerical computing — powers RSI, SMA, MACD, volatility formulas |
| `plotly` | Interactive charting — 30-day trend line charts with hover/zoom |
| `matplotlib` | Supplementary static chart rendering |
| `python-dotenv` | Loads API key securely from the `.env` file |

---

## 🔮 Future Enhancements

The following features are planned for future iterations of CurrencyGuard:
- **User Authentication**: Implement user accounts to save favorite currency pairs and custom alert thresholds.
- **Portfolio Tracking**: Allow users to mock-invest in different currencies and track their portfolio performance over time.
- **Machine Learning Forecasts**: Integrate a basic predictive model (like ARIMA or Prophet) to forecast short-term exchange rate movements.
- **Broader Data Coverage**: Expand from forex to include cryptocurrencies and major global stock indices.
- **Email Notifications**: Send alerts to users via email or SMS when extreme volatility is detected.

---

## 💼 Real-World Use Cases

- **Travelers**: Monitor exchange rates and set alerts to buy foreign currency at the most optimal times before a trip.
- **Freelancers/Contractors**: Keep track of income received in foreign currencies and convert it to local currency at the best rates.
- **Students**: Use this project as a reference implementation for learning how to consume REST APIs, handle errors robustly, and build dashboards with Streamlit.

---

## ⚠️ Disclaimer

This application is strictly an **educational project** created for the PPCA (Practical Python & Computer Applications / Advanced & Core Python Programming) curriculum. The risk indicators, alerts, and technical signals are generated using simple, rule-based historical calculations and **should NOT be interpreted as financial advice**. Do not make real financial decisions based on this tool.

All market data is sourced from the free tier of the **Twelve Data API**.

---

<div align="center">

Made with ❤️ by **Nishant Mishra** &nbsp;|&nbsp; PPCA Mini Project &nbsp;|&nbsp; 2026

</div>
