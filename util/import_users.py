from datetime import datetime
import pytz
from fast_zero.models.models import User
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

password = "1q2w3e4r5t!@#$%12345"
encoded_password = quote_plus(password)

DATABASE_URL = (
    f"postgresql+psycopg://sifomento:{encoded_password}@10.99.1.49:5432/sifomento"
)
DATABASE_URL2 = (
    'postgresql+psycopg://app_user:app_password@172.16.238.10:5432/app_db'
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar o mecanismo de conexão
engine = create_engine(DATABASE_URL)

engine2 = create_engine(DATABASE_URL2)


def consultaUsers():
    select_user_sql = """SELECT id, username, password, email,
    is_active, date_joined, first_name, last_name, last_login, is_superuser, is_staff 
    FROM public.auth_user ORDER BY id;"""

    with engine.connect() as connection:
        # Execute um comando SQL
        resultado = connection.execute(sa.text(select_user_sql))

        # Imprima os resultados
        for linha in resultado:
            print(linha)
            insertUser(linha)


def insertUser(row):
    # Formate a string SQL para inserção
    insert_sql = """
    INSERT INTO public.users(
	id, username, password, email, is_active, created_at, updated_at,
    full_name, otp_base32, otp_created_at, login_otp_used, is_staff,
    is_superuser, otp_auth_url, last_login)
	VALUES (
        :id,
        :username,
        :password,
        :email,
        :is_active,
        :created_at,
        :updated_at,
        :full_name,
        :otp_base32,
        :otp_created_at,
        :login_otp_used,
        :is_staff,
        :is_superuser,
        :otp_auth_url,
        :last_login
    );
    """

    # Substitui None por valores apropriados para SQL
    row = tuple('' if x is None else x for x in row)
    TIME_ZONE = 'America/Sao_Paulo'
    tz = pytz.timezone(TIME_ZONE)

    with engine2.connect() as connection:
        transaction = connection.begin()
        db_row = connection.execute(sa.text(f"SELECT id FROM public.users where id ={row[0]}"))
        result = db_row.fetchone()
        if not result:
            try:
                # Execute o comando SQL com a ligação de parâmetros
                resultado = connection.execute(
                    sa.text(insert_sql),
                    {
                        'id':row[0],
                        'username':row[1],
                        'password':row[2],
                        'email':row[3] if row[3] else row[1]+'@fomento.to.gov.br',
                        'is_active':row[4],
                        'created_at':row[5],
                        'updated_at':datetime.now(tz),
                        'full_name':row[6]+' '+row[7],
                        'otp_base32':User.create_otp_base32(),
                        'otp_created_at':datetime.now(tz),
                        'login_otp_used':False,
                        'is_staff':row[10],
                        'is_superuser':row[9],
                        'otp_auth_url':'',
                        'last_login': row[8]
                    },
                )
                print(resultado)
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                print(f'Erro ao inserir negociação de crédito: {e}')
                raise


if __name__ == '__main__':
    consultaUsers()
