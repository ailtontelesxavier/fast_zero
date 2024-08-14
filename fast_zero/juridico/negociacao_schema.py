from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class NegociacaoInSchema(BaseModel):
    processo: str
    executado: str
    contrato: str
    val_devido: Decimal
    val_desconto: Decimal | None
    val_neg: Decimal
    data_pri_parc: date | None
    data_ult_parc: date | None
    val_entrada: Decimal | None
    qtd_parc_ent: int | None
    data_pri_parc_entr: date | None
    data_ult_parc_entr: date | None
    obs_val_neg: str
    is_term_ex_jud: bool
    is_hom_ext_jud: bool
    qtd: int
    taxa_mes: Decimal
    val_parc: Decimal
    is_cal_parc_mensal: bool
    is_cal_parc_entrada: bool
    is_descumprido: bool
    is_liquidado: bool
    is_retorno_execucao: bool


class NegociacaoOutSchema(NegociacaoInSchema):
    id: int


class NegociacaoListSchema(BaseModel):
    rows: list[NegociacaoOutSchema]
    total_records: int
