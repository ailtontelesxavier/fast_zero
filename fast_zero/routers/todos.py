from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from fast_zero.controllers.todo_controller import TodoController
from fast_zero.core.database import get_session
from fast_zero.core.security import get_current_user
from fast_zero.models.models import User
from fast_zero.schemas.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: T_CurrentUser,
    session: T_Session,
):
    return TodoController.create_todo(todo, user, session)


@router.get('/', response_model=TodoList)
def list_todos(  # noqa
    session: T_Session,
    user: T_CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    todos = TodoController.list_todos(
        session, user, title, description, state, offset, limit
    )
    return {'todos': todos}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: T_Session, user: T_CurrentUser, todo: TodoUpdate
):
    return TodoController.patch_todo(todo_id, session, user, todo)


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: T_CurrentUser):
    return TodoController.delete_todo(todo_id, session, user)
