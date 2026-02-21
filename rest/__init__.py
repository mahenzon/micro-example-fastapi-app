from fastapi import APIRouter

from .items import router as items_router
from .main import router as main_router


router = APIRouter()
router.include_router(main_router)
router.include_router(items_router)
