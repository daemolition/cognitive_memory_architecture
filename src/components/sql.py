import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from ..models.persistant_memory_model import Base

class SQL:
    def __init__(self, filename: str="stmemory.sqlite3"):
        self.filename = filename
        self.database_uri = f"postgresql+psycopg2://postgres:postgres@localhost:5432/lstm_rag"
        self.engine = self.get_engine()
        self.SessionLocal = scoped_session(sessionmaker(bind=self.engine, autoflush=False, autocommit=False))
        
        self.metadata = Base.metadata
        
    def create_all(self):
        Base.metadata.create_all(bind=self.engine)
        
    def get_db(self):
        db: Session = self.SessionLocal()
        try:
            yield db
        except Exception as e:
            logging.error("Error using the db session: %s", e)          
        finally:
            db.close()
            
    def get_engine(self):
        return create_engine(self.database_uri)