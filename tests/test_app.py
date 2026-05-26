from fastapi.testclient import TestClient
from http import HTTPStatus
from api_gerenciador_tarefas.app import app


def test_create_user():
    client = TestClient(app)

    resposta = client.post(
        "/users",
        json={
            "user_name": "sabrina",
            "email": "sabrina@gmail.com",
            "password": "sabrina",
        },
    )

    assert resposta.status_code == HTTPStatus.CREATED


def test_update_user():
    client = TestClient(app)
    resposta = client.put("/users/1",
        json={
            "user_name": "sabrina",
            "email": "sabrina@gmail.com",
            "password": "sabrina",
        },
    
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {"id": 1, "user_name": "sabrina","email": "sabrina@gmail.com",}