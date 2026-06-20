import time
import jwt  # PyJWT, a transitive dep of the SDK
from fastapi.testclient import TestClient

from app.main import app
from app.db import init_db
from app.installs import upsert_install, InstallRecord

client = TestClient(app)
SECRET = "install-secret"
SLUG = "my-addon"  # must match settings.addon_slug default


def setup_function():
    init_db()
    upsert_install(InstallRecord(15, 42, SECRET, "tok", []))


def _token(page_id: str) -> str:
    claims = {
        "iss": "23bisnis.com",
        "aud": SLUG,
        "tenant_id": 42,
        "install_id": 15,
        "user_id": 7,
        "user_role": "admin",
        "page_id": page_id,
        "context": {},
        "exp": int(time.time()) + 300,
    }
    return jwt.encode(claims, SECRET, algorithm="HS256")


def test_iframe_page_renders_with_valid_jwt():
    r = client.get("/ui/accounts", params={"jwt": _token("accounts")})
    assert r.status_code == 200
    assert "Accounts" in r.text


def test_iframe_page_rejects_missing_jwt():
    r = client.get("/ui/accounts")
    assert r.status_code == 401


def test_iframe_unknown_page_404():
    r = client.get("/ui/does-not-exist", params={"jwt": _token("does-not-exist")})
    assert r.status_code == 404
