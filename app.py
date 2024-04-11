import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
import asyncio
from create_perspective import generate_perspective
import agent_chat
import simple_chat

load_dotenv()

st.set_page_config(page_title="My App", page_icon=":smiley:",
                   layout="wide", initial_sidebar_state="expanded")

# Read client_id, client_secret, and redirect_uri from environment variables
client_id = os.getenv('CLIENT_ID')
tenant_id = os.getenv('TENANT_ID')
redirect_uri = os.getenv('REDIRECT_URI')
scopes = ['User.Read']

# Function to get profile info from Microsoft Graph API and SQLite database


async def get_profile_info(email):
    # Initialize the session state if it doesn't exist
    if 'credentials_dict' not in st.session_state:
        st.session_state['credentials_dict'] = {}

    # Get the InteractiveBrowserCredential for the email address
    if email in st.session_state['credentials_dict']:
        credentials = st.session_state['credentials_dict'][email]
    else:
        # Replace with your actual code to create a new InteractiveBrowserCredential
        credentials = DeviceCodeCredential(
            client_id=client_id, tenant_id=tenant_id, prompt_callback=lambda uri, code, expires: st.write(f"Go to {uri} and enter code {code}"))
        st.session_state['credentials_dict'][email] = credentials

    graph_client = GraphServiceClient(credentials, scopes)

    query_params = UserItemRequestBuilder.UserItemRequestBuilderGetQueryParameters(
        select=["displayName", "jobTitle", "aboutMe",
                "city", "skills", "department", "interests"],
    )

    request_configuration = UserItemRequestBuilder.UserItemRequestBuilderGetRequestConfiguration(
        query_parameters=query_params,
    )

    result = await graph_client.users.by_user_id(email).get(request_configuration=request_configuration)
    return result


def parse_profile_info(profile_info):
    return {k: v for k, v in profile_info.__dict__.items() if v is not None and k not in ['backing_store', 'additional_data']}

# Function to interact with OpenAI API


def chat_with_openai(email, prompt):
    # Replace with your actual code to interact with the OpenAI API
    return simple_chat.chat(email, prompt)
    # return agent_chat.chat(email, prompt)

def clear_history():
    simple_chat.clear_history()

# Function to create perspective
def create_perspective(profile_info, user_info):
    # Replace with your actual code to create perspective
    return generate_perspective(profile_info, user_info)

# Function to write to SQLite database
def write_to_db(email, profile_info, user_info, perspective):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_info (email text, profile_info text, user_info text, perspective text)")
    c.execute("SELECT * FROM user_info WHERE email=?", (email,))
    record = c.fetchone()
    if record:
        c.execute("UPDATE user_info SET profile_info=?, user_info=?, perspective=? WHERE email=?",
                  (profile_info, user_info, perspective, email))
    else:
        c.execute("INSERT INTO user_info VALUES (?,?,?,?)",
                  (email, profile_info, user_info, perspective))
    conn.commit()
    conn.close()


def read_from_db(email):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_info (email text, profile_info text, user_info text, perspective text)")
    c.execute("SELECT * FROM user_info WHERE email=?", (email,))
    record = c.fetchone()
    conn.close()
    if record:
        return record[1], record[2], record[3]


# Streamlit app
page = st.sidebar.selectbox("Choose a page", ["Configure", "Chat"])

if page == "Configure":
    st.title("Configure")
    email = st.text_input("Enter your email address")

    # Initialize the session state if it doesn't exist
    if 'profile_info' not in st.session_state:
        st.session_state['profile_info'] = "N/A"
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = "N/A"
    if 'perspective' not in st.session_state:
        st.session_state['perspective'] = "N/A"

    if st.button("Fetch"):
        record = read_from_db(email)
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
        write_to_db(email, str(st.session_state['profile_info']),
                    st.session_state['user_info'], st.session_state['perspective'])
        st.success("Information saved successfully!")

    st.text_area("Your perspective",
                 value=st.session_state['perspective'], disabled=True)

elif page == "Chat":
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
