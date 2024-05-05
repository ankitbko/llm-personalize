import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_openai import AzureChatOpenAI
from langchain.globals import set_verbose

set_verbose(True)

load_dotenv()

system_message = """You will be given information about a user. Your job is to create a digital twin persona of the person based on the information provided. 
Persona will be used later to adapt the conversation with other Large Language Model to the user's preferences. Create a detailed user persona based on the information provided.
Only create the persona of the user. Do not output anything else. The persona that you create will be used by other system and not by you.
"""

user_mesasge = """User profile info from Microsoft Graph API is: {profile_info}
Preferences provided by user: {user_info}
"""

chat = AzureChatOpenAI(model=os.getenv("OPENAI_MODEL"), verbose=True)


def generate_msgraph_perspective(profile_info, user_info):

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_message),
            HumanMessagePromptTemplate.from_template(user_mesasge),
        ])
    messages = chat_template.format_messages(
        profile_info=profile_info, user_info=user_info)
    print(f"{messages=}")
    response = chat.invoke(messages)

    return response.content
