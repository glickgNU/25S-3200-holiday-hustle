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

st.header("📈 Visualize Data")

st.markdown("Welcome to your data insights dashboard, Carlos. Explore trends and behavior visually.")

# 🎉 Carlos-1: Holiday Spending
st.subheader("Holiday Spending vs. Clicks")
try:
    response = requests.get("http://api:4000/fda/holiday")
    response.raise_for_status()
    data = pd.DataFrame(response.json())
    fig = px.bar(data, x="HolidayName", y=["AvgSpending", "TotalClicks"],
                 barmode="group", title="Average Spending and Clicks per Holiday")
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load holiday data: {e}")

# 📅 Carlos-4: Monthly Planning Trends
st.subheader("Monthly Suggestion Trends")
try:
    response = requests.get("http://api:4000/fda/personalized_suggestions/presets")
    response.raise_for_status()
    data = pd.DataFrame(response.json())
    fig = px.line(data, x="Month", y="TotalSuggestions", markers=True,
                  title="Total Suggestions Created per Month")
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load monthly trends: {e}")

# 👥 Carlos-6: Spending by Host Type
st.subheader("Spending by Host Type")
try:
    response = requests.get("http://api:4000/fda/analysis")
    response.raise_for_status()
    data = pd.DataFrame(response.json())
    fig = px.pie(data, names="HostType", values="AvgSpending",
                 title="Average Spending: Casual Hosts vs Professional Planners")
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load host spending data: {e}")
