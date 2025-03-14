import json
import re
import os

import json

import json

def update_main_json(recreated_path, main_path, filtered_json_path, output_path):
    # Load the JSON data
    with open(recreated_path) as f:
        recreated = json.load(f)
    with open(main_path) as f:
        main = json.load(f)
    with open(filtered_json_path) as f:
        filtered_json = json.load(f)
    
    # Create a lookup dictionary for filtered_json values
    filtered_values = {
        "traffic": filtered_json.get("traffic_YoY"),
        "demand": filtered_json.get("demand_YoY"),
        "discount": filtered_json.get("discount_YoY"),
        "price": filtered_json.get("price_YoY"),
        "AOS": filtered_json.get("AOS_YoY"),
        "UPT": filtered_json.get("UPT_YoY"),
        "AUR": filtered_json.get("AUR_YoY"),
        "Conversion Rate": filtered_json.get("conversion_YoY"),
        "conversion": filtered_json.get("conversion_YoY")  # Matching name in main.json
    }
    
    # Extract "start" nodes from recreated edges
    start_nodes = {edge["start"] for edge in recreated["edges"]}
    
    # Update low and high values in main.json
    for node in main["nodes"]:
        node_id = node["id"]
        if node_id in filtered_values and filtered_values[node_id] is not None:
            value = filtered_values[node_id]
            if node_id in start_nodes:  # Directly present in recreated edges
                if value < node["low"]:
                    node["low"] = value
                elif value > node["high"]:
                    node["high"] = value
            else:  # Not in start_nodes, adjust based on closest boundary
                low_diff = abs(value - node["low"])
                high_diff = abs(value - node["high"])
                if low_diff < high_diff:
                    node["low"] = value
                else:
                    node["high"] = value
    
    # Save the updated main.json
    with open(output_path, "w") as f:
        json.dump(main, f, indent=2)
    
    print(f"Updated main.json has been saved to {output_path}.")



def process_causal_maps(recreated_folder, main_folder, derived_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get file lists from recreated_CM and derived folders
    recreated_files = {f.replace("_recreated_CM.json", ""): f for f in os.listdir(recreated_folder) if f.endswith("_recreated_CM.json")}
    derived_files = {f.replace("_filtered_data.json", ""): f for f in os.listdir(derived_folder) if f.endswith("_filtered_data.json")}

    # Loop through recreated_CM files
    for brand, recreated_file in recreated_files.items():
        recreated_path = os.path.join(recreated_folder, recreated_file)
        filtered_json_path = os.path.join(derived_folder, derived_files.get(brand, ""))
        print("brand:",brand)
        # Find the corresponding file in causal_maps
        main_file = next((f for f in os.listdir(main_folder) if f.startswith(f"KB_")), None)
        if not main_file or not os.path.exists(filtered_json_path):
            print(f"Skipping {brand}: Matching files not found in all folders.")
            continue
        
        main_path = os.path.join(main_folder, main_file)
        output_path = os.path.join(output_folder, f"{brand}_processed.json")
        
        # Run the function
        update_main_json(recreated_path, main_path, filtered_json_path, output_path)
        print(f"Processed: {brand}")

        
# Define folders



# Load the JSON data from files
# with open("recreated.json", "r") as f:
#     recreated_data = json.load(f)

# with open("main.json", "r") as f:
#     main_data = json.load(f)

# # Process and adjust values
# updated_main = adjust_main_values(recreated_data, main_data)

# # Save the updated main.json
# with open("updated_main.json", "w") as f:
#     json.dump(updated_main, f, indent=2)

# print("Updated main.json saved successfully!")
