from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from fast_zero.core.database import get_session
from fast_zero.models.models import Module
from fast_zero.routers import (
    auth,
    permission_role_permission,
    permissions_module,
    permissions_permission,
    permissions_role,
    todos,
    users,
)
from fast_zero.schemas.permissioes_schema import ModuleInShema
from fast_zero.schemas.schemas import Message

resource = {}


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print('init lifespan')
    resource['msg'] = "Hello, it's beautiful day!!"
    yield
    resource.clear()
    print('clean up lifespan')


app = FastAPI(lifespan=app_lifespan)

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(users.router)
app.include_router(permissions_role.router)
app.include_router(permissions_module.router)
app.include_router(permissions_permission.router)
app.include_router(permission_role_permission.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola Mundo!'}

