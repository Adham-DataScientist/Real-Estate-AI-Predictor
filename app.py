import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(
    page_title="Madrid Elite Real Estate AI",
    page_icon="🇪🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم CSS متقدم (Premium Dark Theme)
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stMetric {
        background: linear-gradient(145deg, #1c2128, #161b22);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #8b949e;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f6feb !important;
        color: white !important;
    }
    h1 { color: #58a6ff; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/609/609036.png", width=80)
    st.title("Madrid Real Estate")
    uploaded_file = st.file_uploader("Upload 'houses_Madrid.csv'", type=['csv'])
    st.divider()
    st.info("AI Model: Multiple Linear Regression")
    st.caption("Developed by Adham 🚀 - 2026 Edition")

# --- الصفحة الرئيسية ---
st.title("🏰 Madrid Elite Property Predictor")
st.markdown("---")

if uploaded_file:
    # تحميل البيانات وتنظيفها
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    
    # تحويل السعر والمساحة لأرقام وحذف القيم الفارغة
    df['buy_price'] = pd.to_numeric(df['buy_price'], errors='coerce')
    df['sq_mt_built'] = pd.to_numeric(df['sq_mt_built'], errors='coerce')
    df = df.dropna(subset=['buy_price', 'sq_mt_built', 'n_rooms', 'n_bathrooms'])

    # --- القسم الأول: لوحة المؤشرات الذكية (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Properties Analyzed", f"{len(df):,}")
    with col2:
        st.metric("Avg Market Price", f"€{df['buy_price'].mean():,.0f}")
    with col3:
        st.metric("Avg Price / m²", f"€{df['buy_price'].mean() / df['sq_mt_built'].mean():,.2f}")
    with col4:
        st.metric("Neighborhoods", f"{df['subtitle'].nunique() if 'subtitle' in df.columns else 'N/A'}")

    st.markdown("### 📊 Interactive Insights")
    
    # --- القسم الثاني: التبويبات (Tabs) ---
    tab_viz, tab_map, tab_ai, tab_raw = st.tabs(["📉 Market Visuals", "📍 Location Map", "🤖 AI Price Predictor", "📑 Dataset Explorer"])

    with tab_viz:
        c1, c2 = st.columns(2)
        with c1:
            # توزيع الأسعار
            fig_hist = px.histogram(df[df['buy_price'] < 2000000], x="buy_price", 
                                   title="Price Distribution (Below €2M)",
                                   nbins=50, color_discrete_sequence=['#58a6ff'], template="plotly_dark")
            st.plotly_chart(fig_hist, width="stretch")
        with c2:
            # العلاقة بين الغرف والسعر
            fig_box = px.box(df[df['n_rooms'] < 7], x="n_rooms", y="buy_price", 
                            title="Price Range by Number of Rooms",
                            color="n_rooms", template="plotly_dark")
            st.plotly_chart(fig_box, width="stretch")

    with tab_map:
        if 'latitude' in df.columns and 'longitude' in df.columns:
            st.subheader("Property Density Across Madrid")
            map_data = df[['latitude', 'longitude', 'buy_price']].dropna().head(1000)
            st.map(map_data, size=20, color="#1f6feb")
        else:
            st.warning("Coordinate data (Latitude/Longitude) not found in CSV.")

    with tab_ai:
        st.subheader("🤖 Artificial Intelligence Valuation")
        st.write("Enter property details to get an AI-estimated market value.")
        
        # تدريب الموديل
        features = ['sq_mt_built', 'n_rooms', 'n_bathrooms']
        X = df[features]
        y = df['buy_price']
        
        model = LinearRegression()
        model.fit(X.values, y.values)
        
        # واجهة المدخلات
        with st.container():
            col_in1, col_in2, col_in3 = st.columns(3)
            with col_in1:
                in_area = st.slider("Built Area (m²)", int(df['sq_mt_built'].min()), 1000, 120)
            with col_in2:
                in_rooms = st.number_input("Rooms", 1, 10, 3)
            with col_in3:
                in_baths = st.number_input("Bathrooms", 1, 10, 2)
            
            if st.button("🔮 Estimate Price Now", use_container_width=True):
                prediction = model.predict([[in_area, in_rooms, in_baths]])[0]
                st.markdown(f"""
                    <div style="background-color: #1f6feb; padding: 40px; border-radius: 20px; text-align: center; border: 2px solid #58a6ff;">
                        <h1 style="color: white; margin: 0;">€{prediction:,.2f}</h1>
                        <p style="color: #adbac7; font-size: 18px;">Estimated Market Value</p>
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()

    with tab_raw:
        st.dataframe(df, width="stretch")

else:
    # واجهة الترحيب عند عدم وجود ملف
    st.markdown("""
        <div style="text-align: center; padding: 80px;">
            <h1 style="font-size: 60px;">🚀</h1>
            <h2>Ready to Analyze Madrid?</h2>
            <p style="color: #8b949e; font-size: 20px;">Upload 'houses_Madrid.csv' in the sidebar to begin your AI journey.</p>
        </div>
    """, unsafe_allow_html=True)
    st.image("https://tse2.mm.bing.net/th/id/OIP.xOwCSIWL4eHUF-k3r51AQQHaDt?pid=Api&h=220&P=0", width="stretch")