from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.juridico import (
    router_negociacao,
)
from app.routers import (
    auth,
    permission_role_permission,
    permissions_module,
    permissions_permission,
    permissions_role,
    todos,
    users,
)
from app.schemas.schemas import Message

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
    'http://127.0.0.1:8002',
    'http://localhost:8002',
    "http://172.16.238.9:3000",
    "http://172.16.238.9:8002",
    'http://172.16.238.11:8002',
    'http://172.16.238.11:3000',
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
app.include_router(router_negociacao.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola Mundo!'}
