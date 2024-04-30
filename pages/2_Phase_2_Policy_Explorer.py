import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from utils.cflp_function import *
from utils.calculate_od import *
# from shapely.geometry import mapping
from datetime import date
from pydeck.types import String
import plotly.express as px


today = date.today()

### PAGE CONFIGURATIONS #######################################
st.set_page_config(page_title="BIOZE Tool - Policy Exploration (Saved Sites)", layout="wide")
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
    J = load_data_from_pickle(folder_path, 'Farm_test.pickle')
    # set P     set of potential digester locations
    # Plant = load_data_from_pickle(folder_path, 'Plant_test_2.pickle')

    # Dictionary 
    # p_i       manure production of each i
    M = load_data_from_pickle(folder_path, 'manure_production_test.pickle')
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
    return J, M

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

def initialize_map(digester_df, farm_df, suitability_df, boundary):
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
    
    boundary_layer = pdk.Layer(
        "GeoJsonLayer",
        data=boundary,
        stroked=True, 
        filled=False,  
        getLineColor = [128,128,128],
        getLineWidth= 80)

    digester_df['name'] = digester_df.index.astype(str)
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
        layers=[hex_layer, farm_layer, digester_layer, digester_label_layer, boundary_layer],
        initial_view_state=view_state, 
        map_style= 
        #'mapbox://styles/mapbox/satellite-v9',
        'mapbox://styles/mapbox/streets-v12',
        tooltip=TOOLTIP_TEXT
        )
    return deck

def update_digester_layer_color(digester_df, I, deck):
    # Update the color of digester to grey if not selected 
    digester_df_copy = digester_df.copy()
    digester_df_copy.loc[~digester_df_copy.index.isin(I), 'color'] ='[169, 169, 169]'
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
def prepare_model_input(loi, _h3_gdf, _farm_gdf):

    loi_gdf = _h3_gdf[_h3_gdf['hex9'].isin(loi.hex9)]
    loi_gdf.index = range(1, len(loi_gdf) + 1) # Reset index to start with 1
    C, plant = calculate_od_matrix(_farm_gdf, loi_gdf, cost_per_km=0.69)

    Plant_all = ['All'] + plant # add "ALL" to the list of candidate sites as input labels for customizing which sites to include in analysis
    color_mapping = {label: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for label in loi_gdf.index}
    loi_gdf['color'] = loi_gdf.index.map(color_mapping)

    d, f = assign_capacity_capex(plant) # random M and f generator for the time being

    return loi_gdf, C, plant, Plant_all, d, f

### SESSION STATE INITIALIZATION #######################################
@st.cache_data
def session_load():
    ### LOAD DATA ###
    boundary = load_gdf('./app_data/twente_4326.geojson')
    h3_gdf = load_gdf('./app_data/h3_geometry.shp')
    # loi_gdf = h3_gdf[h3_gdf['hex9'].isin(loi.hex9)]
    # loi_gdf.index = range(1, len(loi_gdf) + 1) # Reset index to start with 1
    farm_gdf = load_gdf("./app_data/farm.shp")

    ### CALCULATE OD MATRIX ###
    
    # C, plant = calculate_od_matrix(farm_gdf, loi_gdf, cost_per_km=0.69)

    ### FORMAT DATA ###
    # Plant_all = ['All'] + plant # add "ALL" to the list of candidate sites as input labels for customizing which sites to include in analysis
    # color_mapping = {label: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for label in loi_gdf.index}
    # loi_gdf['color'] = loi_gdf.index.map(color_mapping)
    J, M  = load_pickle() # Load mock data for farm locations and manure production 

    # Load suitability map
    farm = load_csv("./farm/farm_mock.csv")
    farm['color'] = '[169, 169, 169]'
    hex_df = load_csv('./hex/hex_df2.csv') # need to be changed later

    data_dict = {
        'boundary':boundary,
        'h3_gdf':h3_gdf,
        'farm_gdf':farm_gdf,
        # 'loi_gdf':loi_gdf,
        # 'C':C,
        # 'plant':plant,
        # 'Plant_all':Plant_all,
        'M':M,
        # 'f':f,
        'J':J,
        # 'd':d,
        'farm':farm,
        'hex_df':hex_df
    }
    return data_dict

### FUNCTION TO PERFORM THE ONE-TIME INITIAL CALCULATION ##################################
def perform_initial_setup(page_2_space):
    data_name = ['boundary', 'h3_gdf', 'farm_gdf', 'M', 'J', 'farm', 'hex_df']
    # Check if any key in data_names is missing in st.session_state.keys()
    missing_keys = [key for key in data_name if key not in page_2_space.keys()]
    if missing_keys:
        loaded_data = session_load()
        for key, value in loaded_data.items():
            page_2_space[key] = value
    if 'target' not in page_2_space:
        page_2_space['target'] = 0  # Set a default value, adjust as needed

