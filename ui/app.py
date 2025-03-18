import json
import os
import sys

import pandas as pd
import streamlit as st
from backend import return_plot, return_summary, return_table, update_summary

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from main import all_brand_summary
from main2 import all_brand_edit_summary
from plot import plot_function


# Function to handle date selection
def handle_date_change():
    selected_date = st.session_state.date_range
    st.toast(f"Date selected: {selected_date}")
    # Call your function here
    month, year_str = selected_date.split()
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if month in month_names:
        month=month_names.index(month) + 1
    year = int(year_str)
    channel = 'ONL'
    input_file_name = "Brand_data_mock.csv"
    df=pd.read_csv(input_file_name)
    col_list = ['brand', 'year', 'month', 'channel', 'demand_YoY', 'discount_YoY', 'traffic_YoY', 'AOS_YoY', 'UPT_YoY', 'AUR_YoY', 'conversion_YoY']
    causal_maps_folder = "causal_maps"
    all_brand_summary(year, month, channel, input_file_name,causal_maps_folder,col_list)
    input_folder = "causal_maps"
    output_folder = "graphs"
    plot_function(input_folder,output_folder)

def handle_brand_change(brand_selected):
    selected_date = st.session_state.date_range
    st.toast(f"Date selected: {selected_date}")
    # Call your function here
    month, year_str = selected_date.split()
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if month in month_names:
        month=month_names.index(month) + 1
    year = int(year_str)
    channel = 'ONL'
    input_file_name = "Brand_data_mock.csv"
    df=pd.read_csv(input_file_name)
    col_list = ['brand', 'year', 'month', 'channel', 'demand_YoY', 'discount_YoY', 'traffic_YoY', 'AOS_YoY', 'UPT_YoY', 'AUR_YoY', 'conversion_YoY']
    all_brand_edit_summary(brand_selected)
    causal_maps_folder = "updated_base_CM"
    all_brand_summary(year, month, channel, input_file_name,causal_maps_folder,col_list,brand_selected)
    input_folder = causal_maps_folder
    output_folder = "graphs"
    plot_function(input_folder, output_folder, brand_selected)

with st.sidebar:
    st.image("ui/assets/gap_logo.png", width=140)

    st.divider()
    st.subheader("WBR Summary")
    st.markdown("*Accelerate executive insights to action cycle*")

col1,col2 = st.columns(2)
with col1:
    st.selectbox("Executive Persona", options=["Executive Persona"], disabled=True, label_visibility="hidden")

with col2:
    st.selectbox("Date range", options=["Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024"],
                 disabled=False, label_visibility="hidden",
                         key="date_range",   # Tie the widget to session state
                         on_change=handle_date_change)  # Trigger function dynamically
org_level, brand_level = st.tabs(["WBR Summary", "Analyst WBR edits"])

def read_text_file(filename, folder="edited_summary"):
    """
    Reads a text file from a specified folder and returns its content.

    Args:
        filename (str): The name of the text file.
        folder (str, optional): The name of the folder containing the file. Defaults to "edited_summary".

    Returns:
        str: The content of the file, or None if the file could not be read.
    """
    filepath = os.path.join(folder, filename)
    if "_edit_summary.txt" in filename:
        brand_name= filename.split("_edit_summary.txt")[0]

    try:
        with open(filepath, 'r', encoding='utf-8') as file: #Using utf-8 encoding to avoid encoding issues.
            content = file.read()
            return brand_name,content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found in folder '{folder}'.")
        return brand_name,None
    except Exception as e:
        print(f"An error occurred: {e}")
        return brand_name,None

# brand_1_name,brand_1=read_text_file(filename="Brand_A_edit_summary.txt")
# brand_2_name,brand_2=read_text_file(filename="Brand_B_edit_summary.txt")
# brand_3_name,brand_3=read_text_file(filename="Brand_C_edit_summary.txt")
# brand_4_name,brand_4=read_text_file(filename="Brand_D_edit_summary.txt")

brand_1_name,brand_1=read_text_file(filename="ATHL_edit_summary.txt")
brand_2_name,brand_2=read_text_file(filename="BR_edit_summary.txt")
brand_3_name,brand_3=read_text_file(filename="GAP_edit_summary.txt")
brand_4_name,brand_4=read_text_file(filename="ON_edit_summary.txt")


