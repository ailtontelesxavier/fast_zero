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
    # insert_user_sql = "INSERT INTO public.auth_user( \
    #            id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) \
    #            VALUES ({}, '{}', '{}', {}, '{}', '{}', '{}', '{}', {}, {}, '{}');".format(*row)
    insert_user_sql = "INSERT INTO public.juridico_negociacaocredito( \
	                id, processo, executado, contrato, is_term_ex_jud, \
                    is_hom_ext_jud, val_devido, val_desconto, val_neg, \
                    obs_val_neg, qtd, taxa_mes, val_parc, data_pri_parc,\
                    data_ult_parc, val_entrada, qtd_parc_ent,\
                    data_pri_parc_entr, data_ult_parc_entr,\
                    is_cal_parc_mensal, is_cal_parc_entrada,\
                    is_descumprido, is_liquidado, is_retorno_execucao)\
	        VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});".format(*('' if x is None else x for x in row))

    with engine2.connect() as connection:
        transaction = connection.begin()
        try:
            # Execute um comando SQL
            resultado = connection.execute(sa.text(insert_user_sql))
            print(resultado)
            transaction.commit()
        except:
            transaction.rollback()
            raise


if __name__ == '__main__':
    consultaNegociacaoCredito()
