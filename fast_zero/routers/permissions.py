from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session
from fast_zero.models.models import Role
from fast_zero.schemas.permissioes_schema import RoleListSchema, RolePublic, RoleSchema

router = APIRouter(prefix='/permissoes', tags=['permissoes'])
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


@router.post(
    '/role', status_code=HTTPStatus.CREATED, response_model=RolePublic
)
def create_role(role: RoleSchema, session: T_Session):
    db_role = session.scalar(
        select(Role).where(Role.name == role.name)
    )

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
