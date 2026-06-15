import asyncio

from api_gerenciador_tarefas.database.connection import Base, engine
from api_gerenciador_tarefas.models.task import Task

async def criar_tabela():
    #Base.metadata.create_all(bind=engine)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        print("tabela criada")

if __name__ == "__main__":
    asyncio.run(criar_tabela())    