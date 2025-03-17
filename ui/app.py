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


# Function to handle date selection
def handle_date_change():
    selected_date = st.session_state.date_range
    print("I'm running this function")
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
    print(df)
    col_list = ['brand', 'year', 'month', 'channel', 'demand_YoY', 'discount_YoY', 'price_YoY', 'traffic_YoY', 'AOS_YoY', 'UPT_YoY', 'AUR_YoY', 'conversion_YoY']
    print("I'm running this function")
    print("The Year is: ",year)
    print("The Year is: ",month)
    all_brand_summary(year, month, channel, input_file_name, col_list)



with st.sidebar:
    st.image("ui/assets/gap_logo.png", width=100)

    st.divider()
    st.subheader("WBR Summary")
    st.markdown("*Accelerate executive insights to action cycle*")

col1,col2 = st.columns(2)
with col1:
    st.selectbox("Executive Persona", options=["Executive Persona"], disabled=True, label_visibility="hidden")

with col2:
    st.selectbox("Date range", options=["Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024", "Jan 2025"],
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

    try:
        with open(filepath, 'r', encoding='utf-8') as file: #Using utf-8 encoding to avoid encoding issues.
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found in folder '{folder}'.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

brand_1=read_text_file(filename="Brand_A_edit_summary.txt")
brand_2=read_text_file(filename="Brand_B_edit_summary.txt")
brand_3=read_text_file(filename="Brand_C_edit_summary.txt")
brand_4=read_text_file(filename="Brand_D_edit_summary.txt")


with org_level:
    st.subheader("Summary")
    # st.markdown("**Org**")
    st.markdown("XYZ Solutions is a technology consulting firm specializing in AI-driven automation and digital transformation. We help businesses streamline operations, enhance efficiency, and drive growth with innovative solutions.")
    st.divider()
    summaries = return_summary(brand_1,brand_2,brand_3,brand_4)
    for key,value in summaries.items():
        st.markdown(f"**{key}**")
        st.write(value)




with brand_level:

    table = return_table()
    plot = return_plot()
    selected_brand = st.selectbox("Select brand",options=summaries.keys())

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("KPIs")
        st.dataframe(table[selected_brand])

    with col2:
        st.subheader("Plot")
        st.image(plot[selected_brand], use_container_width=True)


    st.markdown(summaries[selected_brand])

    with st.popover("Modify summary"):
        with st.form("my_form"):
            updated_summary = st.text_area("Current Summary", value=summaries[selected_brand])

            submitted = st.form_submit_button("Submit")
            if submitted:
                st.toast("Changes made")
