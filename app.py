import streamlit as st 
import pandas as pd


st.set_page_config(page_title="Real-Estate-AI-Predictor" , layout="wide")
st.markdown(
  """
<style>
.main {
    background-color: #0e1117;
}
stMetric {
    background-color: #1e2130;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True
)
st.title("Welcome adham")
st.write("شغال كويس 😍")

Upload_file = st.file_uploader("Updated_Real_Estate_Date" , type=['xlsx'])

if Upload_file is not None :
    if st.button("🚀✈️ Start DAta Analysis "):
        try :
            if Upload_file.name.endswith('.xlsx') or Upload_file.name.endswith(".xls"):  
                df =pd.read_excel(Upload_file)
                st.success("🚀 Excel loaded file successfuly")
            elif Upload_file.name.endswith(".csv"):
                df = pd.read_csv(Upload_file)   
                st.success("🚀 CSV Loaded file Successfuly") 
        except Exception as a :
            st.error(f"Error reading file {a}")    