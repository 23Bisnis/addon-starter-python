import hashlib
import hmac
import json
import time
import uuid


def build_callback_request(
    *,
    platform_base_url: str,
    slug: str,
    install_id: int,
    secret: str,
    ref_id: str,
    outcome: str,
    supplier_ref: str | None = None,
    raw: dict | None = None,
) -> dict:
    """Build the signed pending->terminal callback request (caller sends it via httpx)."""
    payload = {"ref_id": ref_id, "outcome": outcome}
    if supplier_ref is not None:
        payload["supplier_ref"] = supplier_ref
    if raw is not None:
        payload["raw"] = raw
    body = json.dumps(payload).encode()
    ts = str(int(time.time()))
    nonce = str(uuid.uuid4())
    msg = ts.encode() + b"\n" + nonce.encode() + b"\n" + body
    sig = "hmac_sha256=" + hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()
    return {
        "url": f"{platform_base_url}/api/v2/addons/callback/{slug}/{install_id}",
        "body": body,
        "headers": {
            "Content-Type": "application/json",
            "X-Platform-Signature": sig,
            "X-Platform-Timestamp": ts,
            "X-Platform-Nonce": nonce,
        },
    }
