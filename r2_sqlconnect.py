import pymysql
import pandas as pd
from r1_transformdata import agg_trans,agg_user,agg_ins
from r1_transformdata import map_trans,map_user,map_ins
from r1_transformdata import top_trans,top_user,top_ins

#Connecting with SQL
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
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM agg_trans 
            WHERE state = %s AND year = %s AND quarter = %s AND transaction_type = %s
        """, (row['State'], row['Year'], row['Quarter'], row['Transaction_type']))
        
        count_result = cursor.fetchone()
            
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
            cursor.execute("""
                INSERT INTO agg_trans (state, year, quarter, transaction_type, transaction_count, transaction_amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['Transaction_type'], row['Transaction_count'], row['Transaction_amount']))
       

        
def insert_agg_user_data(cursor, agg_user):
    for _, row in agg_user.iterrows():
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM agg_user 
            WHERE state = %s AND year = %s AND quarter = %s AND brand = %s
        """, (row['State'], row['Year'], row['Quarter'], row['Brand']))
        
        count_result = cursor.fetchone()
            
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
            cursor.execute("""
                INSERT INTO agg_user (state, year, quarter, brand, count, percentage)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['Brand'], row['Count'], row['Percentage']))

def insert_agg_ins_data(cursor, agg_ins):
    for _, row in agg_ins.iterrows():
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM agg_ins 
            WHERE state = %s AND year = %s AND quarter = %s AND transaction_type = %s
        """, (row['State'], row['Year'], row['Quarter'], row['Transaction_type']))
        
        count_result = cursor.fetchone()
            
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
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


def insert_map_trans_data(cursor, map_trans):
    for _, row in map_trans.iterrows():
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM map_trans 
            WHERE state = %s AND year = %s AND quarter = %s AND user_district = %s
        """, (row['State'], row['Year'], row['Quarter'], row['User_District']))
        
        count_result = cursor.fetchone()
        
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
            cursor.execute("""
                INSERT INTO map_trans (state, year, quarter, user_district, transaction_count, transaction_amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['User_District'], row['Transaction_count'], row['Transaction_amount']))

def insert_map_user_data(cursor, map_user):
    for _, row in map_user.iterrows():
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM map_user 
            WHERE state = %s AND year = %s AND quarter = %s AND user_district = %s
        """, (row['State'], row['Year'], row['Quarter'], row['User_District']))
        
        count_result = cursor.fetchone()
        
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
            cursor.execute("""
                INSERT INTO map_user (state, year, quarter, user_district, registered_users, app_opens)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['User_District'], row['Registered_Users'], row['App_opens']))

def insert_map_ins_data(cursor, map_ins):
    for _, row in map_ins.iterrows():
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM map_ins 
            WHERE state = %s AND year = %s AND quarter = %s AND user_district = %s
        """, (row['State'], row['Year'], row['Quarter'], row['User_District']))
        
        count_result = cursor.fetchone()
        
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
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
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM top_trans 
            WHERE state = %s AND year = %s AND quarter = %s AND user_district_pincodes = %s
        """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes']))
        
        count_result = cursor.fetchone()
        
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
            cursor.execute("""
                INSERT INTO top_trans (state, year, quarter, user_district_pincodes, transaction_count, transaction_amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes'], row['Transaction_Count'], row['Transaction_Amount']))

def insert_top_user_data(cursor, top_user):
    for _, row in top_user.iterrows():
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM top_user 
            WHERE state = %s AND year = %s AND quarter = %s AND user_district_pincodes = %s
        """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes']))
        
        count_result = cursor.fetchone()
        
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
            cursor.execute("""
                INSERT INTO top_user (state, year, quarter, user_district_pincodes, registered_users)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes'], row['Registered_Users']))

def insert_top_ins_data(cursor, top_ins):
    for _, row in top_ins.iterrows():
        # Check if the record already exists
        cursor.execute("""
            SELECT COUNT(*) FROM top_ins 
            WHERE state = %s AND year = %s AND quarter = %s AND user_district_pincodes = %s
        """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes']))
        
        count_result = cursor.fetchone()
        
        # Extract the count value
        count_value = count_result[0] if count_result else None
    
        # Check if no such record exists, then insert the new record
        if count_value == 0:
            cursor.execute("""
                INSERT INTO top_ins (state, year, quarter, user_district_pincodes, transaction_count, transaction_amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['User_District_Pincodes'], row['Transaction_Count'], row['Transaction_Amount']))

# Create, Insert function call for Aggregated Data sets
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

# Create, Insert function call for Map Data sets
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
    
# Create, Insert function call for Top Data sets
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

#Inserting Data Frame into SQL
Aggregated_SQL(agg_trans,agg_user,agg_ins)
print("Aggregated_SQL Transfer Successfull")

Map_SQL(map_trans,map_user,map_ins)
print("Map_SQL Transfer Successfull")

Top_SQL(top_trans,top_user,top_ins)
print("Top_SQL Transfer Successfull")

print("All Table transferred to SQL Successfully")