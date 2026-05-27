from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from api_gerenciador_tarefas.models.user_schema import User, UserPublic, UserDB, UserList

app = FastAPI()
usuarios = []


@app.get("/usersList", status_code=HTTPStatus.OK, response_model=UserList)
def users():
    return {"users": usuarios}

@app.get("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def user(user_id: int):
    for user in usuarios:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado")

@app.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: User):
    user_with_id = UserDB(
        user_name=user.user_name,
        email=user.email,
        password=user.password,
        id=len(usuarios) + 1,
    )
    usuarios.append(user_with_id)

    return user_with_id

@app.put("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int ,user: User):
    if  user_id not in [userio.id for userio in usuarios]:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado")

    dados_novos = UserDB(
        user_name=user.user_name,
        email=user.email,
        password=user.password,
        id=user_id,
    )
    usuarios[user_id -1] = dados_novos
    return dados_novos

