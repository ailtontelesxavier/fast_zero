from datetime import date, timedelta
from decimal import Decimal
from http import HTTPStatus
from typing import Annotated, Optional

from dateutil import parser
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.security import get_current_user
from app.juridico.models import NegociacaoCredito, ParcelamentoNegociacao
from app.juridico.negociacao_schema import (
    NegociacaoInSchema,
    NegociacaoListSchema,
    NegociacaoOutSchema,
    NegociacaoUpdateSchema,
    NegociacaoVenciNaSemanaResponse,
    ParcelamentoInSchema,
    ParcelamentoListSchema,
    ParcelamentoOurSchema,
    ParcelamentoUpdateSchema,
)
from app.models.models import User
from app.schemas.schemas import Message

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
    negociacao: NegociacaoInSchema, session: T_Session, user: T_CurrentUser
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
        obs_val_neg=negociacao.obs_val_neg,  # type: ignore
        is_term_ex_jud=negociacao.is_term_ex_jud,  # type: ignore
        is_hom_ext_jud=negociacao.is_hom_ext_jud,  # type: ignore
        qtd=negociacao.qtd,
        taxa_mes=negociacao.taxa_mes,
        val_parc=negociacao.val_parc,
        is_cal_parc_mensal=True,
        is_cal_parc_entrada=True,
        is_descumprido=negociacao.is_descumprido,  # type: ignore
        is_liquidado=negociacao.is_liquidado,  # type: ignore
        is_retorno_execucao=negociacao.is_retorno_execucao,  # type: ignore
    )

    session.add(db_negociacao)
    session.commit()
    session.refresh(db_negociacao)
    return db_negociacao


@router.patch(
    '/negociacao/{negociacao_id}', response_model=NegociacaoOutSchema
)
def update_negociacao_by_id(  # type: ignore
    negociacao_id: int,
    negociacao: NegociacaoUpdateSchema,
    session: T_Session,
    user: T_CurrentUser,
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
def delete_negociacao(  # type: ignore
    negociacao_id: int, session: T_Session, user: T_CurrentUser
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


@router.post(
    '/parcelamento',
    status_code=HTTPStatus.CREATED,
    response_model=ParcelamentoOurSchema,
)
def create_parcelamento(
    parcelamento: ParcelamentoInSchema, session: T_Session, user: T_CurrentUser
):
    db_parcelamento = session.scalar(
        select(ParcelamentoNegociacao).where(
            (
                ParcelamentoNegociacao.numero_parcela
                == parcelamento.numero_parcela
            )
            & (ParcelamentoNegociacao.type == parcelamento.type)
            & (
                ParcelamentoNegociacao.negociacao_id
                == parcelamento.negociacao_id
            )
        )
    )

    if db_parcelamento:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='parcelamento Credito ja cadastrado',
        )

    db_parcelamento = ParcelamentoNegociacao(
        negociacao_id=parcelamento.negociacao_id,
        data=parcelamento.data,  # type: ignore
        val_parcela=parcelamento.val_parcela,  # type: ignore
        val_pago=parcelamento.val_pago,  # type: ignore
        obs_val_pago=parcelamento.obs_val_pago,  # type: ignore
        data_pgto=parcelamento.data_pgto,  # type: ignore
        type=parcelamento.type,
        numero_parcela=parcelamento.numero_parcela,
        is_pg=parcelamento.is_pg,
        is_val_juros=parcelamento.is_val_juros,
    )

    session.add(db_parcelamento)
    session.commit()
    session.refresh(db_parcelamento)
    return db_parcelamento


@router.patch(
    '/parcelamento/{parcelamento_id}', response_model=ParcelamentoOurSchema
)
def update_parcelamento_by_id(
    parcelamento_id: int,
    parcelamento: ParcelamentoUpdateSchema,
    session: T_Session,
    user: T_CurrentUser,
):
    db_row = session.get(ParcelamentoNegociacao, parcelamento_id)
    if not db_row:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Parcelamento not found.'
        )
    for key, value in parcelamento.model_dump(exclude_unset=True).items():
        setattr(db_row, key, value)

    session.add(db_row)
    session.commit()
    session.refresh(db_row)
    return db_row


@router.delete('/parcelamento/{parcelamento_id}', response_model=Message)
async def delete_parcelamento(
    parcelamento_id: int, session: T_Session, user: T_CurrentUser
):
    db_row = session.get(ParcelamentoNegociacao, parcelamento_id)

    if not db_row:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Parcelamento not found.'
        )

    session.delete(db_row)
    session.commit()

    return {'message': 'Parcelamento deletado'}


