from pydantic import BaseModel


class NasiyaBase(BaseModel):
    money: int
    


class NasiyaCreate(NasiyaBase):
    customer_id: int
    order_id: int


class NasiyaUpdate(NasiyaBase):
    id: int
    order_id: int
    customer_id: int
    status:bool
