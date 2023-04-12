

from fastapi import HTTPException

from sqlalchemy.orm import Session, joinedload


from functions.customers import one_customer
from functions.users import one_user
from models.phones import Phones
from models.customers import Customers

from utils.pagination import pagination


def get_all_phones(search, customer_id, status, page, limit, db):
	"""return a list of all phones"""
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Phones.number.like(search_formatted) | Phones.comment.like(search_formatted)
	else:
		search_filter=Phones.id > 0
	
	if customer_id:
		source_filter=Phones.source_id == customer_id
	else:
		source_filter=Phones.id > 0
	
	if status in [True, False]:
		status_filter=Phones.status == status
	else:
		status_filter=Phones.id > 0
	
	phones=db.query(Phones).options(
		joinedload(Phones.owner).load_only(Customers.name)).filter(search_filter, source_filter,
	                                                               status_filter).order_by(Phones.id.desc())
	if page and limit:
		return pagination(phones, page, limit)
	else:
		return phones.all()


def one_phone(id, db):
	"""returns a phone that matches the id"""
	
	return db.query(Phones).options(
		joinedload(Phones.owner).load_only(Customers.name)).filter(Phones.id == id).first()


def create_phone(form, user,db):
	phone_verification=db.query(Phones).filter(Phones.number == form.number).first()
	if phone_verification:
		raise HTTPException(status_code=400, detail="Bunday telefon raqam mavjud")
	
	if one_customer(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli customer mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	new_phone_db=Phones(
		number=form.number,
		source_id=form.source_id,
		comment=form.comment,
		user_id=user.id,
	)
	db.add(new_phone_db)
	db.commit()
	db.refresh(new_phone_db)
	return new_phone_db


def update_phone(form,user, db):
	if one_phone(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli telefon raqam mavjud emas")
	phone_verification=db.query(Phones).filter(Phones.number == form.number, Phones.source_id == form.source_id).first()
	if phone_verification and phone_verification.id != form.id:
		raise HTTPException(status_code=400, detail="Bunday telefon raqam mavjud")
	db.query(Phones).filter(Phones.id == form.id).update({
		Phones.number: form.number,
		Phones.comment: form.comment,
		Phones.user_id: user.id
	})
	db.commit()
	return one_phone(form.id, db)


def phone_delete(id,user, db):
	if one_phone(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Phones).filter(Phones.id == id).update({
		Phones.status: False,
		Phones.user_id:user.id
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}
