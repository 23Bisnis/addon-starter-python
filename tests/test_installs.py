from app.db import init_db, engine
from app.installs import upsert_install, get_install, InstallRecord


def setup_function():
    init_db()


def test_upsert_and_get_install():
    rec = InstallRecord(
        install_id=15,
        tenant_id=42,
        signing_secret="s3cr3t",
        oauth_token="tok",
        scopes=["supplier.dispatch"],
    )
    upsert_install(rec)
    got = get_install(15)
    assert got is not None
    assert got.tenant_id == 42
    assert got.signing_secret == "s3cr3t"
    assert "supplier.dispatch" in got.scopes


def test_get_missing_install_returns_none():
    assert get_install(9999) is None


def test_upsert_updates_existing():
    upsert_install(InstallRecord(install_id=1, tenant_id=10, signing_secret="s", oauth_token="t", scopes=[]))
    upsert_install(InstallRecord(install_id=1, tenant_id=10, signing_secret="new", oauth_token="t2", scopes=["x"]))
    got = get_install(1)
    assert got is not None
    assert got.signing_secret == "new"
    assert got.oauth_token == "t2"
    assert "x" in got.scopes
