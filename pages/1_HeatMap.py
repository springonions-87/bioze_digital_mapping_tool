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

# # Set the view
# view_state = pdk.ViewState(
#     longitude=df['Longitude'].mean(),
#     latitude=df['Latitude'].mean(),
#     zoom=10,
#     pitch=0)

# layer = pdk.Layer(
#     "HeatmapLayer",
#     data=df,
#     opacity=0.4,
#     get_position=["Longitude", "Latitude"],
#     aggregation=pdk.types.String("MEAN"),
#     get_weight="Value",
#     pickable=True)

# r = pdk.Deck(
#     layers=[layer],
#     initial_view_state=view_state, 
#     tooltip = {
#         "html": "<b>Suitability:</b> {Value}",
#         "style": {
#                 "backgroundColor": "steelblue",
#                 "color": "white"
#         }}
# )

# # Rendering the map 
# st.pydeck_chart(r, use_container_width=True)