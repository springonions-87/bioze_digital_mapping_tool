import networkx as nx
import osmnx as ox
import geopandas as gpd
import pandas as pd
import h3
from shapely.ops import nearest_points
from shapely.geometry import Polygon, Point
from cflp_function import store_data_to_pickle


def cell_to_shapely_polygon(h3_index):
    """
    A function to convert H3 index to Shapely polygons
    """
    # hex_center_coords = h3.h3_to_geo(h3_index)
    coords = h3.h3_to_geo_boundary(h3_index)
    flipped = tuple(coord[::-1] for coord in coords)
    # center_point = Point(hex_center_coords)
    return Polygon(flipped) #, center_point

def cell_to_shaply_point(h3_index):
    """
    A function to convert H3 index to Shapely points
    """
    lat, lon = h3.h3_to_geo(h3_index)
    return Point(lon, lat)

def loi_to_gdf(loi):
    loi['geometry'] = loi['hex9'].apply(cell_to_shaply_point) # can change the function here
    loi_gdf = gpd.GeoDataFrame(loi, geometry='geometry', crs=4326)
    return loi_gdf

# convert ot gdf

def find_closest_osmid(gdf, n):
    gdf['closest_osmid'] = gdf['geometry'].apply(
        lambda location: n.loc[n['geometry'] == nearest_points(location, n.unary_union)[1], 'osmid'].iloc[0])


def calculate_od_matrix(farm_gdf, loi_gdf, cost_per_km=0.69):
    g = ox.load_graphml('./osm_network/G.graphml') 
    orig = farm_gdf['closest_osmid'].unique().tolist()
    dest = loi_gdf['closest_osmid'].unique().tolist()

    # Initialize an empty OD matrix
    od_matrix = {}
    # Calculate shortest path between all pair orig (farm) and dest (potential location)
    for origin in orig:
        od_matrix[origin] = {}
        for destination in dest:
            distance = nx.shortest_path_length(g, origin, destination, weight='length')
            od_matrix[origin][destination] = distance/1000 # convert from m to km
            # output dict = {orig:{dest:distance, dest:distance....}}

    # Initialize an empty nested dictionary
    new_nested_dict = {}
    # Create a new nested dictionary with DataFrame index as keys
    # {farm1:{dest:distance, dest:distance....}} # some nodes are the closest for more than 1 farms, so now we make sure the dictionary is with key of all farms and each take the 
    # associated distances (i.e. some farms will have the same od to all dest)
    for idx, row in farm_gdf.iterrows():
        osmid_value = row['closest_osmid']
        if osmid_value in od_matrix:
            new_nested_dict[idx] = od_matrix[osmid_value]    

    placeholders = {i:j for i, j in zip(loi_gdf.index.values, loi_gdf['closest_osmid'])}

    restructured_od = {}
    for farm, distances in new_nested_dict.items():
        restructured_od[farm] = {}
        for index, placeholder in placeholders.items():
            restructured_od[farm][index] = distances.get(placeholder, None)

    transport_cost = {(farm, index): distance for farm, distances in restructured_od.items() for index, distance in distances.items()}

    # Convert from distance to cost
    c = {key: value * cost_per_km for key, value in transport_cost.items()}

    # store_data_to_pickle(transport_cost, 'app_data', transport_cost_file_name)
    # store_data_to_pickle(loi_gdf.index.tolist(), 'app_data', plant_file_name)

    return c, (loi_gdf.index.tolist())