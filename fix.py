import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from cflp_function import *
from calculate_od import *
from shapely.geometry import mapping
from datetime import date

today = date.today()
# import os
# print("Current working directory: ", os.getcwd())

########## PAGE CONFIGURATIONS ##########
# st.title('BIOZE Digital Mapping Tool')
# st.text('This is an interactive mapping tool on biogas.')
st.set_page_config(page_title="Bioze Mapping Tool", layout="wide")
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
    unsafe_allow_html=True)

### FUNCTIONS #######################################
@st.cache_data
def load_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

@st.cache_data
def load_gdf(gdf_path):
    gdf = gpd.read_file(gdf_path)
    return gdf

@st.cache_data
def load_data():
    folder_path = 'app_data'
    # List
    # set F     set of farm locations (list)
    Farm = load_data_from_pickle(folder_path, 'Farm_test.pickle')
    # set P     set of potential digester locations
    # Plant = load_data_from_pickle(folder_path, 'Plant_test_2.pickle')

    # Dictionary 
    # p_i       manure production of each i
    manure_production = load_data_from_pickle(folder_path, 'manure_production_test.pickle')
    # q_j       max capacity of each j 
    # max_capacity = load_data_from_pickle(folder_path, 'max_capacity_test.pickle')
    # f_j       fixed cost of establishing each j
    # fixed_cost = load_data_from_pickle(folder_path, 'fixed_cost_test.pickle')        
    # C_ij      transportation matrix 
    # transport_cost = load_data_from_pickle(folder_path, 'transportation_cost_test.pickle') - cflp version
    # transport_cost = load_data_from_pickle(folder_path, 'c_test.pickle') # scip flp version

    # Float
    # alpha     total manure production
    total_manure = load_data_from_pickle(folder_path, 'total_manure_test.pickle')
    
    # DataFrame
    potential_digester_location = load_csv(r'./farm/farm_cluster_mock_5.csv')
    farm = load_csv(r"./farm/farm_mock.csv")

    return Farm, manure_production, total_manure, potential_digester_location, farm

# @st.cache_data
# def filter_Plant(original_dict, selected_plant):
#     # Extract key-value pairs where the key is not in the list
#     filtered_dict = {key: value for key, value in original_dict.items() if key in selected_plant}
#     return filtered_dict

@st.cache_data
def filter_Plant(original_dict, J):
    """
    Extract key-value pairs where the key is in the Plant selection
    """
    filtered_dict = {key: value for key, value in original_dict.items() if key in J}
    return filtered_dict

def configure_main_deck(avg_lat, avg_lon,_suitability_layer, _digesters_layer, _assigned_farms_layer, _unassigned_farms_layer, _arc_layer, _polygon_layer):
    """
    Configure the view state and deck property for the main plot of the model visualisation
    """
    view_state=pdk.ViewState(
        latitude=avg_lat,
        longitude=avg_lon,
        zoom=9,
        # pitch=0
        )
    deck = pdk.Deck(
        layers=[_suitability_layer, _digesters_layer, _assigned_farms_layer, _unassigned_farms_layer, _arc_layer, _polygon_layer],
        initial_view_state=view_state, 
        map_style='mapbox://styles/mapbox/streets-v12',
        tooltip=
        # {'html': '<b>Farm:</b> {farm_number}<br/><b>Digester:</b> {digester_number}<br/><b>Quantity:</b> {material_quantity}t','style': {'color': 'white'}}, 
        {"text": "Suitability: {Value}"}
        )
    return deck
        

