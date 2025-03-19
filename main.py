import json
import os

import pandas as pd

from step2_create_fil_CM import process_data
from step2b_create_updated_CM import fetch_importance_mapper, calculate_degree, suppress_edges
from step3_CM_to_summary import process_causal_maps


# , col_list, brand_selected, input_file_name

def all_brand_summary(year, month, channel, input_file_name, importance_mapper_file_name , causal_maps_folder,col_list, brand_selected="All", metric_type=""):
    output_dir = "derived"
    derived_folder = "derived"
    # causal_maps_folder = "causal_maps"
    new_cm_folder = "CM_filtered"
    cm_folder = "CM_filtered"
    cm_suppressed_folder = "CM_filtered_suppressed"

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("summary", exist_ok=True)
    os.makedirs("edited_summary", exist_ok=True)
    os.makedirs(new_cm_folder, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(cm_suppressed_folder, exist_ok=True)


    df = pd.read_csv(input_file_name)

    importance_mapper = fetch_importance_mapper(importance_mapper_file_name)

    # # filtered_df = df[(df['brand'] == 'Brand A') & (df['year'] == 2024) & (df['month'] == 9) & (df['channel'] == 'ONL')]
    # filtered_df = df[(df['year'] == 2024) & (df['month'] == 9) & (df['channel'] == 'ONL')][['brand', 'year', 'month', 'channel', 'demand_YoY', 'discount_YoY', 'price_YoY', 'traffic_YoY', 'AOS_YoY', 'UPT_YoY', 'AUR_YoY', 'conversion_YoY']]
    filtered_df = df[(df['year'] == year) & (df['month'] == month) & (df['channel'] == channel)]
    # filtered_df = filtered_df.loc[:, ~filtered_df.columns.str.contains(r'\bprice\b', case=False, regex=True)]
    # [col_list]
    filtered_df = filtered_df.to_dict(orient='records')

    # Save each row as a separate JSON file
    for row in filtered_df:
        try:
            brand_name = row["brand"].replace(" ", "_")
        except:
            brand_name = "Overall"  # Replace spaces with underscores
        file_name = f"{output_dir}/{brand_name}_filtered_data.json"

        with open(file_name, "w") as file:
            json.dump(row, file, indent=4)

        print(f"Saved: {file_name}")



    filtered_files = [
        filename for filename in os.listdir(derived_folder)
        if filename.endswith("_filtered_data.json") and (not brand_selected or filename.startswith(brand_selected))
    ]
    print("filtered_files:",filtered_files)
    if len(filtered_files) == 0:
        filtered_files = os.listdir(derived_folder)
    # Loop through all JSON files in the derived folder
    for filename in filtered_files:
        if filename.endswith("_filtered_data.json"):
            brand_name = filename.split("_filtered")[0]  # Extract brand name (Brand_A, Brand_B, etc.)
            #brand_name=brand_name.replace("Brand_", "Brand ")

            # Construct file paths
            input_file = os.path.join(derived_folder, filename)
            kb_file = os.path.join(causal_maps_folder, f"KB_{brand_name}.json")
            output_file = os.path.join(new_cm_folder, f"{brand_name}_causal_map.json")
            suppressed_output_file = os.path.join(cm_suppressed_folder, f"{brand_name}_causal_map_suppressed.json")
            # Load JSON data
            with open(input_file, "r") as file:
                filtered_df = json.load(file)

            # Call process_data function
            output = process_data(filtered_df, kb_file, output_file)

            suppressed_output = suppress_edges(output, filtered_df, importance_mapper, metric_type)

            with open(suppressed_output_file, 'w') as f:
                json.dump(suppressed_output, f)

    # for filename in os.listdir(derived_folder):
    #     if filename.endswith("_filtered_data.json"):
    #         brand_name = filename.split("_filtered")[0]  # Extract brand name (Brand_A, Brand_B, etc.)

    #         # Apply brand filter if provided
    #         if brand_selected and brand_name != brand_selected:
    #             continue

    #         # Construct file paths
    #         input_file = os.path.join(derived_folder, filename)
    #         kb_file = os.path.join(causal_maps_folder, f"KB_{brand_name}.json")
    #         output_file = os.path.join(new_cm_folder, f"{brand_name}_causal_map.json")

    #         # Load JSON data
    #         with open(input_file, "r") as file:
    #             filtered_df = json.load(file)

    #         # Call process_data function
    #         output = process_data(filtered_df, kb_file, output_file)


    # Example usage
    process_causal_maps(cm_suppressed_folder, derived_folder, brand_selected)

# year = 2024
# month = 9
# channel = 'ONL'
brand_selected = "All"
# brand_selected = "Brand_B"
# input_file_name = "Brand_data_mock.csv"

# col_list = ['brand', 'year', 'month', 'channel', 'demand_YoY', 'discount_YoY', 'price_YoY', 'traffic_YoY', 'AOS_YoY', 'UPT_YoY', 'AUR_YoY', 'conversion_YoY']
# all_brand_summary(year, month, channel, input_file_name, col_list, brand_selected)

# input_file_name = "overall_data_new_demand.csv"
# col_list = ['year', 'month', 'channel', 'demand_YoY', 'ATHL_demand_contribution_YoY', 'BR_demand_contribution_YoY', 'ON_demand_contribution_YoY', 'GAP_demand_contribution_YoY']
# all_brand_summary(year, month, channel, input_file_name, col_list)





