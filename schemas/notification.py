from pydantic import BaseModel


class NotificationBase(BaseModel):
    money: int
    type: str
    source: str
    source_id: int


class NotificationCreate(NotificationBase):
      pass


class NotificationUpdate(NotificationBase):
    id: int
    status: bool
