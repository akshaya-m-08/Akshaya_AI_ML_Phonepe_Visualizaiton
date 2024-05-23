from transformdata import clone_repo
from transformdata import load_agg_trans_data,load_agg_user_data,load_agg_ins_data
from transformdata import load_map_trans_data,load_map_user_data,load_map_ins_data
from transformdata import load_top_trans_data,load_top_user_data,load_top_ins_data

from sqlconnect import Aggregated_SQL,Map_SQL,Top_SQL
from sqlconnect import fetch_agg_trans_data, fetch_agg_user_data, fetch_agg_ins_data
from sqlconnect import fetch_map_trans_data, fetch_map_user_data, fetch_map_ins_data
from sqlconnect import fetch_top_trans_data, fetch_top_user_data, fetch_top_ins_data

import streamlit as st
import plotly.express as px


#Get Phonepe Data from Repo
clone_repo()

# Transform Aggregate data
agg_trans = load_agg_trans_data()
agg_user = load_agg_user_data()
agg_ins = load_agg_ins_data()


# Transform Map data
map_trans = load_map_trans_data()
map_user = load_map_user_data()
map_ins = load_map_ins_data()


# Transform Top data
top_trans = load_top_trans_data()
top_user = load_top_user_data()
top_ins = load_top_ins_data()

Aggregated_SQL(agg_trans,agg_user,agg_ins)
Map_SQL(map_trans,map_user,map_ins)
Top_SQL(top_trans,top_user,top_ins)

df_agg_trans = fetch_agg_trans_data()
df_agg_user = fetch_agg_user_data()
df_agg_ins = fetch_agg_ins_data()

df_map_trans = fetch_map_trans_data()
df_map_user = fetch_map_user_data()
df_map_ins = fetch_map_ins_data()


df_top_trans = fetch_top_trans_data()
df_top_user = fetch_top_user_data()
df_top_ins= fetch_top_ins_data()
