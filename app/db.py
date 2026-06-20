from sqlalchemy import create_engine, MetaData
from app.config import settings

_connect_args = {"check_same_thread": False} if settings.db_url.startswith("sqlite") else {}
engine = create_engine(settings.db_url, future=True, connect_args=_connect_args)
metadata = MetaData()


def init_db() -> None:
    # Import table modules so they register on `metadata`, then create all.
    from app import installs  # noqa: F401

    metadata.create_all(engine)
