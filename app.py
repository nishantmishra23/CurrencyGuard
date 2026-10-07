import os
import time
import math
import requests
import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CurrencyGuard | Financial Risk Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "📊 Dashboard"


def get_theme_css(theme: str) -> str:
    if theme == "light":
        return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

:root {
    --bg-main: #F1F5F9;
    --bg-card: #FFFFFF;
    --bg-card-subtle: #F8FAFC;
    --border-color: #E2E8F0;
    --border-highlight: #CBD5E1;
    --text-main: #0F172A;
    --text-muted: #475569;
    --text-dim: #64748B;
    --hero-bg: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 50%, #F8FAFC 100%);
    --sidebar-bg: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 65%, #F1F5F9 100%);
    --sidebar-border: #E2E8F0;

    --primary-blue: #2563EB;
    --accent-blue: #1D4ED8;
    --blue-light: #EFF6FF;
    --blue-border: #BFDBFE;

    --primary-red: #E11D48;
    --accent-red: #BE123C;
    --red-light: #FFF1F2;
    --red-border: #FECDD3;

    --emerald-green: #059669;
    --emerald-bg: #ECFDF5;
    --emerald-border: #A7F3D0;
    --amber-gold: #D97706;
    --amber-bg: #FFFBEB;
    --amber-border: #FDE68A;

    --btn-secondary-bg: #FFFFFF;
    --btn-secondary-border: #E2E8F0;
    --btn-secondary-text: #334155;
    --btn-secondary-hover-bg: #F8FAFC;

    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 16px -2px rgba(37, 99, 235, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04);
    --shadow-lg: 0 10px 25px -4px rgba(37, 99, 235, 0.12), 0 4px 10px -2px rgba(0, 0, 0, 0.06);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--text-main);
}

.stApp {
    background-color: var(--bg-main) !important;
    background-image: 
        radial-gradient(circle at 10% 10%, rgba(37, 99, 235, 0.03) 0%, transparent 40%),
        radial-gradient(circle at 90% 90%, rgba(225, 29, 72, 0.03) 0%, transparent 40%) !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
    width: 100% !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0.85rem !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text-main) !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em;
}

.cg-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: var(--shadow-md);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    color: var(--text-main);
}
.cg-card:hover {
    border-color: var(--primary-blue);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.cg-hero {
    background: var(--hero-bg);
    border: 1px solid var(--border-color);
    border-left: 5px solid var(--primary-blue);
    border-right: 5px solid var(--accent-blue);
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 14px;
    box-shadow: var(--shadow-md);
    position: relative;
}

.cg-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 16px;
    font-size: 0.76rem;
    font-weight: 700;
    line-height: 1;
}
.cg-badge-blue {
    background-color: var(--blue-light);
    color: var(--primary-blue);
    border: 1px solid var(--blue-border);
}
.cg-badge-red {
    background-color: var(--red-light);
    color: var(--primary-red);
    border: 1px solid var(--red-border);
}
.cg-badge-green {
    background-color: var(--emerald-bg);
    color: var(--emerald-green);
    border: 1px solid var(--emerald-border);
}
.cg-badge-amber {
    background-color: var(--amber-bg);
    color: var(--amber-gold);
    border: 1px solid var(--amber-border);
}

.cg-rate-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.035em;
}
.cg-rate-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}

[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--sidebar-border) !important;
}

.cg-brand-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: var(--shadow-sm);
    border-left: 4px solid var(--primary-blue);
}

/* Sidebar Navigation Buttons */
[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
    margin-bottom: 3px !important;
    text-align: left !important;
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #1D4ED8 !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.30) !important;
    transform: translateX(3px) !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
    background: var(--btn-secondary-bg) !important;
    color: var(--btn-secondary-text) !important;
    border: 1px solid var(--btn-secondary-border) !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
    background: var(--btn-secondary-hover-bg) !important;
    color: var(--text-main) !important;
    border-color: var(--primary-blue) !important;
    transform: translateX(2px) !important;
}

/* Primary buttons in main view */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
}

.beacon-blue {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #2563EB;
    display: inline-block;
    vertical-align: middle;
    margin-right: 6px;
}
.beacon-red {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #E11D48;
    display: inline-block;
    vertical-align: middle;
    margin-right: 6px;
}

