from fastapi import Request, APIRouter

from templating import templates

router = APIRouter()


@router.get("/")
def home_page(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query=None,
    )
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "name": name,
            "docs_url": docs_url,
        },
    )
