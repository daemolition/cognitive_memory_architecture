from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class MessagesState(BaseModel):
    session_id: Optional[int] = None
    context: List[Dict[str, str]] = Field(default_factory=list, description="""Conversation between Humand and AI Assistant""")  
    context_summary: str = Field(default="", description="""Memory State""")  
    token_count: int = Field(default=0, description="""Current token usage""")
    last_summary: Optional[str] = Field(default=None, description="""Last generated Summary""")
    trigger_summary: bool = Field(default=False, description="Flag if summary generation ist needed")