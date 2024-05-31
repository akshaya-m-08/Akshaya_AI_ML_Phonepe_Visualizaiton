def app():
    import streamlit as st
    import json
    import folium
    from folium import  GeoJson, GeoJsonPopup
    from r3_fetchsql import agg_trans
    
    agg_trans['State'] = agg_trans['State'].str.replace('-', ' ').str.title()
    
    with open('json/modified_geojson_file.geojson') as f:
        modified_geojson_file = json.load(f)
    
    def folium_map(input_df, geojson_data, id_column, value_column):
    
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=6)
        
        choropleth = folium.Choropleth(
            geo_data=geojson_data,
            data=input_df,
            columns=[id_column, value_column],
            key_on='feature.properties.st_nm',
            fill_color='PuRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Transaction Amount'
        ).add_to(m)


        GeoJson(
            geojson_data,
            name='States',
            popup=GeoJsonPopup(
                fields=[id_column, value_column],
                aliases=['State', 'Transaction Amount']
            )
        ).add_to(m)
        
        choropleth.add_to(m)

        
        folium.LayerControl(collapsed=False).add_to(m)
        return m

    st.markdown("<h1 style='text-align: center; font-size: 40px'> Geographical View", unsafe_allow_html=True)
    
    col1, col2, col3,col4,col5,col6 = st.columns((2, 2,1,1,1,1), gap='large')
    with col1:
        years = st.selectbox("#### Select Year", options=agg_trans["Year"].unique())
        
    with col2:
        quarters = st.selectbox("#### Select Quarter", options=agg_trans["Quarter"].unique())
    
    trans_selected_year = agg_trans[(agg_trans['Year'] == years) & 
                                (agg_trans['Quarter'] == quarters)]
    
    trans_selected_year = trans_selected_year.groupby('State').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)

    trans_selected_year = trans_selected_year.rename(columns={'State': 'st_nm','Transaction_amount' : 'transaction_amount'})

    choropleth_map = folium_map(trans_selected_year, modified_geojson_file, 'st_nm', 'transaction_amount') 

    # Convert Folium map to HTML
    choropleth_map.save("choropleth_map.html")

    with open("choropleth_map.html", "r") as f:
        html = f.read()
    st.components.v1.html(html, width=2000, height=1900)
        

