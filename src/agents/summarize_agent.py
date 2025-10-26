from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.models.model_base import LLM


class SummarizeAgent:
    def __init__(self):
        self.llm = LLM(model="qwen3:4b", reasoning=True)
        self.model = self.llm.load_llm()

    def set_summarize_prompt(self):
        return ChatPromptTemplate.from_template(
            """
            You are an expert context summarizer
            Summarize the context with all key facts to help an llm continue the conversation.
            Use markup, lists and whatever is needed to use the context later on.
            Do not insert your own opinion. Just summarize.
            
            Structure the Summarization as follow:
            
            ### Chat Summary – Session {session_id}

            ### 1. Topic Overview
            - Topic A: ...
            - Topic B: ...
            - Topic C: ...

            ### 2. Key Facts
            - {Fact 1}
            - {Fact 2}
            - {Fact 3}

            ### 3. Decisions / Outcomes
            - User decided to ...
            - System responded with ...
            - Follow-up actions: ...

            ### 4. Open Questions / To-Dos
            - Still unclear: ...
            - Next step: ...

            ### 5. Mood / Tone
            - Neutral / Positive / Critical (optional)

            ### 6. Technical Context (if applicable)
            - Models used: llama-3.1 / nllb-200
            - Token usage: 1750
            - Last user message: "How can I dynamically reload LDAP?"
            
            Context: {context}
                        
            """
        )

    def summarize_content(self, content: str, session_id: str):
        summarize_chain = self.set_summarize_prompt() | self.model | StrOutputParser()

        return summarize_chain.invoke({"context": content, "session_id": session_id})
