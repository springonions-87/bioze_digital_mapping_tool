import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from cflp_function import *
from calculate_od import *
from shapely.geometry import mapping
from datetime import date
from pydeck.types import String

today = date.today()
# import os
# print("Current working directory: ", os.getcwd())

### PAGE CONFIGURATIONS #######################################
# st.title('BIOZE Digital Mapping Tool')
# st.text('This is an interactive mapping tool on biogas.')
st.set_page_config(page_title="Bioze Mapping Tool - Policy Exploration (Random Sites)", layout="wide")
# st.markdown(
#     """
#     <style>
#     #root .block-container {
#         max-width: none;
#         padding-left: 0;
#         padding-right: 0;
#     }
#     .stFrame {
#         width: 100vw !important;
#         height: 100vh !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True)


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
def load_pickle():
    folder_path = 'app_data'
    # List
    # set F     set of farm locations (list)
    I = load_data_from_pickle(folder_path, 'Farm_test.pickle')
    # set P     set of potential digester locations
    # Plant = load_data_from_pickle(folder_path, 'Plant_test_2.pickle')

    # Dictionary 
    # p_i       manure production of each i
    d = load_data_from_pickle(folder_path, 'manure_production_test.pickle')
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
    # potential_digester_location = load_csv(r'./farm/farm_cluster_mock_5.csv')
    # farm = load_csv(r"./farm/farm_mock.csv")

    return I, d, total_manure

@st.cache_data
def filter_Plant(original_dict, J):
    """
    Extract key-value pairs where the key is in the Plant selection
    """
    filtered_dict = {key: value for key, value in original_dict.items() if key in J}
    return filtered_dict

# def configure_main_deck(avg_lat, avg_lon,_suitability_layer, _digesters_layer, _assigned_farms_layer, _unassigned_farms_layer, _arc_layer):
#     """
#     Configure the view state and deck property for the main plot of the model visualisation
#     """
#     view_state=pdk.ViewState(
#         latitude=avg_lat,
#         longitude=avg_lon,
#         zoom=9,
#         )
#     deck = pdk.Deck(
#         layers=[_suitability_layer, _digesters_layer, _assigned_farms_layer, _unassigned_farms_layer, _arc_layer],
#         initial_view_state=view_state, 
#         map_style='mapbox://styles/mapbox/streets-v12',
#         tooltip=
#         # {'html': '<b>Farm:</b> {farm_number}<br/><b>Digester:</b> {digester_number}<br/><b>Quantity:</b> {material_quantity}t','style': {'color': 'white'}}, 
#         {"text": "Suitability: {Value}"}
#         )
#     return deck

def initialize_map(digester_df, farm_df, suitability_df):
    digester_layer = pdk.Layer(type='ScatterplotLayer',
                                data=digester_df,
                                get_position=['x', 'y'],
                                get_radius=800,
                                get_fill_color='color',
                                pickable=True,
                                auto_highlight=True, 
                                get_line_color=[255, 255, 255],
                                get_line_width=3)
    farm_layer = pdk.Layer(type='ScatterplotLayer',
                           data=farm_df,
                           get_position=['x', 'y'],
                           get_radius=300,
                                       get_fill_color='color',
                                       get_line_color=[0, 0, 0],
                                       pickable=False,
                                       auto_highlight=True)
    hex_layer = pdk.Layer(type="H3HexagonLayer",
        data=suitability_df,
        pickable=True,
        filled=True,
        extruded=False,
        opacity=0.5,
        get_hexagon="he7",
        # get_fill_color ='[255 * Value, 255 * (100 - Value), 0, 255]',
        get_fill_color ='[0, 0, 255*Value, 255]',
        auto_highlight=True)
    
    digester_df['name'] = digester_df.index.astype(str)
    # Define a layer to display on a map
    digester_label_layer = pdk.Layer(
        "TextLayer",
        digester_df,
        pickable=True,
        get_position=['x', 'y'],
        get_text="name",
        get_size=18,
        get_color=[255,255,255],
        get_angle=0,
        # Note that string constants in pydeck are explicitly passed as strings
        # This distinguishes them from columns in a data set
        get_text_anchor=String("middle"),
        get_alignment_baseline=String("center"))
    
    view_state=pdk.ViewState(
        latitude=farm_df['y'].mean(),
        longitude=farm_df['x'].mean(),
        zoom=9,
        )
    deck = pdk.Deck(
        layers=[hex_layer, farm_layer, digester_layer, digester_label_layer],
        initial_view_state=view_state, 
        map_style= 
        #'mapbox://styles/mapbox/satellite-v9',
        'mapbox://styles/mapbox/streets-v12',
        tooltip=
        # {'html': '<b>Farm:</b> {farm_number}<br/><b>Digester:</b> {digester_number}<br/><b>Quantity:</b> {material_quantity}t','style': {'color': 'white'}}, 
        {"text": "Suitability: {Value}"}
        )
    return deck

