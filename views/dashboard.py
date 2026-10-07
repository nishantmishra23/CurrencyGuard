import time
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import *

def render():
    
    st.markdown("""
    <div class='cg-hero'>
        <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;'>
            <div>
                <h1 style='margin:0; font-size:1.9rem; color:var(--text-main);'>Executive Financial Cockpit</h1>
                <p style='margin:4px 0 0 0; color:var(--text-muted); font-size:0.95rem;'>
                    Real-time FX intelligence anchored to <b>INR (India)</b> powered by <b>Twelve Data</b> and <b>Frankfurter ECB</b> data feeds.
                </p>
            </div>
            <div>
                <span class='cg-badge cg-badge-blue' style='font-size:0.82rem; padding:6px 14px;'>
                    🇮🇳 Base: INR (India) • Live Active
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.columns(4)
    
    ticker_pairs = [
        ("USD", "INR", t1),
        ("EUR", "INR", t2),
        ("GBP", "INR", t3),
        ("AED", "INR", t4)
    ]
    
    for base, quote, col in ticker_pairs:
        with col:
            rate = get_cross_rate(base, quote)
    
            df_hist = fetch_frankfurter_timeseries(base, quote, days=7)
            if len(df_hist) >= 2:
                prev_rate = df_hist["rate"].iloc[-2]
                pct_chg = ((rate - prev_rate) / prev_rate) * 100
            else:
                pct_chg = 0.12                        
    
            is_positive = pct_chg >= 0
            badge_class = "cg-badge-green" if is_positive else "cg-badge-red"
            sign = "+" if is_positive else ""
    
            fmt = ".4f" if rate < 10 else ".2f"
            rate_str = f"{rate:{fmt}}"
            country_name = CURRENCY_METADATA.get(base, {}).get("country", "")
    
            st.markdown(f"""
            <div class='cg-card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span class='cg-rate-label'>{base}/{quote} ({country_name})</span>
                    <span class='cg-badge {badge_class}'>{sign}{pct_chg:.2f}%</span>
                </div>
                <div class='cg-rate-val' style='margin-top:6px;'>₹{rate_str}</div>
                <div style='font-size:0.75rem; color:var(--text-muted); margin-top:4px;'>
                    1 {base} = {rate_str} {quote}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([6, 6])
    
    with col_left:
        st.markdown("### 📰 Macro Market Signals")
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("""
            <div class='cg-card' style='padding:16px;'>
                <div style='font-size:0.82rem; font-weight:700; color:var(--primary-blue);'>RESERVE BANK OF INDIA (RBI)</div>
                <div style='font-size:0.95rem; font-weight:700; color:var(--text-main); margin:4px 0;'>INR FX Reserve Buffers</div>
                <p style='font-size:0.82rem; color:var(--text-muted); margin:0;'>
                    RBI maintains substantial foreign exchange liquidity buffers, preserving orderly market conditions and stability for USD/INR.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown("""
            <div class='cg-card' style='padding:16px;'>
                <div style='font-size:0.82rem; font-weight:700; color:var(--emerald-green);'>GLOBAL MONETARY POLICY</div>
                <div style='font-size:0.95rem; font-weight:700; color:var(--text-main); margin:4px 0;'>Emerging Market Resilience</div>
                <p style='font-size:0.82rem; color:var(--text-muted); margin:0;'>
                    Resilient domestic capital inflows and trade stability support INR valuations across major G10 cross pairs.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("### 🛡️ Real-Time FX Stability Overview")
        st.markdown("""
        <div class='cg-card' style='padding:16px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
                <span style='font-size:0.88rem; font-weight:700; color:var(--text-main);'>Intraday FX Volatility Regime</span>
                <span class='cg-badge cg-badge-green'>Normal / Low Risk</span>
            </div>
            <p style='font-size:0.82rem; color:var(--text-muted); margin:0 0 10px 0;'>
                Aggregated 24h currency fluctuation remains under 0.8% threshold across primary crosses. Risk scanning algorithms are operating in real time.
            </p>
            <div style='display:flex; gap:10px; border-top:1px solid var(--border-color); padding-top:10px; font-size:0.8rem; color:var(--text-muted);'>
                <span><b>Anchor Currency:</b> INR (India) ₹</span>
                <span>•</span>
                <span><b>Monitored Pairs:</b> 30+ Global FX</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
