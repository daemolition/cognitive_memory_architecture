from datetime import datetime
from src.components.sql import SQL
from src.models.episodic_memory_model import ChatSession, ChatSummary
from src.states.message_state import MessagesState

class EpisodicMemory:
    """
    This class is responsible for managing persistent memory in the chat application.
    It stores and retrieves chat sessions and summaries using a database.
    """
    def __init__(self):
        """Initializes the SQL Engine"""
        self.db_engine = SQL()
        self.session_gen = self.db_engine.get_db()
    
    def save_session(self, session_id: str, title: str) -> None: 
        """Saving the session to the database"""
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
        """Saving the summary to the database"""
        
        db = next(self.session_gen)
        
        try:
            save_summary = ChatSummary(
                initial_question=params.get('initial_question', ''),
                count_tokens=params.get('token_count', 0),
                human_summary=params.get('human_summary', ''),
                ai_summary=params.get('ai_summary', ''),
                session_id=params.get('session_id', ''),
                context_summary=params.get('context_summary', ''),
                created_at=datetime.now().utcnow
                )
            db.add(save_summary)
            db.commit()
            db.flush()
            print("Successfully saved summary to database")
        except Exception as e:
            print(f"Error saving summary to database: {e}")
            
            
    def get_summary(self, session_id: str) -> str | None:
        """Retrieve summary from database"""
        
        db = next(self.session_gen)
        
        try:
            # Filter by summary id and ordered by id descending to get the last entry
            retrieve_summary = db.query(ChatSummary) \
                                .filter_by(session_id=session_id) \
                                .order_by(ChatSummary.id.desc()) \
                                .first()
            if retrieve_summary:
                return retrieve_summary.context_summary
            else:
                return None
        except Exception as e:
            print(f"Error retrieving summary: {e}")

        