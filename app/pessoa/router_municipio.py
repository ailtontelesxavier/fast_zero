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

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.pessoa.apis import getCityforState, getStates
from app.pessoa.models import Municipio, Regiao, Uf


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
