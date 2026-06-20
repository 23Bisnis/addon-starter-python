import json
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from addon_sdk_23bisnis import AddonVerificationError
from app.installs import get_install
from app.platform.sig import verify_dispatch

router = APIRouter()


def _install_id_from_body(raw: bytes) -> int | None:
    try:
        return int(json.loads(raw).get("install_id"))
    except (ValueError, TypeError, json.JSONDecodeError):
        return None


@router.post("/dispatch")
async def dispatch(request: Request) -> JSONResponse:
    raw = await request.body()
    install_id = _install_id_from_body(raw)
    install = get_install(install_id) if install_id is not None else None
    if install is None:
        return JSONResponse(status_code=401, content={"outcome": "dispatch_failed", "message": "unknown install"})
    try:
        verify_dispatch(secret=install.signing_secret, body=raw, headers=request.headers)
    except AddonVerificationError:
        return JSONResponse(status_code=401, content={"outcome": "dispatch_failed", "message": "bad signature"})

    # STUB — a real addon fills this in (see digipos-addon).
    return JSONResponse(
        status_code=200,
        content={"outcome": "failed_definitive", "message": "dispatch not implemented in starter template"},
    )
