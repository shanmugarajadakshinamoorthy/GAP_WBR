import os
import json
import pickle
import pandas as pd


def fetch_importance_mapper(file_path):
    with open(file_path, "rb") as f:
        mapper = pickle.load(f)
    
    return mapper

def calculate_degree(graph):
    degree = {}
    for node in graph["nodes"]:
        name = node["id"]
        count = len([j for j in graph["edges"] if (j["start"] == name) or (j['end'] == name)])
        degree[name] = count
    
    return degree


def suppress_edges(graph, filtered_df, mapper, metric_type=""):
    """
    Suppresses certain edges from a graph based on node importance and degree criteria.
    Parameters:
    ----------
    graph : dict
        A dictionary containing graph structure with "nodes" and "edges". 
        Each edge should have 'start' and 'end' keys, and each node should have an 'id' key.
    
    filtered_df : pandas.DataFrame
        DataFrame containing importance values associated with nodes. Columns should correspond to node IDs.
    
    mapper : dict
        A dictionary mapping node IDs to importance information, typically pandas Series or objects supporting `.contains()` and `.argmax()` methods.

    metric_type : str, optional (default="")
        Specifies the metric type suffix appended to node IDs when accessing `filtered_df` and `mapper`.
        Acceptable values:
            - ""   : No suffix applied (default behavior).
            - "YoY": Year-over-Year comparison.
            - "LY" : Last Year comparison.    

    Returns:
    -------
    dict
        A dictionary containing the updated graph structure with:
        - "nodes": List of nodes after removing nodes with zero degree.
        - "edges": List of edges after removing suppressed edges.
    """

    edge_drop = []
    drop_nodes = []

    degree = calculate_degree(graph)
    # # print("old degree:", degree)
    degree = {k:v for k, v in degree.items()}

    suffix = "" if not metric_type else f"_{metric_type}"

    removal_pairs = []
    for node in graph['nodes']:
        name = node['id']
        
        name_val = filtered_df[f"{name}{suffix}"]
        name_pri = mapper[name].contains(abs(name_val)).argmax()
        if name_pri < 2:
            continue

        start_nodes = []
        for link in graph['edges']:
            if link['end'] == name:
                start = link['start']
                start_val = filtered_df[f"{start}{suffix}"]
                pri = mapper[start].contains(abs(start_val)).argmax()
                start_nodes.append((start, pri))
                # # print("Node Priority for edge(start end):",start, pri, name, name_pri)
        all_pairs = [(j[0], j[1], k[0], k[1], k[1]-j[1]) for j in start_nodes for k in start_nodes]
        elimination_pairs = [j for j in all_pairs if j[-1] == 2]
        
        elimination_start_nodes = list(set([j[0] for j in elimination_pairs]))
        # # print("Edges to be removed:", name, elimination_start_nodes)
        removal_pairs.extend([(name, j) for j in elimination_start_nodes])
    
    removal_pairs = set(removal_pairs)
    

    remove_link_flag = []
    
    for link in graph['edges']:
        if (link['end'], link['start']) in removal_pairs:
            remove_link_flag.append(True)
        else:
            remove_link_flag.append(False)

    graph['edges'] = [j for j, k in zip(graph['edges'], remove_link_flag) if not k]

    degree_new = calculate_degree(graph)
    # # print("new degree:", degree_new)
    remove_node_flag = []

    for node in degree_new:
        if degree_new[node] == 0 and degree[node] != 0:
            remove_node_flag.append(True)
        else:
            remove_node_flag.append(False)
    
    graph['nodes'] = [j for j, k in zip(graph['nodes'], remove_node_flag) if not k]

    return graph


if __name__ == "__main__":

    cm_path = "D:\\GAP_WBR-main\\GAP_WBR-version_3 (1)\\GAP_WBR-version_3\\CM_filtered\\"
    data_path = "D:\\GAP_WBR-main\\GAP_WBR-version_3 (1)\\GAP_WBR-version_3\\derived\\"
    mapper = fetch_importance_mapper("discretizer.pkl")

    with open(os.path.join(cm_path, "ATHL_causal_map.json"), 'r') as f:
        causal_map = json.load(f)
    
    with open(os.path.join(data_path, "ATHL_filtered_data.json"), 'r') as f:
        filtered_df = json.load(f)
    
    # print()
    # # print(mapper)
    
    # # print(mapper['demand'].contains(50000000000))
    filtered_df['demand_YoY'] = 50000000000000
    filtered_df['AOS_YoY'] = 50000000000000
    # print(causal_map)
    # print()
    # print(suppress_edges(causal_map, filtered_df, mapper, "YoY"))