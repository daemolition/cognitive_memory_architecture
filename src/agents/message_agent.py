
from src.models.ollama import LLM
from langchain_core.messages import HumanMessage
import uuid

class MessageAgent:
    def __init__(self):
        self.model = LLM()
        self.llm = self.model.load_llm()        
        
        
    def generate_message(self, user_input: str, session_id: str):
        
        call_id = str(uuid.uuid4())
        config = {"configurable": {"session_id": session_id}}

        print(f"[{session_id}] Start call {call_id}")

        try:
            for chunk in self.llm.stream([HumanMessage(content=user_input)], config=config):
                if chunk.content:
                    yield chunk.content
            yield "[DONE]"
        except Exception as e:
            print("Error:", e)
            yield f"Error: {str(e)}"
    