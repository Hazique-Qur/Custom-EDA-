import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ELITE BI SUITE | M.Hazique Qureshi", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LUXURY STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    :root { --bg: #0E1117; --card: #161B22; --accent: #00D4FF; --border: #30363D; }
    .stApp { background-color: var(--bg); color: #E6EDF3; font-family: 'Inter', sans-serif; }
    
    /* KPI Styles */
    .kpi-container { background: var(--card); border-radius: 12px; padding: 25px; border: 2px solid var(--border); box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align: center; margin-bottom: 30px; }
    .kpi-label { color: #8B949E; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
    .kpi-value { font-size: 32px; font-weight: 800; color: #FFFFFF; }
    
    /* Insight Cards - The 4 Grid */
    .insight-card { background: #1C2128; padding: 25px; border-radius: 12px; border: 1px solid var(--border); border-left: 5px solid var(--accent); box-shadow: 0 10px 20px rgba(0,0,0,0.4); margin-bottom: 20px; }
    
    /* Tabs Overlap Fix */
    .stTabs [data-baseweb="tab-list"] { gap: 20px !important; padding: 10px !important; background: var(--card) !important; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 30px !important; }
    .stTabs [data-baseweb="tab"] { min-width: 150px !important; color: #8B949E !important; font-weight: 600 !important; }
    .stTabs [aria-selected="true"] { color: var(--accent) !important; border-bottom: 2px solid var(--accent) !important; }

    .header-style { font-size: 42px; font-weight: 800; background: linear-gradient(90deg, #00D4FF, #7000FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    header {visibility: hidden;} footer {visibility: hidden;}
    .custom-footer { text-align: center; color: #484F58; padding: 50px; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# --- CORE ENGINE ---
def get_col(df, opts):
    for o in opts:
        for c in df.columns:
            if o.lower() in c.lower(): return c
    return None

def process_data(df):
    df.columns = [c.strip() for c in df.columns]
    m = {
        'date': get_col(df, ['date', 'time', 'timestamp']),
        'rev': get_col(df, ['amount', 'sales', 'revenue', 'transaction_amount']),
        'qty': get_col(df, ['qty', 'quantity', 'units']),
        'item': get_col(df, ['item_name', 'product', 'dish', 'item']),
        'cat': get_col(df, ['category', 'type', 'item_type']),
    }
    if m['date']:
        df[m['date']] = pd.to_datetime(df[m['date']], errors='coerce')
        df = df.dropna(subset=[m['date']])
        df['Day'] = df[m['date']].dt.day_name()
        df['Hour'] = df[m['date']].dt.hour
        df['Month'] = df[m['date']].dt.month_name()
    if m['rev']: df[m['rev']] = pd.to_numeric(df[m['rev']], errors='coerce').fillna(0)
    if m['qty']: df[m['qty']] = pd.to_numeric(df[m['qty']], errors='coerce').fillna(0).astype(int)
    return df, m

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00D4FF; margin-bottom:0;'>BI COMMAND</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B949E; font-size:11px;'>M.HAZIQUE QURESHI PLATFORM</p>", unsafe_allow_html=True)
    st.markdown("---")
    up = st.file_uploader("📥 Upload Business CSV", type="csv")
    st.markdown("---")
    if up:
        st.success("System: ONLINE")
        df_raw = pd.read_csv(up, low_memory=False)
        df, cols = process_data(df_raw)
        st.markdown("### 📥 Global Export")
        st.download_button("Download Processed CSV", df.to_csv(index=False), "Cleaned_Report.csv", "text/csv")

# --- MAIN ---
if not up:
    st.markdown("""
        <div style='text-align:center; padding:100px; border:3px dashed #30363D; border-radius:20px; margin-top:50px; background:#161B22;'>
            <h1 style='color:#00D4FF; font-size: 80px;'>🚀</h1>
            <h1 style='color:white;'>Welcome, M.Hazique Qureshi</h1>
            <p style='color:#8B949E; font-size: 18px;'>Upload a file to activate 20+ Advanced Analytics Models.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<div class='header-style'>STRATEGIC BUSINESS INTELLIGENCE</div>", unsafe_allow_html=True)

    # 1. KPIs
    k1, k2, k3, k4 = st.columns(4)
    rev = df[cols['rev']].sum() if cols['rev'] else 0
    vol = df[cols['qty']].sum() if cols['qty'] else 0
    with k1: st.markdown(f'<div class="kpi-container"><div class="kpi-label">Revenue</div><div class="kpi-value">${rev:,.0f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-container"><div class="kpi-label">Volume</div><div class="kpi-value">{vol:,}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-container"><div class="kpi-label">AOV</div><div class="kpi-value">${rev/len(df) if len(df)>0 else 0:,.0f}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-container"><div class="kpi-label">Total Orders</div><div class="kpi-value">{len(df):,}</div></div>', unsafe_allow_html=True)

    # 2. Tabs
    t1, t2, t3, t4, t5, t6 = st.tabs(["🚀 Strategies", "📈 Sales Intelligence", "📦 Inventory", "⏰ Behavior", "🔥 Market Heatmaps", "📥 Data Hub"])
    
    with t1:
        st.subheader("💡 Strategic AI Insights")
        if cols['date'] and cols['rev']:
            r1, r2 = st.columns(2)
            p_day = df.groupby('Day')[cols['rev']].sum().idxmax()
            r1.markdown(f'<div class="insight-card"><h4>Market Peak</h4>Highest business velocity on <b>{p_day}s</b>.</div>', unsafe_allow_html=True)
            p_hr = df.groupby('Hour')[cols['rev']].sum().idxmax()
            r2.markdown(f'<div class="insight-card"><h4>Golden Hour</h4>Max traffic occurs at <b>{p_hr}:00</b>.</div>', unsafe_allow_html=True)
            r3, r4 = st.columns(2)
            star = df.groupby(cols['item'])[cols['rev']].sum().idxmax() if cols['item'] else "N/A"
            r3.markdown(f'<div class="insight-card"><h4>Star Product</h4><b>{star}</b> is your top generator.</div>', unsafe_allow_html=True)
            r4.markdown(f'<div class="insight-card"><h4>Profit Strategy</h4>Aim for <b>+20%</b> AOV through bundling deals.</div>', unsafe_allow_html=True)

    with t2:
        st.subheader("Revenue Dynamics & Trends")
        c1, c2 = st.columns(2)
        with c1:
            st.write("### Sales vs Units Trend")
            df_t = df.set_index(cols['date'])[[cols['rev'], cols['qty']]].resample('D').sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_t[cols['date']], y=df_t[cols['rev']], name='Revenue', line=dict(color='#00D4FF', width=3)))
            fig.add_trace(go.Bar(x=df_t[cols['date']], y=df_t[cols['qty']], name='Qty', yaxis='y2', opacity=0.3))
            fig.update_layout(template='plotly_dark', yaxis2=dict(overlaying='y', side='right'), height=400)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.write("### Cumulative Value Growth")
            df_t['cum'] = df_t[cols['rev']].cumsum()
            st.plotly_chart(px.area(df_t, x=cols['date'], y='cum', template='plotly_dark', color_discrete_sequence=['#7000FF']), use_container_width=True)

    with t3:
        st.subheader("Product & Category Intelligence")
        c3, c4 = st.columns(2)
        with c3:
            st.write("### Top 10 Best Sellers")
            if cols['item']:
                top = df.groupby(cols['item'])[cols['rev']].sum().sort_values(ascending=False).head(10).reset_index()
                st.plotly_chart(px.bar(top, x=cols['rev'], y=cols['item'], orientation='h', template='plotly_dark', color=cols['rev']), use_container_width=True)
        with c4:
            st.write("### ⚠️ Underperforming Assets")
            if cols['item']:
                low = df.groupby(cols['item'])[cols['rev']].sum().sort_values(ascending=True).head(5).reset_index()
                st.plotly_chart(px.bar(low, x=cols['rev'], y=cols['item'], orientation='h', template='plotly_dark', color_discrete_sequence=['#F85149']), use_container_width=True)

    with t4:
        st.subheader("Time-Based Behavior")
        c5, c6 = st.columns(2)
        with c5:
            st.write("### Weekday Performance")
            day_d = df.groupby('Day')[cols['rev']].sum().reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']).reset_index()
            st.plotly_chart(px.bar(day_d, x='Day', y=cols['rev'], template='plotly_dark', color='Day'), use_container_width=True)
        with c6:
            st.write("### Hourly Intensity")
            st.plotly_chart(px.line(df.groupby('Hour')[cols['rev']].sum().reset_index(), x='Hour', y=cols['rev'], template='plotly_dark', markers=True), use_container_width=True)

    with t5:
        st.subheader("Global Heatmap Recognition")
        piv = df.pivot_table(index='Day', columns='Hour', values=cols['rev'], aggfunc='sum').fillna(0)
        st.plotly_chart(px.imshow(piv, template='plotly_dark', color_continuous_scale='Viridis'), use_container_width=True)

    with t6:
        st.write("### System Audit & Raw Access")
        st.dataframe(df.head(100), use_container_width=True)
        st.download_button("📥 Full Report CSV", df.to_csv(index=False), "Hazique_BI_Report.csv")

# Footer
st.markdown(f"<div class='custom-footer'>DEVELOPED BY M.HAZIQUE QURESHI | 2026</div>", unsafe_allow_html=True)
