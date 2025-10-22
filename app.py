import time
import streamlit as st
from langchain_ollama import ChatOllama

NUM_CONTEXT = 32768

# Demo App
st.title("Project LSTM RAG")

def chat_stream(input_text):
    model = ChatOllama(
        model="qwen3:4b",
        num_ctx=NUM_CONTEXT
    )
    response = model.stream(input_text)
    
    for char in response:
        yield char   
       

def save_feedback(index):
    st.session_state.history[index]['feedback'] = st.session_state[f"feedback_{index}"]
    
if "history" not in st.session_state:
    st.session_state.history = []
    

for i, message in enumerate(st.session_state.history):
    with st.chat_message(message["role"]):
        st.write(message['content'])
        if message["role"] == "assistant":
            feedback = message.get("feedback", None)
            st.session_state[f"feedback_{i}"] = feedback
            st.feedback(
                "thumbs",
                key=f"feedback_{i}",
                disabled=feedback is not None,
                on_change=save_feedback,
                args=[i],
            )

if prompt := st.chat_input("Say something"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = st.write_stream(chat_stream(prompt))
        st.feedback(
            "thumbs",
            key=f"feedback_{len(st.session_state.history)}",
            on_change=save_feedback,
            args=[len(st.session_state.history)],
        )
    st.session_state.history.append({"role": "assistant", "content": response})
            
        
        
