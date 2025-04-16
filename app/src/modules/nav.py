# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")

#### ------------------------ Examples for Role of casual_user ------------------------
def casualUser():
    st.sidebar.page_link("pages/00_Casual_User_Home.py", label="Casual User Home", icon="👤")

def subscriptionPage():
    st.sidebar.page_link("pages/04_Subscription_Page.py", label="Subscription Page", icon="💵")

def suggestionsHistoryPage():
    st.sidebar.page_link("pages/06_Suggestions_History_Page.py", label="Suggestions History Page", icon="💵")

def makeComplaintPage():
    st.sidebar.page_link("pages/07_Make_Complaint_Page.py", label="Make Complaint Page", icon="💵")




#### ------------------------ Examples for Role of experienced_user ------------------------
def experiencedUser():
    st.sidebar.page_link("pages/01_Experienced_User_Home.py", label="Experienced User Home", icon="🗺️")

def suggestionsPage():
    st.sidebar.page_link("pages/05_Suggestions_Page.py", label="Suggestions Page", icon="💵")

def suggestionsHistoryPage():
    st.sidebar.page_link("pages/06_Suggestions_History_Page.py", label="Suggestions History Page", icon="💵")

def specializedSearchPage():
    st.sidebar.page_link("pages/08_Specialized_Search_Page.py", label="Specialized Search Page", icon="💵")

#### ------------------------ Examples for Role of data_analyst_user ------------------------
def dataAnalystUser():
    st.sidebar.page_link("pages/02_Data_Analyst_User_Home.py", label="Data Analyst User Home", icon="📈")

def reportsPage():
    st.sidebar.page_link("pages/09_Reports_Page.py", label="Reports Page", icon="📈" )

def downloadsReportsPage():
    st.sidebar.page_link("pages/10_Download_Reports_Page.py", label="Download Reports Page", icon="📈")

def visualizeData():
    st.sidebar.page_link("pages/14_Visualize_Data.py", label="Visualize Data", icon="📈")

#### ------------------------ Examples for Role of system_administrator_user ------------------------
def systemAdministratorUser():
    st.sidebar.page_link("pages/03_System_Admin_User_Home.py", label="System Administrator User Home", icon="🗺️")

def viewUserActivityPage():
    st.sidebar.page_link("pages/11_View_User_Activity_Page.py", label="View User Activity Page", icon="🗺️")

def viewUserComplaintsPage():
    st.sidebar.page_link("pages/12_View_User_Complaints_Page.py", label="View User Complaint Page", icon="🗺️")

def accessInterfaceModificationTools():
    st.sidebar.page_link("pages/13_Access_Interface_Modification_Tools_Page.py", label="Access Interface Modification Tools ", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction_worker.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:


       # If the user is casual, give them access to a normal user pages
        if st.session_state["role"] == "casual_user":
            casualUser()
            suggestionsPage()
            subscriptionPage()
            suggestionsHistoryPage()
            makeComplaintPage()

        # If the user is an experienced event planner, give them access to a experienced event planner user pages
        if st.session_state["role"] == "experienced_user":
            experiencedUser()
            suggestionsPage()
            suggestionsHistoryPage()
            specializedSearchPage()

          # If the user is an experienced event planner, give them access to a experienced event planner user pages
        if st.session_state["role"] == "data_analyst":
            dataAnalystUser()
            reportsPage()
            downloadsReportsPage()
            visualizeData()
        
              # If the user is an experienced event planner, give them access to a experienced event planner user pages
        if st.session_state["role"] == "system_admin":
            systemAdministratorUser()
            viewUserActivityPage()
            viewUserComplaintsPage()
            accessInterfaceModificationTools()


    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
