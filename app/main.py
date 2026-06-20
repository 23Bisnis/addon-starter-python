from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="addon-starter-python", lifespan=lifespan)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


from fastapi.staticfiles import StaticFiles  # noqa: E402
import pathlib  # noqa: E402
from app.platform.oauth import router as oauth_router  # noqa: E402
from app.dispatch import router as dispatch_router  # noqa: E402
from app.ui import router as ui_router  # noqa: E402

app.include_router(oauth_router)
app.include_router(dispatch_router)
app.include_router(ui_router)
app.mount(
    "/static",
    StaticFiles(directory=str(pathlib.Path(__file__).parent / "ui" / "static")),
    name="static",
)
