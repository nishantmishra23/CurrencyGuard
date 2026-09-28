import pandas as pd
from api.currency_api import TwelveDataAPI
from exceptions.custom_exceptions import DataProcessingError
import datetime

class CurrencyService:
    """
    Service layer for business logic and data processing.
    """
    def __init__(self):
        self.api = TwelveDataAPI()

    def get_latest_rates(self, base="USD", targets=None):
        if not targets:
            targets = ["EUR", "GBP", "INR", "JPY"]
            
        rates = {}
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Twelve Data batching via comma separated string
        symbols = ",".join([f"{base}/{t}" for t in targets])
        data = self.api._make_request("quote", params={"symbol": symbols})
        
        if len(targets) > 1:
            for t in targets:
                pair = f"{base}/{t}"
                if pair in data:
                    rates[t] = float(data[pair].get("close", data[pair].get("previous_close", 0)))
                    date_str = data[pair].get("datetime", date_str)
        else:
            if 'close' in data:
                rates[targets[0]] = float(data.get("close", 0))
                date_str = data.get("datetime", date_str)
                
        return rates, date_str

    def get_historical_dataframe(self, base, target, days=30):
        try:
            data = self.api.get_historical_rates(base, target, days)
            values = data.get("values", [])
            if not values:
                return None
                
            df = pd.DataFrame(values)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)
            df['close'] = df['close'].astype(float)
            df.sort_index(inplace=True)
            
            # For compatibility with RiskAnalyzer, rename 'close' column to the target currency string
            df.rename(columns={'close': target}, inplace=True)
            return df
        except Exception as e:
            raise DataProcessingError(f"Failed to process historical data for {base}/{target}") from e

    def convert_currency(self, amount, from_curr, to_curr):
        if from_curr == to_curr:
            return amount, "N/A"
            
        try:
            data = self.api.get_latest_rate(from_curr, to_curr)
            rate = float(data.get("close", data.get("previous_close", 1.0)))
            date_str = data.get("datetime", "Unknown")
            return amount * rate, date_str
        except Exception as e:
            raise e
            
    def get_available_currencies(self):
        from config import DEFAULT_CURRENCIES
        return {c: c for c in DEFAULT_CURRENCIES}

    @staticmethod
    def calculate_technical_indicators(df, target_col):
        """Calculates basic technical indicators locally to save API calls."""
        import numpy as np
        if df is None or df.empty or len(df) < 2:
            return {"RSI": "N/A", "SMA_20": "N/A", "SMA_50": "N/A", "MACD": "N/A", "RSI_Label": "N/A"}
            
        try:
            # RSI (14 day)
            delta = df[target_col].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            # SMA
            sma20 = df[target_col].rolling(window=20).mean().iloc[-1]
            sma50 = df[target_col].rolling(window=50).mean().iloc[-1]
            
            # MACD (12, 26)
            ema12 = df[target_col].ewm(span=12, adjust=False).mean()
            ema26 = df[target_col].ewm(span=26, adjust=False).mean()
            macd = ema12 - ema26
            current_macd = macd.iloc[-1]
            
            rsi_label = "Neutral"
            if not np.isnan(current_rsi):
                if current_rsi > 70: rsi_label = "Overbought"
                elif current_rsi < 30: rsi_label = "Oversold"
                
            return {
                "RSI": round(current_rsi, 2) if not np.isnan(current_rsi) else "N/A",
                "SMA_20": round(sma20, 4) if not np.isnan(sma20) else "N/A",
                "SMA_50": round(sma50, 4) if not np.isnan(sma50) else "N/A",
                "MACD": round(current_macd, 4) if not np.isnan(current_macd) else "N/A",
                "RSI_Label": rsi_label
            }
        except Exception:
            return {"RSI": "N/A", "SMA_20": "N/A", "SMA_50": "N/A", "MACD": "N/A", "RSI_Label": "N/A"}

    @staticmethod
    def calculate_market_metrics(df, target_col):
        """Calculates high, low, average, volatility for a given dataframe."""
        if df is None or df.empty:
            return {}
        try:
            current = df[target_col].iloc[-1]
            oldest = df[target_col].iloc[0]
            pct_change = ((current - oldest) / oldest) * 100
            
            return {
                "Current": current,
                "High": df[target_col].max(),
                "Low": df[target_col].min(),
                "Average": df[target_col].mean(),
                "Change_Pct": pct_change,
                "Volatility": df[target_col].pct_change().std() * 100
            }
        except Exception:
            return {}
