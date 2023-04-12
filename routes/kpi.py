
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.kpi import one_kpi, all_kpis, create_kpi, update_kpi, kpi_delete
from schemas.kpi import *

router_kpi = APIRouter()



@router_kpi.post('/add', )
def add_kpi(form: KpiCreate, db: Session = Depends(get_db),current_user: KpiBase = Depends(get_current_active_user) ) : #current_user: CustomerBase = Depends(get_current_active_user)
    if create_kpi(form, current_user,db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_kpi.get('/',  status_code = 200)
def get_kpis(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25, db: Session = Depends(get_db), current_user: KpiBase = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_kpi(id, db)
    else :
        return all_kpis(search,status, page, limit, db,)


@router_kpi.put("/update")
def kpi_update(form: KpiUpdate, db: Session = Depends(get_db),current_user: KpiBase = Depends(get_current_active_user)) :
    if update_kpi(form,current_user,  db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_kpi.delete('/{id}',  status_code = 200)
def delete_kpi(id: int = 0,db: Session = Depends(get_db), current_user: KpiBase = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return kpi_delete(id, current_user,db)
    
    
