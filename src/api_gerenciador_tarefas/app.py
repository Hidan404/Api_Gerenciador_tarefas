from fastapi import FastAPI
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from api_gerenciador_tarefas.models.task import Task
import uvicorn


from datetime import datetime

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

app = FastAPI(
    title="Gerenciador de Tarefas API", 
    version="1.0.0", 
    description="API para gerenciar tarefas, permitindo criar, ler, atualizar e excluir tarefas." 
)

@app.get("/")
def read_root():
    return JSONResponse(content=tarefas, status_code=status.HTTP_200_OK)

@app.get("/{tarefa_id}",status_code=status.HTTP_200_OK)
def tarefa_get(tarefa_id: int):
    for t in tarefas:
        if t["id"] == tarefa_id:
            return JSONResponse(content=t, status_code=status.HTTP_200_OK)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado")

@app.post("/", status_code=status.HTTP_201_CREATED)
def banda_post(task: Task):
    if task.id is not None:
        id_existentes = [t["id"] for t in tarefas]
        print(id_existentes)

        if task.id in id_existentes:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="ja existe ")
        
        nova_tarefa = task.model_dump()
        tarefas.append(nova_tarefa)

        return JSONResponse(content={"message": "Tarefa criada com sucesso"}, status_code=status.HTTP_201_CREATED)


@app.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
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
    

@app.delete("/{id}",status_code=status.HTTP_200_OK)
def tarefas_delete(id: int,):
    for t in tarefas:
        if t["id"] == id:
            tarefas.remove(t)
            return JSONResponse(content={"message": "Tarefa deletada com sucesso"}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



