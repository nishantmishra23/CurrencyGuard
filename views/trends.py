import time
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import *

def render():
    st.markdown("""
    <div class='cg-hero'>
        <h1 style='margin:0; font-size:1.85rem; color:var(--text-main);'>Market Trends & Technical Intelligence</h1>
        <p style='margin:4px 0 0 0; color:var(--text-muted); font-size:0.95rem;'>
            High-precision historical charts powered by direct <b>Frankfurter ECB API</b> with technical moving averages (SMA 20/50) and Bollinger Bands.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tc1, tc2, tc3, tc4 = st.columns([3, 3, 3, 3])
    with tc1:
        t_base = st.selectbox("Base Currency", list(CURRENCY_METADATA.keys()), index=1, format_func=format_currency_label)
    with tc2:
        t_quote = st.selectbox("Quote Currency", [c for c in CURRENCY_METADATA.keys() if c != t_base], index=0, format_func=format_currency_label)
    with tc3:
        timeframe = st.selectbox("Select Timeframe", ["7 Days", "30 Days", "90 Days", "1 Year (365D)", "5 Years"], index=1)
    with tc4:
        chart_type = st.selectbox("Technical Overlay", ["SMA 20 & SMA 50", "Bollinger Bands", "Clean Line Only"], index=0)
    
    days_map = {
        "7 Days": 7,
        "30 Days": 30,
        "90 Days": 90,
        "1 Year (365D)": 365,
        "5 Years": 1825
    }
    num_days = days_map.get(timeframe, 30)
    
    with st.spinner(f"Loading ECB historical data for {t_base}/{t_quote}..."):
        df_trends = fetch_frankfurter_timeseries(t_base, t_quote, days=num_days)
    
    if not df_trends.empty:
        df_calc = add_technical_indicators(df_trends)
    
        curr_rate = df_calc["rate"].iloc[-1]
        min_rate = df_calc["rate"].min()
        max_rate = df_calc["rate"].max()
        first_rate = df_calc["rate"].iloc[0]
        period_chg = ((curr_rate - first_rate) / first_rate) * 100
        spread = max_rate - min_rate
    
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class='cg-card'>
                <div class='cg-rate-label'>CURRENT RATE</div>
                <div class='cg-rate-val'>{curr_rate:.4f}</div>
                <div style='font-size:0.75rem; color:var(--text-muted);'>Latest quote</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class='cg-card'>
                <div class='cg-rate-label'>PERIOD CHANGE</div>
                <div class='cg-rate-val' style='color:{"#059669" if period_chg >= 0 else "#dc2626"}'>
                    {"+" if period_chg >= 0 else ""}{period_chg:.2f}%
                </div>
                <div style='font-size:0.75rem; color:var(--text-muted);'>Across {timeframe}</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class='cg-card'>
                <div class='cg-rate-label'>PERIOD HIGH / LOW</div>
                <div style='font-size:1.15rem; font-weight:700; color:var(--text-main); margin-top:4px;'>
                    <span style='color:#059669;'>H: {max_rate:.4f}</span> | <span style='color:#dc2626;'>L: {min_rate:.4f}</span>
                </div>
                <div style='font-size:0.75rem; color:var(--text-muted); margin-top:4px;'>Range bounds</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class='cg-card'>
                <div class='cg-rate-label'>PERIOD SPREAD</div>
                <div class='cg-rate-val' style='color:var(--primary-blue);'>{spread:.4f}</div>
                <div style='font-size:0.75rem; color:var(--text-muted);'>High - Low Delta</div>
            </div>
            """, unsafe_allow_html=True)
    
        pass  # Chart removed per user request
    
