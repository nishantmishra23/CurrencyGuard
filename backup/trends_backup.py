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
    
        fig = go.Figure()
    
        fig.add_trace(go.Scatter(
            x=df_calc["date"],
            y=df_calc["rate"],
            mode="lines",
            name=f"{t_base}/{t_quote} Rate",
            line=dict(color="#2563eb", width=2.5),
        ))
    
        if chart_type == "SMA 20 & SMA 50":
            fig.add_trace(go.Scatter(
                x=df_calc["date"],
                y=df_calc["sma_20"],
                mode="lines",
                name="SMA 20",
                line=dict(color="#d97706", width=1.5, dash="dot"),
            ))
            fig.add_trace(go.Scatter(
                x=df_calc["date"],
                y=df_calc["sma_50"],
                mode="lines",
                name="SMA 50",
                line=dict(color="#7c3aed", width=1.5, dash="dash"),
            ))
        elif chart_type == "Bollinger Bands":
            fig.add_trace(go.Scatter(
                x=df_calc["date"],
                y=df_calc["bb_upper"],
                mode="lines",
                name="Upper Band",
                line=dict(color="#94a3b8", width=1, dash="dash"),
            ))
            fig.add_trace(go.Scatter(
                x=df_calc["date"],
                y=df_calc["bb_lower"],
                mode="lines",
                name="Lower Band",
                line=dict(color="#94a3b8", width=1, dash="dash"),
                fill='tonexty',
                fillcolor='rgba(148, 163, 184, 0.15)'
            ))
    
        plotly_theme = "plotly_dark" if st.session_state.theme == "dark" else "plotly_white"
        fig.update_layout(
            title=f"Exchange Rate Trajectory: {t_base}/{t_quote} ({timeframe})",
            template=plotly_theme,
            xaxis_title="Date",
            yaxis_title=f"Exchange Rate ({t_quote})",
            height=440,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
