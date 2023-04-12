from pydantic import BaseModel
from typing import Optional


class OrderBase(BaseModel):
    customer_id: int
    comment: Optional[str]


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    id: int
    status:bool
