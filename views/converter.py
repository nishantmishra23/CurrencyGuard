import time
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import *

def render():
    st.markdown("""
    <div class='cg-hero'>
        <h1 style='margin:0; font-size:1.85rem; color:var(--text-main);'>Smart Multi-Currency Converter</h1>
        <p style='margin:4px 0 0 0; color:var(--text-muted); font-size:0.95rem;'>
            Live interbank conversions powered by <b>Twelve Data</b> and <b>Frankfurter ECB</b> with instant multi-target payout calculation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 6])
    
    with col1:
        st.markdown("### 🧮 Primary Live Conversion")
        with st.container():
            c_amt = st.number_input("Enter Amount to Convert", min_value=1.0, value=10000.0, step=500.0)
    
            c_row1, c_row2 = st.columns(2)
            with c_row1:
                c_from = st.selectbox("Source Currency (From)", list(CURRENCY_METADATA.keys()), index=0, format_func=format_currency_label)
            with c_row2:
                c_to = st.selectbox("Target Currency (To)", list(CURRENCY_METADATA.keys()), index=1, format_func=format_currency_label)
    
            rate = get_cross_rate(c_from, c_to)
            total = c_amt * rate
            inv_rate = 1.0 / rate if rate != 0 else 0.0
    
            sym_from = CURRENCY_METADATA.get(c_from, {}).get("symbol", "")
            sym_to = CURRENCY_METADATA.get(c_to, {}).get("symbol", "")
    
            st.markdown(f"""
            <div class='cg-card' style='margin-top:10px;'>
                <div style='font-size:0.82rem; font-weight:700; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.05em;'>LIVE INTERBANK RESULT</div>
                <div style='font-size:2.2rem; font-weight:800; color:var(--text-main); font-family:"JetBrains Mono"; margin:6px 0;'>
                    {sym_to} {total:,.2f} <span style='font-size:1.1rem; color:var(--primary-blue);'>{c_to}</span>
                </div>
                <div style='font-size:0.9rem; color:var(--text-muted); font-weight:600; margin-bottom:10px;'>
                    {sym_from} {c_amt:,.2f} {c_from} = {sym_to} {total:,.2f} {c_to}
                </div>
                <div style='display:flex; gap:16px; font-size:0.82rem; color:var(--text-muted); border-top:1px solid var(--border-color); padding-top:10px;'>
                    <span><b>1 {c_from}</b> = {rate:.4f} {c_to}</span>
                    <span>•</span>
                    <span><b>1 {c_to}</b> = {inv_rate:.4f} {c_from}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Pair Market Specifications")
        st.markdown("<p style='font-size:0.85rem; color:var(--text-muted); margin-top:-8px;'>Live currency pair attributes and interbank exchange parameters.</p>", unsafe_allow_html=True)
    
        meta_from = CURRENCY_METADATA.get(c_from, {})
        meta_to = CURRENCY_METADATA.get(c_to, {})
    
        st.markdown(f"""
        <div class='cg-card' style='margin-top:10px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid var(--border-color);'>
                <span style='font-weight:800; font-size:1.05rem; color:var(--text-main);'>{c_from} / {c_to} Pair Profile</span>
                <span class='cg-badge cg-badge-blue'>Mid-Market Spot</span>
            </div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:12px;'>
                <div>
                    <div style='font-size:0.75rem; color:var(--text-dim); text-transform:uppercase;'>Base Currency</div>
                    <div style='font-weight:700; color:var(--text-main); font-size:0.92rem;'>{meta_from.get('name', c_from)} ({meta_from.get('symbol', '')})</div>
                    <div style='font-size:0.78rem; color:var(--text-muted);'>{meta_from.get('country', '')} • {meta_from.get('bank', '')}</div>
                </div>
                <div>
                    <div style='font-size:0.75rem; color:var(--text-dim); text-transform:uppercase;'>Quote Currency</div>
                    <div style='font-weight:700; color:var(--text-main); font-size:0.92rem;'>{meta_to.get('name', c_to)} ({meta_to.get('symbol', '')})</div>
                    <div style='font-size:0.78rem; color:var(--text-muted);'>{meta_to.get('country', '')} • {meta_to.get('bank', '')}</div>
                </div>
            </div>
            <div style='background:var(--bg-card-subtle); border-radius:8px; padding:10px; font-size:0.82rem; color:var(--text-muted);'>
                <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                    <span>Direct Rate:</span>
                    <b>1 {c_from} = {rate:.4f} {c_to}</b>
                </div>
                <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                    <span>Inverse Rate:</span>
                    <b>1 {c_to} = {inv_rate:.4f} {c_from}</b>
                </div>
                <div style='display:flex; justify-content:space-between;'>
                    <span>Pricing Model:</span>
                    <span style='color:var(--primary-blue); font-weight:700;'>Interbank Zero-Spread Benchmark</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
