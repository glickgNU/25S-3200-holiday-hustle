import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import requests
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Specialized Search Page')

preview_what = ""



if st.button("Preview Most Popular Items" ,type='primary',
             use_container_width=True):
        preview_what = "Most_Popular_Items"

if st.button("Preview Most Popular Suggestions" ,type='primary',
             use_container_width=True):
        preview_what = "Most_Popular_Suggestions"

if st.button("Preview Most Food, Decorations, Activities" ,type='primary',
             use_container_width=True):
        preview_what = "Most_Food_Decorations_Activities"
        

# Press to send the complaint (Jason 6)
if st.button("Get most popular items, suggestions, food, decorations, and activities" ,type='primary',
             use_container_width=True):
             results = requests.get(f'http://api:4000/f/fda/personal_suggestions/{preview_what}').json()
             st.dataframe(results)


# See most popular personalized suggestions (Jason 5)
if st.button("Find most popular suggestions" ,type='primary',
             use_container_width=True):
             results = requests.get(f'http://api:4000/f/fda/personal_suggestions/').json()
             st.dataframe(results)
