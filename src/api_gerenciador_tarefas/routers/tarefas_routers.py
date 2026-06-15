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
            created_at
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao salvar no banco de dados")



@router.get("/tarefas", description="Retorna a lista de todas as tarefas", status_code=status.HTTP_200_OK, summary="Listar Tarefas",response_model=List[Task])
def read_root():
    return JSONResponse(content=tarefas, status_code=status.HTTP_200_OK)

@router.get("/tarefas/{tarefa_id}",status_code=status.HTTP_200_OK, description="Retorna os detalhes de uma tarefa específica com base no ID fornecido", summary="Obter Detalhes da Tarefa", response_model=Task)
def tarefa_get(tarefa_id: int):
    for t in tarefas:
        if t["id"] == tarefa_id:
            return JSONResponse(content=t, status_code=status.HTTP_200_OK)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado")

@router.post("/tarefas", status_code=status.HTTP_201_CREATED, response_model=Task, description="Cria uma nova tarefa com os dados fornecidos", summary="Criar Tarefa")
def banda_post(task: Task):
    if task.id is not None:
        id_existentes = [t["id"] for t in tarefas]
        print(id_existentes)

        if task.id in id_existentes:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="ja existe ")
        
        nova_tarefa = task.model_dump()
        tarefas.append(nova_tarefa)

        return JSONResponse(content={"message": "Tarefa criada com sucesso"}, status_code=status.HTTP_201_CREATED)


@router.put("/tarefas/{id}", status_code=status.HTTP_202_ACCEPTED)
def tarefa_update(id: int, task: Task):
    for t in tarefas:
        if t["id"] == id:
            t["title"] = task.title
            t["description"] = task.description
            t["status"] = task.status.value
            t["created_at"] = task.created_at.isoformat()
            t["updated_a"] = task.updated_at.isoformat()

            return JSONResponse(content={"message": "Tarefa atualizada com sucesso"}, status_code=status.HTTP_202_ACCEPTED)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado")
    

@router.delete("/tarefas/{id}",status_code=status.HTTP_200_OK)
def tarefas_delete(id: int,):
    for t in tarefas:
        if t["id"] == id:
            tarefas.remove(t)
            return JSONResponse(content={"message": "Tarefa deletada com sucesso"}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado")



