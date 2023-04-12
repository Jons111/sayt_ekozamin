from datetime import datetime
import logging
from fastapi import HTTPException,WebSocket,WebSocketDisconnect
from sqlalchemy.orm import Session, joinedload
from models.kpi_history import Kpi_History
from functions.kpi import one_kpi, filter_kpi
from functions.nasiya import filter_nasiya, nasiya_update_,update_nasiya_status_via_order
from functions.trades import one_trade
from functions.users import one_user, update_user_salary, filter_users
from models.incomes import Incomes
from models.orders import Orders

from utils.pagination import pagination


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

def all_incomes(search, status,order_id, page, limit, db):
	if search:
		search_formatted = "%{}%".format(search)
		search_filter = Incomes.money.like(search_formatted)
	else:
		search_filter = Incomes.id > 0
	if status in [True, False]:
		status_filter = Incomes.status == status
	else:
		status_filter = Incomes.status.in_([True, False])
	
	if order_id:
		order_filter = Incomes.source_id==order_id
	else:
		order_filter  = Incomes.source_id>0
	
	incomes = db.query(Incomes).filter(search_filter, status_filter,order_filter).order_by(Incomes.id.desc())
	if page and limit:
		return pagination(incomes, page, limit)
	else:
		return incomes.all()


def one_income(id, db):

	return db.query(Incomes).filter(Incomes.id == id).first()


def create_income(form,cur_user, db):
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	
	if one_trade(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	new_income_db = Incomes(
		money=form.money,
		type=form.type,
		source_id=form.source_id,
		source="Trade",
		user_id=cur_user.id
	)
	db.add(new_income_db)
	db.commit()
	db.refresh(new_income_db)
	
	# async def heavy_data_processing(data: dict):
	# 	"""Some (fake) heavy data processing logic."""
	# 	await asyncio.sleep(2)
	# 	message_processed=data.get("message", "").upper()
	# 	return message_processed
	
	# Note that the verb is `websocket` here, not `get`, `post`, etc.
	# @app.websocket("/ws")
	# async def websocket_endpoint(websocket: WebSocket):
	# 	# Accept the connection from a client.
	# 	await websocket.accept()
	#
	# 	while True:
	# 		try:
	# 			# Receive the JSON data sent by a client.
	# 			data=await websocket.receive_json()
	# 			# Some (fake) heavey data processing logic.
	# 			message_processed=await heavy_data_processing(data)
	# 			# Send JSON data to the client.
	# 			await websocket.send_json(
	# 				{
	# 					"message": message_processed,
	# 					"time": datetime.now().strftime("%H:%M:%S"),
	# 				}
	# 			)
	# 		except WebSocketDisconnect:
	# 			logger.info("The connection is closed.")
	# 			break
	nasiya = filter_nasiya(order_id=form.source_id, db=db)
	if nasiya:
		user_kpi=one_kpi(id=cur_user.id, db=db)
		money=user_kpi.percentage * form.money / 100
		user=one_user(id=cur_user.id, db=db)
		updated_salary=user.salary + money
		update_user_salary(id=cur_user.id, salary=updated_salary, db=db)
	
		users=filter_users(roll='string', db=db)
		for worker in users:
				worker_kpi = filter_kpi(source_id=worker.id, db=db)
				money=worker_kpi.percentage * form.money / 100
				user=one_user(id=worker.id, db=db)
				updated_salary=user.salary + money
				update_user_salary(id=worker.id, salary=updated_salary, db=db)
		
		
		new_history_db=Kpi_History(
			money=money,
			type=form.type,
			order_id=form.source_id,
			comment='',
			user_id=cur_user.id,
		
		)
		db.add(new_history_db)
		db.commit()
		db.refresh(new_history_db)
		
		nasiya_money = nasiya.money - form.money
		if nasiya_money>0:
			nasiya_update_(order_id=form.source_id, money=nasiya_money, db=db)
		elif nasiya_money == 0:
			nasiya_update_(order_id=form.source_id, money=0, db=db)
			update_nasiya_status_via_order(order_id=form.source_id,db=db)
			return {"data":f"{form.source_id} id raqamli nasiya to'liq qoplandi!"}
		else:
			update_nasiya_status_via_order(order_id=form.source_id, db=db)
			return {"data":f"{form.source_id} id raqamli nasiyaga orticha {nasiya_money} so'm to'lov qilindi"}
	return new_income_db


def update_income(form,cur_user, db):
	if one_income(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli income mavjud emas")
	
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	if one_trade(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	
	db.query(Incomes).filter(Incomes.id == form.id).update({
		Incomes.money: form.money,
		Incomes.type: form.type,
		Incomes.source_id: form.source_id,
		Incomes.source: form.source,
		Incomes.user_id: cur_user.id,
		Incomes.status:form.status
	})
	db.commit()
	return one_income(form.id, db)
