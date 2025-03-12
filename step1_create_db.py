import pandas as pd
import json
import os

# Load DataFrame
df = pd.read_csv("all_brand_mock_data (1).csv")

# Define causal mappings
causal_mappings = [
    {"source": "discount_YoY", "destination": "demand_YoY"},
    {"source": "traffic_YoY", "destination": "demand_YoY"},
    {"source": "AOS_YoY", "destination": "demand_YoY"},
    {"source": "AUR_YoY", "destination": "AOS_YoY"},
    {"source": "UPT_YoY", "destination": "AOS_YoY"},
    {"source": "traffic_YoY", "destination": "conversion_YoY"},
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



# # filtered_df = df[(df['brand'] == 'Brand A') & (df['year'] == 2024) & (df['month'] == 9) & (df['channel'] == 'ONL')]
filtered_df = df[(df['year'] == 2024) & (df['month'] == 9) & (df['channel'] == 'ONL')][['brand', 'year', 'month', 'channel', 'demand_YoY', 'discount_YoY', 'price_YoY', 'traffic_YoY', 'AOS_YoY', 'UPT_YoY', 'AUR_YoY', 'conversion_YoY']]
filtered_df = filtered_df.to_dict(orient='records')
# # Convert to dictionary
# result_dict = filtered_df.to_dict(orient='records')
# with open("derived/filtered_df.json", "w") as file:
#     json.dump(result_dict, file, indent=4)

# print("Causal maps generated successfully!")

output_dir = "derived"
os.makedirs(output_dir, exist_ok=True)

# Save each row as a separate JSON file
for row in filtered_df:
    brand_name = row["brand"].replace(" ", "_")  # Replace spaces with underscores
    file_name = f"{output_dir}/{brand_name}_filtered_data.json"
    
    with open(file_name, "w") as file:
        json.dump(row, file, indent=4)
    
    print(f"Saved: {file_name}")
