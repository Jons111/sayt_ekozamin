from fastapi import HTTPException

from functions.users import one_user
from models.products import Products
from utils.pagination import pagination


def all_products(search, status, page, limit, db):
	if search:
		search_formatted = "%{}%".format(search)
		search_filter = Products.name.like(search_formatted) | Products.birlik.like(
			search_formatted) | Products.price.like(search_formatted)
	else:
		search_filter = Products.id > 0
	if status in [True, False]:
		status_filter = Products.status == status
	else:
		status_filter = Products.status.in_([True, False])
	
	products = db.query(Products).filter(search_filter, status_filter).order_by(Products.name.asc())
	if page and limit:
		return pagination(products, page, limit)
	else:
		return products.all()


def one_product(id, db):
	return db.query(Products).filter(Products.id == id).first()


def create_product(form,user, db):
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	new_product_db = Products(
		name=form.name,
		birlik=form.birlik,
		price=form.price,
		comment=form.comment,
		user_id=user.id,
	
	)
	db.add(new_product_db)
	db.commit()
	db.refresh(new_product_db)
	return new_product_db


def update_product(form,user, db):
	if one_product(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	db.query(Products).filter(Products.id == form.id).update({
		Products.name: form.name,
		Products.birlik: form.birlik,
		Products.price: form.price,
		Products.status: form.status,
		Products.comment: form.comment,
		Products.user_id: user.id,
	})
	db.commit()
	return one_product(form.id, db)

def product_delete(id,user, db):
	if one_product(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")
	db.query(Products).filter(Products.id == id).update({
		Products.status: False,
		Products.user_id:user.id
		})
	db.commit()
	return {"date":"Mahsulot o'chirildi !"}