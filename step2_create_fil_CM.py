import json
import pandas as pd

def process_data(filtered_df, kb_file, output_file):
    # Load knowledge base JSON
    with open(kb_file, "r") as f:
        kb_data = json.load(f)

    nodes_kb = {node["id"]: (node["low"], node["high"]) for node in kb_data["nodes"]}
    edges_kb = {(edge["start"], edge["end"]) for edge in kb_data["edges"]}

    # Identify significant variables
    significant_nodes = {}
    data = filtered_df[0]  # Assuming single row
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
            {"id": key, "value": value, "correct": True} for key, value in significant_nodes.items()
        ],
        "edges": significant_edges
    }

    # Save output JSON
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    return output

# Example usage
with open("derived/filtered_df.json", "r") as file:
    filtered_df = json.load(file)

output = process_data(filtered_df, "causal_maps/KB_ATHL.json", "derived/fil_data_causal_map.json")
print(json.dumps(output, indent=2))
