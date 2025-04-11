import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Experienced Event Planner {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Suggestions Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_Suggestions_Page.py')

if st.button('View Suggestions History Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/06_Suggestions_History_Page.py')

if st.button('View Specialized Search Page Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/08_Specialize_Search_Page.py')