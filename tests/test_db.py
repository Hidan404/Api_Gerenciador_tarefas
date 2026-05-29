from src.api_gerenciador_tarefas.models.user_schema import User

def test_create_db(session):
    user = User(user_name="ronald", email="ererer",password="deus")
    breakpoint()
    session.add(user)
    session.commit()
    assert user.password == "deus"