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
    
    
@app.route("/stream", methods=["GET", "POST"])
def stream():
    data = request.get_json()
    if not data or "message" not in data:
        return "Missing input", 400

    # Session-ID
    if "id" not in session:
        session["id"] = str(uuid.uuid4())
    session_id = session["id"]
    
    if request.method == "GET":
        return redirect(url_for("stream_with_session_id", session_id=session_id))
    
    return jsonify({'session_id': session_id}), 200


@app.route('/stream/<session_id>', methods=["GET", "POST"])
def stream_with_session_id(session_id):
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
    
    return render_template('chat.html', messages=history)
                
@app.route('/delete_history/<session_id>')
def delete_history(session_id):
    short_term_memory.delete_short_term_memory(session_id)
    return {'Success': 'Memory esuccessfully deleted'}

if __name__ == "__main__":
    app.run(debug=True)       