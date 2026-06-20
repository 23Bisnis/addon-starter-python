from typing import Mapping

from addon_sdk_23bisnis import verify_signature
from app.nonce import get_nonce_store


def verify_dispatch(*, secret: str, body: bytes, headers: Mapping[str, str | None]) -> None:
    """Verify an incoming signed dispatch (shared canonical). Raises on failure.

    On failure raises AddonVerificationError (including its subclasses SignatureError,
    SkewError, ReplayError). Callers should catch AddonVerificationError, not just
    SignatureError. The SDK's verify_signature expects the signature exactly as the
    platform produces it, i.e. the full 'hmac_sha256=<hex>' header value — do not strip
    the prefix.
    """
    verify_signature(
        secret=secret,
        body=body,
        signature=headers.get("X-Platform-Signature") or "",
        timestamp=headers.get("X-Platform-Timestamp") or "",
        nonce=headers.get("X-Platform-Nonce") or "",
        store=get_nonce_store(),
    )
