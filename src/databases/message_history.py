

class MessageHistory:
    def __init__(self, token_limit: int = 8192):
        self.messages = []
        self.token_limit = token_limit
        
        
    def add(self, role: str, content: str):
        self.messages.append({'role': role, 'content': content})
        if self.total_tokens() > self.token_limit * 0.8:
            return True
        return False
    
    def total_tokens(self):
        return sum(len(m['content']) / 4 for m in self.messages)
    
    def clear(self):
        self.messages = []
        