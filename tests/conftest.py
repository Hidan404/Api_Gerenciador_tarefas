import pytest
from fastapi.testclient import TestClient
from api_gerenciador_tarefas.app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from api_gerenciador_tarefas.models.user_schema import tabela_registro



@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    # Configura um banco de dados em memória para testes
    engine = create_engine("sqlite:///:memory:")
    tabela_registro.metadata.create_all(engine)
    session = Session(bind=engine.connect())
    yield session
    session.close()