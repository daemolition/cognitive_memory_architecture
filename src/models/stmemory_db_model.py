from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass

class StMemory(Base):
    __tablename__ = "stmemory"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_question: Mapped[str] = mapped_column(String, nullable=False)
    count_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    human_summary: Mapped[str] = mapped_column(String, nullable=False)
    ai_summary: Mapped[str] = mapped_column(String, nullable=False)  
    created_at: Mapped[str] = mapped_column(String, nullable=False)  
    
    def  to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
