import time
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import *

def render():
    st.markdown("""
    <div class='cg-hero'>
        <h1 style='margin:0; font-size:1.85rem; color:var(--text-main);'>System Architecture & Live API Monitor</h1>
        <p style='margin:4px 0 0 0; color:var(--text-muted); font-size:0.95rem;'>
            Technical blueprint, dual-engine data pipeline status, mathematical references, and zero-downtime resilience metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📡 Live API Engine Health Ping")
    st.markdown("<p style='font-size:0.85rem; color:var(--text-muted); margin-top:-8px;'>Test round-trip latency and payload validity for both data engines in real time.</p>", unsafe_allow_html=True)
    
    ping_col1, ping_col2 = st.columns(2)
    
    with ping_col1:
        if st.button("🧪 Ping Twelve Data Endpoint"):
            t_start = time.time()
            res = fetch_twelve_exchange_rate("EUR/USD")
            latency = (time.time() - t_start) * 1000
            if "rate" in res:
                st.success(f"Twelve Data Responded in {latency:.1f} ms • Live Rate: {res['rate']}")
            else:
                st.warning(f"Twelve Data call completed in {latency:.1f} ms (Fallback engaged)")
        else:
            st.info("Click above to test Twelve Data API latency.")
    
    with ping_col2:
        if st.button("🧪 Ping Frankfurter ECB Endpoint"):
            t_start = time.time()
            res = fetch_frankfurter_latest("USD")
            latency = (time.time() - t_start) * 1000
            if "rates" in res:
                st.success(f"Frankfurter Responded in {latency:.1f} ms • Currencies Loaded: {len(res['rates'])}")
            else:
                st.warning(f"Frankfurter call completed in {latency:.1f} ms (Fallback engaged)")
        else:
            st.info("Click above to test Frankfurter API latency.")
    
    st.divider()
    
    st.markdown("### 🏗️ Dual-Engine Data Pipeline")
    
    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""
        <div class='cg-card'>
            <div style='font-size:0.85rem; font-weight:700; color:var(--primary-blue);'>ENGINE 1: TWELVE DATA REST API</div>
            <div style='font-size:1.1rem; font-weight:700; color:var(--text-main); margin:6px 0;'>Live Interbank Quotes & Spreads</div>
            <ul style='font-size:0.85rem; color:var(--text-muted); padding-left:18px;'>
                <li><b>Role</b>: Powers live real-time currency conversions, top tickers, and intraday rates.</li>
                <li><b>Authentication</b>: Key-based via <code>.env</code> (TWELVEDATA_API_KEY).</li>
                <li><b>Optimization</b>: 120-second intelligent cache prevents free-tier quota exhaustion.</li>
                <li><b>Failover</b>: Seamlessly passes execution to Frankfurter if rate-limited.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class='cg-card'>
            <div style='font-size:0.85rem; font-weight:700; color:var(--emerald-green);'>ENGINE 2: FRANKFURTER OPEN API</div>
            <div style='font-size:1.1rem; font-weight:700; color:var(--text-main); margin:6px 0;'>Direct European Central Bank (ECB) Data</div>
            <ul style='font-size:0.85rem; color:var(--text-muted); padding-left:18px;'>
                <li><b>Role</b>: Powers historical time series, multi-currency tables, volatility, and VaR models.</li>
                <li><b>Authentication</b>: 100% Free & Open (Zero API keys required).</li>
                <li><b>Coverage</b>: Daily reference rates published by the European Central Bank.</li>
                <li><b>Dual Host Routing</b>: Automatically tries <code>api.frankfurter.dev</code> then <code>api.frankfurter.app</code>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📐 Quantitative Methodology & Formulations")
    st.markdown("""
    <div class='cg-card'>
        <div style='font-weight:700; color:var(--text-main); margin-bottom:8px;'>1. Parametric Value at Risk (VaR)</div>
        <p style='font-size:0.85rem; color:var(--text-muted);'>
            <code>VaR(α) = - (μ - Z_α * σ)</code><br>
            Where <code>μ</code> is the mean daily log return, <code>σ</code> is daily standard deviation, and <code>Z_0.95 = 1.645</code> (or <code>Z_0.99 = 2.326</code>).
        </p>
        <div style='font-weight:700; color:var(--text-main); margin-top:12px; margin-bottom:8px;'>2. Annualized Volatility</div>
        <p style='font-size:0.85rem; color:var(--text-muted);'>
            <code>σ_annual = σ_daily * sqrt(252) * 100</code><br>
            Scaling standard deviation over 252 international market trading days.
        </p>
        <div style='font-weight:700; color:var(--text-main); margin-top:12px; margin-bottom:8px;'>3. Bollinger Bands</div>
        <p style='font-size:0.85rem; color:var(--text-muted);'>
            <code>Upper = SMA_20 + (2 * σ_20)</code> | <code>Lower = SMA_20 - (2 * σ_20)</code>
        </p>
    </div>
    """, unsafe_allow_html=True)
