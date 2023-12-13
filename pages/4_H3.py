import pandas as pd
import pydeck as pdk
import streamlit as st


st.set_page_config(layout="wide")

color_scale = [
    [0, 255, 0, 255],  # RGB color for value 0 (green)
    [255, 0, 0, 255]   # RGB color for value 1 (red)
]

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

df_7 = load_data('./hex/df_hex_7.csv')
df_8 = load_data('./hex/df_hex_8.csv')
df_9 = load_data('./hex/df_hex_9.csv')
df_10 = load_data('./hex/d_to_farm_hex_complete.csv')

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
    # get_line_color=[255, 255, 255],
    line_width_min_pixels=2)

hex_9 = pdk.Layer(
    "H3HexagonLayer",
    df_10,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    opacity=0.7,
    get_hexagon="h3",
    get_fill_color = [255, 255, 255], #'[255 * Value, 255 * (1 - Value), 0, 255]', 
    get_line_color=[255, 255, 255],
    line_width_min_pixels=2)

# Set the viewport location
# view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=14, bearing=0, pitch=30)
view_state = pdk.ViewState(longitude=df_7['lng'].mean(), latitude=df_7['lat'].mean(), zoom=8, bearing=0, pitch=0)

# Render
deck = pdk.Deck(layers=[hex_7, hex_8, hex_9], initial_view_state=view_state, tooltip={"text": "Suitability: {Value}"})

deck.layers[0].visible = show_7
deck.layers[1].visible = show_8
deck.layers[2].visible = show_9

st.pydeck_chart(deck, use_container_width=True)