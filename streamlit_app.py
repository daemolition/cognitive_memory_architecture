import streamlit as st

from src.components.semantic_memory import LtMemory
from src.components.stmemory import StMemory
from src.components.message_history import MessageHistory
from src.agents.chat_agent import ChatAgent
from src.models.persistant_memory_model import StMemory, Base
from src.components.sql import SQL
from src.models.model_base import LLM

# Initialize the database
sql = SQL()
Base.metadata.create_all(sql.get_engine())

# Overall context
CONTEXT = 32768

# Model
model = LLM(context=CONTEXT)
llm = model.load_llm()

# Agent
message_agent = ChatAgent()

  
if not "history" in st.session_state:
    st.session_state.history = []
    

    
prompt = st.chat_input("Please rovide a message")
        
if prompt:
    st.session_state.history.append({'role':'user', 'content': prompt})
    with st.chat_message("user"):
        st.write(prompt)
        

    with st.chat_message("assistant"):
        stream = llm.stream(prompt)
        
    response = st.write_stream(
        (c.content for c in llm.stream(prompt) if hasattr(c, "content"))
    )

    st.session_state.history.append({
        "role": "assistant",
        "content": response
    })
    
    print(st.session_state.history)
