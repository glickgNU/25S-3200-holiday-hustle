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
st.header('Suggestions History Page')

if st.button('View Suggestions Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_Suggestions_Page.py')



 # ----- change ----

# Initialize session state to store inputs
if "input_history" not in st.session_state:
    st.session_state.input_history = []

# Input box for user to add inputs
user_input = st.text_input("Enter your input:")

# Add user input to the history
if user_input:
    st.session_state.input_history.append(user_input)

# Convert input history to a DataFrame
input_history_df = pd.DataFrame(
    st.session_state.input_history, columns=["Input History"]
)

# Display the table
st.write("History of Inputs:")
st.table(input_history_df)

