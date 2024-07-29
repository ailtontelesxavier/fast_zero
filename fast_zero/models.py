from datetime import datetime
from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


# Associação muitos-para-muitos entre Roles e Permissões
@table_registry.mapped_as_dataclass
class role_permissions:
    __tablename__ = 'role_permissions'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    permission_id: Mapped[int] = mapped_column(ForeignKey('permissions.id'))


# Associação muitos-para-muitos entre Usuários e Roles
@table_registry.mapped_as_dataclass
class user_roles:
    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    todos: Mapped[list['Todo']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Role:
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    permissions: Mapped[list['Permission']] = relationship(
            'Permission', secondary='role_permissions', back_populates='roles'
        )
    users: Mapped[list['User']] = relationship(
        'User', secondary='user_roles'
    )


@table_registry.mapped_as_dataclass
class Permission:
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    roles: Mapped[list[Role]] = relationship(
        'Role', secondary='role_permissions', back_populates='permissions'
    )



@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(init=False, back_populates='todos')
