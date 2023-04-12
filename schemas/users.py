
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    username: str
    roll: str
    status: bool


class UserCreate(UserBase):
    password: str
    number: str


class UserUpdate(UserBase):
    id: int
    password: str
    number: str


class UpdateUserBalance(BaseModel):
    id: int
    balance: float
    user_id: int

class UpdateUserSalary(BaseModel):
    id: int
    salary: float
    user_id: int
class UpdateUserSalaryBalance(BaseModel):
    id: int
    balance: int
    salary: int
    user_id: int

class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[str] = None
