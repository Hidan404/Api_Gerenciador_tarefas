from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status
from api_gerenciador_tarefas.models.task import Task
from api_gerenciador_tarefas.schemas.task_schemas import TaskSchema, TaskUpdateSchema
from typing import List
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from  api_gerenciador_tarefas.database.connection import get_session

router = APIRouter()



@router.post("/tarefas",status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
async def criar_tarefa(tarefa: TaskSchema, db: AsyncSession = Depends(get_session)):
    try:
        nova_tarefa = Task(
            title=tarefa.title,
            description=tarefa.description,
            status=tarefa.status.value if tarefa.status else "pending"
        )
        db.add(nova_tarefa)
        await db.commit()
        await db.refresh(nova_tarefa)
        return nova_tarefa
    except Exception:
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

        return resultado.scalar_one_or_none()
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
        tarefa_banco_atualizar.created_at = tarefa.created_at
        tarefa_banco_atualizar.updated_at = tarefa.updated_at

        await db.commit()
        await db.refresh(tarefa_banco_atualizar)

        return tarefa_banco_atualizar
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontraa")    
    

@router.patch("/tarefas/{tarefa-id}", response_model=TaskSchema)
async def atualizar_tarefa(tarefa_id: int, tarefa_data: TaskUpdateSchema, db: AsyncSession = Depends(get_session)):
    query = select(Task).where(Task.id == tarefa_id)
    resultado = await db.execute(query)
    tarefa = resultado.scalar_one_or_none()

    if not tarefa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    
    dados = tarefa_data.model_dump(exclude_unset=True)
    for campo, valor in dados.items():
        setattr(tarefa, campo, valor)

    tarefa.updated_at = datetime.now(timezone.utc)    

    await db.commit()
    await db.refresh(tarefa)
    
    return tarefa


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