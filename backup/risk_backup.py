import time
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import *

def render():
    st.markdown("""
    <div class='cg-hero'>
        <h1 style='margin:0; font-size:1.85rem; color:var(--text-main);'>Quantitative FX Risk & Hedging Engine</h1>
        <p style='margin:4px 0 0 0; color:var(--text-muted); font-size:0.95rem;'>
            Evaluate Value-at-Risk (VaR), annualized volatility, maximum drawdown, and simulate commercial invoice downside exposure.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        r_base = st.selectbox("Portfolio Base Currency", list(CURRENCY_METADATA.keys()), index=0, format_func=format_currency_label)
    with rc2:
        r_foreign = st.selectbox("Foreign Currency Exposure", [c for c in CURRENCY_METADATA.keys() if c != r_base], index=0, format_func=format_currency_label)
    with rc3:
        r_history_window = st.selectbox("Historical Window for Modeling", ["30 Days", "90 Days", "180 Days", "365 Days"], index=1)
    
    r_days = int(r_history_window.split()[0])
    df_risk = fetch_frankfurter_timeseries(r_base, r_foreign, days=r_days)
    metrics = calculate_risk_metrics(df_risk)
    
    rm1, rm2, rm3, rm4 = st.columns(4)
    with rm1:
        st.markdown(f"""
        <div class='cg-card'>
            <div class='cg-rate-label'>ANNUALIZED VOLATILITY</div>
            <div class='cg-rate-val' style='color:#d97706;'>{metrics["volatility_pct"]}%</div>
            <div style='font-size:0.75rem; color:var(--text-muted);'>252-day scaled std dev</div>
        </div>
        """, unsafe_allow_html=True)
    with rm2:
        st.markdown(f"""
        <div class='cg-card'>
            <div class='cg-rate-label'>1-DAY 95% VaR</div>
            <div class='cg-rate-val' style='color:#dc2626;'>{metrics["var_95"]}%</div>
            <div style='font-size:0.75rem; color:var(--text-muted);'>95% confidence max daily loss</div>
        </div>
        """, unsafe_allow_html=True)
    with rm3:
        st.markdown(f"""
        <div class='cg-card'>
            <div class='cg-rate-label'>1-DAY 99% VaR</div>
            <div class='cg-rate-val' style='color:#dc2626;'>{metrics["var_99"]}%</div>
            <div style='font-size:0.75rem; color:var(--text-muted);'>Severe stress threshold</div>
        </div>
        """, unsafe_allow_html=True)
    with rm4:
        st.markdown(f"""
        <div class='cg-card'>
            <div class='cg-rate-label'>MAX HISTORICAL DRAWDOWN</div>
            <div class='cg-rate-val' style='color:var(--text-main);'>{metrics["max_drawdown"]}%</div>
            <div style='font-size:0.75rem; color:var(--text-muted);'>Peak-to-trough decline</div>
        </div>
        """, unsafe_allow_html=True)
    
