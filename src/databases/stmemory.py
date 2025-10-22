from datetime import datetime

from src.components.sql import SQL
from src.models.stmemory_db_model import StMemory

class StMemoryDatabase:
    def __init__(self):
        self.db_engine = SQL()
    
    def save(self, id: int, 
             session_id: str, 
             initial_question: str,
             count_tokens: int,
             human_summary: str,
             ai_summary: str,
             ):
        
        session_gen = self.db_engine.get_db()
        db = next(session_gen)
        
        try:
            save_memory = StMemory(
                session_id=session_id,
                initial_question=initial_question,
                count_tokens=count_tokens,
                human_summary=human_summary,
                ai_summary=ai_summary,
                created_at=datetime.now()
            )
            db.add(save_memory)
            db.commit()
            db.refresh(save_memory)
            return save_memory
        finally:
            session_gen.close()
        
        
        