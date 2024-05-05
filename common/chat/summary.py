import os
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain.schema.runnable import Runnable
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema import BaseChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_openai import AzureChatOpenAI
from langchain.globals import set_verbose
from langchain.callbacks import StdOutCallbackHandler
import requests

set_verbose(True)

load_dotenv()

system_message = """You are a helpful assistant. Your job is to summarize the given content according to the user's profile and preference.
User Profile and preference:
{profile_info}
"""

user_mesasge = """Content to summarize: {input}
Summary: 
"""

handler = StdOutCallbackHandler()


def get_perspective(email):
    result = requests.get(f"http://localhost:8000/api/perspective/{email}")
    return result.content


llm = AzureChatOpenAI(model=os.getenv("OPENAI_MODEL"), verbose=True)


def clear_history():
    store = {}


def chat(email, content):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message),
            HumanMessagePromptTemplate.from_template(user_mesasge),
        ])

    chat = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
    response = chat.invoke(
        {"input": content, "profile_info": get_perspective(email)},
        config={"configurable": {"session_id": email}},
    )
    print(response)
    return response['text']
