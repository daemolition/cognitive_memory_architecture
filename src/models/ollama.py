from langchain_ollama import ChatOllama

class LLM:
    def __init__(self, model: str ="gemma3:4b-it-q4_K_M", context: int = 32768, reasoning: bool = False):
        self.model = model
        self.context = context
        self.reasoning = reasoning
    
    def load_llm(self):
        """Initializes the llm"""        
        llm = ChatOllama(
            model=self.model,
            num_ctx=self.context,
            reasoning=self.reasoning
        )
        return llm