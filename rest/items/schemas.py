import uuid
from uuid import UUID

from pydantic import BaseModel, constr, Field


class ItemBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    description: constr(min_length=1, max_length=300)


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: UUID


class Item(ItemBase):
    id: UUID = Field(default_factory=uuid.uuid7)
