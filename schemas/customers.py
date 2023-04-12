
from pydantic import BaseModel


class CustomerBase(BaseModel):
	name: str
	address: str



class CustomerCreate(CustomerBase):
	comment: str = None

class CustomerUpdate(CustomerBase):
	id: int
	status: bool
	comment: str = None
	

class CustomerOut(CustomerBase):
		id: int
		user_id: int
		status: bool
		comment: str = None
		phones : list = []

		class Config:
			orm_mode = True



