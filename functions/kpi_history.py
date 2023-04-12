from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.incomes import create_income
from functions.kpi import one_kpi, filter_kpi
from functions.orders import update_order_status, one_order
from functions.trades import one_trade, get_order_id_from_trades, get_deadline_from_trades
from functions.users import one_user, update_user_salary, all_users, filter_users, update_user_balance
from models.incomes import Incomes
from models.kpi_history import Kpi_History
from models.nasiya import Nasiya
from models.orders import Orders
from routes.users import get_users
from schemas.kpi_history import Kpi_HistoryCreate,Kpi_HistoryBase
from utils.pagination import pagination


def all_history(search, status,source_id, page, limit, db):
	if search:
		search_formatted = "%{}%".format(search)
		search_filter = Kpi_History.money.like(search_formatted) | Kpi_History.trade_id.like(
			search_formatted) 
	else:
		search_filter = Kpi_History.id > 0
	if status in [True, False]:
		status_filter = Kpi_History.status == status
	else:
		status_filter = Kpi_History.status.in_([True, False])
	
	if source_id:
		source_id_filter = Kpi_History.source_id == source_id
	else:
		source_id_filter = Kpi_History.id > 0
	
	history = db.query(Kpi_History).filter(search_filter, status_filter,source_id_filter).order_by(Kpi_History.id.desc())

	if page and limit:
		return pagination(history, page, limit)
	else:
		return history.all()


def one_history(id, db):
	return db.query(Kpi_History).filter(Kpi_History.id == id).first()


def create_history(form,cur_user, db):
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

	if one_order(form.order_id,db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	
	
	# update user salary section
	user_kpi = one_kpi(id=cur_user.id,db=db)
	money = user_kpi.percentage*form.money/100
	user = one_user(id=cur_user.id,db=db)
	real_money = get_order_id_from_trades(id=form.order_id,user_id=cur_user.id,db=db).get('money')
	
	updated_salary=user.salary + money
	update_user_salary(id=cur_user.id, salary=updated_salary, db=db)
	users=filter_users(roll='string', db=db)
	for worker in users:
		worker_kpi=filter_kpi(source_id=worker.id, db=db)
		money=worker_kpi.percentage * form.money / 100
		user=one_user(id=worker.id, db=db)
		
		updated_salary=user.salary + money
		update_user_salary(id=worker.id, salary=updated_salary, db=db)
	
	if real_money == form.money:
		
		new_history_db=Kpi_History(
			money=money,
			type=form.type,
			order_id=form.order_id,
			comment=form.comment,
			user_id=cur_user.id,
		
		)
		db.add(new_history_db)
		db.commit()
		db.refresh(new_history_db)
		update_order_status(order_id=form.order_id, user_id=cur_user.id, db=db)
		
		
		
	elif real_money > form.money:
		nasiya = real_money - form.money
		updated_balance = user.balance + nasiya
		update_user_balance(id=cur_user.id, balance=updated_balance, db=db)
		users=filter_users(roll='string', db=db)
		for worker in users:
			worker_kpi=filter_kpi(source_id=worker.id, db=db)
			money=worker_kpi.percentage * nasiya / 100
			user=one_user(id=worker.id, db=db)
			updated_balance=user.balance + money
			update_user_balance(id=worker.id, balance=updated_balance, db=db)
		
		order = one_order(id=form.order_id,db=db)
		
		new_history_db=Nasiya(
			money=nasiya,
			order_id = form.order_id,
			customer_id = order.customer_id,
			deadline=form.return_date,
			user_id=cur_user.id,
		
		)
		db.add(new_history_db)
		db.commit()
		db.refresh(new_history_db)
		update_history_status(order_id=form.order_id, user_id=cur_user.id, db=db)
		
		
	else:
		extra = form.money - real_money
		raise HTTPException(status_code=400, detail=f"Ortiqcha to'lov qilindi {extra} so'm")
	
	new_income_db=Incomes(
		money=form.money,
		type=form.type,
		source_id=form.order_id,
		source="Trade",
		user_id=cur_user.id
	)
	
	db.add(new_income_db)
	db.commit()
	db.refresh(new_income_db)
	return new_income_db
	
		
	
	
	
	


def update_history(form,cur_user, db):
	if one_history(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo tarixi mavjud emas")
	
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	if one_trade(form.trade_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	
	
	db.query(Kpi_History).filter(Kpi_History.id == form.id).update({
		Kpi_History.money: form.money,
		Kpi_History.type: form.type,
		Kpi_History.trade_id: form.trade_id,
		Kpi_History.status: form.status,
		Kpi_History.comment: form.comment,
		Kpi_History.user_id: cur_user.id
	})
	db.commit()
	return one_history(form.id, db)


def update_history_status(order_id, user_id, db):
	if one_order(order_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {order_id} raqamli order mavjud emas")
	if one_user(user_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {user_id} raqamli user mavjud emas")
	
	db.query(Kpi_History).filter(Kpi_History.order_id == order_id).update({
		Kpi_History.status: False,
		
	})
	db.commit()
	return one_history(order_id, db)


