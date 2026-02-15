import tkinter as tk 
from tkinter import filedialog
import pandas as pd 
import matplotlib.pyplot as plt 
from functions import load_data ,setup_enviroment ,start_robot,export_sql
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

def main ():
    root =tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    file_path = filedialog.askopenfilename(
        title="Select Data File",
        filetypes=[("CSV files",".csv" ) , ("Excel files" ,"*.xlsx *.xls")]
    )
    if file_path :
        try :
            df = load_data(file_path)
            if df is not None : 
                export_sql(df)
            
            df['Commition'] = df['Price'] * 0.15
    
            df_Country = df.groupby('Country')["Paid"].agg(["sum" ,"max" , "min"]).plot(kind= "bar", ylabel="Paid",title ="Total paid by country")
            print(df_Country)
            df_Type = df.groupby('Type')["Paid"].agg(["sum"]).plot(kind= "bar", ylabel="Paid",title ="Total paid by type")
            print(df_Type)
            df_Direction= df.groupby('Direction')["Commition"].agg(["sum","max"]).plot(kind= "bar", ylabel="Paid",title ="Total paid by District")
            print(df_Direction)
            plt.show()
              
    
    
            x = df[['Price']]
            y=df['Profits']
    
            model=LinearRegression()
            model.fit(x,y)
            test_model = model.predict([[1000]])
            print("##################################################################")
            print(f"Predicted profit for price 1000:\n {test_model}")
    
            df.to_excel("Updated_Real_Estate_Date.xlsx" ,index=False)
            
            print(df.head())
            print("Data loaded successfuly")
        except Exception as e :
            print (f"Erorr Loading Data: {e}")
    else :
        print("No File Selected")    

   

if __name__ == "__main__":
    main()   
setup_enviroment()     
start_robot()