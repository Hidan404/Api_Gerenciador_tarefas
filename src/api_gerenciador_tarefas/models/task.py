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