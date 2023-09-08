import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

from plots import MyPlots

st.set_page_config(layout="wide")

# Unpack CSS styling
with open("style-dist.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

with open("fonts.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Read Excel file
data_path = "my_test_data.xlsx"
@st.cache_data
def get_data(data_path) -> pd.DataFrame:
    return pd.read_excel(data_path, index_col=0)

data = get_data(data_path)


# SIDEBAR
st.sidebar.header('Dashboard control filters')

# Provider
st.sidebar.subheader('Choose Provider')
provider_filter = st.sidebar.multiselect(label='Provider', 
                                         options=data['provider'].unique(), 
                                         default=data['provider'].unique(),
                                         key='_provider') 

# Income Group
st.sidebar.subheader('Choose Income Group')
income_filter = st.sidebar.multiselect(label='Income Group', 
                                       options=data['income_groups'].unique(), 
                                       default=data['income_groups'].unique(),
                                       key='_income')

# Gender
st.sidebar.subheader('Choose Gender')
gender_filter = st.sidebar.multiselect(label='Select from given genders', 
                                       options=data['gender'].unique(), 
                                       default=data['gender'].unique(),
                                       key='_gender')

st.sidebar.subheader('Credit Score')
slider_filter = st.sidebar.slider(
                    label='Select Credit Score Interval',
                    min_value=0.0,
                    max_value=1.0,
                    value=[0.0, 1.0],
                    step=0.1,
                    )

df = data[(data['provider'].isin(provider_filter)) &
          (data['income_groups'].isin(income_filter)) &
          (data['gender'].isin(gender_filter))&
          (data['score']>=slider_filter[0])&
          (data['score']<=slider_filter[1])]

my_plots = MyPlots(df)


# TOP
with st.container():
    st.markdown("<div class='logo-wrapper' style='position:absolute;top:0;right:0;max-width:400px;width:100%;z-index:10'></div>", unsafe_allow_html = True)

    st.plotly_chart(my_plots.products_pie(), use_container_width=True)

col1, col2 = st.columns([1, 4])

# COL1
# Metrics
visitors = df['user'].sum()
avg_call_duration = round(df['calls_duration'].mean(), ndigits=1)
locations_visited = df['location'].sum()
transactions_done = df['transactions_done'].sum()
avg_gb_spend = round(df['internet_traffic_gb'].mean(), ndigits=1)
goal_conversion = (visitors/data['user'].sum())*100

col1.metric(label="visitors",          value=f"{visitors}")
col1.metric(label="avg call duration", value=f"{avg_call_duration}m")
col1.metric(label="locations visited", value=f"{locations_visited}")
col1.metric(label="transactions done", value=f"{transactions_done}")
col1.metric(label="avg GB spend",      value=f"{avg_gb_spend}Gb")
col1.metric(label="chosen proportion", value=f"{goal_conversion}%")

config = {'displayModeBar': False, 'displaylogo': False, 'showLink':False}

with col2.container():
    col3, col4 = st.columns([2, 2])
    # Top Left
    col3.plotly_chart(my_plots.providers_donut_chart(), use_container_width=True, **config)
    # Top Right
    col4.plotly_chart(my_plots.gender_age_histo(), use_container_width=True)
    # Bottom Left
    col3.plotly_chart(my_plots.income_hist(), use_container_width=True)
    # Bottom Right
    col4.plotly_chart(my_plots.score_v_hist(), use_container_width=True)
    
    
    
if st.button("Give a Loan"):
    # TODO make it GIF instead of .mp4
    if "Beeline" in provider_filter:
        st.write("You chose Beeline")
        
        user_input_gif = st.expander("Verification")
        # user_input_gif.image(Image.open("gifs/verification.gif"), caption="Optional caption", use_column_width=True)
        user_input_gif.image("gifs/verification.gif", caption="User Verification", use_column_width=True)
            
        scoring_gif = st.expander("Scoring")
        # scoring_gif.image(Image.open("gifs/scoring.gif"), caption="Optional caption", use_column_width=True)
        # scoring_gif.markdown("![Alt Text](https://github.com/DSU-VEON/dashboard/blob/main/scoring.gif?raw=true)")
        scoring_gif.markdown('<img src="https://github.com/DSU-VEON/dashboard/blob/main/scoring.gif?raw=true" alt="Alt Text" width=1200 height=800>', unsafe_allow_html=True)
        

            
        income_gif = st.expander("Income")
        # income_gif.markdown("![Alt Text](https://github.com/DSU-VEON/dashboard/blob/main/income.gif?raw=true)")
        income_gif.markdown('<img src="https://github.com/DSU-VEON/dashboard/blob/main/income.gif?raw=true" alt="Alt Text" width=1200 height=800>', unsafe_allow_html=True)


        location_expander = st.expander("Roaming")
        location_expander.markdown("### Changing Place of Living")
        location_expander.plotly_chart(my_plots.wkt_polygon(), use_container_width=True)
                
        location_expander.plotly_chart(my_plots.roaming_plot(version="Scattermapbox"), use_container_width=True)
        location_expander.markdown("### Roaming Country: USA")
    
    else:
        st.write("You chose other provider(s)")
        user_input_gif = st.expander("Expand to Input User Data")
        user_input_gif.image("gifs/verification.gif", caption="User Verification", use_column_width=True)

# if st.button("Test Gif"):
    
#     # user_input_gif = st.expander("Verification")
#     st.image("gifs/income.gif", caption="Income", use_column_width=True)
