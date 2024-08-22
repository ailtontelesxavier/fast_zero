from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class NegociacaoInSchema(BaseModel):
    processo: str
    executado: str
    contrato: str
    val_devido: Decimal
    val_desconto: Optional[Decimal] = Field(default=Decimal("0.00"))
    val_neg: Decimal
    data_pri_parc: Optional[date]
    data_ult_parc: Optional[date]
    val_entrada: Optional[Decimal] = Field(default=Decimal("0"))
    qtd_parc_ent: Optional[int] = Field(default=0)
    data_pri_parc_entr: Optional[date] = Field(default=None)
    data_ult_parc_entr: Optional[date] = Field(default=None)
    obs_val_neg: Optional[str] = None
    is_term_ex_jud: Optional[bool] = Field(default=False)
    is_hom_ext_jud: Optional[bool] = Field(default=False)
    qtd: int
    taxa_mes: Decimal
    val_parc: Decimal
    is_cal_parc_mensal: Optional[bool] = Field(default=False)
    is_cal_parc_entrada: Optional[bool] = Field(default=False)
    is_descumprido: Optional[bool] = Field(default=False)
    is_liquidado: Optional[bool] = Field(default=False)
    is_retorno_execucao: Optional[bool] = Field(default=False)


class NegociacaoUpdateSchema(BaseModel):
    processo: str | None = None
    executado: str | None = None
    contrato: str | None = None
    val_devido: Decimal | None = None
    val_desconto: Decimal | None = None
    val_neg: Decimal | None = None
    data_pri_parc: date | None = None
    data_ult_parc: date | None = None
    val_entrada: Decimal | None = None
    qtd_parc_ent: int | None = None
    data_pri_parc_entr: date | None = None
    data_ult_parc_entr: date | None = None
    obs_val_neg: str | None = None
    is_term_ex_jud: bool | None = None
    is_hom_ext_jud: bool | None = None
    qtd: int | None = None
    taxa_mes: Decimal | None = None
    val_parc: Decimal | None = None
    is_cal_parc_mensal: bool | None = None
    is_cal_parc_entrada: bool | None = None
    is_descumprido: bool | None = None
    is_liquidado: bool | None = None
    is_retorno_execucao: bool | None = None


class NegociacaoOutSchema(NegociacaoInSchema):
    id: int


class NegociacaoListSchema(BaseModel):
    rows: list[NegociacaoOutSchema]
    total_records: int


class ParcelamentoInSchema(BaseModel):
    negociacao_id: int 
    data: date
    val_parcela: Decimal
    val_pago: Decimal | None = None
    obs_val_pago: str | None = None
    data_pgto: date | None = None
    type: int
    numero_parcela: int
    is_pg: bool | None = False
    is_val_juros: bool


class ParcelamentoUpdateSchema(BaseModel):
    negociacao_id: int | None = None
    data: date | None = None
    val_parcela: Decimal | None = None
    val_pago: Decimal | None = None
    obs_val_pago: str | None = None
    data_pgto: date | None = None
    type: int | None = None
    numero_parcela: int | None = None
    is_pg: bool | None = False
    is_val_juros: bool | None = False


class ParcelamentoOurSchema(ParcelamentoInSchema):
    id: int


class ParcelamentoListSchema(BaseModel):
    rows: list[ParcelamentoOurSchema]
    total_records: int
