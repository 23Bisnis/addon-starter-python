from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pathlib

from addon_sdk_23bisnis import IframeContext
from app.platform.iframe import require_iframe_context

router = APIRouter(prefix="/ui")
_templates = Jinja2Templates(directory=str(pathlib.Path(__file__).parent / "templates"))

_PAGES = {"accounts": "accounts.html", "mapping": "mapping.html", "history": "history.html"}


@router.get("/{page_id}", response_class=HTMLResponse)
def page(page_id: str, request: Request, ctx: IframeContext = Depends(require_iframe_context)):
    template = _PAGES.get(page_id)
    if template is None:
        raise HTTPException(status_code=404, detail="unknown page")
    return _templates.TemplateResponse(request=request, name=template, context={"ctx": ctx})
