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
st.header('Access Interface Modification Tools Page')

if st.button("Get Available Interface Tools"):
    response = requests.get('http://api:4000/f/fda/visuals')

    if response.status_code == 200:
        st.write('')
        st.write("Interface tools successfully retrieved.")
    else:
        st.write('')
        st.write("Failed to retrieve tools.")