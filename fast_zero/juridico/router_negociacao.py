from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session
from fast_zero.juridico.models import NegociacaoCredito
from fast_zero.juridico.negociacao_schema import (
    NegociacaoListSchema,
    NegociacaoOutSchema,
)

router = APIRouter(prefix='/juridico', tags=['negociação'])
T_Session = Annotated[Session, Depends(get_session)]


@router.get('/negociacao', response_model=NegociacaoListSchema)
def read_negociacao(
    session: T_Session,
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
def get_negociacao_by_id(session: T_Session, negociacao_id: int):
    row = session.get(NegociacaoCredito, negociacao_id)

    if row is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil not found',
        )

    return row
