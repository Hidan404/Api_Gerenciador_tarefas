from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    user_name: str
    email: EmailStr


class UserDB(User):
    id: int

class UserList(BaseModel):
    users: list[UserDB]