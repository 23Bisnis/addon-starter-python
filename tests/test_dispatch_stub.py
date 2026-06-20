import json
from fastapi.testclient import TestClient

from app.main import app
from app.db import init_db
from app.installs import upsert_install, InstallRecord

client = TestClient(app)
SECRET = "install-secret"


def setup_function():
    init_db()
    upsert_install(InstallRecord(15, 42, SECRET, "tok", ["supplier.dispatch"]))


def test_dispatch_stub_returns_failed_definitive(signer):
    payload = {
        "ref_id": "trx-1",
        "tenant_id": "42",
        "install_id": "15",
        "sku": "DGP-TEST",
        "destination": "081234567890",
        "amount_idr": 50000,
    }
    body = json.dumps(payload).encode()
    headers = signer(SECRET, body)
    r = client.post("/dispatch", content=body, headers=headers)
    assert r.status_code == 200
    out = r.json()
    assert out["outcome"] == "failed_definitive"
    assert "not implemented" in (out.get("message") or "").lower()


def test_dispatch_rejects_bad_signature(signer):
    body = b'{"ref_id":"x","install_id":"15"}'
    headers = signer("wrong-secret", body)
    r = client.post("/dispatch", content=body, headers=headers)
    assert r.status_code == 401
