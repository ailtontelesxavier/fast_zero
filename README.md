sudo snap refresh node --channel=22

# gera SECRET_KEY no terminal
python
import secrets
secrets.token_hex(256)

# fazer migrate
docker exec -it b8d4ddba3a4a sh -c "poetry run alembic upgrade head"

# subir somento o banco para teste
docker-compose up -d fastzero_database


# controle de rotas
Para controlar rotas por permissão e roles em um projeto FastAPI utilizando SQLAlchemy 2, você pode seguir esses passos gerais:

Criação do Modelo de Usuário e Roles:
Defina um modelo para usuários e roles no seu banco de dados.

Autenticação e Autorização:
Implemente uma maneira de autenticar usuários (por exemplo, utilizando OAuth2 com password flow) e atribua roles aos usuários.

Dependências Personalizadas:
Crie dependências personalizadas para verificar permissões e roles.

Aplicação das Dependências nas Rotas:
Utilize essas dependências nas rotas que necessitam de controle de acesso.

1. Criação do Modelo de Usuário e Roles
Defina seus modelos com SQLAlchemy:

python
Copy code
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Associação muitos-para-muitos entre Usuários e Roles
user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    roles = relationship('Role', secondary=user_roles, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    users = relationship('User', secondary=user_roles, back_populates='roles')
2. Autenticação e Autorização
Utilize o OAuth2 para autenticação. Aqui está um exemplo simples de autenticação com o FastAPI:

python
Copy code
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)  # Implementar esta função
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
3. Dependências Personalizadas
Crie uma dependência personalizada para verificar permissões e roles:

python
Copy code
from fastapi import Depends
from jose import JWTError, jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)  # Implementar esta função
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_user_with_roles(roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if not any(role.name in roles for role in current_user.roles):
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions",
            )
        return current_user
    return role_checker
4. Aplicação das Dependências nas Rotas
Use as dependências nas rotas que requerem controle de acesso:

python
Copy code
@app.get("/items/", response_model=List[Item])
def read_items(current_user: User = Depends(get_current_user_with_roles(["admin", "user"]))):
    return [{"item_id": "Foo", "owner": current_user.username}]
Este é um exemplo básico, mas cobre a estrutura principal necessária para controlar rotas por permissão e roles em um projeto FastAPI utilizando SQLAlchemy 2. Certifique-se de ajustar conforme necessário para atender aos requisitos específicos do seu projeto.





utilizando tambem permission
ChatGPT
Para adicionar um sistema de permissões ao seu projeto FastAPI usando SQLAlchemy, você pode seguir um fluxo semelhante ao descrito anteriormente, mas estendendo o modelo para incluir permissões e integrando-as no controle de acesso. Abaixo está um guia passo a passo sobre como você pode implementar isso.

1. Criação do Modelo de Usuário, Roles e Permissões
Defina seus modelos incluindo permissões:

python
Copy code
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Associação muitos-para-muitos entre Roles e Permissões
role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

# Associação muitos-para-muitos entre Usuários e Roles
user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    roles = relationship('Role', secondary=user_roles, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')
    users = relationship('User', secondary=user_roles, back_populates='roles')

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')
2. Autenticação e Autorização
Como antes, utilize o OAuth2 para autenticação.

3. Dependências Personalizadas com Permissões
Crie dependências para verificar permissões específicas:

python
Copy code
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)  # Implementar esta função
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_user_with_roles_and_permissions(roles: list[str] = [], permissions: list[str] = []):
    def role_permission_checker(current_user: User = Depends(get_current_active_user)):
        if roles and not any(role.name in roles for role in current_user.roles):
            raise HTTPException(
                status_code=403,
                detail="Not enough role permissions",
            )
        if permissions:
            user_permissions = {perm.name for role in current_user.roles for perm in role.permissions}
            if not all(perm in user_permissions for perm in permissions):
                raise HTTPException(
                    status_code=403,
                    detail="Not enough permissions",
                )
        return current_user
    return role_permission_checker
4. Aplicação das Dependências nas Rotas
Utilize as dependências nas rotas que requerem controle de acesso baseado em roles e permissões:

python
Copy code
@app.get("/items/", response_model=List[Item])
def read_items(current_user: User = Depends(get_current_user_with_roles_and_permissions(roles=["admin"], permissions=["read_items"]))):
    return [{"item_id": "Foo", "owner": current_user.username}]
Função de Utilidade para Obter Usuário
Implemente a função get_user_by_username:

python
Copy code
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
Exemplos de Uso
Para rotas que requerem apenas roles específicas:

python
Copy code
@app.get("/admin/", response_model=List[AdminItem])
def read_admin_items(current_user: User = Depends(get_current_user_with_roles_and_permissions(roles=["admin"]))):
    return [{"admin_item_id": "Bar", "owner": current_user.username}]
Para rotas que requerem permissões específicas:

python
Copy code
@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate, current_user: User = Depends(get_current_user_with_roles_and_permissions(permissions=["create_items"]))):
    return {"item_id": "New", "owner": current_user.username}
Conclusão
Com essas implementações, você pode controlar de maneira eficiente o acesso às rotas em seu projeto FastAPI usando roles e permissões integradas ao SQLAlchemy. Certifique-se de adaptar e expandir esses exemplos para atender aos requisitos específicos do seu projeto.