

from fastapi import APIRouter, Depends, HTTPException
from pydantic.datetime_parse import datetime,date

from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.orders import one_order,all_orders,create_order,update_order
from schemas.orders import *

router_order = APIRouter()



@router_order.post('/add', )
def add_order(form: OrderCreate, db: Session = Depends(get_db),current_user: OrderBase = Depends(get_current_active_user) ) : #current_user: CustomerBase = Depends(get_current_active_user)
	if create_order(form,current_user, db) :
		raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_order.get('/',  status_code = 200)
def get_orders(search: str = None, status: bool = True, id: int = 0, page: int = 1,start_date=date.min, end_date = date.today(), limit: int = 25, db: Session = Depends(get_db),current_user: OrderBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
	if not id:
		
		return all_orders(search=search,status=status, page=page, limit=limit, db=db,start_date=start_date,end_date = end_date)
	else :
		return one_order(id, db)


@router_order.put("/update")
def order_update(form: OrderUpdate, db: Session = Depends(get_db),current_user: OrderBase = Depends(get_current_active_user)) :
	if update_order(form, current_user, db) :
		raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

