import pandas as pd
import json
import os

# Load DataFrame
df = pd.read_csv("overall_data_new_demand.csv")

# Define causal mappings
causal_mappings = [
    {"source": "discount_YoY", "destination": "demand_YoY"},
    {"source": "traffic_YoY", "destination": "demand_YoY"},
    {"source": "AOS_YoY", "destination": "demand_YoY"},
    {"source": "AUR_YoY", "destination": "AOS_YoY"},
    {"source": "UPT_YoY", "destination": "AOS_YoY"},
    {"source": "AT_demand_contribution_YoY", "destination": "demand_YoY"},
    {"source": "ON_demand_contribution_YoY", "destination": "demand_YoY"},
    {"source": "GAP_demand_contribution_YoY", "destination": "demand_YoY"},
    {"source": "BR_demand_contribution_YoY", "destination": "demand_YoY"}
    
]

# Identify numeric columns
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

numeric_cols = [col for col in numeric_cols if "YoY" in col]

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
output_dir = "overall"
os.makedirs(output_dir, exist_ok=True)


brand_df = df
filename = os.path.join(output_dir, f"KB_overall.json")
create_causal_map(brand_df, filename, causal_mappings, numeric_cols)

# Create overall causal map
# overall_filename = os.path.join(output_dir, "KB_overall.json")
# create_causal_map(df, overall_filename)




