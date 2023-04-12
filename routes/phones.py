
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from functions.phones import one_phone, get_all_phones, create_phone, update_phone, phone_delete
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)



from schemas.phones import *

router_phone = APIRouter()



@router_phone.post('/add', )
def phone_create(form: PhoneCreate, db: Session = Depends(get_db),current_user: PhoneCreate = Depends(get_current_active_user)) :
    if create_phone(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_phone.get('/',  status_code = 200)
def get_phones(search: str = None, customer_id: int = 0, status: bool = True, id: int = 0, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: PhoneCreate = Depends(get_current_active_user)) :
    if id :
        return one_phone(id, db)
    else :
        return get_all_phones(search, customer_id, status, page, limit, db)


@router_phone.put('/', status_code = 200,)
def phone_update(form: PhoneUpdate, db: Session = Depends(get_db),current_user: PhoneCreate = Depends(get_current_active_user)) :
    if update_phone(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")



@router_phone.delete('/{id}',  status_code = 200)
def delete_phone(id: int = 0,db: Session = Depends(get_db),current_user: PhoneCreate = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return phone_delete(id,current_user, db)
    
    
