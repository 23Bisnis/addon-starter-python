import json
from dataclasses import dataclass

from sqlalchemy import Table, Column, Integer, String, Text, insert, select, update
from app.db import metadata, engine

installs_table = Table(
    "installs",
    metadata,
    Column("install_id", Integer, primary_key=True),
    Column("tenant_id", Integer, nullable=False),
    Column("signing_secret", String, nullable=False),
    Column("oauth_token", String, nullable=False),
    Column("scopes_json", Text, nullable=False, default="[]"),
)


@dataclass
class InstallRecord:
    install_id: int
    tenant_id: int
    signing_secret: str
    oauth_token: str
    scopes: list[str]


def upsert_install(rec: InstallRecord) -> None:
    with engine.begin() as conn:
        exists = conn.execute(
            select(installs_table.c.install_id).where(
                installs_table.c.install_id == rec.install_id
            )
        ).first()
        values = dict(
            tenant_id=rec.tenant_id,
            signing_secret=rec.signing_secret,
            oauth_token=rec.oauth_token,
            scopes_json=json.dumps(rec.scopes),
        )
        if exists:
            conn.execute(
                update(installs_table)
                .where(installs_table.c.install_id == rec.install_id)
                .values(**values)
            )
        else:
            conn.execute(insert(installs_table).values(install_id=rec.install_id, **values))


def get_install(install_id: int) -> InstallRecord | None:
    with engine.connect() as conn:
        row = conn.execute(
            select(installs_table).where(installs_table.c.install_id == install_id)
        ).first()
    if row is None:
        return None
    return InstallRecord(
        install_id=row.install_id,
        tenant_id=row.tenant_id,
        signing_secret=row.signing_secret,
        oauth_token=row.oauth_token,
        scopes=json.loads(row.scopes_json),
    )
