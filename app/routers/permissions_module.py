from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.security import get_current_user, verify_user_with_roles_and_permissions
from app.models.models import Module, User
from app.schemas.permissioes_schema import (
    ModuleInShema,
    ModuleListSchema,
    ModuleOutSchema,
)
from app.schemas.schemas import Message

router = APIRouter(prefix='/permissoes', tags=['permissoes'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/module', response_model=ModuleListSchema)
def read_module(
    session: T_Session,
    user_current: T_CurrentUser,
    page: int = 1,
    page_size: int = 10
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    skip = (page - 1) * page_size
    limit = page_size

    total_records = session.scalar(select(func.count(Module.id)))
    modules = session.scalars(
        select(Module).order_by(Module.id).offset(skip).limit(limit)
    ).all()

    return {
        'modules': modules,
        'total_records': total_records,
    }


@router.get('/module/find/', response_model=ModuleListSchema)
def get_modules_by_partial_title(
    title: str,
    session: T_Session,
    user_current: T_CurrentUser,
    page: int = 1,
    page_size: int = 10
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    skip = (page - 1) * page_size
    limit = page_size
    partial_title = f'%{title}%'

    subquery = (
        select(Module).where(Module.title.like(partial_title)).subquery()
    )
    total_records = session.scalar(select(func.count()).select_from(subquery))
    modules = session.scalars(
        select(Module)
        .where(Module.title.like(partial_title))
        .order_by(Module.id)
        .offset(skip)
        .limit(limit)
    ).all()

    return {
        'modules': modules,
        'total_records': total_records,
    }


@router.get('/module/{module_id}', response_model=ModuleOutSchema)
def read_module_by_id(module_id: int, session: T_Session, user_current: T_CurrentUser):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_module = session.get(Module, module_id)

    if db_module is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil not found',
        )

    return db_module


@router.post(
    '/module', status_code=HTTPStatus.CREATED, response_model=ModuleOutSchema
)
def create_module(
    module: ModuleInShema,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_module = session.scalar(
        select(Module).where(Module.title == module.title)
    )

    if db_module:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Modulo ja cadastrado'
        )

    db_module = Module(
        title=module.title,
        permissions=[],
    )

    session.add(db_module)
    session.commit()
    session.refresh(db_module)
    return db_module


@router.put('/module/{module_id}', response_model=ModuleOutSchema)
def update_module_by_id(
    module_id: int,
    module: ModuleOutSchema,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_module = session.get(Module, module_id)

    if db_module is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Perfil not found'
        )

    if module.id != module_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Perfil ID diferentes'
        )

    db_module2 = session.scalar(
        select(Module).where(
            (Module.title == module.title) & (Module.id != module.id)
        )
    )

    if db_module2:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Nome de Perfil ja cadastrado',
        )

    for key, value in module.model_dump(exclude_unset=True).items():
        setattr(db_module, key, value)

    session.add(db_module)
    session.commit()
    session.refresh(db_module)

    return db_module


@router.delete('/module/{module_id}', response_model=Message)
def delete_module(module_id: int, session: T_Session, user_current: T_CurrentUser):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_module = session.get(Module, module_id)

    if not db_module:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Module not found.'
        )

    session.delete(db_module)
    session.commit()

    return {'message': 'Module deletado'}
