from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.db import init_db
from app.installs import get_install

client = TestClient(app)


class _Creds:
    install_id = 15
    tenant_id = 42
    signing_secret = "sek"
    platform_oauth_token = "tok"
    scopes_granted = ["supplier.dispatch"]


class _Resp:
    data = _Creds()


def setup_function():
    init_db()


def test_oauth_install_exchanges_code_and_persists():
    with patch("app.platform.oauth.oauth_exchange") as m:
        m.sync.return_value = _Resp()
        r = client.get("/oauth/install", params={"install_id": 15, "code": "one-time"})
    assert r.status_code == 200
    rec = get_install(15)
    assert rec is not None
    assert rec.signing_secret == "sek"
    assert rec.oauth_token == "tok"