### FUNCTION TO DISPLAY THE MAIN CONTENT OF THE APP ##################################
def main_content(page_2_space):
    ### ACCESS INITIAL SESSION VARIABLES ##################################
    boundary = page_2_space.get('boundary', None)
    J = page_2_space.get('J', None)  # Replace None with an appropriate default
    # d = page_2_space.get('d', None)
    farm = page_2_space.get('farm', None)
    hex_df = page_2_space.get('hex_df', None)
    # C = page_2_space.get('C', None)
    # plant = page_2_space.get('plant', None)
    M = page_2_space.get('M', None)
    # f = page_2_space.get('f', None)
    # Plant_all = page_2_space.get('Plant_all', None)
    # loi_gdf = page_2_space.get('loi_gdf', None)
    target = page_2_space.get('target', None)
    h3_gdf = page_2_space.get('h3_gdf', None)
    farm_gdf = page_2_space.get('farm_gdf', None)

    loi_gdf, C, plant, Plant_all, d, f = prepare_model_input(st.session_state.loi, h3_gdf, farm_gdf)
    deck = initialize_map(loi_gdf, farm, hex_df, boundary)

    ### SIDEBAR ##################################
    with st.sidebar:
        target = (st.slider(':dart: **Manure Utilization Target (%):**', min_value=0, max_value=100,step=10)/ 100) # Define manure use goal (mu)

        with st.container():
            st.write("**Map Layers**")
            show_farm = st.sidebar.checkbox('Farms', value=True)
            show_digester = st.sidebar.checkbox('Digesters', value=True)
            # show_arcs = st.sidebar.checkbox('Farm-Digester Assignment', value=True)
            show_suitability = st.sidebar.checkbox('Suitability', value=False)

        st.markdown("")
        st.markdown("")
        st.markdown("")
        with st.expander("Click to learn more about this dashboard"):
            st.markdown(f"""
            Introduce Bioze...
            *Updated on {str(today)}.*  
            """)

    # Toggle the visibility of the ArcLayer based on the checkbox 
        # PROBLEM : every time after re ticking the layer, all data is gone on the layer
    deck.layers[0].visible = show_suitability
    deck.layers[1].visible = show_farm
    deck.layers[2].visible = show_digester
    # deck.layers[-1].visible = show_arcs 

    ### SELECT PLANT FORM ##########################################
    with st.expander(':white_check_mark: Customize Site Selection'):
        with st.form('select_plant'):
            I = st.multiselect("Select specific sites to include in the analysis. By default, all sites are included.", Plant_all)
            if "All" in I or not I:
                I = plant
            submit_select_loi = st.form_submit_button("Submit")

    if submit_select_loi and page_2_space['target'] == 0:
        deck = update_digester_layer_color(loi_gdf, I, deck)

    if submit_select_loi or page_2_space['target'] != target:
        with st.spinner('Running the model...'):
            page_2_space['target'] = target # Update the session state with the new target value
            d = filter_Plant(d, I)
            f = filter_Plant(f, I)
            C = {(i, j): value for (i, j), value in C.items() if i in I}

        ### RUN MODEL ##########################################
            m, processed_manure = flp_scip(I, J, d, M, f, C, target)
            m.optimize()
            total_cost, assignment_decision, used_capacity_df = flp_get_result(m, I, J, d, C)
            ### OUTCOME INDICATORS ##########################################
            total_biogas = processed_manure * 20 # 1 tonne manure yields around 20m³ biogas
            # Methane savings (m3/yr)=Biogas yield potential (m3/yr)× Methane content of biogas (%)
            methane_saving = total_biogas*0.6 # methane content of biogas is assumed 60%

            # Display metrics side by side 
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Total Cost over Lifetime (12 yr)", value="€{:,.2f}M".format(sum(total_cost['Value']) / 1000000))
                        #value= "€{:,.0f}".format(sum(total_cost['Value']))) #, delta="1.2 °F")
            # with col1:
            #     fig = px.pie(total_cost, names='Category', values='Value')
            #     st.plotly_chart(fig, use_container_width=True)
            col1.metric(label="Total Manure Processed", value="{:,.0f} t/yr".format(processed_manure))
            col1.metric(label="Total Biogas Yield Potential", value="{:,.0f}M m³/yr".format(total_biogas/ 1000000))
            # col1.metric(label="Total Methane Saving Potential", value="{:,.0f} m³/yr".format(methane_saving))
            with col3:
            # Plot bar chart
                st.markdown("Digester Capacity Utilization Rate")
                st.bar_chart(used_capacity_df)

            deck = update_digester_layer_color(loi_gdf, I, deck)
            deck = update_farm_layer_color(farm, loi_gdf, assignment_decision, deck)
            deck = update_map(farm, loi_gdf, assignment_decision, deck)

    # Rendering the map 
    # deck.layers[-1].visible = show_arcs
    st.pydeck_chart(deck, use_container_width=True)

        
### CREATE STREAMLIT ##################################
def main():
    st.markdown("### Phase 2: Policy Explorer")
    st.markdown(
        "The map below displays where your candidate sites from **Phase 1** and the farms in the area are located."
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
    if 'page_2' not in st.session_state:
        st.session_state.page_2 = {}
    
    page_2_space = st.session_state.page_2

    if "loi" not in st.session_state or len(st.session_state.loi) == 0:
        st.warning("Oops! It looks like you haven't saved any results yet. Go to **Phase 1** first.", icon="⚠️")
        if st.button("Visit **Phase 1**"):
            st.switch_page("app.py")
    else:
        with st.spinner("Running..."):
            perform_initial_setup(page_2_space) # Replace with your function to generate trial selection
            main_content(page_2_space)

if __name__ == "__main__":
    main()
