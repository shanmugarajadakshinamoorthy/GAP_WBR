import os

import streamlit as st


def return_table():
    table = {
        "brand_1": {
            "AUR": "$5",
            "Sales": "$500000",
            "UPT": "1.5",
            "Conversion Rate": "3.0%",
            "Traffic": "60000"
        },
        "brand_2": {
            "AUR": "$6",
            "Sales": "$300000",
            "UPT": "1.2",
            "Conversion Rate": "2.0%",
            "Traffic": "45000"
        },
        "brand_3": {
            "AUR": "$4.5",
            "Sales": "$350000",
            "UPT": "1.4",
            "Conversion Rate": "2.8%",
            "Traffic": "52000"
        },
        "brand_4": {
            "AUR": "$5.5",
            "Sales": "$450000",
            "UPT": "1.6",
            "Conversion Rate": "3.2%",
            "Traffic": "58000"
        }
    }

    return table
def return_plot():
    plot= {
        "brand_1": "https://dummyimage.com/600x400/000/fff&text=Sample+Graph",
        "brand_2": "https://dummyimage.com/600x400/000/fff&text=Sample+Graph",
        "brand_3": "https://dummyimage.com/600x400/000/fff&text=Sample+Graph",
        "brand_4": "https://dummyimage.com/600x400/000/fff&text=Sample+Graph"
    }

    return plot



def return_summary(brand_1,brand_2,brand_3,brand_4):
    summaries = {
    "brand_1": brand_1,
    "brand_2": brand_2,
    "brand_3":brand_3,
    "brand_4":brand_4
    }
    return summaries

def update_summary(summaries, brand,summary):
    summaries[brand] = summary
    print(summaries)
    st.rerun()