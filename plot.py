import json
import os

import matplotlib.pyplot as plt
import networkx as nx

# Define input and output folders
input_folder = "Knowledge_base"
output_folder = "graphs"


# def plot_function(input_folder,output_folder):
#     # Ensure the output folder exists
#     os.makedirs(output_folder, exist_ok=True)

#     # Loop through all JSON files in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".json"):  # Process only JSON files
#             input_path = os.path.join(input_folder, filename)

#             # Load JSON data
#             with open(input_path, "r", encoding="utf-8") as file:
#                 causal_map = json.load(file)

#             # Create directed graph
#             G = nx.DiGraph()

#             # Add nodes with attributes
#             for node in causal_map.get("nodes", []):
#                 G.add_node(node["id"], low_pass=node["low_pass"], high_pass=node["high_pass"])

#             # Add edges
#             for edge in causal_map.get("edges", []):
#                 G.add_edge(edge["start"], edge["end"])

#             # Draw graph
#             plt.figure(figsize=(8, 6))
#             pos = nx.spring_layout(G)  # Layout for visualization
#             nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=3000, font_size=10, font_weight="bold")

#             # Save the graph as an image
#             output_path = os.path.join(output_folder, filename.replace("KB_", "").replace(".json", ".png"))
#             plt.savefig(output_path, dpi=300, bbox_inches='tight')
#             plt.close()  # Close the figure to avoid memory issues

#             print(f"Saved: {output_path}")



import json
import os

import matplotlib.pyplot as plt
import networkx as nx

# def plot_function(input_folder, output_folder, brand_filter=None):

#     print("input_folder:", input_folder)
#     print("input_folder:", output_folder)
#     # Ensure the output folder exists
#     os.makedirs(output_folder, exist_ok=True)

#     # Loop through all JSON files in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".json"):  # Process only JSON files
#             brand_name = filename.replace("KB_", "").replace(".json", "")

#             # Apply brand filter if provided
#             if brand_filter and brand_name != brand_filter:
#                 continue

#             input_path = os.path.join(input_folder, filename)

#             # Load JSON data
#             with open(input_path, "r", encoding="utf-8") as file:
#                 causal_map = json.load(file)

#             # Create directed graph
#             G = nx.DiGraph()

#             # Add nodes with attributes
#             for node in causal_map.get("nodes", []):
#                 G.add_node(node["id"], low_pass=node["low_pass"], high_pass=node["high_pass"])

#             # Add edges
#             for edge in causal_map.get("edges", []):
#                 G.add_edge(edge["start"], edge["end"])

#             # Draw graph
#             plt.figure(figsize=(8, 6))
#             pos = nx.spring_layout(G)  # Layout for visualization
#             nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=3000, font_size=10, font_weight="bold")

#             # Save the graph as an image
#             output_path = os.path.join(output_folder, f"{brand_name}.png")
#             plt.savefig(output_path, dpi=300, bbox_inches='tight')
#             plt.close()  # Close the figure to avoid memory issues

#             print(f"Saved: {output_path}")

def plot_function(input_folder, output_folder, brand_filter=None):

    print("input_folder:", input_folder)
    print("output_folder:", output_folder)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all JSON files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):  # Process only JSON files
            brand_name = filename.replace("KB_", "").replace(".json", "")

            # Apply brand filter if provided
            if brand_filter and brand_name != brand_filter:
                continue

            input_path = os.path.join(input_folder, filename)

            # Load JSON data
            with open(input_path, "r", encoding="utf-8") as file:
                causal_map = json.load(file)

            # Create directed graph
            G = nx.DiGraph()

            # Add nodes with attributes
            for node in causal_map.get("nodes", []):
                G.add_node(node["id"], low_pass=node["low_pass"], high_pass=node["high_pass"])

            # Add edges
            for edge in causal_map.get("edges", []):
                G.add_edge(edge["start"], edge["end"])

            # Improved graph visualization
            plt.figure(figsize=(12, 10))  # Increased figure size for better clarity

            # Use spring layout with increased k value for better node spacing
            pos = nx.spring_layout(G, k=0.5, iterations=50)

            nx.draw(
                G, pos, with_labels=True, node_color="lightblue", edge_color="gray",
                node_size=4000, font_size=12, font_weight="bold", arrowsize=20
            )

            # Save the graph as an image
            output_path = os.path.join(output_folder, f"{brand_name}.png")
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()  # Close the figure to avoid memory issues

            print(f"Saved: {output_path}")