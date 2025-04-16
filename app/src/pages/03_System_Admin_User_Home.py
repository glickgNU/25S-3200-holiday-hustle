import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome System Administrator {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View User Activity Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_View_User_Activity.py')

if st.button('View User Complaints Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_View_User_Complaints_Page.py')

if st.button('View Access Interface Modification Tools Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_View_Access_Interface_Modification_Tools_Page.py')
