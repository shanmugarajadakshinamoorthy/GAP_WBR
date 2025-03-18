import json
import os

import pandas as pd

from step2_create_fil_CM import process_data
from step3_CM_to_summary import process_causal_maps


def overall_brand_summary(year, month, channel, input_file_name , causal_maps_folder,col_list, brand_selected="All"):
    output_dir = "overall"
    derived_folder = "overall"
    #causal_maps_folder = "causal_maps"
    new_cm_folder = "overall"
    cm_folder = "overall"

    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_file_name)

    filtered_df = df[(df['year'] == year) & (df['month'] == month) & (df['channel'] == channel)]
     # [col_list]
    filtered_df = filtered_df.to_dict(orient='records')

    # Save each row as a separate JSON file
    for row in filtered_df:
        try:
            brand_name = row["brand"].replace(" ", "_")
        except:
            brand_name = "overall"  # Replace spaces with underscores
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

            # Load JSON data
            with open(input_file, "r") as file:
                filtered_df = json.load(file)

            # Call process_data function
            output = process_data(filtered_df, kb_file, output_file)

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
    process_causal_maps(cm_folder, derived_folder, brand_selected, 'overall')

# year = 2024
# month = 9
# channel = 'ONL'
# brand_selected = "All"
# brand_selected = "Brand_B"
# input_file_name = "Brand_data_mock.csv"

# col_list = ['brand', 'year', 'month', 'channel', 'demand_YoY', 'discount_YoY', 'price_YoY', 'traffic_YoY', 'AOS_YoY', 'UPT_YoY', 'AUR_YoY', 'conversion_YoY']
# all_brand_summary(year, month, channel, input_file_name, col_list, brand_selected)

# input_file_name = "overall_data_new_demand.csv"
# col_list = ['year', 'month', 'channel', 'demand_YoY', 'ATHL_demand_contribution_YoY', 'BR_demand_contribution_YoY', 'ON_demand_contribution_YoY', 'GAP_demand_contribution_YoY']
# overall_brand_summary(year, month, channel, input_file_name,'overall', col_list)





