import os
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_openai import AzureChatOpenAI
from langchain.globals import set_verbose

set_verbose(True)

system_message = """You will be given information about a user and few emails that user has written in past. Your job is to create a digital twin persona of the person based on the information provided reflecting the user's personality, interests, preferences and writing style. Extract the writing style from the emails provided. 
Persona will be used later to adapt the conversation with other Large Language Model to the user's preferences. Create a detailed user persona based on the information provided.
Only create the persona of the user based on information provided. Do not hallucinate and do not make up things for user However you can be creative when inferring things about the user using the information provided. Do not output anything else. The persona that you create will be used by other system and not by you.
"""

user_mesasge = """User profile info from Microsoft graph: {profile_info}
Preferences provided by user: {user_info}
Emails: 
{emails}
"""

chat = AzureChatOpenAI(model=os.getenv("OPENAI_MODEL"), verbose=True)


def generate_writing_style_perspective(profile_info, user_info, emails):
    concat_emails = ''
    for i in range(len(emails)):
        concat_emails += f"Email {i+1}: {emails[i]}\n"

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_message),
            HumanMessagePromptTemplate.from_template(user_mesasge),
        ])
    messages = chat_template.format_messages(
        profile_info=profile_info, user_info=user_info, emails=concat_emails)
    print(f"{messages=}")
    response = chat.invoke(messages)
    print(f"{response.content=}")
    return response.content
