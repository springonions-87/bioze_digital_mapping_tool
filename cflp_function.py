import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os
import pickle
import random
from pyscipopt import Model, quicksum
# from pulp import *

"""
This notebook contains various functions required by the Streamlit app. 
The functions are called by both Phase 1 and 2 of the app.

"""

def assign_capacity_capex(J):
    opex_12_yr = 1047200*12
    capex = 6089160
    large = [119547, capex + opex_12_yr] # [capacity, CAPEX]

    M = {j: large[0] for j in J}
    f = {j: large[1] for j in J}

    return M, f


def flp_scip(I, J, d, M, f, C, p):
    """
    Model for defining and solving the capacitated facility location problem.

    Parameters
    ----------
    I : list
        set of candidate digester sites
    J : list
        set of feedstock locations
    d: list
        d[i] is capacity of digester site i ('demand' of digester site i)
    M : list
        M[j] is maximum manure production of farm j
    f: list
        f[i] is fixed cost for building a digester site i 
    C: dict
        C[i,j] is unit cost of transporting feedstock from farm j to digester i
    p: float 
        percentage of total demand to be met (manure utilization target, determined by user input through the slider in the app)

    Outputs
    ----------
    model : dict

    target_demand : float
        The minimum amount of manure to be processed in the model.

    """
    model = Model("flp_percentage_demand")
    
    X,y = {},{}

    # Express the total manure in the region & target demand input by users
    total_demand = sum(M[j] for j in J)
    target_demand = total_demand * p
    # Decision variables
    for i in I:
        y[i] = model.addVar(vtype="B", name="y(%s)"%i)
        for j in J:
            X[i,j] = model.addVar(vtype="C", name="X(%s,%s)"%(i,j))
    # Constraint 1
    for i in I:
        model.addCons(quicksum(X[i,j] for j in J) <= d[i]*y[i], "Demand_(of_Digester_Capacity)(%s)"%i)
    # Constrain 2
    for j in M:
        model.addCons(quicksum(X[i,j] for i in I) <= M[j], "Capacity_(of_Farm_Manure_Production)(%s)"%i)
    # Constrain 3
    for (i,j) in X:
        model.addCons(X[i,j] <= d[i]*y[i], "Strong(%s,%s)"%(i,j))
    # Constraint 4
    model.addCons(quicksum(X[i, j] for i in I for j in J) >= target_demand, "TargetManureDemand")

    # Objective function
    model.setObjective(
        quicksum(f[i]*y[i] for i in I) +
        quicksum(C[i,j]*X[i,j] for i in I for j in J),
        "minimize")
    model.data = X,y

    return model, target_demand

# def find_farm_not_in_solution_plant_in_solution(assignment_decision, Farm, use_plant_index):
    """
    Input:
        assignment_decision         dictionary of model output {plant:[all the assigned farms]}
        Farm                        list (sets/array) of customer indices
        use_plant_index             {Plant index:0 or 1}

    Output:
        empty_keys_unused_plant     a list of indices of unused plants
        farm_not_in_solution        a list of indices of excluded farms
        
    """
    
    # Find plants that in the optimal solution
    plant_in_use = []
    
    # for key, value in assignment_decision.items():
    #     if value is not None and not (
    #         (isinstance(value, str) and value.strip() == '') or
    #         (isinstance(value, (list, dict)) and not value)
    #     ):
    #         plant_in_use.append(key)
    for key, value in use_plant_index.items():
        if value > 0:
            plant_in_use.append(key)
    
    # Find farms that are excluded in the optimal solution aka. it is not assigned to any plants
    # Append the lists from the dictionary to a combined list
    combined_dict = []

    for key in assignment_decision:
        combined_dict.extend(assignment_decision[key])
    
    farm_not_in_solution = []

    for i in Farm:
        if i not in combined_dict:
            farm_not_in_solution.append(i)

    # Sanity check - check if there are duplicates in combined_dict (a farm is assigned to more than one plant)
    # Initialize a dictionary to store seen values
    seen = {}
    # Initialize a list to store duplicate values
    duplicates = []

    # Iterate through the list
    for item in combined_dict:
        # If the item is already in the dictionary, it's a duplicate
        if item in seen:
            duplicates.append(item)
        else:
            seen[item] = True
    if duplicates:
        print("Duplicate values:", duplicates)
    else:
        print("There are no duplicates in the list.")
    
    return plant_in_use, farm_not_in_solution 


