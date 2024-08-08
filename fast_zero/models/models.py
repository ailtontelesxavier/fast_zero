from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint, func, select
from sqlalchemy.orm import (
    Mapped,
    Session,
    mapped_column,
    registry,
    relationship,
    validates,
)

table_registry = registry()


class Base:
    @classmethod
    def get_by_id(cls, session: Session, id: BigInteger):
        return session.get(cls, cls.id)

    @classmethod
    def delete(cls, session: Session):
        row = session.get(cls, cls.id)
        session.delete(row)
        session.commit()
        return {'message': f'<{row}> deleted'}


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


# Associação muitos-para-muitos entre Roles e Permissões
@table_registry.mapped_as_dataclass
class RolePermissions(Base):
    __tablename__ = 'role_permissions'
    __table_args__ = (
        UniqueConstraint(
            'role_id', 'permission_id', name='uix_role_id_permission_id'
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, init=False, primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    permission_id: Mapped[int] = mapped_column(ForeignKey('permissions.id'))


# Associação muitos-para-muitos entre Usuários e Roles
@table_registry.mapped_as_dataclass
class UserRoles(Base):
    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(BigInteger, init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))

    @classmethod
    def get_role_by_user_id(
        cls,
        session: Session,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
    ):
        skip = (page - 1) * page_size
        limit = page_size

        subquery = select(cls).where(cls.user_id == user_id).subquery()

        total_records = session.scalar(
            select(func.count()).select_from(subquery)
        )

        rows = (
            session.query(subquery)
            .order_by(cls.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return {
            'rows': rows,
            'total_records': total_records,
        }


@table_registry.mapped_as_dataclass
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
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

    roles = relationship('UserRoles', backref='User', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username} - {self.email} >'

    @validates('username')
    def validate_username(self, key, value):  # noqa: PLR6301
        if value is None or not value:
            raise ValueError('Username não pode ser vazio')
        return value

    @classmethod
    def get_by_username(cls, session: Session, username: str):
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def get_like_by_username(
        cls,
        session: Session,
        username: str,
        page: int = 1,
        page_size: int = 10,
    ):
        skip = (page - 1) * page_size
        limit = page_size
        partial_name = f'%{username}%'

        subquery = (
            select(cls).where(cls.username.like(partial_name)).subquery()
        )

        total_records = session.scalar(
            select(func.count()).select_from(subquery)
        )

        rows = (
            session.query(cls)
            .filter(cls.username.like(partial_name))
            .order_by(cls.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return {
            'rows': rows,
            'total_records': total_records,
        }


@table_registry.mapped_as_dataclass
class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(BigInteger, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    permissions: Mapped[list['Permission']] = relationship(
        'Permission',
        secondary='role_permissions',
        back_populates='roles',
        order_by=('Permission.module_id'),
    )

    def __repr__(self):
        return f'<Role {self.name}>'


@table_registry.mapped_as_dataclass
class Permission(Base):
    __tablename__ = 'permissions'
    __table_args__ = (
        UniqueConstraint('name', 'module_id', name='uix_name_modules'),
    )

    id: Mapped[int] = mapped_column(BigInteger, init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    module_id: Mapped[int] = mapped_column(ForeignKey('module.id'))

    module: Mapped['Module'] = relationship(
        'Module', back_populates='permissions', order_by=('Module.title')
    )
    roles: Mapped[list[Role]] = relationship(
        'Role',
        secondary='role_permissions',
        back_populates='permissions',
        order_by=('Permission.name'),
    )

    def __repr__(self):
        return f'<Permission {self.name}>'

    @classmethod
    def get_by_module_and_name(
        cls, session: Session, module_id: int, name: str
    ):
        return (
            session.query(cls)
            .filter_by(module_id=module_id, name=name)
            .first()
        )


@table_registry.mapped_as_dataclass
class Module(Base):
    __tablename__ = 'module'

    id: Mapped[int] = mapped_column(BigInteger, init=False, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    permissions: Mapped[list['Permission']] = relationship(
        'Permission', back_populates='module'
    )

    def __repr__(self):
        return f'<Module {self.title}>'


@table_registry.mapped_as_dataclass
class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(BigInteger, init=False, primary_key=True)
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
