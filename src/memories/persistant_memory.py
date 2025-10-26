from datetime import datetime
from src.components.sql import SQL
from src.models.episodic_memory_model import ChatMessage, ChatSession, ChatSummary
from src.states.message_state import MessagesState

class PersistantMemory:
    
    def __init__(self):
        self.db_engine = SQL()
    
    def save(self, id: int, 
             session_id: str, 
             count_tokens: int,
             human_summary: str,
             ai_summary: str,
             ):
        
        session_gen = self.db_engine.get_db()
        db = next(session_gen)     
        
        try:
            # Saving Chat Session
            save_session = ChatSession(
                id=session_id
            )
            db.add(save_session)
            db.commit()
            db.flush()
            
            save_message = ChatMessage(
                session_id=session_id,
                count_tokens=count_tokens,
                human_summary=human_summary,
                ai_summary=ai_summary,
                created_at=datetime.now()
            )
            db.add(save_message)
            db.commit()
            db.flush()            

            return True
        finally:
            session_gen.close()
            
            
    def get_conversation_context(self, session_id):
        session_gen = self.db_engine.get_db()
        db = next(session_gen)    
        
        messages = db.query(ChatMessage).filter_by(session_id=session_id).all()
        conversation = "\n".join([f"{m.role}: {m.content}" for m in messages])
        return conversation
        
        
        