def app():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from babel.numbers import format_currency
    import streamlit as st
    from r3_fetchsql import agg_trans,agg_user,agg_ins,map_trans,map_user,map_ins

    st.markdown("""
    <style>
        .stTabs [role="tab"] {
            display: block;
            margin: 0 auto;
            width: 100%;
            font-size: 20px !important;
            color: white !important;
            background-color: #391C59 !important;
            text-align: center !important;
            font-weight: bold !important;
        }
        .stTabs [role="tab"]:hover {
            color: white !important;
            background-color: #05C2DD !important;
        }
        .stTabs [role="tab"]:focus {
            color: white !important;
            background-color: #230B43 !important;
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

    tab1, tab2= st.tabs(["# All India Insights", "# State-Wise Insights"])

    with tab1:     
        insight_options = [
            'Yearly Growth of Transaction Amount in India',
            'Yearly Growth of Transaction Count in India',
            'Yearly Growth of Insurance Premium amount in India',
            'Yearly Growth of Insurance Premium Count in India',
            'Yearly Growth of Registered User in India',
            'Yearly Growth of App Open in India',
            'Transaction Amount by State',
            'Transaction Count by State',
            'Transaction Count by Brand',
            'Insurance Premium Amount by State',
            'Insurance Premium Count by State',
            'Registered User by State',
            'App Opens by State',
            'State Wise - Brand & Transaction Amounts',
            'Transaction Types Analysis by Years and Quarters',
            'Average Transaction Amount by Quarter',
            'Percentage of Transactions by Type']

        selected_insight = st.selectbox('Select an Insight', insight_options)
#----------------------------------------------       
        if selected_insight == 'Yearly Growth of Transaction Amount in India':
            st.markdown('#### Yearly Growth of Transaction Amount in India')
            aggregated_data_yearly = agg_trans[agg_trans['Year'] != 2024].groupby('Year')['Transaction_amount'].sum().reset_index()
            aggregated_data_yearly['Transaction_amount']=aggregated_data_yearly['Transaction_amount'].apply(format_amount)
            fig = px.line(aggregated_data_yearly, x='Year', y='Transaction_amount', 
                    labels={'Year': 'Year', 'Transaction_amount': 'Transaction Amount'}, 
                    title='Yearly Growth of Transaction Amount in India')
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
                            
            on1 = st.toggle("Advanced Insights", key="states_toggle1")

            if on1:
                st.markdown("#### Quarterly Distribution of Transaction Amounts by Year in India")
                map1 , table1 = st.columns((5,2),gap= 'large')   
                aggregated_data1 = agg_trans.groupby(['Year', 'Quarter'])[['Transaction_amount','Transaction_count']].sum().reset_index()  
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Year'] = aggregated_data1['Year'].astype(str)
                with map1:   
                    fig = px.box(aggregated_data1, x='Year', y='Transaction_amount', color='Quarter',
                                title='Box Plot of Quarterly Transaction Amount by Year in India',
                                points='all',  
                                hover_data=['Transaction_count'])

                    st.plotly_chart(fig, use_container_width=True)
                with table1:  
                    distribution_data = aggregated_data1.groupby(['Year', 'Quarter']).agg({
                        'Transaction_amount': 'sum'
                    }).reset_index()

                    st.markdown('#### Quarterly Transaction Distribution')
                    st.dataframe(distribution_data, use_container_width=True, hide_index=True)   

                aggregated_data_state = agg_trans[agg_trans['Year'] != 2024].groupby(['Year', 'Quarter'])['Transaction_amount'].sum().reset_index()
                st.markdown('#### Quarterly Transaction Amount Distribution by Transaction Amount for Each Year')


                years = aggregated_data_state['Year'].unique()

                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_amount'], hole=.3)])
                        fig.update_layout(
                            title=f'Transaction Amount Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Aggregated Transaction Amount for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    aggregated_total = agg_trans.groupby(['Quarter'])['Transaction_amount'].sum().reset_index()


                    
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_amount'], hole=.3)])
                    fig_total.update_layout(
                        title='Aggregated Transaction Amount for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    
        
#----------------------------------------------                
        if selected_insight == "Yearly Growth of Transaction Count in India":
            st.markdown('#### Yearly Growth of Transaction Count in India')
            aggregated_data_yearly_count = agg_trans[agg_trans['Year'] != 2024].groupby('Year')['Transaction_count'].sum().reset_index()
            aggregated_data_yearly_count['Transaction_count']=aggregated_data_yearly_count['Transaction_count'].apply(format_number)
            fig = px.line(aggregated_data_yearly_count, x='Year', y='Transaction_count', 
                            labels={'Year': 'Year', 'Transaction_count': 'Transaction Count'}, 
                            title='Yearly Growth of Transaction Count in India')
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True)   
            
            on = st.toggle("Advanced Insights")

            if on:
                map2 , table2 = st.columns((5,2),gap= 'large')   
                aggregated_data1 = agg_trans.groupby(['Year', 'Quarter'])[['Transaction_amount','Transaction_count']].sum().reset_index()  
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Year'] = aggregated_data1['Year'].astype(str)
                with map2:   
                    st.markdown('#### Box Plot of Quarterly Transaction Count by Year in India')

          
                    fig = px.box(aggregated_data1, x='Year', y='Transaction_count', color='Quarter',
                                title='Box Plot of Quarterly Transaction Count by Year in India',
                                points='all',  
                                hover_data=['Transaction_amount'])

                    st.plotly_chart(fig, use_container_width=True)
                with table2:  
                    distribution_data = aggregated_data1.groupby(['Year', 'Quarter']).agg({
                        'Transaction_count': 'sum'
                    }).reset_index()

                    st.markdown('#### Quarterly Transaction Count Distribution')
                    st.dataframe(distribution_data, use_container_width=True, hide_index=True)   
                    
                            
                aggregated_data_state = agg_trans[agg_trans['Year'] != 2024].groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
                st.markdown('#### Quarterly Transaction Count Distribution by Transaction Count for Each Year')

                years = aggregated_data_state['Year'].unique()

                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_count'], hole=.3)])
                        fig.update_layout(
                            title=f'Transaction Count Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Aggregated Transaction Count for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    aggregated_total = agg_trans.groupby(['Quarter'])['Transaction_count'].sum().reset_index()
                    
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_count'], hole=.3)])
                    fig_total.update_layout(
                        title='Aggregated Transaction Count for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

    #----------------------------------------------       
        if selected_insight == 'Yearly Growth of Insurance Premium amount in India':
            st.markdown('#### Yearly Growth of Insurance Premium Amount in India')
            agg_ins_yearly = agg_ins[agg_ins['Year'] != 2024].groupby('Year')['Transaction_amount'].sum().reset_index()
            agg_ins_yearly['Transaction_amount']=agg_ins_yearly['Transaction_amount'].apply(format_amount)
            fig = px.line(agg_ins_yearly, x='Year', y='Transaction_amount', 
                    labels={'Year': 'Year', 'Transaction_amount': 'Insurance Premium Amount'}, 
                    title='Yearly Growth of Transaction Amount in India')
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
                            
            on = st.toggle("Advanced Insights")

            if on:
                st.markdown("#### Quarterly Distribution of Insurance Premium Amount by Year in India")
                map1 , table1 = st.columns((5,2),gap= 'large')   
                agg_ins_data1 = agg_ins.groupby(['Year', 'Quarter'])[['Transaction_amount','Transaction_count']].sum().reset_index()  
                agg_ins_data1['Transaction_amount']=agg_ins_data1['Transaction_amount'].apply(format_amount)
                agg_ins_data1['Transaction_count']=agg_ins_data1['Transaction_count'].apply(format_number)
                agg_ins_data1['Year'] = agg_ins_data1['Year'].astype(str)
                with map1:   

                    fig = px.box(agg_ins_data1, x='Year', y='Transaction_amount', color='Quarter',
                                title='Box Plot of Quarterly Insurance Premium Amount by Year in India',
                                points='all', 
                                hover_data=['Transaction_count'])

                    st.plotly_chart(fig, use_container_width=True)
                with table1:  
                    distribution_data = agg_ins_data1.groupby(['Year', 'Quarter']).agg({
                        'Transaction_amount': 'sum'
                    }).reset_index()

                    st.markdown('#### Quarterly Insurance Premium Amount Distribution')
                    st.dataframe(distribution_data, use_container_width=True, hide_index=True)

                agg_ins_state = agg_ins[agg_ins['Year'] != 2024].groupby(['Year', 'Quarter'])['Transaction_amount'].sum().reset_index()
                st.markdown('#### Quarterly Transaction Amount Distribution by Insurance Premium Amount for Each Year')

                years = agg_ins_state['Year'].unique()


                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = agg_ins_state[agg_ins_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_amount'], hole=.3)])
                        fig.update_layout(
                            title=f'Premium Amount Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Insurance Premium Amount for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    agg_ins_total = agg_ins.groupby(['Quarter'])['Transaction_amount'].sum().reset_index()
                    
                    fig_total = go.Figure(data=[go.Pie(labels=agg_ins_total['Quarter'], values=agg_ins_total['Transaction_amount'], hole=.3)])
                    fig_total.update_layout(
                        title='Insurance Premium Amount for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    
        
#----------------------------------------------
        if selected_insight == "Yearly Growth of Insurance Premium Count in India":
            st.markdown('#### Yearly Growth of Insurance Premium Count in India')
            agg_ins_data_yearly_count = agg_ins[agg_ins['Year'] != 2024].groupby('Year')['Transaction_count'].sum().reset_index()
            agg_ins_data_yearly_count['Transaction_count']=agg_ins_data_yearly_count['Transaction_count'].apply(format_number)
            fig = px.line(agg_ins_data_yearly_count, x='Year', y='Transaction_count', 
                            labels={'Year': 'Year', 'Transaction_count': 'Insurance Premium Count'}, 
                            title='Yearly Growth of Insurance Premium Count in India')
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True)   
            
            on = st.toggle("Advanced Insights")

            if on:
                map2 , table2 = st.columns((5,2),gap= 'large')   
                aggregated_data1 = agg_ins.groupby(['Year', 'Quarter'])[['Transaction_amount','Transaction_count']].sum().reset_index()  
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Year'] = aggregated_data1['Year'].astype(str)
                with map2:   
                    st.markdown('#### Box Plot of Quarterly Insurance Premium Count by Year in India')


                    fig = px.box(aggregated_data1, x='Year', y='Transaction_count', color='Quarter',
                                title='Box Plot of Quarterly Insurance Premium Count by Year in India',
                                points='all', 
                                hover_data=['Transaction_amount'])

                    st.plotly_chart(fig, use_container_width=True)
                with table2:  
                    distribution_data = aggregated_data1.groupby(['Year', 'Quarter']).agg({
                        'Transaction_count': 'sum'
                    }).reset_index()

                    st.markdown('#### Quarterly Insurance Premium Count Distribution')
                    st.dataframe(distribution_data, use_container_width=True, hide_index=True)
                    

                aggregated_data_state = agg_ins[agg_trans['Year'] != 2024].groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
            
                st.markdown('#### Quarterly Distribution by Insurance Premium Count for Each Year')

                years = aggregated_data_state['Year'].unique()

                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_count'], hole=.3)])
                        fig.update_layout(
                            title=f'Premium Count Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Insurance Premium Count for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:

                    aggregated_total = agg_ins.groupby(['Quarter'])['Transaction_count'].sum().reset_index()

                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_count'], hole=.3)])
                    fig_total.update_layout(
                        title='Insurance Premium Count for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

    #----------------------------------------------         
        if selected_insight == "Yearly Growth of Registered User in India":
            
            st.markdown('#### Yearly Growth of Registered User in India')
            map_user_yearly = map_user[map_user['Year'] != 2024].groupby('Year')['Registered_Users'].sum().reset_index()
            map_user_yearly['Registered_Users']=map_user_yearly['Registered_Users'].apply(format_number)
            fig = px.line(map_user_yearly, x='Year', y='Registered_Users',
                            labels={'Year': 'Year', 'Registered_Users': 'Registered User'}, title='Yearly Growth of Registered User in India')
            fig.update_xaxes(tickmode='array', tickvals=[2020,2021,2022,2023,2024])
            st.plotly_chart(fig, use_container_width=True)
            
            on = st.toggle("Advanced Insights")

            if on:            
                st.markdown('#### Area chart Quarter-wise Growth of Registered User in India ')
                map_data = map_user[map_user['Year'] != 2024].groupby(['Year', 'Quarter'])['Registered_Users'].sum().reset_index()
                fig = px.area(
                    map_data,
                    x='Quarter',
                    y='Registered_Users',
                    color='Year',
                    title="Quarter-wise Growth of Registered User in India",
                    labels={'Quarter': 'Quarter', 'Registered_Users': 'Registered User'},
                    hover_data={'Registered_Users': ':.2f'}
                )
                fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
                fig.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                st.plotly_chart(fig, use_container_width=True)
                
                map_user_state = map_user[map_user['Year'] != 2024].groupby(['Year', 'Quarter'])['Registered_Users'].sum().reset_index()
                st.markdown('#### Quarterly Distribution by Registered User for Each Year')

                years = map_user_state['Year'].unique()

                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = map_user_state[map_user_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Registered_Users'], hole=.3)])
                        fig.update_layout(
                            title=f'Registered User Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Registered User for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    map_user_total = map_user.groupby(['Quarter'])['Registered_Users'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=map_user_total['Quarter'], values=map_user_total['Registered_Users'], hole=.3)])
                    fig_total.update_layout(
                        title='Registered User for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)  
    #---------------------------------
        if selected_insight == "Yearly Growth of App Open in India":
            st.markdown('#### Yearly Growth of App Opens in India')
            map_user_years_appopens = map_user[map_user['Year'] != 2024].groupby('Year')['App_opens'].sum().reset_index()
            map_user_years_appopens['App_opens']=map_user_years_appopens['App_opens'].apply(format_number)
            fig = px.line(map_user_years_appopens, x='Year', y='App_opens', 
                            labels={'Year': 'Year', 'App_opens': 'App Opens'},title='Yearly Growth of App Opens in India')
            fig.update_xaxes(tickmode='array', tickvals=[2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
            on = st.toggle("Advanced Insights")

            if on:            
                st.markdown('#### Area chart Quarter-wise Growth of App Opens in India ')
                map_data = map_user[map_user['Year'] != 2024].groupby(['Year', 'Quarter'])['App_opens'].sum().reset_index()

                fig = px.area(
                    map_data,
                    x='Quarter',
                    y='App_opens',
                    color='Year',
                    title="Quarter-wise Growth of App Opens in India",
                    labels={'Quarter': 'Quarter', 'App_opens': 'App Opens'},
                    hover_data={'App_opens': ':.2f'}
                )
                fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
                fig.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                st.plotly_chart(fig, use_container_width=True)
                
                map_user_state = map_user[map_user['Year'] != 2024].groupby(['Year', 'Quarter'])['App_opens'].sum().reset_index()

                st.markdown('#### Quarterly Distribution by App Opens for Each Year')


                years = map_user_state['Year'].unique()


                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = map_user_state[map_user_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['App_opens'], hole=.3)])
                        fig.update_layout(
                            title=f'App Opens Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### App Opens for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    map_user_total = map_user.groupby(['Quarter'])['App_opens'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=map_user_total['Quarter'], values=map_user_total['App_opens'], hole=.3)])
                    fig_total.update_layout(
                        title='App Opens for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)                            
    #----------------------------------------------  
        if selected_insight == "Transaction Amount by State":
            st.markdown('#### Total Transaction Amount by State in India')
            aggregated_data_state = agg_trans.groupby('State')['Transaction_amount'].sum().reset_index()
            fig = px.bar(aggregated_data_state, x='State', y='Transaction_amount', height=600,
                        title='Transaction Amount by State in India',
                        labels={'Transaction_amount': 'Transaction Amount', 'State': 'State'},
                        color='State', color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True) 
            
    #----------------------------------------------  
        if selected_insight == "Transaction Count by State":    
            st.markdown('#### Total Transaction Count by State in India')
            aggregated_data_state = agg_trans.groupby('State')['Transaction_count'].sum().reset_index()
            fig = px.bar(aggregated_data_state, x='State', y='Transaction_count', 
                        title='Total Transaction Count by State in India',
                        labels={'Transaction_count': 'Transaction Count', 'State': 'State'},
                        color='State', color_discrete_sequence=px.colors.qualitative.Pastel1,height=600)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True)     
    #----------------------------------------------  
        if selected_insight == "Insurance Premium Amount by State":
            st.markdown('#### Total Insurance Premium Amount by State in India')
            aggregated_data_state = agg_ins.groupby('State')['Transaction_amount'].sum().reset_index()
            fig = px.bar(aggregated_data_state, x='State', y='Transaction_amount', height=600,
                        title='Insurance Premium Amount by State in India',
                        labels={'Transaction_amount': 'Insurance Premium Amount', 'State': 'State'},
                        color='State', color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True) 
            
    #----------------------------------------------  
        if selected_insight == "Insurance Premium Count by State":    
            st.markdown('#### Total Insurance Premium Count by State in India')
            aggregated_data_state = agg_ins.groupby('State')['Transaction_count'].sum().reset_index()
            fig = px.bar(aggregated_data_state, x='State', y='Transaction_count', 
                        title='Total Insurance Premium Count by State in India',
                        labels={'Transaction_count': 'Insurance Premium Count', 'State': 'State'},
                        color='State', color_discrete_sequence=px.colors.qualitative.Pastel1,height=600)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True)                            
    #-------------------------------
        if selected_insight == "Registered User by State":
        
            st.markdown('#### Total Registered User Count by State in India')
            map_data_state = map_user.groupby('State')['Registered_Users'].sum().reset_index()
            fig = px.bar(map_data_state, x='State', y='Registered_Users',
                        title='Total Registered User by State in India',
                        labels={'Registered_Users': 'Registered User', 'State': 'State'},
                        color='State', color_discrete_sequence=px.colors.qualitative.Pastel1,height=500)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True) 
    #----------------------------------------------       
        if selected_insight == "App Opens by State":
        
            st.markdown('#### Total App Opens Count by State in India')
            map_data_state = map_user.groupby('State')['App_opens'].sum().reset_index()
            fig = px.bar(map_data_state, x='State', y='App_opens',
                        title='Total App Opens by State in India',
                        labels={'App_opens': 'App Opens', 'State': 'State'},
                        color='State', color_discrete_sequence=px.colors.qualitative.Pastel1,height=500)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True) 
    #----------------------------------------------              
        if selected_insight == "Transaction Count by Brand":
            st.markdown('#### Transaction Count by Brand')
            agg_user_data = agg_user.groupby(['Brand'])['Count'].sum().reset_index()

            fig = px.bar(agg_user_data, x='Brand', y='Count',
                        title='Total Registered User Count by Mobile Brand in India',
                        labels={'Count': 'Registered Users'}, height=600)

            fig.update_layout(barmode='stack', xaxis_title="Brand", yaxis_title="Registered Users")

            fig.update_traces(hovertemplate='Brand: %{x}<br>Registered Users: %{y}<extra></extra>')

            st.plotly_chart(fig, use_container_width=True)              
    #-------------------------------------------------        
        if selected_insight == "State Wise - Brand & Transaction Amounts":
            agg_user_data = agg_user.groupby(['State', 'Brand'])['Count'].sum().reset_index()

            fig = px.bar(agg_user_data, x='Brand', y='Count', color='State',
                        title='Total Registered User Count by Mobile Brand in India',
                        labels={'Count': 'Registered Users', 'State': 'State'},
                        color_discrete_sequence=px.colors.qualitative.Pastel1, height=600)

            fig.update_layout(barmode='stack', legend_title="State", xaxis_title="State", yaxis_title="Registered Users")

            fig.update_traces(showlegend=True, selector=dict(type='bar'))

            fig.update_traces(hovertemplate='State: %{x}<br>Registered Users: %{y}<extra></extra>')

            st.plotly_chart(fig, use_container_width=True)  
    #----------------------------

        if selected_insight == "Transaction Types Analysis by Years and Quarters":
            st.markdown('#### Transaction Type Distribution over years')
            aggregated_data_state = agg_trans.groupby(['Year','Transaction_type'])['Transaction_amount'].sum().reset_index()
            
            st.markdown('#### Transaction Distribution by Year & Transaction Type')

    
            fig = go.Figure()
            aggregated_data_state['Year'] = aggregated_data_state['Year'].astype(str)
   
            years = aggregated_data_state['Year'].unique()
            for year in years:
                df_year = aggregated_data_state[aggregated_data_state['Year'] == year]
                fig.add_trace(go.Bar(
                    x=df_year['Transaction_type'],
                    y=df_year['Transaction_amount'],
                    name=year
                ))

           
            fig.update_layout(barmode='group',
                            title='Transaction Distribution by Quarter & Transaction Type',
                            xaxis_title='Transaction Type',
                            yaxis_title='Transaction Amount',
                            width=900, height=500)

            st.plotly_chart(fig, use_container_width=True)

            aggregated_data_state = agg_trans.groupby(['Quarter','Transaction_type'])['Transaction_amount'].sum().reset_index()
            
            st.markdown('#### Transaction Distribution by Quarter & Transaction Type')

       
            fig = go.Figure()
            aggregated_data_state['Quarter'] = aggregated_data_state['Quarter'].astype(str)

            quarters = aggregated_data_state['Quarter'].unique()
            for quarter in quarters:
                df_quarter = aggregated_data_state[aggregated_data_state['Quarter'] == quarter]
                fig.add_trace(go.Bar(
                    x=df_quarter['Transaction_type'],
                    y=df_quarter['Transaction_amount'],
                    name=quarter
                ))

 
            fig.update_layout(barmode='group',
                            title='Transaction Distribution by Quarter & Transaction Type',
                            xaxis_title='Transaction Type',
                            yaxis_title='Transaction Amount',
                            width=900, height=500)

            st.plotly_chart(fig, use_container_width=True)

            aggregated_data_state = agg_trans.groupby(['Transaction_type'])['Transaction_amount'].sum().reset_index()

            st.markdown('#### Transaction amount to transaction type')


            fig = go.Figure()
            colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
            fig.add_trace(go.Bar(
                x=aggregated_data_state['Transaction_type'],
                y=aggregated_data_state['Transaction_amount'],
                hovertext=aggregated_data_state['Transaction_amount'],
                marker_color=colors,
                name='Transaction Amount'
            ))

      
            fig.update_layout(
                title='Transaction amount to transaction type',
                xaxis_title='Transaction Type',
                yaxis_title='Transaction Amount',
                legend_title='Transaction Type',
                width=900,
                height=500,
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)
#----------------------------------------------                     
        if selected_insight=="Average Transaction Amount by Quarter":
            st.markdown('### Average Transaction Amount by Quarter')
            c1, c2 = st.columns((5,2),gap="large")

            
            with c1:
                avg_trans_amount_data = agg_trans.groupby('Quarter')['Transaction_amount'].mean().reset_index()
                avg_trans_amount_data['Transaction_amount']=avg_trans_amount_data['Transaction_amount'].apply(format_amount)
                fig16 = px.bar(avg_trans_amount_data, x='Quarter', y='Transaction_amount', title='Average Transaction Amount by Quarter')
                st.plotly_chart(fig16)
            with c2:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.dataframe(avg_trans_amount_data, use_container_width=True, hide_index=True)
    #-----------------------------
        if selected_insight == 'Percentage of Transactions by Type':
            st.markdown('### Percentage of Transactions by Type')
            c1, c2 = st.columns((5,2),gap="large")
           
            with c1:
                transaction_type_percentage = agg_trans.groupby('Transaction_type')['Transaction_amount'].sum().reset_index()
                transaction_type_percentage['Percentage'] = (transaction_type_percentage['Transaction_amount'] / transaction_type_percentage['Transaction_amount'].sum()) * 100
                fig20 = px.pie(transaction_type_percentage, names='Transaction_type', values='Percentage', title='Percentage of Transactions by Type')
                st.plotly_chart(fig20)
            with c2:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.dataframe(transaction_type_percentage, use_container_width=True, hide_index=True)
                    

    with tab2:

        col1,c1,c2,c3,c4,c5 = st.columns((1,0.8,1,1,1,1),gap="large")
        with col1:
            states = st.selectbox("#### Select State", options=map_trans["State"].unique())            

        map_user = map_user[map_user['State'] == states] 
        map_trans = map_trans[map_trans['State'] == states]
        map_ins = map_ins[map_ins['State'] == states]
        
        insight_options = [
            f'Yearly Growth of Transaction Amount in {states}',
            f'Yearly Growth of Transaction Count in {states}',
            f'Yearly Growth of Insurance Premium amount in {states}',
            f'Yearly Growth of Insurance Premium Count in {states}',
            f'Yearly Growth of Registered User in {states}',
            f'Yearly Growth of App Open in {states}',
            f'{states} - Transaction Amount by District',
            f'{states} - Transaction Count by District',
            f'{states} - Insurance Premium Amount by District',
            f'{states} - Insurance Premium Count by District',
            f'{states} - Registered User by District',
            f'{states} - App Opens by District',
            f'{states} - Average Transaction Amount by Quarter by District']

        selected_insight = st.selectbox('Select an Insight', insight_options)
#----------------------------------------------       
        if selected_insight == f'Yearly Growth of Transaction Amount in {states}':
            st.markdown(f'#### Yearly Growth of Transaction Amount in {states}')
            aggregated_data_yearly = map_trans[map_trans['Year'] != 2024].groupby('Year')['Transaction_amount'].sum().reset_index()
            aggregated_data_yearly['Transaction_amount']=aggregated_data_yearly['Transaction_amount'].apply(format_amount)
            fig = px.line(aggregated_data_yearly, x='Year', y='Transaction_amount', 
                    labels={'Year': 'Year', 'Transaction_amount': 'Transaction Amount'}, 
                    title=f'Yearly Growth of Transaction Amount in {states}')
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
                            
            on2 = st.toggle("Advanced Insights", key="states_toggle2")

            if on2:
                st.markdown(f"#### Quarterly Distribution of Transaction Amounts by Year in {states}")
                map1 , table1 = st.columns((5,2),gap= 'large')   
                aggregated_data1 = map_trans.groupby(['Year', 'Quarter'])[['Transaction_amount','Transaction_count']].sum().reset_index()  
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Year'] = aggregated_data1['Year'].astype(str)
                with map1:   
                  
                    fig = px.box(aggregated_data1, x='Year', y='Transaction_amount', color='Quarter',
                                title=f'Box Plot of Quarterly Transaction Amount by Year in {states}',
                                points='all', 
                                hover_data=['Transaction_count'])

                    st.plotly_chart(fig, use_container_width=True)
                with table1:  
                    distribution_data = aggregated_data1.groupby(['Year', 'Quarter']).agg({
                        'Transaction_amount': 'sum'
                    }).reset_index()

                    st.markdown('#### Quarterly Transaction Distribution')
                    st.dataframe(distribution_data, use_container_width=True, hide_index=True)    

    
                aggregated_data_state = map_trans[map_trans['Year'] != 2024].groupby(['Year', 'Quarter'])['Transaction_amount'].sum().reset_index()
                
                st.markdown('#### Quarterly Transaction Amount Distribution by Transaction Amount for Each Year')


                years = aggregated_data_state['Year'].unique()

  
                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_amount'], hole=.3)])
                        fig.update_layout(
                            title=f'Transaction Amount Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Aggregated Transaction Amount for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
            
                    aggregated_total = map_trans.groupby(['Quarter'])['Transaction_amount'].sum().reset_index()
            
                    
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_amount'], hole=.3)])
                    fig_total.update_layout(
                        title='Aggregated Transaction Amount for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    
        
#----------------------------------------------                
        if selected_insight == f'Yearly Growth of Transaction Count in {states}':
            st.markdown(f'#### Yearly Growth of Transaction Count in {states}')
            aggregated_data_yearly_count = map_trans[map_trans['Year'] != 2024].groupby('Year')['Transaction_count'].sum().reset_index()
            aggregated_data_yearly_count['Transaction_count']=aggregated_data_yearly_count['Transaction_count'].apply(format_number)
            fig = px.line(aggregated_data_yearly_count, x='Year', y='Transaction_count', 
                            labels={'Year': 'Year', 'Transaction_count': 'Transaction Count'}, 
                            title=f'Yearly Growth of Transaction Count in {states}')
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True)   
            
            on3 = st.toggle("Advanced Insights", key="states_toggle3")

            if on3:
                map2 , table2 = st.columns((5,2),gap= 'large')   
                aggregated_data1 = map_trans.groupby(['Year', 'Quarter'])[['Transaction_amount','Transaction_count']].sum().reset_index()  
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Year'] = aggregated_data1['Year'].astype(str)
                with map2:   
                    st.markdown(f'#### Box Plot of Quarterly Transaction Count by Year in {states}')

              
                    fig = px.box(aggregated_data1, x='Year', y='Transaction_count', color='Quarter',
                                title=f'Box Plot of Quarterly Transaction Count by Year in {states}',
                                points='all', 
                                hover_data=['Transaction_amount'])

                    st.plotly_chart(fig, use_container_width=True)
                with table2:  
                    distribution_data = aggregated_data1.groupby(['Year', 'Quarter']).agg({
                        'Transaction_count': 'sum'
                    }).reset_index()

                    st.markdown('#### Quarterly Transaction Count Distribution')
                    st.dataframe(distribution_data, use_container_width=True, hide_index=True)
                    

                aggregated_data_state = map_trans[map_trans['Year'] != 2024].groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
                
                st.markdown('#### Quarterly Transaction Count Distribution by Transaction Count for Each Year')

      
                years = aggregated_data_state['Year'].unique()

           
                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_count'], hole=.3)])
                        fig.update_layout(
                            title=f'Transaction Count Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Aggregated Transaction Count for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
          
                    aggregated_total = map_trans.groupby(['Quarter'])['Transaction_count'].sum().reset_index()
             
                    
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_count'], hole=.3)])
                    fig_total.update_layout(
                        title='Aggregated Transaction Count for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

    #----------------------------------------------       
        if selected_insight == f'Yearly Growth of Insurance Premium amount in {states}':
            st.markdown(f'#### Yearly Growth of Insurance Premium Amount in {states}')
            map_ins_yearly = map_ins[map_ins['Year'] != 2024].groupby('Year')['Transaction_amount'].sum().reset_index()
            map_ins_yearly['Transaction_amount']=map_ins_yearly['Transaction_amount'].apply(format_amount)
            fig = px.line(map_ins_yearly, x='Year', y='Transaction_amount', 
                    labels={'Year': 'Year', 'Transaction_amount': 'Insurance Premium Amount'}, 
                    title=f'Yearly Growth of Transaction Amount in {states}')
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
                            
            on4 = st.toggle("Advanced Insights",key="states_toggle4")

            if on4:
                st.markdown(f"#### Quarterly Distribution of Insurance Premium Amount by Year in {states}")
                map1 , table1 = st.columns((5,2),gap= 'large')   
                map_ins_data1 = map_ins.groupby(['Year', 'Quarter'])[['Transaction_amount','Transaction_count']].sum().reset_index()  
                map_ins_data1['Transaction_amount']=map_ins_data1['Transaction_amount'].apply(format_amount)
                map_ins_data1['Transaction_count']=map_ins_data1['Transaction_count'].apply(format_number)
                map_ins_data1['Year'] = map_ins_data1['Year'].astype(str)
                with map1:   

                    fig = px.box(map_ins_data1, x='Year', y='Transaction_amount', color='Quarter',
                                title=f'Box Plot of Quarterly Insurance Premium Amount by Year in {states}',
                                points='all',  
                                hover_data=['Transaction_count'])

                    st.plotly_chart(fig, use_container_width=True)
                with table1:  
                    distribution_data = map_ins_data1.groupby(['Year', 'Quarter']).agg({
                        'Transaction_amount': 'sum'
                    }).reset_index()

                    st.markdown('#### Quarterly Insurance Premium Amount Distribution')
                    st.dataframe(distribution_data, use_container_width=True, hide_index=True)  


                map_ins_state = map_ins[map_ins['Year'] != 2024].groupby(['Year', 'Quarter'])['Transaction_amount'].sum().reset_index()

                st.markdown('#### Quarterly Transaction Amount Distribution by Insurance Premium Amount for Each Year')


                years = map_ins_state['Year'].unique()


                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = map_ins_state[map_ins_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_amount'], hole=.3)])
                        fig.update_layout(
                            title=f'Premium Amount Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Insurance Premium Amount for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:

                    map_ins_total = map_ins.groupby(['Quarter'])['Transaction_amount'].sum().reset_index()
                   
                    
                    fig_total = go.Figure(data=[go.Pie(labels=map_ins_total['Quarter'], values=map_ins_total['Transaction_amount'], hole=.3)])
                    fig_total.update_layout(
                        title='Insurance Premium Amount for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    
        
#----------------------------------------------
        if selected_insight == f'Yearly Growth of Insurance Premium Count in {states}':
            st.markdown(f'#### Yearly Growth of Insurance Premium Count in {states}')
            map_ins_data_yearly_count = map_ins[map_ins['Year'] != 2024].groupby('Year')['Transaction_count'].sum().reset_index()
            map_ins_data_yearly_count['Transaction_count']=map_ins_data_yearly_count['Transaction_count'].apply(format_number)
            fig = px.line(map_ins_data_yearly_count, x='Year', y='Transaction_count', 
                            labels={'Year': 'Year', 'Transaction_count': 'Insurance Premium Count'}, 
                            title=f'Yearly Growth of Insurance Premium Count in {states}')
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True)   
            
            on5 = st.toggle("Advanced Insights", key="states_toggle5")

            if on5:
                map2 , table2 = st.columns((5,2),gap= 'large')   
                aggregated_data1 = map_ins.groupby(['Year', 'Quarter'])[['Transaction_amount','Transaction_count']].sum().reset_index()  
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Year'] = aggregated_data1['Year'].astype(str)
                with map2:   
                    st.markdown(f'#### Box Plot of Quarterly Insurance Premium Count by Year in {states}')


                    fig = px.box(aggregated_data1, x='Year', y='Transaction_count', color='Quarter',
                                title=f'Box Plot of Quarterly Insurance Premium Count by Year in {states}',
                                points='all',
                                hover_data=['Transaction_amount'])

                    st.plotly_chart(fig, use_container_width=True)
                with table2:  
                    distribution_data = aggregated_data1.groupby(['Year', 'Quarter']).agg({
                        'Transaction_count': 'sum'
                    }).reset_index()

                    st.markdown('#### Quarterly Insurance Premium Count Distribution')
                    st.dataframe(distribution_data, use_container_width=True, hide_index=True)  
                    

                aggregated_data_state = map_ins[map_ins['Year'] != 2024].groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
              
                st.markdown('#### Quarterly Distribution by Insurance Premium Count for Each Year')


                years = aggregated_data_state['Year'].unique()


                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_count'], hole=.3)])
                        fig.update_layout(
                            title=f'Premium Count Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Insurance Premium Count for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:

                    aggregated_total = map_ins.groupby(['Quarter'])['Transaction_count'].sum().reset_index()

                    
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_count'], hole=.3)])
                    fig_total.update_layout(
                        title='Insurance Premium Count for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

    #----------------------------------------------         
        if selected_insight == f"Yearly Growth of Registered User in {states}":
            
            st.markdown(f'#### Yearly Growth of Registered User in {states}')
            map_user_yearly = map_user[map_user['Year'] != 2024].groupby('Year')['Registered_Users'].sum().reset_index()
            map_user_yearly['Registered_Users']=map_user_yearly['Registered_Users'].apply(format_number)
            fig = px.line(map_user_yearly, x='Year', y='Registered_Users',
                            labels={'Year': 'Year', 'Registered_Users': 'Registered User'}, title=f'Yearly Growth of Registered User in {states}')
            fig.update_xaxes(tickmode='array', tickvals=[2020,2021,2022,2023,2024])
            st.plotly_chart(fig, use_container_width=True)
            
            on6 = st.toggle("Advanced Insights", key="states_toggle6")

            if on6:            
                st.markdown(f'#### Area chart Quarter-wise Growth of Registered User in {states} ')
                map_data = map_user[map_user['Year'] != 2024].groupby(['Year', 'Quarter'])['Registered_Users'].sum().reset_index()

                fig = px.area(
                    map_data,
                    x='Quarter',
                    y='Registered_Users',
                    color='Year',
                    title=f"Quarter-wise Growth of Registered User in {states}",
                    labels={'Quarter': 'Quarter', 'Registered_Users': 'Registered User'},
                    hover_data={'Registered_Users': ':.2f'}
                )
                fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
                fig.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                st.plotly_chart(fig, use_container_width=True)
                
                map_user_state = map_user[map_user['Year'] != 2024].groupby(['Year', 'Quarter'])['Registered_Users'].sum().reset_index()

                st.markdown('#### Quarterly Distribution by Registered User for Each Year')


                years = map_user_state['Year'].unique()


                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = map_user_state[map_user_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Registered_Users'], hole=.3)])
                        fig.update_layout(
                            title=f'Registered User Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Registered User for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    map_user_total = map_user.groupby(['Quarter'])['Registered_Users'].sum().reset_index()

                    fig_total = go.Figure(data=[go.Pie(labels=map_user_total['Quarter'], values=map_user_total['Registered_Users'], hole=.3)])
                    fig_total.update_layout(
                        title='Registered User for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)  
    #---------------------------------
        if selected_insight == f"Yearly Growth of App Open in {states}":
            st.markdown('#### Yearly Growth of App Opens in {states}')
            map_user_years_appopens = map_user[map_user['Year'] != 2024].groupby('Year')['App_opens'].sum().reset_index()
            map_user_years_appopens['App_opens']=map_user_years_appopens['App_opens'].apply(format_number)
            fig = px.line(map_user_years_appopens, x='Year', y='App_opens', 
                            labels={'Year': 'Year', 'App_opens': 'App Opens'},title=f'Yearly Growth of App Opens in {states}')
            fig.update_xaxes(tickmode='array', tickvals=[2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
            on5 = st.toggle("Advanced Insights", key="states_toggle5")

            if on5:            
                st.markdown(f'#### Area chart Quarter-wise Growth of App Opens in {states} ')
                map_data = map_user[map_user['Year'] != 2024].groupby(['Year', 'Quarter'])['App_opens'].sum().reset_index()
                fig = px.area(
                    map_data,
                    x='Quarter',
                    y='App_opens',
                    color='Year',
                    title=f"Quarter-wise Growth of App Opens in {states}",
                    labels={'Quarter': 'Quarter', 'App_opens': 'App Opens'},
                    hover_data={'App_opens': ':.2f'}
                )
                fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
                fig.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                st.plotly_chart(fig, use_container_width=True)
                
                map_user_state = map_user[map_user['Year'] != 2024].groupby(['Year', 'Quarter'])['App_opens'].sum().reset_index()
                st.markdown('#### Quarterly Distribution by App Opens for Each Year')

                years = map_user_state['Year'].unique()

                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = map_user_state[map_user_state['Year'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['App_opens'], hole=.3)])
                        fig.update_layout(
                            title=f'App Opens Distribution for {year} - All Quarters',
                            width=450,
                            height=450,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### App Opens for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    map_user_total = map_user.groupby(['Quarter'])['App_opens'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=map_user_total['Quarter'], values=map_user_total['App_opens'], hole=.3)])
                    fig_total.update_layout(
                        title='App Opens for All Quarters Combined',
                        width=450,
                        height=450,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)                            
    #----------------------------------------------  
        if selected_insight == f'{states} - Transaction Amount by District':
            st.markdown(f'#### Total Transaction Amount by District in {states}')
            aggregated_data_state = map_trans.groupby('User_District')['Transaction_amount'].sum().reset_index()
            fig = px.bar(aggregated_data_state, x='User_District', y='Transaction_amount', height=600,
                        title=f'Transaction Amount by District in {states}',
                        labels={'Transaction_amount': 'Transaction Amount', 'User_District': 'District'},
                        color='User_District', color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True) 
            
    #----------------------------------------------  
        if selected_insight == f'{states} - Transaction Count by District':    
            st.markdown(f'#### Total Transaction Count by District in {states}')
            aggregated_data_state = map_trans.groupby('User_District')['Transaction_count'].sum().reset_index()
            fig = px.bar(aggregated_data_state, x='User_District', y='Transaction_count', 
                        title=f'Total Transaction Count by District in {states}',
                        labels={'Transaction_count': 'Transaction Count', 'User_District': 'District'},
                        color='User_District', color_discrete_sequence=px.colors.qualitative.Pastel1,height=600)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True)     
    #----------------------------------------------  
        if selected_insight == f'{states} - Insurance Premium Amount by District':
            st.markdown(f'#### Total Insurance Premium Amount by District in {states}')
            aggregated_data_state = map_ins.groupby('User_District')['Transaction_amount'].sum().reset_index()
            fig = px.bar(aggregated_data_state, x='User_District', y='Transaction_amount', height=600,
                        title=f'Insurance Premium Amount by District in {states}',
                        labels={'Transaction_amount': 'Insurance Premium Amount', 'User_District': 'District'},
                        color='User_District', color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True) 
            
    #----------------------------------------------  
        if selected_insight ==f'{states} - Insurance Premium Count by District':    
            st.markdown(f'#### Total Insurance Premium Count by District in {states}')
            aggregated_data_state = map_ins.groupby('User_District')['Transaction_count'].sum().reset_index()
            fig = px.bar(aggregated_data_state, x='User_District', y='Transaction_count', 
                        title=f'Total Insurance Premium Count by District in {states}',
                        labels={'Transaction_count': 'Insurance Premium Count', 'User_District': 'District'},
                        color='User_District', color_discrete_sequence=px.colors.qualitative.Pastel1,height=600)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True)                            
    #-------------------------------
        if selected_insight == f'{states} - Registered User by District':
        
            st.markdown(f'#### Total Registered User Count by District in {states}')
            map_data_state = map_user.groupby('User_District')['Registered_Users'].sum().reset_index()
            fig = px.bar(map_data_state, x='User_District', y='Registered_Users',
                        title=f'Total Registered User by District in {states}',
                        labels={'Registered_Users': 'Registered User', 'User_District': 'District'},
                        color='User_District', color_discrete_sequence=px.colors.qualitative.Pastel1,height=500)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True) 
    #----------------------------------------------       
        if selected_insight == f'{states} - App Opens by District':
        
            st.markdown(f'#### Total App Opens Count by District in {states}')
            map_data_state = map_user.groupby('User_District')['App_opens'].sum().reset_index()
            fig = px.bar(map_data_state, x='User_District', y='App_opens',
                        title=f'Total App Opens by District in {states}',
                        labels={'App_opens': 'App Opens', 'User_District': 'District'},
                        color='User_District', color_discrete_sequence=px.colors.qualitative.Pastel1,height=500)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True)  
    #----------------------------
        if selected_insight==f'{states} - Average Transaction Amount by Quarter by District':
            st.markdown(f'### Average Transaction Amount by Quarter in {states}')
            c1, c2 = st.columns((5,2),gap="large")

            
            with c1:
                avg_trans_amount_data = map_trans.groupby('Quarter')['Transaction_amount'].mean().reset_index()
                avg_trans_amount_data['Transaction_amount']=avg_trans_amount_data['Transaction_amount'].apply(format_amount)
                fig16 = px.bar(avg_trans_amount_data, x='Quarter', y='Transaction_amount', title='Average Transaction Amount by Quarter')
                st.plotly_chart(fig16)
            with c2:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.dataframe(avg_trans_amount_data, use_container_width=True, hide_index=True)
