import pandas as pd
import json
import os

# Load DataFrame
df = pd.read_csv("sample_11_3.csv")

# Define causal mappings
causal_mappings = [
    {"source": "discount_YoY", "destination": "demand_YoY"},
    {"source": "traffic_YoY", "destination": "demand_YoY"},
    {"source": "ATV_YoY", "destination": "demand_YoY"},
    {"source": "AUP_YoY", "destination": "ATV_YoY"},
    {"source": "UPT_YoY", "destination": "ATV_YoY"},
]

# Identify numeric columns
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

numeric_cols = [col for col in numeric_cols if "YoY" in col]

# Function to create causal map
def create_causal_map(sub_df, filename):
    nodes = []
    edges = []
    
    # Calculate percentiles for each numeric column
    for col in numeric_cols:
        low, high = sub_df[col].quantile([0.5, 1]).values
        col_id = col.replace("_YoY", "")  # Remove "_YoY" if present
        nodes.append({"id": col_id, "low": round(low, 2), "high": round(high, 2)})
    
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

for brand in df['brand'].unique():
    brand_df = df[df['brand'] == brand]
    filename = os.path.join(output_dir, f"KB_{brand}.json")
    create_causal_map(brand_df, filename)

# Create overall causal map
overall_filename = os.path.join(output_dir, "KB_overall.json")
create_causal_map(df, overall_filename)



filtered_df = df[(df['brand'] == 'ATHL') & (df['year'] == 2023) & (df['month'] == 7) & (df['channel'] == 'ONL')]

# Convert to dictionary
result_dict = filtered_df.to_dict(orient='records')
with open("derived/filtered_df.json", "w") as file:
    json.dump(result_dict, file, indent=4)

print("Causal maps generated successfully!")
