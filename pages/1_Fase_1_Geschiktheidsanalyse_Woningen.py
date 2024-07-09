# Importing standard libraries
from io import BytesIO

# Importing third-party libraries
import base64
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import pydeck as pdk
import streamlit as st
from pysal.explore import esda
from pysal.lib import weights
from libpysal.weights import w_subset

# Importing local application/library specific imports
from utils.cflp_function import *

#####

# Constants
PADDING = 0
COLORMAP = 'magma'
VIEW_STATE = pdk.ViewState(longitude=4.390, latitude=51.891, zoom=8, bearing=0, pitch=0)
DATA_PATHS = {
    # 'farm': './hex/aantal_meergezins_woningen.csv',
    'farm': './standalone/cbs_2022_h3.csv',
    'road': './hex/aantal_huurwoningen_in_bezit_woningcorporaties.csv',
    'industry': './hex/aantal_inwoners.csv',
    'nature': './hex/aantal_meergezins_woningen.csv',
    'water': './hex/aantal_niet_bewoonde_woningen.csv',
    'urban': './hex/aantal_woningen_bouwjaar_voor_1945.csv',
    'inlet': './hex/aantal_woningen.csv',
}

# Generating colormap
color_mapping = generate_color_mapping(COLORMAP)

# Setting page configuration
st.set_page_config(page_title="Geschiktheids Analyse", layout="wide")

# Setting markdown
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

#####

def load_data(csv_path):
    """Function to load data from a CSV file."""
    try:
        data = pd.read_csv(csv_path)
        if data.empty:
            raise ValueError(f"File {csv_path} is empty.")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File {csv_path} not found.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"No data in file {csv_path}.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file {csv_path}: {str(e)}")

def load_gdf(gdf_path):
    """Function to load a GeoDataFrame from a file."""
    try:
        return gpd.read_file(gdf_path).set_index('hex9')
    except FileNotFoundError:
        raise FileNotFoundError(f"File {gdf_path} not found.")

# Loading dataframes
d_to_farm = load_data(DATA_PATHS['farm'])
d_to_road = load_data(DATA_PATHS['road'])
d_to_industry = load_data(DATA_PATHS['industry'])
d_to_nature = load_data(DATA_PATHS['nature'])
d_to_water = load_data(DATA_PATHS['water'])
d_to_urban = load_data(DATA_PATHS['urban'])
d_to_inlet = load_data(DATA_PATHS['inlet'])

# Checking if data is loaded correctly
if d_to_farm is None or d_to_road is None or d_to_industry is None or d_to_nature is None or d_to_water is None or d_to_urban is None or d_to_inlet is None:
    st.write("Error loading data.")
    exit()

#####

# Fuzzify input variables
@st.cache_data
def fuzzify(df, type="close", colormap_name=color_mapping):
    df_array = np.array(df['value'])
    fuzzified_array = np.maximum(0, 1 - (df_array - df_array.min()) / (df_array.max() - df_array.min())) if type == "close" else np.maximum(0, (df_array - df_array.min()) / (df_array.max() - df_array.min()))
    df['fuzzy'] = fuzzified_array.round(3)
    apply_color_mapping(df, 'fuzzy', color_mapping)
    return df

# Fuzzifying dataframes
fuzzy_farm = fuzzify(d_to_farm, type='close')
fuzzy_road = fuzzify(d_to_road, type='close')
fuzzy_industry = fuzzify(d_to_industry, type='close')
fuzzy_nature = fuzzify(d_to_nature, type='far')
fuzzy_water = fuzzify(d_to_water, type='far')
fuzzy_urban = fuzzify(d_to_urban, type='far')
fuzzy_inlet = fuzzify(d_to_inlet, type='close')
# fuzzy_pm25 = fuzzify(d_to_pm25, type='close')  # or type='far',

