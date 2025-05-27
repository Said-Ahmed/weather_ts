from sqlalchemy import Column, String, DateTime, Integer
from src.database import Base
from datetime import datetime


class History(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    city = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)