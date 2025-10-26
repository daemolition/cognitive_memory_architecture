import itertools

from .persistant_memory import PersistantMemory
from .short_term_memory import ShortTermMemory
from ..agents.summarize_agent import SummarizeAgent


class MessageHistory:
    """
    This class manages a history of messages between two users. It uses two types of memory: persistent and short-term.

    Attributes:
        persistent_memory (PersistantMemory): An instance of PersistantMemory to store long-term messages.
        short_term_memory (ShortTermMemory): An instance of ShortTermMemory to store recent messages.
    """

    def __init__(self, token_limit: int = 8192):
        """
        Initializes the Message history
        Args:
            token_limit(int): The tokens provided with a standard value for counting and initiating the summary
            short_term_memory(Redis): The redis database for the conversional message history
        """

        self.token_limit = token_limit
        self.short_term_memory = ShortTermMemory()
        self.persitant_memory = PersistantMemory()


    def add(self, role: str, message: str, session_id: str):
        self.short_term_memory.save_short_term_memory(
            role=role,
            messages=message,
            session_id=session_id,
            token_count=self.total_tokens(session_id),
        )

        if self.total_tokens(session_id) > self.token_limit * 0.8:
            return True
        return False

    def total_tokens(self, session_id: str) -> int:
        """Estimate total token usage for a session based on message content length."""
        messages = self.get_messages(session_id=session_id)
        total = sum(
            len(m["content"]) / 4 for m in messages
        )  # /4 als Schätzwert (≈ GPT-Tokenisierung)
        return int(total)

    def get_messages(self, session_id: str):
        return self.short_term_memory.get_short_term_memory(session_id=session_id)

    def summarize_content(self, session_id: str):
        """Summarizes and saving the messages"""

        summarizer = SummarizeAgent()

        # Extract the messages per role from the memory
        human_msg = [
            message
            for message in self.get_messages(session_id)
            if message["role"] == "user"
        ]
        ai_message = [
            message
            for message in self.get_messages(session_id)
            if message["role"] == "assistant"
        ]
        
        # Combines the text for each role
        human_text = "\n".join([message["content"] for message in human_msg])
        ai_text = "\n".join([message["content"] for message in ai_message])
        
        # Summarize the text per Role
        human_summary = summarizer.summarize_content(human_text, session_id)
        ai_summay = summarizer.summarize_content(ai_text, session_id)

        # Summarize combined
        combined_summary = summarizer.summarize_content(f"{human_summary}\n{ai_summay}", session_id)
        
        # Save to Database
        
        
        