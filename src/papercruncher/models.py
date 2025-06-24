from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime


BaseModel = declarative_base()


class Paper(BaseModel):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    summary = Column(String, nullable=False)
    authors = Column(String, nullable=True)
    published = Column(DateTime, default=datetime.utcnow)
