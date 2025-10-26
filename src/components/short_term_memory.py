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
        memory = Redis(self.host, self.port, decode_responses=True)
        return memory
    
    def close_memory(self):
        """Closes the memory"""
        return self.memory.close()
    
    def save_short_term_memory(self, role: str, messages: str, session_id: str,  token_count: float) -> None:
        """Saves the chat session to the short term memory"""
        
        memory = self.initate_short_term_memory()
        memory.hset(session_id, mapping={
            'role': role,
            'messages': messages,
            'token_count': token_count
        })
        
        if self.ttl:
            memory.expire(session_id, self.ttl)
        
        memory.close()
        
    
    def get_short_term_memory(self, session_id: str):
        """Get the short term memory"""
        data = self.memory.hgetall(session_id)
        self.close_memory()
        return data if data else None

    def delete_short_term_memory(self, session_id: str):
        """Deletes the short term memory"""
        deleted = self.memory.delete(session_id)
        return bool(deleted)
        
        