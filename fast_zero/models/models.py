from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import (
    Mapped,
    Session,
    mapped_column,
    registry,
    relationship,
    validates,
)

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


# Associação muitos-para-muitos entre Roles e Permissões
@table_registry.mapped_as_dataclass
class RolePermissions:
    __tablename__ = 'role_permissions'
    __table_args__ = (
        UniqueConstraint('role_id', 'permission_id', name='uix_role_id_permission_id'),
    )

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

    @validates('username')
    def validate_username(self, key, value):  # noqa: PLR6301
        if value is None or not value:
            raise ValueError('Username não pode ser vazio')
        return value


@table_registry.mapped_as_dataclass
class Role:
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    permissions: Mapped[list['Permission']] = relationship(
        'Permission', secondary='role_permissions', back_populates='roles',
        order_by=('Permission.module_id')
    )


@table_registry.mapped_as_dataclass
class Permission:
    __tablename__ = 'permissions'
    __table_args__ = (
        UniqueConstraint('name', 'module_id', name='uix_name_modules'),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    module_id: Mapped[int] = mapped_column(ForeignKey('module.id'))

    module: Mapped['Module'] = relationship(
        'Module', back_populates='permissions',
        order_by=('Module.title')
    )
    roles: Mapped[list[Role]] = relationship(
        'Role', secondary='role_permissions', back_populates='permissions',
        order_by=('Permission.name')
    )

    @classmethod
    def get_by_module_and_name(
        cls, session: Session, module_id: int, name: str
    ):
        return session.query(cls).filter_by(
            module_id=module_id, name=name).first()


@table_registry.mapped_as_dataclass
class Module:
    __tablename__ = 'module'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    permissions: Mapped[list['Permission']] = relationship(
        'Permission', back_populates='module'
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
