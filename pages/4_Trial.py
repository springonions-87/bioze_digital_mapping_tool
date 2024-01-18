import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np
from cflp_function import *
import matplotlib.pyplot as plt
from io import BytesIO
import base64

padding=0
st.set_page_config(layout="wide")

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

colormap_name = 'Reds'
colormap_name_suitability_map = 'plasma'

### LOAD DATA ##################################
@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # get color for plotting
    return df

d_to_farm = load_data('./hex/d_to_farm_hex_complete.csv')
# d_to_road = load_data('./hex/d_to_road_hex_complete.csv', colormap_name)
d_to_industry = load_data('./hex/proximity_to_industry_hex_complete.csv')
# d_to_nature = load_data('./hex/proximity_to_nature_hex_complete.csv', colormap_name)
# d_to_urban = load_data('./hex/proximity_to_urban_hex_complete.csv', colormap_name)

### GENERATE COLORMAP ##################################
colormap = 'magma'
color_mapping = generate_color_mapping(colormap)

### FUZZIFY INPUT VARIABLES ##################################
@st.cache_data
def fuzzify_close(df, colormap_name=color_mapping):
    df_array = np.array(df['value'])
    fuzzified_array_close = np.maximum(0, 1 - (df_array - df_array.min()) / (df_array.max() - df_array.min()))
    df['fuzzy'] = fuzzified_array_close.round(3)
    apply_color_mapping(df, 'fuzzy', color_mapping)
    return df

st.cache_data
def fuzzify_far(df, colormap_name=color_mapping): 
    df_array = np.array(df['value'])
    fuzzified_array_far = np.maximum(0, (df_array - df_array.min()) / (df_array.max() - df_array.min()))
    df['fuzzy'] = fuzzified_array_far.round(3)
    apply_color_mapping(df, 'fuzzy', color_mapping)
    return df

# fuzzy_farm = fuzzify(d_to_farm, type='close')
# fuzzy_road = fuzzify(d_to_road, type='close')
fuzzy_industry_c = fuzzify_close(d_to_industry)
fuzzy_industry_f = fuzzify_close(d_to_industry)
# fuzzy_nature = fuzzify(d_to_nature, type='far')
# fuzzy_urban = fuzzify(d_to_urban, type='far')

fuzzy_farm_close = fuzzify_close(d_to_farm)
fuzzy_farm_far = fuzzify_far(d_to_farm)
# st.write(fuzzy_farm_far)

### INITIALIZE SESSION STATE ##################################
def initialize_session_state():
    if 'dist_choice' not in st.session_state:
        st.session_state.dist_choice = "Close"
    if 'choice_industry' not in st.session_state:
        st.session_state.choice_industry = "Close"

### FUZZIFY INPUT VARIABLES ################################## V1
# @st.cache_data
# def fuzzify(df, type="close", colormap_name=color_mapping):
#     df_array = np.array(df['value'])
#     if type == "close":
#         fuzzified_array = np.maximum(0, 1 - (df_array - df_array.min()) / (df_array.max() - df_array.min()))
#         df['fuzzy'] = fuzzified_array.round(3)
#         # get_fill_color(df, "fuzzy", colormap_name)
#         apply_color_mapping(df, 'fuzzy', color_mapping)
#     elif type == "far":
#         fuzzified_array = np.maximum(0, (df_array - df_array.min()) / (df_array.max() - df_array.min()))
#         df['fuzzy'] = fuzzified_array.round(3)
#         # get_fill_color(df, "fuzzy", colormap_name)
#         apply_color_mapping(df, 'fuzzy', color_mapping)
#     else:
#         raise ValueError("Invalid type. Choose 'close' or 'far'.")
#     return df

# fuzzy_farm = fuzzify(d_to_farm, type='close')
# fuzzy_road = fuzzify(d_to_road, type='close')
# fuzzy_industry = fuzzify(d_to_industry, type='close')
# fuzzy_nature = fuzzify(d_to_nature, type='far')
# fuzzy_urban = fuzzify(d_to_urban, type='far')

# all_arrays = {'Farms': np.array(fuzzy_farm['fuzzy']), 
#               'Road infrastructure': np.array(fuzzy_road['fuzzy']),
#               'Urban and residential areas': np.array(fuzzy_urban['fuzzy']), 
#               'Industrial areas': np.array(fuzzy_industry['fuzzy']), 
            #   'Nature and water bodies': np.array(fuzzy_nature['fuzzy'])}

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
    # get_fill_color(hex_df, 'fuzzy', colormap_name_suitability_map)
    apply_color_mapping(hex_df, 'fuzzy', color_mapping)
    hex_df['fuzzy'] = hex_df['fuzzy'].round(3)
    return hex_df