def update_digester_layer_color(digester_df, J, deck):
    # Update the color of digester to grey if not selected 
    digester_df_copy = digester_df.copy()
    digester_df_copy.loc[~digester_df_copy.index.isin(J), 'color'] ='[169, 169, 169]'
    deck.layers[2].data = digester_df_copy
    return deck

def update_farm_layer_color(farm_df, digester_df, assignment_decision, deck): 
    # Update the color of farms to match the color of digester assigned to
    farm_df_copy = farm_df.copy()
    farm_df_copy['color'] = farm_df_copy.index.map({index: digester_df['color'].iloc[farm_index] for farm_index, indices in assignment_decision.items() for index in indices})
    deck.layers[1].data = farm_df_copy
    return deck

def update_map(farm_df, digester_df, assignment_decision, deck):
    arc_layer_df = get_arc(assignment_decision, digester_df, farm_df)
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
    # Add the ArcLayer to the existing deck
    deck.layers.append(arc_layer)

    # Update the map with the modified deck
    return deck

### SESSION STATE INITIALIZATION #######################################
@st.cache_data
def session_load(loi):
    main_crs ='EPSG:4326'

    # Load data and calculate od matrix
    # loi = load_csv('./hex/loi.csv') #st.session_state.list_of_locations
    # loi_gdf = loi_to_gdf(loi) # find centroid of hexagons and convert to gdf
    loi_gdf = loi_to_gdf(loi.reset_index(drop=True))
    loi_gdf['y'] = loi_gdf['geometry'].y
    loi_gdf['x'] = loi_gdf['geometry'].x

    farm_gdf = load_gdf("./farm/farm_new.shp")
    n = load_gdf("./osm_network/G_n.shp")
    n = n.to_crs(main_crs)

    find_closest_osmid(farm_gdf, n)
    find_closest_osmid(loi_gdf, n)
    c, plant = calculate_od_matrix(farm_gdf, loi_gdf, cost_per_km=0.69)

    Plant_all = ['All'] + plant
    # Plant_all = ['All'] + [str(x) for x in plant]
    M, f = random_M_f(plant) # random M and f generator for the time being

    I, d, total_manure  = load_pickle()

    color_mapping = {label: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for label in loi_gdf.index}
    loi_gdf['color'] = loi_gdf.index.map(color_mapping)

    # Load suitability map
    farm = load_csv("./farm/farm_mock.csv")
    farm['color'] = '[169, 169, 169]'
    hex_df = load_csv('./hex/df_hex_7.csv')

    # Load location of interest
    # polygons = load_gdf('./suitable_polygon_plot.shp')
    # polygons['coordinates'] = polygons['geometry'].apply(lambda geom: mapping(geom)['coordinates'][0])    
    data_dict = {
        'loi_gdf':loi_gdf,
        'c':c,
        'plant':plant,
        'Plant_all':Plant_all,
        'M':M,
        'f':f,
        'I':I,
        'd':d,
        'farm':farm,
        'hex_df':hex_df
    }
    return data_dict

