from pydantic import BaseModel


class ExpenseBase(BaseModel):
    money: int
    type: str
    source: str


class ExpenseCreate(ExpenseBase):
   
    source_id: int


class ExpenseUpdate(ExpenseBase):
    id: int
    source_id: int
    status:bool
