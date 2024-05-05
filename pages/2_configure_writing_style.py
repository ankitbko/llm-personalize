import streamlit as st

from common.db import delete_from_user_additional_info, read_from_user_additional_info, read_from_userinfo, write_to_user_additional_info, write_to_userinfo
from common.perspectives.writing_style_perspective import generate_writing_style_perspective

st.title("Create Perspective from Writing Style")

email = st.text_input("Enter your email address")
if 'email' not in st.session_state:
    st.session_state.email = email
elif st.session_state.email != email:
    st.session_state.clear()
    st.session_state.email = email

if 'perspective' not in st.session_state:
    st.session_state['perspective'] = "N/A"
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = "N/A"
if 'profile_info' not in st.session_state:
    st.session_state['profile_info'] = "N/A"
if 'email_body_count' not in st.session_state:
    st.session_state.email_body_count = 1

if st.button("Fetch"):
    record = read_from_userinfo(email)
    if record:
        st.session_state['profile_info'], st.session_state['user_info'], st.session_state['perspective'] = record
    additional_info = read_from_user_additional_info(email)
    emails = [info[1]
              for info in additional_info if info[1] != "" or info[1] is not None]
    print(f'{len(emails)=}')
    st.session_state.email_body_count = len(emails)
    for i, email_body in enumerate(emails):
        st.session_state[f'email_body_{i}'] = email_body

st.session_state['profile_info'] = st.text_area(
    "Profile Info:", value=st.session_state['profile_info'])

st.session_state['user_info'] = st.text_area(
    "User Info:", value=st.session_state['user_info'])


# Function to add a new email body text area


def add_email_body():
    st.session_state.email_body_count += 1


# Button to add more email body text areas
st.button("Add Email Body", on_click=add_email_body)

# After displaying the email body text areas
email_bodies = {}  # Initialize a dictionary to store email body contents

for i in range(st.session_state.email_body_count):
    # Use the key to uniquely identify each text area and store its value in the dictionary
    if f"email_body_{i}" not in st.session_state:
        st.session_state[f"email_body_{i}"] = ""
    email_bodies[f"email_body_{i}"] = st.text_area(
        f"Email Body {i+1}:", key=f"email_body_{i}", value=st.session_state[f"email_body_{i}"])


if st.button("Submit"):
    # Replace with your actual code to create perspective
    st.session_state['perspective'] = generate_writing_style_perspective(st.session_state['profile_info'],
                                                                         st.session_state['user_info'], list(email_bodies.values()))
    write_to_userinfo(email, st.session_state['profile_info'],
                      st.session_state['user_info'], st.session_state['perspective'])
    delete_from_user_additional_info(email)
    write_to_user_additional_info(email, list(email_bodies.values()))
    st.success("Information saved successfully!")


st.text_area("Your perspective",
             value=st.session_state['perspective'], disabled=True)
