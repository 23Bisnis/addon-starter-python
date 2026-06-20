# addon-starter-python

Starter template for building a 23bisnis platform addon (supplier adapter + admin UI) in Python,
built on [`23bisnis-addon-sdk`](https://github.com/23Bisnis/addon-sdk-python).

## What you get
- Signed dispatch endpoint (`POST /dispatch`) with HMAC verification — fill in your fulfillment logic.
- OAuth install handler (`GET /oauth/install`) that exchanges the one-time code for per-install creds.
- Admin-UI iframe pages (Accounts / Mapping / History) with JWT verification — fill in your UI.
- Pending→terminal callback helper for async outcomes.

## Run
    python -m venv .venv && . .venv/bin/activate
    pip install -e ".[dev]"   # if the SDK isn't on PyPI yet: pip install -e ../addon-sdk-python first
    cp .env.example .env       # set ADDON_SLUG + CLIENT_SECRET from the developer console
    uvicorn app.main:app --reload
    pytest -v

## Fill these in
- `app/dispatch.py` — translate `sku` → your upstream call, return one of
  `success | failed_definitive | pending | dispatch_failed`.
- `app/accounts.py`, `app/catalog.py` — your credential + catalog/mapping storage.
- `app/ui/templates/*.html` — your admin pages.
