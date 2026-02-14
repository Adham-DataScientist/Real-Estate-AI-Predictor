import streamlit as st 
import pandas as pd
from functions import proccess_date


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

Upload_file = st.file_uploader("Updated_Real_Estate_Date" , type=['xlsx' ,'csv'])

if Upload_file is not None :
    if st.button("🚀✈️ Start DAta Analysis "):
        try :
            if Upload_file.name.endswith('.xlsx') or Upload_file.name.endswith(".xls"):  
                df =pd.read_excel(Upload_file)
                st.success("🚀 Excel loaded file successfuly")
            elif Upload_file.name.endswith(".csv"):
                df = pd.read_csv(Upload_file , encoding="utf-8" ,on_bad_lines="skip" )  
                st.info("CSV file detected") 
                st.success("🚀 CSV Loaded file Successfuly") 
            df = pd.DataFrame(df.head(10))    
            proccess_date(df)
            st.subheader("Proccessed Data preview 🚀")
            st.dataframe(df.head())
            st.divider()
            st.dataframe(df.describe())
        except Exception as a :
            st.error(f"Error reading file {a}")  
            
        col1 , col2 , col3 = st.columns(3)
        col1.metric("AVG Price" ,f"$ {df['Price'].mean():,.02f}" )     
        col2.metric("Total Rows" ,len(df) )     
        total_sales=(df['Price'] * df['Quantity']).sum() 
        col3.metric("Total Sales" ,f"${total_sales :,.2f}" )     
        
        
        #st.subheader("📈Businees Real Estate ")
        #df.groupby("")
else:
    st.info("☝️ (Browse files)  يرجي اختيار الملف من")          