import pandas as pd
import geopandas as gpd
import pydeck as pdk
import streamlit as st
import numpy as np
from utils.cflp_function import *
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import networkx as nx
from pysal.lib import weights
from pysal.explore import esda
import plotly.figure_factory as ff


padding=0
st.set_page_config(page_title="Geschiktheids Analyse", layout="wide")


st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(4)
        {
            text-align: end;
        } 
    </style>
    """,
    unsafe_allow_html=True
)


### LOAD DATA ##################################
@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # get color for plotting
    return df

@st.cache_data
def load_gdf(gdf_path):
    gdf = gpd.read_file(gdf_path)
    return gdf

d_to_farm = load_data('./hex/h3_hexagons_mock_data_1.csv')
d_to_road = load_data('./hex/h3_hexagons_mock_data_2.csv')
d_to_industry = load_data('./hex/h3_hexagons_mock_data_3.csv')
d_to_nature = load_data('./hex/h3_hexagons_mock_data_4.csv')
d_to_water = load_data('./hex/h3_hexagons_mock_data_5.csv')
d_to_urban = load_data('./hex/h3_hexagons_mock_data_6.csv')
d_to_inlet = load_data('./hex/h3_hexagons_mock_data_7.csv')


### GENERATE COLORMAP ##################################
colormap = 'magma'
color_mapping = generate_color_mapping(colormap)

### FUZZIFY INPUT VARIABLES ##################################
@st.cache_data
def fuzzify(df, type="close", colormap_name=color_mapping):
    df_array = np.array(df['value'])
    if type == "close":
        fuzzified_array = np.maximum(0, 1 - (df_array - df_array.min()) / (df_array.max() - df_array.min()))
        df['fuzzy'] = fuzzified_array.round(3)
        # get_fill_color(df, "fuzzy", colormap_name)
        apply_color_mapping(df, 'fuzzy', color_mapping)
    elif type == "far":
        fuzzified_array = np.maximum(0, (df_array - df_array.min()) / (df_array.max() - df_array.min()))
        df['fuzzy'] = fuzzified_array.round(3)
        # get_fill_color(df, "fuzzy", colormap_name)
        apply_color_mapping(df, 'fuzzy', color_mapping)
    else:
        raise ValueError("Invalid type. Choose 'close' or 'far'.")
    return df

fuzzy_farm = fuzzify(d_to_farm, type='close')
fuzzy_road = fuzzify(d_to_road, type='close')
fuzzy_industry = fuzzify(d_to_industry, type='close')
fuzzy_nature = fuzzify(d_to_nature, type='far')
fuzzy_water = fuzzify(d_to_water, type='far')
fuzzy_urban = fuzzify(d_to_urban, type='far')
fuzzy_inlet = fuzzify(d_to_inlet, type='close')

all_arrays = {'Farms': np.array(fuzzy_farm['fuzzy']), 
              'Road infrastructure': np.array(fuzzy_road['fuzzy']),
              'Urban and residential areas': np.array(fuzzy_urban['fuzzy']), 
              'Industrial areas': np.array(fuzzy_industry['fuzzy']), 
              'Nature': np.array(fuzzy_nature['fuzzy']),
              'Water Bodies': np.array(fuzzy_water['fuzzy']),
              'Gas Inlets': np.array(fuzzy_inlet['fuzzy'])}

### CREATE EMPTY LAYER ##################################

def create_empty_layer(d_to_farm):
    df_empty = d_to_farm[['hex9']]
    df_empty['color'] = '[0,0,0,0]'
    return df_empty

idx = load_gdf('./app_data/h3_indices_polygon.geojson')
idx = idx.set_index('hex9')

### UPDATE EMPTY DF ##################################
def update_layer(selected_variables, all_arrays, d_to_farm):
    if not selected_variables:
        return create_empty_layer(d_to_farm)
    
    # Extract the selected variables (array) from the dictionary
    selected_array_list = [all_arrays[key] for key in selected_variables]
    
    # METHOD 1 NP.MINIMUM
    # result_array = selected_array_list[0] 
    # for arr in selected_array_list[1:]:
    #     result_array = np.minimum(result_array, arr)
    
    # METHOD 2 AVERAGE
    result_array = np.mean(selected_array_list, axis=0)
    
    hex_df = create_empty_layer(d_to_farm)
    hex_df['fuzzy'] = result_array
    # get_fill_color(hex_df, 'fuzzy', colormap_name_suitability_map)
    apply_color_mapping(hex_df, 'fuzzy', color_mapping)
    hex_df['fuzzy'] = hex_df['fuzzy'].round(3)
    return hex_df

### FILTER POTENTIAL DIGESTER LOCATIONS ##################################
# def filter_loi(fuzzy_cut_off, fuzzy_df):
#     st.session_state.all_loi = fuzzy_df[(fuzzy_df['fuzzy'] >=fuzzy_cut_off[0]) & (fuzzy_df['fuzzy'] <= fuzzy_cut_off[1])]

def get_sites(fuzzy_df, w, g, idx):
    if 'fuzzy' in fuzzy_df.columns:
        fuzzy_df = fuzzy_df.set_index('hex9').reindex(idx.index)
        # 1. Compute loca moran's I
        lisa = esda.Moran_Local(fuzzy_df['fuzzy'], w, seed=42)
        # 2. Break observations into significant or not
        # fuzzy_df['significant'] = lisa.p_sim < 0.01
        # 3. Store the quadrant they belong to
        HH = fuzzy_df[(lisa.q == 1) & (lisa.p_sim < 0.01)].index.to_list()
        # Build sub graph that includes only the HH quadrant
        H = g.subgraph(HH)
        # Get sub components in the sub graphs
        subH = list(nx.connected_components(H))
        filter_subH = [component for component in subH if len(component) > 10]
        # Calculate eigenvector centrality for each connected component
        site_idx = []
        for component in filter_subH:
            # Create a subgraph for the current connected component
            subgraph = H.subgraph(component)
            # Calculate eigenvector centrality for a connected graph
            eigenvector_centrality = nx.eigenvector_centrality(subgraph, max_iter=1500)
            # Get the node index with the highest eigenvector centrality in that connected graph
            max_node_index = max(eigenvector_centrality, key=eigenvector_centrality.get)
            # Append the node index to a list
            site_idx.append(max_node_index)
        st.session_state.all_loi = fuzzy_df.loc[site_idx].reset_index()
    else:
        return None

### PLOT PYDECK MAPS ##################################
view_state = pdk.ViewState(longitude=6.747489560596507, latitude=52.316862707395394, zoom=8, bearing=0, pitch=0)

@st.cache_data
def generate_pydeck(df, view_state=view_state):
    return pdk.Deck(initial_view_state=view_state,
                    layers=[
                        pdk.Layer(
                            "H3HexagonLayer",
                            df,
                            pickable=True,
                            stroked=True,
                            filled=True,
                            extruded=False,
                            opacity=0.6,
                            get_hexagon="hex9",
                            get_fill_color ='color', 
                            # get_line_color=[255, 255, 255],
                            # line_width_min_pixels=1
                        ),
                    ],
                    tooltip={"text": "Suitability:" f"{{fuzzy}}"})

### CREATE VARIABLE LEGEND ##################################
@st.cache_data
def generate_colormap_legend(label_left='Far', label_right='Near', cmap=plt.get_cmap(colormap)):
    # Create Viridis colormap image
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    # Create Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(4, 0.5))
    ax.imshow(gradient, aspect='auto', cmap=cmap)
    ax.axis('off') 

    # Add labels 
    ax.text(-10, 0.5, label_left, verticalalignment='center', horizontalalignment='right', fontsize=12)
    ax.text(266, 0.5, label_right, verticalalignment='center', horizontalalignment='left', fontsize=12)

    # Save Matplotlib figure as PNG image
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    buffer.seek(0)
    image_png = buffer.getvalue()
    plt.close(fig)    # Close Matplotlib figure
    # Convert Matplotlib PNG image to Base64 string
    image_base64 = base64.b64encode(image_png).decode()

    # Create HTML content with image and labels
    legend_html = f'''
        <div style="width: 100%; height: 300px; overflow: auto; padding: 10px;">
            <img src="data:image/png;base64,{image_base64}" alt="Colorbar" style="max-width: 100%; max-height: 100%; height: auto; width: auto; display: block; margin-left: auto; margin-right: auto;">
        </div>
    '''
    return legend_html

variable_legend_html = generate_colormap_legend(label_left='Least Suitable (0)', label_right='Most Suitable (1)',)

### 
@st.cache_data
def get_layers(hex_df):
    hex_fuzzy = pdk.Layer(
        "H3HexagonLayer",
        hex_df.reset_index(),
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        opacity=0.6,
        get_hexagon="hex9",
        get_fill_color='color', 
                    # get_line_color=[255, 255, 255],
            # line_width_min_pixels=2
    )

    layers = [hex_fuzzy]
    return layers

###
@st.cache_data 
def plot_result(fig):
    if fig is not None:
        st.plotly_chart(fig, theme="streamlit")


### INITIALIZE SESSION STATE ##################################
def initialize_session_state(idx):
    if 'all_loi' not in st.session_state:
        st.session_state.all_loi = pd.DataFrame()
    if 'loi' not in st.session_state:
        st.session_state.loi = pd.DataFrame()
    if 'fig' not in st.session_state:
        st.session_state.fig = None
    if 'w' not in st.session_state: #and 'hex_df' not in st.session_state
        st.session_state.w = weights.Queen.from_dataframe(idx, use_index=True)
        # df = pd.DataFrame(index=idx.index)
        # df['color'] = '[0,0,0,0]'
        # st.session_state.hex_df = df
    if 'g' not in st.session_state:
        st.session_state.g = nx.read_graphml('./app_data/g.graphml')

### CREATE STREAMLIT ##################################
def main():
    initialize_session_state(idx)
    st.markdown("### Fase 1: Geschiktheidsanalyse - Identificeer kandidaatlocaties voor grootschalige vergister")
    st.markdown("")
    st.markdown(
        "Bekijk de onderstaande kaarten. Elke kaart vertegenwoordigt een vooraf geselecteerd criterium dat van cruciaal belang wordt geacht om te bepalen hoe geschikt een gebied is voor grote vergisters."
        "Elk gebied in de regio krijgt een geschiktheidsscore tussen 0 en 1, respectievelijk het minst en het meest geschikt."
        "Tip: Klik op het vraagtekenpictogram :grey_question: bovenaan elke kaart voor meer informatie."
    )
    st.markdown("")
    st.markdown("**Stap**:one:")
    st.markdown(
        "Identificeer kandidaat-gebieden die geschikt zijn voor het bouwen van grote vergisters door de criteria van uw interesse te selecteren en op **'Bouw Geschiktheidskaart'** te klikken. De tool geeft hieronder een nieuwe geschiktheidskaart weer door al uw geselecteerde criteria te combineren."
        " Het aantal kandidaat-locaties wordt weergegeven en de locaties zijn gemarkeerd **:groen[groen]** op de nieuwe geschiktheidskaart. Probeer verschillende combinaties van criteria totdat u tevreden bent."
    )
    st.markdown("**Stap**:two:")
    # st.markdown(
    #     "Selecteer vervolgens, op basis van uw nieuwe geschiktheidskaart, een bereik van geschiktheidsscores (bijvoorbeeld 0,8 - 1) om kandidaat-sites te filteren. **'Aantal kandidaatsites'** wordt bijgewerkt en kandidaatsites worden uitgelicht **:green[green]** op uw geschiktheidskaart. Herhaal stap 1 en 2 totdat u tevreden bent." 
    # )
    # st.markdown("**Stap**:three:")
    st.markdown("Zodra u tevreden bent met de lijst met kandidaat-sites, bent u klaar om door te gaan naar **Fase 2** van de tool. Klik op **'Resultaat opslaan'** en de tool begeleidt u naar de volgende fase.") #:red[Zorg ervoor dat het aantal kandidaat-sites niet groter is dan **15**].

    st.markdown("")
    st.markdown("")
    # Plotting suitability variables
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Boerderijen Locaties**", 
                    help="Geschiktheid voor het bouwen van grote vergisters, bepaald door de afstand tot locaties van grondstoffen. De geschiktheidsscore varieert van 0 (minst geschikt) tot 1 (meest geschikt). Hoe ***dichter*** bij de grondstoffen, hoe ***hoger*** de geschiktheid.")
        st.pydeck_chart(generate_pydeck(fuzzy_farm), use_container_width=True)
    with col1:
        st.markdown("**Wegen Infrastructuur**", 
                    help="Geschiktheid voor het bouwen van grote vergisters, afhankelijk van de afstand tot de wegeninfrastructuur. De geschiktheidsscore varieert van 0 (minst geschikt) tot 1 (meest geschikt). Hoe ***dichter*** bij wegen, hoe ***hoger*** de geschiktheid. De wegeninfrastructuur omvat alleen hoofdwegen.")
        st.pydeck_chart(generate_pydeck(fuzzy_road), use_container_width=True)
    with col1:
        st.markdown("**Water Lichamen**", 
                    help="Geschiktheid voor het bouwen van grote vergisters, afhankelijk van de afstand tot binnen- en zeewateren. De geschiktheidsscore varieert van 0 (minst geschikt) tot 1 (meest geschikt). Hoe ***verder*** verwijderd van waterlichamen, hoe ***hoger*** de geschiktheid.")
        st.pydeck_chart(generate_pydeck(fuzzy_water), use_container_width=True)
    with col2:
        st.markdown("**Industrie Gebieden**", help="Geschiktheid voor het bouwen van grote vergisters, bepaald door de afstand tot industriële gebieden, inclusief industriële en commerciële eenheden, havengebieden, mijnen, stortplaatsen en bouwplaatsen. De geschiktheidsscore varieert van 0 (minst geschikt) tot 1 (meest geschikt). Hoe ***dichter*** bij industriële gebieden, hoe ***hoger*** de geschiktheid.")
        st.pydeck_chart(generate_pydeck(fuzzy_industry), use_container_width=True)
    with col2:
        st.markdown("**Stedelijke en residentiele gebieden**", help="Geschiktheid voor het bouwen van grote vergisters, afhankelijk van de afstand tot stedelijke en residentiële gebieden. De geschiktheidsscore varieert van 0 (minst geschikt) tot 1 (meest geschikt). Hoe ***verder*** verwijderd van stedelijke en residentiële gebieden, hoe ***hoger*** de geschiktheid.")
        st.pydeck_chart(generate_pydeck(fuzzy_urban), use_container_width=True)
    with col3:
        st.markdown("**Natuur en bos**", help="Geschiktheid voor het lokaliseren van vergisters, het bouwen van grote vergisters, bepaald door de afstand tot natuur- en bosgebieden, waaronder ook graslanden, wetlands, stranden, duinen, zand en bossen. De geschiktheidsscore varieert van 0 (minst geschikt) tot 1 (meest geschikt). Hoe ***verder*** verwijderd van natuurgebieden en waterlichamen, hoe ***hoger*** de geschiktheid.")
        st.pydeck_chart(generate_pydeck(fuzzy_nature), use_container_width=True)
    with col3:
        st.markdown("**Gasinlaatpunten**", 
                    help="Geschiktheid voor het bouwen van grote vergisters, bepaald door de afstand tot willekeurig gegenereerde gasinlaatpunten. De geschiktheidsscore varieert van 0 (minst geschikt) tot 1 (meest geschikt). Hoe ***dichter*** bij de inlaten, hoe ***hoger*** de geschiktheid. Momenteel worden willekeurig gegenereerde gegevenspunten gebruikt vanwege een gebrek aan gegevens, en deze zouden idealiter moeten worden vervangen door echte gegevens van gasinjectiestations of andere representaties van inlaten naar gasnetten.")
        st.pydeck_chart(generate_pydeck(fuzzy_inlet), use_container_width=True)
    with col3:
        st.markdown(variable_legend_html, unsafe_allow_html=True)
   
    "---"
    st.markdown("")

    # Suitability analysis section 
    with st.sidebar.form("suitability_analysis_form"):
        selected_variables = st.multiselect(":one: Select Criteria", list(all_arrays.keys()))
        submit_button = st.form_submit_button("Bouw Geschiktheidskaart")

    if submit_button and not selected_variables:
        st.warning("Geen variabelen geselecteerd.")
        pass
    
    if submit_button:
        hex_df = update_layer(selected_variables, all_arrays, d_to_farm)
        get_sites(hex_df, st.session_state.w, st.session_state.g, idx)
        fig = ff.create_distplot([st.session_state.all_loi['fuzzy'].tolist()], ['Distribution'], show_hist=False, bin_size=0.02)
        fig.update_layout(autosize=True,
                            width=600,
                            height=400)
        st.session_state.fig = fig

    st.markdown("### **Geschiktheidskaart**")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Aantal kandidaatsites: {len(st.session_state['all_loi'])}**")
    # with col3:
    if st.sidebar.button(':two: Resultaat opslaan en fase 2 betreden', help="Klik om de huidige gefilterde locaties op te slaan voor verder onderzoek in ***Fase 2: Beleidsverkenner***."):
        # st.session_state.loi = st.session_state.all_loi.nlargest(12, 'fuzzy')
        st.session_state.loi = st.session_state.all_loi
        st.switch_page("pages/2_Phase_2_Policy_Explorer.py")

    hex_df = update_layer(selected_variables, all_arrays, d_to_farm)
    layers = get_layers(hex_df)


    plot_result(st.session_state.fig)

    loi_plot = pdk.Layer(
        "H3HexagonLayer",
        st.session_state.all_loi,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        opacity=0.6,
        get_hexagon="hex9",
        get_fill_color=[0, 0, 0, 0], 
        get_line_color=[0, 255, 0],
        line_width_min_pixels=2)
    layers.append(loi_plot)
    
    deck = pdk.Deck(layers=layers, initial_view_state=view_state, tooltip={"text": "Geschiktheid: {fuzzy}"})
    st.pydeck_chart(deck, use_container_width=True)
    st.markdown(variable_legend_html, unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()

# # import sys
# import leafmap.foliumap as leafmap

# # sys.path

# raster_file = '/Users/wenyuc/Desktop/UT/data/raster/fuzzy_complete_3857.tif'

# m = leafmap.Map()
# m.add_basemap()
# m.add_raster(raster_file, cmap="viridis", layer_name="Raster Layer")

# m.to_streamlit()

