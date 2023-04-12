from fastapi import HTTPException


from functions.trades import one_trade
from functions.users import one_user, update_user_salary
from models.expenses import Expenses

from utils.pagination import pagination


def all_expenses(search, status,source_id, page, limit, db):
	if search:
		search_formatted = "%{}%".format(search)
		search_filter = Expenses.money.like(search_formatted)
	else:
		search_filter = Expenses.id > 0
	if status in [True, False]:
		status_filter = Expenses.status == status
	else:
		status_filter = Expenses.status.in_([True, False])
	
	if source_id:
		source_id_filter = Expenses.source_id == source_id
	else:
		source_id_filter = Expenses.id > 0
	
	expenses = db.query(Expenses).filter(search_filter, status_filter,source_id_filter).order_by(Expenses.id.desc())
	if page and limit:
		return pagination(expenses, page, limit)
	else:
		return expenses.all()


def one_expense(id, db):
	return db.query(Expenses).filter(Expenses.id == id).first()


def create_expense(form,cur_user, db):
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	
	if one_user(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	user=one_user(id=cur_user.id, db=db)
	
	
	updated_salary=user.salary - form.money
	update_user_salary(id=cur_user.id, salary=updated_salary, db=db)
	new_expense_db = Expenses(
		money=form.money,
		type=form.type,
		source_id=form.source_id,
		source=form.source,
		user_id=cur_user.id,
	
	)
	db.add(new_expense_db)
	db.commit()
	db.refresh(new_expense_db)
	return new_expense_db


def update_expense(form,cur_user, db):
	if one_expense(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli expense mavjud emas")
	
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	if one_trade(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	
	db.query(Expenses).filter(Expenses.id == form.id).update({
		Expenses.money: form.money,
		Expenses.type: form.type,
		Expenses.source_id: form.source_id,
		Expenses.source: form.source,
		Expenses.user_id: cur_user.id,
		Expenses.status: form.status
	})
	db.commit()
	return one_expense(form.id, db)


def expense_delete(id, db):
	if one_expense(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli expense mavjud emas")
	db.query(Expenses).filter(Expenses.id == id).update({
		Expenses.status: False,
		})
	db.commit()
	return {"date":"Ma'lumot o'chirildi !"}