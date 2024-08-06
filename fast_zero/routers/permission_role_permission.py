from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session
from fast_zero.models.models import RolePermissions
from fast_zero.schemas.permissioes_schema import (
    RolePermissionListSchema,
    RolePermissionsPublicSchema,
    RolePermissionsSchema,
)
from fast_zero.schemas.schemas import Message

router = APIRouter(prefix='/permissoes', tags=['role-permission'])
T_Session = Annotated[Session, Depends(get_session)]


@router.get('/role-permission', response_model=RolePermissionListSchema)
def read_role_permission(
    session: T_Session, page: int = 1, page_size: int = 10
):
    skip = (page - 1) * page_size
    limit = page_size

    total_records = session.scalar(select(func.count(RolePermissions.id)))
    rows = session.scalars(
        select(RolePermissions)
        .order_by(RolePermissions.id)
        .offset(skip)
        .limit(limit)
    ).all()

    return {'role_permissions': rows, 'total_records': total_records}


@router.post(
    '/role-permission',
    status_code=HTTPStatus.CREATED,
    response_model=RolePermissionsPublicSchema,
)
def create_role_permission(
    role_permission: RolePermissionsSchema, session: T_Session
):
    db_row = session.scalar(
        select(RolePermissions).where(
            (RolePermissions.role_id == role_permission.role_id)
            & (RolePermissions.permission_id == role_permission.permission_id)
        )
    )

    if db_row:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Pefil permission ja cadastrado',
        )

    db_row = RolePermissions(
        role_id=role_permission.role_id,
        permission_id=role_permission.permission_id,
    )

    session.add(db_row)
    session.commit()
    session.refresh(db_row)
    return db_row


@router.delete('/role-permission/{role_permission_id}', response_model=Message)
def delete_rele_permission_by_id(role_permission_id: int, session: T_Session):
    db_row = session.get(RolePermissions, role_permission_id)

    if not db_row:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Role Permission not found.',
        )

    session.delete(db_row)
    session.commit()

    return {'message': 'Role Permission deletado'}


@router.delete('/role-permission/role_by_permission/', response_model=Message)
def delete_rele_permission_by_role_permission(
    role_id: int, permission_id: int, session: T_Session
):
    db_row = session.scalar(
        select(RolePermissions).where(
            (RolePermissions.role_id == role_id)
            & (RolePermissions.permission_id == permission_id)
        )
    )

    if not db_row:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Role Permission not found.',
        )

    session.delete(db_row)
    session.commit()

    return {'message': 'Role Permission deletado'}
