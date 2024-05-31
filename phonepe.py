import streamlit as st
import base64
from exploredata import app as exploredata_app
from statedata import app as statedata_app
from datainsight import app as datainsight_app
from geoview import app as geoview_app
import plotly.io as pio
from streamlit_option_menu import option_menu
import cryptography
# Clear the cache
pio.templates.default = None

# Page configuration
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    page_icon="asset/web_logo.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>

.image-container {
    text-align: left;  
    padding: 20px 0;
}
.image-container img {
    height: 20%;
    width: 100%; 
}
[data-testid="stSidebar"] 
{
    background-color: white; 
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
image_path = "asset/PAGE_LOGO.svg"

# Function to load and encode the image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Get the base64 encoded image
image_base64 = get_image_base64(image_path)

# Render the HTML content
st.markdown(f'<div class="image-container"><img src="data:image/svg+xml;base64,{image_base64}" /></div>', unsafe_allow_html=True)



with st.sidebar:
    st.write("")
    st.write("")
    selected = option_menu(
        menu_title="Dashboard",
        options=["Explore Data", "State-Wise Data", "Data Insights","Geo View"],
        icons=["bar-chart-line", "bar-chart-line", "bar-chart-line","globe"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
                    "container": {"padding": "5!important","background-color":"#230B43"},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#391C59"},
                    "nav-link-selected": {"background-color": "#391C59"},}
                
                )
    
if selected == "Explore Data":
    exploredata_app()  
    
if selected == "State-Wise Data":
    statedata_app() 
    
if selected == "Data Insights":
    datainsight_app() 
        
if selected == "Geo View":
    geoview_app() 

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.markdown("***")
st.write("Created by **Akshaya Muralidharan**")