div[role="radiogroup"] label > div:first-of-type,
div[role="radiogroup"] input[type="radio"] {
    display: none !important;
}
</style>
"""
    else:

        return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

:root {
    --bg-main: #0B0D17;
    --bg-card: #141724;
    --bg-card-subtle: #1C2033;
    --border-color: #242942;
    --border-highlight: #3A426B;
    --text-main: #F8FAFC;
    --text-muted: #CBD5E1;
    --text-dim: #94A3B8;
    --hero-bg: linear-gradient(135deg, #131524 0%, #1A1636 50%, #151124 100%);
    --sidebar-bg: linear-gradient(180deg, #0A0D14 0%, #111421 65%, #151829 100%);
    --sidebar-border: #1E233B;

    --primary-blue: #7C3AED;
    --accent-blue: #6D28D9;
    --blue-light: #2E1B59;
    --blue-border: #4C1D95;

    --primary-red: #F43F5E;
    --accent-red: #E11D48;
    --red-light: #4C1525;
    --red-border: #881337;

    --emerald-green: #10B981;
    --emerald-bg: #064E3B;
    --emerald-border: #047857;
    --amber-gold: #F59E0B;
    --amber-bg: #78350F;
    --amber-border: #B45309;

    --btn-secondary-bg: #141724;
    --btn-secondary-border: #242942;
    --btn-secondary-text: #CBD5E1;
    --btn-secondary-hover-bg: #1C2033;

    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
    --shadow-md: 0 4px 20px -2px rgba(124, 58, 237, 0.15), 0 2px 8px -1px rgba(0, 0, 0, 0.5);
    --shadow-lg: 0 14px 30px -4px rgba(124, 58, 237, 0.25), 0 6px 14px -2px rgba(0, 0, 0, 0.6);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--text-main);
}

.stApp {
    background-color: var(--bg-main) !important;
    background-image: 
        radial-gradient(circle at 15% 10%, rgba(124, 58, 237, 0.1) 0%, transparent 40%),
        radial-gradient(circle at 85% 90%, rgba(59, 130, 246, 0.08) 0%, transparent 40%) !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
    width: 100% !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0.85rem !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em;
}

.cg-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: var(--shadow-md);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    color: var(--text-main);
}
.cg-card:hover {
    border-color: var(--primary-blue);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.cg-hero {
    background: var(--hero-bg);
    border: 1px solid var(--border-color);
    border-left: 5px solid var(--primary-blue);
    border-right: 5px solid var(--accent-blue);
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 14px;
    box-shadow: var(--shadow-md);
    position: relative;
}

.cg-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 16px;
    font-size: 0.76rem;
    font-weight: 700;
    line-height: 1;
}
.cg-badge-blue {
    background-color: var(--blue-light);
    color: #A78BFA;
    border: 1px solid var(--blue-border);
}
.cg-badge-red {
    background-color: var(--red-light);
    color: var(--primary-red);
    border: 1px solid var(--red-border);
}
.cg-badge-green {
    background-color: var(--emerald-bg);
    color: var(--emerald-green);
    border: 1px solid var(--emerald-border);
}
.cg-badge-amber {
    background-color: var(--amber-bg);
    color: var(--amber-gold);
    border: 1px solid var(--amber-border);
}

.cg-rate-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.85rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.035em;
}
.cg-rate-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}

[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--sidebar-border) !important;
}

.cg-brand-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: var(--shadow-sm);
    border-left: 4px solid var(--primary-blue);
}

/* Sidebar Navigation Buttons */
[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
    margin-bottom: 3px !important;
    text-align: left !important;
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #8B5CF6 !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35) !important;
    transform: translateX(3px) !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
    background: var(--btn-secondary-bg) !important;
    color: var(--btn-secondary-text) !important;
    border: 1px solid var(--btn-secondary-border) !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
    background: var(--btn-secondary-hover-bg) !important;
    color: var(--text-main) !important;
    border-color: var(--primary-blue) !important;
    transform: translateX(2px) !important;
}

/* Primary buttons in main view */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3) !important;
}

.beacon-blue {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #8B5CF6;
    display: inline-block;
    vertical-align: middle;
    margin-right: 6px;
}
.beacon-red {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #F43F5E;
    display: inline-block;
    vertical-align: middle;
    margin-right: 6px;
}

div[role="radiogroup"] label > div:first-of-type,
div[role="radiogroup"] input[type="radio"] {
    display: none !important;
}
</style>
"""

st.markdown(get_theme_css(st.session_state["theme"]), unsafe_allow_html=True)


