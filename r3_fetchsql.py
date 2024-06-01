#SQL connect to Fetch data from database
import pymysql
import pandas as pd

def my_sql_database_connect():
    conn = pymysql.connect(
        host="localhost",
        port=3307,
        user="root",
        password="root",
        database="phonepe_pulse"
    )
    
    return conn

# Function to Fetch from Aggregated Transaction Table to store it into the DataFrame
def fetch_agg_trans_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()
    query1 = "SELECT * FROM agg_trans"
    cursor.execute(query1)
    conn.commit()
    table1 = cursor.fetchall()
    df_agg_trans = pd.DataFrame(table1, columns=["Id","State","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"])
    df_agg_trans.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_agg_trans

# Function to Fetch from Aggregated Map Table to store it into the DataFrame    
def fetch_agg_user_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()  
    query2 = "SELECT * FROM agg_user"
    cursor.execute(query2)
    conn.commit()
    table2 = cursor.fetchall()
    df_agg_user = pd.DataFrame(table2, columns=["Id",'State', 'Year','Quarter','Brand', 'Count', 'Percentage'])
    df_agg_user.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_agg_user

#Function to Fetch from Aggregated Insurance Table to store it into the DataFrame
def fetch_agg_ins_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()
    query3 = "SELECT * FROM agg_ins"
    cursor.execute(query3)
    conn.commit()
    table3 = cursor.fetchall()
    df_agg_ins = pd.DataFrame(table3, columns=["Id",'State', 'Year','Quarter','Transaction_type', 'Transaction_count', 'Transaction_amount'])
    df_agg_ins.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_agg_ins

#Function to Fetch from Map Transaction Table to store it into the DataFrame
def fetch_map_trans_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()
    query4 = "SELECT * FROM map_trans"
    cursor.execute(query4)
    conn.commit()
    table4 = cursor.fetchall()
    df_map_trans = pd.DataFrame(table4, columns=["Id","State","Year","Quarter",'User_District', 'Transaction_count', 'Transaction_amount'])
    df_map_trans.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_map_trans

#Function to Fetch from Map User Table to store it into the DataFrame   
def fetch_map_user_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()
    query5 = "SELECT * FROM map_user"
    cursor.execute(query5)
    conn.commit()
    table5 = cursor.fetchall()
    df_map_user = pd.DataFrame(table5, columns=["Id","State","Year","Quarter",'User_District', 'Registered_Users', 'App_opens'])
    df_map_user.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_map_user

#Function to Fetch from Map Insurance Table to store it into the DataFrame 
def fetch_map_ins_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()
    query6 = "SELECT * FROM map_ins"
    cursor.execute(query6)
    conn.commit()
    table6 = cursor.fetchall()
    df_map_ins = pd.DataFrame(table6, columns=["Id","State","Year","Quarter",'User_District', 'Transaction_count', 'Transaction_amount'])
    df_map_ins.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_map_ins  

#Function to Fetch from Top Transaction Table to store it into the DataFrame     
def fetch_top_trans_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()
    query7 = "SELECT * FROM top_trans"
    cursor.execute(query7)
    conn.commit()
    table7 = cursor.fetchall()
    df_top_trans = pd.DataFrame(table7, columns=["Id","State","Year","Quarter","User_District_Pincodes","Transaction_count","Transaction_amount"])
    df_top_trans.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_top_trans
 
#Function to Fetch from Top User Table to store it into the DataFrame      
def fetch_top_user_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()
    query8 = "SELECT * FROM top_user"
    cursor.execute(query8)
    conn.commit()
    table8 = cursor.fetchall()
    df_top_user = pd.DataFrame(table8, columns=["Id","State","Year","Quarter","User_District_Pincodes","Registered_Users"])
    df_top_user.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_top_user
 
#Function to Fetch from Top Insurance Table to store it into the DataFrame      
def fetch_top_ins_data():
    conn=my_sql_database_connect()
    cursor=conn.cursor()
    query9 = "SELECT * FROM top_ins"
    cursor.execute(query9)
    conn.commit()
    table9 = cursor.fetchall()
    df_top_ins= pd.DataFrame(table9, columns=["Id","State","Year","Quarter","User_District_Pincodes","Transaction_count","Transaction_amount"])
    df_top_ins.drop('Id', axis=1, inplace=True)
    conn.close()
    return df_top_ins   


#Fetching Data Frame into SQL

agg_trans = fetch_agg_trans_data()
agg_user = fetch_agg_user_data()
agg_ins = fetch_agg_ins_data()

map_trans = fetch_map_trans_data()
map_user = fetch_map_user_data()
map_ins = fetch_map_ins_data()


top_trans = fetch_top_trans_data()
top_user = fetch_top_user_data()
top_ins= fetch_top_ins_data()
