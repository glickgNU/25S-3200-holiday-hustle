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

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('View User Activity Page')

# Add a button to fetch user activity
if st.button('Get User Activity'):
    url = 'http://api:4000/fda/user_activity'

    # Send a GET request 
    response = requests.get(url)
    
    if response.status_code == 200:
        # display the user activity data
        data = response.json()
        st.write("User Activity Data:", data)
    else:
        # show an error message
        st.error(f"Failed to fetch user activity.")