# def plot_result(Plant, potential_digester_location, assignment_decision, farm, Farm, use_plant_index, target, total_cost, filename, save_fig=False):
    
    # Get farm_not_in_solution 
    plant_in_use, farm_not_in_solution = find_farm_not_in_solution_plant_in_solution(assignment_decision, Farm, use_plant_index)

    # Visualize the results
    plt.figure(figsize=(8, 6))
    
    for i in Plant:
        plt.scatter(potential_digester_location.loc[i, 'x'], potential_digester_location.loc[i, 'y'], marker="^", s=50, c='Black')
        # label = f"Plant {i} \n Capacity:{potential_digester_location.loc[i, 'capacity']} (t/yr)"
        label = f"Digester {i}"
        plt.annotate(label, # this is the text
                    (potential_digester_location.loc[i, 'x'], potential_digester_location.loc[i, 'y']), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(-20,10), # distance from text to points (x,y)
                    ha='left', va='bottom') # horizontal alignment can be left, right or center 

    # Plot farms in solution
    for j in Plant:
        assigned = assignment_decision[j]
        plt.scatter([farm.loc[i, 'x'] for i in assigned], [farm.loc[i, 'y'] for i in assigned], label=f"Farm assigned to Digester {j}", marker='o', s=30, alpha=0.5)

    # Plot farms excluded in solution
    for i in farm_not_in_solution:
        plt.scatter(farm.loc[i, 'x'], farm.loc[i, 'y'], marker='o', s=30, c='Grey', alpha=0.5)

    # Add labels and legend
    plt.xlabel("Longtitude")
    plt.ylabel("Latitude")
    plt.title(f"Manure Use: {int(target*100)}%  Total cost: €{int(total_cost)}", loc='left')
    legend = plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    if save_fig:
        plt.savefig(filename, dpi=400, bbox_extra_artists=(legend,), bbox_inches='tight')
    
    plt.show()


def flp_get_result(m, I, J, d, C):
    """
    Retrieve the results of a SCIP optimization model (PySCIPOpt).

    Parameters
    ----------
    m : model
        SCIP optimization model instance.
    I : list
        set of candidate digester sites 
    J : list
        set of feedstock locations
    d: list
        d[i] is capacity of digester site i ('demand' of digester site i)
    C: dict
        C[i,j] is unit cost of transporting feedstock from farm j to digester i

    Outputs
    ----------
    total_cost : float 
        Total cost of the solution.
    result_dict : dict
        Dictionary of the assignment of farms to digesters in the solution.
    used_capacity : list
        List of the percentage utilization of each digester site's capacity.

    """
    EPS = 1.e-6
    x,y = m.data
    assignment = [(i,j) for (i,j) in x if m.getVal(x[i,j]) > EPS]
    digester = [i for i in y if m.getVal(y[i]) > EPS]    
    
    total_cost = m.getObjVal()

    # Create a dictionary to store the results
    result_dict = {x: [] for x in digester}
    # Iterate over edges and populate the result_dict
    for (i, j) in assignment:
        if i in digester:
            result_dict[i].append(j)

    # Get percentage of utilization
    x_values = {(i, j): m.getVal(x[i, j]) for (i, j) in x if m.getVal(x[i, j]) > EPS} # get how much is flowing between every assignment
    flow_matrix = np.array([[x_values.get((i, j), 0) for i in I] for j in J]) # create a flow matrix (len(farm)xlen(plant))
    column_sum = np.sum(flow_matrix, axis=0) # sum of total flow going to every plant    used_capacity = (column_sum/np.array(list(M.values())))*100
    used_capacity = (column_sum/np.array(list(d.values())))*100
    used_capacity_df = pd.DataFrame(used_capacity, index=I)

    # Total costs
    total_c = sum(C[key] for key in assignment if key in C)*365*12
    total_capex = len(digester)*6089160
    total_opex = len(digester)*(1047200*12)
    total_cost = pd.DataFrame({'Category': ['CAPEX', 'OPEX', 'Transportation Costs'],
        'Value': [total_capex, total_opex, total_c]})

    return total_cost, result_dict, used_capacity_df

# def get_plot_variables(assignment_decision, digester_df, farm, color_mapping):

#     # Map digesters to colors
#     digester_df['color'] = digester_df.index.map(color_mapping)
#     digester_df['color'] = digester_df['color'].fillna('[0, 0, 0,0]') # the color doesn't really work here

