
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.users import one_user, all_users, update_user, create_user, user_delete,user_current
from schemas.users import UserBase,UserCreate,UserUpdate

router_user = APIRouter()



@router_user.post('/add', )
def add_user(form: UserCreate, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_active_user) ) : #
    if create_user(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_user.get('/',  status_code = 200)
def get_users(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_user(id, db)
    else :
        return all_users(search, status,roll, page, limit, db)

@router_user.get('/user',  status_code = 200)
def get_user_current(db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if current_user:
        return user_current(current_user, db)


@router_user.put("/update")
def user_update(form: UserUpdate, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_active_user)) :
    if update_user(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_user.delete('/{id}',  status_code = 200)
def delete_user(id: int = 0,db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return user_delete(id,current_user, db)