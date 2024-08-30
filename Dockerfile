FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && pip install poetry \
&& poetry config installer.max-workers 10 \
&& poetry install --no-interaction --no-ansi

EXPOSE 8001

# Comando para iniciar o servidor UVicorn
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8002", "app.app:app"]