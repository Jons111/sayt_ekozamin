from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.customers import one_customer
from functions.users import one_user
from models.kpi import Kpi
from models.users import Users
from schemas.kpi import KpiBase, KpiCreate, KpiUpdate
from utils.pagination import pagination


def all_kpis(search, status, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Kpi.percentage.like(search_formatted) | \
		              Kpi.roll.like(search_formatted)
	else:
		search_filter=Kpi.id > 0
	if status in [True, False]:
		status_filter=Kpi.status == status
	else:
		status_filter=Kpi.status.in_([True, False])
	
	kpis=db.query(Kpi).options(
		joinedload(Kpi.user).load_only(Users.name)).filter(search_filter, status_filter).order_by(Kpi.id.desc())
	# join(Customers.kpis).options(joinedload(Customers.kpis).load_only(Customers.kpis, Customers.comment))
	if page and limit:
		return pagination(kpis, page, limit)
	else:
		return kpis.all()


def one_kpi(id, db):
	return db.query(Kpi).options(
		joinedload(Kpi.user).load_only(Users.name)).filter(Kpi.id == id).first()


def create_kpi(form,user, db):
	if one_user(user, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	
	if one_user(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ishchi mavjud emas")
	
	new_kpi_db=Kpi(
		percentage=form.percentage,
		source_id=form.source_id,
		user_id=user.id
	
	)
	db.add(new_kpi_db)
	db.commit()
	db.refresh(new_kpi_db)
	return new_kpi_db


def update_kpi(form,user, db):
	if one_kpi(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli kpi mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	if one_user(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ishchi mavjud emas")
	
	db.query(Kpi).filter(Kpi.id == form.id).update({
		Kpi.id: form.id,
		Kpi.source_id: form.source_id,
		Kpi.status: form.status,
		Kpi.percentage: form.percentage,
		Kpi.user_id: user.id
	})
	db.commit()
	return one_kpi(form.id, db)


def filter_kpi(source_id, db, status=True):
	if status in [True, False]:
		status_filter=Kpi.status == status
	else:
		status_filter=Kpi.id > 0
	
	if source_id:
		source_filter=Kpi.source_id == source_id
	else:
		source_filter=Kpi.id > 0
	
	users=db.query(Kpi).options(
		joinedload(Kpi.user).load_only(Users.name)).filter(status_filter, source_filter).order_by(Kpi.id.asc())
	
	return users.first()


def kpi_delete(id, db):
	if one_kpi(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Kpi).filter(Kpi.id == id).update({
		Kpi.status: False,
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}
