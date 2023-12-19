# import rasterio 
# import pandas as pd
# import pydeck as pdk
# import numpy as np
# import streamlit as st
# from cflp_function import *

############################

# max_capacity = load_data_from_pickle('app_data', 'max_capacity_test.pickle')
# max_capacity
# plant = load_data_from_pickle('app_data', 'Plant_test.pickle')
# plant
# # Plant_all = Plant.insert(0, -1)
# Plant_all = ['All'] + plant.copy()
# Plant_all
# st.write(len(Plant_all))

# @st.cache_data
# def filter_Plant(original_dict, Plant):
#     # Extract key-value pairs where the key is not in the list
#     filtered_dict = {key: value for key, value in original_dict.items() if key in Plant}
#     return filtered_dict

# with st.expander('Select Locations'):
#     with st.form('select_plant'):
#         Plant = st.multiselect(" ", Plant_all)
#         if "All" in Plant:
#             Plant = plant
#         submit = st.form_submit_button("Submit")

# Plant

# st.write(sum(Plant))
# max_capacity = filter_Plant(max_capacity, Plant)
# max_capacity

############################


# available_options = [i for i in range(-1,10)]
# available_options
# if "max_selections" not in st.session_state:
#     st.session_state["max_selections"] = len(Plant_all)

# def options_select():
#     if "selected_options" in st.session_state:
#         if -1 in st.session_state["selected_options"]:
#             st.session_state["selected_options"] = Plant_all[0]
#             st.session_state["max_selections"] = 1
#         else:
#             st.session_state["max_selections"] = len(Plant_all)

# selected_plants = st.multiselect(
#     label="Select an option",
#     options=Plant_all,
#     key='selected_options',
#     max_selections=st.session_state["max_selections"],
#     on_change=options_select,
#     format_func=lambda x: "All" if x == -1 else f"Location {x}")

# st.write(
#     Plant_all[1:] if st.session_state["max_selections"] == 1 
#     else st.session_state["selected_options"])


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