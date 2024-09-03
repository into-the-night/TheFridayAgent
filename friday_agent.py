from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt.chat_agent_executor import AgentState

from settings import Settings

tvly_api_key = Settings.tvly_api_key
google_api_key = Settings.gemini_api_key

tools = [TavilySearchResults(max_results=1)]
tool_node = ToolNode(tools)


llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key).bind_tools(tools)

def should_continue(state: AgentState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        print('tools')
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END

def call_model(state: MessagesState):
    messages = state['messages']
    response = llm.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue,)
workflow.add_edge("tools", 'agent')

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

final_state = app.invoke(
    {"messages": [HumanMessage(content="Who is the President of India?")]},
    config={"configurable": {"thread_id": 42}}
)

print(final_state["messages"][-1].content)
