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
st.header('Subscription Page')

Acc_ID = st.number_input("Account ID: ", step=1)
sub_type = st.radio('Choose a pro or free subscription: ', ("Free", "Pro"))

if st.button("Subscription change complete", type='primary',
             use_container_width=True):
             st.write("Your Subscription type is: ", sub_type)
             results = requests.get(f'http://api:4000/u/users/subscription/{Acc_ID}/{sub_type}').json()
             st.dataframe(results)

  
