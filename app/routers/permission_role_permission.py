from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.security import get_current_user, verify_user_with_roles_and_permissions
from app.models.models import RolePermissions, User
from app.schemas.permissioes_schema import (
    RolePermissionListSchema,
    RolePermissionsPublicSchema,
    RolePermissionsSchema,
)
from app.schemas.schemas import Message

router = APIRouter(prefix='/permissoes', tags=['role-permission'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/role-permission', response_model=RolePermissionListSchema)
def read_role_permission(
    session: T_Session,
    user_current: T_CurrentUser,
    page: int = 1,
    page_size: int = 10
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
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
    role_permission: RolePermissionsSchema,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
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
def delete_rele_permission_by_id(
    role_permission_id: int,
    session: T_Session,
    user_current: T_CurrentUser,
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
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
    role_id: int,
    permission_id: int,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
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
