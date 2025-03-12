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

def return_summary():
    summaries = {
    "brand_1": "Sales increased by 4% due to successful new product launches and targeted marketing campaigns. Customer engagement rose, leading to higher retention rates.",
    "brand_2": "Expanded into three new markets, driving a 12% revenue boost year-over-year. Strengthened supply chain efficiency to support growing demand.",
    "brand_3": "Operational improvements reduced costs by 8%, increasing overall profit margins. Streamlined processes enhanced productivity and resource utilization.",
    "brand_4": "A successful digital transformation led to a 20% rise in online sales. Enhanced user experience and personalized marketing contributed to growth."
    }
    return summaries

def update_summary(summaries, brand,summary):
    summaries[brand] = summary
    print(summaries)
    st.rerun()