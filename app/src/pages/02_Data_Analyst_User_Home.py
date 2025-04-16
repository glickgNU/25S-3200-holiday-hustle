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

# Option to view spending pattern summary (Carlos-6)
if st.button("📊 Show Host Type Spending Summary", type='primary', use_container_width=True):
    try:
        response = requests.get("http://api:4000/fda/analysis")
        response.raise_for_status()
        data = response.json()
        st.subheader("Spending by Host Type")
        st.dataframe(data)
    except Exception as e:
        st.error(f"Failed to fetch analysis data: {e}")

st.write("---")

st.write("### What would you like to do next?")

col1, col2 = st.columns(2)
with col1:
if st.button('🗂️ View Reports Page', use_container_width=True):
        st.switch_page('pages/09_Reports_Page.py')

with col2:
if st.button('📥 View Reports Downloads Page', use_container_width=True):
        st.switch_page('pages/10_Downloads_Reports_Page.py')

