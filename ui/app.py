import streamlit as st
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

col1,col2 = st.columns(2)
with col1:
    st.selectbox("Executive Persona", options=["Executive Persona"], disabled=True, label_visibility="hidden")

with col2:
    st.selectbox("Date range", options=["Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024", "Jan 2025"], disabled=False, label_visibility="hidden")
org_level, brand_level = st.tabs(["WBR Summary", "Analyst WBR edits"])

with org_level:
    st.subheader("Summary")
    # st.markdown("**Org**")
    st.markdown("XYZ Solutions is a technology consulting firm specializing in AI-driven automation and digital transformation. We help businesses streamline operations, enhance efficiency, and drive growth with innovative solutions.")
    st.divider()
    summaries = return_summary()
    for key,value in summaries.items():
        st.markdown(f"**{key}**")
        st.write(value)
            



with brand_level:

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
