from datetime import timedelta
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from sqlalchemy import (
    DECIMAL,
    BigInteger,
    Date,
    ForeignKey,
    Integer,
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

from fast_zero.models.models import Base, event

table_registry = registry()


@table_registry.mapped_as_dataclass
class NegociacaoCredito(Base):
    __tablename__ = 'negociacao_credito'
    __table_args__ = (
        UniqueConstraint(
            'processo',
            'executado',
            'contrato',
            name='unique_processo_executado_contrato',
        ),
        # {'order_by': 'id DESC'},
    )

    id: Mapped[int] = mapped_column(BigInteger, init=False, primary_key=True)
    processo: Mapped[str] = mapped_column(String(200), nullable=True)
    executado: Mapped[str] = mapped_column(String(200), nullable=False)
    contrato: Mapped[str] = mapped_column(String(100), nullable=True)
    val_devido: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    val_desconto: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=True
    )
    val_neg: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    data_pri_parc: Mapped[Date] = mapped_column(Date)
    data_ult_parc: Mapped[Date] = mapped_column(Date)
    val_entrada: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)
    qtd_parc_ent: Mapped[int] = mapped_column(Integer, nullable=True)
    data_pri_parc_entr: Mapped[Date] = mapped_column(Date, nullable=True)
    data_ult_parc_entr: Mapped[Date] = mapped_column(Date, nullable=True)
    obs_val_neg: Mapped[str] = mapped_column(String(100), nullable=True)
    is_term_ex_jud: Mapped[bool] = mapped_column(default=False)
    is_hom_ext_jud: Mapped[bool] = mapped_column(default=False)
    qtd: Mapped[int] = mapped_column(Integer, default=1)
    taxa_mes: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0.00)
    val_parc: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0.00)
    is_cal_parc_mensal: Mapped[bool] = mapped_column(default=False)
    is_cal_parc_entrada: Mapped[bool] = mapped_column(default=False)
    is_descumprido: Mapped[bool] = mapped_column(default=False)
    is_liquidado: Mapped[bool] = mapped_column(default=False)
    is_retorno_execucao: Mapped[bool] = mapped_column(default=False)

    def _gerarParcelasMensal(self):
        valor_emprestimo = self.val_neg
        taxa_juros = self.taxa_mes / 100
        numero_parcelas = self.qtd
        valor_parcela = (
            valor_emprestimo
            * (taxa_juros * (1 + taxa_juros) ** numero_parcelas)
            / ((1 + taxa_juros) ** numero_parcelas - 1)
        )

        # print(f"O pagamento mensal é:
        # {valor_parcela:.2f} : {numero_parcelas}")

        return round(valor_parcela, 2)


@event.listens_for(NegociacaoCredito, 'after_insert')
def after_insert_negociacao_credito(mapper, connection, target):
    # Abre uma nova sessão para realizar operações subsequentes
    session = Session(bind=connection)

    try:
        if target.is_cal_parc_mensal:
            target.val_parc = target._gerarParcelasMensal()
            target.is_cal_parc_mensal = False

            # Salvar parcelas qtd data_pri_parc
            if target.qtd > 0:
                data_temp = target.data_pri_parc + timedelta(days=1)
                for i in range(1, target.qtd + 1):
                    if i != 1:
                        # calcular_data_final
                        data_temp += relativedelta(months=1)
                    try:
                        parcela = ParcelamentoNegociacao(
                            negociacao_id=target.id,  # type: ignore
                            type=1,
                            numero_parcela=i,
                            data=data_temp,
                            val_parcela=target.val_parc,
                            is_pg=False,
                            is_val_juros=False,
                            val_pago=None,
                            data_pgto=None,
                            obs_val_pago='',
                        )
                        session.add(parcela)
                    except Exception as e:
                        print(f'Erro ao criar parcela: {e}')
            session.commit()  # Salva as parcelas geradas
            # session.refresh(target)  # Atualiza o objeto `target` na sessão

        if target.is_cal_parc_entrada:
            target.is_cal_parc_entrada = False

            if target.qtd_parc_ent > 0:
                valor_parcela = target.val_entrada / target.qtd_parc_ent
                data_temp = target.data_pri_parc_entr + timedelta(days=1)
                for i in range(1, target.qtd_parc_ent + 1):
                    if i != 1:
                        # calcular_data_final
                        data_temp += relativedelta(months=1)
                    try:
                        parcela = ParcelamentoNegociacao(
                            negociacao_id=target.id,  # type: ignore
                            type=2,
                            numero_parcela=i,
                            data=data_temp,
                            val_parcela=valor_parcela,
                            is_pg=False,
                            is_val_juros=False,
                            val_pago=None,
                            data_pgto=None,
                            obs_val_pago='',
                        )
                        session.add(parcela)
                    except Exception as e:
                        print(f'Erro ao criar parcela de entrada: {e}')
            session.commit()  # Salva as parcelas de entrada geradas
            # session.refresh(target)  # Atualiza o objeto `target` na sessão

        session.commit()  # Salva todas as alterações finais no objeto `target`

    except Exception as e:
        session.rollback()
        print(f'Erro ao executar tarefa pós-inserção: {e}')
    finally:
        session.close()


@table_registry.mapped_as_dataclass
class ParcelamentoNegociacao(Base):
    __tablename__ = 'parcelamento_negociacao'
    __table_args__ = (
        UniqueConstraint(
            'numero_parcela',
            'type',
            'negociacao_id',
            name='unique_numero_type_negociacao',
        ),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    negociacao_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('negociacao_credito.id', ondelete='CASCADE'),
        nullable=False,
    )
    negociacao: Mapped['NegociacaoCredito'] = relationship('NegociacaoCredito')

    data: Mapped[Date] = mapped_column(Date, nullable=False)
    val_parcela: Mapped[DECIMAL] = mapped_column(
        DECIMAL(10, 2), nullable=False
    )
    val_pago: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=True)
    obs_val_pago: Mapped[str] = mapped_column(String(100), nullable=True)
    data_pgto: Mapped[Date] = mapped_column(Date, nullable=True)
    type: Mapped[int] = mapped_column(Integer, default=1)
    numero_parcela: Mapped[int] = mapped_column(Integer, default=0)
    is_pg: Mapped[bool] = mapped_column(default=False)
    is_val_juros: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'<ParcelamentoNegociacao(numero_parcela={self.numero_parcela},'
        +'data={self.data}, type={self.type})>'
