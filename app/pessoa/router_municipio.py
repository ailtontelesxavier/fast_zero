"""
def save_states_and_citys():
    # salva stados e cidades via api ibge
    list_uf = getStates()
    for _uf in list_uf:
        unidade = Uf.objects.get_or_create(
            id=_uf.get('id'),
            sigla=_uf.get('sigla'),
            nome=_uf.get('nome')
            )
        Regiao.objects.get_or_create(
            id=_uf.get('regiao').get('id'),
            nome=_uf.get('regiao').get('nome'),
            sigla=_uf.get('regiao').get('sigla')
        )
        list_city = getCityforState(_uf.get('sigla'))
        for city in list_city:
            Municipio.objects.get_or_create(
                id=city.get('id'),
                nome=city.get('nome'),
                uf=unidade[0]
            )

"""

from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, func, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.pessoa.apis import getCityforState, getStates
from app.pessoa.models import Municipio, Regiao, Uf
from app.pessoa.municipio_schema import MunicipioList, UfList


router = APIRouter(prefix='/pessoa', tags=['municipio'])
T_Session = Annotated[Session, Depends(get_session)]


@router.get('/atualizar')
def update_municipios(session: T_Session):
    # salva stados e cidades via api ibge
    list_uf = getStates()
    for _uf in list_uf:
        unidade = session.get(Uf, _uf.get('id'))
        if not unidade:
            unidade = Uf(
                id=_uf.get('id'),
                sigla=_uf.get('sigla'),
                nome=_uf.get('nome')
            )
            session.add(unidade)
        
        regiao = session.get(Regiao, _uf.get('regiao').get('id'))
        if not regiao:
            regiao = Regiao(
                id=_uf.get('regiao').get('id'),
                nome=_uf.get('regiao').get('nome'),
                sigla=_uf.get('regiao').get('sigla')
            )
            session.add(regiao)
        
        list_city = getCityforState(_uf.get('sigla'))
        for city in list_city:
            db_municipio = session.get(Municipio, city.get('id'))
            if not db_municipio:
                db_municipio = Municipio(
                    id=city.get('id'),
                    nome=city.get('nome'),
                    uf_id=_uf.get('id'),
                    uf=unidade,
                )
                session.add(db_municipio)

        session.commit()


@router.get('/uf', response_model=UfList)
def read_ufs(session: T_Session):
    rows = session.scalars(
        select(Uf).order_by(Uf.sigla)
    ).all()

    return {'rows': rows}


@router.get('/cidades/{uf_id}', response_model=MunicipioList)
def read_cidades_by_uf(
    session:T_Session,
    uf_id: int,
    page: int = 1,
    page_size: int = 10
):
    skip = (page - 1) * page_size
    limit = page_size

    db_uf = session.get(Uf, uf_id)
    
    if db_uf is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='UF not found'
        )

    query = select(Municipio).where(
        (Municipio.uf_id == uf_id)
    )
    total_records = session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    rows = session.scalars(
        query.order_by(asc(Municipio.nome))
        .offset(skip)
        .limit(limit)
    ).all()

    return {'rows': rows, 'total_records': total_records}