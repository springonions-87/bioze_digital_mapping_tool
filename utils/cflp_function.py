# The script is designed to be run as a standalone program.

# It assigns capacity and capex to each location defines and solves the capacitated facility location problem, and finds farms that are not in the solution and plants that are in the solution

# * plots the result of the optimization problem
# * retrieves the results of the optimization problem
# * generates a DataFrame for plotting ArcLayer on Pydeck
# * maps values of a DataFrame to a Matplotlib color map
# * generates a function that maps values to a Matplotlib color map
# * applies a color mapping function to a DataFrame


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os
import pickle
from pyscipopt import Model, quicksum

# Constants for repeated values
OPEX_12_YR = 1047200*12
CAPEX = 6089160
LARGE_CAPACITY = 119547
LARGE_CAPEX = CAPEX + OPEX_12_YR

def assign_capacity_capex(J):
    """
    Assigns capacity and capital expenditure (capex) to each location in J.
    """
    M = {j: LARGE_CAPACITY for j in J}
    f = {j: LARGE_CAPEX for j in J}
    return M, f

def flp_scip(I, J, d, M, f, C, p):
    """
    Defines and solves the capacitated facility location problem.
    """
    model = Model("flp_percentage_demand")
    # Decision variables
    X = {(i,j): model.addVar(vtype="C", name=f"X({i},{j})") for i in I for j in J}
    y = {i: model.addVar(vtype="B", name=f"y({i})") for i in I}

    total_demand = sum(M[j] for j in J)
    target_demand = total_demand * p

    # Constraints
    for i in I:
        model.addCons(quicksum(X[i,j] for j in J) <= d[i]*y[i], f"Demand_(of_Digester_Capacity)({i})")
    for j in M:
        model.addCons(quicksum(X[i,j] for i in I) <= M[j], f"Capacity_(of_Farm_Manure_Production)({i})")
    for (i,j) in X:
        model.addCons(X[i,j] <= d[i]*y[i], f"Strong({i},{j})")
    model.addCons(quicksum(X[i, j] for i in I for j in J) >= target_demand, "TargetManureDemand")

    # Objective function
    model.setObjective(
        quicksum(f[i]*y[i] for i in I) +
        quicksum(C[i,j]*X[i,j] for i in I for j in J),
        "minimize")
    model.data = X,y

    return model, target_demand

def find_farm_not_in_solution_plant_in_solution(assignment_decision, Farm, use_plant_index):
    """
    Finds farms that are not in the solution and plants that are in the solution.
    """
    plant_in_use = [key for key, value in use_plant_index.items() if value > 0]
    combined_dict = [i for indices in assignment_decision.values() for i in indices]
    farm_not_in_solution = [i for i in Farm if i not in combined_dict]

    duplicates = list(set([item for item in combined_dict if combined_dict.count(item) > 1]))
    if duplicates:
        print("Duplicate values:", duplicates)
    else:
        print("There are no duplicates in the list.")
    
    return plant_in_use, farm_not_in_solution 

def plot_result(Plant, potential_digester_location, assignment_decision, farm, Farm, use_plant_index, target, total_cost, filename, save_fig=False):
    """
    Plots the result of the optimization problem.
    """
    plant_in_use, farm_not_in_solution = find_farm_not_in_solution_plant_in_solution(assignment_decision, Farm, use_plant_index)

    plt.figure(figsize=(8, 6))
    
    for i in Plant:
        plt.scatter(potential_digester_location.loc[i, 'x'], potential_digester_location.loc[i, 'y'], marker="^", s=50, c='Black')
        label = f"Digester {i}"
        plt.annotate(label, (potential_digester_location.loc[i, 'x'], potential_digester_location.loc[i, 'y']), textcoords="offset points", xytext=(-20,10), ha='left', va='bottom') 

    for j in Plant:
        assigned = assignment_decision[j]
        plt.scatter([farm.loc[i, 'x'] for i in assigned], [farm.loc[i, 'y'] for i in assigned], label=f"Farm assigned to Digester {j}", marker='o', s=30, alpha=0.5)

    for i in farm_not_in_solution:
        plt.scatter(farm.loc[i, 'x'], farm.loc[i, 'y'], marker='o', s=30, c='Grey', alpha=0.5)

    plt.xlabel("Longtitude")
    plt.ylabel("Latitude")
    plt.title(f"Manure Use: {int(target*100)}%  Total cost: €{int(total_cost)}", loc='left')
    legend = plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    if save_fig:
        plt.savefig(filename, dpi=400, bbox_extra_artists=(legend,), bbox_inches='tight')
    
    plt.show()

