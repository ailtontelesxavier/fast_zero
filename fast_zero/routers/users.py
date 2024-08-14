from datetime import datetime
from http import HTTPStatus
from typing import Annotated

import pytz
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session
from fast_zero.core.security import (
    get_current_user,
    get_password_hash,
)
from fast_zero.models.models import User, UserRoles
from fast_zero.schemas.schemas import (
    ListUserFull,
    Message,
    UserFull,
    UserList,
    UserPasswordUpdate,
    UserPublic,
    UserRolesIn,
    UserRolesList,
    UserRolesOut,
    UserSchema,
)

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: T_Session):
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
        otp_auth_url=''
    )

    # configura otp
    # totp = pyotp.TOTP(db_user.otp_base32).now()
    TIME_ZONE = 'America/Sao_Paulo'
    tz = pytz.timezone(TIME_ZONE)
    db_user.otp_created_at = datetime.now(tz)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/', response_model=UserList)
async def read_users(session: T_Session, page: int = 1, page_size: int = 10):
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
    username: str = Path(..., title='nome de usuario'),
):
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
    username: str = Path(..., title='nome de usuario'),
    page: int = 1,
    page_size: int = 10,
):
    db_rows = User.get_like_by_username(session, username, page, page_size)

    return db_rows


@router.get('/{user_id}', response_model=UserFull)
async def get_user_by_id(
    session: T_Session,
    user_id: int = Path(..., title='The ID of the user to retrieve'),
):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    return user


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: User = Depends(get_current_user),
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


@router.put('/update-password/{user_id}', response_model=UserPublic)
async def update_user_password(
    session: T_Session,
    user_id: int,
    password: UserPasswordUpdate = Body(...),
):
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
    user: UserPublic,
    session: T_Session,
):
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


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    session: T_Session,
    current_user: User = Depends(get_current_user),
):
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
    user_id: int = Path(..., ge=1, title='id do usuario'),
    page: int = 1,
    page_size: int = 10,
):
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
async def create_role_user(session: T_Session, role_user: UserRolesIn):
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
async def delete_role_user_by_id(user_role_id: int, session: T_Session):
    db_row = session.get(UserRoles, user_role_id)

    if db_row is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User role not found.',
        )

    session.delete(db_row)
    session.commit()

    return {'message': 'User role deletado'}
