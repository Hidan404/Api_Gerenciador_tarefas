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

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(SqlEnum(TaskStatus), index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)