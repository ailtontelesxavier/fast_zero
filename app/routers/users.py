from datetime import datetime
from http import HTTPStatus
from typing import Annotated

import pytz
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.security import (
    get_current_active_user,
    get_password_hash,
    verify_password,
    verify_user_with_roles_and_permissions,
)
from app.core.util import get_data_now_for_time_zone
from app.models.models import User, UserRoles
from app.schemas.schemas import (
    ListUserFull,
    Message,
    UpdatePasswordRequest,
    UserFull,
    UserList,
    UserPasswordUpdate,
    UserPublic,
    UserQrCode,
    UserRolesIn,
    UserRolesList,
    UserRolesOut,
    UserSchema,
)

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_active_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: T_Session, user_current: T_CurrentUser):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )
    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already registered',
            )
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Username already registered',
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
        full_name=user.full_name,
        otp_base32=User.create_otp_base32(),
        otp_auth_url='',
        otp_created_at=None,
    )

    # configura otp
    # totp = pyotp.TOTP(db_user.otp_base32).now()
    db_user.otp_created_at = get_data_now_for_time_zone()

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/', response_model=UserList)
async def read_users(session: T_Session, user: T_CurrentUser, page: int = 1, page_size: int = 10):
    verify_user_with_roles_and_permissions(user, permissions=["is_superuser"])
    skip = (page - 1) * page_size
    limit = page_size

    total_records = session.scalar(select(func.count(User.id)))
    users = session.scalars(
        select(User).order_by(User.id).offset(skip).limit(limit)
    ).all()
    return {
        'users': users,
        'total_records': total_records,
        'page': page,
        'page_size': page_size,
    }


@router.get('/user/{username}', response_model=UserFull)
async def get_user_by_username(
    session: T_Session,
    user_current: T_CurrentUser,
    username: str = Path(..., title='nome de usuario'),
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    user = User.get_by_username(session, username)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    return user


@router.get('/user-like/{username}', response_model=ListUserFull)
async def get_user_like_by_username(
    session: T_Session,
    user: T_CurrentUser,
    username: str = Path(..., title='nome de usuario'),
    page: int = 1,
    page_size: int = 10,
):
    verify_user_with_roles_and_permissions(user, permissions=["is_superuser"])
    db_rows = User.get_like_by_username(session, username, page, page_size)

    return db_rows


@router.get('/{user_id}', response_model=UserQrCode)
async def get_user_by_id(
    session: T_Session,
    user: T_CurrentUser,
    user_id: int = Path(..., title='The ID of the user to retrieve'),
):
    verify_user_with_roles_and_permissions(user, permissions=["is_superuser"])
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    db_user.qr_code = db_user.get_otp_url()
    return db_user


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: User = Depends(get_current_active_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions'
        )

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@router.put('/update-password/', response_model=Message)
async def update_password(
    session: T_Session,
    current_user: T_CurrentUser,
    data: UpdatePasswordRequest,
):
    db_user = session.get(User, current_user.id)
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    if not verify_password(data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect password',
        )

    db_user.password = get_password_hash(data.new_password)
    session.commit()
    session.refresh(db_user)

    return {'message': 'Senha atualizada'}


@router.put('/update-password/{user_id}', response_model=UserPublic)
async def update_user_password(
    session: T_Session,
    user_current: T_CurrentUser,
    user_id: int,
    password: UserPasswordUpdate = Body(...),
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    db_user.password = get_password_hash(password.password)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/update/{user_id}', response_model=UserFull)
async def update_user_by_id(
    user_id: int,
    user_current: T_CurrentUser,
    user: UserPublic,
    session: T_Session,
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_user = session.scalar(select(User).where(User.id == user_id))

    if user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User ID diferentes'
        )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    db_user2 = session.scalar(
        select(User).where(
            ((User.email == user.email) | (User.username == user.username))
            & (User.id != user.id)
        )
    )
    if db_user2:
        if db_user2.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already registered',
            )
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Username already registered',
        )

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db_user.updated_at = func.now()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/update-otp/{user_id}', response_model=UserQrCode)
async def update_otp_user_by_id(
    user_id: int,
    user_current: T_CurrentUser,
    session: T_Session,
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    try:
        setattr(db_user, 'otp_base32', User.create_otp_base32())
        setattr(db_user, 'otp_created_at', get_data_now_for_time_zone())

        setattr(db_user, 'updated_at', func.now())
        setattr(db_user, 'otp_auth_url', db_user.get_otp_auth_url())
        setattr(db_user, 'qr_code', str(db_user.get_qr_code()))

        session.commit()
        session.refresh(db_user)
    except Exception as e:
        print(f'Erro ao update otp: {e}')
        raise

    return db_user


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    user_current: T_CurrentUser,
    session: T_Session,
    current_user: User = Depends(get_current_active_user),
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@router.get('/user-role/{user_id}', response_model=UserRolesList)
async def get_role_by_user_id(
    session: T_Session,
    user_current: T_CurrentUser,
    user_id: int = Path(..., ge=1, title='id do usuario'),
    page: int = 1,
    page_size: int = 10,
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    row = session.get(User, user_id)
    # user = session.query(User).filter_by(id=user_id).one_or_none()

    if row is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    # db_rows = user.roles.order_by(UserRoles.id.desc()).limit(10).all()
    db_rows = UserRoles.get_role_by_user_id(session, user_id, page, page_size)

    return db_rows


@router.post('/user-role', response_model=UserRolesOut)
async def create_role_user(
    session: T_Session,
    user_current: T_CurrentUser,
    role_user: UserRolesIn
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_role_user = session.scalar(
        select(UserRoles).where(
            (UserRoles.user_id == role_user.user_id)
            & (UserRoles.role_id == role_user.role_id)
        )
    )
    if db_role_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Role user already registered',
        )

    db_role_user = UserRoles(
        user_id=role_user.user_id,
        role_id=role_user.role_id,
    )

    session.add(db_role_user)
    session.commit()
    session.refresh(db_role_user)
    return db_role_user


@router.delete('/user-role/', response_model=Message)
async def delete_role_user_by_id(
    user_role_id: int,
    session: T_Session,
    user_current: T_CurrentUser
):
    verify_user_with_roles_and_permissions(user_current, permissions=["is_superuser"])
    db_row = session.get(UserRoles, user_role_id)

    if db_row is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User role not found.',
        )

    session.delete(db_row)
    session.commit()

    return {'message': 'User role deletado'}
