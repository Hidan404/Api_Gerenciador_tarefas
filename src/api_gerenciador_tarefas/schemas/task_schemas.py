# src/api_gerenciador_tarefas/schemas/task_schemas.py
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from enum import Enum

class StatusEnum(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    status: Optional[StatusEnum] = StatusEnum.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)

    @field_validator('description')
    def validar_descrition(cls, valor: str):
        palavras = valor.split(" ")
        if len(palavras) < 3:
            raise ValueError("Descrição muito pequena")
        return valor
    
    @field_validator('created_at', 'updated_at', mode='before')
    def ensure_utc(cls, v):
        if isinstance(v, datetime):
            if v.tzinfo is None:
                return v.replace(tzinfo=timezone.utc)
            return v.astimezone(timezone.utc)
        return v


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    status: StatusEnum = StatusEnum.PENDING


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    
    @field_validator('description')
    def validar_descrition(cls, valor: str):
        palavras = valor.split(" ")
        if len(palavras) < 3:
            raise ValueError("Descrição muito pequena")
        return valor
    
    
    