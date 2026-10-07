# ==============================================================================
# CURRENCYGUARD: REMOVED FEATURES & DATA ARCHIVE
# ==============================================================================
# This file contains the exact descriptions and verbatim code of all features
# temporarily removed from app.py for the presentation.
#
# NOTE: The complete 100% original application is ALSO backed up in:
#       `app_backup_full_original.py`
#
# When you want to restore the entire site exactly as before, you can simply
# copy `app_backup_full_original.py` back over `app.py`.
# ==============================================================================

"""
--------------------------------------------------------------------------------
1. PAGE 1 (Executive Dashboard)
--------------------------------------------------------------------------------
REMOVED FEATURES:
- Global Currency Cross Matrix:
  Interactive interbank mid-market exchange matrix calculating cross-rates for
  INR, USD, EUR, GBP, AED, JPY, CAD, AUD.
- Top Daily Currency Movers:
  Real-time table showing intraday momentum and trend flags for pairs
  (USD/JPY, EUR/USD, GBP/USD, USD/CAD, AUD/USD).

VERBATIM CODE:
"""

PAGE_1_REMOVED_CODE = '''
        st.markdown("### 🌐 Global Currency Cross Matrix")
        st.markdown("<p style='font-size:0.85rem; color:var(--text-muted); margin-top:-8px;'>Live interbank mid-market exchange matrix featuring major currencies and <b>INR (India)</b>.</p>", unsafe_allow_html=True)

        matrix_curr = ["INR", "USD", "EUR", "GBP", "AED", "JPY", "CAD", "AUD"]
        frank_data = fetch_frankfurter_latest("USD")
        rates = frank_data.get("rates", {})
        
        matrix_rows = []
        for c1 in matrix_curr[:6]:
            row = {}
            for c2 in matrix_curr[:6]:
                if c1 == c2:
                    row[c2] = 1.0000
                else:
                    r1 = rates.get(c1, BASELINE_USD_RATES.get(c1, 1.0))
                    r2 = rates.get(c2, BASELINE_USD_RATES.get(c2, 1.0))
                    row[c2] = round(r2 / r1, 4) if r1 != 0 else 1.0
            matrix_rows.append(row)

        df_matrix = pd.DataFrame(matrix_rows, index=matrix_curr[:6])
        # Display clean formatted matrix without requiring external matplotlib dependency
        st.dataframe(df_matrix.style.format("{:.4f}"), use_container_width=True)


        # Top Daily Movers Table
        st.markdown("### 🚀 Top Daily Currency Movers")
        st.markdown("<p style='font-size:0.85rem; color:var(--text-muted); margin-top:-8px;'>Intraday price drift & directional momentum across high-volume global pairs.</p>", unsafe_allow_html=True)
        movers_data = [
            {"Pair": "USD/JPY", "Change": "+0.45%", "Trend": "Bullish", "Signal": "Strong Volatility"},
            {"Pair": "EUR/USD", "Change": "-0.22%", "Trend": "Bearish", "Signal": "Moderate Drift"},
            {"Pair": "GBP/USD", "Change": "+0.18%", "Trend": "Bullish", "Signal": "Neutral Steady"},
            {"Pair": "USD/CAD", "Change": "-0.31%", "Trend": "Bearish", "Signal": "Commodity Drift"},
            {"Pair": "AUD/USD", "Change": "+0.52%", "Trend": "Bullish", "Signal": "High Momentum"},
        ]
        df_movers = pd.DataFrame(movers_data)
        st.dataframe(df_movers, use_container_width=True, hide_index=True)
'''

"""
--------------------------------------------------------------------------------
2. PAGE 2 (Smart Currency Converter)
--------------------------------------------------------------------------------
REMOVED FEATURE:
- Multi-Currency Simultaneous Payout Engine:
  Simultaneous multi-currency conversion table and Plotly bar chart comparing
  converted payouts across selectable world currencies and regional groupings.

VERBATIM CODE:
"""

