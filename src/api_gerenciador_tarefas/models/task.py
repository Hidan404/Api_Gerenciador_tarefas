# src/api_gerenciador_tarefas/models/task.py
from datetime import datetime
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from api_gerenciador_tarefas.database.connection import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)





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