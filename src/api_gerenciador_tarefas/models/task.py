from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class StatusEnum(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(BaseModel):
    id:Optional[int] =None
    title: str
    description: str
    status: Optional[StatusEnum]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)