with org_level:
    st.subheader("Summary")
    # st.markdown("**Org**")
    st.markdown("XYZ Solutions is a technology consulting firm specializing in AI-driven automation and digital transformation. We help businesses streamline operations, enhance efficiency, and drive growth with innovative solutions.")
    st.divider()
    summaries = return_summary(brand_1_name,brand_2_name,brand_3_name,brand_4_name,
                               brand_1,brand_2,brand_3,brand_4)
    for key,value in summaries.items():
        # st.markdown(f"**{key}**")
        # st.write(value)
        st.text_area(label=key, value=value, height=100)


def read_json_file(filename, folder="derived"):
    """
    Reads a JSON file from a specified folder and returns its content as a Python dictionary.

    Args:
        filename (str): The name of the JSON file.
        folder (str, optional): The name of the folder containing the file. Defaults to "derived".

    Returns:
        dict: The content of the JSON file as a dictionary, or None if the file could not be read or parsed.
    """
    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found in folder '{folder}'.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
# brand_1_json = read_json_file(filename="Brand_A_filtered_data.json")
# brand_2_json = read_json_file(filename="Brand_B_filtered_data.json")
# brand_3_json = read_json_file(filename="Brand_C_filtered_data.json")
# brand_4_json = read_json_file(filename="Brand_D_filtered_data.json")

brand_1_json = read_json_file(filename="ATHL_filtered_data.json")
brand_2_json = read_json_file(filename="BR_filtered_data.json")
brand_3_json = read_json_file(filename="GAP_filtered_data.json")
brand_4_json = read_json_file(filename="ON_filtered_data.json")

def save_summary(brand, updated_summary):
    folder_path = "edited_summary"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{brand}_edit_summary.txt")
    
    print(f"Saved the file successfully {brand}_edit_summary.txt")
    with open(file_path, "w") as f:
        f.write(updated_summary)


with brand_level:

    table = return_table(brand_1_name,brand_2_name,brand_3_name,brand_4_name,
                         brand_1_json,brand_2_json,brand_3_json,brand_4_json)
    plot = return_plot(brand_1_name,brand_2_name,brand_3_name,brand_4_name)
    selected_brand = st.selectbox("Select brand",options=summaries.keys())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("KPIs")
        st.dataframe(table[selected_brand])

    with col2:
        st.subheader("Plot")
        st.image(plot[selected_brand], use_container_width=True)

    # st.markdown(summaries[selected_brand])
    st.text_area("Current Summary", value=summaries[selected_brand])

    with st.popover("Modify summary"):
        with st.form("my_form"):
            updated_summary = st.text_area("Current Summary", value=summaries[selected_brand])

            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Submit")
            with col2:
                canceled = st.form_submit_button("Cancel")

            if submitted:
                # Show loading overlay by making screen white
                #st.markdown("""<style>body { background-color: white; }</style>""", unsafe_allow_html=True)
                save_summary(selected_brand, updated_summary)
                handle_brand_change(selected_brand)

                # brand_1_name,brand_1=read_text_file(filename="Brand_A_edit_summary.txt")
                # brand_2_name,brand_2=read_text_file(filename="Brand_B_edit_summary.txt")
                # brand_3_name,brand_3=read_text_file(filename="Brand_C_edit_summary.txt")
                # brand_4_name,brand_4=read_text_file(filename="Brand_D_edit_summary.txt")

                brand_1_name,brand_1=read_text_file(filename="ATHL_edit_summary.txt")
                brand_2_name,brand_2=read_text_file(filename="BR_edit_summary.txt")
                brand_3_name,brand_3=read_text_file(filename="GAP_edit_summary.txt")
                brand_4_name,brand_4=read_text_file(filename="ON_edit_summary.txt")

                summaries = return_summary(brand_1_name,brand_2_name,brand_3_name,brand_4_name,
                               brand_1,brand_2,brand_3,brand_4)
                # Close the popover and clear the white overlay
                st.session_state.show_popover = False
                st.rerun()
                st.toast("Changes done successfully")
            if canceled:
                st.session_state.show_popover = False
                st.rerun()
                st.toast("No changes made.")
