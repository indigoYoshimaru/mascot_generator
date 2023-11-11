from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.utils import app_config, get_logger

logger = get_logger(__name__)

logger.info(f"{app_config=}")

engine = create_engine(
    url=app_config.db_config.url,
    connect_args=app_config.db_config.connect_args,
    echo=True,
)
SessionLocal = sessionmaker(**app_config.db_config.session_args)

Base = declarative_base()

logger.info(f"{engine=}")
logger.info(f"{SessionLocal=}")
logger.info(f"{Base=}")
