import pandas as pd 
import numpy as np
import tkinter as tk 
from tkinter import filedialog 
import os
import time
import shutil
import urllib
from sqlalchemy import create_engine
def load_data(file_path):
    try : 
        
        if file_path.endswith('.csv'):
           df = pd.read_csv(file_path, sep=";" , decimal=",")
           print("download CSV")
        elif file_path.endswith(".xlsx"):
           df =pd.read_excel(file_path )
           print("download Excel")
        else :
           print("NOT Uploaded File")
           return df
        return df
    except Exception as e :
        print(f"Error {e}")

def setup_enviroment():
    folders =["Input","output" ,"archive"]
    for file in folders :
        if not os.path.exists(file):
            os.makedirs(file)
        else :
            print(f"already files {file}")
            
            
def start_robot():
    while True :
        input_dir = "Input"
        archive_dir ="archive"
                    
        file_path =os.listdir(input_dir)    
                
        if len(file_path)>0:
           print("ok New file ") 
           
           for file in file_path:
               current_file_path=os.path.join(input_dir , file) 
               try :
                   
                   if file.endswith('.csv'):
                       df =pd.read_csv(current_file_path)
                   elif file.endswith('.xlsx') or file.endswith('.xls'):
                       df =pd.read_excel(current_file_path)
                   else :
                       print("not found")
                       continue
                   destination = os.path.join(archive_dir , file)
                   shutil.move(current_file_path , destination)
                   print("the file is moved")
                       
               except Exception as a :
                   print (f"Error {a}")
           break
        else :
            
            print("not found files")
            time.sleep(10)   
def proccess_date(df):
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'] , dayfirst=True , errors="coerce")
        df['Year'] = df['Date'].dt.year 
        df['Month_Num'] = df['Date'].dt.month_name()
        df['Day_Num'] = df['Date'].dt.day_name() 
        return df
                   
                   
def export_sql (df):
    
    server_name=r'.\SQLEXPRESS'
    database_name ='Real_Estate_Ai_Prodictor'
    table_name = 'real_estate'
    
    connection_string=(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server_name};"
        f"DATABASE={database_name};"
        f"Trusted_Connection=yes;"
    )
    quote =urllib.parse.quote(connection_string)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote}" ,fast_executemany = True )
    df.to_sql("real_estate" , con =engine , if_exists ="replace" , index=False , chunksize = 200000)
    print(f"ok new sql server {table_name}")
    