from fastapi import FastAPI, Request
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
    get_redoc_html,
)
from fastapi.staticfiles import StaticFiles

from config import BASE_DIR
from rest import router

STATIC_PATH = BASE_DIR / "static"

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)
app.mount(
    "/static",
    StaticFiles(directory=STATIC_PATH),
    name="static",
)
app.include_router(router)

#


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=str(
            request.url_for(
                "static",
                path="/js/swagger-ui-bundle.js",
            ),
        ),
        swagger_css_url=str(
            request.url_for(
                "static",
                path="/css/swagger-ui.css",
            ),
        ),
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html(request: Request):
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url=str(
            request.url_for(
                "static",
                path="/js/redoc.standalone.js",
            ),
        ),
    )
