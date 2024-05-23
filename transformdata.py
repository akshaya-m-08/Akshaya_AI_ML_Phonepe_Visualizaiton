import os
import subprocess
import json
import pandas as pd

#Clone Repo
def clone_repo():
    repo_url = "https://github.com/PhonePe/pulse.git"
    clone_dir = "phonepe_pulse"
    if not os.path.exists(clone_dir):
        subprocess.run(["git", "clone", repo_url, clone_dir])
    else:
        print("Repository already cloned.")

#Transform Data - Aggregated_Transactions
def load_agg_trans_data():
    path_agg_trans = "phonepe_pulse/data/aggregated/transaction/country/india/state/"
    agg_state_list = os.listdir(path_agg_trans)
    
    agg_trans = {'State':[], 
                 'Year':[],
                 'Quarter':[],
                 'Transaction_type':[], 
                 'Transaction_count':[], 
                 'Transaction_amount':[]}

    for state in agg_state_list:
        state_path = os.path.join(path_agg_trans, state)
        agg_years = os.listdir(state_path)
        
        for year in agg_years:
            year_path = os.path.join(state_path, year)
            agg_quarters = os.listdir(year_path)
            
            for quarter in agg_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            if data.get('success') and data.get('data'):
                                for transaction in data['data']['transactionData']:
                                    count = transaction['paymentInstruments'][0]['count']
                                    amount = transaction['paymentInstruments'][0]['amount']
                                    agg_trans['Transaction_type'].append(transaction.get('name'))
                                    agg_trans['Transaction_count'].append(count)
                                    agg_trans['Transaction_amount'].append(amount)
                                    agg_trans['State'].append(state)
                                    agg_trans['Year'].append(year)
                                    agg_trans['Quarter'].append(int(quarter.strip('.json')))
                    
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(agg_trans)

#Transform Data - Aggregate User

def load_agg_user_data():
    path_agg_user = "phonepe_pulse/data/aggregated/user/country/india/state/"
    agg_state_list = os.listdir(path_agg_user)
    
    agg_user = {'State':[], 
                'Year':[],
                'Quarter':[],
                'Brand':[], 
                'Count':[], 
                'Percentage':[]}

    for state in agg_state_list:
        state_path = os.path.join(path_agg_user, state)
        agg_years = os.listdir(state_path)
        
        for year in agg_years:
            year_path = os.path.join(state_path, year)
            agg_quarters = os.listdir(year_path)
            
            for quarter in agg_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            
                            if data.get('success') and data.get('data'):
                                users_by_device = data['data'].get('usersByDevice')
                                if users_by_device:
                                    for user in users_by_device:
                                        agg_user['Brand'].append(user.get('brand'))
                                        agg_user['Count'].append(user.get('count'))
                                        agg_user['Percentage'].append(user.get('percentage'))
                                        agg_user['State'].append(state)
                                        agg_user['Year'].append(year)
                                        agg_user['Quarter'].append(int(quarter.strip('.json')))           
                                
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(agg_user)

#Transform Data - Aggregate Insurance

def load_agg_ins_data():
    path_agg_ins = "phonepe_pulse/data/aggregated/insurance/country/india/state/"
    agg_state_list = os.listdir(path_agg_ins)
    
    agg_ins = {'State':[], 
               'Year':[],
               'Quarter':[],
               'Transaction_type':[], 
               'Transaction_count':[], 
               'Transaction_amount':[]}

    for state in agg_state_list:
        state_path = os.path.join(path_agg_ins, state)
        agg_years = os.listdir(state_path)
        
        for year in agg_years:
            year_path = os.path.join(state_path, year)
            agg_quarters = os.listdir(year_path)
            
            for quarter in agg_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            if data.get('success') and data.get('data'):
                                for insurance in data['data']['transactionData']:
                                    count = insurance['paymentInstruments'][0]['count']
                                    amount = insurance['paymentInstruments'][0]['amount']
                                    agg_ins['Transaction_type'].append(insurance.get('name'))
                                    agg_ins['Transaction_count'].append(count)
                                    agg_ins['Transaction_amount'].append(amount)
                                    agg_ins['State'].append(state)
                                    agg_ins['Year'].append(year)
                                    agg_ins['Quarter'].append(int(quarter.strip('.json')))
                    
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(agg_ins)

#Transform Data - Map Transactions

def load_map_trans_data():
    path_map_trans = "phonepe_pulse/data/map/transaction/hover/country/india/state"
    map_state_list = os.listdir(path_map_trans)
    
    map_trans = {'State':[], 
                 'Year':[],
                 'Quarter':[],
                 'User_District':[], 
                 'Transaction_count':[], 
                 'Transaction_amount':[]}

    for state in map_state_list:
        state_path = os.path.join(path_map_trans, state)
        map_years = os.listdir(state_path)
        
        for year in map_years:
            year_path = os.path.join(state_path, year)
            map_quarters = os.listdir(year_path)
            
            for quarter in map_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            if data.get('success') and data.get('data'):
                                for transaction in data['data']['hoverDataList']:
                                    count = transaction['metric'][0]['count']
                                    amount = transaction['metric'][0]['amount']
                                    map_trans['User_District'].append(transaction.get('name'))
                                    map_trans['Transaction_count'].append(count)
                                    map_trans['Transaction_amount'].append(amount)
                                    map_trans['State'].append(state)
                                    map_trans['Year'].append(year)
                                    map_trans['Quarter'].append(int(quarter.strip('.json')))
                    
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(map_trans)

#Transform Data - Map User

