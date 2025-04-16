import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('View User Complaints Page')

# Add a button to fetch complaints
if st.button("Fetch Complaints"):

    response = requests.get('http://api:4000/u/users/complaints/get')

    # display the complaints
    if response.status_code == 200:
        complaints = response.json()

        # Loop through each complaint and display the information
        for complaint in complaints:
            st.write(f"Complaint ID: {complaint['ComplaintID']}")
            st.write(f"Complaint Text: {complaint['ComplaintText']}")
            st.write(f"User ID: {complaint['UserID']}")
            st.write(f"App ID: {complaint['AppID']}")
            st.write("----")
    else:
        st.error(f"Failed to retrieve complaints data.")
