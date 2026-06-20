import hashlib
import hmac
import time
import uuid

import pytest


def sign_body(secret: str, body: bytes, ts: str | None = None, nonce: str | None = None):
    ts = ts or str(int(time.time()))
    nonce = nonce or str(uuid.uuid4())
    msg = ts.encode() + b"\n" + nonce.encode() + b"\n" + body
    mac = hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()
    return {
        "X-Platform-Signature": f"hmac_sha256={mac}",
        "X-Platform-Timestamp": ts,
        "X-Platform-Nonce": nonce,
    }


@pytest.fixture
def signer():
    return sign_body


from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


@pytest.fixture(autouse=True)
def in_memory_db(monkeypatch):
    """Isolate every test on a fresh in-memory SQLite DB (no real addon.db writes)."""
    from app import db as _db

    mem_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    monkeypatch.setattr(_db, "engine", mem_engine)
    import app.installs as _installs
    monkeypatch.setattr(_installs, "engine", mem_engine)
    # Register all tables defined so far on the shared metadata, then create them.
    _db.metadata.create_all(mem_engine)
    yield
