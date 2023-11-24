# import rasterio 
# import pandas as pd
# import pydeck as pdk
# import numpy as np
# import streamlit as st

# raster_file = '/Users/wenyuc/Desktop/UT/data/raster/fuzzy_4326.tif'

# @st.cache_data
# def load_raster(raster_file):
#     with rasterio.open(raster_file) as src:
#         band1 = src.read(1)
#         # print('Band1 has shape', band1.shape)
#         height = band1.shape[0]
#         width = band1.shape[1]
#         cols, rows = np.meshgrid(np.arange(width), np.arange(height))
#         xs, ys = rasterio.transform.xy(src.transform, rows, cols)
#         lons= np.array(xs)
#         lats = np.array(ys)
#         # print('lons shape', lons.shape)
#     df = pd.DataFrame({
#         'Latitude': lats.flatten(),
#         'Longitude': lons.flatten(),
#         'Value': band1.flatten()})
#     # Optionally, you can filter out no-data values
#     df = df[df['Value'] != src.nodatavals[0]]
#     return (df)

# df = load_raster(raster_file)

# # Define a layer to display on a map
# layer = pdk.Layer(
#     "ScreenGridLayer",
#     df,
#     pickable=False,
#     opacity=0.7,
#     cell_size_pixels=15,
#     color_range=[
#         [0, 25, 0, 25],
#         [0, 85, 0, 85],
#         [0, 127, 0, 127],
#         [0, 170, 0, 170],
#         [0, 190, 0, 190],
#         [0, 255, 0, 255],
#     ],
#     get_position=["Longitude", "Latitude"],
#     get_weight="Value",
# )
# # Set the viewport location
# view_state = pdk.ViewState(longitude=df['Longitude'].mean(), latitude=df['Latitude'].mean(), zoom=10, bearing=0, pitch=0)

# # Render
# r = pdk.Deck(layers=[layer], initial_view_state=view_state,
#              tooltip={
#             'html': '<b>Value:</b> {Value}',
#             'style': {
#             'color': 'white'}})

# st.pydeck_chart(r, use_container_width=True)