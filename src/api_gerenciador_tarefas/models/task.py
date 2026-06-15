from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
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






tarefas = [
    {
        "id": 1,
        "title": "Estudar FastAPI",
        "description": "Aprender a criar rotas e usar o Pydantic para validação.",
        "status": "in_progress",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": 2,
        "title": "Configurar o Banco de Dados",
        "description": "Criar as tabelas usando SQLAlchemy ou outro ORM.",
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": 3,
        "title": "Corrigir bug da URL do ViaCEP",
        "description": "Adicionar o protocolo https:// na requisição do script.",
        "status": "completed",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
]    