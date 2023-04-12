
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.users import Users

from routes.auth import get_password_hash
from utils.pagination import pagination


def all_users(search, status, roll, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Users.name.like(search_formatted) | Users.number.like(search_formatted) | Users.username.like(
			search_formatted) | Users.roll.like(search_formatted)
	else:
		search_filter=Users.id > 0
	if status in [True, False]:
		status_filter=Users.status == status
	else:
		status_filter=Users.id > 0
	
	if roll:
		roll_filter=Users.roll == roll
	else:
		roll_filter=Users.id > 0
	
	users=db.query(Users).filter(search_filter, status_filter, roll_filter).order_by(Users.name.asc())
	if page and limit:
		return pagination(users, page, limit)
	else:
		return users.all()


def one_user(id, db):
	return db.query(Users).filter(Users.id == id).first()

def user_current(user, db):
	return db.query(Users).filter(Users.id == user.id).first()

def create_user(form, user, db):
	user_verification=db.query(Users).filter(Users.username == form.username).first()
	if user_verification:
		raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
	number_verification=db.query(Users).filter(Users.number == form.number).first()
	if number_verification:
		raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")
	if user.roll == "admin":
		allowed_rolls=["admin", "seller", "trade_admin", "worker"]
	elif user.roll == "trade_admin":
		allowed_rolls=["worker", 'seller']
	elif user.roll == "seller":
		allowed_rolls=["worker"]
	else:
		allowed_rolls=[]
	if form.roll not in allowed_rolls:
		raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
	#
	new_user_db=Users(
		name=form.name,
		username=form.username,
		number=form.number,
		password=get_password_hash(form.password),
		roll=form.roll,
		status=form.status,
	
	)
	db.add(new_user_db)
	db.commit()
	db.refresh(new_user_db)
	return new_user_db


def update_user(form, user, db):
	if one_user(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	user_verification=db.query(Users).filter(Users.username == form.username).first()
	if user_verification and user_verification.id != form.id:
		raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
	if user.roll == "admin":
		allowed_rolls=["admin", "seller", "seller_admin", "worker"]
	elif user.roll == "seller_admin":
		allowed_rolls=["worker", 'seller']
	elif user.roll == "seller":
		allowed_rolls=["worker"]
	else:
		allowed_rolls=[]
	if form.roll not in allowed_rolls:
		raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
	db.query(Users).filter(Users.id == form.id).update({
		Users.name: form.name,
		Users.username: form.username,
		Users.password: get_password_hash(form.password),
		Users.roll: form.roll,
		Users.status: form.status,
		Users.number: form.number,
		
	})
	db.commit()
	return one_user(form.id, db)


def update_user_salary(id, salary,db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")
	
	db.query(Users).filter(Users.id == id).update({
		Users.salary: salary,
		
	})
	db.commit()
	return one_user(id, db)


def update_user_balance(id, balance,db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")
	
	
	db.query(Users).filter(Users.id == id).update({
		Users.balance: balance,
		
	})
	db.commit()
	return one_user(id, db)


def filter_users(roll, db,status=True):
	if status in [True, False]:
		status_filter=Users.status == status
	else:
		status_filter=Users.id > 0
	
	if roll:
		roll_filter=Users.roll == roll
	else:
		roll_filter=Users.id > 0
	
	users=db.query(Users).filter(status_filter, roll_filter).order_by(Users.name.asc())
	
	return users.all()


def user_delete(id, db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Users).filter(Users.id == id).update({
		Users.status: False,
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}
