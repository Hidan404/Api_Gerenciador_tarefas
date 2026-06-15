from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from api_gerenciador_tarefas.models.task import Task
from api_gerenciador_tarefas.schemas.task_schemas import TaskSchema
from typing import List
from api_gerenciador_tarefas.models.task import tarefas
from sqlalchemy.ext.asyncio import AsyncSession
from  api_gerenciador_tarefas.database.connection import get_session

router = APIRouter()

'''id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
'''


@router.post("/tarefas",status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
async def criar_tarefa(tarefa: TaskSchema, db: AsyncSession = Depends(get_session)):
    try:
        nova_tarefa = Task(
            title=tarefa.title,
            description=tarefa.description,
            status=tarefa.status.value,
            created_at=tarefa.created_at.isoformat(),
            updated_at=tarefa.updated_at.isoformat()
        )
        db.add(nova_tarefa)
        db.commit()
        return nova_tarefa
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao salvar no banco de dados")



