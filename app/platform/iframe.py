from fastapi import HTTPException, Request

from addon_sdk_23bisnis import verify_iframe_token, IframeContext, AddonVerificationError
from app.config import settings
from app.installs import get_install


def require_iframe_context(request: Request) -> IframeContext:
    token = request.query_params.get("jwt")
    if not token:
        raise HTTPException(status_code=401, detail="missing jwt")
    # The JWT is HS256-signed with the per-install signing secret. Decode the install_id
    # from the unverified claims first (only to look up the secret), then fully verify.
    import jwt as _jwt

    try:
        unsafe = _jwt.decode(token, options={"verify_signature": False})
        install = get_install(int(unsafe["install_id"]))
    except Exception:
        raise HTTPException(status_code=401, detail="bad token")
    if install is None:
        raise HTTPException(status_code=401, detail="unknown install")
    try:
        return verify_iframe_token(
            token=token, secret=install.signing_secret, addon_slug=settings.addon_slug
        )
    except AddonVerificationError:
        raise HTTPException(status_code=401, detail="invalid iframe token")
