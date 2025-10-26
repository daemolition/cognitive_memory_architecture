import streamlit as st
import time
from flask import Flask, render_template, request, session, redirect, url_for, Response, stream_with_context, jsonify, json 
import uuid

from src.components.semantic_memory import SemanticMemory
from src.components.message_history import MessageHistory
from src.components.episodic_memory import EpisodicMemory
from src.agents.chat_agent import ChatAgent
from src.models.episodic_memory_model import ChatSession, ChatSummary
from src.components.sql import SQL
from src.models.model_base import LLM

from langchain_core.messages import AIMessage, HumanMessage
from markupsafe import Markup

# Initialize the database
sql = SQL()

# Overall context
CONTEXT = 32768

# Model
model = LLM(context=CONTEXT)

# Agent
message_agent = ChatAgent()

# Markup Patch
def nl2br(value):
    return Markup(value.replace("\n", "<br>\n"))

app = Flask(__name__)
app.jinja_env.filters['nl2br'] = nl2br
app.secret_key = "TestKey123"

# MessageTokenCounter
msg = MessageHistory(token_limit=CONTEXT)
persistant_memory = EpisodicMemory()

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('chat.html')
    
def generate(user_input, session_id):
    try:
        for chunk in message_agent.generate_message(user_input, session_id):
            token = None
            # Adds Message zu History

            if hasattr(chunk, "content") and chunk.content:
                token = chunk.content
            elif isinstance(chunk, str):
                token = chunk
            else:
                continue  # skip leere oder irrelevante Chunks

            if token.strip():
                token = token.replace("\\n", "\n")
                yield f"data: {json.dumps({'token': token})}\n\n"

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
    
    return jsonify({'session_id': session_id}), 200


@app.route('/stream/<sessionid>', methods=["GET", "POST"])
def stream_with_session_id(session_id):
    messages=msg.get_messages(session_id)
    
    if request.method == "POST":
        data = request.get_json()
        # Chatverlauf sichern (optional)
        msg.add(role=data.get("user", "User"),message=data["message"], session_id=session['id'])

        return Response(
            stream_with_context(generate(data["message"], session_id)),
            mimetype="text/event-stream"
        )
    
    return render_template('caht.html', messages=messages)
                

if __name__ == "__main__":
    app.run(debug=True)       