import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_openai import AzureChatOpenAI
from langchain.globals import set_verbose
from langchain_community.utilities import SerpAPIWrapper
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import BaseTool, StructuredTool, tool
import requests
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


set_verbose(True)

load_dotenv()

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# search = SerpAPIWrapper()
# search_tool = StructuredTool.from_function(
#     func=search.search,
#     name="Google Search Tool",
#     description="useful for when you need to answer questions by searching the web",
# )

# write a method to call fastapi endpoint
def get_perspective_form_email(email):
    def get_perspective():
        result = requests.get(f"http://localhost:8000/api/perspective/{email}")
        return result
    return get_perspective

system_message = """You are a helpful assistant. Before returning answer you MUST use profile tool to get the user's preference and then format the answer based on user's preference and profile."""

user_message = """{input}"""

llm = AzureChatOpenAI(model=os.getenv("OPENAI_MODEL"), verbose=True)

def chat(email: str, query: str):
    perspective_tool = StructuredTool.from_function(
        func=get_perspective_form_email(email),
        name="Profile_Tool",
        description="Get the profile and perspective of the user.",
    )

    tools = [perspective_tool]
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            HumanMessagePromptTemplate.from_template(user_message),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    response = agent_with_chat_history.invoke(
        {"input": query},
        # This is needed because in most real world scenarios, a session id is needed
        # It isn't really used here because we are using a simple in memory ChatMessageHistory
        config={"configurable": {"session_id": email}},
    )
    return response['output']
