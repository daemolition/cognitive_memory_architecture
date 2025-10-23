
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.models.ollama import LLM


class Summarizer:
    def __init__(self):
        self.llm = LLM()
        self.model = self.llm.load_llm()
        
    def set_summarize_prompt(self):
        return PromptTemplate.from_template(
            """
            You are an expert context summarizer
            Summarize the context with all key facts to help an llm continue the conversation.
            Use markup, lists and whatever is needed to use the context later on.
            Do not insert your own opinion. Just summarize.
            
            Use maximum 10% of the the context for the summarization.
            
            <context>
            {context}
            </context>
            
            """
        )
        
    def summarize_text(self, text: str):
        summarize_chain = (
            self.set_summarize_prompt() |
            self.model |
            StrOutputParser()
        )
        
        return summarize_chain.invoke({'context':text})
        