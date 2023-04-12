
from pydantic import BaseModel



class TradeBase(BaseModel):
    product_id: int
    quantity: float
    


class TradeCreate(TradeBase):
     order_id: int


class TradeUpdate(TradeBase):
    id: int
    order_id: int
    status:bool