# All arrays
all_arrays = {'Aantal eenpersoonshuishoudens': np.array(fuzzy_farm['fuzzy']), 
              'Aantal meergezinswoningen': np.array(fuzzy_road['fuzzy']),
              'Aantal woningen bouwjaar voor 1945': np.array(fuzzy_urban['fuzzy']), 
              'Aantal niet bewoonde woningen': np.array(fuzzy_industry['fuzzy']), 
              'Aantal woningen': np.array(fuzzy_nature['fuzzy']),
              'Aantal inwoners': np.array(fuzzy_water['fuzzy']),
              'Aantal huurwoningen in bezit van woningcooperaties': np.array(fuzzy_inlet['fuzzy']),
            #   'Pm25': np.array(fuzzy_pm25['fuzzy'])
            }

#####

# Create empty layer
def create_empty_layer(d_to_farm):
    df_empty = d_to_farm[['hex9']]
    df_empty['color'] = '[0,0,0,0]'
    return df_empty

# Update empty df
def update_layer(selected_variables, all_arrays, d_to_farm):
    if not selected_variables:
        return create_empty_layer(d_to_farm)
    
    selected_array_list = [all_arrays[key] for key in selected_variables]
    result_array = np.mean(selected_array_list, axis=0)
    hex_df = create_empty_layer(d_to_farm)
    hex_df['fuzzy'] = result_array
    apply_color_mapping(hex_df, 'fuzzy', color_mapping)
    hex_df['fuzzy'] = hex_df['fuzzy'].round(3)
    return hex_df



def get_sites(df, w, g, idx, score_column: str = 'fuzzy', seed: int = 42) -> pd.DataFrame:
    """
    Analyzes potential digester locations based on suitability scores and spatial factors.

    Args:
        df (pd.DataFrame): DataFrame containing a column with suitability scores.
        w (pysal.W): Spatial weights object for spatial analysis.
        g (networkx.Graph): Graph object representing the network.
        idx (pd.DataFrame): DataFrame containing potential digester locations (indexed by "hex9").
        score_column (str, optional): Name of the column containing suitability scores. Defaults to 'fuzzy'.
        seed (int, optional): Seed for the random number generator. Defaults to 42.

    Returns:
        pd.DataFrame: DataFrame containing the most central locations within significant suitability clusters.

    Raises:
        ValueError: If required columns are missing, data quality issues are detected, or errors occur during spatial analysis.
    """

    # Input Validation
    if score_column not in df.columns:
        raise ValueError(f"The DataFrame does not contain a '{score_column}' column.")
    if not isinstance(idx, pd.DataFrame) or idx.index.name != 'hex9':
        raise ValueError("The idx should be a pandas DataFrame with 'hex9' as index.")

    # Data Cleaning and Preprocessing
    df.dropna(subset=[score_column], inplace=True)  # Handle missing values in score column
    df = df.drop_duplicates(subset='hex9').set_index('hex9')  # Ensure unique hex9 and set as index
    unique_idx = df.index.intersection(idx.index)
    if unique_idx.empty:
        raise ValueError("No overlapping 'hex9' values found between df and idx. Check data quality and 'hex9' formatting.")
    df = df.loc[unique_idx]  # Retain data with matching hex9 values

    if 'geometry' in df.columns:
        df['geometry'] = gpd.GeoSeries(df['geometry']).to_shapely()  # Convert geometry to shapely format (if applicable)

    w_subset_result = w_subset(w, df.index)  # Create sub-weights object based on df index

    # Spatial Analysis
    try:
        
        lisa = esda.Moran_Local(df[score_column], w_subset_result, seed=seed)
        significant_locations = df[(lisa.q == 1) & (lisa.p_sim < 0.01)].index.to_list()
    except ValueError as e:
        raise ValueError(f"Error computing Moran's I: {str(e)}") from e

    # Network Analysis (Identify central locations within significant clusters - Optional)
    H = g.subgraph(significant_locations)
    H_undirected = nx.Graph(H.to_undirected())
    filtered_components = [component for component in nx.connected_components(H_undirected) if len(component) > 2]


    return df[df.index.isin(significant_locations)]  # Return DataFrame with significant locations







