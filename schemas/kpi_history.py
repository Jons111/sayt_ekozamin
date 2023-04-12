from pydantic import BaseModel
from typing import Optional


from pydantic.datetime_parse import date


class Kpi_HistoryBase(BaseModel):
    money: int
    type: str
    order_id: int
    comment: Optional[str]


class Kpi_HistoryCreate(Kpi_HistoryBase):
      return_date : date
    


class Kpi_HistoryUpdate(Kpi_HistoryBase):
    id: int
    status: bool