# Capacitated Facility Location Problem - Functions
# Latest version = 6

from pulp import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import random


def cflp(Plant, Farm, fixed_cost, transport_cost, manure_production, max_capacity, target, total_manure):
    """
    Input
    * Plant: list (sets/array) of facility indices
    * Farm: list (sets/array) of customer indices
    * fixed_cost: dictionary of fixed cost of each Plant - {Plant:fixed cost}
    * transport_cost: nested dictionary of shortest paths (OD matrix) from all Farm to all Plant - {Plant:{Farm:distance}}
    * manure_production: quantity of manure in each Farm - {Farm:manure quantity}
    * max_capacity: maximum capacity of each Plant - {Plant:max capacity}
    * target: float of manure use goal defined as policy
    * total_manure: total manure produced by all Farm
    """

    # Setting the Problem
    prob = LpProblem("Capacitated_Facility_Location_Problem", LpMinimize)

    # Defining our Decision Variables
    use_plant = LpVariable.dicts("Plant", Plant, 0, 1, LpBinary) 
    ser_farm = LpVariable.dicts("Farm_Plant", [(i, j) for i in Farm for j in Plant], 0, 1, LpBinary) 

    # Objective Function
    prob += lpSum(fixed_cost[j]*use_plant[j] for j in Plant) + lpSum(transport_cost[j][i]*ser_farm[(i,j)] for j in Plant for i in Farm)

    # Costraints
    for i in Farm:
        prob += lpSum(ser_farm[(i, j)] for j in Plant) <= 1 # Very strange, the model becomes infeasible  if it's == 1, maybe because now the constraint has relaxed and not all farms need to be assigned to facility, which will be the case if ==1

    # The capacity constraint here it differnt than the one in paper, but i think it does the work still
    for j in Plant:
        prob += lpSum(manure_production[i] * ser_farm[(i,j)] for i in Farm) <= max_capacity[j]*use_plant[j]

    # Not really sure what this constraint does, I think it makes sure a farm can only be assigned to a facility given it's open, hence the value of xij is smaller or equal to yj 
    for i in Farm:
        for j in Plant:
            prob += ser_farm[(i,j)] <= use_plant[j]

    # Add a constraint to ensure at least x% of total manure production is sent to plants
    prob += lpSum(manure_production[i] * ser_farm[(i, j)] for i in Farm for j in Plant) >= target * total_manure

    # Solve 
    prob.solve()
    print("Solution Status = ", LpStatus[prob.status])

    """ Solution Outputs """
    
    # # Solution matrix
    # assignment_matrix = pd.DataFrame(index=Farm, columns=Plant)
    # for i in Plant:
    #     for j in Farm:
    #         assignment_matrix.at[j, i] = ser_farm[(j, i)].varValue

    # Solution dictionary
    # Initialize lists to store assignment information
    assignment_decision = {j: [] for j in Plant}

    # Collect assigned farms
    for i in Plant:
        for j in Farm:
            if ser_farm[(j,i)].varValue > 0.00001:
                assignment_decision[i].append(j)
    
    # Get total cost
    total_cost = pulp.value(prob.objective)

    # Extracting the values of the decision variables
    use_plant_index = {j: use_plant[j].varValue for j in Plant}
    ser_farm_index = {(i, j): ser_farm[(i, j)].varValue for i in Farm for j in Plant}

    # Calculating total fixed cost
    total_fixed_cost = sum(fixed_cost[j] * use_plant_index[j] for j in Plant)

    # Calculating total transportation cost
    total_transport_cost = sum(transport_cost[j][i] * ser_farm_index[(i, j)] for j in Plant for i in Farm)
    
    return total_cost, total_fixed_cost, total_transport_cost, assignment_decision, use_plant_index # assignment_matrix,


def find_farm_not_in_solution_plant_in_solution(assignment_decision, Farm, use_plant_index):
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


def plot_result(Plant, potential_digester_location, assignment_decision, farm, Farm, use_plant_index, target, total_cost, filename, save_fig=False):
    
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


def get_plot_variables(assignment_decision, digester_df, farm, color_mapping):

    # Map digesters to colors
    digester_df['color'] = digester_df.index.map(color_mapping)

    # Map assigned farms to colors
    assigned_farms_df = farm[farm.index.isin([i for indices in assignment_decision.values() for i in indices])]
    assigned_farms_df['color'] = assigned_farms_df.index.map({index: color_mapping[digester] for digester, indices in assignment_decision.items() for index in indices})

    # Map unassigned farms to a default color (e.g., grey)
    unassigned_farms_df = farm[~farm.index.isin([index for indices in assignment_decision.values() for index in indices])]

    return digester_df, assigned_farms_df, unassigned_farms_df


def store_data_to_pickle(data, folder_path, file_name):
    """
    Store data (dictionary or list) to a pickle file in a specific folder.

    Parameters:
    data (dict or list): The data (dictionary or list) to be stored.
    folder_path (str): The path of the folder to store the data.
    file_name (str): The name of the file to store the data.

    Returns:
    None
    """
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def load_data_from_pickle(folder_path, file_name):
    """
    Load data from a pickle file in a specific folder.

    Parameters:
    folder_path (str): The path of the folder to load the data from.
    file_name (str): The name of the file to load the data from.

    Returns:
    The data (dictionary, list, or float) loaded from the pickle file.
    """
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
        return data