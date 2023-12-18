import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np
from cflp_function import get_fill_color

padding = 0

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .small-font {
        font-size:12px;
        font-style: italic;
        color: #b1a7a6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

colormap_name = 'viridis'

### LOAD DATA ##################################
@st.cache_data
def load_data(csv_path, colormap_name):
    df = pd.read_csv(csv_path)
    # get color for plotting
    get_fill_color(df, "value", colormap_name)
    return df

d_to_farm = load_data('./hex/d_to_farm_hex_complete.csv', colormap_name)
d_to_road = load_data('./hex/d_to_road_hex_complete.csv', colormap_name)
d_to_industry = load_data('./hex/proximity_to_industry_hex_complete.csv', colormap_name)
d_to_nature = load_data('./hex/proximity_to_nature_hex_complete.csv', colormap_name)

# get_fill_color(d_to_farm, "value", colormap_name)
# get_fill_color(d_to_road, "value", colormap_name)
# get_fill_color(d_to_industry, "value", colormap_name)
# get_fill_color(d_to_nature, "value", colormap_name)

### FUZZIFY INPUT VARIABLES ##################################
@st.cache_data
def fuzzify(df, type="close"):
    df_array = np.array(df['value'])
    if type == "close":
        fuzzified_array = np.maximum(0, 1 - (df_array - df_array.min()) / (df_array.max() - df_array.min()))
    elif type == "far":
        fuzzified_array = np.maximum(0, (df_array - df_array.min()) / (df_array.max() - df_array.min()))
    else:
        raise ValueError("Invalid type. Choose 'close' or 'far'.")
    return fuzzified_array

#def fuzzify(df):
#     df_array = np.array(df['value'])
#     fuzzified_array = np.maximum(0, 1 - (df_array - df_array.min()) / (df_array.max() - df_array.min()))
#     return fuzzified_array

fuzzy_farm = fuzzify(d_to_farm, type='close')
fuzzy_road = fuzzify(d_to_road, type='close')
fuzzy_industry = fuzzify(d_to_industry, type='close')
fuzzy_nature = fuzzify(d_to_nature, type='far')

all_arrays = {'Farm':fuzzy_farm, 
              'Road':fuzzy_road, 
              'Industry':fuzzy_industry, 
              'Nature':fuzzy_nature}

### CREATE EMPTY LAYER ##################################
def create_empty_layer(d_to_farm):
    df_empty = d_to_farm[['hex9']]
    df_empty['color'] = None
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
    get_fill_color(hex_df, 'fuzzy', colormap_name)
    return hex_df

### FILTER POTENTIAL DIGESTER LOCATIONS ##################################
def filter_loi(fuzzy_cut_off, fuzzy_df):
    loi = fuzzy_df[(fuzzy_df['fuzzy'] >= fuzzy_cut_off[0]) & (fuzzy_df['fuzzy'] <= fuzzy_cut_off[1])]
    return loi

### PLOT PYDECK MAPS ##################################
view_state = pdk.ViewState(longitude=6.747489560596507, latitude=52.316862707395394, zoom=8, bearing=0, pitch=0)
@st.cache_data
def generate_pydeck(df, layer_info, view_state=view_state):
    return pdk.Deck(initial_view_state=view_state,
                    layers=[
                        pdk.Layer(
                            "H3HexagonLayer",
                            df,
                            pickable=True,
                            stroked=True,
                            filled=True,
                            extruded=False,
                            opacity=0.7,
                            get_hexagon="hex9",
                            get_fill_color ='color', 
                            # get_line_color=[255, 255, 255],
                            # line_width_min_pixels=1
                        ),
                    ],
                    tooltip={"text": f"{layer_info}: {{value}}"})

### CREATE STREAMLIT ##################################
def main():
    st.markdown("### Analysis for Identifying Suitable Digester Sites")
    # Plotting suitability variables
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Distance to Farm**")
        st.pydeck_chart(generate_pydeck(d_to_farm, "Distance to farm"), use_container_width=True)
    with col1:
        st.markdown("**Distance to Road**")
        st.pydeck_chart(generate_pydeck(d_to_road, "Distance to road"), use_container_width=True)
    with col2:
        st.markdown("**Distance to Industry**")
        st.pydeck_chart(generate_pydeck(d_to_industry, "Distance to industry"), use_container_width=True)
    with col3:
        st.markdown("**Distance to Nature and Water**")
        st.pydeck_chart(generate_pydeck(d_to_nature, "Distance to nature and water"), use_container_width=True)

    # Suitability analysis section
    with st.sidebar.form("suitability_analysis_form"):
        selected_variables = st.multiselect("Select Criteria", list(all_arrays.keys()))
        submit_button = st.form_submit_button("Build Suitability Map")

    if submit_button and not selected_variables:
        st.warning("No variable selected.")
        return
    
    hex_df = update_layer(selected_variables, all_arrays, d_to_farm)

    # Plot suitability map
    st.title("**Suitability Map**")
    hex_fuzzy = pdk.Layer(
            "H3HexagonLayer",
            hex_df,
            pickable=True,
            stroked=True,
            filled=True,
            extruded=False,
            opacity=0.7,
            get_hexagon="hex9",
            get_fill_color='color', 
            # get_line_color=[255, 255, 255],
            # line_width_min_pixels=2
        )

    # Filtering location of interest (loi) section
    with st.sidebar.form("select_loi"):
        fuzzy_cut_off = st.slider('Select suitability range to filter potential digester locations', 0.0, 1.0, (0.8, 1.0), step=0.01)
        submit_button_loi = st.form_submit_button("Filter")
    
    if submit_button_loi:
        loi = filter_loi(fuzzy_cut_off, hex_df)
        st.markdown(f"**Number of Potential Locations:{len(loi)}**")
        loi_plot = pdk.Layer(
            "H3HexagonLayer",
            loi,
            pickable=True,
            stroked=True,
            filled=True,
            extruded=False,
            opacity=0.7,
            get_hexagon="hex9",
            get_fill_color=[0,0,0,0], 
            get_line_color=[255, 0, 0],
            line_width_min_pixels=1
            )
        deck = pdk.Deck(layers=[hex_fuzzy, loi_plot], 
                        initial_view_state=view_state, 
                        # map_style='mapbox://styles/mapbox/streets-v12',
                        tooltip={"text": "Suitability: {fuzzy}"})
        st.pydeck_chart(deck, use_container_width=True)
    else:
        deck = pdk.Deck(layers=[hex_fuzzy], 
                        initial_view_state=view_state, 
                        # map_style='mapbox://styles/mapbox/streets-v12',
                        tooltip={"text": "Suitability: {fuzzy}"})
        st.pydeck_chart(deck, use_container_width=True)
    
    # Filtering location of interest (loi) section
    # with st.sidebar.expander("Save Suitability Analysis Results"):
    with st.sidebar.form("save_loi_form"):
        st.markdown("Save Suitability Analysis Results")
        save_loi = st.form_submit_button("Save")
    if save_loi:
        loi.to_csv('./hex/loi.csv')


    # st.download_button(
    #     label="Save Suitable Areas",
    #     data=loi,
    #     file_name='./hex/loi.csv',
    #     mime='text/csv',
    # )    

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

