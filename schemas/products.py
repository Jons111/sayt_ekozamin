
from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    birlik:str
    comment: Optional[str]
    price: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int
    status:bool