
from pydantic import BaseModel
from typing import Optional


class PhoneBase(BaseModel):
    number: str
   


class PhoneCreate(PhoneBase):
    comment: Optional[str]
    source_id: int


class PhoneUpdate(PhoneBase):
    id: int
    comment: Optional[str]
    source_id: int


class PhoneOut(PhoneBase):
    id: int
    comment: Optional[str]
    source_id: int

    class Config:
        orm_mode = True
