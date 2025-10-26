
from src.databases.semantic_memory import LtMemory
from .persistant_memory import PersistantMemory

class MessageHistory:
    def __init__(self, token_limit: int = 8192):
        self.messages = []
        self.token_limit = token_limit     
        self.ltmemory = LtMemory()   
        
    def add(self, role: str, content: str, session_id: str):
        self.messages.append({'role': role, 'content': content, 'session_id': session_id})
        print(self.messages)
        
        # Save to VectorDatabase -> LT Memory
        self.ltmemory.add_message(message=content, session_id=session_id, role=role)      

       
        if self.total_tokens() > self.token_limit * 0.8:
            return True
        return False
    
    def total_tokens(self):
        return sum(len(m['content']) / 4 for m in self.messages)
    
    def clear(self):
        self.messages = []
        
    def get_messages(self):
        return self.get_messages
        