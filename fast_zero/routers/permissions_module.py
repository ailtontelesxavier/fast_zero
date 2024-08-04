from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from fast_zero.core.database import get_session
from fast_zero.models.models import Module
from fast_zero.schemas.permissioes_schema import (
    ModuleListSchema,
    ModulePublic,
    ModuleSchema,
)
from fast_zero.schemas.schemas import Message

router = APIRouter(prefix='/permissoes', tags=['permissoes'])
T_Session = Annotated[Session, Depends(get_session)]


@router.get('/module', response_model=ModuleListSchema)
def read_module(session: T_Session, page: int = 1, page_size: int = 10):
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


@router.get('/module/find', response_model=ModuleListSchema)
def get_modules_by_partial_title(
    title: str, session: T_Session, page: int = 1, page_size: int = 10
):
    skip = (page - 1) * page_size
    limit = page_size
    partial_title = f"%{title}%"

    subquery = select(Module).where(
        Module.title.like(partial_title)).subquery()
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


@router.get('/module/{module_id}', response_model=ModulePublic)
def read_module_by_id(module_id: int, session: T_Session):
    db_module = session.get(Module, module_id)

    if db_module is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil not found',
        )

    return db_module


@router.post(
    '/module', status_code=HTTPStatus.CREATED, response_model=ModulePublic
)
def create_module(module: ModuleSchema, session: T_Session):
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


@router.put('/module/{module_id}', response_model=ModulePublic)
def update_module_by_id(
    module_id: int, module: ModulePublic, session: T_Session
):
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
def delete_module(module_id: int, session: T_Session):
    db_module = session.get(Module, module_id)

    if not db_module:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Module not found.'
        )

    session.delete(db_module)
    session.commit()

    return {'message': 'Module deletado'}