#####

# Generate pydeck
@st.cache_resource
def generate_pydeck(df, view_state=VIEW_STATE):
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
                        ),
                    ],
                    tooltip={"text": "Geschiktheid:" f"{{fuzzy}}"}
    )

# Create variable legend
@st.cache_data
def generate_colormap_legend(label_left='Far', label_right='Near', cmap=plt.get_cmap(COLORMAP)):
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    fig, ax = plt.subplots(figsize=(4, 0.5))
    ax.imshow(gradient, aspect='auto', cmap=cmap)
    ax.axis('off')
    ax.text(-10, 0.5, label_left, verticalalignment='center', horizontalalignment='right', fontsize=12)
    ax.text(266, 0.5, label_right, verticalalignment='center', horizontalalignment='left', fontsize=12)
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    buffer.seek(0)
    image_png = buffer.getvalue()
    plt.close(fig)
    image_base64 = base64.b64encode(image_png).decode()
    legend_html = f''' <div style="width: 100%; height: 300px; overflow: auto; padding: 10px;"> <img src="data:image/png;base64,{image_base64}" alt="Colorbar" style="max-width: 100%; max-height: 100%; height: auto; width: auto; display: block; margin-left: auto; margin-right: auto;"> </div> '''
    return legend_html

variable_legend_html = generate_colormap_legend(label_left='Minst Geschikt (0)', label_right='Meest Geschikt (1)',)

# Get layers
@st.cache_data
def get_layers(hex_df):
    hex_fuzzy = pdk.Layer(
        "H3HexagonLayer",
        hex_df.reset_index(),
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        opacity=0.1,
        get_hexagon="hex9",
        get_fill_color='color', 
    )

    layers = [hex_fuzzy]
    return layers

# Plot result
def plot_result(fig):
    if fig is not None:
        st.plotly_chart(fig, theme="streamlit")

#####

### CREATE STREAMLIT ##
def main(idx):
    initialize_session_state(idx)
    display_intro_text()
    plot_suitability_variables()
    perform_suitability_analysis()


# Initialize session state | STAP 1
def initialize_session_state(idx):
    if 'all_loi' not in st.session_state:
        st.session_state.all_loi = pd.DataFrame()
    if 'loi' not in st.session_state:
        st.session_state.loi = pd.DataFrame()
    if 'fig' not in st.session_state:
        st.session_state.fig = None
    if 'w' not in st.session_state:
        st.session_state.w = weights.Queen.from_dataframe(idx, use_index=True)
        # st.write(st.session_state.w)
    if 'g' not in st.session_state:
        st.session_state.g = nx.read_graphml('./osm_network/G.graphml')


### STAP 2
def display_intro_text():
    st.markdown("### Fase 1: Geschiktheidsanalyse - Potentiële Locaties voor Nieuwbouw Projecten")
    st.markdown(
        "Bekijk de onderstaande kaarten, elk vertegenwoordigt een vooraf geselecteerd criterium dat essentieel wordt geacht voor het bepalen van de geschiktheid van een gebied voor nieuwbouw projecten.  "
        " Elk gebied in de regio krijgt een geschiktheidsscore tussen 0 en 1, waarbij 0 het minst geschikt en 1 het meest geschikt vertegenwoordigt.  "
        "<br>Tip: Klik op het vraagtekenpictogram :grey_question: boven elke kaart voor meer informatie.",
        unsafe_allow_html=True
    )


