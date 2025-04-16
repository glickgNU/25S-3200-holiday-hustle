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
st.header('Suggestions Page')



# inputs
#

selected_options = []
# Create a button
if st.button("Allergies"):

    selected_options = st.multiselect(
        "Choose your allergies:",
        ["Tree Nuts", "Peanuts", "Dairy", "Gluten", "Soy", "Almonds"]
    )
    # Display the selected items
    if selected_options:
        st.write("You selected:", selected_options)


# Create a text input box
user_input = st.text_input("Group size:", "Type in your group size")

# Display the input value
if user_input:
    st.write("You entered:", user_input)
else:
    st.write("What's your group size?")

# Create a button
if st.button("Audience"):

    selected_options = st.multiselect(
        "Choose your allergies:",
        ["Adults", "Children", "Men", "Women", "Older people", "People w/ pets", "Food lovers", "Fashion Lovers"]
    )
    # Display the selected items
    if selected_options:
        st.write("You selected:", selected_options)


list_of_associated_suggestions = []
st.write("Here is your list:")
for item in list_of_associated_suggestions:
    st.write(f"- {item}")

if st.button("These are suggestions based on your preferences: ", type='primary',
             use_container_width=True):
             results = requests.get(f'http://api:4000/f/fda/personal_suggestions/{user_input}/{selected_options}/{list_of_associated_suggestions}').json()
             st.dataframe(results)


# Jason 1:
if st.button("Click here to view the input you made: ", type='primary',
             use_container_width=True):
    results = requests.get(f'http://api:4000/i/inputs/inputs/{user_input}/{selected_options}/{list_of_associated_suggestions}').json()
    st.write(results)

