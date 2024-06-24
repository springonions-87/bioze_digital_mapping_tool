# The script is designed to be run as a standalone program

# * It converts H3 indices to Shapely polygons and points
# * converts a DataFrame with H3 spatial indices to a GeoDataFrame
# * finds the nearest road network node for each point in a GeoDataFrame
# * calculates an Origin-Destination (OD) matrix

from sklearn.neighbors import BallTree
import numpy as np
import networkx as nx
import osmnx as ox
import geopandas as gpd
import pandas as pd
import h3
from shapely.ops import nearest_points
from shapely.geometry import Polygon, Point
from utils.cflp_function import store_data_to_pickle

def cell_to_shapely_polygon(h3_index):
    """
    Converts H3 index to Shapely polygons.
    """
    coords = h3.h3_to_geo_boundary(h3_index)
    flipped = tuple(coord[::-1] for coord in coords)
    return Polygon(flipped)

def cell_to_shaply_point(h3_index):
    """
    Converts H3 indices to Shapely points (lat, lon). 
    """
    lat, lon = h3.h3_to_geo(h3_index)
    return Point(lon, lat)

def loi_to_gdf(loi):
    """
    Converts a DataFrame with H3 spatial indices to a GeoDataFrame.
    """
    loi['geometry'] = loi['hex9'].apply(cell_to_shaply_point)
    loi_gdf = gpd.GeoDataFrame(loi, geometry='geometry', crs=4326)
    return loi_gdf

def find_closest_osmid(gdf, n):
    """
    Finds the nearest road network node for each candidate site and each farm. 
    """
    # Create a BallTree for efficient nearest neighbor search
    tree = BallTree(np.array(list(zip(n.y, n.x))), leaf_size=15, metric='haversine')

    # Find the index of the closest point from 'n' for each point in 'gdf'
    indices = tree.query(np.array(list(zip(gdf.geometry.y, gdf.geometry.x))), return_distance=False)

    # Use the indices to map to the corresponding osmid
    gdf['closest_osmid'] = n.iloc[indices.flatten()]['osmid_original'].values

    print(gdf)

def calculate_od_matrix(farm_gdf, loi_gdf, cost_per_km=0.69, frequency_per_day=1, lifetime_in_days=1):
    """
    Finds the nearest road network node for each candidate site and calculates the cost matrix.
    """
    # Load the graph
    g = ox.load_graphml('./osm_network/G.graphml') 

    # Get unique origin and destination nodes
    orig = farm_gdf['closest_os'].unique().tolist()
    dest = loi_gdf['closest_os'].unique().tolist()

    print(f"Unique origin nodes: {orig}")
    print(f"Unique destination nodes: {dest}")

    # Initialize the OD matrix
    od_matrix = {}

    # Calculate shortest path between all pair orig (farm) and dest (set of candidate digester sites)
    for origin in orig:
        if origin in g.nodes:
            od_matrix[origin] = {destination: nx.shortest_path_length(g, origin, destination, weight='length') / 1000 
                                 for destination in dest if destination in g.nodes}
        else:
            print(f"Origin node {origin} is not in the graph.")

    # Create a placeholder that maps digester candidate site index with the index of its closest node
    placeholders = {i:j for i, j in zip(loi_gdf.index.values, loi_gdf['closest_os'])}

    # Restructure the OD matrix
    restructured_od = {farm: {index: distances.get(placeholder, None) 
                              for index, placeholder in placeholders.items()} 
                       for farm, distances in od_matrix.items() if farm in farm_gdf['closest_os'].values}

    # Create a new dictionary with sorted keys
    new_dict = {(digester, farm): distance 
                for farm, digester_distances in restructured_od.items() 
                for digester, distance in digester_distances.items()}

    # Sort the transport cost dictionary
    transport_cost = dict(sorted(new_dict.items(), key=lambda x: x[0][0]))

    # Convert from distance to cost
    C = {key: value * cost_per_km * frequency_per_day * lifetime_in_days 
         for key, value in transport_cost.items()}

    # Get the list of plants
    plant = loi_gdf.index.tolist()

    return C, plant