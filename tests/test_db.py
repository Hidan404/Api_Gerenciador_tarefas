from src.api_gerenciador_tarefas.models.user_schema import User

def test_create_db():
    user = User(user_name="ronald", email="ererer",password="deus")

    assert user.password == "deus"