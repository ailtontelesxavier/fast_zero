from decimal import Decimal
from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session
from fast_zero.core.security import get_current_user
from fast_zero.juridico.models import NegociacaoCredito, ParcelamentoNegociacao
from fast_zero.juridico.negociacao_schema import (
    NegociacaoInSchema,
    NegociacaoListSchema,
    NegociacaoOutSchema,
    NegociacaoUpdateSchema,
    ParcelamentoListSchema,
    ParcelamentoOurSchema,
)
from fast_zero.models.models import User
from fast_zero.schemas.schemas import Message

router = APIRouter(prefix='/juridico', tags=['negociação'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/negociacao', response_model=NegociacaoListSchema)
def read_negociacao(
    session: T_Session,
    user: T_CurrentUser,
    searchTerm: Optional[str] = '',
    page: int = 1,
    page_size: int = 10,
):
    skip = (page - 1) * page_size
    limit = page_size

    # Construir a consulta base
    query = select(NegociacaoCredito)

    if searchTerm:
        partial_name = f'%{searchTerm}%'
        query = query.where(
            NegociacaoCredito.processo.ilike(partial_name)
            | NegociacaoCredito.executado.ilike(partial_name)
            | NegociacaoCredito.contrato.ilike(partial_name)
        )

    # Obter o total de registros
    total_records = session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    # Obter os registros paginados
    rows = session.scalars(
        query.order_by(desc(NegociacaoCredito.id)).offset(skip).limit(limit)
    ).all()

    return {'rows': rows, 'total_records': total_records}


@router.get('/negociacao/{negociacao_id}', response_model=NegociacaoOutSchema)
def get_negociacao_by_id(
    session: T_Session, user: T_CurrentUser, negociacao_id: int
):
    row = session.get(NegociacaoCredito, negociacao_id)

    if row is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Negociação not found',
        )

    return row


@router.post(
    '/negociacao',
    status_code=HTTPStatus.CREATED,
    response_model=NegociacaoOutSchema,
)
def create_negociacao(
    negociacao: NegociacaoInSchema,
    session: T_Session,
    user: T_CurrentUser
):
    db_negociacao = session.scalar(
        select(NegociacaoCredito).where(
            (NegociacaoCredito.executado == negociacao.executado)
            & (NegociacaoCredito.processo == negociacao.processo)
            & (NegociacaoCredito.contrato == negociacao.contrato)
        )
    )

    if db_negociacao:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Negociacao Credito ja cadastrado',
        )

    db_negociacao = NegociacaoCredito(
        processo=negociacao.processo,
        executado=negociacao.executado,
        contrato=negociacao.contrato,
        val_devido=(
            negociacao.val_devido
            if negociacao.val_devido is not None
            else Decimal(0)
        ),
        val_desconto=(
            negociacao.val_desconto
            if negociacao.val_desconto is not None
            else Decimal(0)
        ),
        val_neg=negociacao.val_neg,
        data_pri_parc=(negociacao.data_pri_parc),  # type: ignore
        data_ult_parc=negociacao.data_ult_parc,  # type: ignore
        val_entrada=negociacao.val_entrada,  # type: ignore
        qtd_parc_ent=negociacao.qtd_parc_ent,  # type: ignore
        data_pri_parc_entr=negociacao.data_pri_parc_entr,  # type: ignore
        data_ult_parc_entr=negociacao.data_ult_parc_entr,  # type: ignore
        obs_val_neg=negociacao.obs_val_neg,
        is_term_ex_jud=negociacao.is_term_ex_jud,
        is_hom_ext_jud=negociacao.is_hom_ext_jud,
        qtd=negociacao.qtd,
        taxa_mes=negociacao.taxa_mes,
        val_parc=negociacao.val_parc,
        is_cal_parc_mensal=True,
        is_cal_parc_entrada=True,
        is_descumprido=negociacao.is_descumprido,
        is_liquidado=negociacao.is_liquidado,
        is_retorno_execucao=negociacao.is_retorno_execucao,
    )

    session.add(db_negociacao)
    session.commit()
    session.refresh(db_negociacao)
    return db_negociacao


@router.patch(
    '/negociacao/{negociacao_id}',
    response_model=NegociacaoOutSchema)
def update_negociacao_by_id(
    negociacao_id: int,
    negociacao: NegociacaoUpdateSchema,
    session: T_Session,
    user: T_CurrentUser
):
    db_row = session.get(NegociacaoCredito, negociacao_id)
    if not db_row:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Negociação not found.'
        )
    for key, value in negociacao.model_dump(exclude_unset=True).items():
        setattr(db_row, key, value)
        
    session.add(db_row)
    session.commit()
    session.refresh(db_row)
    return db_row


@router.delete('/negociacao/{negociacao_id}', response_model=Message)
def delete_negociacao(
    negociacao_id: int,
    session: T_Session,
    user: T_CurrentUser
):
    db_row = session.get(NegociacaoCredito, negociacao_id)

    if not db_row:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Negociação not found.'
        )

    session.delete(db_row)
    session.commit()

    return {'message': 'Negociação deletado'}


@router.get('/parcelamento', response_model=ParcelamentoListSchema)
def read_parcelmanto_by_negociacao_id(  # noqa: PLR0913, PLR0917
    session: T_Session,
    user: T_CurrentUser,
    negociacao_id: int,
    type: int,
    page: int = 1,
    page_size: int = 10,
):
    skip = (page - 1) * page_size
    limit = page_size

    query = select(ParcelamentoNegociacao).where(
        (ParcelamentoNegociacao.negociacao_id == negociacao_id)
        & (ParcelamentoNegociacao.type == type)
    )
    total_records = session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    rows = session.scalars(
        query.order_by(asc(ParcelamentoNegociacao.numero_parcela))
        .offset(skip)
        .limit(limit)
    ).all()

    return {'rows': rows, 'total_records': total_records}


@router.get(
    '/parcelamento/{parcelamento_id}', response_model=ParcelamentoOurSchema
)
def get_parcelamento_by_id(
    session: T_Session, user: T_CurrentUser, parcelamento_id: int
):
    row = session.get(ParcelamentoNegociacao, parcelamento_id)

    if row is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Parcelamento not Found'
        )

    return row
