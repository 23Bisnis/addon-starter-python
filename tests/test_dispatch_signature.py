import pytest
from app.platform.sig import verify_dispatch
from addon_sdk_23bisnis import SignatureError

SECRET = "install-secret"


def test_verify_dispatch_accepts_valid_signature(signer):
    body = b'{"ref_id":"r1"}'
    headers = signer(SECRET, body)
    # Should not raise:
    verify_dispatch(secret=SECRET, body=body, headers=headers)


def test_verify_dispatch_rejects_tampered_body(signer):
    headers = signer(SECRET, b'{"ref_id":"r1"}')
    with pytest.raises(SignatureError):
        verify_dispatch(secret=SECRET, body=b'{"ref_id":"TAMPERED"}', headers=headers)


def test_verify_dispatch_rejects_replay(signer):
    from addon_sdk_23bisnis import ReplayError
    body = b"{}"
    headers = signer(SECRET, body)
    verify_dispatch(secret=SECRET, body=body, headers=headers)  # first use consumes the nonce
    with pytest.raises(ReplayError):
        verify_dispatch(secret=SECRET, body=body, headers=headers)


def test_verify_dispatch_rejects_missing_headers():
    from addon_sdk_23bisnis import AddonVerificationError
    with pytest.raises(AddonVerificationError):
        verify_dispatch(secret=SECRET, body=b"{}", headers={})
