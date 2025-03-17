import json
import os

import streamlit as st


def return_table(brand_1_name,brand_2_name,brand_3_name,brand_4_name,
                 brand_1,brand_2,brand_3,brand_4):
    table = {
        brand_1_name: {
            "AUR": brand_1["AUR_YoY"],
            "Sales": brand_1["demand_YoY"],
            "UPT": brand_1["UPT_YoY"],
            "Conversion Rate": brand_1["conversion_YoY"],
            "Traffic": brand_1["traffic_YoY"],
            "Discount":brand_1["discount_YoY"],
            # "Price":brand_1["price_YoY"],
            "AOS":brand_1["AOS_YoY"]
        },
        brand_2_name: {
            "AUR": brand_2["AUR_YoY"],
            "Sales": brand_2["demand_YoY"],
            "UPT": brand_2["UPT_YoY"],
            "Conversion Rate": brand_2["conversion_YoY"],
            "Traffic": brand_2["traffic_YoY"],
            "Discount":brand_1["discount_YoY"],
            # "Price":brand_1["price_YoY"],
            "AOS":brand_1["AOS_YoY"]
        },
        brand_3_name: {
            "AUR": brand_3["AUR_YoY"],
            "Sales": brand_3["demand_YoY"],
            "UPT": brand_3["UPT_YoY"],
            "Conversion Rate": brand_3["conversion_YoY"],
            "Traffic": brand_3["traffic_YoY"],
            "Discount":brand_1["discount_YoY"],
            # "Price":brand_1["price_YoY"],
            "AOS":brand_1["AOS_YoY"]
        },
        brand_4_name: {
            "AUR": brand_4["AUR_YoY"],
            "Sales": brand_4["demand_YoY"],
            "UPT": brand_4["UPT_YoY"],
            "Conversion Rate": brand_4["conversion_YoY"],
            "Traffic": brand_4["traffic_YoY"],
            "Discount":brand_1["discount_YoY"],
            # "Price":brand_1["price_YoY"],
            "AOS":brand_1["AOS_YoY"]
        }
    }
    return table



# def return_plot(brand_1_name,brand_2_name,brand_3_name,brand_4_name):
#     plot= {
#         brand_1_name: "https://dummyimage.com/600x400/000/fff&text=Sample+Graph",
#         brand_2_name: "https://dummyimage.com/600x400/000/fff&text=Sample+Graph",
#         brand_3_name: "https://dummyimage.com/600x400/000/fff&text=Sample+Graph",
#         brand_4_name: "https://dummyimage.com/600x400/000/fff&text=Sample+Graph"
#     }
#     return plot

def return_plot(brand_1_name, brand_2_name, brand_3_name, brand_4_name):
    graphs_folder = "graphs"
    plot = {}
    os.makedirs(graphs_folder, exist_ok=True)
    # Get all PNG files in the graphs folder
    image_files = {filename.replace(".png", ""): os.path.join(graphs_folder, filename)
                   for filename in os.listdir(graphs_folder) if filename.endswith(".png")}

    # Map the given brand names to their corresponding graph images (if available)
    for brand_name in [brand_1_name, brand_2_name, brand_3_name, brand_4_name]:
        plot[brand_name] = image_files.get(brand_name, "Image Not Found")

    return plot

def return_summary(brand_1_name,brand_2_name,brand_3_name,brand_4_name,
                               brand_1,brand_2,brand_3,brand_4):
    summaries = {
    brand_1_name: brand_1,
    brand_2_name: brand_2,
    brand_3_name:brand_3,
    brand_4_name:brand_4
    }
    return summaries

def update_summary(summaries, brand,summary):
    summaries[brand] = summary
    print(summaries)
    st.rerun()
