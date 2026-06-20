import hashlib
import hmac
from app.callback import build_callback_request


def test_build_callback_signs_shared_canonical():
    req = build_callback_request(
        platform_base_url="https://api.x",
        slug="my-addon",
        install_id=15,
        secret="sek",
        ref_id="trx-1",
        outcome="success",
        supplier_ref="DGP-9",
    )
    assert req["url"] == "https://api.x/api/v2/addons/callback/my-addon/15"
    body = req["body"]
    h = req["headers"]
    ts = h["X-Platform-Timestamp"]
    nonce = h["X-Platform-Nonce"]
    msg = ts.encode() + b"\n" + nonce.encode() + b"\n" + body
    expected = "hmac_sha256=" + hmac.new(b"sek", msg, hashlib.sha256).hexdigest()
    assert h["X-Platform-Signature"] == expected