### CREATE STREAMLIT ##################################
def main():

    ### CALCULATE OD MATRIX ##########################################
    # Load od matrix calculation inputs
    main_crs ='EPSG:4326'
    loi = load_csv('./hex/loi.csv')
    farm_gdf = load_gdf("./farm/farm_new.shp")
    n = load_gdf("./osm_network/G_n.shp")
    n = n.to_crs(main_crs)

    loi_gdf = loi_to_gdf(loi)    
    loi_gdf['y'] = loi_gdf['geometry'].y
    loi_gdf['x'] = loi_gdf['geometry'].x
    find_closest_osmid(farm_gdf, n)
    find_closest_osmid(loi_gdf, n)
    c, plant = calculate_od_matrix(farm_gdf, loi_gdf, cost_per_km=0.69)

    #### LOAD DATA ##################################
    # Load model inputs
    I, d, total_manure, potential_digester_location, farm = load_data()
    Plant_all = ['All'] + plant
    # Plant_all = ['All'] + [str(x) for x in plant]
    M, f = random_M_f(plant)

    # Load suitability map
    hex_df = load_csv('./hex/df_hex_7.csv')

    # Load location of interest
    polygons = load_gdf('./suitable_polygon_plot.shp')
    polygons['coordinates'] = polygons['geometry'].apply(lambda geom: mapping(geom)['coordinates'][0])

    #### SIDEBAR ##################################
    with st.sidebar:
        target = (st.slider('Manure Utilization target (%):', min_value=0, max_value=100,step=10)/ 100) # Define manure use goal (mu)

        with st.container():
            st.write("**Layers**")
            show_farm = st.sidebar.checkbox('Farms', value=True)
            show_digester = st.sidebar.checkbox('Digesters', value=True)
            show_arcs = st.sidebar.checkbox('Farm-Digester Assignment', value=True)
            show_suitability = st.sidebar.checkbox('Suitability', value=False)
            show_polygon = st.sidebar.checkbox('Suitable Areas', value=False)

        with st.expander("Click to learn more about this dashboard"):
            st.markdown(f"""
            Introduce Bioze
            *Updated on {str(today)}.*  
            """)

    ### SELECT PLANT FORM ##########################################
    with st.expander('Select Locations'):
        with st.form('select_plant'):
            J = st.multiselect(" ", Plant_all)
            if "All" in J:
                J = plant
            submit_select_loi = st.form_submit_button("Submit")
        if submit_select_loi:
            M = filter_Plant(M, J)
            f = filter_Plant(f, J)
            c = {(i, j): value for (i, j), value in c.items() if j in J}

    ### RUN FLP MODEL ##########################################
    # Run the model 
    # total_cost, total_fixed_cost, total_transport_cost, assignment_decision, use_plant_index = cflp(Plant, 
    #                                                                                                 Farm, 
    #                                                                                                 fixed_cost, 
    #                                                                                                 transport_cost, 
    #                                                                                                 manure_production, 
    #                                                                                                 max_capacity, 
    #                                                                                                 target, total_manure)
            m = flp_scip(I, J, d, M, f, c, target)
            m.optimize()

            total_cost, assignment_decision = flp_get_result(m)

            arc_layer_df = get_arc(assignment_decision, loi_gdf, farm)

            color_mapping = {label: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for label in J}

            digester_df, assigned_farms_df, unassigned_farms_df = get_plot_variables(assignment_decision, loi_gdf, farm, color_mapping)
            assignment_decision
            ### OUTCOME INDICATORS ##########################################
            # total_biogas = (total_manure * target) * 1000 * 0.39 # ton of manure to biogas potential m3
            # # Display metrics side by side 
            # col1, col2 = st.columns(2)
            # col1.metric(label="Total Cost", value= "€{:,.2f}".format(total_cost)) #, delta="1.2 °F")
            # col2.metric(label="Total Biogas Production", value="{:,.2f} m³".format(total_biogas))

            ### PLOT PYDECK LAYERS ###############################################
            # Create a Pydeck layer for digesters
            avg_lat=farm['y'].mean()
            avg_lon=farm['x'].mean()
            digesters_layer = pdk.Layer(
                type='ScatterplotLayer',
                data=digester_df,
                get_position=['x', 'y'],
                get_radius=800,
                get_fill_color='color',
                pickable=True,
                auto_highlight=True, 
                get_line_color=[255, 255, 255],
                get_line_width=3,
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

            # Set up the Pydeck PolygonLayer
            polygon_layer = pdk.Layer(
                "PolygonLayer",
                data=polygons,
                get_polygon='coordinates',
                get_fill_color=[255, 0, 0, 150],  # Red color with 150 transparency
                get_line_color=[255, 255, 255],
                get_line_width=2,
                pickable=True,
            )

            hex_layer = pdk.Layer(
                "H3HexagonLayer",
                hex_df,
                pickable=True,
                filled=True,
                extruded=False,
                opacity=0.5,
                get_hexagon="hex7",
                # get_fill_color ='[255 * Value, 255 * (100 - Value), 0, 255]',
                get_fill_color ='[0, 0, 255*Value, 255]',
                auto_highlight=True)

            deck = configure_main_deck(avg_lat, avg_lon, hex_layer, digesters_layer, assigned_farms_layer, unassigned_farms_layer, arc_layer, polygon_layer)

            # Toggle the visibility of the ArcLayer based on the checkbox
            deck.layers[0].visible = show_suitability
            deck.layers[1].visible = show_digester
            deck.layers[2].visible = show_farm
            deck.layers[3].visible = show_farm
            deck.layers[-2].visible = show_arcs
            deck.layers[-1].visible = show_polygon

            # Rendering the map 
            st.pydeck_chart(deck, use_container_width=True)


if __name__ == "__main__":
    main()


# filename = f"./outputs/cflp_v{6}_{int(target*100)}%manure.png"  # You can choose the file extension (e.g., .png, .jpg, .pdf)
# plot_result(Plant, 
#             potential_digester_location, 
#             assignment_decision, farm, Farm, use_plant_index, target, total_cost, filename, save_fig=False)
