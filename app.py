import streamlit as st

from src.databases.ltmemory import LtMemory
from src.databases.stmemory import StMemory
from src.databases.message_history import MessageHistory
from src.agents.message_agent import LLM
from src.models.stmemory_db_model import StMemory, Base
from src.components.sql import SQL

# Initialize the database
sql = SQL()
Base.metadata.create_all(sql.get_engine())

# Overall context
CONTEXT = 32768

