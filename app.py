from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import BASE_DIR
from rest import router

STATIC_PATH = BASE_DIR / "static"

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=STATIC_PATH),
    name="static",
)
app.include_router(router)