### STAP 3
def plot_suitability_variables():
    col1, col2, col3 = st.columns(3)
    plot_variable(col1, "Aantal eenpersoonshuishoudens", fuzzy_farm, "Hoe dichter bij voedingsstoffen, hoe geschikter.")
    plot_variable(col1, "Aantal huurwoningen in bezit van woningcooperaties", fuzzy_road, "Hoe dichter bij wegen, hoe geschikter.")
    plot_variable(col1, "Aantal inwoners", fuzzy_water, "Hoe verder weg van waterlichamen, hoe geschikter.")
    plot_variable(col2, "Aantal meergezinswoningen", fuzzy_industry, "Hoe dichter bij industriële gebieden, hoe geschikter.")
    plot_variable(col2, "Aantal niet bewoonde woningen", fuzzy_urban, "Hoe verder weg van stedelijke en woongebieden, hoe geschikter.")
    plot_variable(col3, "Aantal woningen bouwjaar voor 1945", fuzzy_nature, "Hoe verder weg van natuurgebieden en waterlichamen, hoe geschikter.")
    plot_variable(col3, "Aantal woningen", fuzzy_inlet, "Hoe dichter bij inlaten, hoe geschikter.")
    # plot_variable(col3, "Pm25", fuzzy_pm25, "The closer to pm25 the higher the suitability.")
    col3.markdown(variable_legend_html, unsafe_allow_html=True)

def plot_variable(column, title, data, help_text):
    # st.write(data)
    column.markdown(f"**{title}**", help=help_text)
    column.pydeck_chart(generate_pydeck(data), use_container_width=True)


### STAP 4
def perform_suitability_analysis():
    """
        Performs suitability analysis based on selected criteria and visualizes results.
    """
    with st.sidebar.form("suitability_analysis_form"):
        selected_variables = st.multiselect(":one: Selecteer Criteria", list(all_arrays.keys()))
        submit_button = st.form_submit_button("Bouw Geschiktheidskaart")

    if submit_button and not selected_variables:
        st.warning("Geen variabele geselecteerd.")
        return

    if submit_button:
        hex_df = update_layer(selected_variables, all_arrays, d_to_farm)

        # Improved data handling in get_sites
        all_loi = get_sites(hex_df, st.session_state.w, st.session_state.g, idx)
        if all_loi is not None and not all_loi.empty:
            st.session_state.all_loi = all_loi
            fig = ff.create_distplot([all_loi['fuzzy'].tolist()], ['Distribution'], show_hist=False, bin_size=0.02)
            fig.update_layout(autosize=True, width=600, height=400)
            st.session_state.fig = fig
        else:
            st.write("No suitable locations identified based on selected criteria.")

    st.markdown("### **Geschiktheidskaart**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Aantal Potentiële Locaties: {len(st.session_state['all_loi'])}**")

    if st.sidebar.button(':two: Resultaat Opslaan & Ga naar Fase 2', help="Klik om de huidige gefilterde locaties op te slaan voor verder onderzoek in ***Fase 2: Beleid Verkenner***."):
        st.session_state.loi = st.session_state.all_loi
        st.switch_page("pages/2_Fase_2_Beleidsverkenner.py")

    hex_df = update_layer(selected_variables, all_arrays, d_to_farm)
    layers = get_layers(hex_df)
    plot_result(st.session_state.fig)
    
    loi_plot = pdk.Layer(
        "H3HexagonLayer",
        st.session_state.all_loi.reset_index(),
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        opacity=0.7,
        get_hexagon="hex9",
        get_fill_color=[0, 255, 0], 
        get_line_color=[0, 255, 0],
        line_width_min_pixels=2)

    layers.append(loi_plot)
    
    deck = pdk.Deck(layers=layers, initial_view_state=VIEW_STATE, tooltip={"text": "Suitability: {fuzzy}"})
    st.pydeck_chart(deck, use_container_width=True)
    st.markdown(variable_legend_html, unsafe_allow_html=True)



# Run the Streamlit app
if __name__ == "__main__":
    idx = load_gdf('./app_data/h3_pzh_polygons.shp')
    main(idx)
