from pydantic import BaseModel


class ModuleSchema(BaseModel):
    title: str


class ModulePublic(BaseModel):
    id: int
    title: str


class ModuleListSchema(BaseModel):
    modules: list[ModulePublic]
    total_records: int


class RoleSchema(BaseModel):
    name: str


class RolePublic(BaseModel):
    id: int
    name: str


class RoleFull(BaseModel):
    id: int
    name: str
    permissions: list['PermissionPublic']


class RoleListSchema(BaseModel):
    roles: list[RolePublic]
    total_records: int


class RoleList(BaseModel):
    roles: list[RoleFull]
    total_records: int


class PermissionSchema(BaseModel):
    name: str
    description: str
    module_id: int


class PermissionUpdateSchema(BaseModel):
    id: int
    name: str
    description: str
    module_id: int


class PermissionPublic(PermissionSchema):
    id: int
    module: ModulePublic


class PermissionListSchema(BaseModel):
    permissions: list[PermissionPublic]
    total_records: int


class RolePermissionsSchema(BaseModel):
    role_id: int
    permission_id: int


class RolePermissionsPublicSchema(RolePermissionsSchema):
    id: int


class RolePermissionListSchema(BaseModel):
    role_permissions: list[RolePermissionsPublicSchema]
    total_records: int
