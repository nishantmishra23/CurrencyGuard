import time
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import *

def render():
    st.markdown("""
    <div class='cg-hero'>
        <h1 style='margin:0; font-size:1.85rem; color:var(--text-main);'>Global Currency Explorer & Macro Profiles</h1>
        <p style='margin:4px 0 0 0; color:var(--text-muted); font-size:0.95rem;'>
            Explore 30+ world currencies, central bank institutions, macroeconomic profiles, and live valuations in <b>INR (India) ₹</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    e_col1, e_col2 = st.columns([4, 8])
    with e_col1:
        region_filter = st.selectbox("Filter by Global Region", ["All Regions", "Americas", "Europe", "Asia-Pacific", "Middle East & Africa"])
    with e_col2:
        search_query = st.text_input("🔍 Search Currency, Country, or Central Bank", placeholder="e.g. Yen, Switzerland, Federal Reserve...")
    
    filtered_currencies = {}
    for code, meta in CURRENCY_METADATA.items():
        if region_filter != "All Regions" and meta["region"] != region_filter:
            continue
        if search_query:
            query = search_query.lower()
            if (query not in code.lower() and 
                query not in meta["name"].lower() and 
                query not in meta["country"].lower() and 
                query not in meta["bank"].lower()):
                continue
        filtered_currencies[code] = meta
    
    st.markdown(f"##### Showing {len(filtered_currencies)} Currencies")
    
    grid_cols = st.columns(3)
    for idx, (code, meta) in enumerate(filtered_currencies.items()):
        col = grid_cols[idx % 3]
        with col:
            rate_vs_inr = get_cross_rate(code, "INR")
            fmt_r = ".2f" if rate_vs_inr > 1 else ".4f"
            st.markdown(f"""
            <div class='cg-card' style='padding:16px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:1.25rem; font-weight:800; color:var(--text-main);'>{code} ({meta['symbol']})</span>
                    <span class='cg-badge cg-badge-blue'>{meta['region']}</span>
                </div>
                <div style='font-size:0.95rem; font-weight:700; color:var(--primary-blue); margin:4px 0;'>{meta['name']}</div>
                <div style='font-size:0.82rem; color:var(--text-muted);'><b>Country:</b> {meta['country']}</div>
                <div style='font-size:0.82rem; color:var(--text-muted);'><b>Central Bank:</b> {meta['bank']}</div>
                <div style='margin-top:10px; padding-top:8px; border-top:1px solid var(--border-color); display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:0.8rem; color:var(--text-dim);'>Rate in INR (₹):</span>
                    <span style='font-size:0.92rem; font-weight:800; font-family:"JetBrains Mono"; color:var(--primary-blue);'>
                        1 {code} = ₹{rate_vs_inr:{fmt_r}}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
