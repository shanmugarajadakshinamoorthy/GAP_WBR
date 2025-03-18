import json
import os

import pandas as pd
import streamlit as st


def return_table(all_brand_data):
    # Define the metrics and map them to their current and YoY values
    metrics_mapping = {
        "AUR": ("AUR", "AUR_YoY"),
        "Demand": ("demand", "demand_YoY"),
        "UPT": ("UPT", "UPT_YoY"),
        "Conversion Rate": ("conversion", "conversion_YoY"),
        "Traffic": ("traffic", "traffic_YoY"),
        "Discount": ("discount", "discount_YoY"),
        "AOS": ("AOS", "AOS_YoY")
    }

    brand_tables = {}

    for brand_name, brand_data in all_brand_data.items():
        # Prepare rows for the DataFrame
        table_data = []
        for metric, (current_key, yoy_key) in metrics_mapping.items():
            current_value = brand_data.get(current_key, 'N/A')
            yoy_value = brand_data.get(yoy_key, 'N/A')
            table_data.append([metric, current_value, yoy_value])

        # Create DataFrame for the current brand
        brand_df = pd.DataFrame(table_data, columns=["Metric", "Current Year", "Change YoY"])
        # Round numeric columns to two decimal places
        brand_df[["Current Year", "Change YoY"]] = brand_df[["Current Year", "Change YoY"]].round(2)

        # Convert DataFrame to JSON
        brand_json = brand_df.to_json(orient='records')

        # Store the brand JSON in the output table
        brand_tables[brand_name] = json.loads(brand_json)

    return brand_tables


def return_plot(graphs_folder="graphs"):
    plot = {}
    os.makedirs(graphs_folder, exist_ok=True)

    # Get all PNG files in the graphs folder and extract brand names
    image_files = {filename.replace(".png", ""): os.path.join(graphs_folder, filename)
                   for filename in os.listdir(graphs_folder) if filename.endswith(".png")}

    # Map the extracted brand names to their corresponding graph images
    for brand_name, image_path in image_files.items():
        plot[brand_name] = image_path

    return plot

def read_text_files(folder="edited_summary"):
    """
    Reads all .txt files in the specified folder and returns a dictionary with brand names as keys and file content as values.

    Args:
        folder (str, optional): The folder containing the text files. Defaults to "edited_summary".

    Returns:
        dict: A dictionary where keys are brand names and values are file contents.
    """
    summaries = {}

    # Iterate through all files in the folder
    for filename in os.listdir(folder):
        if filename.endswith("_edit_summary.txt"):
            brand_name = filename.split("_edit_summary.txt")[0]
            filepath = os.path.join(folder, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    summaries[brand_name] = content
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
                summaries[brand_name] = None

    return summaries

def update_summary(summaries, brand,summary):
    summaries[brand] = summary
    print(summaries)
    st.rerun()
