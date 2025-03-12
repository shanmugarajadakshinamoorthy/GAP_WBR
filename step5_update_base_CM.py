import json
import re
import os

def extract_percentage(value_str):
    match = re.search(r"([-+]?[0-9]*\.?[0-9]+)%", value_str)
    return float(match.group(1)) if match else None

def adjust_main_values(recreated, main):
    # Create a lookup for main nodes by ID
    main_nodes = {node["id"].lower(): node for node in main["nodes"]}
    
    for edge in recreated["edges"]:
        start = edge["start"].lower()
        value = extract_percentage(edge["value"])
        
        if value is not None and start in main_nodes:
            node = main_nodes[start]
            if value < node["low"]:
                node["low"] = value
            if value > node["high"]:
                node["high"] = value
    print(node)
    print(main_nodes)
    return main


def extract_brand_name(filename):
    """Extract brand name from filename using regex."""
    match = re.search(r'Brand[_ ]([A-Za-z]+)', filename)
    return match.group(1) if match else None

def process_files(recreated_folder, causal_maps_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    recreated_files = {extract_brand_name(f): os.path.join(recreated_folder, f) for f in os.listdir(recreated_folder) if f.endswith('.json')}
    causal_files = {extract_brand_name(f): os.path.join(causal_maps_folder, f) for f in os.listdir(causal_maps_folder) if f.endswith('.json')}
    
    for brand, recreated_path in recreated_files.items():
        causal_path = causal_files.get(brand)
        if causal_path:
            with open(recreated_path, 'r') as f:
                recreated_data = json.load(f)
            with open(causal_path, 'r') as f:
                main_data = json.load(f)
            
            updated_main = adjust_main_values(recreated_data, main_data)
            output_file = os.path.join(output_folder, f"Updated_Brand_{brand}.json")
            with open(output_file, 'w') as f:
                json.dump(updated_main, f, indent=2)
            print(f"Updated {output_file} saved successfully!")
        else:
            print(f"No matching file found for Brand {brand}")

# Define folders
recreated_folder = "recreated_CM"
causal_maps_folder = "causal_maps"
output_folder = "updated_base_CM"

# Run the process
process_files(recreated_folder, causal_maps_folder, output_folder)


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
