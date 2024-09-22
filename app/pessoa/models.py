from datetime import timedelta
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    Session,
    mapped_column,
    registry,
    relationship,
)

from app.models.models import Base

table_registry = registry()


@table_registry.mapped_as_dataclass
class Regiao(Base):
    __tablename__ = 'regiao'
    __table_args__ = (
        UniqueConstraint(
            'nome',
            'sigla',
            name='unique_regiao_nome_sigla',
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str]
    sigla: Mapped[str]

    def __repr__(self) -> str:
        return f'{self.nome} - {self.sigla}'


@table_registry.mapped_as_dataclass
class Uf(Base):
    """
    API - https://servicodados.ibge.gov.br/api/docs/localidades
    https://servicodados.ibge.gov.br/api/v1/localidades/estados
    """
    __tablename__ = 'uf'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sigla: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)
    nome: Mapped[str]

    #municipio: Mapped['Municipio'] = relationship('Municipio')

    def __repr__(self):
        return self.sigla


@table_registry.mapped_as_dataclass
class Municipio(Base):
    """
    API - https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios
    https://servicodados.ibge.gov.br/api/v1/localidades/estados/TO/municipios
    """
    __tablename__ = 'municipio'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str]
    uf_id: Mapped[int] = mapped_column(
        ForeignKey('uf.id', ondelete='CASCADE')
    )

    uf: Mapped[Uf] = relationship('Uf')


    def __repr__(self):
        return self.nome + ' - ' + self.uf.sigla


@table_registry.mapped_as_dataclass
class bairro(Base):
    __tablename__ = 'bairro'
    __table_args__ = (
        UniqueConstraint(
            'municipio_id', 'nome', name='uix_municipio_id_nome'
        )
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    municipio_id: Mapped[int] = mapped_column(ForeignKey('municipio.id'))
    nome: Mapped[str]


@table_registry.mapped_as_dataclass
class cep(Base):
    __tablename__ = 'cep'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    cep: Mapped[str] = mapped_column(String(10))
    bairro_id: Mapped[int] = mapped_column(ForeignKey('bairro.id'))


@table_registry.mapped_as_dataclass
class endereco(Base):
    __tablename__ = 'endereco'
    id: Mapped[int] = mapped_column(int=False, primary_key=True)
    rua: Mapped[str] = mapped_column(String(255))
    numero: Mapped[str] = mapped_column(String(10))
    complemento: Mapped[str]
    cep_id: Mapped[int] = mapped_column(ForeignKey('cep.id'))


@table_registry.mapped_as_dataclass
class Pessoa(Base):
    __tablename__ = 'pessoa'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    #fisica=11, juridica=14
    cpf_cnpj: Mapped[str] = mapped_column(String(14), unique=True)
    rg: Mapped[str] = mapped_column(String(11), nullable=True)
    ie: Mapped[str] = mapped_column(String(12), nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    telefone: Mapped[str] = mapped_column(nullable=True)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    endereco_id: Mapped[int] = mapped_column(ForeignKey('endereco.id'))