PAGE_2_REMOVED_CODE = '''
    st.divider()

    # Multi-Target Simultaneous Payout Matrix
    st.markdown("### 🌍 Multi-Currency Simultaneous Payout Engine")
    st.markdown(f"<p style='font-size:0.85rem; color:var(--text-muted); margin-top:-8px;'>Instantly convert <b>{c_amt:,.2f} {c_from}</b> into multiple target global currencies simultaneously.</p>", unsafe_allow_html=True)

    default_targets = [c for c in ["USD", "EUR", "GBP", "AED", "CAD"] if c != c_from][:5]
    selected_targets = st.multiselect(
        "Select Target Currencies for Simultaneous Quote",
        options=[c for c in CURRENCY_METADATA.keys() if c != c_from],
        default=default_targets,
        format_func=format_currency_label
    )

    if selected_targets:
        multi_data = []
        for t_curr in selected_targets:
            t_rate = get_cross_rate(c_from, t_curr)
            payout = c_amt * t_rate
            meta = CURRENCY_METADATA.get(t_curr, {})
            multi_data.append({
                "Target Currency": f"{t_curr} - {meta.get('name', '')} ({meta.get('country', '')})",
                "Symbol": meta.get("symbol", ""),
                "Exchange Rate": t_rate,
                "Converted Amount": payout,
                "Region": meta.get("region", "")
            })

        df_multi = pd.DataFrame(multi_data)
        
        col_t1, col_t2 = st.columns([6, 6])
        with col_t1:
            st.dataframe(
                df_multi.style.format({
                    "Exchange Rate": "{:.4f}",
                    "Converted Amount": "{:,.2f}"
                }),
                use_container_width=True,
                hide_index=True
            )
        with col_t2:
            fig_bar = px.bar(
                df_multi,
                x="Target Currency",
                y="Converted Amount",
                text="Converted Amount",
                title=f"Multi-Currency Output Comparison ({c_from})",
                color="Region",
                template="plotly_dark" if st.session_state.theme == "dark" else "plotly_white",
                color_discrete_sequence=["#2563eb", "#059669", "#d97706", "#7c3aed"]
            )
            fig_bar.update_traces(texttemplate='%{text:,.2s}', textposition='outside')
            fig_bar.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bar, use_container_width=True)
'''

"""
--------------------------------------------------------------------------------
3. PAGE 3 (Market Trends & Technical Intelligence)
--------------------------------------------------------------------------------
REMOVED FEATURE:
- Multi-Currency Performance Benchmark (% Growth):
  Normalized relative return line chart comparing growth of EUR, GBP, JPY, INR
  against the chosen base currency over the selected timeframe.

VERBATIM CODE:
"""

PAGE_3_REMOVED_CODE = '''
        # Multi-Currency Normalized Growth Benchmark
        st.divider()
        st.markdown("### 📊 Multi-Currency Performance Benchmark (% Growth)")
        st.markdown("<p style='font-size:0.85rem; color:var(--text-muted); margin-top:-8px;'>Compare normalized relative return of major currencies against the chosen base currency over the same period.</p>", unsafe_allow_html=True)

        benchmark_targets = ["EUR", "GBP", "JPY", "INR"]
        bench_df_list = []
        for b_curr in benchmark_targets:
            if b_curr != t_base:
                b_df = fetch_frankfurter_timeseries(t_base, b_curr, days=num_days)
                if not b_df.empty:
                    initial_val = b_df["rate"].iloc[0]
                    b_df[f"{b_curr} Return (%)"] = ((b_df["rate"] - initial_val) / initial_val) * 100
                    bench_df_list.append(b_df[["date", f"{b_curr} Return (%)"]])

        if bench_df_list:
            merged_bench = bench_df_list[0]
            for next_df in bench_df_list[1:]:
                merged_bench = pd.merge(merged_bench, next_df, on="date", how="inner")

            fig_bench = px.line(
                merged_bench,
                x="date",
                y=[c for c in merged_bench.columns if c != "date"],
                template=plotly_theme,
                title=f"Relative Percentage Movement Against {t_base}",
                labels={"value": "Percentage Change (%)", "variable": "Currency Pair"},
                color_discrete_sequence=["#2563eb", "#059669", "#d97706", "#dc2626"]
            )
            fig_bench.update_layout(height=340, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bench, use_container_width=True)
'''

