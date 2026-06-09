from fastapi import FastAPI
from fastapi import status, HTTPException
import uvicorn


bandas = [
    {
        "id": 1,
        "nome": "Dir en Grey",
        "musica": "The Final",
        "duracao": "4:45"
    },
    {
        "id": 2,
        "nome": "the GazettE",
        "musica": "Filth in the Beauty",
        "duracao": "4:32"
    },
    {
        "id": 3,
        "nome": "Versailles",
        "musica": "Ascendead Master",
        "duracao": "4:15"
    }
]

app = FastAPI(
    title="Gerenciador de Tarefas API", 
    version="1.0.0", 
    description="API para gerenciar tarefas, permitindo criar, ler, atualizar e excluir tarefas." 
)

@app.get("/")
def read_root():
    return {"message": bandas}

@app.get("/{banda_id}",status_code=status.HTTP_200_OK)
def banda_get(banda_id: int):
    for i in bandas:
        if i["id"] == banda_id:
            print(i["id"])
            return i
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



