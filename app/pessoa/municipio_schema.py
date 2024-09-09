
from pydantic import BaseModel

class UFIn(BaseModel):
    sigla: str
    nome: str


class UfOut(UFIn):
    id: int


class UfList(BaseModel):
    rows: list[UfOut]


class RegiaoIn(BaseModel):
    nome: str
    sigla: str


class RegiaoOut(RegiaoIn):
    id: int


class RegiaoList(BaseModel):
    rows: list[RegiaoOut]
    total_records: int


class MunicipioIn(BaseModel):
    nome: str
    uf_id: int


class MunicipioOut(MunicipioIn):
    id: int


class MunicipioList(BaseModel):
    rows: list[MunicipioOut]
    total_records: int
