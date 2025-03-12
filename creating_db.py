import pandas as pd
import json

# Sample DataFrame (replace with actual data loading)
df = pd.read_csv("sample_11_3.csv")

# Define causal mappings
causal_mappings = [
    {"source": "discount_YoY", "destination": "demand_YoY"},
    {"source": "traffic_YoY", "destination": "demand_YoY"},
    {"source": "AUP_YoY", "destination": "demand_YoY"},
    {"source": "UPT_YoY", "destination": "ATV_YoY"},
]

# Function to check if a column is numeric
def is_numeric(series):
    return pd.api.types.is_numeric_dtype(series)

def json_structural_data(df, causal_mappings, user_id="overall"):
    output_data = []
    
    # Process each brand separately
    for brand, brand_df in df.groupby("brand"):
        mappings = []
        
        for mapping in causal_mappings:
            source = mapping["source"]
            destination = mapping["destination"]
            
            if source in brand_df.columns and destination in brand_df.columns:
                filtered_df = brand_df.dropna(subset=[source, destination])
                
                if not filtered_df.empty:
                    if is_numeric(filtered_df[source]):
                        low = filtered_df[source].quantile(0.10)
                        high = filtered_df[source].quantile(0.90)
                    else:
                        low = filtered_df[source].value_counts().idxmin()
                        high = filtered_df[source].value_counts().idxmax()
                    
                    mappings.append({
                        "source": source,
                        "destination": destination,
                        "low": low,
                        "high": high
                    })
        
        output_data.append({
            "user_id": user_id,
            "brand_name": str(brand),
            "mappings": mappings
        })
    
    # Process overall data without brand filtering
    overall_mappings = []
    for mapping in causal_mappings:
        source = mapping["source"]
        destination = mapping["destination"]
        
        if source in df.columns and destination in df.columns:
            filtered_df = df.dropna(subset=[source, destination])
            
            if not filtered_df.empty:
                if is_numeric(filtered_df[source]):
                    low = filtered_df[source].quantile(0.10)
                    high = filtered_df[source].quantile(0.90)
                else:
                    low = filtered_df[source].value_counts().idxmin()
                    high = filtered_df[source].value_counts().idxmax()
                
                overall_mappings.append({
                    "source": source,
                    "destination": destination,
                    "low": low,
                    "high": high
                })
    
    output_data.append({
        "user_id": user_id,
        "brand_name": "overall",
        "mappings": overall_mappings
    })
    
    # Convert to JSON
    json_output = json.dumps(output_data, indent=4)
    with open("derived/db_json.json", "w") as file:
        file.write(json_output)
    
    print("JSON file saved successfully.")
    return json_output

(json_structural_data(df,causal_mappings,user_id="overall"))


filtered_df = df[(df['brand'] == 'ATHL') & (df['year'] == 2023) & (df['month'] == 7) & (df['channel'] == 'ONL')]

# Convert to dictionary
result_dict = filtered_df.to_dict(orient='records')
with open("derived/filtered_df.json", "w") as file:
    json.dump(result_dict, file, indent=4)

print("Dictionary saved as JSON successfully.")
