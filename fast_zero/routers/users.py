from http import HTTPStatus
from typing import Annotated

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
    UserSchema,
)

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
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
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/', response_model=UserList)
def read_users(session: T_Session, page: int = 1, page_size: int = 10):
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
def get_user_by_username(
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
def get_user_like_by_username(
    session: T_Session,
    username: str = Path(..., title='nome de usuario'),
    page: int = 1,
    page_size: int = 10,
):
    db_rows = User.get_like_by_username(session, username, page, page_size)

    return db_rows


@router.get('/{user_id}', response_model=UserFull)
def get_user_by_id(
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
def update_user(
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
def update_user_password(
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
def update_user_by_id(
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
def delete_user(
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


@router.get('/user-role/{username}', response_model=ListUserFull)
def get_role_by_user_id(
    session: T_Session,
    user_id: int = Path(..., title='id do usuario'),
    page: int = 1,
    page_size: int = 10,
):
    row = session.get(User, user_id)

    if row is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    db_rows = UserRoles.get_role_by_user_id(session, user_id, page, page_size)

    return db_rows
