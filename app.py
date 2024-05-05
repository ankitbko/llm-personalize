import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="My App", page_icon=":smiley:",
                   layout="wide", initial_sidebar_state="expanded")

st.write("Select one of the links from the sidebar to navigate to the respective page.")
