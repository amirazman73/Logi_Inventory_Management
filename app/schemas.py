from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class StockCreate(BaseModel):
    item_id: int
    date_of_collection: Optional[date]
    quantity: int
    location: str
    pallet_id: Optional[int] = None
    status: Optional[str] = "active"


class StockUpdate(BaseModel):
    item_name: Optional[str] = None
    brand: Optional[str] = None
    date_of_collection: Optional[date] = None
    quantity: Optional[int] = None
    location: Optional[str] = None
    pallet_id: Optional[int] = None

class StockResponse(StockCreate):
    id: int

    class Config:
        orm_mode = True

class PalletCreate(BaseModel):
    pallet_code: str
    created_at: date
    item_ids: List[int]  # list of stock item IDs to assign to this pallet

class PalletResponse(BaseModel):
    id: int
    pallet_code: str
    created_at: date
    item_ids: List[int]

    class Config:
        orm_mode = True

class StockResponse(BaseModel):
    id: int
    item_id: int
    date_of_collection: Optional[date]
    quantity: int
    location: str
    pallet_id: Optional[int]
    status: str

    class Config:
        from_attributes = True  


class ItemCreate(BaseModel):
    name: str
    brand: str

class ItemResponse(ItemCreate):
    id: int
    class Config:
        from_attributes = True
