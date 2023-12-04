import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np

padding = 0

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .small-font {
        font-size:12px;
        font-style: italic;
        color: #b1a7a6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

view_state = pdk.ViewState(longitude=6.747489560596507, latitude=52.316862707395394, zoom=8, bearing=0, pitch=0)

### LOAD DATA ##################################
@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

d_to_farm = load_data('./hex/d_to_farm_hex.csv')
d_to_road = load_data('./hex/d_to_road_hex.csv')
fake = load_data("./hex/fake_hex.csv")

### FUZZY ANALYSIS ##################################
@st.cache_data
def fuzzify(df):
    df_array = np.array(df['Value'])
    fuzzified_array = np.maximum(0, 1 - (df_array - df_array.min()) / (df_array.max() - df_array.min()))
    return fuzzified_array

fuzzy_farm = fuzzify(d_to_farm)
fuzzy_road = fuzzify(d_to_road)
fuzzy_fake = fuzzify(fake)

### CREATE STREAMLIT ##################################
st.title("Suitability Criteria for Selecting Digester Sites")

col1, col2 = st.columns(2)
# Plot Map 1
with col1:
    st.header("Map 1")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view_state,
        layers=[
            pdk.Layer(
                "H3HexagonLayer",
                d_to_farm,
                pickable=True,
                stroked=True,
                filled=True,
                extruded=False,
                opacity=0.7,
                get_hexagon="hex9",
                get_fill_color ='[255, 255, 255]', 
                get_line_color=[255, 255, 255],
                line_width_min_pixels=2
            ),
        ],
        tooltip={"text": "Distance to farm: {Value}"}
    ), use_container_width=True)

# Plot Map 2
with col2:
    st.header("Map 2")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view_state,
        layers=[
            pdk.Layer(
                "H3HexagonLayer",
                d_to_road,
                pickable=True,
                stroked=True,
                filled=True,
                extruded=False,
                opacity=0.7,
                get_hexagon="hex9",
                get_fill_color ='[255, 255, 255]', 
                get_line_color=[255, 255, 255],
                line_width_min_pixels=2
            ),
        ],
        tooltip={"text": "Distance to road: {Value}"}
    ), use_container_width=True)

# Create a form in the main content area
with st.sidebar.form(key="suitability_analysis_form"):
    # Allow users to select variables
    selected_variables = st.sidebar.multiselect("Select suitability criteria", ['fuzzy_farm', 'fuzzy_road', 'fuzzy_fake'])

    # Add other form elements as needed
    submit = st.form_submit_button(label="Build Suitability Map")

# if submit


# # import sys
# import leafmap.foliumap as leafmap

# # sys.path

# raster_file = '/Users/wenyuc/Desktop/UT/data/raster/fuzzy_complete_3857.tif'

# m = leafmap.Map()
# m.add_basemap()
# m.add_raster(raster_file, cmap="viridis", layer_name="Raster Layer")

# m.to_streamlit()

