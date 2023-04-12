from fastapi import HTTPException
from sqlalchemy.orm import Session

from functions.users import one_user, update_user,update_user_salary
from models.extra import Extra

from utils.pagination import pagination


def all_extras(search, status,source_id, page, limit, db):
	if search:
		search_formatted = "%{}%".format(search)
		search_filter = Extra.money.like(search_formatted)
	else:
		search_filter = Extra.id > 0
		
	if status in [True, False]:
		status_filter = Extra.status == status
	else:
		status_filter = Extra.status.in_([True, False])
	
	if source_id:
		source_id_filter = Extra.source_id==source_id
	else:
		source_id_filter = Extra.source_id > 0
	
	extras = db.query(Extra).filter(search_filter, status_filter,source_id_filter).order_by(Extra.id.desc())
	if page and limit:
		return pagination(extras, page, limit)
	else:
		return extras.all()


def one_extra(id, db):
	return db.query(Extra).filter(Extra.id == id).first()


def create_extra(form,cur_user, db):
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	
	if one_user(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")



	new_extra_db = Extra(
		money=form.money,
		type=form.type,
		source_id=form.source_id,
		source=form.source,
		user_id=cur_user.id,
		comment=form.comment
	
	)
	db.add(new_extra_db)
	db.commit()
	db.refresh(new_extra_db)
	return new_extra_db


def update_extra(form,cur_user,db):
	if one_extra(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli extra mavjud emas")
	
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	
	
	db.query(Extra).filter(Extra.id == form.id).update({
		Extra.money: form.money,
		Extra.type: form.type,
		Extra.source_id: form.source_id,
		Extra.source: form.source,
		Extra.user_id: cur_user.id,
		Extra.status: form.status
	})
	db.commit()
	return one_extra(form.id, db)


def extra_delete(id,cur_user, db):
	if one_extra(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Extra).filter(Extra.id == id).update({
		Extra.status: False,
		Extra.user_id:cur_user.id
		})
	db.commit()
	return {"date":"Ma'lumot o'chirildi !"}