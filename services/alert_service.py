# services/alert_service.py
class AlertService:
    """
    Generates alerts based on risk analysis results.
    """
    @staticmethod
    def generate_alerts(analysis_results, currency_pair):
        """
        Returns a list of alert dictionaries: {"type": "HIGH|MEDIUM|LOW|INFO", "message": str}
        """
        alerts = []
        if not analysis_results:
            return alerts
            
        pct_change = analysis_results["pct_change"]
        volatility = analysis_results["volatility"]
        label = analysis_results["risk_label"]
        trend = analysis_results["trend"]
        
        # Risk level alert
        if label == "HIGH RISK":
            alerts.append({"type": "HIGH", "message": f"{currency_pair} is showing HIGH volatility or large movements."})
        elif label == "MEDIUM RISK":
            alerts.append({"type": "MEDIUM", "message": f"{currency_pair} has moderate risk characteristics."})
            
        # Movement alerts
        if pct_change > 1.5:
            alerts.append({"type": "INFO", "message": f"Strong upward movement detected in {currency_pair} (+{pct_change:.2f}%)."})
        elif pct_change < -1.5:
            alerts.append({"type": "INFO", "message": f"Strong downward movement detected in {currency_pair} ({pct_change:.2f}%)."})
            
        # Stability alert
        if trend == "Stable" and volatility < 0.3:
            alerts.append({"type": "LOW", "message": f"{currency_pair} is currently showing relatively stable movement."})
            
        return alerts
