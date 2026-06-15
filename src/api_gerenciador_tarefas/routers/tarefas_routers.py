from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Erro interno ao salvar no banco de dados"
                )


@router.get("/tarefas",status_code=status.HTTP_200_OK,response_model=List[TaskSchema])
async def ler_tarefas( db: AsyncSession = Depends(get_session)):
    query = select(Task)
    resultado= await db.execute(query)

    return resultado.scalars().all()



@router.get("/tarefas/{tarefa_id}",status_code=status.HTTP_200_OK, response_model=TaskSchema)
async def ler_tarefas_id(tarefa_id: int, db: AsyncSession = Depends(get_session)):
    try:
        query = select(Task).filter(Task.id == tarefa_id)
        resultado = await db.execute(query)

        return resultado.scalars().all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@router.put("/tarefas/{tarefa_id}", status_code=status.HTTP_200_OK,response_model=TaskSchema)
async def atualizar_tarefa(tarefa_id: int, tarefa: TaskSchema , db: AsyncSession = Depends(get_session)):
    
    query = select(Task).where(Task.id == tarefa_id)
    resultado = await db.execute(query)

    tarefa_banco_atualizar = resultado.scalar_one_or_none()

    if tarefa_banco_atualizar:
        tarefa_banco_atualizar.title = tarefa.title
        tarefa_banco_atualizar.description = tarefa.description
        tarefa_banco_atualizar.status = tarefa.status.value if tarefa.status else tarefa_banco_atualizar.status
        
        # Dica: O PostgreSQL aceita o objeto datetime direto, não precisa do .isoformat()!
        tarefa_banco_atualizar.created_at = tarefa.created_at
        tarefa_banco_atualizar.updated_at = tarefa.updated_at

        await db.commit()
        await db.refresh(tarefa_banco_atualizar)

        return tarefa_banco_atualizar
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontraa")    
    

@router.delete("/tarefas/{tarefa_id}",status_code=status.HTTP_204_NO_CONTENT)
async def deletar_tarefa(tarefa_id: int,db: AsyncSession = Depends(get_session)):
    query = select(Task).filter(Task.id == tarefa_id)
    resultado = await db.execute(query)
    deletado_tarefa = resultado.scalar_one_or_none()

    if deletado_tarefa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarefa não pode ser deletada")  
    else:
        await db.delete(deletado_tarefa)
        await db.commit()