from sqlalchemy import Column, Enum as SqlEnum, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

class TaskStatus(str, Enum):

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskSchema(Base):
    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title: str = Column(String, index=True)
    description: str = Column(String, index=True, nullable=False)
    status = Column(SqlEnum(TaskStatus), index=True, nullable=False)
    created_at: DateTime = Column(DateTime, index=True)
    updated_at: DateTime = Column(DateTime, index=True)

   