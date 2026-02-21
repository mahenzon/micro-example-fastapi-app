from collections import deque

from .schemas import Item, ItemCreate


class Storage:

    def __init__(self, max_items=100):
        self.items = deque(maxlen=max_items)

    def get(self) -> list[Item]:
        return list(self.items)

    def add(self, item_create: ItemCreate) -> Item:
        new_item = Item(**item_create.model_dump())
        self.items.append(new_item)
        return new_item


storage = Storage()
