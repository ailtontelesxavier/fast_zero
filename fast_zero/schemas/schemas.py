from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class UserFull(UserPublic):
    created_at: datetime
    updated_at: datetime


class ListUserFull(BaseModel):
    rows: list[UserFull]
    total_records: int


class UserPasswordUpdate(BaseModel):
    password: str


class UserList(BaseModel):
    users: list[UserPublic]
    total_records: int
    page: int
    page_size: int


class UserRolesSchema(BaseModel):
    user_id: int
    role_id: int


class UserRolesPublic(UserRolesSchema):
    id: int


class UserRolesList(BaseModel):
    rows: list[UserRolesPublic]
    total_records: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TodoState


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
