from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from addon_sdk_23bisnis.generated import AuthenticatedClient
from addon_sdk_23bisnis.generated.api.oauth import oauth_exchange
from addon_sdk_23bisnis.generated.models import OauthExchangeBody

from app.config import settings
from app.installs import upsert_install, InstallRecord

router = APIRouter()


@router.get("/oauth/install", response_class=HTMLResponse)
def oauth_install(install_id: int, code: str) -> HTMLResponse:
    # Exchange the one-time code for per-install credentials.
    # The exchange authenticates via (code, client_secret) in the body; the bearer
    # token is not yet known, so construct the client with an empty token.
    client = AuthenticatedClient(base_url=settings.platform_base_url, token="")
    body = OauthExchangeBody(code=code, client_secret=settings.client_secret)
    result = oauth_exchange.sync(client=client, body=body)
    if result is None or result.data is None:
        raise HTTPException(status_code=400, detail="oauth exchange failed")
    creds = result.data
    upsert_install(
        InstallRecord(
            install_id=creds.install_id,
            tenant_id=creds.tenant_id,
            signing_secret=creds.signing_secret,
            oauth_token=creds.platform_oauth_token,
            scopes=list(creds.scopes_granted),
        )
    )
    return HTMLResponse("<h1>Addon installed</h1><p>You can close this window.</p>")