def flp_get_result(m, I, J, d, C):
    """
    Retrieves the results of the optimization problem.
    """
    EPS = 1.e-6
    x,y = m.data
    assignment = [(i,j) for (i,j) in x if m.getVal(x[i,j]) > EPS]
    digester = [i for i in y if m.getVal(y[i]) > EPS]    
    
    total_cost = m.getObjVal()

    result_dict = {x: [] for x in digester}
    for (i, j) in assignment:
        if i in digester:
            result_dict[i].append(j)

    x_values = {(i, j): m.getVal(x[i, j]) for (i, j) in x if m.getVal(x[i, j]) > EPS}
    flow_matrix = np.array([[x_values.get((i, j), 0) for i in I] for j in J])
    column_sum = np.sum(flow_matrix, axis=0)
    used_capacity = (column_sum/np.array(list(d.values())))*100
    used_capacity_df = pd.DataFrame(used_capacity, index=I)

    total_c = sum(C[key] for key in assignment if key in C)*365*12
    total_capex = len(digester)*CAPEX
    total_opex = len(digester)*OPEX_12_YR
    total_cost = pd.DataFrame({'Category': ['CAPEX', 'OPEX', 'Transportation Costs'], 'Value': [total_capex, total_opex, total_c]})

    return total_cost, result_dict, used_capacity_df

def get_arc(assignment_decision, candidate_sites, farm):
    """
    Generates a DataFrame for plotting ArcLayer on Pydeck.
    """
    arc_data = [{
        'start_lon': farm_coords[0],
        'start_lat': farm_coords[1],
        'end_lon': digester_coords[0],
        'end_lat': digester_coords[1],
        'digester_number': digester_number,
        'farm_number': farm_index,
        'material_quantity': farm_coords[2]
    } for digester_number, farm_indices in assignment_decision.items() for farm_index in farm_indices for digester_coords in candidate_sites[candidate_sites.index == digester_number][['x', 'y']].values for farm_coords in farm[farm.index == farm_index][['x', 'y', 'manure_t']].values]
    arc_layer_df = pd.DataFrame(arc_data)
    return arc_layer_df

def get_fill_color(df, value_column, colormap_name):
    """
    Maps values of a DataFrame to a Matplotlib color map.
    """
    min_value = df[value_column].min()
    max_value = df[value_column].max()
    diff = max_value - min_value
    cmap = plt.get_cmap(colormap_name)
    norm = mcolors.Normalize(vmin=min_value, vmax=max_value)
    df['color'] = df[value_column].apply(lambda value: [int(rgba*255) for rgba in cmap(1 - norm(value))[:3]])
    return df

def generate_color_mapping(colormap_name):
    """
    Generates a function that maps values to a Matplotlib color map.
    """
    cmap = plt.get_cmap(colormap_name)
    norm = mcolors.Normalize(vmin=0, vmax=1)
    return lambda value: [int(rgba*255) for rgba in cmap(norm(value))[:3]]

def apply_color_mapping(df, value_column, color_mapping):
    """
    Applies a color mapping function to a DataFrame.
    """
    df['color'] = df[value_column].apply(color_mapping)
    return df

def store_data_to_pickle(data, folder_path, file_name):
    """
    Stores data to a pickle file in a specific folder.
    """
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def load_data_from_pickle(folder_path, file_name):
    """
    Loads data from a pickle file in a specific folder.
    """
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'rb') as f:
        return pickle.load(f)
