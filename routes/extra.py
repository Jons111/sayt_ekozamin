
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from functions.users import update_user_salary, one_user
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.extra import one_extra, all_extras, create_extra, update_extra, extra_delete
from schemas.extra import *

router_extra = APIRouter()



@router_extra.post('/add', )
def add_extra(form: ExtraCreate, db: Session = Depends(get_db),current_user: ExtraBase = Depends(get_current_active_user) ) : #current_user: CustomerBase = Depends(get_current_active_user)
    if create_extra(form,current_user, db) :
        if form.type == 'reward':
            user = one_user(id=form.source_id,db=db)
            updated_salary = user.salary+int(form.money)
            update_user_salary(id=form.source_id,salary=updated_salary,db=db)
            raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli amalga oshirildi")
        elif form.type=="fine":
            user = one_user(id=form.source_id, db=db)
            updated_salary = user.salary - int(form.money)
            update_user_salary(id=form.source_id, salary=updated_salary, db=db)
            raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli amalga oshirildi")
        else:
            raise HTTPException(status_code=200, detail=f"Bunday type mavjud emas!")

@router_extra.get('/',  status_code = 200)
def get_extras(search: str = None, status: bool = True, id: int = 0, source_id:int=0,page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: ExtraBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_extra(id, db)
    else :
        return all_extras(search,status,source_id, page, limit, db,)


@router_extra.put("/update")
def extra_update(form: ExtraUpdate, db: Session = Depends(get_db),current_user: ExtraBase = Depends(get_current_active_user)) :
    if update_extra(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_extra.delete('/{id}',  status_code = 200)
def delete_extra(id: int = 0,db: Session = Depends(get_db),current_user: ExtraBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return extra_delete(id,current_user, db)
    
    