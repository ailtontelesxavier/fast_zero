from pydantic import BaseModel

from fast_zero.models.models import Module


class ModuleFullSchema(BaseModel):
    module: Module


class ModuleSchema(BaseModel):
    id: int | None
    title: str


class RoleSchema(BaseModel):
    name: str


class RolePublic(BaseModel):
    id: int
    name: str
