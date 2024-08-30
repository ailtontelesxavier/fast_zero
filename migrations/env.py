from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
#from app.models.models import table_registry
from app.core.settings import Settings

from logging.config import fileConfig
from sqlalchemy import engine_from_config, MetaData
from sqlalchemy import pool
from alembic import context
import os
import importlib

# Atualize aqui para incluir o caminho onde seus arquivos models.py estão localizados
MODEL_PATHS = [
    'app.models.models',  # Por exemplo, se os arquivos estão em app/models
    'app.juridico.models',  # Adicione outros caminhos conforme necessário
]


# Função para importar todos os módulos de models e coletar a metadata
def collect_metadata():
    metadata = MetaData()

    for path in MODEL_PATHS:
        try:
            # Importar o módulo
            module = importlib.import_module(path)
            # Adicionar a metadata
            if hasattr(module, 'table_registry'):
                for table in module.table_registry.metadata.tables.values():
                    table.tometadata(metadata)
            else:
                print(f"Warning: No table_registry found in module {path}")
        except ImportError as e:
            print(f"Error importing module {path}: {e}")
    return metadata

# Use a função para coletar a metadata
target_metadata = collect_metadata()

# Alembic Config object
config = context.config
config.set_main_option('sqlalchemy.url', Settings().DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
