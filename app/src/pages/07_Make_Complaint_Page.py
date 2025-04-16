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
st.header('Make Complaint Page')


complaint_input = st.text_input("Your Complaint: ")

# Create a multiple selection box
common_complaints = st.multiselect(
"Choose as many complaints:",
["Too many adds", "Too laggy", "Not enough suggestions", "Suggestions are not helpful enough", "too difficult to narrow search"])



# Press to send the complaint
if st.button("Send complaint to app" ,type='primary',
             use_container_width=True):
             results = requests.get(f'http://api:4000/u/users/complaints{complaint_input}/{common_complaints}').json()
             st.dataframe(results)
             print(f"Sending selected options: {common_complaints}")
             st.write("You wrote:", complaint_input)
             print(f"Sending input: {complaint_input}")

             
