import json
import pandas as pd


with open("derived/filtered_df.json", "r") as file:
    filtered_df = json.load(file)

# print("filtered_df:", filtered_df)
df = pd.DataFrame(filtered_df)

# Causal mappings
causal_mappings = [
    {"source": "discount_YoY", "destination": "demand_YoY"},
    {"source": "traffic_YoY", "destination": "demand_YoY"},
    {"source": "AUP_YoY", "destination": "demand_YoY"},
    {"source": "UPT_YoY", "destination": "ATV_YoY"},
]

# Mapping of column names to required IDs
node_names = {
    "discount_YoY": "Promotion",
    "AUP_YoY": "AUP",
    "UPT_YoY": "UPT",
    "demand_YoY": "Demand",
    "ATV_YoY": "ATV",
    "traffic_YoY": "Traffic"
}

# Extract nodes
nodes = []
for col, node_id in node_names.items():
    if col in df.columns and pd.notna(df[col][0]):
        nodes.append({
            "id": node_id,
            "value": round(df[col][0], 1),
            "correct": True
        })

# Extract edges
edges = []
for mapping in causal_mappings:
    source_col = mapping["source"]
    dest_col = mapping["destination"]
    
    if source_col in df.columns and dest_col in df.columns and pd.notna(df[source_col][0]):
        edges.append({
            "start": node_names[source_col],
            "end": node_names[dest_col],
            "value": round(df[source_col][0], 1),
        })

# Create the causal mapping JSON
causal_mapping_json = {
    "nodes": nodes,
    "edges": edges
}

# Print or save the JSON
json_output = (json.dumps(causal_mapping_json, indent=2))

with open("derived/fil_data_causal_map.json", "w") as file:
    file.write(json_output)

    print("JSON file saved successfully.")
