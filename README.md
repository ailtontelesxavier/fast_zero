# gera SECRET_KEY no terminal
python
import secrets
secrets.token_hex(256)

# fazer migrate
docker exec -it b8d4ddba3a4a sh -c "poetry run alembic upgrade head"

# subir somento o banco para teste
docker-compose up -d fastzero_database