from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models.models import Todo, User
from fast_zero.schemas.schemas import (
    Message,
    TodoSchema,
    TodoUpdate,
)


class TodoController:
    @staticmethod
    def create_todo(
        todo: TodoSchema,
        user: User,
        session: Session,
    ) -> Todo:
        db_todo: Todo = Todo(
            title=todo.title,
            description=todo.description,
            state=todo.state,
            user_id=user.id,
        )
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def list_todos(  # noqa: PLR0917, PLR0913
        session: Session,
        user: User,  # T_CurrentUser,
        title: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Todo]:
        query = select(Todo).where(Todo.user_id == user.id)
        if title:
            query = query.filter(Todo.title.contains(title))
        if description:
            query = query.filter(Todo.description.contains(description))
        if state:
            query = query.filter(Todo.state == state)
        todos = session.scalars(query.offset(offset).limit(limit)).all()
        return todos

    @staticmethod
    def patch_todo(
        todo_id: int, session: Session, user: User, todo: TodoUpdate
    ) -> Todo:
        db_todo = session.scalar(
            select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
        )
        if not db_todo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
            )
        for key, value in todo.model_dump(exclude_unset=True).items():
            setattr(db_todo, key, value)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete_todo(
        todo_id: int,
        session: Session,
        user: User,  # T_CurrentUser
    ) -> Message:
        todo = session.scalar(
            select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
        )
        if not todo:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
            )
        session.delete(todo)
        session.commit()
        return {'message': 'Task has been deleted successfully.'}
