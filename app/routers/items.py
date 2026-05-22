from fastapi import APIRouter, HTTPException
from typing import List
from app.models.item import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])

# In-memory store — replace with a real DB in production
_items: dict[int, Item] = {
    1: Item(id=1, name="Widget", description="A useful widget", price=9.99),
    2: Item(id=2, name="Gadget", description="An even more useful gadget", price=24.99),
}
_next_id = 3


@router.get("", response_model=List[Item], summary="List all items")
async def list_items():
    return list(_items.values())


@router.get("/{item_id}", response_model=Item, summary="Get a single item")
async def get_item(item_id: int):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return _items[item_id]


@router.post("", response_model=Item, status_code=201, summary="Create an item")
async def create_item(payload: ItemCreate):
    global _next_id
    item = Item(id=_next_id, **payload.model_dump())
    _items[_next_id] = item
    _next_id += 1
    return item


@router.delete("/{item_id}", status_code=204, summary="Delete an item")
async def delete_item(item_id: int):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    del _items[item_id]
