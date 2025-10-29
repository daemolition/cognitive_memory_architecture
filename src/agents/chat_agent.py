
from src.models.model_base import LLM
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from ..components.short_term_memory import ShortTermMemory


class ChatAgent:
    """
    A class for handling interactions with a language model to engage in conversations.

    Attributes:
        llm (LLM): An instance of the language model that the chat agent will use to generate responses.
        history (list): A list of conversation messages, where each message is an instance of HumanMessage.
    """

    def __init__(self):
        self.model = LLM()
        self.llm = self.model.load_llm()       
        self.short_term_memory = ShortTermMemory()         
        
    def generate_message(self, user_input: str, session_id: str, history=None):
        """Generates the chat message"""
        
        config = {"configurable": {"session_id": session_id}}
        
        messages = []
        
        # Add full history (human + assistant)
        if history:
            for item in history:
                messages.append({
                    'role': item['role'],
                    'content': item['messages']
                })

        # Add the new user input at the end
        messages.append({'role': 'user', 'content': user_input, "session_id": session_id})
        
        try:
            for chunk in self.llm.stream(messages, config=config):
                if chunk.content:
                    yield chunk.content
            yield "[DONE]"
            
        except Exception as e:
            print("Error:", e)
            yield f"Error: {str(e)}"
    