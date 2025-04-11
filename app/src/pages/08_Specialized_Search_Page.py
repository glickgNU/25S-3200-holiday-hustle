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

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Specialized Search Page')


# Define the data for the table
data = {
    "Most Popular Items": ["Customized T-Shirts", "Sustainable Water Bottles", "Trendy Sneakers"], # put from databases
    "Most Popular Suggestions": ["Add a live music band", "Include more vegetarian options", "Offer themed gift baskets"],
    "Most Previewed Food, Decoration, Activities": ["Pasta Bar, Floral Centerpieces, Photo Booth", "Sushi Rolls, LED Decorations, Escape Room", "Cupcakes, Rustic Lights, DIY Workshops"]
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Display the table in Streamlit
st.title("Event Insights Table")
st.table(df)

