import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from cflp_function import *
from calculate_od import *
from shapely.geometry import mapping
from datetime import date
from pydeck.types import String
import plotly.express as px

import os
os.environ['USE_PYGEOS'] = '0'
import geopandas

today = date.today()

### PAGE CONFIGURATIONS #######################################
# st.title('BIOZE Digital Mapping Tool')
# st.text('This is an interactive mapping tool on biogas.')
st.set_page_config(page_title="BIOZE Tool - Policy Exploration (Random Sites)", layout="wide")
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
    # total_manure = load_data_from_pickle(folder_path, 'total_manure_test.pickle')
    
    # DataFrame
    # potential_digester_location = load_csv(r'./farm/farm_cluster_mock_5.csv')
    # farm = load_csv(r"./farm/farm_mock.csv")

    return I, d #, total_manure

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

def initialize_map(digester_df, farm_df, boundary):
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

    boundary_layer = pdk.Layer(
        "GeoJsonLayer",
        data=boundary,
        stroked=True, 
        filled=False,  
        getLineColor = [128,128,128],
        getLineWidth= 80
    )
    
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
    TOOLTIP_TEXT = {
        "html": "Manure: {material_quantity} ton/yr <br /> From: farm #<span style='color:white; font-weight:bold;'>{farm_number}</span> <br /> To: digester site #<span style='color:white; font-weight:bold;'>{digester_number}</span>"
    }
    deck = pdk.Deck(
        layers=[boundary_layer, farm_layer, digester_layer, digester_label_layer],
        initial_view_state=view_state, 
        map_style= 
        #'mapbox://styles/mapbox/satellite-v9',
        'mapbox://styles/mapbox/streets-v12',
        tooltip=TOOLTIP_TEXT
        # {'html': '<b>Farm:</b> {farm_number}<br/><b>Digester:</b> {digester_number}<br/><b>Quantity:</b> {material_quantity}t','style': {'color': 'white'}}, 
        # {"text": "Suitability: {Value}"}
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
    # farm_df_copy['color'] = farm_df_copy.index.map({index: digester_df['color'].iloc[farm_index] for farm_index, indices in assignment_decision.items() for index in indices})
    for digester_index, farm_indices in assignment_decision.items():
        digester_color = digester_df.loc[digester_index, 'color']
        for farm_index in farm_indices:
            farm_df_copy.at[farm_index, 'color'] = digester_color
    deck.layers[1].data = farm_df_copy
    return deck

def update_map(farm_df, digester_df, assignment_decision, deck):
    # st.write(digester_df)
    arc_layer_df = get_arc(assignment_decision, digester_df, farm_df)
    # st.write(arc_layer_df)
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
def session_load():
    main_crs ='EPSG:4326'

    ### LOAD DATA ###
    boundary = load_gdf('./data/twente_4326.geojson')
    loi = load_csv('./hex/loi.csv') # Mock candidate sites
    farm_gdf = load_gdf("./farm/farm_new.shp")
    n = load_gdf("./osm_network/G_n.shp") # Road network nodes
    n = n.to_crs(main_crs)
    ### CALCULATE OD MATRIX ###
    loi.index = range(1, len(loi) +1) # Reset index to start with 1 (because users don't like 0 as the 1st value...)
    loi_gdf = loi_to_gdf(loi) # Find centroid of hexagons and convert to gdf
    loi_gdf['y'] = loi_gdf['geometry'].y
    loi_gdf['x'] = loi_gdf['geometry'].x
    find_closest_osmid(farm_gdf, n)
    find_closest_osmid(loi_gdf, n)
    c, plant = calculate_od_matrix(farm_gdf, loi_gdf, cost_per_km=0.69)

    ### FORMAT DATA ###
    Plant_all = ['All'] + plant # add "ALL" to the list of candidate sites as input labels for customizing which sites to include in analysis
    color_mapping = {label: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for label in loi_gdf.index}
    loi_gdf['color'] = loi_gdf.index.map(color_mapping)
    M, f = assign_capacity_capex(plant) # random M and f generator for the time being
    I, d  = load_pickle() # Load mock data for farm locations and manure production 

    # Load suitability map
    farm = load_csv("./farm/farm_mock.csv")
    farm['color'] = '[169, 169, 169]'

    data_dict = {
        'boundary':boundary,
        'loi_gdf':loi_gdf,
        'c':c,
        'plant':plant,
        'Plant_all':Plant_all,
        'M':M,
        'f':f,
        'I':I,
        'd':d,
        'farm':farm}
    return data_dict

### FUNCTION TO PERFORM THE ONE-TIME INITIAL CALCULATION ##################################
def perform_initial_setup():
    data_name = ['boundary', 'loi_gdf', 'c', 'plant', 'Plant_all', 'M', 'f', 'I', 'd', 'farm']
    # Check if any key in data_names is missing in st.session_state.keys()
    missing_keys = [key for key in data_name if key not in st.session_state.keys()]
    # st.write(missing_keys)
    if missing_keys:
        loaded_data = session_load()
        for key, value in loaded_data.items():
            st.session_state[key] = value
        # Initialize session_state if it doesn't exist
    if 'target' not in st.session_state:
        st.session_state['target'] = 0  # Set a default value, adjust as needed

### FUNCTION TO DISPLAY THE MAIN CONTENT OF THE APP ##################################
def main_content_random():
    ### ACCESS INITIAL SESSION VARIABLES ##################################
    boundary = st.session_state['boundary']
    I = st.session_state['I']
    d = st.session_state['d']
    # total_manure = st.session_state.total_manure
    farm = st.session_state['farm']
    c = st.session_state['c']
    plant = st.session_state['plant']
    M = st.session_state['M']
    f = st.session_state['f']
    Plant_all = st.session_state['Plant_all']
    loi_gdf = st.session_state['loi_gdf']
    target = st.session_state['target']
    deck = initialize_map(loi_gdf, farm, boundary)

    ### SIDEBAR ##################################
    with st.sidebar:
        target = (st.slider(':dart: **Manure Utilization Target (%):**', min_value=0, max_value=100,step=10, key="target_random")/ 100) # Define manure use goal (mu)

        with st.container():
            st.write("**Map Layers**")
            show_farm = st.sidebar.checkbox('Farms', value=True, key="show_farm_random")
            show_digester = st.sidebar.checkbox('Digesters', value=True, key="show_digester_random")
            show_arcs = st.sidebar.checkbox('Farm-Digester Assignment', value=True, key="show_arcs_random")
            show_suitability = st.sidebar.checkbox('Suitability', value=False, key="show_suitability_random")
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
    with st.expander(':white_check_mark: Customize Site Selection'):
        with st.form('select_plant_random_form'):
            J = st.multiselect("Select specific sites to include in the analysis. By default, all sites are included.", Plant_all, key="select_plant_random")
            if "All" in J or not J:
                J = plant
            submit_select_loi = st.form_submit_button("Submit")

    if submit_select_loi and st.session_state['target'] == 0:
        deck = update_digester_layer_color(loi_gdf, J, deck)

    if submit_select_loi or st.session_state['target'] != target:
        with st.spinner('Running the model...'):
            st.session_state['target'] = target # Update the session state with the new target value
            M = filter_Plant(M, J)
            f = filter_Plant(f, J)
            c = {(i, j): value for (i, j), value in c.items() if j in J}

        ### RUN MODEL ##########################################
            m, processed_manure = flp_scip(I, J, d, M, f, c, target)
            m.optimize()
            total_cost, assignment_decision, used_capacity_df = flp_get_result(m, I, J, M, c, plant)
            ### OUTCOME INDICATORS ##########################################
            total_biogas = processed_manure * 20 # 1 tonne manure yields around 20m³ biogas
            # Methane savings (m3/yr)=Biogas yield potential (m3/yr)× Methane content of biogas (%)
            methane_saving = total_biogas*0.6 # methane content of biogas is assumed 60%

            # Display metrics side by side 
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Total Cost over Lifetime (12 yr)", value="€{:,.2f}M".format(sum(total_cost['Value']) / 1000000))
                        #value= "€{:,.0f}".format(sum(total_cost['Value']))) #, delta="1.2 °F")
            with col1:
                fig = px.pie(total_cost, names='Category', values='Value')
                st.plotly_chart(fig, use_container_width=True)
            col2.metric(label="Total Manure Processed", value="{:,.0f} t/yr".format(processed_manure))
            col2.metric(label="Total Biogas Yield Potential", value="{:,.0f}M m³/yr".format(total_biogas/ 1000000))
            # col1.metric(label="Total Methane Saving Potential", value="{:,.0f} m³/yr".format(methane_saving))
            with col3:
            # Plot bar chart
                st.markdown("Digester Capacity Utilization Rate")
                st.bar_chart(used_capacity_df)
            # st.write(total_cost)

            # Find and list duplicates within lists in the assignment_decision dict aka when farm is assigned to more than one digester
            # def find_duplicates_in_lists(d):
            #     seen_values = set()
            #     duplicates = set()

            #     for values_list in d.values():
            #         for value in values_list:
            #             if value in seen_values:
            #                 duplicates.add(value)
            #             seen_values.add(value)

            #     return list(duplicates)

            # duplicates_list = find_duplicates_in_lists(assignment_decision)

            # if duplicates_list:
            #     st.write("Duplicates found within the lists in the dictionary:", duplicates_list)
            # else:
            #     st.write("There are no duplicates within the lists in the dictionary.")

            deck = update_digester_layer_color(loi_gdf, J, deck)
            deck = update_farm_layer_color(farm, loi_gdf, assignment_decision, deck)
            deck = update_map(farm, loi_gdf, assignment_decision, deck)

    # Rendering the map 
    # deck.layers[-1].visible = show_arcs
    st.pydeck_chart(deck, use_container_width=True)

        
### CREATE STREAMLIT ##################################
def main():
    st.markdown("### Phase 2: Policy Explorer (Random Sites)")
    st.markdown(
        "The map below displays farms in the region and 7 **randomly** generated candidate sites for large-scale digester."
        " By utilizing manure from local farms, we can produce biogas as a substitute for natural gas, promoting renewable energy and preventing greenhouse gas emissions from manure. "
        " Investigate the best locations to build large digesters based on various policy goals concerning the amount of manure designated for biogas production.")
    st.markdown("")
    st.markdown(":dart:"
        " Determine how much of the manure in the region you would like to use for biogas production and indicate that amount with the **'Manure Utilization Target (%)'** slider. "
        " The tool will find the most strategic locations to build large digesters to meet your target."
    )
    st.markdown("")
    st.markdown(":white_check_mark:"
        " You can determine which candidate sites are included in the analysis by selecting them in **'Customize Site Selection'**. By default all sites are included in the analysis."
    )
    st.markdown("")
    with st.expander("**How to read the map :mag_right:**"):
        st.markdown("Farms - :black_circle:")
        st.markdown("Candidate digester sites - :rainbow[Colored] and numbered markers")
        st.markdown("Assignment of farms to digester sites - **:green[green]** and **:red[red]** arcs")
        st.markdown("Note: Color of farms will change to the color of the digester sites they are assigned to in the solution. If the farms are excluded in the solution, they will remain black.")
    st.markdown("")
    st.divider()
    st.markdown("")
    ### INITIALIZE SESSION STATE ##########################################

    # # Buttons for choosing between "Use Saved Results" and "Use Trial Selection"
    # use_saved_button = st.button("Explore with Saved Digester Sites", help="Continue with the saved filtered suitable locations from previous section.")
    # use_trial_button = st.button("Explore with Random Digester Sites", help="Continue with random locations.")

    # if use_saved_button:
    #     with st.spinner("Preparing the data..."):
    #         perform_initial_setup(loi=st.session_state.loi)
    #         main_content()
    # elif use_trial_button:
    #     with st.spinner("Preparing the data..."):
    #         perform_initial_setup(loi=load_csv('./hex/loi.csv')) # Replace with your function to generate trial selection
    #         main_content()

    with st.spinner("Preparing the data..."):
        perform_initial_setup() # Replace with your function to generate trial selection
    
    main_content_random()

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
