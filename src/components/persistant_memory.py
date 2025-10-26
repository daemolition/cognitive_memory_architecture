from datetime import datetime
from src.components.sql import SQL
from src.models.persistant_memory_model import ChatSession, ChatSummary
from src.states.message_state import MessagesState

class PersistantMemory:
    """
    This class is responsible for managing persistent memory in the chat application.
    It stores and retrieves chat sessions and summaries using a database.
    """
    def __init__(self):
        """Initializes the SQL Engine"""
        self.db_engine = SQL()
        self.session_gen = self.db_engine.get_db()
    
    def save_session(self, session_id: str, title: str) -> None: 
        """Saves the session to the database"""
        db = next(self.session_gen)     
        
        try:
            # Saving Chat Session
            save_session = ChatSession(
                id=session_id,
                title=title
            )
            db.add(save_session)
            db.commit()
            db.flush()    

        finally:
            self.session_gen.close()
            
    def save_summary(self, **params: dict):
        """Saves the summary to the database"""
        
        db = next(self.session_gen)
        
        try:
            save_summary = ChatSummary(
                initial_question=params.get('initial_question', ''),
                count_tokens=params.get('token_count', 0),
                human_summary=params.get('human_summary', ''),
                ai_summary=params.get('ai_summary', ''),
                context_summary=params.get('context_summary', ''),
                created_at=datetime.now().utcnow
                )
            db.add(save_summary)
            db.commit()
            db.flush()
            print("Successfully saved summary to database")
        except Exception as e:
            print(f"Error saving summary to database: {e}")

        