@router.get(
    '/negociacao/relatorio/venci-na-semana',
    response_model=NegociacaoVenciNaSemanaResponse,
)
async def negoc_venci_na_semana(
    session: T_Session,
    user: T_CurrentUser,
    page: int = 1,
    page_size: int = 10,
):
    skip = (page - 1) * page_size
    limit = page_size

    hoje = date.today()
    inicio_da_semana = hoje - timedelta(days=hoje.weekday())
    fim_da_semana = inicio_da_semana + timedelta(days=6)

    query = (
        select(
            ParcelamentoNegociacao.id,
            NegociacaoCredito.processo.label('processo'),
            NegociacaoCredito.executado,
            ParcelamentoNegociacao.type,
            ParcelamentoNegociacao.data,
            ParcelamentoNegociacao.val_parcela,
            ParcelamentoNegociacao.val_pago,
            ParcelamentoNegociacao.data_pgto,
            ParcelamentoNegociacao.is_val_juros.label('juros'),
        )
        .join(ParcelamentoNegociacao.negociacao)
        .filter(
            and_(
                ParcelamentoNegociacao.data > inicio_da_semana,
                ParcelamentoNegociacao.data < fim_da_semana,
                ParcelamentoNegociacao.data_pgto.is_(None),
                NegociacaoCredito.is_liquidado.is_(False),
            )
        )
        .order_by(asc(ParcelamentoNegociacao.data))
    )

    total_records = session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    rows = session.execute(query.offset(skip).limit(limit)).all()

    # resumo
    query2 = (
        select(
            # func.count(ParcelamentoNegociacao.id).label("total_parcelas"),
            func.sum(ParcelamentoNegociacao.val_parcela).label(
                'total_val_parcela'
            ),
        )
        .select_from(ParcelamentoNegociacao)
        .join(
            NegociacaoCredito,
            ParcelamentoNegociacao.negociacao_id == NegociacaoCredito.id,
        )
        .filter(
            and_(
                ParcelamentoNegociacao.data > inicio_da_semana,
                ParcelamentoNegociacao.data < fim_da_semana,
                ParcelamentoNegociacao.data_pgto.is_(None),
                NegociacaoCredito.is_liquidado.is_(False),
            )
        )
    )

    result = session.execute(query2).first()

    total_val_parcela = result[0] if result is not None else 0

    return {
        'rows': rows,
        'total_records': total_records,
        'total_val_parcela': total_val_parcela,
    }


@router.get(
    '/negociacao/relatorio/ha-venc-30d',
    response_model=NegociacaoVenciNaSemanaResponse,
)
async def negoc_ha_venc_30d(
    session: T_Session,
    user: T_CurrentUser,
    page: int = 1,
    page_size: int = 10,
):
    skip = (page - 1) * page_size
    limit = page_size

    hoje = date.today()
    data_mais_30_dias = hoje + timedelta(days=30)

    query = (
        select(
            ParcelamentoNegociacao.id,
            NegociacaoCredito.processo.label('processo'),
            NegociacaoCredito.executado,
            ParcelamentoNegociacao.type,
            ParcelamentoNegociacao.data,
            ParcelamentoNegociacao.val_parcela,
            ParcelamentoNegociacao.val_pago,
            ParcelamentoNegociacao.data_pgto,
            ParcelamentoNegociacao.is_val_juros.label('juros'),
        )
        .join(ParcelamentoNegociacao.negociacao)
        .filter(
            and_(
                ParcelamentoNegociacao.data > hoje,
                ParcelamentoNegociacao.data < data_mais_30_dias,
                ParcelamentoNegociacao.data_pgto.is_(None),
                NegociacaoCredito.is_liquidado.is_(False),
            )
        )
        .order_by(asc(ParcelamentoNegociacao.data))
    )

    total_records = session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    rows = session.execute(query.offset(skip).limit(limit)).all()

    # resumo
    query2 = (
        select(
            # func.count(ParcelamentoNegociacao.id).label("total_parcelas"),
            func.sum(ParcelamentoNegociacao.val_parcela).label(
                'total_val_parcela'
            ),
        )
        .select_from(ParcelamentoNegociacao)
        .join(
            NegociacaoCredito,
            ParcelamentoNegociacao.negociacao_id == NegociacaoCredito.id,
        )
        .filter(
            and_(
                ParcelamentoNegociacao.data > hoje,
                ParcelamentoNegociacao.data < data_mais_30_dias,
                ParcelamentoNegociacao.data_pgto.is_(None),
                NegociacaoCredito.is_liquidado.is_(False),
            )
        )
    )

    result = session.execute(query2).first()

    total_val_parcela = result[0] if result is not None else 0

    return {
        'rows': rows,
        'total_records': total_records,
        'total_val_parcela': total_val_parcela,
    }


