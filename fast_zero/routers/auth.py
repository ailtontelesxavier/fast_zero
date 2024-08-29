from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session
from fast_zero.core.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
from fast_zero.models.models import Permission, Role, User, UserRoles
from fast_zero.schemas.permissioes_schema import (
    ModuleListSchema,
)
from fast_zero.schemas.schemas import Message, Token

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        )

    if not user.is_valid_otp(form_data.client_secret):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username, password or secret',
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': user.username})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}


@router.get('/verify-token', status_code=HTTPStatus.OK, response_model=Message)
async def verify_user_token(
    session: T_Session,
    user: T_CurrentUser,
):
    # return verify_token(token=token)
    return {'message': 'Ola Mundo!'}


@router.get('/modules', response_model=ModuleListSchema)
async def get_user_modules(current_user: T_CurrentUser, session: T_Session):
    # Obtém as roles do usuário atual
    user_roles = session.scalars(
        select(UserRoles).where(UserRoles.user_id == current_user.id)
    ).all()

    # Coleta os IDs das roles
    role_ids = [user_role.role_id for user_role in user_roles]

    if not role_ids:
        raise HTTPException(
            status_code=404, detail='No roles found for this user.'
        )

    # Obtém as permissões associadas às roles
    permissions = session.scalars(
        select(Permission).join(Role.permissions).where(Role.id.in_(role_ids))
    ).all()

    if not permissions:
        raise HTTPException(
            status_code=404,
            detail="No permissions found for the user's roles.",
        )

    # Coleta os módulos associados às permissões
    modules = [permission.module for permission in permissions]

    return {'modules': modules, 'total_records': len(modules)}
