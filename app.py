import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np
from cflp_function import *
import matplotlib.pyplot as plt
from io import BytesIO
import base64

padding=0
st.set_page_config(page_title="Bioze Mapping Tool - Suitability Analysis", layout="wide")

# st.markdown(
#     """
#     <style>
#     .small-font {
#         font-size:12px;
#         font-style: italic;
#         color: #b1a7a6;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

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

d_to_farm = load_data('./hex/d_to_farm_hex_complete.csv')
d_to_road = load_data('./hex/d_to_road_hex_complete.csv')
d_to_industry = load_data('./hex/proximity_to_industry_hex_complete.csv')
d_to_nature = load_data('./hex/proximity_to_nature_hex_complete.csv')
d_to_urban = load_data('./hex/proximity_to_urban_hex_complete.csv')


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
fuzzy_urban = fuzzify(d_to_urban, type='far')

all_arrays = {'Farms': np.array(fuzzy_farm['fuzzy']), 
              'Road infrastructure': np.array(fuzzy_road['fuzzy']),
              'Urban and residential areas': np.array(fuzzy_urban['fuzzy']), 
              'Industrial areas': np.array(fuzzy_industry['fuzzy']), 
              'Nature and water bodies': np.array(fuzzy_nature['fuzzy'])}

### CREATE EMPTY LAYER ##################################
def create_empty_layer(d_to_farm):
    df_empty = d_to_farm[['hex9']]
    df_empty['color'] = '[0,0,0,0]'
    return df_empty

### UPDATE EMPTY DF ##################################
def update_layer(selected_variables, all_arrays, d_to_farm):
    if not selected_variables:
        return create_empty_layer(d_to_farm)
    
    # Extract the selected variables (array) from the dictionary
    selected_array_list = [all_arrays[key] for key in selected_variables]
    
    result_array = selected_array_list[0]
    for arr in selected_array_list[1:]:
        result_array = np.minimum(result_array, arr)
    
    hex_df = create_empty_layer(d_to_farm)
    hex_df['fuzzy'] = result_array
    # get_fill_color(hex_df, 'fuzzy', colormap_name_suitability_map)
    apply_color_mapping(hex_df, 'fuzzy', color_mapping)
    hex_df['fuzzy'] = hex_df['fuzzy'].round(3)
    return hex_df

### FILTER POTENTIAL DIGESTER LOCATIONS ##################################
# def filter_loi(fuzzy_cut_off, fuzzy_df):
#     loi = fuzzy_df[(fuzzy_df['fuzzy'] >= fuzzy_cut_off[0]) & (fuzzy_df['fuzzy'] <= fuzzy_cut_off[1])]
#     return loi

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
# suitability_map_legend_html = generate_colormap_legend(label_left='Most Suitable', label_right='Least Suitable', cmap=plt.cm.plasma)

### 

def filter_loi(fuzzy_cut_off, fuzzy_df):
    st.session_state.loi = fuzzy_df[(fuzzy_df['fuzzy'] >=fuzzy_cut_off[0]) & (fuzzy_df['fuzzy'] <= fuzzy_cut_off[1])]

@st.cache_data
def get_layers(hex_df):
    hex_fuzzy = pdk.Layer(
        "H3HexagonLayer",
        hex_df,
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



### INITIALIZE SESSION STATE ##################################
def initialize_session_state():
    if 'loi' not in st.session_state:
        st.session_state.loi = pd.DataFrame()


### CREATE STREAMLIT ##################################
def main():
    initialize_session_state()
    st.markdown("### Biogas Digester Site: Suitability Analysis")
    st.markdown(
        "This analysis identifies potential sites for biogas digesters based on five key criteria: "
        "distance to major roads, farms, industrial areas, and nature and water bodies."
    )
    st.markdown(
        "You have the flexibility to select specific criteria for the suitability analysis. "
        "The resulting suitability map will be displayed below for your exploration."
    )
    st.markdown("")
    st.markdown("")
    # Plotting suitability variables
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Farms/Feedstock Locations**", help="Suitability for locating digesters determined by distance to feedstock locations.")
        st.pydeck_chart(generate_pydeck(fuzzy_farm), use_container_width=True)
    with col1:
        st.markdown("**Road Infrastructure**", help="Suitability for locating digesters determined by distance to road infrastructure.")
        st.pydeck_chart(generate_pydeck(fuzzy_road), use_container_width=True)
    with col2:
        st.markdown("**Industrial Areas**", help="Suitability for locating digesters determined by distance to industrial areas.")
        st.pydeck_chart(generate_pydeck(fuzzy_industry), use_container_width=True)
    with col2:
        st.markdown("**Urban and Residential Areas**", help="Suitability for locating digesters determined by distance to urban and residential areas.")
        st.pydeck_chart(generate_pydeck(fuzzy_urban), use_container_width=True)
    with col3:
        st.markdown("**Nature and Water Bodies**", help="Suitability for locating digesters determined by distance to nature and water bodies, including canals etc...")
        st.pydeck_chart(generate_pydeck(fuzzy_nature), use_container_width=True)
    with col3:
        st.markdown(variable_legend_html, unsafe_allow_html=True)
   
    st.markdown("")
    "---"
    st.markdown("")

    # Suitability analysis section 
    with st.sidebar.form("suitability_analysis_form"):
        selected_variables = st.multiselect("Select criteria", list(all_arrays.keys()))
        submit_button = st.form_submit_button("Build Suitability Map")

    if submit_button and not selected_variables:
        st.warning("No variable selected.")
        return
    
    st.markdown("### **Suitability Map**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Number of Potential Locations:{len(st.session_state['loi'])}**")
    with col3:
        if st.button('Save Result'):
            st.write("Saved Successfully!")

    hex_df = update_layer(selected_variables, all_arrays, d_to_farm)
    layers = get_layers(hex_df)


    # Filtering location of interest (loi) section
    with st.sidebar.form("select_loi"):
        st.slider('Filter potential digester sites with suitability score', 0.0, 1.0, (0.8, 1.0), step=0.01, key='myslider')
        # st.form_submit_button("Filter", on_click=filter_loi, args=(st.session_state.myslider, hex_df))
        on_click_filter_loi = lambda: filter_loi(st.session_state.myslider, hex_df)
        st.form_submit_button("Filter", on_click=on_click_filter_loi)

    loi_plot = pdk.Layer(
        "H3HexagonLayer",
        st.session_state.loi,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        opacity=0.6,
        get_hexagon="hex9",
        get_fill_color=[0, 0, 0, 0], 
        get_line_color=[255, 0, 0],
        line_width_min_pixels=1)
    layers.append(loi_plot)
    
    deck = pdk.Deck(layers=layers, initial_view_state=view_state, tooltip={"text": "Suitability: {fuzzy}"})
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