@router.get(
    '/negociacao/relatorio/negoc-venvidos',
    response_model=NegociacaoVenciNaSemanaResponse,
)
async def negoc_vencidos(
    session: T_Session,
    user: T_CurrentUser,
    page: int = 1,
    page_size: int = 10,
):
    skip = (page - 1) * page_size
    limit = page_size

    hoje = date.today()

    query = (
        select(
            ParcelamentoNegociacao.id,
            NegociacaoCredito.processo.label('processo'),
            NegociacaoCredito.executado,
            ParcelamentoNegociacao.type,
            ParcelamentoNegociacao.data,
            ParcelamentoNegociacao.val_parcela,
            ParcelamentoNegociacao.val_pago,
            ParcelamentoNegociacao.data_pgto,
            ParcelamentoNegociacao.is_val_juros.label('juros'),
        )
        .join(ParcelamentoNegociacao.negociacao)
        .filter(
            and_(
                ParcelamentoNegociacao.data < hoje,
                ParcelamentoNegociacao.data_pgto.is_(None),
                NegociacaoCredito.is_liquidado.is_(False),
            )
        )
        .order_by(asc(ParcelamentoNegociacao.data))
    )

    total_records = session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    rows = session.execute(query.offset(skip).limit(limit)).all()

    # resumo
    query2 = (
        select(
            # func.count(ParcelamentoNegociacao.id).label("total_parcelas"),
            func.sum(ParcelamentoNegociacao.val_parcela).label(
                'total_val_parcela'
            ),
        )
        .select_from(ParcelamentoNegociacao)
        .join(
            NegociacaoCredito,
            ParcelamentoNegociacao.negociacao_id == NegociacaoCredito.id,
        )
        .filter(
            and_(
                ParcelamentoNegociacao.data < hoje,
                ParcelamentoNegociacao.data_pgto.is_(None),
                NegociacaoCredito.is_liquidado.is_(False),
            )
        )
    )

    result = session.execute(query2).first()

    total_val_parcela = result[0] if result is not None else 0

    return {
        'rows': rows,
        'total_records': total_records,
        'total_val_parcela': total_val_parcela,
    }


@router.get('/negociacao/relatorio/')
async def negociacao_relatorio(
    session: T_Session,
    user: T_CurrentUser,
    tipo: int,
    data_inicial: str,
    data_final: str,
):
    # Parse das datas
    data_inicial_parsed = parser.parse(' '.join(data_inicial.split(' ')[0:6]))
    data_final_parsed = parser.parse(' '.join(data_final.split(' ')[0:6]))

    if tipo == 1:
        # Tipo 1: Negociações de Crédito
        query = (
            select(
                NegociacaoCredito.id,
                NegociacaoCredito.processo,
                NegociacaoCredito.executado,
                NegociacaoCredito.contrato,
                NegociacaoCredito.val_devido,
                NegociacaoCredito.val_neg,
                NegociacaoCredito.taxa_mes,
                NegociacaoCredito.qtd,
                NegociacaoCredito.val_parc,
            )
            .filter(
                and_(
                    NegociacaoCredito.data_pri_parc >= data_inicial_parsed,
                    NegociacaoCredito.data_pri_parc <= data_final_parsed,
                )
            )
            .order_by(NegociacaoCredito.executado)
        )
        result = session.execute(query).all()
        return [dict(row._mapping) for row in result]

    elif tipo == int(2):
        # Tipo 2: Parcelas de Negociação
        query = (
            select(
                ParcelamentoNegociacao.id,
                ParcelamentoNegociacao.numero_parcela,
                NegociacaoCredito.processo,
                NegociacaoCredito.executado,
                ParcelamentoNegociacao.type,
                ParcelamentoNegociacao.data,
                ParcelamentoNegociacao.val_parcela,
                ParcelamentoNegociacao.val_pago,
                ParcelamentoNegociacao.data_pgto,
                ParcelamentoNegociacao.is_val_juros,
            )
            .join(
                NegociacaoCredito,
                (ParcelamentoNegociacao.negociacao_id == NegociacaoCredito.id),
            )
            .filter(
                or_(
                    and_(
                        ParcelamentoNegociacao.data >= data_inicial_parsed,
                        ParcelamentoNegociacao.data <= data_final_parsed,
                    ),
                    and_(
                        (
                            ParcelamentoNegociacao.data_pgto
                            >= data_inicial_parsed
                        ),
                        ParcelamentoNegociacao.data_pgto <= data_final_parsed,
                    ),
                )
            )
            .order_by(
                NegociacaoCredito.executado,
                ParcelamentoNegociacao.numero_parcela,
                ParcelamentoNegociacao.type,
                ParcelamentoNegociacao.data,
                ParcelamentoNegociacao.data_pgto,
            )
        )
        result = session.execute(query).all()
        return [dict(row._mapping) for row in result]

    return {'detail': 'Invalid type parameter'}
