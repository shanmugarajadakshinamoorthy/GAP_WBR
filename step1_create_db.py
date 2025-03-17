import json
import os

import pandas as pd


# Function to create causal map
def create_causal_map(sub_df, filename, causal_mappings, numeric_cols):
    nodes = []
    edges = []

    # Calculate percentiles for each numeric column
    for col in numeric_cols:
        low, high = sub_df[col].quantile([0.4,0.7]).values
        col_id = col.replace("_YoY", "")  # Remove "_YoY" if present
        nodes.append({"id": col_id, "low_pass": round(low, 2), "high_pass": round(high, 2)})

    # Create edges based on causal mappings
    for mapping in causal_mappings:
        edges.append({"start": mapping["source"].replace("_YoY", ""), "end": mapping["destination"].replace("_YoY", "")})

    causal_map = {"nodes": nodes, "edges": edges}

    # Save as JSON file
    with open(filename, "w") as f:
        json.dump(causal_map, f, indent=2)

# Create directory for outputs
output_dir = "causal_maps"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv("Brand_data_mock.csv")

# Identify numeric columns
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
numeric_cols = [col for col in numeric_cols if "YoY" in col]

# causal_mappings = [
#     {"source": "discount_YoY", "destination": "demand_YoY"},
#     # {"source": "traffic_YoY", "destination": "demand_YoY"},
#     {"source": "AOS_YoY", "destination": "demand_YoY"},
#     {"source": "AUR_YoY", "destination": "AOS_YoY"},
#     {"source": "UPT_YoY", "destination": "AOS_YoY"},
#     {"source": "traffic_YoY", "destination": "conversion_YoY"},
#     {"source": "orders_YoY", "destination": "conversion_YoY"},

# ]
causal_mappings = [
    {"source": "orders_YoY", "destination": "demand_YoY"},
    {"source": "AOS_YoY", "destination": "demand_YoY"},
    {"source": "AUR_YoY", "destination": "demand_YoY"},
    {"source": "UPT_YoY", "destination": "AOS_YoY"},
    {"source": "traffic_YoY", "destination": "conversion_YoY"},
    {"source": "orders_YoY", "destination": "conversion_YoY"},
    {"source": "discount_YoY", "destination": "AUR_YoY"}
]
for brand in df['brand'].unique():
    brand_df = df[df['brand'] == brand]
    brand=brand.replace(" ","_")
    filename = os.path.join(output_dir, f"KB_{brand}.json")
    create_causal_map(brand_df, filename, causal_mappings, numeric_cols)

# Create overall causal map
# overall_filename = os.path.join(output_dir, "KB_overall.json")
# overall = pd.read_csv(overall_filename)
# numeric_cols = overall.select_dtypes(include=['number']).columns.tolist()
# numeric_cols = [col for col in numeric_cols if "YoY" in col]

# causal_mappings = [
#     {"source": "discount_YoY", "destination": "demand_YoY"},
#     # {"source": "traffic_YoY", "destination": "demand_YoY"},
#     {"source": "AOS_YoY", "destination": "demand_YoY"},
#     {"source": "AUR_YoY", "destination": "AOS_YoY"},
#     {"source": "UPT_YoY", "destination": "AOS_YoY"},
#     {"source": "traffic_YoY", "destination": "conversion_YoY"},
#     {"source": "orders_YoY", "destination": "conversion_YoY"},

# ]
# create_causal_map(overall, overall_filename, causal_mappings, numeric_cols)




