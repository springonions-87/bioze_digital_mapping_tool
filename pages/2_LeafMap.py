import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np

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

### LOAD DATA ##################################
@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

d_to_farm = load_data('./hex/d_to_farm_hex.csv')
d_to_road = load_data('./hex/d_to_road_hex.csv')
fake = load_data("./hex/fake_hex.csv")

### FUZZIFY INPUT VARIABLES ##################################
@st.cache_data
def fuzzify(df):
    df_array = np.array(df['Value'])
    fuzzified_array = np.maximum(0, 1 - (df_array - df_array.min()) / (df_array.max() - df_array.min()))
    return fuzzified_array

fuzzy_farm = fuzzify(d_to_farm)
fuzzy_road = fuzzify(d_to_road)
fuzzy_fake = fuzzify(fake)

all_arrays = {'Farm': fuzzy_farm, 'Road': fuzzy_road, 'Fake': fuzzy_fake}

### CREATE EMPTY LAYER ##################################
def create_empty_layer(d_to_farm):
    df_empty = d_to_farm[['hex9']]
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
    return hex_df

### CREATE STREAMLIT ##################################
def main():
    st.markdown("### Analysis for Identifying Suitable Digester Sites")

    with st.sidebar.form("suitability_analysis_form"):
        selected_variables = st.multiselect("Select Criteria", list(all_arrays.keys()))
        submit_button = st.form_submit_button("Build Suitability Map")

    if submit_button and not selected_variables:
        st.warning("No variable selected.")
        return
    
    hex_df = update_layer(selected_variables, all_arrays, d_to_farm)
    
    view_state = pdk.ViewState(longitude=6.747489560596507, latitude=52.316862707395394, zoom=10, bearing=0, pitch=0)

    col1, col2 = st.columns(2)
    # Plot Map 1
    with col1:
        st.markdown("**Distance to Farm**")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=view_state,
            layers=[
                pdk.Layer(
                    "H3HexagonLayer",
                    d_to_farm,
                    pickable=True,
                    stroked=True,
                    filled=True,
                    extruded=False,
                    opacity=0.7,
                    get_hexagon="hex9",
                    get_fill_color ='[255, 255, 255]', 
                    get_line_color=[255, 255, 255],
                    line_width_min_pixels=2
                ),
            ],
            tooltip={"text": "Distance to farm: {Value}"}
        ), use_container_width=True)

    # Plot Map 2
    with col2:
        st.markdown("**Distance to  road**")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=view_state,
            layers=[
                pdk.Layer(
                    "H3HexagonLayer",
                    d_to_road,
                    pickable=True,
                    stroked=True,
                    filled=True,
                    extruded=False,
                    opacity=0.7,
                    get_hexagon="hex9",
                    get_fill_color ='[255, 255, 255]', 
                    get_line_color=[255, 255, 255],
                    line_width_min_pixels=2
                ),
            ],
            tooltip={"text": "Distance to road: {Value}"}
        ), use_container_width=True)

    # Define a layer to display on a map
    hex_fuzzy = pdk.Layer(
        "H3HexagonLayer",
        hex_df,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        opacity=0.7,
        get_hexagon="hex9",
        get_fill_color ='[255 * fuzzy, 255 * (1 - fuzzy), 0, 255]', 
        get_line_color=[255, 255, 255],
        line_width_min_pixels=2)

    deck = pdk.Deck(layers=[hex_fuzzy], initial_view_state=view_state, tooltip={"text": "Suitability: {fuzzy}"})
    st.pydeck_chart(deck, use_container_width=True)
    

# Run the Streamlit app
if __name__ == "__main__":
    main()


# # Create multiple arrays
# array1 = np.array([1, 5, 3, 8])
# array2 = np.array([2, 4, 1, 7])
# array3 = np.array([0, 6, 2, 9])

# # Create a dictionary mapping array names to their corresponding numpy arrays
# all_arrays = {'Farm': array1, 'Road': array2, 'Fake': array3}

# # # import sys
# # import leafmap.foliumap as leafmap

# # # sys.path

# # raster_file = '/Users/wenyuc/Desktop/UT/data/raster/fuzzy_complete_3857.tif'

# # m = leafmap.Map()
# # m.add_basemap()
# # m.add_raster(raster_file, cmap="viridis", layer_name="Raster Layer")

# # m.to_streamlit()

