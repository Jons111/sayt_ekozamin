
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.kpi_history import one_history,all_history,create_history,update_history
from schemas.kpi_history import *

router_kpi_history = APIRouter()

@router_kpi_history.post('/add', )
def add_kpi(form: Kpi_HistoryCreate, db: Session = Depends(get_db),current_user: Kpi_HistoryBase = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
	
	if create_history(form, current_user,db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_kpi_history.get('/',  status_code = 200)
def get_kpis(search: str = None, status: bool = True, id: int = 0,source_id:int=0, page: int = 1,
             limit: int = 25, db: Session = Depends(get_db),current_user: Kpi_HistoryBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_history(id, db)
    else :
        return all_history(search,status,source_id, page, limit, db,)


@router_kpi_history.put("/update")
def kpi_history_update(form: Kpi_HistoryUpdate, db: Session = Depends(get_db),current_user: Kpi_HistoryBase = Depends(get_current_active_user)) :
    if update_history(form,current_user,  db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")
