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

# --- CINEMATIC UI STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    :root { 
        --bg: #05070A; 
        --glass: rgba(255, 255, 255, 0.03);
        --accent: #00D4FF; 
        --gradient: linear-gradient(135deg, #00D4FF 0%, #7000FF 100%);
    }
    
    .stApp { 
        background: radial-gradient(circle at top right, #1A1F2C, #05070A);
        color: #F8F9FA; 
        font-family: 'Outfit', sans-serif; 
    }
    
    /* Premium Hero Section */
    .hero-container {
        text-align: center;
        padding: 100px 20px;
        animation: fadeIn 1.5s ease-in-out;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    .hero-title {
        font-size: 72px;
        font-weight: 800;
        letter-spacing: -2px;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .hero-tagline {
        font-size: 24px;
        color: #8B949E;
        font-weight: 400;
        margin-bottom: 40px;
    }

    /* Glass Cards */
    .glass-card {
        background: var(--glass);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        transition: 0.3s;
    }
    .glass-card:hover { border-color: var(--accent); transform: translateY(-5px); }
    
    .feature-icon { font-size: 30px; margin-bottom: 15px; }
    .feature-title { font-weight: 700; color: white; font-size: 18px; }
    .feature-desc { color: #8B949E; font-size: 14px; }

    /* KPI Overrides */
    .kpi-container { background: var(--glass); border-radius: 20px; padding: 25px; border: 1px solid rgba(255,255,255,0.05); text-align: center; }
    .kpi-label { color: #8B949E; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 34px; font-weight: 800; color: #FFFFFF; }

    header {visibility: hidden;} footer {visibility: hidden;}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; padding: 8px; background: var(--glass); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); }
    .stTabs [data-baseweb="tab"] { min-width: 150px; color: #8B949E; font-weight: 600; padding: 12px; }
</style>
""", unsafe_allow_html=True)

# --- ENGINE ---
def get_col(df, opts):
    for o in opts:
        for c in df.columns:
            if o.lower() in c.lower(): return c
    return None

def process_data(df):
    df.columns = [c.strip() for c in df.columns]
    m = {
        'date': get_col(df, ['date', 'time']),
        'rev': get_col(df, ['amount', 'sales', 'revenue', 'transaction_amount']),
        'qty': get_col(df, ['qty', 'quantity', 'units']),
        'item': get_col(df, ['item_name', 'product', 'dish']),
        'cat': get_col(df, ['category', 'type', 'item_type'])
    }
    if m['date']:
        df[m['date']] = pd.to_datetime(df[m['date']], errors='coerce')
        df = df.dropna(subset=[m['date']])
        df['Day'] = df[m['date']].dt.day_name()
        df['Hour'] = df[m['date']].dt.hour
    if m['rev']: df[m['rev']] = pd.to_numeric(df[m['rev']], errors='coerce').fillna(0)
    if m['qty']: df[m['qty']] = pd.to_numeric(df[m['qty']], errors='coerce').fillna(0).astype(int)
    return df, m

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00D4FF; letter-spacing:-1px;'>💎 ELITE SYSTEM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B949E; font-size:11px; margin-top:-10px;'>BY M.HAZIQUE QURESHI</p>", unsafe_allow_html=True)
    st.markdown("---")
    up = st.file_uploader("Upload Business Intelligence Dataset", type="csv")
    st.markdown("---")
    if up:
        st.success("Analysis Ready")
        df_raw = pd.read_csv(up, low_memory=False)
        df, cols = process_data(df_raw)
        st.download_button("📥 Full Report CSV", df.to_csv(index=False), "Analysis_Report.csv")

# --- MAIN ---
if not up:
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">M.Hazique Qureshi</h1>
            <p class="hero-tagline">Strategic Intelligence & Advanced Data Solutions</p>
            <div style="max-width: 900px; margin: 0 auto;">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; text-align: left;">
                    <div class="glass-card">
                        <div class="feature-icon">🚀</div>
                        <div class="feature-title">AI Strategy</div>
                        <div class="feature-desc">Automated business recommendations and growth mapping.</div>
                    </div>
                    <div class="glass-card">
                        <div class="feature-icon">📊</div>
                        <div class="feature-title">15+ Analytics</div>
                        <div class="feature-desc">Deep-dive visualizations across revenue, items, and behavior.</div>
                    </div>
                    <div class="glass-card">
                        <div class="feature-icon">🔥</div>
                        <div class="feature-title">Market Heatmaps</div>
                        <div class="feature-desc">Recognize peak traffic patterns and hourly sales velocity.</div>
                    </div>
                </div>
            </div>
            <br><br>
            <div style="color:#8B949E; font-size: 14px; border: 1px solid rgba(255,255,255,0.1); display: inline-block; padding: 10px 30px; border-radius: 50px;">
                Waiting for data... Please upload CSV in sidebar to activate engine.
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<h1 style='font-size:38px; font-weight:800; letter-spacing:-1px; margin-bottom:30px;'>STRATEGIC BI DASHBOARD</h1>", unsafe_allow_html=True)

    # KPIs Row
    k1, k2, k3, k4 = st.columns(4)
    rev = df[cols['rev']].sum() if cols['rev'] else 0
    vol = df[cols['qty']].sum() if cols['qty'] else 0
    k1.markdown(f'<div class="kpi-container"><div class="kpi-label">Revenue</div><div class="kpi-value">${rev:,.0f}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-container"><div class="kpi-label">Volume</div><div class="kpi-value">{vol:,}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-container"><div class="kpi-label">AOV</div><div class="kpi-value">${rev/len(df) if len(df)>0 else 0:,.0f}</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-container"><div class="kpi-label">Transactions</div><div class="kpi-value">{len(df):,}</div></div>', unsafe_allow_html=True)

    # Tabs
    t1, t2, t3, t4, t5 = st.tabs(["🎯 Strategy", "📈 Dynamics", "📦 Products", "⏰ Behavior", "📑 Audit"])
    
    with t1:
        st.subheader("💡 Actionable Intelligence")
        if cols['date'] and cols['rev']:
            r1, r2 = st.columns(2)
            p_day = df.groupby('Day')[cols['rev']].sum().idxmax()
            r1.markdown(f'<div class="glass-card" style="border-left: 4px solid #00D4FF;"><h4>Market Peak</h4>Your business is strongest on <b>{p_day}s</b>.</div>', unsafe_allow_html=True)
            p_hr = df.groupby('Hour')[cols['rev']].sum().idxmax()
            r2.markdown(f'<div class="glass-card" style="border-left: 4px solid #7000FF;"><h4>Golden Hour</h4>Peak velocity detected at <b>{p_hr}:00</b>.</div>', unsafe_allow_html=True)
            r3, r4 = st.columns(2)
            star = df.groupby(cols['item'])[cols['rev']].sum().idxmax() if cols['item'] else "N/A"
            r3.markdown(f'<div class="glass-card" style="border-left: 4px solid #00D4FF;"><h4>Star Product</h4><b>{star}</b> is your top generator.</div>', unsafe_allow_html=True)
            r4.markdown(f'<div class="glass-card" style="border-left: 4px solid #7000FF;"><h4>Growth Strategy</h4>Increase revenue by 15% via strategic product bundling.</div>', unsafe_allow_html=True)

    with t2:
        st.plotly_chart(px.line(df.set_index(cols['date'])[cols['rev']].resample('D').sum().reset_index(), x=cols['date'], y=cols['rev'], template='plotly_dark', color_discrete_sequence=['#00D4FF']), use_container_width=True)

    with t3:
        if cols['item']:
            top = df.groupby(cols['item'])[cols['rev']].sum().sort_values(ascending=False).head(15).reset_index()
            st.plotly_chart(px.bar(top, x=cols['rev'], y=cols['item'], orientation='h', template='plotly_dark', color=cols['rev']), use_container_width=True)

    with t4:
        piv = df.pivot_table(index='Day', columns='Hour', values=cols['rev'], aggfunc='sum').fillna(0)
        st.plotly_chart(px.imshow(piv, template='plotly_dark', color_continuous_scale='Viridis'), use_container_width=True)

    with t5:
        st.dataframe(df.head(100), use_container_width=True)

# Footer
st.markdown(f"<div style='text-align:center; color:#484F58; padding:60px; font-weight:500; letter-spacing:1px;'>DEVELOPED BY M.HAZIQUE QURESHI | 2026</div>", unsafe_allow_html=True)
