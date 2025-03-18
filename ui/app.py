import streamlit as st
from streamlit_option_menu import option_menu

from backend import (
    update_summary,
    return_plot,
    return_summary,
    return_table)



# st.title('WBR')

with st.sidebar:
    st.image("ui/assets/gap_logo.png", width=100)

    st.divider()
    st.subheader("WBR Summary")
    st.markdown("*Accelerate executive insights to action cycle*")
    # org_level, brand_level = st.tabs(["WBR Summary", "Analyst WBR edits"])
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
    st.selectbox("Date range", options=["Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024", "Jan 2025"], disabled=False, label_visibility="hidden")

# org_level, brand_level = st.tabs(["WBR Summary", "Analyst WBR edits"])

# with org_level:
if selected_tab == "WBR Summary":
    st.subheader("Summary")
    # st.markdown("**Org**")
    st.markdown("XYZ Solutions is a technology consulting firm specializing in AI-driven automation and digital transformation. We help businesses streamline operations, enhance efficiency, and drive growth with innovative solutions.")
    st.divider()
    summaries = return_summary()
    for key,value in summaries.items():
        st.markdown(f"**{key}**")
        st.write(value)
            



# with brand_level:
if selected_tab == "Analyst WBR edits":
    summaries = return_summary()
    table = return_table()
    plot = return_plot()
    selected_brand = st.selectbox("Select brand",options=summaries.keys())
    # col1, col2 = st.columns(2)

    # with col1:
    #     st.subheader("KPIs")
    #     st.dataframe(table[selected_brand])

    # with col2:
    #     st.subheader("Plot")
    #     st.image(plot[selected_brand], use_container_width=True)

    st.markdown(summaries[selected_brand])

    with st.popover("Modify summary"):
        with st.form("my_form"):
            updated_summary = st.text_area("Current Summary", value=summaries[selected_brand])

            submitted = st.form_submit_button("Submit")
            if submitted:
                st.toast("Changes made")
