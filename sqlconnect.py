import pymysql
import pandas as pd

def my_sql_connect():
    conn = pymysql.connect(
        host="localhost",
        port = 3307,
        user="root",
        password="root")
    
    return conn


#Creating a database
def select_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_pulse")
    cursor.execute("USE phonepe_pulse")
    
    
# Creating Aggregated Transaction, User, Insurance Table
def create_Agg_Trans_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agg_trans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            transaction_type VARCHAR(50),
            transaction_count INT,
            transaction_amount FLOAT
        )
    """)
    
def create_Agg_User_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agg_user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            brand VARCHAR(50),
            count INT,
            percentage FLOAT
        )
    """)

def create_Agg_Ins_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agg_ins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            transaction_type VARCHAR(50),
            transaction_count INT,
            transaction_amount FLOAT
        )
    """)


#Inserting Aggregated Transactions, User, Insurance data into SQL
def insert_agg_trans_data(cursor, agg_trans):
    for _, row in agg_trans.iterrows():
        cursor.execute("""
            INSERT INTO agg_trans (state, year, quarter, transaction_type, transaction_count, transaction_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['Transaction_type'], row['Transaction_count'], row['Transaction_amount']))

def insert_agg_user_data(cursor, agg_user):
    for _, row in agg_user.iterrows():
        cursor.execute("""
            INSERT INTO agg_user (state, year, quarter, brand, count, percentage)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['Brand'], row['Count'], row['Percentage']))

def insert_agg_ins_data(cursor, agg_ins):
    for _, row in agg_ins.iterrows():
        cursor.execute("""
            INSERT INTO agg_ins (state, year, quarter, transaction_type, transaction_count, transaction_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['Transaction_type'], row['Transaction_count'], row['Transaction_amount']))

# Creating Map Transaction, User, Insurance Table
def create_Map_Trans_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS map_trans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            user_district VARCHAR(50),
            transaction_count INT,
            transaction_amount FLOAT
        )
    """)
    
def create_Map_User_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS map_user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            user_district VARCHAR(50),
            registered_users INT,
            app_opens INT
        )
    """)

def create_Map_Ins_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS map_ins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            user_district VARCHAR(50),
            transaction_count INT,
            transaction_amount FLOAT
        )
    """)


#Inserting Map Transactions, User, Insurance data into SQL
def insert_map_trans_data(cursor, map_trans):
    for _, row in map_trans.iterrows():
        cursor.execute("""
            INSERT INTO map_trans (state, year, quarter, user_district, transaction_count, transaction_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['User_District'], row['Transaction_count'], row['Transaction_amount']))

def insert_map_user_data(cursor, map_user):
    for _, row in map_user.iterrows():
        cursor.execute("""
            INSERT INTO map_user (state, year, quarter, user_district, registered_users, app_opens)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['User_District'], row['Registered_Users'], row['App_opens']))

def insert_map_ins_data(cursor, map_ins):
    for _, row in map_ins.iterrows():
        cursor.execute("""
            INSERT INTO map_ins (state, year, quarter, user_district, transaction_count, transaction_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['User_District'], row['Transaction_count'], row['Transaction_amount']))

# Creating Top Transaction, User, Insurance Table
def create_Top_Trans_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_trans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            user_district_pincodes INT,
            transaction_count INT,
            transaction_amount FLOAT
        )
    """)
    
def create_Top_User_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            user_district_pincodes INT,
            registered_users INT
        )
    """)

def create_Top_Ins_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_ins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state VARCHAR(50),
            year INT,
            quarter INT,
            user_district_pincodes INT,
            transaction_count INT,
            transaction_amount FLOAT
        )
    """)

#Inserting Top Transactions, User, Insurance data into SQL
def insert_top_trans_data(cursor, top_trans):
    for _, row in top_trans.iterrows():
        cursor.execute("""
            INSERT INTO top_trans (state, year, quarter, user_district_pincodes, transaction_count, transaction_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes'], row['Transaction_Count'], row['Transaction_Amount']))

def insert_top_user_data(cursor, top_user):
    for _, row in top_user.iterrows():
        cursor.execute("""
            INSERT INTO top_user (state, year, quarter, user_district_pincodes, registered_users)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes'], row['Registered_Users']))

def insert_top_ins_data(cursor, top_ins):
    for _, row in top_ins.iterrows():
        cursor.execute("""
            INSERT INTO top_ins (state, year, quarter, user_district_pincodes, transaction_count, transaction_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes'], row['Transaction_Count'], row['Transaction_Amount']))

def Aggregated_SQL(agg_trans,agg_user,agg_ins):
    
    conn=my_sql_connect()
    
    cursor = conn.cursor()
    
    select_database(cursor)
    
    #Aggregated Tables
    create_Agg_Trans_table(cursor)
    create_Agg_User_table(cursor)
    create_Agg_Ins_table(cursor)
    insert_agg_trans_data(cursor, agg_trans)
    insert_agg_user_data(cursor, agg_user)
    insert_agg_ins_data(cursor, agg_ins)
    
    conn.commit()
    cursor.close()
    conn.close()


def Map_SQL(map_trans,map_user,map_ins):
    
    conn=my_sql_connect()
    
    cursor = conn.cursor()   
    
    select_database(cursor)
     
    #Map Tables
    create_Map_Trans_table(cursor)
    create_Map_User_table(cursor)
    create_Map_Ins_table(cursor)
    insert_map_trans_data(cursor, map_trans)
    insert_map_user_data(cursor, map_user)
    insert_map_ins_data(cursor, map_ins)
    
    conn.commit()
    cursor.close()
    conn.close()
    

def Top_SQL(top_trans,top_user,top_ins):
    
    conn=my_sql_connect()
    
    cursor = conn.cursor()     
    
    select_database(cursor)
    
    #Top Tables
    create_Top_Trans_table(cursor)
    create_Top_User_table(cursor)
    create_Top_Ins_table(cursor)
    insert_top_trans_data(cursor, top_trans)
    insert_top_user_data(cursor, top_user)
    insert_top_ins_data(cursor, top_ins)
    
    conn.commit()
    cursor.close()
    conn.close()
    
import pymysql
def my_sql_database_connect():
    conn = pymysql.connect(
        host="localhost",
        port=3307,
        user="root",
        password="root",
        database="phonepe_pulse"
    )
    
    return conn

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
