from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy.orm import Mapped, registry, mapped_column
from sqlalchemy import func

tabela_registro = registry()

# 1. MODELO DO BANCO DE DADOS (SQLAlchemy)
@tabela_registro.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True) 
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


# 2. SCHEMAS DA API (Pydantic v2)
class UserSchema(BaseModel):
    """Dados recebidos para criar um usuário."""
    user_name: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """Dados retornados publicamente pela API (sem senha)."""
    id: int
    user_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserDB(UserPublic):
    """Representação interna com senha, caso o app.py precise."""
    password: str


class UserList(BaseModel):
    """Lista de usuários para paginação ou listagem."""
    users: list[UserPublic]

