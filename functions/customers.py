
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import joinedload
from starlette import status

from models.orders import Orders
from models.phones import Phones
from models.users import Users
from models.customers import Customers

from utils.pagination import pagination


def all_customers(search, status, user_id, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Customers.name.like(search_formatted) | Customers.address.like(
			search_formatted) | Customers.address.like(search_formatted)
	else:
		search_filter=Customers.id > 0
	if status in [True, False]:
		status_filter=Customers.status == status
	else:
		status_filter=Customers.status.in_([True, False])
	
	if user_id:
		user_id_filter=Customers.user_id == user_id
	else:
		user_id_filter=Users.id > 0
	
	customers=db.query(Customers).options(
		joinedload(Customers.phones).load_only(Phones.number),
		joinedload(Customers.orders).load_only(Orders.customer_id)).filter(search_filter, status_filter,
	                                                                  user_id_filter).order_by(Customers.id.desc())
	
	if page and limit:
		return pagination(customers, page, limit)
	else:
		return customers.all()


def one_customer(id, db):
	return db.query(Customers).options(
		joinedload(Customers.phones).load_only(Phones.number)).filter(Customers.id == id).first()


def create_customer(form, user, db):
	try:
		new_customer_db=Customers(
			name=form.name,
			address=form.address,
			comment=form.comment,
			user_id=user.id, )
		db.add(new_customer_db)
		db.commit()
		db.refresh(new_customer_db)
		if new_customer_db:
			raise HTTPException(status_code=status.HTTP_201_CREATED, detail='Qo`shildi')
		else:
			raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=user)

	except ValidationError as e:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e)


def update_customer(form,user, db):
	if one_customer(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli mijoz mavjud emas")
	
	db.query(Customers).options(
		joinedload(Customers.phones).load_only(Phones.number, Phones.comment)).filter(Customers.id == form.id).update({
		Customers.name: form.name,
		Customers.address: form.address,
		Customers.status: form.status,
		Customers.comment: form.comment,
		Customers.user_id: user.id,
		
	})
	db.commit()
	return one_customer(form.id, db)


def customer_delete(id, user,db):
	if one_customer(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli customer mavjud emas")
	db.query(Customers).filter(Customers.id == id).update({
		Customers.status: False,
		Customers.user_id:user.id
	})
	db.commit()
	return {"date": "Customer o'chirildi !"}
