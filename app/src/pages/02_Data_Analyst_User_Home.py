import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Session check
if 'first_name' not in st.session_state:
    st.error("You're not logged in. Please return to the login page.")
    st.stop()

st.title(f"Welcome Data Analyst {st.session_state['first_name']}.")
st.write("Here are your available insights at a glance.")
st.write("")


st.write('### What would you like to do today?')

if st.button('View Reports Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/09_Reports_Page.py')

if st.button('View Reports Downloads Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/10_Downloads_Reports_Page.py')

