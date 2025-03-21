import json
import os
import sys

import pandas as pd
import streamlit as st
from backend import read_text_files, return_plot, return_table
from streamlit_option_menu import option_menu

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from main import all_brand_summary
from main2 import all_brand_edit_summary
from overall_main import overall_brand_summary
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
    input_file_name = 'overall_data_new_demand.csv'
    col_list = ['year', 'month', 'channel', 'demand_YoY', 'ATHL_demand_contribution_YoY', 'BR_demand_contribution_YoY', 'ON_demand_contribution_YoY', 'GAP_demand_contribution_YoY']
    overall_brand_summary(year, month, channel, input_file_name,'overall', col_list)

    input_file_name = "Brand_data_mock.csv"
    df=pd.read_csv(input_file_name)
    col_list = ['brand', 'year', 'month', 'channel', 'demand_YoY', 'discount_YoY', 'traffic_YoY', 'AOS_YoY', 'UPT_YoY', 'AUR_YoY', 'conversion_YoY']
    causal_maps_folder = "updated_base_CM"
    importance_mapper_file_name = "discretizer.pkl"
    # all_brand_summary(year, month, channel, input_file_name,causal_maps_folder,col_list)
    all_brand_summary(year, month, channel, input_file_name,importance_mapper_file_name, causal_maps_folder, col_list)
    
    # input_folder = "causal_maps"
    input_folder = 'CM_filtered_suppressed'
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
    importance_mapper_file_name = "discretizer.pkl"
    # all_brand_summary(year, month, channel, input_file_name,causal_maps_folder,col_list,brand_selected)
    all_brand_summary(year, month, channel, input_file_name,importance_mapper_file_name, causal_maps_folder, col_list, brand_selected)
    
    # input_folder = causal_maps_folder
    input_folder = 'recreated_CM_for_graphs'
    output_folder = "graphs"
    plot_function(input_folder, output_folder, brand_selected)

def read_all_json_files(folder="derived"):
    """
    Reads all JSON files from a specified folder and returns their contents as a dictionary
    where keys are filenames and values are the JSON data.

    Args:
        folder (str, optional): The name of the folder containing the files. Defaults to "derived".

    Returns:
        dict: A dictionary containing the content of all JSON files, or an empty dictionary if no JSON files are found.
    """
    all_data = {}

    try:
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                filepath = os.path.join(folder, filename)
                brand_name= filename.split("_filtered_data.json")[0]
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        all_data[brand_name] = data
                except json.JSONDecodeError:
                    print(f"Error: File '{filename}' is not a valid JSON file.")
                except FileNotFoundError:
                    print(f"Error: File '{filename}' not found in folder '{folder}'.")
                except Exception as e:
                    print(f"An error occurred reading {filename}: {e}")

        return all_data

    except FileNotFoundError:
        print(f"Error: Folder '{folder}' not found.")
        return {}
    except Exception as e:
        print(f"An error occurred while reading from folder {folder}: {e}")
        return {}

all_json_data=read_all_json_files()
def read_overall_edit_summary():
    # Define the path to the file
    folder_path = 'overall'
    file_name = 'Overall_edit_summary.txt'
    file_path = os.path.join(folder_path, file_name)

    # Read and return the contents of the file
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File '{file_name}' not found in folder '{folder_path}'."
    except Exception as e:
        return f"An error occurred: {e}"


markdown=read_overall_edit_summary()

with st.sidebar:
    st.image("ui/assets/gap_logo.png", width=140)

    st.divider()
    st.subheader("WBR Summary")
    st.markdown("*Accelerate executive insights to action cycle*")

    selected_tab = option_menu(None, ["WBR Summary", "Analyst WBR edits"],icons=None, menu_icon="cast", default_index=0, orientation="vertical",
                                   styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "0px"},
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"font-size": "15px", "font-weight":"normal"},
    })

col1,col2 = st.columns(2)
with col1:
    st.selectbox("Executive Persona", options=["Executive Persona"], disabled=True, label_visibility="hidden")

with col2:
    st.selectbox("Date range", options=["Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024"],
                 disabled=False, label_visibility="hidden",
                         key="date_range",   # Tie the widget to session state
                         on_change=handle_date_change)  # Trigger function dynamically
# org_level, brand_level = st.tabs(["WBR Summary", "Analyst WBR edits"])



# with org_level:
if selected_tab == "WBR Summary":
    st.subheader("Summary")
    st.markdown(markdown)
    st.divider()
    summaries = read_text_files()
    for key,value in summaries.items():
        st.text_area(label=key, value=value, height=100)


def save_summary(brand, updated_summary):
    folder_path = "edited_summary"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{brand}_edit_summary.txt")

    print(f"Saved the file successfully {brand}_edit_summary.txt")
    with open(file_path, "w") as f:
        f.write(updated_summary)


# with brand_level:
if selected_tab == "Analyst WBR edits":

    table = return_table(all_json_data)
    plot = return_plot()
    summaries = read_text_files()
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
                save_summary(selected_brand, updated_summary)
                handle_brand_change(selected_brand)
                summaries = read_text_files()
                # Close the popover and clear the white overlay
                st.session_state.show_popover = False
                st.rerun()
                st.toast("Changes done successfully")
            if canceled:
                st.session_state.show_popover = False
                st.rerun()
                st.toast("No changes made.")
