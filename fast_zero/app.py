from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fast_zero.routers import (
    auth,
    permissions,
    permissions_module,
    todos,
    users,
)
from fast_zero.schemas.schemas import Message

app = FastAPI()

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
app.include_router(permissions.router)
app.include_router(permissions_module.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola Mundo!'}