### FUNCTION TO PERFORM THE ONE-TIME INITIAL CALCULATION ##################################
def perform_initial_setup(loi, page_2_space):
    data_name = ['loi_gdf', 'c', 'plant', 'Plant_all', 'M', 'f', 'I', 'd', 'farm', 'hex_df']
    # Check if any key in data_names is missing in st.session_state.keys()
    missing_keys = [key for key in data_name if key not in page_2_space.keys()]
    # st.write(missing_keys)
    if missing_keys:
        loaded_data = session_load(loi)
        for key, value in loaded_data.items():
            page_2_space[key] = value
        # Initialize session_state if it doesn't exist
    if 'target' not in page_2_space:
        page_2_space['target'] = 0  # Set a default value, adjust as needed

### FUNCTION TO DISPLAY THE MAIN CONTENT OF THE APP ##################################
def main_content(page_2_space):
    ### ACCESS INITIAL SESSION VARIABLES ##################################
    # I = st.session_state['I']
    # d = st.session_state['d']
    # # total_manure = st.session_state.total_manure
    # farm = st.session_state['farm']
    # hex_df = st.session_state['hex_df']
    # c = st.session_state['c']
    # plant = st.session_state['plant']
    # M = st.session_state['M']
    # f = st.session_state['f']
    # Plant_all = st.session_state['Plant_all']
    # loi_gdf = st.session_state['loi_gdf']
    # target = st.session_state['target']

    I = page_2_space.get('I', None)  # Replace None with an appropriate default
    d = page_2_space.get('d', None)
    # total_manure = page_namespace.get('total_manure', None)
    farm = page_2_space.get('farm', None)
    hex_df = page_2_space.get('hex_df', None)
    c = page_2_space.get('c', None)
    plant = page_2_space.get('plant', None)
    M = page_2_space.get('M', None)
    f = page_2_space.get('f', None)
    Plant_all = page_2_space.get('Plant_all', None)
    loi_gdf = page_2_space.get('loi_gdf', None)
    target = page_2_space.get('target', None)
    deck = initialize_map(loi_gdf, farm, hex_df)

    ### SIDEBAR ##################################
    with st.sidebar:
        target = (st.slider('**Manure Utilization Target (%):**', min_value=0, max_value=100,step=10)/ 100) # Define manure use goal (mu)

        with st.container():
            st.write("**Map Layers**")
            show_farm = st.sidebar.checkbox('Farms', value=True)
            show_digester = st.sidebar.checkbox('Digesters', value=True)
            show_arcs = st.sidebar.checkbox('Farm-Digester Assignment', value=True)
            show_suitability = st.sidebar.checkbox('Suitability', value=False)
            # show_polygon = st.sidebar.checkbox('Suitable Areas', value=False)

        st.markdown("")
        st.markdown("")
        st.markdown("")
        with st.expander("Click to learn more about this dashboard"):
            st.markdown(f"""
            Introduce Bioze...
            *Updated on {str(today)}.*  
            """)

    # Toggle the visibility of the ArcLayer based on the checkbox
    # deck.layers[0].visible = show_suitability
    # deck.layers[1].visible = show_digester
    # deck.layers[2].visible = show_farm
    # deck.layers[3].visible = show_farm
    # deck.layers[-1].visible = show_polygon

    ### SELECT PLANT FORM ##########################################
    with st.expander('Customize Site Selection'):
        with st.form('select_plant'):
            J = st.multiselect("Select specific sites to include in the analysis. By default, all sites are included.", Plant_all)
            if "All" in J or not J:
                J = plant
            submit_select_loi = st.form_submit_button("Submit")

    if submit_select_loi and page_2_space['target'] == 0:
        deck = update_digester_layer_color(loi_gdf, J, deck)

    if submit_select_loi or page_2_space['target'] != target:
        with st.spinner('Running the model...'):
            page_2_space['target'] = target # Update the session state with the new target value
            M = filter_Plant(M, J)
            f = filter_Plant(f, J)
            c = {(i, j): value for (i, j), value in c.items() if j in J}

        ### RUN MODEL ##########################################
            m, total_manure = flp_scip(I, J, d, M, f, c, target)
            m.optimize()
            total_cost, assignment_decision, percentage_utilization = flp_get_result(m, I, J, M)
            ### OUTCOME INDICATORS ##########################################
            # old
            # total_biogas = (total_manure * target) * 1000 * 0.39 # ton of manure to biogas potential m3
            # new
            total_biogas = (total_manure * target) * 50 # 1Mg cattle or pig manure (20% org. dry matter) 50 m³ biogas
            # Methane savings (m3/yr)=Biogas yield potential (m3/yr)× Methane content of biogas (%)
            methane_saving = total_biogas*0.6 # methane content of biogas is assumed 60%

            # Display metrics side by side 
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Total Cost", value= "€{:,.2f}".format(total_cost)) #, delta="1.2 °F")
            col1.metric(label="Total Manure Used", value="{:,.2f} Mg/yr".format(total_manure))
            col1.metric(label="Total Biogas Yield Potential", value="{:,.2f} m³/yr".format(total_biogas))
            col1.metric(label="Total Methane Saving Potential", value="{:,.2f} m³/yr".format(methane_saving))
            with col3:
            # Plot bar chart
                st.markdown("Digester Capacity Utilization Rate")
                st.bar_chart(percentage_utilization)

            # arc_layer_df = get_arc(assignment_decision, loi_gdf, farm)
            deck = update_digester_layer_color(loi_gdf, J, deck)
            deck = update_farm_layer_color(farm, loi_gdf, assignment_decision, deck)
            deck = update_map(farm, loi_gdf, assignment_decision, deck)
        # st.success('Optimal solution found!')

    # Rendering the map 
    # deck.layers[-1].visible = show_arcs
    st.pydeck_chart(deck, use_container_width=True)

        
