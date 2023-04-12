
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.expenses import one_expense, all_expenses, update_expense, create_expense, expense_delete
from schemas.expenses import *

router_expense = APIRouter()



@router_expense.post('/add', )
def add_expense(form: ExpenseCreate, db: Session = Depends(get_db),current_user: ExpenseBase = Depends(get_current_active_user) ) : #current_user: CustomerBase = Depends(get_current_active_user)
    if create_expense(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_expense.get('/',  status_code = 200)
def get_expenses(search: str = None, status: bool = True, id: int = 0,source_id:int=0, page: int = 1, limit: int = 25, db: Session = Depends(get_db), ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_expense(id, db)
    else :
        return all_expenses(search,status,source_id, page, limit, db,)


@router_expense.put("/update")
def expense_update(form: ExpenseUpdate, db: Session = Depends(get_db),current_user: ExpenseBase = Depends(get_current_active_user)) :
    if update_expense(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

@router_expense.delete('/{id}',  status_code = 200)
def delete_expense(id: int = 0,db: Session = Depends(get_db),current_user: ExpenseBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return expense_delete(id,current_user, db)
    
    