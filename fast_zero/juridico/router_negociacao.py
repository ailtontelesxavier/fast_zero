from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, asc, func, select
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session
from fast_zero.core.security import get_current_user
from fast_zero.juridico.models import NegociacaoCredito, ParcelamentoNegociacao
from fast_zero.juridico.negociacao_schema import (
    NegociacaoListSchema,
    NegociacaoOutSchema,
    ParcelamentoListSchema,
    ParcelamentoOurSchema,
)
from fast_zero.models.models import User

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


@router.get('/parcelamento', response_model=ParcelamentoListSchema)
def read_parcelmanto_by_negociacao_id(
    session: T_Session, user: T_CurrentUser,
    negociacao_id: int, type: int, page: int = 1, page_size: int = 10,
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
        query.order_by(asc(ParcelamentoNegociacao.data)).offset(skip).limit(limit)
    ).all()
    
    return {'rows': rows, 'total_records': total_records}


@router.get('/parcelamento/{parcelamento_id}', response_model=ParcelamentoOurSchema)
def get_parcelamento_by_id(
    session: T_Session, user: T_CurrentUser, parcelamento_id: int
):
    row = session.get(ParcelamentoNegociacao, parcelamento_id)
    
    if row is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Parcelamento not Found'
        )
    
    return row

