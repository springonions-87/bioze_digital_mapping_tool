import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(layout="wide")


# Add a subtitle for the checkboxes
st.sidebar.markdown("### Hexagon Resolution")
# Streamlit checkbox for toggling the visibility of the ArcLayer
show_7 = st.sidebar.checkbox('7', value=True)
show_8 = st.sidebar.checkbox('8', value=False)
show_9 = st.sidebar.checkbox('9', value=False)

@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

d_to_farm = load_data('./hex/d_to_farm_hex.csv')
d_to_road = load_data('./hex/d_to_road_hex.csv')

# Define a layer to display on a map
hex_7 = pdk.Layer(
    "H3HexagonLayer",
    df_7,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    opacity=0.7,
    get_hexagon="hex7",
    get_fill_color ='[255 * Value, 255 * (1 - Value), 0, 255]', 
    get_line_color=[255, 255, 255],
    line_width_min_pixels=2)

hex_8 = pdk.Layer(
    "H3HexagonLayer",
    df_8,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    opacity=0.7,
    get_hexagon="hex8",
    get_fill_color ='[255 * Value, 255 * (1 - Value), 0, 255]', 
    get_line_color=[255, 255, 255],
    line_width_min_pixels=2)


# Set the viewport location
# view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=14, bearing=0, pitch=30)
view_state = pdk.ViewState(longitude=6.747489560596507, latitude=52.316862707395394, zoom=8, bearing=0, pitch=0)

# Render
deck = pdk.Deck(layers=[hex_7, hex_8, hex_9], initial_view_state=view_state, tooltip={"text": "Suitability: {Value}"})

deck.layers[0].visible = show_7
deck.layers[1].visible = show_8
deck.layers[2].visible = show_9

st.pydeck_chart(deck, use_container_width=True)


import streamlit as st
import pydeck as pdk

# Example data for Map 1
data_map1 = ...

# Example data for Map 2
data_map2 = ...

# # Create a Streamlit app
# st.title("Two Maps Side by Side")

# Create two columns for the maps
col1, col2 = st.columns(2)

# Plot Map 1
with col1:
    st.header("Map 1")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=37.7749,
            longitude=-122.4194,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=data_map1,
                get_position="[lon, lat]",
                get_radius=100,
                get_color="[200, 30, 0, 160]",
                pickable=True,
            ),
        ],
    ))

# Plot Map 2
with col2:
    st.header("Map 2")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=37.7749,
            longitude=-122.4194,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=data_map2,
                get_position="[lon, lat]",
                get_radius=100,
                get_color="[0, 30, 200, 160]",
                pickable=True,
            ),
        ],
    ))


# # import sys
# import leafmap.foliumap as leafmap

# # sys.path

# raster_file = '/Users/wenyuc/Desktop/UT/data/raster/fuzzy_complete_3857.tif'

# m = leafmap.Map()
# m.add_basemap()
# m.add_raster(raster_file, cmap="viridis", layer_name="Raster Layer")

# m.to_streamlit()

