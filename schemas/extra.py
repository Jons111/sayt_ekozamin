from pydantic import BaseModel



class ExtraBase(BaseModel):
	money: int
	type: str
	source: str


class ExtraCreate(ExtraBase):
	source_id: int
	comment: str = None
	


class ExtraUpdate(ExtraBase):
	id: int
	source_id: int
	status:bool
