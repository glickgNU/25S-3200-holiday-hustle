import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests
# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Suggestions History Page')

if st.button('View Suggestions Page', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_Suggestions_Page.py')



 # ----- change ----

# Jason 2
# Look at person whose input you want to look at
look_at_person = st.text_input("Whose inputs do you want to look at?")

if st.button('View someones history', 
             type='primary',
             use_container_width=True):
    results = requests.get(f'http://api:4000/i/inputs/inputs/history/{look_at_person}').json()


# Jason 3
look_at_person = st.text_input("Whose inputs do you want to delete?")
specific_input = st.text_input("Which input do you want to delete?")

if st.button('View someones history', 
             type='primary',
             use_container_width=True):
    results = requests.get(f'http://api:4000/i/inputs/inputs/history/{look_at_person}/{specific_input}').json()




# Initialize session state to store inputs
#if "input_history" not in st.session_state:
#    st.session_state.input_history = []

# Input box for user to add inputs
#user_input = st.text_input("Enter your input:")

# Add user input to the history
#if user_input:
#    st.session_state.input_history.append(user_input)

# Convert input history to a DataFrame
#input_history_df = pd.DataFrame(
#    st.session_state.input_history, columns=["Input History"]
#)

# Display the table
#st.write("History of Inputs:")
#st.table(input_history_df)

