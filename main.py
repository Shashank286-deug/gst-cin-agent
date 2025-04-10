import streamlit as st
import pandas as pd
from gst_lookup import search_gst_and_cin

st.title("GST & CIN Lookup Agent")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["GST"] = ""
    df["CIN"] = ""

    if st.button("Start Lookup"):
        with st.spinner("Fetching data..."):
            for idx, row in df.iterrows():
                gst, cin = search_gst_and_cin(row["Legal Name"])
                df.at[idx, "GST"] = gst
                df.at[idx, "CIN"] = cin

        st.success("Done!")
        st.dataframe(df)

        # Download button
        st.download_button(
            label="Download Result",
            data=df.to_excel(index=False, engine='openpyxl'),
            file_name="output_with_gst_cin.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
