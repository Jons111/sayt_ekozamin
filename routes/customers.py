from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from .notification import manager
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.customers import one_customer, create_customer, update_customer, all_customers, customer_delete

from schemas.customers import *
from schemas.users import *

router_customer=APIRouter()


@router_customer.post('/add', )
def add_customer(form: CustomerCreate, db: Session = Depends(get_db), current_user: UserBase = Depends(
	get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user
	if create_customer(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_customer.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: UserBase = Depends(get_current_active_user)):
	await manager.connect(websocket, user)
	try:
		while True:
			data=await websocket.receive_text()
			await manager.send_personal_message(f"You add {data}", websocket)
			await manager.broadcast(f"Client{user} added {data}")
	except WebSocketDisconnect:
		manager.disconnect(websocket)
		await manager.broadcast(f"Client {user} left chat")


@router_customer.get('/', status_code=200)
def get_customers(search: str = None, status: bool = True, id: int = 0, user_id: int = 0, page: int = 1,
                  limit: int = 25, db: Session = Depends(get_db), current_user: CustomerBase = Depends(
		get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
	if id:
		return one_customer(id, db)
	
	else:
		return all_customers(search, status, user_id, page, limit, db, )


@router_customer.put("/update")
def customer_update(form: CustomerUpdate, db: Session = Depends(get_db),
                    current_user: CustomerBase = Depends(get_current_active_user)):
	if update_customer(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_customer.delete('/{id}', status_code=200)
def delete_customer(id: int = 0, db: Session = Depends(get_db), current_user: CustomerBase = Depends(
	get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
	if id:
		return customer_delete(id, current_user, db)
