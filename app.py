from cflp_function import *
import streamlit as st
# import folium
# from streamlit_folium import st_folium
from pulp import *
import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import geopandas as gpd
import pydeck as pdk
import random
import rasterio
from rasterio.plot import reshape_as_image


# import os
# print("Current working directory: ", os.getcwd())

st.title('BIOZE Digital Mapping Tool')
st.text('This is an interactive mapping tool on biogas.')
# st.set_page_config(layout="wide")


# Load files and create parameters
folder_path = 'app_data'
    # List
        # set F     set of farm locations (list)
Farm = load_data_from_pickle(folder_path, 'Farm.pickle')
        # set P     set of potential digester locations
Plant = load_data_from_pickle(folder_path, 'Plant.pickle')
    # Dictionary 
        # p_i       manure production of each i
manure_production = load_data_from_pickle(folder_path, 'manure_production.pickle')
        # q_j       max capacity of each j 
max_capacity = load_data_from_pickle(folder_path, 'max_capacity.pickle')
        # f_j       fixed cost of establishing each j
fixed_cost = load_data_from_pickle(folder_path, 'fixed_cost.pickle')        
        # C_ij      transportation matrix 
transport_cost = load_data_from_pickle(folder_path, 'transportation_cost.pickle')
    # Float
        # alpha     total manure production
total_manure = load_data_from_pickle(folder_path, 'total_manure.pickle')
    # Float defined here
        # mu        manure utilization target 

potential_digester_location = pd.read_csv(r'./farm_cluster_mock_5.csv')
farm = pd.read_csv(r"./farm_mock.csv")

# Define manure use goal (mu)
target = (st.slider('Choose manure use percentage', 
                   min_value=0, max_value=100, step=10))/ 100

# farm_gdf = gpd.read_file(r"./farm_new.shp")

# # Extract latitude and longitude from the 'geometry' column
# farm_gdf['latitude'] = farm_gdf['geometry'].y
# farm_gdf['longitude'] = farm_gdf['geometry'].x

# Run the model 
total_cost, total_fixed_cost, total_transport_cost, assignment_decision, use_plant_index = cflp(Plant, 
                                                                                                Farm, 
                                                                                                fixed_cost, 
                                                                                                transport_cost, 
                                                                                                manure_production, 
                                                                                                max_capacity, 
                                                                                                target, total_manure)

# # Load raster data
# with rasterio.open('./raster/fuzzy_and_complete_1.tif') as src:
#     raster_data = src.read()

# # Reshape raster data for Pydeck
# raster_image = reshape_as_image(raster_data)

# # Create a Pydeck layer for the raster data
# fuzzy_layer = pdk.Layer(
#     "BitmapLayer",
#     data={"image": raster_image},
#     opacity=0.7,
#     get_position=[0, 0],
#     image_size=20,
#     bounds=[src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top],
# )

arc_layer_df = get_arc(assignment_decision, potential_digester_location, farm)
color_mapping = {label: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for label in assignment_decision.keys()}
digester_df, assigned_farms_df, unassigned_farms_df = get_plot_variables(assignment_decision, potential_digester_location, farm, color_mapping)

# Create a Pydeck layer for digesters
digesters_layer = pdk.Layer(
    type='ScatterplotLayer',
    data=digester_df,
    get_position=['x', 'y'],
    get_radius=800,
    get_fill_color='color',
    pickable=True,
    auto_highlight=True
)

# Create a Pydeck layer for assigned farms
assigned_farms_layer = pdk.Layer(
    type='ScatterplotLayer',
    data=assigned_farms_df,
    get_position=['x', 'y'],
    get_radius=300,
    get_fill_color='color',
    pickable=True,
    auto_highlight=True
)

# Create a Pydeck layer for unassigned farms
unassigned_farms_layer = pdk.Layer(
    type='ScatterplotLayer',
    data=unassigned_farms_df,
    get_position=['x', 'y'],
    get_radius=300,
    get_fill_color=[128, 128, 128],
    pickable=True,
    auto_highlight=True
)

# Create ArcLayer
arc_layer = pdk.Layer(
    'ArcLayer',
    data=arc_layer_df,
    get_width=2,          # Width of the arcs
    get_source_position=['start_lon', 'start_lat'],
    get_target_position=['end_lon', 'end_lat'],
    get_source_color=[0, 255, 0, 160],   # RGBA color of the starting points
    get_target_color=[255, 0, 0, 160],   # RGBA color of the ending points
    pickable=True,
    auto_highlight=True
)



# # Create the Deck
# st.pydeck_chart(pdk.Deck(layers=[raster_layer], initial_view_state=view_state))

# Inject custom CSS to make the map full screen
st.markdown(
    """
    <style>
    #root .block-container {
        max-width: none;
        padding-left: 0;
        padding-right: 0;
    }
    .stFrame {
        width: 100vw !important;
        height: 100vh !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# # Define your map view
# view_state = pdk.ViewState(
#     latitude=potential_digester_location['y'].mean(),
#     longitude=potential_digester_location['x'].mean(), # Center of the raster bounds
#     zoom=8,
# )


# # Create the deck
# view_state = pdk.ViewState(latitude=37.7749, longitude=-122.4194, zoom=10)
# deck = pdk.Deck(layers=[arc_layer, point_layer], initial_view_state=view_state)

view_state=pdk.ViewState(
        latitude=potential_digester_location['y'].mean(),
        longitude=potential_digester_location['x'].mean(),
        zoom=9,
        pitch=0
    )

deck = pdk.Deck(layers=[digesters_layer, assigned_farms_layer, unassigned_farms_layer, arc_layer],
                initial_view_state=view_state, 
                 tooltip={
        'html': '<b>Farm:</b> {farm_number}<br/><b>Digester:</b> {digester_number}<br/><b>Quantity:</b> {material_quantity}t',
        'style': {
            'color': 'white'
        }
    })

# Streamlit checkbox for toggling the visibility of the ArcLayer
show_arcs = st.checkbox('Show assignment of farms to digesters', value=True)

# Toggle the visibility of the ArcLayer based on the checkbox
deck.layers[3].visible = show_arcs

# Rendering the map 
st.pydeck_chart(deck, use_container_width=True)

# Update the map when the checkbox is toggled
# if not show_arcs:
#     updated_deck = pdk.Deck(layers=[digesters_layer, assigned_farms_layer, unassigned_farms_layer], initial_view_state=view_state)
#     st.pydeck_chart(updated_deck)
# else:
#     st.pydeck_chart(deck)

# center_map_coords = [52.40659843013704, 6.485187055207251]
# map = folium.Map(location=center_map_coords, zoom_start=9, tiles='OpenStreetMap')

# for lat, long in zip(farm.y, farm.x):
#     folium.Marker(
#         location=[lat, long], 
#         icon=folium.Icon(icon_color='white')
#     ).add_to(map)
# st_folium(map)

# Display the plot using st.pyplot()
# st.pyplot(plt.gcf()) # get current figure, explicitly providing the current figure to Streamlit, 
                        # which avoids using Matplotlib's global figure object directly. 

# st.map(farm_gdf)



# filename = f"./outputs/cflp_v{6}_{int(target*100)}%manure.png"  # You can choose the file extension (e.g., .png, .jpg, .pdf)
# plot_result(Plant, 
#             potential_digester_location, 
#             assignment_decision, farm, Farm, use_plant_index, target, total_cost, filename, save_fig=False)