with st.sidebar:

    st.markdown("""
    <div class='cg-brand-card'>
        <div style='display:flex; align-items:center; gap:10px;'>
            <div style='font-size:1.8rem; line-height:1; filter:drop-shadow(0 2px 4px rgba(37,99,235,0.3));'>🛡️</div>
            <div>
                <div style='font-size:1.15rem; font-weight:800; letter-spacing:-0.03em; color:var(--text-main); line-height:1.1;'>
                    CURRENCY<span style='color:var(--primary-red);'>GUARD</span>
                </div>
                <div style='font-size:0.75rem; color:var(--text-muted); font-weight:600; margin-top:2px;'>
                    Dual-Engine FX Intelligence
                </div>
            </div>
        </div>
        <div style='display:flex; gap:6px; margin-top:10px;'>
            <span class='cg-badge cg-badge-blue' style='font-size:0.72rem; padding:3px 8px;'>🇮🇳 INR Base</span>
            <span class='cg-badge cg-badge-red' style='font-size:0.72rem; padding:3px 8px;'>🛡️ Risk Engine</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    theme_is_dark = (st.session_state.theme == "dark")
    theme_btn_text = "☀️ Switch to Light Theme" if theme_is_dark else "🌙 Switch to Dark Theme"
    if st.button(theme_btn_text, use_container_width=True, key="theme_toggle_btn"):
        st.session_state.theme = "light" if theme_is_dark else "dark"
        st.rerun()

    st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center; margin:14px 4px 8px 4px;'>
        <span style='font-size:0.75rem; font-weight:800; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.08em;'>NAVIGATION</span>
        <span class='cg-badge cg-badge-blue' style='font-size:0.68rem; padding:2px 7px;'>6 MODULES</span>
    </div>
    """, unsafe_allow_html=True)

    nav_pages = [
        "📊 Dashboard",
        "💱 Currency Converter",
        "📈 Market Trends",
        "🔔 Alerts & Signals",
        "🌐 Currency Explorer",
        "ℹ️ Architecture & About",
    ]

    for p in nav_pages:
        is_sel = (st.session_state.current_page == p)
        if st.button(p, key=f"nav_btn_{p}", use_container_width=True, type="primary" if is_sel else "secondary"):
            st.session_state.current_page = p
            st.rerun()

    menu = st.session_state.current_page

    st.markdown("""
    <div style='font-size:0.75rem; font-weight:700; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.08em; margin:14px 4px 6px 4px;'>
        LIVE PIPELINE TELEMETRY
    </div>
    <div style='background:var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:12px; box-shadow:var(--shadow-sm);'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
            <div style='display:flex; align-items:center; font-size:0.82rem; font-weight:700; color:var(--text-main);'>
                <span class='beacon-blue'></span>Twelve Data
            </div>
            <span class='cg-badge cg-badge-blue' style='font-size:0.7rem; padding:2px 8px;'>Live Keyed</span>
        </div>
        <div style='display:flex; justify-content:space-between; align-items:center; padding-top:6px; border-top:1px solid var(--border-color);'>
            <div style='display:flex; align-items:center; font-size:0.82rem; font-weight:700; color:var(--text-main);'>
                <span class='beacon-red'></span>Frankfurter ECB
            </div>
            <span class='cg-badge cg-badge-red' style='font-size:0.7rem; padding:2px 8px;'>Direct Open</span>
        </div>
        <div style='font-size:0.75rem; color:var(--text-muted); margin-top:6px; padding-top:6px; border-top:1px dashed var(--border-color);'>
            <b>Primary Base:</b> INR (India) ₹
        </div>
    </div>
    <div style='margin-top:10px;'></div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Refresh Market Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("<div style='font-size:0.72rem; color:var(--text-dim); text-align:center; margin-top:14px; font-weight:500;'>CurrencyGuard • Fintech Edition</div>", unsafe_allow_html=True)


import views.dashboard
import views.converter
import views.trends
import views.alerts
import views.explorer
import views.about

if menu == "📊 Dashboard":
    views.dashboard.render()
elif menu == "💱 Currency Converter":
    views.converter.render()
elif menu == "📈 Market Trends":
    views.trends.render()
elif menu == "🔔 Alerts & Signals":
    views.alerts.render()
elif menu == "🌐 Currency Explorer":
    views.explorer.render()
elif menu == "ℹ️ Architecture & About":
    views.about.render()
