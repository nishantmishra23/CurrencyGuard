import time
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import *

def render():
    st.markdown("""
    <div class='cg-hero'>
        <h1 style='margin:0; font-size:1.85rem; color:var(--text-main);'>Intelligent Alerts & Volatility Signals</h1>
        <p style='margin:4px 0 0 0; color:var(--text-muted); font-size:0.95rem;'>
            Define rate threshold triggers, monitor intraday volatility spikes, and export rules for algorithmic monitoring.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if "user_alerts" not in st.session_state:
        st.session_state.user_alerts = [
            {"pair": "USD/INR", "type": "Upper Ceiling", "threshold": 84.50, "active": True, "created": "2026-09-21"},
            {"pair": "USD/INR", "type": "Lower Floor", "threshold": 82.50, "active": True, "created": "2026-09-21"},
            {"pair": "EUR/INR", "type": "Upper Ceiling", "threshold": 92.00, "active": True, "created": "2026-09-21"},
            {"pair": "GBP/INR", "type": "Volatility Spike (>1.2%)", "threshold": 108.00, "active": True, "created": "2026-09-21"},
        ]
    
    al_col1, al_col2 = st.columns([5, 7])
    
    with al_col1:
        st.markdown("### ➕ Create New Alert Rule")
        with st.form("new_alert_form"):
            a_pair = st.selectbox("Select Currency Pair", ["USD/INR", "EUR/INR", "GBP/INR", "AED/INR", "EUR/USD", "GBP/USD", "USD/JPY"])
            a_type = st.selectbox("Alert Condition", ["Upper Ceiling (Rate >= Threshold)", "Lower Floor (Rate <= Threshold)", "Rapid Volatility (> 1.2% Daily)"])
    
            base_p, quote_p = a_pair.split("/")
            cur_p_rate = get_cross_rate(base_p, quote_p)
    
            a_thresh = st.number_input("Threshold Rate", value=float(round(cur_p_rate * 1.02, 4)), step=0.001, format="%.4f")
    
            submitted = st.form_submit_button("🔔 Register Alert Rule")
            if submitted:
                st.session_state.user_alerts.append({
                    "pair": a_pair,
                    "type": a_type.split("(")[0].strip(),
                    "threshold": a_thresh,
                    "active": True,
                    "created": str(datetime.date.today())
                })
                st.success(f"Alert rule for {a_pair} registered successfully!")
                st.rerun()
    
    with al_col2:
        st.markdown("### 📋 Active Monitoring Rulebook")
    
        alerts_display = []
        for idx, alt in enumerate(st.session_state.user_alerts):
            base_c, quote_c = alt["pair"].split("/")
            curr_rate = get_cross_rate(base_c, quote_c)
            thresh = alt["threshold"]
    
            is_triggered = False
            if "Upper" in alt["type"] and curr_rate >= thresh:
                is_triggered = True
            elif "Lower" in alt["type"] and curr_rate <= thresh:
                is_triggered = True
    
            status = "🚨 TRIGGERED" if is_triggered else "🟢 WATCHING"
    
            alerts_display.append({
                "Pair": alt["pair"],
                "Condition": alt["type"],
                "Target Threshold": thresh,
                "Current Live Rate": round(curr_rate, 4),
                "Status": status,
                "Created": alt["created"]
            })
    
        df_alerts = pd.DataFrame(alerts_display)
        st.dataframe(df_alerts, use_container_width=True, hide_index=True)
    
        csv_data = df_alerts.to_csv(index=False)
        st.download_button(
            label="📥 Export Alert Rulebook (CSV)",
            data=csv_data,
            file_name="currencyguard_alerts.csv",
            mime="text/csv"
        )
    
