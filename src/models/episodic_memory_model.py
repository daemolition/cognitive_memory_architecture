from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from typing import List, Optional

from pydantic import BaseModel

class Base(DeclarativeBase):
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class ChatSession(Base):
    __tablename__ = "chat_session"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    session_id: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # One-to-many relationship with ChatMessage
    summaries: Mapped[List["ChatSummary"]] = relationship(back_populates="session", cascade="all, delete-orphan")  
    
        
class ChatSummary(Base):
    __tablename__ = "chat_summary"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)    
    initial_question: Mapped[str] = mapped_column(String, nullable=False)
    count_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    human_summary: Mapped[str] = mapped_column(String, nullable=False)
    ai_summary: Mapped[str] = mapped_column(String, nullable=False) 
    context_summary: Mapped[str] = mapped_column(String, nullable=False)     
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)    
    
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("chat_session.session_id", ondelete="CASCADE"),
        nullable=False
    )

    session: Mapped["ChatSession"] = relationship(
        back_populates="summaries"
    )  
    
    
class ChatSessionSchema(BaseModel):
    id: int
    title: str
    created_at: datetime   
    summaries: List[str]
    
    class Config:
        from_attributes=True    

class ChatSummarySchema(BaseModel):
    id: int
    initial_question: str
    count_tokens: int
    human_summary: str
    ai_summary: str  
    context_summary: str
    created_at: datetime
    session_id: int
    
    class Config:
        from_attributes = True