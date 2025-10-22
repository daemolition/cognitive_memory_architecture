import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

class SQL:
    def __init__(self, filename: str="stmemory.sqlite3"):
        self.filename = filename
        self.sqlite_uri = f"sqlite:///{self.filename}"
        self.connection_args = {"check_same_thread": False}
        self.engine = create_engine(self.sqlite_uri, connect_args=self.connection_args)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        
    def get_db(self):
        db: Session = self.SessionLocal()
        try:
            yield db
        except Exception as e:
            logging.error("Error using the db session: %s", e)          
        finally:
            db.close()