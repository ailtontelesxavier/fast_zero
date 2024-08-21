from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class NegociacaoInSchema(BaseModel):
    processo: str
    executado: str
    contrato: str
    val_devido: Decimal
    val_desconto: Optional[Decimal]
    val_neg: Decimal
    data_pri_parc: Optional[date]
    data_ult_parc: Optional[date]
    val_entrada: Optional[Decimal]
    qtd_parc_ent: Optional[int]
    data_pri_parc_entr: Optional[date]
    data_ult_parc_entr: Optional[date]
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


class ParcelamentoInSchema(BaseModel):
    negociacao_id: int
    data: date | None
    val_parcela: Decimal
    val_pago: Decimal | None
    obs_val_pago: str
    data_pgto: date | None
    type: int
    numero_parcela: int
    is_pg: bool
    is_val_juros: bool


class ParcelamentoOurSchema(ParcelamentoInSchema):
    id: int


class ParcelamentoListSchema(BaseModel):
    rows: list[ParcelamentoOurSchema]
    total_records: int
