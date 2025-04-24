# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from threading import Lock
from models.db_models import Base

class Database:
    _instance = None
    _lock = Lock()

    def __init__(self, db_url: str = "sqlite:///./image_cms.db"):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)  # Create tables on first run
        self._initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def get_session(self) -> Session:
        return self.SessionLocal()