### CREATE STREAMLIT ##################################
def main():
    st.markdown("### Welcome to Policy Explorer!")
    st.markdown("Dive into your saved digester sites from the suitability analysis. Explore the optimal combinations of locations for digesters to process manure in the region.")
    st.markdown("")
    st.markdown("")

    ### INITIALIZE SESSION STATE ##########################################
    if 'page_2' not in st.session_state:
        st.session_state.page_2 = {}
    
    page_2_space = st.session_state.page_2

    if "loi" not in st.session_state or len(st.session_state.loi) == 0:
        st.warning("Oops! It looks like you haven't saved any results yet. Visit suitability snalysis page with the button below, to explore, filter suitable locations, and save your results.", icon="⚠️")
        if st.button("Visit suitability analysis"):
            st.switch_page("app.py")
    else:
        with st.spinner("Preparing the data..."):
            perform_initial_setup(st.session_state.loi, page_2_space) # Replace with your function to generate trial selection
            main_content(page_2_space)

    # with tab2:
    #     with st.spinner("Preparing the data..."):
    #         perform_initial_setup(loi=st.session_state.loi)
    #         main_content_saved()

    ### DISPLAY MAIN CONTENT OF THE APP ##########################################
    # if st.button('Show Data'):
    #     st.write('Data:', st.session_state.list_of_locations)

    # Run the model 
    # total_cost, total_fixed_cost, total_transport_cost, assignment_decision, use_plant_index = cflp(Plant, 
    #                                                                                                 Farm, 
    #                                                                                                 fixed_cost, 
    #                                                                                                 transport_cost, 
    #                                                                                                 manure_production, 
    #                                                                                                 max_capacity, 
    #                                                                                                 target, total_manure)
           

if __name__ == "__main__":
    main()
