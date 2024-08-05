from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, func, select
from sqlalchemy.orm import Session, joinedload

from fast_zero.core.database import get_session
from fast_zero.models.models import Permission, Role
from fast_zero.schemas.permissioes_schema import (
    RoleFull,
    RoleList,
    RoleListSchema,
    RolePublic,
    RoleSchema,
)
from fast_zero.schemas.schemas import Message

router = APIRouter(prefix='/permissoes', tags=['role'])
T_Session = Annotated[Session, Depends(get_session)]


@router.get('/role', response_model=RoleListSchema)
def read_role(session: T_Session, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    limit = page_size

    total_records = session.scalar(select(func.count(Role.id)))
    roles = session.scalars(
        select(Role).order_by(Role.id).offset(skip).limit(limit)
    ).all()

    return {
        'roles': roles,
        'total_records': total_records,
    }


@router.get('/role/{role_id}', response_model=RolePublic)
def read_role_by_id(role_id: int, session: T_Session):
    db_role = session.get(Role, role_id)

    if db_role is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil not found',
        )

    return db_role


@router.get('/role/full/{role_id}', response_model=RoleFull)
def read_role_full_by_id(role_id: int, session: T_Session):
    db_role = session.get(Role, role_id)

    if db_role is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil not found',
        )

    return db_role


@router.get('/role/find/', response_model=RoleList)
def get_roles_by_partial_name(
    name: str, session: T_Session, page: int = 1, page_size: int = 10
):
    skip = (page - 1) * page_size
    limit = page_size
    partial_name = f'%{name}%'

    subquery = select(Role).where(Role.name.like(partial_name)).subquery()
    total_records = session.scalar(select(func.count()).select_from(subquery))
    roles = session.scalars(
        select(Role)
        .where(Role.name.like(partial_name))
        .order_by(Role.id)
        .offset(skip)
        .limit(limit)
    ).all()

    return {
        'roles': roles,
        'total_records': total_records,
    }


@router.post(
    '/role', status_code=HTTPStatus.CREATED, response_model=RolePublic
)
def create_role(role: RoleSchema, session: T_Session):
    db_role = session.scalar(select(Role).where(Role.name == role.name))

    if db_role:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Modulo ja cadastrado'
        )

    db_role = Role(
        name=role.name,
        permissions=[],
    )

    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role


@router.put('/role/{role_id}', response_model=RolePublic)
def update_role_by_id(role_id: int, role: RolePublic, session: T_Session):
    db_role = session.get(Role, role_id)

    if db_role is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Perfil not found'
        )

    if role.id != role_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Perfil ID diferentes'
        )

    db_role2 = session.scalar(
        select(Role).where((Role.name == role.name) & (Role.id != role.id))
    )

    if db_role2:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Nome de Perfil ja cadastrado',
        )

    for key, value in role.model_dump(exclude_unset=True).items():
        setattr(db_role, key, value)

    session.add(db_role)
    session.commit()
    session.refresh(db_role)

    return db_role


@router.delete('/role/{role_id}', response_model=Message)
def delete_role(role_id: int, session: T_Session):
    db_role = session.get(Role, role_id)

    if not db_role:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Perfil not found.'
        )

    session.delete(db_role)
    session.commit()

    return {'message': 'Perfil deletado'}
