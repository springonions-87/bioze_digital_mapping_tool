import streamlit as st
import pandas as pd
import pydeck as pdk
import random
import rasterio
from pulp import *
from cflp_function import *

# import os
# print("Current working directory: ", os.getcwd())

# st.title('BIOZE Digital Mapping Tool')
# st.text('This is an interactive mapping tool on biogas.')
# st.set_page_config(layout="wide")


# # Load files and create parameters
# folder_path = 'app_data'
#     # List
#         # set F     set of farm locations (list)
# Farm = load_data_from_pickle(folder_path, 'Farm_test.pickle')
#         # set P     set of potential digester locations
# Plant = load_data_from_pickle(folder_path, 'Plant_test.pickle')
#     # Dictionary 
#         # p_i       manure production of each i
# manure_production = load_data_from_pickle(folder_path, 'manure_production_test.pickle')
#         # q_j       max capacity of each j 
# max_capacity = load_data_from_pickle(folder_path, 'max_capacity_test.pickle')
#         # f_j       fixed cost of establishing each j
# fixed_cost = load_data_from_pickle(folder_path, 'fixed_cost_test.pickle')        
#         # C_ij      transportation matrix 
# transport_cost = load_data_from_pickle(folder_path, 'transportation_cost_test.pickle')
#     # Float
#         # alpha     total manure production
# total_manure = load_data_from_pickle(folder_path, 'total_manure_test.pickle')
#     # Float defined here
#         # mu        manure utilization target 

# potential_digester_location = pd.read_csv(r'./farm_cluster_mock_5.csv')
# farm = pd.read_csv(r"./farm_mock.csv")

@st.cache_data
def load_data():
    folder_path = 'app_data'

    # List
    # set F     set of farm locations (list)
    Farm = load_data_from_pickle(folder_path, 'Farm_test.pickle')
    # set P     set of potential digester locations
    Plant = load_data_from_pickle(folder_path, 'Plant_test.pickle')

    # Dictionary 
    # p_i       manure production of each i
    manure_production = load_data_from_pickle(folder_path, 'manure_production_test.pickle')
    # q_j       max capacity of each j 
    max_capacity = load_data_from_pickle(folder_path, 'max_capacity_test.pickle')
    # f_j       fixed cost of establishing each j
    fixed_cost = load_data_from_pickle(folder_path, 'fixed_cost_test.pickle')        
    # C_ij      transportation matrix 
    transport_cost = load_data_from_pickle(folder_path, 'transportation_cost_test.pickle')

    # Float
    # alpha     total manure production
    total_manure = load_data_from_pickle(folder_path, 'total_manure_test.pickle')
    
    # DataFrame
    potential_digester_location = pd.read_csv(r'./farm_cluster_mock_5.csv')
    farm = pd.read_csv(r"./farm_mock.csv")

    return Farm, Plant, manure_production, max_capacity, fixed_cost, transport_cost, total_manure, potential_digester_location, farm
    
Farm, Plant, manure_production, max_capacity, fixed_cost, transport_cost, total_manure, potential_digester_location, farm = load_data()

# Add a title to the sidebar
st.sidebar.title("BIOZE Digital Mapping Tool")
# Define manure use goal (mu)
target = (st.sidebar.slider('Select a manure utilization target (%):', 
                   min_value=0, max_value=100,step=10)/ 100)

# Run the model 
total_cost, total_fixed_cost, total_transport_cost, assignment_decision, use_plant_index = cflp(Plant, 
                                                                                                Farm, 
                                                                                                fixed_cost, 
                                                                                                transport_cost, 
                                                                                                manure_production, 
                                                                                                max_capacity, 
                                                                                                target, total_manure)


raster_file = '/Users/wenyuc/Desktop/UT/data/raster/fuzzy_4326.tif'
#'/Users/wenyuc/Desktop/UT/data/raster/fuzzy_and_complete_1_4326.tif'

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

# screen_grid_df = load_raster(raster_file)

color_scale = [
    [0, 255, 0, 255],  # RGB color for value 0 (green)
    [255, 0, 0, 255]   # RGB color for value 1 (red)
]

@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

hex_df = load_data('./df_hex_7.csv')

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
    pickable=False,
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

# # Define a layer to display on a map
# screen_grid_layer = pdk.Layer(
#     "ScreenGridLayer",
#     screen_grid_df,
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

hex_layer = pdk.Layer(
    "H3HexagonLayer",
    hex_df,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    opacity=0.5,
    get_hexagon="hex7",
    get_fill_color ='[255 * Value, 255 * (1 - Value), 0, 255]', 
    # get_line_color=[255, 255, 255],
    line_width_min_pixels=1)

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

@st.cache_data
def configure_deck(potential_digester_location, _suitability_layer, _digesters_layer, _assigned_farms_layer, _unassigned_farms_layer, _arc_layer):
    view_state=pdk.ViewState(
        latitude=potential_digester_location['y'].mean(),
        longitude=potential_digester_location['x'].mean(),
        zoom=9,
        pitch=0
        )
    deck = pdk.Deck(
        layers=[_suitability_layer, _digesters_layer, _assigned_farms_layer, _unassigned_farms_layer, _arc_layer],
        initial_view_state=view_state, 
        tooltip=
        # {'html': '<b>Farm:</b> {farm_number}<br/><b>Digester:</b> {digester_number}<br/><b>Quantity:</b> {material_quantity}t','style': {'color': 'white'}}, 
        {"text": "Suitability: {Value}"}
        )
    return deck

deck = configure_deck(potential_digester_location, hex_layer, digesters_layer, assigned_farms_layer, unassigned_farms_layer, arc_layer)

# Streamlit checkbox for toggling the visibility of the ArcLayer
show_arcs = st.checkbox('Show assignment of farms to digesters', value=True)

# Toggle the visibility of the ArcLayer based on the checkbox
deck.layers[3].visible = show_arcs

# Rendering the map 
st.pydeck_chart(deck, use_container_width=True)


# filename = f"./outputs/cflp_v{6}_{int(target*100)}%manure.png"  # You can choose the file extension (e.g., .png, .jpg, .pdf)
# plot_result(Plant, 
#             potential_digester_location, 
#             assignment_decision, farm, Farm, use_plant_index, target, total_cost, filename, save_fig=False)
