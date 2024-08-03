from pydantic import BaseModel


class ModuleSchema(BaseModel):
    title: str


class ModulePublic(BaseModel):
    id: int
    title: str


class ModuleListSchema(BaseModel):
    modules: list[ModuleSchema]
    total_records: int


class RoleSchema(BaseModel):
    name: str


class RolePublic(BaseModel):
    id: int
    name: str


class RoleListSchema(BaseModel):
    roles: list[RolePublic]
    total_records: int
