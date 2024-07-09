import streamlit as st
import asyncio

from common.db import read_from_userinfo, write_to_userinfo
from common.msgraph import get_profile_info, parse_profile_info

from common.perspectives.msgraph_perspective import generate_msgraph_perspective

st.set_page_config(page_title="Configure - AD")
st.title("Create Perspective From MS Graph")

email = st.text_input("Enter your email address")


# Function to create perspective
def create_perspective(profile_info, user_info):
    # Replace with your actual code to create perspective
    return generate_msgraph_perspective(profile_info, user_info)


# Initialize the session state if it doesn't exist
if 'profile_info' not in st.session_state:
    st.session_state['profile_info'] = "N/A"
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = "N/A"
if 'perspective' not in st.session_state:
    st.session_state['perspective'] = "N/A"

if st.button("Fetch"):
    record = read_from_userinfo(email)
    if record:
        st.session_state['profile_info'], st.session_state['user_info'], st.session_state['perspective'] = record

profile_info_placeholder = st.empty()
profile_info_placeholder.text(
    f"Profile Info: {st.session_state['profile_info']}")

if st.button("Read Profile"):
    profile = asyncio.run(get_profile_info(email))
    profile = parse_profile_info(profile)
    print(profile)
    st.session_state['profile_info'] = profile
    profile_info_placeholder.text(
        f"Profile Info: {st.session_state['profile_info']}")

st.session_state['user_info'] = st.text_area(
    "User Info:", value=st.session_state['user_info'])

if st.button("Submit"):
    print(f"{st.session_state['user_info']=}")
    st.session_state['perspective'] = create_perspective(
        st.session_state['profile_info'], st.session_state['user_info'])
    write_to_userinfo(email, str(st.session_state['profile_info']),
                      st.session_state['user_info'], st.session_state['perspective'])
    st.success("Information saved successfully!")

st.text_area("Your perspective",
             value=st.session_state['perspective'], disabled=True)
