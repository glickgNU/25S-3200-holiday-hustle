import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Download Reports Page')

# Carlos-5: Export user selections
st.subheader(" Export All User Selections")
try:
    response = requests.get("http://api:4000/fda/personalized_suggestions/export")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download User Selections (CSV)",
        data=csv,
        file_name="user_selections.csv",
        mime="text/csv"
    )
except Exception as e:
    st.error(f"Failed to load export data: {e}")