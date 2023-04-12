from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.customers import one_customer
from functions.orders import one_order
from functions.trades import one_trade
from functions.users import one_user
from models.customers import Customers
from models.incomes import Incomes
from models.nasiya import Nasiya

from utils.pagination import pagination


def all_nasiya(search, status, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Nasiya.money.like(search_formatted)
	else:
		search_filter=Nasiya.id > 0
	if status in [True, False]:
		status_filter=Nasiya.status == status
	else:
		status_filter=Nasiya.status.in_([True, False])
	
	nasiya=db.query(Nasiya).filter(search_filter, status_filter).order_by(Nasiya.id.desc())
	if page and limit:
		return pagination(nasiya, page, limit)
	else:
		return nasiya.all()


def one_nasiya(id, db):
	return db.query(Nasiya).options(joinedload(Nasiya.customer).load_only(Customers.name)).filter(Nasiya.id == id).first()

def filter_nasiya(order_id, db):
	return db.query(Nasiya).options(joinedload(Nasiya.customer).load_only(Customers.name)).filter(Nasiya.order_id == order_id).first()

def create_nasiya(form,cur_user, db):
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	
	if one_trade(form.customer_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	new_nasiya_db=Nasiya(
		money=form.money,
		order_id=form.order_id,
		customer_id=form.customer_id,
		user_id=cur_user.id,
	
	)
	db.add(new_nasiya_db)
	db.commit()
	db.refresh(new_nasiya_db)
	return new_nasiya_db


def update_nasiya_status(id, user_id, db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")
	if one_user(user_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {user_id} raqamli user mavjud emas")
	
	db.query(Nasiya).filter(Nasiya.id == id).update({
		Nasiya.status: False,
		
	})
	db.commit()
	return one_nasiya(id, db)


def update_nasiya_status_via_order(order_id, db):
	
	db.query(Nasiya).filter(Nasiya.order_id == order_id).update({
		Nasiya.status: False,
		
	})
	db.commit()
	return filter_nasiya(order_id,db)


def update_nasiya(form,cur_user, db):
	if one_nasiya(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli nasiya mavjud emas")
	
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	if one_order(form.order_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	
	if one_customer(form.customer_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli customer mavjud emas")
	
	user_nasiya=one_nasiya(id=form.id, db=db)
	if form.money == user_nasiya.money:
		new_income_db=Incomes(
			money=form.money,
			type="Naqd",
			source_id=form.order_id,
			source="Trade",
			user_id=cur_user.id
		)
		db.add(new_income_db)
		db.commit()
		db.refresh(new_income_db)
		update_nasiya_status(id=form.id,user_id=cur_user.id,db=db)
		raise HTTPException(status_code=400, detail="Nasiya to'liq to'landi !")
	else:
		
		db.query(Nasiya).filter(Nasiya.id == form.id).update({
			Nasiya.money: form.money,
			Nasiya.customer_id: form.customer_id,
			Nasiya.order_id: form.order_id,
			Nasiya.user_id: cur_user.id,
			Nasiya.status: form.status
		})
		db.commit()
		return one_nasiya(form.id, db)

def nasiya_update_(order_id,money,db):
	db.query(Nasiya).filter(Nasiya.order_id == order_id).update({
		Nasiya.money: money,
		
	})
	db.commit()
	return filter_nasiya(order_id, db)
	
