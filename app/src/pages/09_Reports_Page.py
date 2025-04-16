import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Reports Page')

# Carlos-1: Average spending and total clicks per holiday
st.subheader(" Holiday Spending and Engagement")
try:
    response = requests.get("http://api:4000/fda/holiday")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
except Exception as e:
    st.error(f"Error loading holiday data: {e}")

# Carlos-2: Most popular food/deco/activities
st.subheader(" Top 10 Most Popular Decorations & Activities")
try:
    response = requests.get("http://api:4000/fda")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
except Exception as e:
    st.error(f"Error fetching popular items: {e}")

# Carlos-3: Average pricing per group size
st.subheader("👥 Average Budget by Group Size")
try:
    response = requests.get("http://api:4000/fda/personalized_suggestions")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("GroupSize")["AvgBudget"])
except Exception as e:
    st.error(f"Error fetching budget by group size: {e}")

# Carlos-6: Host type spending summary
st.subheader(" Spending by Host Type")
try:
    response = requests.get("http://api:4000/fda/analysis")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)
except Exception as e:
    st.error(f"Error fetching host type summary: {e}")