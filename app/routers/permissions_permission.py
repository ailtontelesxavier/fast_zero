from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.security import get_current_user, verify_user_with_roles_and_permissions
from app.models.models import Module, Permission, User
from app.schemas.permissioes_schema import (
    ModuleOutSchema,
    PermissionListSchema,
    PermissionPublic,
    PermissionSchema,
    PermissionUpdateSchema,
)
from app.schemas.schemas import Message

router = APIRouter(prefix='/permissoes', tags=['permission'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/permission', response_model=PermissionListSchema)
def read_permission(
    session: T_Session,
    user_current: T_CurrentUser,
    module: int = 0,
    page: int = 1,
    page_size: int = 10
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    skip = (page - 1) * page_size
    limit = page_size

    if module:
        subquery = (
            select(Permission).where(Permission.module_id == module).subquery()
        )
        total_records = session.scalar(
            select(func.count()).select_from(subquery)
        )
        permissions = session.scalars(
            select(Permission)
            .where(Permission.module_id == module)
            .order_by(Permission.id)
            .offset(skip)
            .limit(limit)
        ).all()

        return {
            'permissions': permissions,
            'total_records': total_records,
        }

    total_records = session.scalar(select(func.count(Permission.id)))
    permissions = session.scalars(
        select(Permission).order_by(Permission.id).offset(skip).limit(limit)
    ).all()

    return {
        'permissions': permissions,
        'total_records': total_records,
    }


@router.get('/permission/search/', response_model=PermissionListSchema)
def read_permissions_by_name_or_module(
    session: T_Session,
    user_current: T_CurrentUser,
    title: str,
    page: int = 1,
    page_size: int = 10
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    skip = (page - 1) * page_size
    limit = page_size

    partial_name = f'%{title}%'

    # Junção entre Permission e Module
    query = (
        select(Permission, Module)
        .join(Module, Permission.module_id == Module.id)
        .where(
            (Permission.name.like(partial_name))
            | (Module.title.like(partial_name))
        )
    )

    subquery = query.subquery()
    total_records = session.scalar(select(func.count()).select_from(subquery))

    permissions = session.execute(
        query.order_by(Permission.id).offset(skip).limit(limit)
    ).all()

    permissions_list = [
        PermissionPublic(
            id=perm.Permission.id,
            name=perm.Permission.name,
            description=perm.Permission.description,
            module_id=perm.Permission.module_id,
            module=ModuleOutSchema(id=perm.Module.id, title=perm.Module.title),
        )
        for perm in permissions
    ]

    return {
        'permissions': permissions_list,
        'total_records': total_records,
    }


@router.get('/permission/{permission_id}', response_model=PermissionPublic)
def read_permission_by_id(
    permission_id: int,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_permission = session.get(Permission, permission_id)

    if db_permission is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Permission not found',
        )

    return db_permission


@router.post(
    '/permission',
    status_code=HTTPStatus.CREATED,
    response_model=PermissionPublic,
)
def create_permission(
    permission: PermissionSchema,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_permission = session.scalar(
        select(Permission).where(
            (Permission.name == permission.name)
            & (Permission.module_id == permission.module_id)
        )
    )

    db_module = session.get(Module, permission.module_id)

    if not db_module:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Modulo nao cadastrado'
        )

    if db_permission:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Permission ja cadastrado'
        )

    db_permission = Permission(
        name=permission.name,
        description=permission.description,
        module_id=permission.module_id,
        module=db_module,
        roles=[],
    )

    session.add(db_permission)
    session.commit()
    session.refresh(db_permission)
    return db_permission


@router.put('/permission/{permission_id}', response_model=PermissionPublic)
def update_permission_by_id(
    permission_id: int,
    permission: PermissionUpdateSchema,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_permission = session.get(Permission, permission_id)

    if db_permission is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Permission not found'
        )

    if permission.id != permission_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Permission ID diferentes',
        )

    for key, value in permission.model_dump(exclude_unset=True).items():
        setattr(db_permission, key, value)

    session.add(db_permission)
    session.commit()
    session.refresh(db_permission)

    return db_permission


@router.delete('/permission/{permission_id}', response_model=Message)
def delete_module(
    permission_id: int,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_permission = session.get(Permission, permission_id)

    if not db_permission:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Permission not found.'
        )

    session.delete(db_permission)
    session.commit()

    return {'message': 'Permission deletado'}
