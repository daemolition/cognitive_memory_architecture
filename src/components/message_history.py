import itertools

from .episodic_memory import EpisodicMemory
from .short_term_memory import ShortTermMemory
from ..agents.summarize_agent import SummarizeAgent


class MessageHistory:
    """
    This class manages a history of messages between two users. It uses two types of memory: persistent and short-term.

    Attributes:
        persistent_memory (EpisodicMemory): An instance of EpisodicMemory to store long-term messages.
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
        self.episodic_memory = EpisodicMemory()


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
            len(m["messages"]) / 4 for m in messages
        )  # /4 als Schätzwert (≈ GPT-Tokenisierung)
        return int(total)

    def get_messages(self, session_id: str):
        return self.short_term_memory.get_short_term_memory(session_id=session_id)

    def summarize_content(self, session_id: str) -> None:
        """Summarizes and saving the messages"""

        summarize_agent = SummarizeAgent()

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
        human_summary = summarize_agent.summarize_content(human_text, session_id)
        ai_summary = summarize_agent.summarize_content(ai_text, session_id)

        # Summarize combined
        combined_summary = summarize_agent.summarize_content(f"{human_summary}\n{ai_summary}", session_id)
        
        # Get the first user message for context
        first_user_question = self.short_term_memory.get_first_question(session_id)
        
        # Follow up question after summary
        first_follow_up_question = self.short_term_memory.get_first_follow_up_question(session_id)
        
        # Check if there is already a summary in database
        summary_check = self.episodic_memory.get_summary(session_id)
        
        # Condition for initial question
        if summary_check is not None:
            question = first_user_question
        else:
            question = first_follow_up_question
        
        # Save to Database
        self.episodic_memory.save_summary(params={
            'initial_question': question,
            'tokens_count': self.total_tokens(session_id),
            'human_summary': human_summary,
            'ai_summary': ai_summary,
            'session_id': session_id,
            'context_summary': combined_summary,
        })
        
        # Inject to redis
        self.short_term_memory.save_short_term_memory(role='system', messages=combined_summary, session_id=session_id, token_count=0)
        
        
        