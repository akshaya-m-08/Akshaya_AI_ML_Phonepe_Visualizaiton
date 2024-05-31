def app():

    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import json
    from streamlit_option_menu import option_menu
    from babel.numbers import format_currency
    from r3_fetchsql import agg_trans,agg_user,agg_ins,map_trans,map_user,map_ins,top_trans,top_user,top_ins
    import plotly.io as pio


    pio.templates.default = None

    st.markdown("""
    <style>
        .stButton>button {
        display: block;
        margin: 0 auto;
        width: 100%;
        font-size: 20px; !important;
        color: white !important;
        background-color: #391C59 !important;
        text-align: center !important; 
        font-weight: bold;
    }
    .stButton>button:hover {
        color: white !important;
        background-color: #05C2DD !important;
    }
    .stButton>button:focus {
        color: white !important;
        background-color: #230B43 !important;    
    }
    [data-testid="stMetric"] 
    {
        background-color: #391C59; 
        text-align: center;
        padding: 5px 0;
        font-weight: bold;
        border-radius: 15px;
        color: #05C2DD; 
        width: 400px;
    }

    [data-testid="stTable"] {
        width: 450px;
        height: 460px;
        overflow-y: auto;
        background-color: #391C59;
        border-radius: 8px;  
        font-size: 19px;
        color: white;
        border-right: none; 
        border-left: none; 
        border-top: none; 
        border-bottom: none; 
    }
    [data-testid="stTable"] thead th {
        font-size: 20px;
        text-align: center !important; 
        font-weight: bold;
        border-right: none; 
        border-left: none; 
        border-top: none; 
        border-bottom: none; 
    }

    [data-testid="stTable"] tbody td {
        text-align: left !important; 
        font-size: 20px;
        border-right: none; 
        border-left: none; 
        border-top: none; 
        border-bottom: none; 
    }

    [data-testid="stTable"] table tbody td{
        color: white;
        border-right: none; 
        border-left: none; 
        border-top: none; 
        border-bottom: none; 
    }
    [data-testid="stTable"] table th,
    [data-testid="stTable"] table tbody td:first-child {
        border-right: none; 
        border-left: none; 
        border-top: none; 
        border-bottom: none; 
        color: white; 
    }
    [data-testid="stTable"] table tbody td:nth-child(odd) {
        text-align: right !important;
        color: #05C2DD !important;
        font-weight: bold !important;
        font-size: 22px !important;
        border-right: none; 
        border-left: none; 
        border-top: none; 
        border-bottom: none; 
   
    }
    [data-testid="stTable"] table tbody td:first-child {
        text-align: left !important;
        color: white!important;
        font-weight: italic !important;
        font-size: 22px !important;
        border-right: none; 
        border-left: none; 
        border-top: none; 
        border-bottom: none; 
    }
    [data-testid="stTable"] tbody tr:nth-child(even),
    [data-testid="stTable"] tbody tr:nth-child(odd) {
        background-color: #391C59; 
        border-right: none; 
        border-left: none; 
        border-top: none; 
        border-bottom: none; 
    }
    </style>
    """, unsafe_allow_html=True)

    def format_amount(amount):
        def format_indian_number(number):
            num_str = str(int(number))[::-1]
            formatted_str = ""
            for i in range(len(num_str)):
                if i != 0 and (i == 3 or (i > 3 and (i - 1) % 2 == 0)):
                    formatted_str += ','
                formatted_str += num_str[i]
            return formatted_str[::-1]

        if amount >= 1e7:
            amount_in_crore = amount / 1e7
            formatted_amount = format_currency(amount_in_crore, 'INR', locale='en_IN')
            return f"{formatted_amount} Cr"
        elif amount >= 1e5:
            amount_in_lakhs = amount / 1e5
            formatted_amount = format_currency(amount_in_lakhs, 'INR', locale='en_IN')
            return f"{formatted_amount} L"
        elif amount >= 1e3:
            amount_in_thousand = amount / 1e3
            formatted_amount = format_currency(amount_in_thousand, 'INR', locale='en_IN')
            return f"{formatted_amount} K"
        else:
            formatted_amount = format_currency(amount, 'INR', locale='en_IN')
            return format_indian_number(amount)

    
    def format_number(number):
        num_str = str(int(number))[::-1]  
        formatted_str = ""
        for i in range(len(num_str)):
            if i != 0 and (i == 3 or (i > 3 and (i - 1) % 2 == 0)):
                formatted_str += ','
            formatted_str += num_str[i]
        return formatted_str[::-1]


    
    selected = option_menu(
    menu_title=None,
    options=["Transaction Data", "Insurance Data","User Data"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    )
    if selected == "Transaction Data":

        col1, col2, co3,col4,col5,col6 = st.columns((0.7,0.8,1,1,1,1),gap="large")
        with col1:
            years = st.selectbox("#### Select Year", options=agg_trans["Year"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter", options=agg_trans["Quarter"].unique())
        with co3:
            states = st.selectbox("#### Select State", options=agg_trans["State"].unique())            
        st.markdown(f"<h1 style='font-size: 30px'> {states} Transaction Data", unsafe_allow_html=True)


        trans_selected_year = agg_trans[(agg_trans['Year'] == years) & 
                                        (agg_trans['Quarter'] == quarters) & (agg_trans['State'] == states)] 
        trans_selected_year_dist = map_trans[(map_trans['Year'] == years) & 
                                        (map_trans['Quarter'] == quarters) & (map_trans['State'] == states)]        
        trans_selected_year_pin = top_trans[(top_trans['Year'] == years) & 
                                        (top_trans['Quarter'] == quarters) & (top_trans['State'] == states)] 
        
        if trans_selected_year.empty:
            st.error("#### No data available for the selected year and quarter.")
            
        else:
            trans_selected_year_grouped = trans_selected_year.groupby('State').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
            trans_selected_year_grouped['Serial'] = range(1, len(trans_selected_year_grouped) + 1)
            trans_selected_year_grouped = trans_selected_year_grouped.head(10)

            total_transactions = trans_selected_year['Transaction_count'].sum()
            total_payment_value = trans_selected_year['Transaction_amount'].sum()
            avg_transaction_value = total_payment_value / total_transactions
            total_transactions = format_number(total_transactions)
            col_map, col_data = st.columns((5, 1.65), gap='large')
            with col_map:
                trans_selected_year_dist.loc[:, 'Transaction_amount'] = trans_selected_year_dist['Transaction_amount'].apply(format_amount)
                trans_selected_year_map=trans_selected_year_dist
                trans_selected_year_map.rename(columns={'Transaction_amount': 'Transaction Amount', 'Transaction_count': 'Transaction Count'}, inplace=True)
                formatted_state_name = states.replace(' ', '').lower()
                if formatted_state_name == "andaman&nicobarislands":
                    formatted_state_name='andamanandnicobarislands'
                if formatted_state_name == "dadra&nagarhaveli&daman&diu":
                    formatted_state_name='dadranagarhaveli'
                if formatted_state_name == "jammu&kashmir":
                    formatted_state_name='jammuandkashmir'                      
                geojson_file_path = f'json/state-geojson-master/{formatted_state_name}.json'
                with open(geojson_file_path) as f:
                    state_geojson = json.load(f)
                state_choropleth = px.choropleth(
                            trans_selected_year_map,
                            geojson=state_geojson,
                            featureidkey='properties.district',
                            locations='User_District',
                            projection="mercator",
                            hover_data=['Year','Transaction Amount','Transaction Count'],
                            color='Transaction Amount',
                            color_discrete_sequence=px.colors.sequential.Viridis,
                            range_color=(trans_selected_year_map['Transaction Amount'].min(), trans_selected_year_map['Transaction Amount'].max())
                            )

                state_choropleth.update_geos(fitbounds="locations", visible=False)
                
                state_choropleth.update_layout(
                    width=1200,  
                    height=800, 
                    margin={"r":0,"t":0,"l":0,"b":0},
                    geo=dict(bgcolor='rgba(0,0,0,0)'))
                st.plotly_chart(state_choropleth,use_container_width=True)

            with col_data:
                st.write(f'#### Total Transactions (Q {quarters}) {years})')
                st.metric(label='', value=total_transactions)
                st.write(f'#### Total Payment Value (Q {quarters}) {years})')
                st.metric(label='', value=format_amount(total_payment_value))
                st.write(f'#### Average Payment Value (Q {quarters}) {years})')
                st.metric(label='', value=f"₹{avg_transaction_value:,.0f}")
                st.markdown('***')
                
                trans_selected_year_grp = trans_selected_year.groupby('Transaction_type').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                trans_selected_year_grp['Serial'] = range(1, len(trans_selected_year_grp) + 1)
 
                df = pd.DataFrame(trans_selected_year_grp[['Serial', 'Transaction_type', 'Transaction_amount']])
                df['Transaction_amount']=df['Transaction_amount'].apply(format_amount)
                
                st.markdown("<h1 style='font-size: 30px'>Categorical Data</h1>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                
                for index, row in df.iterrows():
                    with col1:
                        st.markdown(f"<p style='font-size:18px;text-align: left'>{row['Transaction_type']}</p>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<p style='font-size:18px;text-align: right; color:#05C2DD;font-weight:bold'>{row['Transaction_amount']}</p>", unsafe_allow_html=True)

                st.markdown("***")
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11,c13 = st.columns(2)
                with c11:
                    if st.button("# Districts"):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes"):
                        postal_codes_button_clicked = True                
            
                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'> Top 10 Districts", unsafe_allow_html=True)
                    trans_selected_year_grouped_dist = trans_selected_year_dist.groupby('User_District').sum().reset_index().sort_values(by="Transaction Amount", ascending=False)
                    trans_selected_year_grouped_dist['Serial'] = range(1, len(trans_selected_year_grouped_dist) + 1)
                    trans_selected_year_grouped_dist = trans_selected_year_grouped_dist.head(10)
                    df=pd.DataFrame(trans_selected_year_grouped_dist[['Serial', 'User_District', 'Transaction Amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['User District', 'Transaction Amount']
                    st.table(df)  
    
                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'>Top 10 Postal Codes", unsafe_allow_html=True)
                    trans_selected_year_grouped_pin = trans_selected_year_pin.groupby('User_District_Pincodes').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                    trans_selected_year_grouped_pin['Serial'] = range(1, len(trans_selected_year_grouped_pin) + 1)
                    trans_selected_year_grouped_pin['User_District_Pincodes'] = trans_selected_year_grouped_pin['User_District_Pincodes'].apply(lambda x: '{:.0f}'.format(x))
                    trans_selected_year_grouped_pin['Transaction_amount'] = trans_selected_year_grouped_pin['Transaction_amount'].apply(format_amount)
                    df=pd.DataFrame(trans_selected_year_grouped_pin[['Serial', 'User_District_Pincodes', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Postal Codes', 'Transaction Amount']
                    st.table(df)    
            
    if selected == "Insurance Data":

        col1, col2, co3,col4,col5,col6 = st.columns((0.7,0.8,1,1,1,1),gap="large")
        with col1:
            years = st.selectbox("#### Select Year", options=agg_ins["Year"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter", options=agg_ins["Quarter"].unique())
        with co3:
            states = st.selectbox("#### Select State", options=agg_ins["State"].unique())
        st.markdown(f"<h1 style='font-size: 30px'> {states} Insurance Data", unsafe_allow_html=True)
            

        ins_selected_year = agg_ins[(agg_ins['Year'] == years) & 
                                        (agg_ins['Quarter'] == quarters) & (agg_ins['State'] == states)] 
        ins_selected_year_dist = map_ins[(map_ins['Year'] == years) & 
                                        (map_ins['Quarter'] == quarters) & (map_ins['State'] == states)]        
        ins_selected_year_pin = top_ins[(top_ins['Year'] == years) & 
                                        (top_ins['Quarter'] == quarters) & (top_ins['State'] == states)]
        

        if ins_selected_year.empty:
            st.error("No data available for the selected year and quarter.")
            
        else:
            ins_selected_year_grouped = ins_selected_year.groupby('State').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
            ins_selected_year_grouped['Serial'] = range(1, len(ins_selected_year_grouped) + 1)
            ins_selected_year_grouped = ins_selected_year_grouped.head(10)

            total_transactions = ins_selected_year['Transaction_count'].sum()
            total_payment_value = ins_selected_year['Transaction_amount'].sum()
            avg_transaction_value = total_payment_value / total_transactions
            total_transactions = format_number(total_transactions)
            
            col_map, col_data = st.columns((5, 1.65), gap='large')
             
            with col_map:
 
                ins_selected_year_dist.loc[:, 'Transaction_amount'] = ins_selected_year_dist['Transaction_amount'].apply(format_amount)
                ins_selected_year_dist_map=ins_selected_year_dist
                ins_selected_year_dist_map=ins_selected_year_dist_map.rename(columns={'Transaction_amount': 'Premium Amount', 'Transaction_count': 'Premium Count'})
                formatted_state_name = states.replace(' ', '').lower()
                if formatted_state_name == "andaman&nicobarislands":
                    formatted_state_name='andamanandnicobarislands'
                if formatted_state_name == "dadra&nagarhaveli&daman&diu":
                    formatted_state_name='dadranagarhaveli'        
                if formatted_state_name == "jammu&kashmir":
                    formatted_state_name='jammuandkashmir'                              
                geojson_file_path = f'json/state-geojson-master/{formatted_state_name}.json'
                with open(geojson_file_path) as f:
                    state_geojson = json.load(f)
                state_ins_choropleth = px.choropleth(
                            ins_selected_year_dist_map,
                            geojson=state_geojson,
                            featureidkey='properties.district',
                            locations='User_District',
                            projection="mercator",
                            hover_data=['Year','Premium Amount','Premium Count'],
                            color='Premium Amount',
                            color_discrete_sequence=px.colors.sequential.Viridis,
                            range_color=(ins_selected_year_dist_map['Premium Amount'].min(), ins_selected_year_dist_map['Premium Amount'].max())
                            )

                state_ins_choropleth.update_geos(fitbounds="locations", visible=False)
                
                state_ins_choropleth.update_layout(
                    width=1200,  
                    height=800, 
                    margin={"r":0,"t":0,"l":0,"b":0},
                    geo=dict(bgcolor='rgba(0,0,0,0)'))
                st.plotly_chart(state_ins_choropleth,use_container_width=True)    

            with col_data:
                st.write(f'#### Total Premium Count (Q{quarters}) {years})')
                st.metric(label='', value=total_transactions)
                st.write(f'#### Total Premium Value (Q{quarters}) {years})')
                st.metric(label='', value=format_amount(total_payment_value))
                st.write(f'#### Average Premium Value (Q{quarters}) {years})')
                st.metric(label='', value=f"₹{avg_transaction_value:,.0f}")                
                
                st.markdown('***')   
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c13 = st.columns(2)
                with c11:
                    if st.button("# Districts"):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes"):
                        postal_codes_button_clicked = True 
                           
                if districts_button_clicked:
                    st.markdown('#### Top 10 Districts')
                    ins_selected_year_grouped_dist = ins_selected_year_dist.groupby('User_District').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                    ins_selected_year_grouped_dist['Serial'] = range(1, len(ins_selected_year_grouped_dist) + 1)
                    ins_selected_year_grouped_dist = ins_selected_year_grouped_dist.head(10)
                    df=pd.DataFrame(ins_selected_year_grouped_dist[['Serial', 'User_District', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['User District', 'Premium Amount']
                    st.table(df)                     
       
                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'>Top 10 Postal Codes", unsafe_allow_html=True)
                    ins_selected_year_grouped_pin = ins_selected_year_pin.groupby('User_District_Pincodes').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                    ins_selected_year_grouped_pin['Serial'] = range(1, len(ins_selected_year_grouped_pin) + 1)
                    ins_selected_year_grouped_pin['User_District_Pincodes'] = ins_selected_year_grouped_pin['User_District_Pincodes'].apply(lambda x: '{:.0f}'.format(x))
                    ins_selected_year_grouped_pin['Transaction_amount'] = ins_selected_year_grouped_pin['Transaction_amount'].apply(format_amount)                    
                    df=pd.DataFrame(ins_selected_year_grouped_pin[['Serial', 'User_District_Pincodes', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['User Postal Codes', 'Premium Amount']
                    st.table(df)  
                    
                    
    if selected == "User Data":
        col1, col2, co3,col4,col5,col6 = st.columns((0.7,0.8,1,1,1,1),gap="large")
        with col1:
            years = st.selectbox("#### Select Year", options=map_user["Year"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter", options=map_user["Quarter"].unique())
        with co3:
            states = st.selectbox("#### Select State", options=map_user["State"].unique())    

        user_selected_year = agg_user[(agg_user['Year'] == years) & 
                                        (agg_user['Quarter'] == quarters) & (agg_user['State'] == states) ]
        user_selected_year_dist = map_user[(map_user['Year'] == years) & 
                                        (map_user['Quarter'] == quarters) & (map_user['State'] == states) ]     
        user_selected_year_pin = top_user[(top_user['Year'] == years) &
                                        (top_user['Quarter'] == quarters) & (top_user['State'] == states) ]
        st.markdown(f"<h1 style='font-size: 30px'> {states} Insurance User Data", unsafe_allow_html=True)
        if user_selected_year.empty:
            st.error("#### No data available for the selected year and quarter.")
            
        else:
            user_selected_year_grouped = user_selected_year_dist.groupby('State').sum().reset_index().sort_values(by="Registered_Users", ascending=False)
            user_selected_year_group = user_selected_year.groupby('State').sum().reset_index().sort_values(by="Count", ascending=False)
            user_selected_year_grouped['Serial'] = range(1, len(user_selected_year_grouped) + 1)

            total_user = user_selected_year_group['Count'].sum()
            total_app_opens = user_selected_year_grouped['App_opens'].sum()
            total_app_opens = format_amount(total_app_opens)
            total_user = format_amount(total_user)
              
            col_map, col_data = st.columns((5, 1.65), gap='large')
            
            with col_map:
                user_selected_year_dist_map = user_selected_year_dist
                user_selected_year_dist_map["Registered_Users"] = user_selected_year_dist_map["Registered_Users"].apply(format_number)
                user_selected_year_dist_map["App_opens"] = user_selected_year_dist_map["App_opens"].apply(format_number)
                user_selected_year_dist_map= user_selected_year_dist_map.rename(columns={'Registered_Users': 'Total User', 'App_opens': 'App Open Count'})
                formatted_state_name = states.replace(' ', '').lower()
                if formatted_state_name == "andaman&nicobarislands":
                    formatted_state_name='andamanandnicobarislands'
                if formatted_state_name == "dadra&nagarhaveli&daman&diu":
                    formatted_state_name='dadranagarhaveli'   
                if formatted_state_name == "jammu&kashmir":
                    formatted_state_name='jammuandkashmir'                                  
                geojson_file_path = f'json/state-geojson-master/{formatted_state_name}.json'
                with open(geojson_file_path) as f:
                    state_geojson = json.load(f)
                state_user_choropleth = px.choropleth(
                user_selected_year_dist_map,
                geojson=state_geojson,
                featureidkey='properties.district',
                locations='User_District',
                projection="mercator",
                hover_data=['Year','Total User','App Open Count'],
                color='Total User',
                color_discrete_sequence=px.colors.sequential.Viridis,
                range_color=(user_selected_year_dist_map['Total User'].min(), user_selected_year_dist_map['Total User'].max())
                )

                state_user_choropleth.update_geos(fitbounds="locations", visible=False)
                
                state_user_choropleth.update_layout(
                    width=1200,  
                    height=800, 
                    margin={"r":0,"t":0,"l":0,"b":0},
                    geo=dict(bgcolor='rgba(0,0,0,0)')

                )
                st.plotly_chart(state_user_choropleth,use_container_width=True)   

            with col_data:
                st.markdown(f'#### Total User Count (Q{quarters}) {years}')
                st.metric(label="",value=total_user)
                st.markdown(f'#### PhonePe app opens in (Q{quarters}) {years}')
                st.metric(label="",value=total_app_opens)                
                
                st.markdown('***')   
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c13 = st.columns(2)
                with c11:
                    if st.button("# Districts"):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes"):
                        postal_codes_button_clicked = True 

                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'> Top 10 Districts", unsafe_allow_html=True)
                    user_selected_year_grouped_dist = user_selected_year_dist.groupby('User_District').sum().reset_index().sort_values(by="Registered_Users", ascending=False)
                    user_selected_year_grouped_dist['Serial'] = range(1, len(user_selected_year_grouped_dist) + 1)
                    user_selected_year_grouped_dist = user_selected_year_grouped_dist.head(10)
                    df=pd.DataFrame(user_selected_year_grouped_dist[['Serial', 'User_District', 'Registered_Users']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Districts', 'Registered User']
                    st.table(df)
                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'>Top 10 Postal Codes", unsafe_allow_html=True)
                    user_selected_year_grouped_pin = user_selected_year_pin.groupby('User_District_Pincodes').sum().reset_index().sort_values(by="Registered_Users", ascending=False)
                    user_selected_year_grouped_pin['Serial'] = range(1, len(user_selected_year_grouped_pin) + 1)
                    user_selected_year_grouped_pin['User_District_Pincodes'] = user_selected_year_grouped_pin['User_District_Pincodes'].apply(lambda x: '{:.0f}'.format(x))
                    user_selected_year_grouped_pin['Registered_Users'] = user_selected_year_grouped_pin['Registered_Users'].apply(format_number)                    
                    df=pd.DataFrame(user_selected_year_grouped_pin[['Serial', 'User_District_Pincodes', 'Registered_Users']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Postal Codes', 'Registered User']
                    st.table(df)      
                     
                st.markdown("<h1 style='font-size: 30px'>Top 10 Brand Wise ", unsafe_allow_html=True)                     
                
                user_selected_year = user_selected_year.groupby('Brand').sum().reset_index().sort_values(by="Count", ascending=False)
                user_selected_year['Serial'] = range(1, len(user_selected_year) + 1)
                user_selected_year = user_selected_year.head(10)
                user_selected_year['Count']= user_selected_year['Count'].apply(format_number)
                df=pd.DataFrame(user_selected_year[['Serial', 'Brand', 'Count']])
                df.set_index('Serial', inplace=True)
                df.columns = ['Mobile Brands', 'User Count']
                st.table(df)  