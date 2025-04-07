import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from lib.agent import rag_agent
import os
from lib.utils import (
    load_stylesheet,
    usage_guidelines,
    chat_history,
    user_message,
    bot_message,
)
import time
import pprint


# Streamlit user interface
st.set_page_config(
    page_title="Assistant",
    page_icon=":smile:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_stylesheet(os.path.join(os.path.dirname(__file__), 'static/style.css'))

if "messages" not in st.session_state:
    st.session_state["messages"] = []

message_container = st.container()

with message_container:
    bot_message(
        """Hello! I'm your **virtual assistant** and I'd be delighted to assist you in any way I can. If you're unsure how I can be of help, please feel free to take a look at the user guideline below, which outlines the services I can provide."""
    )
    usage_guidelines()
    bot_message("""Could I ask what I can do for you?""")

    # Display chat history in order
    chat_history(st.session_state["messages"])

# Input box at the bottom using st.chat_input
user_input = st.chat_input("Type your message:")

inicio = time.time() 
if user_input:
    with message_container:
        user_message(user_input)
        st.session_state["messages"].append(HumanMessage(content=user_input))
        with st.chat_message(
            "assistant",
            avatar=os.path.join(os.path.dirname(__file__), 'static/img/bot.png')
        ):
            # Get assistant's response using the LangGraph agent
            responses = rag_agent.invoke(
                {"messages": st.session_state["messages"]},
                config={"configurable": {"thread_id": "42"}},
            )
            pprint.pprint(responses)
            st.markdown(responses["messages"][-1].content)
            # # Add assistant's response to history
            for message in responses["messages"]:
                message.pretty_print()
            st.session_state["messages"].append(
                AIMessage(content=responses["messages"][-1].content)
            )
fin = time.time()

print(f"Tiempo de ejecución: {fin - inicio:.4f} segundos")
