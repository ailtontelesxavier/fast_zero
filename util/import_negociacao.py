import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://app_user:app_password@172.16.238.10:5432/bd_intranet"
DATABASE_URL2 = "postgresql+psycopg://app_user:app_password@172.16.238.10:5432/app_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar o mecanismo de conexão
engine = create_engine(DATABASE_URL)

engine2 = create_engine(DATABASE_URL2)


def consultaNegociacaoCredito():
    # select_user_sql = 'SELECT id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined FROM public.auth_user;'
    select_user_sql = """SELECT id, processo, executado, contrato, is_term_ex_jud, 
    is_hom_ext_jud, val_devido,val_desconto, val_neg, obs_val_neg, qtd, taxa_mes, 
    val_parc, data_pri_parc, data_ult_parc, val_entrada, qtd_parc_ent,
    data_pri_parc_entr, data_ult_parc_entr, is_cal_parc_mensal, is_cal_parc_entrada
    , is_descumprido, is_liquidado, is_retorno_execucao FROM public.juridico_negociacaocredito;"""

    with engine.connect() as connection:
        # Execute um comando SQL
        resultado = connection.execute(sa.text(select_user_sql))

        # Imprima os resultados
        for linha in resultado:
            # print(linha)
            insertNegociacaoCredito(linha)


def insertNegociacaoCredito(row):
    # Formate a string SQL para inserção
    insert_sql = """
    INSERT INTO negociacao_credito (
        id, processo, executado, contrato, is_term_ex_jud, 
        is_hom_ext_jud, val_devido, val_desconto, val_neg, 
        obs_val_neg, qtd, taxa_mes, val_parc, data_pri_parc,
        data_ult_parc, val_entrada, qtd_parc_ent,
        data_pri_parc_entr, data_ult_parc_entr,
        is_cal_parc_mensal, is_cal_parc_entrada,
        is_descumprido, is_liquidado, is_retorno_execucao
    ) VALUES (
        :id, :processo, :executado, :contrato, :is_term_ex_jud, 
        :is_hom_ext_jud, :val_devido, :val_desconto, :val_neg, 
        :obs_val_neg, :qtd, :taxa_mes, :val_parc, :data_pri_parc,
        :data_ult_parc, :val_entrada, :qtd_parc_ent,
        :data_pri_parc_entr, :data_ult_parc_entr,
        :is_cal_parc_mensal, :is_cal_parc_entrada,
        :is_descumprido, :is_liquidado, :is_retorno_execucao
    );
    """

    # Substitui None por valores apropriados para SQL
    row = tuple('' if x is None else x for x in row)

    with engine2.connect() as connection:
        transaction = connection.begin()
        try:
            # Execute o comando SQL com a ligação de parâmetros
            resultado = connection.execute(sa.text(insert_sql), {
                'id': row[0],
                'processo': row[1],
                'executado': row[2],
                'contrato': row[3],
                'is_term_ex_jud': row[4],
                'is_hom_ext_jud': row[5],
                'val_devido': row[6],
                'val_desconto': row[7] if row[7] else None,
                'val_neg': row[8],
                'obs_val_neg': row[9],
                'qtd': row[10],
                'taxa_mes': row[11],
                'val_parc': row[12],
                'data_pri_parc': row[13],
                'data_ult_parc': row[14],
                'val_entrada': row[15] if row[15] else None,
                'qtd_parc_ent': row[16] if row[16] else None,
                'data_pri_parc_entr': row[17] if row[17] else None,
                'data_ult_parc_entr': row[18] if row[18] else None,
                'is_cal_parc_mensal': row[19],
                'is_cal_parc_entrada': row[20],
                'is_descumprido': row[21],
                'is_liquidado': row[22],
                'is_retorno_execucao': row[23]
            })
            print(resultado)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            print(f"Erro ao inserir negociação de crédito: {e}")
            raise


if __name__ == '__main__':
    consultaNegociacaoCredito()
