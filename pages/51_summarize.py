import streamlit as st

from common.chat import summary


def chat_with_openai(email, content):
    # Replace with your actual code to interact with the OpenAI API
    return summary.chat(email, content)


st.title("Summarize")
email = st.text_input("Enter your email address")
content = st.text_area("Content:")
if st.button("Summarize"):
    chat_response = chat_with_openai(email, content)
    # chat_log.text(f":person_in_lotus_position: {chat_prompt}")
    # chat_log.text(f":robot_face: {chat_response}")
    st.text_area("Summary",
                 value=chat_response, disabled=True)
