from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from typing import List, Optional

class Base(DeclarativeBase):
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class ChatSession(Base):
    __tablename__ = "chat_session"
    
    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # One-to-many relationship with ChatMessage
    messages: Mapped[List["ChatMessage"]] = relationship(back_populates="session", cascade="all. delete-orphan")
    

class ChatMessage(Base):
    __tablename__ = "chat_message"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_session.id"))
    role: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # One-to-one relationship with ChatSession
    session: Mapped["ChatSession"] = relationship(back_populates="messages")
        
        
class ChatSummary(Base):
    __tablename__ = "chat_summary"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)    
    initial_question: Mapped[str] = mapped_column(String, nullable=False)
    count_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    human_summary: Mapped[str] = mapped_column(String, nullable=False)
    ai_summary: Mapped[str] = mapped_column(String, nullable=False)  
    created_at: Mapped[str] = mapped_column(String, nullable=False)    
    
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_session.id"))
    session: Mapped["ChatSession"] = relationship()  
