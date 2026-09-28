# services/risk_analyzer.py
import numpy as np
import pandas as pd

class RiskAnalyzer:
    """
    Analyzes historical currency data to determine risk levels based on volatility and trends.
    """
    @staticmethod
    def calculate_percentage_change(current_rate, previous_rate):
        if previous_rate == 0:
            return 0.0
        return ((current_rate - previous_rate) / previous_rate) * 100

    @staticmethod
    def calculate_volatility(series):
        """Calculate historical volatility (standard deviation of daily percentage changes)."""
        if len(series) < 2:
            return 0.0
        pct_changes = series.pct_change().dropna()
        return np.std(pct_changes) * 100  # as percentage

    @staticmethod
    def determine_trend(series):
        if len(series) < 2:
            return "Stable"
        first = series.iloc[0]
        last = series.iloc[-1]
        pct_change = RiskAnalyzer.calculate_percentage_change(last, first)
        
        if pct_change > 1.0:
            return "Rising"
        elif pct_change < -1.0:
            return "Falling"
        return "Stable"

    @staticmethod
    def assess_risk(volatility, recent_pct_change):
        """
        Rule-based risk model. Returns a score out of 100 and a label.
        """
        abs_change = abs(recent_pct_change)
        score = 0
        
        # Volatility factor (max 50 points)
        if volatility < 0.2:
            score += 10
        elif volatility < 0.5:
            score += 25
        elif volatility < 1.0:
            score += 40
        else:
            score += 50
            
        # Recent movement factor (max 50 points)
        if abs_change < 0.5:
            score += 10
        elif abs_change < 1.5:
            score += 25
        elif abs_change < 3.0:
            score += 40
        else:
            score += 50
            
        # Labeling
        if score < 40:
            label = "LOW RISK"
        elif score < 75:
            label = "MEDIUM RISK"
        else:
            label = "HIGH RISK"
            
        return score, label

    @staticmethod
    def analyze_pair(df, currency):
        """
        Analyzes a specific currency column from a dataframe.
        """
        if df.empty or currency not in df.columns:
            return None
            
        series = df[currency].dropna()
        if len(series) < 2:
            return None
            
        current = float(series.iloc[-1])
        previous = float(series.iloc[-2])
        
        pct_change = RiskAnalyzer.calculate_percentage_change(current, previous)
        volatility = float(RiskAnalyzer.calculate_volatility(series))
        trend = RiskAnalyzer.determine_trend(series)
        score, label = RiskAnalyzer.assess_risk(volatility, pct_change)
        
        return {
            "current_rate": current,
            "previous_rate": previous,
            "pct_change": pct_change,
            "volatility": volatility,
            "trend": trend,
            "risk_score": score,
            "risk_label": label
        }
