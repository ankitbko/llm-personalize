import os
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
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

system_message = """You are a helpful assistant. Answer user's query and format the answer based on user's preference and profile.
User Profile and preference:
{profile_info}
"""

user_mesasge = """{input}"""

handler = StdOutCallbackHandler()

def get_perspective(email):
    result = requests.get(f"http://localhost:8000/api/perspective/{email}")
    return result.content

llm = AzureChatOpenAI(model=os.getenv("OPENAI_MODEL"), verbose=True)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def clear_history():
    store = {}

def chat(email, query):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            HumanMessagePromptTemplate.from_template(user_mesasge),
        ])

    with_chat_history = RunnableWithMessageHistory(
        LLMChain(llm=llm, prompt=prompt, callbacks=[handler]),
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    response = with_chat_history.invoke(
        {"input": query, "profile_info": get_perspective(email)},
        config={"configurable": {"session_id": email}},
    )
    print(response)
    return response['text']
