from fastapi import APIRouter, status

from .schemas import (
    Item,
    ItemRead,
    ItemCreate,
)
from .storage import storage

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemRead])
def get_items() -> list[Item]:
    return storage.get()


@router.post(
    "/",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_item(item: ItemCreate) -> Item:
    return storage.add(item)
