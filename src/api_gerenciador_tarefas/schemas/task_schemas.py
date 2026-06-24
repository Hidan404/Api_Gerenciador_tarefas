# src/api_gerenciador_tarefas/schemas/task_schemas.py
from datetime import datetime
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
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)

    @field_validator('description')
    def validar_descrition(cls, valor: str):
        palavras = valor.split(" ")
        if len(palavras) < 3:
            raise ValueError("Descrição muito pequena")
        return valor
    
    @model_validator(mode="after")
    def validator_criado_na_data(self):
        if self.updated_at < self.created_at:
            raise ValueError("Data de atualizacao nao pode ser do perido inferior ao criado")
        return self


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
    
    
    