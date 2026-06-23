from fastapi import FastAPI
import uvicorn
from api_gerenciador_tarefas.routers.tarefas_routers import router 




app = FastAPI(
    title="Gerenciador de Tarefas API", 
    version="1.0.0", 
    description="API para gerenciar tarefas, permitindo criar, ler, atualizar e excluir tarefas."
)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True, app_dir="src/api_gerenciador_tarefas")






