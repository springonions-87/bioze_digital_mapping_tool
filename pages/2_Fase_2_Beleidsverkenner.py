import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from utils.cflp_function import *
from utils.calculate_od import *
from datetime import date
from pydeck.types import String
import plotly.express as px
import random

# Constants
TODAY = date.today()
FOLDER_PATH = 'app_data'

# Page configurations
st.set_page_config(page_title="BIOZE Tool - Policy Exploration (Saved Sites)", layout="wide")

class DataLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load_data(self, file_path, file_type):
        if file_type == 'csv':
            return pd.read_csv(file_path)
        elif file_type == 'gdf':
            return gpd.read_file(file_path)
        elif file_type == 'pickle':
            return self.load_data_from_pickle(self.folder_path, file_path)

    def load_all_data(self):
        J = self.load_data('Farm_test.pickle', 'pickle')
        M = self.load_data('manure_production_test.pickle', 'pickle')
        return J, M
    
    def load_data_from_pickle(self, folder_path, file_path):
        with open(f"{folder_path}/{file_path}", "rb") as f:
            data = pickle.load(f)
        return data

class MapInitializer:
    def __init__(self, digester_df, farm_df, suitability_df, boundary):
        self.digester_df = digester_df
        self.farm_df = farm_df
        self.suitability_df = suitability_df
        self.boundary = boundary

    def initialize_map(self):
        digester_layer = pdk.Layer(type='ScatterplotLayer',
                                    data=self.digester_df,
                                    get_position=['x', 'y'],
                                    get_radius=800,
                                    get_fill_color='color',
                                    pickable=True,
                                    auto_highlight=True, 
                                    get_line_color=[255, 255, 255],
                                    get_line_width=3)
        farm_layer = pdk.Layer(type='ScatterplotLayer',
                               data=self.farm_df,
                               get_position=['x', 'y'],
                               get_radius=300,
                                           get_fill_color='color',
                                           get_line_color=[0, 0, 0],
                                           pickable=False,
                                           auto_highlight=True)
        hex_layer = pdk.Layer(type="H3HexagonLayer",
            data=self.suitability_df,
            pickable=True,
            filled=True,
            extruded=False,
            opacity=0.5,
            get_hexagon="he7",
            get_fill_color ='[0, 0, 255*Value, 255]',
            auto_highlight=True)
        
        boundary_layer = pdk.Layer(
            "GeoJsonLayer",
            data=self.boundary,
            stroked=True, 
            filled=False,  
            getLineColor = [128,128,128],
            getLineWidth= 80)

        self.digester_df['name'] = self.digester_df.index.astype(str)
        digester_label_layer = pdk.Layer(
            "TextLayer",
            self.digester_df,
            pickable=True,
            get_position=['x', 'y'],
            get_text="name",
            get_size=18,
            get_color=[255,255,255],
            get_angle=0,
            get_text_anchor=String("middle"),
            get_alignment_baseline=String("center"))
        
        view_state=pdk.ViewState(
            latitude=self.farm_df['y'].mean(),
            longitude=self.farm_df['x'].mean(),
            zoom=9,
            )
        TOOLTIP_TEXT = {
            "html": "Manure: {material_quantity} ton/yr <br /> From: farm #<span style='color:white; font-weight:bold;'>{farm_number}</span> <br /> To: digester site #<span style='color:white; font-weight:bold;'>{digester_number}</span>"
        }
        deck = pdk.Deck(
            layers=[hex_layer, farm_layer, digester_layer, digester_label_layer, boundary_layer],
            initial_view_state=view_state, 
            map_style= 
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

class ModelPreparer:
    def __init__(self, loi, _h3_gdf, _farm_gdf):
        self.loi = loi
        self._h3_gdf = _h3_gdf
        self._farm_gdf = _farm_gdf

    def prepare_model_input(self):
        # Ensure the 'hex9' column exists in the '_h3_gdf' DataFrame
        if 'hex9' not in self._h3_gdf.columns:
            raise ValueError("The '_h3_gdf' DataFrame does not contain a 'hex9' column.")

        # Ensure the 'loi' DataFrame has the correct structure
        if not isinstance(self.loi, pd.DataFrame) or self.loi.shape[1] != 2:
            raise ValueError("The 'loi' object must be a DataFrame with two columns.")

        # Use the DataFrame's index for the 'isin' operation
        loi_gdf = self._h3_gdf[self._h3_gdf['hex9'].isin(self.loi.index)]
        loi_gdf.index = range(1, len(loi_gdf) + 1) # Reset index to start with 1
        C, plant = calculate_od_matrix(self._farm_gdf, loi_gdf, cost_per_km=0.69)

        Plant_all = ['All'] + plant # add "ALL" to the list of candidate sites as input labels for customizing which sites to include in analysis
        color_mapping = {label: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for label in loi_gdf.index}
        loi_gdf['color'] = loi_gdf.index.map(color_mapping)

        d, f = assign_capacity_capex(plant) # random M and f generator for the time being

        return loi_gdf, C, plant, Plant_all, d, f

# Load session data
def session_load():
    # Create an instance of DataLoader
    data_loader = DataLoader(FOLDER_PATH)

    # Now you can call load_data method
    boundary = data_loader.load_data('./app_data/twente_4326.geojson', 'gdf')
    h3_gdf = data_loader.load_data('./app_data/h3_geometry.shp', 'gdf')
    farm_gdf = data_loader.load_data("./app_data/farm.shp", 'gdf')
    J, M  = data_loader.load_all_data()
    farm = data_loader.load_data("./farm/farm_mock.csv", 'csv')
    hex_df = data_loader.load_data('./hex/hex_df2.csv', 'csv')
    return {'boundary': boundary, 'h3_gdf': h3_gdf, 'farm_gdf': farm_gdf, 'M': M, 'J': J, 'farm': farm, 'hex_df': hex_df}

# Perform initial setup
def perform_initial_setup(page_2_space):
    data_name = ['boundary', 'h3_gdf', 'farm_gdf', 'M', 'J', 'farm', 'hex_df']
    missing_keys = [key for key in data_name if key not in page_2_space.keys()]
    if missing_keys:
        loaded_data = session_load()
        for key, value in loaded_data.items():
            page_2_space[key] = value
    if 'target' not in page_2_space:
        page_2_space['target'] = 0  # Set a default value, adjust as needed

# Main content
def main_content(page_2_space):
    boundary = page_2_space.get('boundary', None)
    J = page_2_space.get('J', None)  # Replace None with an appropriate default
    farm = page_2_space.get('farm', None)
    hex_df = page_2_space.get('hex_df', None)
    M = page_2_space.get('M', None)
    target = page_2_space.get('target', None)
    h3_gdf = page_2_space.get('h3_gdf', None)
    farm_gdf = page_2_space.get('farm_gdf', None)
    st.write(st.session_state.loi)

    model_preparer = ModelPreparer(st.session_state.loi, h3_gdf, farm_gdf)
    loi_gdf, C, plant, Plant_all, d, f = model_preparer.prepare_model_input()

    map_initializer = MapInitializer(loi_gdf, farm, hex_df, boundary)
    deck = map_initializer.initialize_map()

    with st.sidebar:
        target = (st.slider(':dart: **Manure Utilization Target (%):**', min_value=0, max_value=100,step=10)/ 100) # Define manure use goal (mu)

        with st.container():
            st.write("**Map Layers**")
            show_farm = st.sidebar.checkbox('Farms', value=True)
            show_digester = st.sidebar.checkbox('Digesters', value=True)
            show_suitability = st.sidebar.checkbox('Suitability', value=False)

        st.markdown("")
        st.markdown("")
        st.markdown("")
        with st.expander("Click to learn more about this dashboard"):
            st.markdown(f"""
            Introduce Bioze...
            *Updated on {str(TODAY)}.*  
            """)

    deck.layers[0].visible = show_suitability
    deck.layers[1].visible = show_farm
    deck.layers[2].visible = show_digester

    with st.expander(':white_check_mark: Customize Site Selection'):
        with st.form('select_plant'):
            I = st.multiselect("Select specific sites to include in the analysis. By default, all sites are included.", Plant_all)
            if "All" in I or not I:
                I = plant
            submit_select_loi = st.form_submit_button("Submit")

    if submit_select_loi and page_2_space['target'] == 0:
        deck = MapInitializer.update_digester_layer_color(loi_gdf, I, deck)

    if submit_select_loi or page_2_space['target'] != target:
        with st.spinner('Running the model...'):
            page_2_space['target'] = target # Update the session state with the new target value
            d = MapInitializer.filter_Plant(d, I)
            f = MapInitializer.filter_Plant(f, I)
            C = {(i, j): value for (i, j), value in C.items() if i in I}

            m, processed_manure = flp_scip(I, J, d, M, f, C, target)
            m.optimize()
            total_cost, assignment_decision, used_capacity_df = flp_get_result(m, I, J, d, C)
            total_biogas = processed_manure * 20 # 1 tonne manure yields around 20m³ biogas
            methane_saving = total_biogas*0.6 # methane content of biogas is assumed 60%

            col1, col2, col3 = st.columns(3)
            col1.metric(label="Total Cost over Lifetime (12 yr)", value="€{:,.2f}M".format(sum(total_cost['Value']) / 1000000))
            col1.metric(label="Total Manure Processed", value="{:,.0f} t/yr".format(processed_manure))
            col1.metric(label="Total Biogas Yield Potential", value="{:,.0f}M m³/yr".format(total_biogas/ 1000000))
            with col3:
                st.markdown("Digester Capacity Utilization Rate")
                st.bar_chart(used_capacity_df)

            deck = MapInitializer.update_digester_layer_color(loi_gdf, I, deck)
            deck = MapInitializer.update_farm_layer_color(farm, loi_gdf, assignment_decision, deck)
            deck = MapInitializer.update_map(farm, loi_gdf, assignment_decision, deck)

    st.pydeck_chart(deck, use_container_width=True)

# Main function
def main():
    st.markdown("### Fase 2: Beleidsverkenner")
    st.markdown(
        "Op onderstaande kaart ziet u waar uw kandidaat-locaties uit **Fase 1** en de boerderijen in de omgeving zich bevinden."
        " Door mest van lokale boerderijen te gebruiken, kunnen we biogas produceren ter vervanging van aardgas, waardoor duurzame energie wordt bevorderd en de uitstoot van broeikasgassen door mest wordt voorkomen. "
        " Onderzoek de beste locaties om grote <placeholder> te bouwen op basis van verschillende beleidsdoelen met betrekking tot de hoeveelheid mest bestemd voor de productie van biogas."
    )
    st.markdown("")
    st.markdown(":dart:"
        " Bepaal hoeveel van de mest in de regio u wilt gebruiken voor de productie van biogas en geef die hoeveelheid aan met de schuifregelaar **'Mestgebruiksdoelstelling (%)'**. "
        " De tool vindt de meest strategische locaties om grote <placeholder> te bouwen om uw doel te bereiken."
    )
    st.markdown("")
    st.markdown(":white_check_mark:"
        " U kunt bepalen welke kandidaat-sites in de analyse worden opgenomen door ze te selecteren in **'Siteselectie aanpassen'**. Standaard worden alle sites meegenomen in de analyse."
    )
    st.markdown("")
    with st.expander("**Hoe de kaart te lezen :mag_right:**"):
        st.markdown("Boerderijen - :black_circle:")
        st.markdown("Kandidaat-<placeholder>ites - :rainbow[Gekleurde] and numbered markers")
        st.markdown("Toewijzing van boerderijen aan vergistingslocaties - **:green[groen]** en **:red[rood]** bogen")
        st.markdown("Opmerking: De kleur van boerderijen verandert in de kleur van de vergistingslocaties waaraan ze in de oplossing zijn toegewezen. Als de boerderijen worden uitgesloten van de oplossing, blijven ze zwart.")
    st.markdown("")
    st.divider()
    st.markdown("")

    if 'page_2' not in st.session_state:
        st.session_state.page_2 = {}
    
    page_2_space = st.session_state.page_2

    if "loi" not in st.session_state or len(st.session_state.loi) == 0:
        st.warning("Oeps! Het lijkt erop dat je nog geen resultaten hebt opgeslagen. Ga eerst naar **Fase 1**.", icon="⚠️")
        if st.button("Visit **Phase 1**"):
            st.switch_page("pages/1_Fase_1_Geschiktheidsanalyse.py")
    else:
        with st.spinner("Running..."):
            perform_initial_setup(page_2_space) # Replace with your function to generate trial selection
            main_content(page_2_space)

if __name__ == "__main__":
    main()
