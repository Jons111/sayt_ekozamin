
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.incomes import one_income,all_incomes,create_income,update_income
from schemas.incomes import *

router_income = APIRouter()



@router_income.post('/add', )
def add_income(form: IncomeCreate, db: Session = Depends(get_db),current_user: IncomeBase = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if create_income(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")



@router_income.get('/',  status_code = 200)
def get_incomes(search: str = None, status: bool = True, id: int = 0,order_id:int = 0, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: IncomeBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_income(id, db)
    else :
        return all_incomes(search,status,order_id, page, limit, db,)


@router_income.put("/update")
def income_update(form: IncomeUpdate, db: Session = Depends(get_db),current_user: IncomeBase = Depends(get_current_active_user)) :
    if update_income(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

