import json
import os

import pandas as pd

from step4_summary_to_CM import generate_causal_link
from step5_update_base_CM import process_causal_maps


# def all_brand_edit_summary():
#     folder_path = "edited_summary"
#     output_folder = "updated_base_CM"
#     os.makedirs("recreated_CM", exist_ok=True)
#     os.makedirs(output_folder, exist_ok=True)
#     os.makedirs(folder_path, exist_ok=True)

#     # Iterate through all files in the folder
#     for file_name in os.listdir(folder_path):
#         if file_name.endswith("_edit_summary.txt"):  # Ensure correct file type
#             brand_name = file_name.split("_edit_summary.txt")[0]  # Extract brand name
#             file_path = os.path.join(folder_path, file_name)

#             with open(file_path, "r", encoding="utf-8") as file:
#                 content = file.read()

#             generate_causal_link(content, brand_name)

#     recreated_folder = "recreated_CM"
#     causal_maps_folder = "causal_maps"
#     derived_folder = "derived"
#     output_folder = "updated_base_CM"

#     # Run the process
#     process_causal_maps(recreated_folder, causal_maps_folder, derived_folder, output_folder)


# all_brand_edit_summary()

import os

def all_brand_edit_summary(brand_filter=None):
    folder_path = "edited_summary"
    output_folder = "updated_base_CM"
    os.makedirs("recreated_CM", exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(folder_path, exist_ok=True)

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith("_edit_summary.txt"):  # Ensure correct file type
            brand_name = file_name.split("_edit_summary.txt")[0]  # Extract brand name

            # Apply brand filter if provided
            if brand_filter and brand_name != brand_filter:
                continue

            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            generate_causal_link(content, brand_name)

    recreated_folder = "recreated_CM"
    causal_maps_folder = "causal_maps"
    derived_folder = "derived"
    output_folder = "updated_base_CM"

    # Run the process
    process_causal_maps(recreated_folder, causal_maps_folder, derived_folder, output_folder)
