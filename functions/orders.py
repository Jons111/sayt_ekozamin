from fastapi import HTTPException
from pydantic.datetime_parse import date
from sqlalchemy import and_,cast,Date,func
from sqlalchemy.orm import joinedload

from functions.customers import one_customer
from functions.users import one_user
from models.customers import Customers
from models.kpi_history import Kpi_History

from models.orders import Orders

from utils.pagination import pagination


def all_orders(search, status,start_date,end_date, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Orders.comment.like(search_formatted)
	else:
		search_filter=Orders.id > 0
	if status in [True, False]:
		status_filter=Orders.status == status
	else:
		status_filter=Orders.status.in_([True, False])
	
	if start_date is None:
		start_date=date.min
	
	if not end_date:
		end_date=date.today()
	
	
	end_date = end_date[:-1] + str(int(end_date[-1])+1)
	
	orders=db.query(Orders).options(
		joinedload(Orders.customer).load_only(Customers.name)).filter(Orders.date <= end_date).filter(Orders.date >= start_date).filter(search_filter,status_filter).order_by(Orders.id.desc())
	
	if page and limit:
		return pagination(orders, page, limit)
	else:
		return orders.all()


def one_order(id, db):
	data=db.query(Orders).options(
		joinedload(Orders.customer).load_only(Customers.name)).filter(Orders.id == id).first()
	 
	return data


def create_order(form,user, db):
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	
	if one_customer(form.customer_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli mijoz mavjud emas")
	
	new_order_db=Orders(
		customer_id=form.customer_id,
		comment=form.comment,
		user_id=user.id,
	
	)
	db.add(new_order_db)
	db.commit()
	db.refresh(new_order_db)
	return new_order_db


def update_order(form,user, db):
	if one_order(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	db.query(Orders).filter(Orders.id == form.id).update({
		Orders.id: form.id,
		Orders.customer_id: form.customer_id,
		Orders.status: form.status,
		Orders.comment: form.comment,
		Orders.user_id: user.id
	})
	db.commit()
	return one_order(form.id, db)


def update_order_status(order_id, user_id, db):
	if one_order(order_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {order_id} raqamli order mavjud emas")
	if one_user(user_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {user_id} raqamli user mavjud emas")
	
	db.query(Orders).filter(Orders.id == order_id).update({
		Orders.status: False,
		
	})
	db.commit()
	return one_order(order_id, db)



def order_delete(id,user, db):
	if one_order(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Orders).filter(Orders.id == id).update({
		Orders.status: False,
		Orders.user_id:user.id
		})
	db.commit()
	return {"date":"Ma'lumot o'chirildi !"}