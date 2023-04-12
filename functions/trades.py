from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.orders import one_order, all_orders
from functions.products import one_product
from functions.users import one_user

from models.products import Products
from models.trades import Trades

from utils.pagination import pagination


def all_trades(search, status, order_id, page, limit, db):
	if search:
		search_formatted = "%{}%".format(search)
		search_filter = Trades.price.like(search_formatted) | Trades.quantity.like(search_formatted)
	else:
		search_filter = Trades.id > 0
	if status in [True, False]:
		status_filter = Trades.status == status
	else:
		status_filter = Trades.status.in_([True, False])
	
	if order_id:
		order_filter = Trades.order_id == order_id
	else:
		order_filter = Trades.order_id > 0
	
	trades = db.query(Trades).options(
        joinedload(Trades.products).load_only(Products.name,Products.birlik,Products.price)).filter(search_filter, status_filter, order_filter).order_by(Trades.id.desc())
	
	
	if page and limit:
		return pagination(trades, page, limit)
	else:
		return trades.all()


def one_trade(id, db):
	return db.query(Trades).options(
        joinedload(Trades.products).load_only(Products.name,Products.birlik,Products.price)).filter(Trades.id == id).first()


def create_trade(form, user,db):
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	
	if one_product(form.product_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")
	
	if one_order(form.order_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli order mavjud emas")
	
	new_trade_db = Trades(
		quantity=form.quantity,
		product_id=form.product_id,
		user_id=user.id,
		order_id=form.order_id,
	
	)
	
	db.add(new_trade_db)
	db.commit()
	db.refresh(new_trade_db)
	return new_trade_db


def update_trade(form, user,db):
	if one_trade(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	if one_product(form.product_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")
	
	if one_order(form.order_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli order mavjud emas")
	
	db.query(Trades).filter(Trades.id == form.id).update({
		Trades.id: form.id,
		Trades.product_id: form.product_id,
		Trades.status: form.status,
		Trades.quantity: form.quantity,
		Trades.user_id:user	})
	db.commit()
	return one_trade(form.id, db)


def filter_trades(order_id, db, status=True):
	if status in [True, False]:
		status_filter = Trades.status == status
	else:
		status_filter = Trades.id > 0
	
	if order_id:
		order_filter = Trades.order_id == order_id
	else:
		order_filter = Trades.id > 0
	
	users = db.query(Trades).filter(status_filter, order_filter).order_by(Trades.id.desc())
	
	return users.all()


def get_order_id_from_trades(id,user_id, db):
	if one_order(id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli order mavjud emas")
	if one_user(user_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {user_id} raqamli user mavjud emas")
	
	orders  = filter_trades(order_id=id,db=db)
	
	
	summa = 0
	for order in orders:
		product=one_product(id=order.product_id, db=db)
		summa += product.price * order.quantity
		
	return {"money":summa}


def get_deadline_from_trades(order_id,user_id,db):
	if one_order(order_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {order_id} raqamli order mavjud emas")
	if one_user(user_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {user_id} raqamli user mavjud emas")
	
	