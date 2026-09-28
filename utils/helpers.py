"""
Utility Helpers for CurrencyGuard
Modern Blue & Red Fluent Physical Design System & Formatting Utilities
"""

import streamlit as st
from datetime import datetime, timedelta

def get_date_range(days: int):
    """Returns start_date and end_date strings in YYYY-MM-DD format."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def generate_css():
    """Returns modern Blue & Red Fluent Physical Theme CSS."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    .stApp {
        background-color: #f8fafc !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.04) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(225, 29, 72, 0.04) 0px, transparent 50%) !important;
        color: #0f172a !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 65%, #eff6ff 100%) !important;
        border-right: 1px solid #cbd5e1 !important;
    }
    
    .metric-card, .cg-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 4px 20px -2px rgba(29, 78, 216, 0.07), 0 2px 8px -1px rgba(225, 29, 72, 0.05);
        color: #0f172a;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
    }
    .metric-card:hover, .cg-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px -4px rgba(29, 78, 216, 0.15), 0 6px 14px -2px rgba(225, 29, 72, 0.10);
    }
    </style>
    """

def render_physics_background():
    """Safe no-op for fluent light theme to maintain compatibility with legacy callers."""
    pass
