import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    The purpose of Holiday Hustle is to make holiday event planning more accessible to 
    people who may not have much prior experience in event planning. We hope to make this
    app appealing to both experienced event planners, and people who may have no experience
    with event planning. We help with all types of holiday planning ranging from large holidays 
    such as Christmas all the way to minor holidays such as President's Day!

    🎃🎄🦃🍎🐰🍀❤️☃️
    """
        )
