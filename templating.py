from config import BASE_DIR

from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)
