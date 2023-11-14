from cflp_function import *
import streamlit as st
import folium
from streamlit_folium import st_folium
from pulp import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# import os
# print("Current working directory: ", os.getcwd())

# st.set_page_config(layout="wide")

st.title('BIOZE Digital Mapping Tool')
st.text('This is an interactive mapping tool on biogas.')

# slider = st.slider('Choose manure use percentage', 
#                    min_value=0, max_value=100, step=10)

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


# Run the model 
total_cost, total_fixed_cost, total_transport_cost, assignment_decision, use_plant_index = cflp(Plant, 
                                                                                                Farm, 
                                                                                                fixed_cost, 
                                                                                                transport_cost, 
                                                                                                manure_production, 
                                                                                                max_capacity, 
                                                                                                target, total_manure)


filename = f"./outputs/cflp_v{6}_{int(target*100)}%manure.png"  # You can choose the file extension (e.g., .png, .jpg, .pdf)
plot_result(Plant, 
            potential_digester_location, 
            assignment_decision, farm, Farm, use_plant_index, target, total_cost, filename, save_fig=False)




# center_map_coords = [52.40659843013704, 6.485187055207251]
# map = folium.Map(location=center_map_coords, zoom_start=9, tiles='OpenStreetMap')

# for lat, long in zip(farm.y, farm.x):
#     folium.Marker(
#         location=[lat, long], 
#         icon=folium.Icon(icon_color='white')
#     ).add_to(map)
# st_folium(map)

# Display the plot using st.pyplot()
st.pyplot(plt.gcf()) # get current figure, explicitly providing the current figure to Streamlit, 
                        # which avoids using Matplotlib's global figure object directly. 