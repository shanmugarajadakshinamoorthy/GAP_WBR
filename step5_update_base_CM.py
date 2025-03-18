import json
import os
import re

def add_missing_edges(recreated_cm, main):
    # Extract existing edges from main
    
    existing_edges = {(edge["start"], edge["end"]) for edge in main["edges"]}
    
    # Extract node IDs from main
    main_nodes = {node["id"] for node in main["nodes"]}
    
    # Iterate over edges in recreated_cm
    for edge in recreated_cm["edges"]:
        start, end = edge["start"], edge["end"]
        
        # Check if edge is missing but both nodes exist in main
        if (start, end) not in existing_edges and start in main_nodes and end in main_nodes:
            main["edges"].append({"start": start, "end": end})
            print("inside add_missing_edges", start, end)
    
    return main

def update_main_json(recreated_path, main_path, filtered_json_path, output_path):
    # Load the JSON data
    with open(recreated_path) as f:
        recreated = json.load(f)
    with open(main_path) as f:
        main = json.load(f)
    with open(filtered_json_path) as f:
        filtered_json = json.load(f)

    main = add_missing_edges(recreated, main)
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
    # print("filtered_values:", filtered_values)
    # Extract "start" nodes from recreated edges
    # start_nodes = {edge["start"] for edge in recreated["edges"]}
    start_nodes = {edge["start"] for edge in recreated["edges"]} | {edge["end"] for edge in recreated["edges"]}


    # Update low and high values in main.json
    for node in main["nodes"]:
        node_id = node["id"]
        if node_id in filtered_values and filtered_values[node_id] is not None:
            value = filtered_values[node_id]
            
            if node_id == 'demand':
                pass
            elif node_id in start_nodes:  # Directly present in recreated edges
                if node["low_pass"] < value < node["high_pass"]:
                    print(f"value inside band pass for {node_id}")
                    low_diff = abs(value - node["low_pass"])
                    high_diff = abs(value - node["high_pass"])
                    if low_diff < high_diff:
                        node["low_pass"] = value
                    else:
                        node["high_pass"] = value
            else:  # Not in start_nodes, adjust based on closest boundary
  
                if value < node["low_pass"]:
                    node["low_pass"] = value
                elif value > node["high_pass"]:
                    node["high_pass"] = value

    # Save the updated main.json
    with open(output_path, "w") as f:
        json.dump(main, f, indent=2)

    print(f"Updated main.json has been saved to {output_path}.")



def process_causal_maps(recreated_folder, main_folder, derived_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(derived_folder, exist_ok=True)

    # Get file lists from recreated_CM and derived folders
    recreated_files = {f.replace("_recreated_CM.json", ""): f for f in os.listdir(recreated_folder) if f.endswith("_recreated_CM.json")}
    derived_files = {f.replace("_filtered_data.json", ""): f for f in os.listdir(derived_folder) if f.endswith("_filtered_data.json")}

    # Loop through recreated_CM files
    for brand, recreated_file in recreated_files.items():
        recreated_path = os.path.join(recreated_folder, recreated_file)
        filtered_json_path = os.path.join(derived_folder, derived_files.get(brand, ""))
        # print("brand:",brand)
        key = f"KB_{brand}"
        # Find the corresponding file in causal_maps
        main_file = next((f for f in os.listdir(main_folder) if f.startswith(key)), None)
        if not main_file or not os.path.exists(filtered_json_path):
            print(f"Skipping {brand}: Matching files not found in all folders.")
            continue

        main_path = os.path.join(main_folder, main_file)
        output_path = os.path.join(output_folder, f"KB_{brand}.json")

        # Run the function

        update_main_json(recreated_path, main_path, filtered_json_path, output_path)
        # print(f"Processed: {brand}")


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
