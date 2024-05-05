import streamlit as st

from common.chat import simple_chat


def chat_with_openai(email, prompt):
    # Replace with your actual code to interact with the OpenAI API
    return simple_chat.chat(email, prompt)


def clear_history():
    simple_chat.clear_history()


st.title("Chat")
email = st.text_input("Enter your email address")
chat_prompt = st.text_input("Enter your chat prompt")
chat_log = st.empty()  # Create an empty placeholder for the chat log
if st.button("Chat"):
    chat_response = chat_with_openai(email, chat_prompt)
    # chat_log.text(f":person_in_lotus_position: {chat_prompt}")
    # chat_log.text(f":robot_face: {chat_response}")
    st.text_area("Response",
                 value=chat_response, disabled=True)

if st.button("Clear History"):
    simple_chat.clear_history()
    st.success("Chat history cleared successfully!")
