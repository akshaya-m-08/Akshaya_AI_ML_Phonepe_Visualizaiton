from functions import clone_repo
from functions import load_agg_trans_data,load_agg_user_data,load_agg_ins_data
from functions import load_map_trans_data,load_map_user_data,load_map_ins_data
from functions import load_top_trans_data,load_top_user_data,load_top_ins_data

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
print(top_ins)