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


file_path_add_complaint = '''C:api\backend\users\users\complaints.py'''
# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Make Complaint Page')


# Create a complaint here
complaint_input = st.text_input(file_path_add_complaint)


# Create a multiple selection box
common_complaints = st.multiselect()
"Choose as many complaints:",
["Too many adds", "Too laggy", "Not enough suggestions", "Suggestions are not helpful enough", "too difficult to narrow search"]



# Press to send the complaint
if st.button("Send complaint to app"):
    st.write("You selected:", common_complaints)
    print(f"Sending selected options: {common_complaints}")
    st.write("You wrote:", complaint_input)
    print(f"Sending input: {complaint_input}")
