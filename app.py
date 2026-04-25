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
    
    .kpi-container { background: var(--card); border-radius: 12px; padding: 25px; border: 2px solid var(--border); box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align: center; margin-bottom: 30px; }
    .kpi-label { color: #8B949E; font-size: 12px; font-weight: 700; text-transform: uppercase; }
    .kpi-value { font-size: 32px; font-weight: 800; color: #FFFFFF; }
    
    .insight-card { background: #1C2128; padding: 25px; border-radius: 12px; border: 1px solid var(--border); border-left: 5px solid var(--accent); margin-bottom: 20px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 20px !important; padding: 10px !important; background: var(--card) !important; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 30px !important; }
    .stTabs [data-baseweb="tab"] { min-width: 150px !important; color: #8B949E !important; font-weight: 600 !important; }

    .header-style { font-size: 42px; font-weight: 800; background: linear-gradient(90deg, #00D4FF, #7000FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    /* Welcome Screen Styling */
    .welcome-box { 
        text-align: center; padding: 80px 40px; background: #161B22; border-radius: 24px; 
        border: 2px solid #30363D; margin-top: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }
    .welcome-title { font-size: 50px; font-weight: 800; color: white; margin-bottom: 10px; }
    .welcome-subtitle { font-size: 20px; color: #00D4FF; font-weight: 600; margin-bottom: 30px; }
    .welcome-text { font-size: 18px; color: #8B949E; line-height: 1.6; max-width: 700px; margin: 0 auto 40px auto; }
    
    header {visibility: hidden;} footer {visibility: hidden;}
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
    st.markdown("<h2 style='color:#00D4FF'>💎 BI CONTROL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8B949E; font-size:11px;'>M.HAZIQUE QURESHI PLATFORM</p>", unsafe_allow_html=True)
    st.markdown("---")
    up = st.file_uploader("Upload Client Data (CSV)", type="csv")
    st.markdown("---")
    if up:
        st.success("Analysis Mode Active")
        df_raw = pd.read_csv(up, low_memory=False)
        df, cols = process_data(df_raw)
        st.download_button("📥 Export Analysis Report", df.to_csv(index=False), "BI_Report.csv")

# --- MAIN ---
if not up:
    st.markdown("""
        <div class="welcome-box">
            <h1 class="welcome-title">M.Hazique Qureshi</h1>
            <p class="welcome-subtitle">STRATEGIC BUSINESS INTELLIGENCE PORTAL</p>
            <p class="welcome-text">
                Unlock deep business insights, optimize revenue streams, and scale your operations with data-driven precision. 
                This platform is designed to transform your raw transaction history into actionable growth strategies.
            </p>
            <div style="background: #1C2128; display: inline-block; padding: 15px 30px; border-radius: 50px; border: 1px solid #00D4FF; color: white; font-weight: 600;">
                Ready to Analyze. Please Upload your Dataset in Sidebar.
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<div class='header-style'>STRATEGIC BUSINESS INTELLIGENCE</div>", unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    rev = df[cols['rev']].sum() if cols['rev'] else 0
    vol = df[cols['qty']].sum() if cols['qty'] else 0
    with k1: st.markdown(f'<div class="kpi-container"><div class="kpi-label">Total Revenue</div><div class="kpi-value">${rev:,.0f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-container"><div class="kpi-label">Units Sold</div><div class="kpi-value">{vol:,}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-container"><div class="kpi-label">Average Ticket</div><div class="kpi-value">${rev/len(df) if len(df)>0 else 0:,.0f}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-container"><div class="kpi-label">Transactions</div><div class="kpi-value">{len(df):,}</div></div>', unsafe_allow_html=True)

    # Tabs
    t1, t2, t3, t4, t5 = st.tabs(["🚀 Strategies", "📈 Sales Dynamics", "📦 Item Analytics", "⏰ Heatmaps", "📥 Data Hub"])
    
    with t1:
        st.subheader("💡 Strategic AI Recommendations")
        if cols['date'] and cols['rev']:
            r1, r2 = st.columns(2)
            p_day = df.groupby('Day')[cols['rev']].sum().idxmax()
            r1.markdown(f'<div class="insight-card"><h4>Market Peak</h4>Capture maximum value on <b>{p_day}s</b>.</div>', unsafe_allow_html=True)
            p_hr = df.groupby('Hour')[cols['rev']].sum().idxmax()
            r2.markdown(f'<div class="insight-card"><h4>Golden Hour</h4>Peak sales velocity at <b>{p_hr}:00</b>.</div>', unsafe_allow_html=True)
            r3, r4 = st.columns(2)
            star = df.groupby(cols['item'])[cols['rev']].sum().idxmax() if cols['item'] else "N/A"
            r3.markdown(f'<div class="insight-card"><h4>Star Product</h4><b>{star}</b> is your primary revenue driver.</div>', unsafe_allow_html=True)
            r4.markdown(f'<div class="insight-card"><h4>Growth Hack</h4>Increase AOV by 15% through strategic bundling.</div>', unsafe_allow_html=True)

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
        st.write("### Final Audit & Raw Access")
        st.dataframe(df.head(100), use_container_width=True)

# Footer
st.markdown(f"<div style='text-align:center; color:#30363D; padding:40px; font-weight:500;'>DEVELOPED BY M.HAZIQUE QURESHI | STRATEGIC DATA SOLUTIONS 2026</div>", unsafe_allow_html=True)
