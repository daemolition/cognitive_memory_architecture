
from src.models.model_base import LLM
from langchain_core.messages import HumanMessage
import uuid

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
        
        
    def generate_message(self, user_input: str, session_id: str):
        """Generates the chat message"""
        
        config = {"configurable": {"session_id": session_id}}

        try:
            for chunk in self.llm.stream([HumanMessage(content=user_input)], config=config):
                if chunk.content:
                    yield chunk.content
            yield "[DONE]"
        except Exception as e:
            print("Error:", e)
            yield f"Error: {str(e)}"
    