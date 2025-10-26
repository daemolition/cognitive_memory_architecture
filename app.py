import streamlit as st
import time
from flask import Flask, render_template, request, session, redirect, url_for, Response, stream_with_context, jsonify, json 
import uuid

from src.databases.semantic_memory import SemanticMemory
from src.databases.message_history import MessageHistory
from src.databases.persistant_memory import PersistantMemory
from src.agents.message_agent import MessageAgent
from src.models.persistant_memory_model import ChatMessage, ChatSession, ChatSummary, Base
from src.components.sql import SQL
from src.models.ollama import LLM

from langchain_core.messages import AIMessage, HumanMessage
from markupsafe import Markup
from markdown import markdown

# Initialize the database
sql = SQL()
Base.metadata.create_all(sql.get_engine())

# Overall context
CONTEXT = 32768

# Model
model = LLM(context=CONTEXT)

# Agent
message_agent = MessageAgent()

# Markup Patch
def nl2br(value):
    return Markup(value.replace("\n", "<br>\n"))

app = Flask(__name__)
app.jinja_env.filters['nl2br'] = nl2br
app.secret_key = "TestKey123"

# MessageTokenCounter
msg = MessageHistory(token_limit=CONTEXT)
persistant_memory = PersistantMemory()

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('chat.html', messages=msg.get_messages())
    
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
    data = request.get_json()
    # Chatverlauf sichern (optional)
    msg.add(role=data.get("user", "User"),content=data["message"], session_id=session['id'])

    return Response(
        stream_with_context(generate(data["message"], session_id)),
        mimetype="text/event-stream"
    )
                

if __name__ == "__main__":
    app.run(debug=True)       