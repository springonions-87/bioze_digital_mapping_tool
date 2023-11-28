# import pandas as pd
# import pydeck as pdk
# import numpy as np
# import streamlit as st


# color_scale = [
#     [0, 255, 0, 255],  # RGB color for value 0 (green)
#     [255, 0, 0, 255]   # RGB color for value 1 (red)
# ]

# @st.cache_data

# def load_data(csv_path):
#     df = pd.read_csv(csv_path)
#     return df

# df = load_data('./df_hex_9.csv')

# # Define a layer to display on a map
# layer = pdk.Layer(
#     "H3HexagonLayer",
#     df,
#     pickable=True,
#     stroked=True,
#     filled=True,
#     extruded=False,
#     opacity=0.7,
#     get_hexagon="hex9",
#     get_fill_color ='[255 * Value, 255 * (1 - Value), 0, 255]', 
#     get_line_color=[255, 255, 255],
#     line_width_min_pixels=2)

# # Set the viewport location
# # view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=14, bearing=0, pitch=30)
# view_state = pdk.ViewState(longitude=df['lng'].mean(), latitude=df['lat'].mean(), zoom=10, bearing=0, pitch=0)


# # Render
# r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "Suitability: {Value}"})

# st.pydeck_chart(r, use_container_width=True)