### FILTER POTENTIAL DIGESTER LOCATIONS ##################################
def filter_loi(fuzzy_cut_off, fuzzy_df):
    loi = fuzzy_df[(fuzzy_df['fuzzy'] >= fuzzy_cut_off[0]) & (fuzzy_df['fuzzy'] <= fuzzy_cut_off[1])]
    return loi


### PLOT PYDECK MAPS ##################################
view_state = pdk.ViewState(longitude=6.747489560596507, latitude=52.316862707395394, zoom=8, bearing=0, pitch=0)
# @st.cache_data
# def generate_pydeck(df, layer_info, view_state=view_state):
#     return pdk.Deck(initial_view_state=view_state,
#                     layers=[
#                         pdk.Layer(
#                             "H3HexagonLayer",
#                             df,
#                             pickable=True,
#                             stroked=True,
#                             filled=True,
#                             extruded=False,
#                             opacity=0.6,
#                             get_hexagon="hex9",
#                             get_fill_color='color', 
#                             # get_line_color=[255, 255, 255],
#                             # line_width_min_pixels=1
#                         ),
#                     ],
#                     tooltip={"text": f"{layer_info}: {{fuzzy}}"})

@st.cache_data
def generate_pydeck_2(df_close, df_far, choice, view_state=view_state):
    st.write(choice)
    if choice == "Close":
        return pdk.Deck(initial_view_state=view_state,
                        layers=[
                            pdk.Layer(
                                "H3HexagonLayer",
                                df_close,
                                pickable=True,
                                stroked=True,
                                filled=True,
                                extruded=False,
                                opacity=0.6,
                                get_hexagon="hex9",
                                get_fill_color='color', 
                                # get_line_color=[255, 255, 255],
                                # line_width_min_pixels=1
                            ),
                        ],
                        tooltip={"text": "Suitability:" f"{{fuzzy}}"})
    elif choice == "Far":
        return pdk.Deck(initial_view_state=view_state,
                    layers=[
                        pdk.Layer(
                            "H3HexagonLayer",
                            df_far,
                            pickable=True,
                            stroked=True,
                            filled=True,
                            extruded=False,
                            opacity=0.6,
                            get_hexagon="hex9",
                            get_fill_color='color', 
                            # get_line_color=[255, 255, 255],
                            # line_width_min_pixels=1
                        ),
                    ],
                    tooltip={"text": "Suitability:" f"{{fuzzy}}"})

def main():

    initialize_session_state

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Farms/Feedstock Locations**", help="Suitability for locating digesters determined by distance to feedstock locations.")
        farm_choice = st.radio("1", ["Close", "Far"], horizontal=True, label_visibility="collapsed", key="dist_choice_key")
        if st.session_state.dist_choice != farm_choice:
            st.session_state.dist_choice = farm_choice
            st.pydeck_chart(generate_pydeck_2(fuzzy_farm_close, fuzzy_farm_far, choice=st.session_state.dist_choice), use_container_width=True)
    with col2:
        st.markdown("**Industrial Areas**", help="Suitability for locating digesters determined by distance to industrial areas.")
        st.session_state.choice_industry = st.radio("1", ["Close", "Far"], horizontal=True, label_visibility="collapsed", key="choice_industry_key")
        st.pydeck_chart(generate_pydeck_2(fuzzy_industry_c, fuzzy_industry_f, choice=st.session_state.choice_industry), use_container_width=True)

    

                # with col1:
    #     st.markdown("**Distance to Roads**")
    #     st.pydeck_chart(generate_pydeck(d_to_road, "Distance to road"), use_container_width=True)

    # with col2:
    #     st.markdown("**Distance to Urban Areas**"
    #     st.pydeck_chart(generate_pydeck(d_to_urban, "Distance to urban"), use_container_width=True)
    # with col3:
    #     st.markdown("**Distance to Nature and Water Bodies**")
    #     st.pydeck_chart(generate_pydeck(d_to_nature, "Distance to nature and water"), use_container_width=True)
    # with col3:
    #     st.markdown(variable_legend_html, unsafe_allow_html=True)
            
            
# Run the Streamlit app
if __name__ == "__main__":
    main()

# if 'dist_choice' not in st.session_state:
#     st.session_state.dist_choice = ["Close", "Far"]

# # def fuzzify(dist_choice_button):
# #     if dist_choice_button == 'Close':
# #         print("now it will be fuzzified for close")
# #         st.session_state.dist_choice = 'Close'
# #         print(st.session_state)
# #     else:
# #         st.session_state.dist_choice = 'Far'
# #         print("now it will be fuzzified for far")
# #         print(st.session_state)

