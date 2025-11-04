import streamlit as st
import time
from flask import Flask, render_template, request, session, redirect, url_for, Response, stream_with_context, jsonify, json 
import uuid
import re

from src.components.semantic_memory import SemanticMemory
from src.components.message_history import MessageHistory
from src.components.episodic_memory import EpisodicMemory
from src.components.short_term_memory import ShortTermMemory
from src.agents.chat_agent import ChatAgent
from src.models.episodic_memory_model import ChatSession, ChatSummary, Base
from src.components.sql import SQL
from src.models.model_base import LLM

from langchain_core.messages import AIMessage, HumanMessage
from markupsafe import Markup


# Initialize the database
sql = SQL()
sql.create_all()

# Overall context
CONTEXT = 32768
MODEL = "google/gemma-3-4b-it"

# Model
model = LLM(context=CONTEXT, model=MODEL)

# Agent
message_agent = ChatAgent()

# Markup Patch
def nl2br(value):
    return Markup(value.replace("\n", "<br>\n"))

app = Flask(__name__)
app.jinja_env.filters['nl2br'] = nl2br
app.secret_key = "TestKey123"

# Memory
msg = MessageHistory(token_limit=CONTEXT, model=MODEL)
persistant_memory = EpisodicMemory()
short_term_memory = ShortTermMemory()

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('chat.html')
    
def generate(user_input: str, session_id: str, history: str):
    try:     
        
        # AI buffer for saving after generating
        ai_response_buffer = ""
            
        for chunk in message_agent.generate_message(user_input, session_id, history):
            token = None

            if hasattr(chunk, "content") and chunk.content: 
                token = chunk.content 
            elif isinstance(chunk, str): 
                token = chunk 
            else: 
                continue # skip leere oder irrelevante Chunks
            
            token = token.replace("\r", "")
            token = re.sub(r"\n{3,}", "\n\n", token)
            
            if token.strip() == "[DONE]":
                continue
            
            ai_response_buffer += token
            yield f"data: {json.dumps({'token': token})}\n\n"

        # Saving AI Buffer to Memory
        if ai_response_buffer.strip():
            msg.add(role="assistant", message=ai_response_buffer, session_id=session_id)

        yield "data: [DONE]\n\n"

    except Exception as e:
        print(f"Error while creating the stream: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    
@app.route("/chats", methods=["GET", "POST"])
def chats():
    all_chats = persistant_memory.get_all_sessions()  
    if not all_chats:
        return redirect(url_for("new_chat"))
    first_chat = all_chats[0]
    return redirect(url_for("chat", session_id=first_chat.session_id,  chats=all_chats))


@app.route('/chat/<session_id>', methods=["GET", "POST"])
def chat(session_id):
    chats=persistant_memory.get_all_sessions()
    history=msg.get_messages(session_id)    
    
    if request.method == "POST":
        data = request.get_json()
        user_message = data['message'].strip()
        
        # Saving first human message
        msg.add(role="user", message=user_message, session_id=session_id)
        
        # Reload the history
        history=msg.get_messages(session_id)
            
        return Response(
            stream_with_context(generate(data["message"], session_id=session_id, history=history)),
            mimetype="text/event-stream"
        )
    
    return render_template('chat.html', messages=history, chats=chats)

@app.route("/new_chat", methods=["POST"])
def new_chat():
    session_id = str(uuid.uuid4())
    
    persistant_memory.save_session(
        session_id=session_id,
        title=session_id
    )   
    
    return redirect(url_for("chat", session_id=session_id))
                
@app.route('/delete_history/<session_id>')
def delete_history(session_id):
    short_term_memory.delete_short_term_memory(session_id)
    return {'Success': 'Memory esuccessfully deleted'}

if __name__ == "__main__":
    app.run(debug=True)       