def load_map_user_data():
    path_map_user = "phonepe_pulse/data/map/user/hover/country/india/state"
    map_state_list = os.listdir(path_map_user)
    
    map_user = {
        'State': [],
        'Year': [],
        'Quarter': [],
        'User_District': [],
        'Registered_Users': [],
        'App_opens': []
    }

    for state in map_state_list:
        state_path = os.path.join(path_map_user, state)
        map_years = os.listdir(state_path)
        
        for year in map_years:
            year_path = os.path.join(state_path, year)
            map_quarters = os.listdir(year_path)
            
            for quarter in map_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            if data.get('success') and data.get('data'):
                                for district, user_data in data['data']['hoverData'].items():
                                    registered_users = user_data['registeredUsers']
                                    app_opens = user_data['appOpens']
                                    map_user['User_District'].append(district)
                                    map_user['Registered_Users'].append(registered_users)
                                    map_user['App_opens'].append(app_opens)
                                    map_user['State'].append(state)
                                    map_user['Year'].append(year)
                                    map_user['Quarter'].append(int(quarter.strip('.json')))
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(map_user)

#Transform Data - Map Insurance

def load_map_ins_data():
    path_map_ins = "phonepe_pulse/data/map/insurance/hover/country/india/state"
    map_state_list = os.listdir(path_map_ins)
    
    map_ins = {'State':[], 'Year':[],'Quarter':[],'User_District':[], 'Transaction_count':[], 'Transaction_amount':[]}

    for state in map_state_list:
        state_path = os.path.join(path_map_ins, state)
        map_years = os.listdir(state_path)
        
        for year in map_years:
            year_path = os.path.join(state_path, year)
            map_quarters = os.listdir(year_path)
            
            for quarter in map_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            if data.get('success') and data.get('data'):
                                for insurance in data['data']['hoverDataList']:
                                    count = insurance['metric'][0]['count']
                                    amount = insurance['metric'][0]['amount']
                                    map_ins['User_District'].append(insurance.get('name'))
                                    map_ins['Transaction_count'].append(count)
                                    map_ins['Transaction_amount'].append(amount)
                                    map_ins['State'].append(state)
                                    map_ins['Year'].append(year)
                                    map_ins['Quarter'].append(int(quarter.strip('.json')))
                    
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(map_ins)

#Transform Data - Top Transactions

def load_top_trans_data():
    path_top_trans = "phonepe_pulse/data/top/transaction/country/india/state"
    top_state_list = os.listdir(path_top_trans)
    
    top_trans = {
        'State': [],
        'Year': [],
        'Quarter': [],
        'User_District_Pincodes': [],
        'Transaction_Count': [],
        'Transaction_Amount': []
    }

    for state in top_state_list:
        state_path = os.path.join(path_top_trans, state)
        top_years = os.listdir(state_path)
        
        for year in top_years:
            year_path = os.path.join(state_path, year)
            top_quarters = os.listdir(year_path)
            
            for quarter in top_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            if data.get('success') and data.get('data'):
                                for transactions in data['data']['pincodes']:
                                    count = transactions['metric']['count']
                                    amount = transactions['metric']['amount']
                                    top_trans['User_District_Pincodes'].append(transactions.get('entityName'))
                                    top_trans['Transaction_Count'].append(count)
                                    top_trans['Transaction_Amount'].append(amount)
                                    top_trans['State'].append(state)
                                    top_trans['Year'].append(year)
                                    top_trans['Quarter'].append(int(quarter.strip('.json')))
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(top_trans)

#Transform Data - Top User

def load_top_user_data():
    path_top_user= "phonepe_pulse/data/top/user/country/india/state"
    top_state_list = os.listdir(path_top_user)
    
    top_user = {
        'State': [],
        'Year': [],
        'Quarter': [],
        'User_District_Pincodes': [],
        'Registered_User': []
    }

    for state in top_state_list:
        state_path = os.path.join(path_top_user, state)
        top_years = os.listdir(state_path)
        
        for year in top_years:
            year_path = os.path.join(state_path, year)
            top_quarters = os.listdir(year_path)
            
            for quarter in top_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            if data.get('success') and data.get('data'):
                                for user in data['data']['pincodes']:
                                    top_user['User_District_Pincodes'].append(user.get('name'))
                                    top_user['Registered_User'].append(user.get('registeredUsers'))
                                    top_user['State'].append(state)
                                    top_user['Year'].append(year)
                                    top_user['Quarter'].append(int(quarter.strip('.json')))
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(top_user)

#Transform Data - Top Insurance

def load_top_ins_data():
    path_top_ins = "phonepe_pulse/data/top/insurance/country/india/state"
    top_state_list = os.listdir(path_top_ins)
    
    top_ins = {
        'State': [],
        'Year': [],
        'Quarter': [],
        'User_District_Pincodes': [],
        'Transaction_Count': [],
        'Transaction_Amount': []
    }

    for state in top_state_list:
        state_path = os.path.join(path_top_ins, state)
        top_years = os.listdir(state_path)
        
        for year in top_years:
            year_path = os.path.join(state_path, year)
            top_quarters = os.listdir(year_path)
            
            for quarter in top_quarters:
                if quarter.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter)
                    try:
                        with open(quarter_path, 'r') as file:
                            data = json.load(file)
                            if data.get('success') and data.get('data'):
                                for insurance in data['data']['pincodes']:
                                    count = insurance['metric']['count']
                                    amount = insurance['metric']['amount']
                                    top_ins['User_District_Pincodes'].append(insurance.get('entityName'))
                                    top_ins['Transaction_Count'].append(count)
                                    top_ins['Transaction_Amount'].append(amount)
                                    top_ins['State'].append(state)
                                    top_ins['Year'].append(year)
                                    top_ins['Quarter'].append(int(quarter.strip('.json')))
                    except Exception as e:
                        print(f"Error reading {quarter_path}: {e}")
    
    return pd.DataFrame(top_ins)


