from langchain_ollama import ChatOllama

class LLM:
    def __init__(self, model="gemma3:4b-it-q4_K_M"):
        self.model = model
    
    def llm(self):
        """Initializes the llm"""        
        llm = ChatOllama(
            model=self.model,
            num_ctx=32768,
        )
        return llm