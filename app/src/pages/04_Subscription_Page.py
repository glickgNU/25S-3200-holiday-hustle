import logging
logger = logging.getLogger(__name__)

import streamlit as st
from streamlit_extras.app_logo import add_logo

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
             results = requests.get('http://api:4000/u/users/subscription/{Acc_ID}/{sub_type}').json()
             st.dataframe(results)
if st.button('Added new Monetization', type='primary',
             use_container_width=True):
             st.write("Your Subscription type is: ", sub_type)
             results = requests.get('http://api:4000/u/users/subscription/post{Acc_ID}/{sub_type}').json()
             st.dataframe(results)



