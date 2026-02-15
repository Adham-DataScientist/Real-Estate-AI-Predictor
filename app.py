import streamlit as st
import pandas as pd
import plotly.express as px 

# إعداد الصفحة
st.set_page_config(page_title="Real Estate Pro AI", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stMetric"] {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/609/609036.png", width=100)
    st.title("Settings")
    uploaded_file = st.file_uploader("Upload Data", type=['csv', 'xlsx'])
    st.divider()
    st.info("Developed by Adham 🚀")

# --- الصفحة الرئيسية ---
st.title("🏢 Real Estate AI Predictor")
st.markdown("---")

if uploaded_file:
    # قراءة البيانات
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # صف المقاييس (KPIs)
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Total Records", f"{len(df):,}")
        st.metric("describe Records", df.info())
    
    with m2:
        if 'Price' in df.columns:
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            avg_price = df['Price'].mean()
        else:
            avg_price = 0
            st.warning("⚠️ Column 'Price' not found")
        
        st.metric("Avg Price/Unit", f"${avg_price:,.2f}")
        
    with m3:
        city_col = 'City' if 'City' in df.columns else df.columns[0]
        st.metric("Unique Locations", df[city_col].nunique())
        
    with m4:
        st.metric("Status", "Ready ✅")

    st.markdown("### 📊 Market Analysis")
    
    tab_charts, tab_data, tab_ai = st.tabs(["Visual Analytics", "Raw Data", "AI Prediction"])

    with tab_charts:
        c1, c2 = st.columns(2)
        with c1:
            # ✅ التعديل: استخدام width="stretch" لمنع تحذير 2026
            fig1 = px.histogram(df, x=df.columns[2], title=f"Distribution of {df.columns[2]}", color_discrete_sequence=['#00f2ff'])
            st.plotly_chart(fig1, width="stretch")
        with c2:
            # ✅ التعديل: استخدام width="stretch" هنا أيضاً
            fig2 = px.scatter(df, x=df.columns[3], y=df.columns[-1], title="Price Analysis", color_discrete_sequence=['#ff4b4b'])
            st.plotly_chart(fig2, width="stretch")

    with tab_data:
        # ✅ التعديل: استخدام width="stretch" للجدول
        st.dataframe(df, width="stretch")

    with tab_ai:
        st.subheader("🤖 Predict House Value")
        st.info("The AI model is learning from your uploaded data...")

else:
    # ✅ التعديل: استخدام width="stretch" للصورة الترحيبية
    st.image("https://tse2.mm.bing.net/th/id/OIP.xOwCSIWL4eHUF-k3r51AQQHaDt?pid=Api&h=220&P=0", width="stretch")
    st.warning("👈 Please upload a dataset from the sidebar to start.")