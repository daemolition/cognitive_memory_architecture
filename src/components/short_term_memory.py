import json

from redis import Redis
from typing import Optional, Literal



class ShortTermMemory:
    """
    A class that provides a simple interface for storing and retrieving short-term memory data using Redis.

    Attributes:
        redis_client (Redis): The Redis client used to interact with the Redis server.
        key_prefix (str): The prefix used for all keys in the Redis database.
    """
    
    def __init__(self, host: str='localhost', port: int=6379, ttl: Optional[int] = 3600):
        """Class for short term Memory"""
        self.host = host
        self.port = port
        self.ttl = ttl
        self.memory = self.initate_short_term_memory()
        
        
    def initate_short_term_memory(self):
        """Initiase the short term memory"""
        return Redis(self.host, self.port, decode_responses=True)
    
    
    def close_memory(self):
        """Closes the memory"""
        return self.memory.close()
    
    
    def save_short_term_memory(self, role: str, messages: str, session_id: str,  token_count: float) -> None:
        """Saves the chat session to the short term memory"""
        
        key = f"session:{session_id}:messages"
        msg = json.dumps({
            'role': role,
            'messages': messages,
            'token_count': token_count
        })
        
        self.memory.rpush(key, msg)
        
        if self.ttl:
            self.memory.expire(session_id, self.ttl)
        
        self.memory.close()
        
        
    def get_first_question(self, session_id: str) -> str | None:
        """Returns the first user question for saving to the summary"""
        key = f"session:{session_id}:messages"
        
        # Check for user input
        messages = self.memory.lrange(key, 0, -1)
        
        for msg_json in messages:
            msg = json.loads(msg_json)
            if msg['role'] == 'user':
                return msg["content"]
        return None
    
    
    def get_first_follow_up_question(self, session_id: str) -> str | None:
        """Returns the first follow up user question after summarize"""
        key = f"session:{session_id}:messages"
        messages = self.memory.lrange(key, -10, -1)
        parsed = [json.loads(m) for m in messages]
        
        # Last user entry after summary
        for msg in reversed(parsed):
            if msg['role'] == 'user':
                return msg['content']
        return None
    
    def get_short_term_memory(self, session_id: str, limit: int = 50) -> list:
        """Get the short term memory"""
        key = f"session:{session_id}:messages"
        messages = self.memory.lrange(key, -limit, -1)
        return [json.loads(m) for m in messages]
    
    
    def trim_messages(self, session_id: str, keep_last=6):
        """Trims the short term memory to the last 6 entries"""
        key = f"session:{session_id}:messages"
        self.memory.ltrim(key, -keep_last, -1)


    def delete_short_term_memory(self, session_id: str):
        """Deletes the short term memory"""
        key = f"session:{session_id}:messages"
        deleted = self.memory.delete(key)
        return bool(deleted)      