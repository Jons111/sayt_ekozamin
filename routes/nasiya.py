
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.nasiya import one_nasiya,all_nasiya,create_nasiya,update_nasiya
from schemas.nasiya import *

router_nasiya = APIRouter()



@router_nasiya.post('/add', )
def add_nasiya(form: NasiyaCreate, db: Session = Depends(get_db),current_user: NasiyaBase = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if create_nasiya(form,current_user,db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_nasiya.get('/',  status_code = 200)
def get_nasiya(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: NasiyaBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_nasiya(id, db)
    else :
        return all_nasiya(search,status, page, limit, db,)


@router_nasiya.put("/update")
def nasiya_update(form: NasiyaUpdate, db: Session = Depends(get_db),current_user: NasiyaBase = Depends(get_current_active_user)) :
    if update_nasiya(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

