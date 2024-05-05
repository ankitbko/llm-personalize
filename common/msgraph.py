import os
import streamlit as st
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder

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
