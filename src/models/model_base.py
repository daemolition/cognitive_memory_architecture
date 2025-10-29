from langchain_ollama import ChatOllama
from transformers import AutoTokenizer

class LLM:
    def __init__(self, model: str ="google/gemma-3-4b-it", context: int = 32768, reasoning: bool = False):
        self.model = model
        self.context = context
        self.reasoning = reasoning
        self.tokenizer = AutoTokenizer.from_pretrained(model)
    
    def load_llm(self):
        """Initializes the llm"""        
        llm = ChatOllama(
            model=self.model,
            num_ctx=self.context,
            reasoning=self.reasoning
        )
        return llm
    
    def count_tokens(self, text: str) -> int:
        """Returns the correct number of tokens"""
        return len(self.tokenizer.encode(text, add_special_tokens=False))