"""
--------------------------------------------------------------------------------
4. PAGE 4 (Quantitative FX Risk & Hedging Engine)
--------------------------------------------------------------------------------
REMOVED FEATURE:
- Commercial FX Exposure & Hedging Simulator:
  Interactive commercial contract calculator, holding horizon slider, multi-day
  VaR downside loss estimation, and recommended hedging strategies (Forward contract & FX Collar).
  (The upper controls and 4 Key Risk Badges: Volatility, 1-Day 95% VaR, 1-Day 99% VaR, Max Drawdown
  are preserved).

VERBATIM CODE:
"""

PAGE_4_REMOVED_CODE = '''
    # Interactive FX Exposure & Hedging Simulator
    st.markdown("### 💼 Commercial FX Exposure & Hedging Simulator")
    st.markdown("<p style='font-size:0.85rem; color:var(--text-muted); margin-top:-8px;'>Model potential financial downside on foreign receivables or payables.</p>", unsafe_allow_html=True)

    sc_col1, sc_col2 = st.columns([6, 6])
    with sc_col1:
        exp_amount = st.number_input(f"Foreign Contract / Receivable Amount ({r_foreign})", min_value=1000.0, value=100000.0, step=5000.0)
        holding_period_days = st.slider("Exposure Holding Horizon (Days)", min_value=7, max_value=90, value=30)
        
        current_rate = get_cross_rate(r_base, r_foreign)
        # Expected base currency value (Amount foreign / rate)
        base_val = exp_amount / current_rate if current_rate != 0 else exp_amount
        
        # Multi-day VaR scaling: VaR_t = VaR_1d * sqrt(t)
        horizon_var_95_pct = metrics["var_95"] * math.sqrt(holding_period_days)
        horizon_loss_amt = base_val * (horizon_var_95_pct / 100)
        stressed_payout = base_val - horizon_loss_amt

        st.markdown(f"""
        <div class='cg-card'>
            <div style='font-size:0.82rem; font-weight:700; color:var(--text-dim); text-transform:uppercase;'>BASE CURRENCY VALUATION ({r_base})</div>
            <div style='font-size:1.9rem; font-weight:800; color:var(--text-main); font-family:"JetBrains Mono"; margin:4px 0;'>
                {base_val:,.2f} {r_base}
            </div>
            <div style='display:flex; justify-content:space-between; margin-top:10px; font-size:0.88rem; color:#dc2626;'>
                <span>Estimated Downside Risk at 95% Confidence:</span>
                <span style='font-weight:700;'>- {horizon_loss_amt:,.2f} {r_base} ({horizon_var_95_pct:.1f}%)</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-top:6px; font-size:0.88rem; color:var(--emerald-green);'>
                <span>Stressed Minimum Portfolio Floor:</span>
                <span style='font-weight:700;'>{stressed_payout:,.2f} {r_base}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sc_col2:
        st.markdown(f"""
        <div class='cg-card' style='height:100%;'>
            <div style='font-weight:700; color:var(--text-main); margin-bottom:8px; font-size:1rem;'>Recommended Hedging Actions</div>
            <div style='margin-bottom:10px;'>
                <span class='cg-badge cg-badge-blue' style='margin-bottom:6px;'>Forward Contract</span>
                <p style='font-size:0.82rem; color:var(--text-muted); margin:0;'>
                    Lock in current exchange rate of <b>{current_rate:.4f}</b> for the next {holding_period_days} days to eliminate {horizon_loss_amt:,.2f} {r_base} downside uncertainty.
                </p>
            </div>
            <div style='margin-bottom:10px;'>
                <span class='cg-badge cg-badge-amber' style='margin-bottom:6px;'>FX Collar Strategy</span>
                <p style='font-size:0.82rem; color:var(--text-muted); margin:0;'>
                    Establish a synthetic floor at {current_rate * (1 - metrics['var_95']/100):.4f} while retaining upside potential up to {current_rate * (1 + metrics['var_95']/100):.4f}.
                </p>
            </div>
            <div style='font-size:0.75rem; color:var(--text-dim); border-top:1px solid var(--border-color); padding-top:8px;'>
                Calculated using empirical volatility modeling via Frankfurter ECB time-series.
            </div>
        </div>
        """, unsafe_allow_html=True)
'''
