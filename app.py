from cflp_function import *
import streamlit as st
from pulp import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import os
# print("Current working directory: ", os.getcwd())

st.title('BIOZE Digital Mapping Tool')
st.text('This is an interactive mapping tool on biogas.')

# slider = st.slider('Choose manure use percentage', 
#                    min_value=0, max_value=100, step=10)


# Load files and create parameters
    # List
        # set F     set of farm locations (list)
        # set P     set of potential digester locations
    # Dictionary 
        # p_i       manure production of each i
        # q_j       max capacity of each j 
        # f_j       fixed cost of establishing each j
        # C_ij      transportation matrix 
    # Float
        # alpha     total manure production
    # Float defined here
        # mu        manure utilization target 

loaded_manure = load_data_from_pickle('manure_production.pickle')
for key, value in loaded_manure.items():
    print(f"{key}: {value}")

# Import farm_cluster_mock_5 dataset - which is the mock data for potential digester locations
potential_digester_location = pd.read_csv('farm_cluster_mock_5.csv')
potential_digester_location.head()


# Define the capacities of digester
medium_digester_capacity = 78480  # in tonne/yr
large_digester_capacity = 150560  # in tonne/yr

# Define the costs of digester 
medium_digester_cost = 209249   # in euro CAPEX
large_digester_cost = 252616    # in euro CAPEX

potential_digester_location = potential_digester_location.drop(['count'], axis=1) # drop unnecessary column

# Create mock digester capacity data 
potential_digester_location['capacity'] = [medium_digester_capacity, medium_digester_capacity, large_digester_capacity, large_digester_capacity, large_digester_capacity]

# Create mock digester cost data (f_j)
potential_digester_location['cost'] = [medium_digester_cost, medium_digester_cost, large_digester_cost, large_digester_cost, large_digester_cost]

# (q_j)
max_capacity = potential_digester_location['capacity'].to_dict()    # Max_Supply = {'Fac-1' : 500, 'Fac-2' : 500, 'Fac-3' : 500}
# (f_j)
fixed_cost = potential_digester_location['cost'].to_dict()  # fixed_cost = {'Fac-1' : 1000, 'Fac-2' : 1000, 'Fac-3' : 1000 }


farm = pd.read_csv(r"./farm_mock.csv")

# Lists (sets / Array) of Customers and Facilities
Farm = farm.index.tolist()  # set F
Plant = potential_digester_location.index.tolist() # set P

# (p_i)
manure_production = farm['manure_t'].to_dict()  

# Define the total manure production by all farms (alpha)
total_manure = sum(manure_production[i] for i in Farm)

# Open the file for reading
with open("./transportation_cost.txt", "r") as fp:
    # Load the dictionary from the file
    transport_cost = json.load(fp)

# Function to recursively convert dictionary keys to integers
def convert_keys_to_int(data):
    if isinstance(data, dict):
        return {int(key) if key.isdigit() else key: convert_keys_to_int(value) for key, value in data.items()}
    else:
        return data

# Convert the keys to integers
transport_cost = convert_keys_to_int(transport_cost) # C_ij

for key, value in transport_cost.items():
    print(f"{key}: {value}")

# Define manure use goal (mu)
target = (st.slider('Choose manure use percentage', 
                   min_value=0, max_value=100, step=10))/ 100


# Run the model 
total_cost, total_fixed_cost, total_transport_cost, assignment_decision, use_plant_index = cflp(Plant, 
                                                                                                Farm, 
                                                                                                fixed_cost, 
                                                                                                transport_cost, 
                                                                                                manure_production, 
                                                                                                max_capacity, 
                                                                                                target, total_manure)


filename = f"./outputs/cflp_v{6}_{int(target*100)}%manure.png"  # You can choose the file extension (e.g., .png, .jpg, .pdf)
plot_result(Plant, 
            potential_digester_location, 
            assignment_decision, farm, Farm, use_plant_index, target, total_cost, filename, save_fig=False)

# Display the plot using st.pyplot()
st.pyplot(plt.gcf()) # get current figure, explicitly providing the current figure to Streamlit, 
                        # which avoids using Matplotlib's global figure object directly. 