#     # Map assigned farms to colors
#     assigned_farms_df = farm[farm.index.isin([i for indices in assignment_decision.values() for i in indices])]
#     assigned_farms_df['color'] = assigned_farms_df.index.map({index: color_mapping[digester] for digester, indices in assignment_decision.items() for index in indices})

#     # Map unassigned farms to a default color (e.g., grey)
#     unassigned_farms_df = farm[~farm.index.isin([index for indices in assignment_decision.values() for index in indices])]

#     return digester_df, assigned_farms_df, unassigned_farms_df


def get_arc(assignment_decision, candidate_sites, farm):
    """
    Generate a DataFrame for plotting ArcLayer on Pydeck. 

    Parameters
    ----------
    assignment_decision : dict
        Assignment of farms to digesters in the optimal solution.
    candidate_sites : DataFrame
        Dataframe of candidate sites of digesters.
    farm : DataFrame
        Dataframe of farm points.

    Outputs
    ----------
    arc_layer_df : DataFrame 
        A DataFrame for plotting an ArcLayer on Pydeck. 

    """
    # Create a list to store dictionaries for the ArcLayer DataFrame
    arc_data = []

    # Iterate through the assignments dictionary
    for digester_number, farm_indices in assignment_decision.items():
        digester_coords = candidate_sites[candidate_sites.index == digester_number][['x', 'y']].values[0]
        for farm_index in farm_indices:
            # Get coordinates for the current digester and farm
            farm_coords = farm[farm.index == farm_index][['x', 'y', 'manure_t']].values[0]
            # Append a dictionary with required columns for ArcLayer to the list
            arc_data.append({
                'start_lon': farm_coords[0],
                'start_lat': farm_coords[1],
                'end_lon': digester_coords[0],
                'end_lat': digester_coords[1],
                'digester_number': digester_number,
                'farm_number': farm_index,
                'material_quantity': farm_coords[2]  # Add the material quantity to the dictionary
            })
    # Create a DataFrame from the list of dictionaries
    arc_layer_df = pd.DataFrame(arc_data)
    return arc_layer_df

def get_fill_color(df, value_column, colormap_name):
    # Calculate min, max, and diff
    min_value = df[value_column].min()
    max_value = df[value_column].max()
    diff = max_value - min_value

    # Obtain colormap
    cmap = plt.get_cmap(colormap_name)

    # Define a normalization function for the data range
    norm = mcolors.Normalize(vmin=min_value, vmax=max_value)

    # Function to convert data values to RGB using reversed colormap
    def get_rgb_reversed(value):
        rgba = cmap(1 - norm(value))
        return [int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255)]

    # Apply the function to the DataFrame to get RGB values
    df['color'] = df[value_column].apply(get_rgb_reversed)
    return df

def generate_color_mapping(colormap_name):
    """
    Generate a function that maps values to a Matplotlib color map.

    Parameters
    ----------
    colormap_name : str
        Any available colormap, I usually use Matplotlib colormap e.g. 'viridis'

    Outputs
    ----------
    get_rgb : function 
        A function that takes a value between 0 and 1 and returns its corresponding RGB color. 

    """
    # Define a colormap 
    cmap = plt.get_cmap(colormap_name)
    # Create a normalization function for the data range (reversed)
    norm = mcolors.Normalize(vmin=0, vmax=1)
    # Function to convert data values to RGB using reversed colormap
    def get_rgb(value):
        # rgba = cmap(1 - norm(value))
        rgba = cmap(norm(value))
        return [int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255)]
    
    return get_rgb


def apply_color_mapping(df, value_column, color_mapping):
    """
    Map values of a DataFrame to a Matplotlib color map. 

    Parameters
    ----------
    df : DataFrame
        The input DataFrame
    value_column : str
        Column name of the DataFrame to generate the color map from.
    color_mapping :  
        A color mapping function that converts values between 0 and 1 to RGB colors.

    """
    # Apply the color mapping to the DataFrame to get RGB values
    df['color'] = df[value_column].apply(color_mapping)
    return df


def store_data_to_pickle(data, folder_path, file_name):
    """
    Store data to a pickle file in a specific folder.

    Parameters
    ----------
    data : any
        Data to be stored as a pickle file
    folder_path : str
        Path to the folder for storing the data.
    file_name : str
        Name given to the stored file.
    
    """
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def load_data_from_pickle(folder_path, file_name):
    """
    Load data from a pickle file in a specific folder.

    Parameters
    ----------
    folder_path : str
        Path to the folder that the data is stored in.
    file_name : str
        Name of the file to be loaded.

    Outputs
    ----------
    data : any 

    """
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
        return data