# def fuzzify_far():
#     st.session_state['dist_choice'] = 100 
#     st.write("Post fuzzify_far session state is", st.session_state.dist_choice)

# dist_choice_button = st.radio("", ["Close", "Far"], horizontal=True, label_visibility="collapsed")

# if dist_choice_button == st.session_state.dist_choice[0]:
#     x = 10
# elif dist_choice_button == st.session_state.dist_choice[1]:
#     x = 20
# else: 
#     print('none')

# # if dist_choice_button == 'Far':
# #     fuzzify_far()
# # else: 
# #     st.session_state['dist_choice'] = 'Close' 

# st.write("Current Session State:", st.session_state.dist_choice, x)

# # Sample DataFrames
# df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
# df2 = pd.DataFrame({'X': [10, 20, 30], 'Y': [40, 50, 60]})

# # Function to initialize session state
# def initialize_session_state():
#     if 'dist_choice' not in st.session_state:
#         st.session_state.dist_choice = "close"

# # Main Streamlit app
# def main():
#     initialize_session_state()

#     st.session_state.dist_choice = st.radio("Choice", ["close", "far"])

#     # Display selected DataFrame
#     st.write("Selected DataFrame:", st.session_state.dist_choice)

#     # Plot selected DataFrame
#     if st.session_state.dist_choice == "close":
#         st.write("Plotting DataFrame 1:")
#         st.write(df1)
#     elif st.session_state.dist_choice == "far":
#         st.write("Plotting DataFrame 2:")
#         st.write(df2)

# if __name__ == "__main__":
#     main()


# st.set_page_config(layout="wide")

# color_scale = [
#     [0, 255, 0, 255],  # RGB color for value 0 (green)
#     [255, 0, 0, 255]   # RGB color for value 1 (red)
# ]

# # Add a subtitle for the checkboxes
# st.sidebar.markdown("### Hexagon Resolution")
# # Streamlit checkbox for toggling the visibility of the ArcLayer
# show_7 = st.sidebar.checkbox('7', value=True)
# show_8 = st.sidebar.checkbox('8', value=False)
# show_9 = st.sidebar.checkbox('9', value=False)


# @st.cache_data
# def load_data(csv_path):
#     df = pd.read_csv(csv_path)
#     return df

# df_7 = load_data('./hex/df_hex_7.csv')
# df_8 = load_data('./hex/df_hex_8.csv')
# df_9 = load_data('./hex/df_hex_9.csv')
# df_10 = load_data('./hex/d_to_farm_hex_complete.csv')

# # Define a layer to display on a map
# hex_7 = pdk.Layer(
#     "H3HexagonLayer",
#     df_7,
#     pickable=True,
#     stroked=True,
#     filled=True,
#     extruded=False,
#     opacity=0.7,
#     get_hexagon="hex7",
#     get_fill_color ='[255 * Value, 255 * (1 - Value), 0, 255]', 
#     get_line_color=[255, 255, 255],
#     line_width_min_pixels=2)

# hex_8 = pdk.Layer(
#     "H3HexagonLayer",
#     df_8,
#     pickable=True,
#     stroked=True,
#     filled=True,
#     extruded=False,
#     opacity=0.7,
#     get_hexagon="hex8",
#     get_fill_color ='[255 * Value, 255 * (1 - Value), 0, 255]', 
#     # get_line_color=[255, 255, 255],
#     line_width_min_pixels=2)

# hex_9 = pdk.Layer(
#     "H3HexagonLayer",
#     df_10,
#     pickable=True,
#     stroked=True,
#     filled=True,
#     extruded=False,
#     opacity=0.7,
#     get_hexagon="h3",
#     get_fill_color = [255, 255, 255], #'[255 * Value, 255 * (1 - Value), 0, 255]', 
#     get_line_color=[255, 255, 255],
#     line_width_min_pixels=2)

# # Set the viewport location
# # view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=14, bearing=0, pitch=30)
# view_state = pdk.ViewState(longitude=df_7['lng'].mean(), latitude=df_7['lat'].mean(), zoom=8, bearing=0, pitch=0)

# # Render
# deck = pdk.Deck(layers=[hex_7, hex_8, hex_9], initial_view_state=view_state, tooltip={"text": "Suitability: {Value}"})

# deck.layers[0].visible = show_7
# deck.layers[1].visible = show_8
# deck.layers[2].visible = show_9

# st.pydeck_chart(deck, use_container_width=True)