import json
import pandas as pd
import os

def process_data(filtered_df, kb_file, output_file):
    # Load knowledge base JSON
    with open(kb_file, "r") as f:
        kb_data = json.load(f)

    nodes_kb = {node["id"]: (node["low"], node["high"]) for node in kb_data["nodes"]}
    edges_kb = {(edge["start"], edge["end"]) for edge in kb_data["edges"]}

    # Identify significant variables
    significant_nodes = {}
    data = filtered_df  # Assuming single row
    for key, value in data.items():
        if value is None or key.replace("_YoY", "") not in nodes_kb:
            continue
        
        node_key = key.replace("_YoY", "")
        low, high = nodes_kb[node_key]
        if low <= value <= high:
            significant_nodes[node_key] = value

    # Identify significant edges
    significant_edges = []
    for start, end in edges_kb:
        if start in significant_nodes and end in significant_nodes:
            significant_edges.append({
                "start": start,
                "end": end,
                "value": significant_nodes[start]
            })

    # Format output
    output = {
        "nodes": [
            {"id": key, "value": value} for key, value in significant_nodes.items()
        ],
        "edges": significant_edges
    }

    # Save output JSON
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    return output

# Example usage
# with open("derived/filtered_df.json", "r") as file:
#     filtered_df = json.load(file)

# output = process_data(filtered_df, "causal_maps/KB_Brand A.json", "derived/fil_data_causal_map.json")
# print(json.dumps(output, indent=2))

derived_folder = "derived"
causal_maps_folder = "causal_maps"
new_cm_folder = "CM_filtered"

os.makedirs(new_cm_folder, exist_ok=True)

# Loop through all JSON files in the derived folder
for filename in os.listdir(derived_folder):
    if filename.endswith("_filtered_data.json"):
        brand_name = filename.split("_filtered")[0]  # Extract brand name (Brand_A, Brand_B, etc.)

        # Construct file paths
        input_file = os.path.join(derived_folder, filename)
        kb_file = os.path.join(causal_maps_folder, f"KB_{brand_name.replace("Brand_", "Brand ")}.json")
        output_file = os.path.join(new_cm_folder, f"{brand_name}_causal_map.json")

        print(input_file)
        print(kb_file)
        print(output_file)
    
        # Load JSON data
        with open(input_file, "r") as file:
            filtered_df = json.load(file)

        # Call process_data function
        output = process_data(filtered_df, kb_file, output_file)

        # Print output
        # print(f"Processed {filename} -> {output_file}")
        # print(json.dumps(output, indent=2))
