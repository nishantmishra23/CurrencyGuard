# CurrencyGuard

**Real-Time Currency Exchange and Financial Risk Alert Application using APIs**

## Project Overview

This is a comprehensive college mini-project built for **Advanced and Core Python Programming**. It specifically demonstrates concepts from **Chapter 4 – Exception Handling and Packages**.

The application, CurrencyGuard, is a fintech-style dashboard that provides real-time currency exchange rates, historical trend visualization, and a rule-based educational risk analysis engine. 

## Features

- **Real-Time Dashboard**: View major currency pair updates in real-time.
- **Currency Converter**: Convert any supported currencies with live exchange rates.
- **Market Trends**: Visualize historical data using interactive Plotly charts.
- **Risk Analysis**: An algorithmic engine that calculates a risk score based on volatility and percentage change.
- **Financial Alerts**: A scanning system that notifies you of high volatility or sudden large movements in currency prices.

## Technologies Used

- **Python 3.11+**
- **Streamlit** (UI Framework)
- **Pandas & NumPy** (Data Processing & Analysis)
- **Plotly** (Interactive Visualizations)
- **Requests** (API Integration)

## Python Concepts Demonstrated

1. **Exception Handling**: 
   - Extensive use of `try`, `except`, `else`, `finally`.
   - Creating a custom hierarchy of exceptions (e.g., `APIRequestError`, `InvalidCurrencyError`).
2. **Packages and Modules**:
   - Organized into a clean, modular architecture (`api/`, `services/`, `utils/`, `exceptions/`).
3. **External Packages**: Practical usage of `pandas`, `requests`, and `streamlit`.
4. **Classes & Functions**: Object-oriented API clients and service singletons.

## Installation

1. Clone or extract the project folder.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Disclaimer
This application is strictly an educational project. The risk indicators are generated using simple historical rules and should **not** be considered financial advice. All data is sourced from the free Frankfurter API.
