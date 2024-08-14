from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select, desc
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session
from fast_zero.juridico.models import NegociacaoCredito
from fast_zero.juridico.negociacao_schema import NegociacaoOutSchema, NegociacaoListSchema

router = APIRouter(prefix='/juridico', tags=['negociação'])
T_Session = Annotated[Session, Depends(get_session)]


@router.get('/negociacao', response_model=NegociacaoListSchema)
def read_negociacao(session: T_Session, page: int=1, page_size: int=10):
    skip = (page - 1) * page_size
    limit = page_size
    
    total_records = session.scalar(select(func.count(NegociacaoCredito.id)))
    
    rows = session.scalars(
        select(NegociacaoCredito)
        .order_by(NegociacaoCredito.id)
        .offset(skip)
        .limit(limit)
    ).all()
    
    return {'rows': rows, 'total_records': total_records}
