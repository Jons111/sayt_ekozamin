from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.trades import one_trade, all_trades, create_trade, update_trade, get_order_id_from_trades
from schemas.trades import TradeCreate, TradeBase, TradeUpdate

router_trade = APIRouter()


@router_trade.post('/add', )
def add_trade(form: TradeCreate, db: Session = Depends(get_db),current_user: TradeBase = Depends(get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user)
	if create_trade(form,current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_trade.get('/', status_code=200)
def get_trades(search: str = None, status: bool = True, id: int = 0, order_id: int = 0, page: int = 1, limit: int = 25,
               db: Session = Depends(get_db),current_user: TradeBase = Depends(get_current_active_user) ):  # current_user: User = Depends(get_current_active_user)
	if id:
		return one_trade(id, db)
	
	else:
		return all_trades(search, status, order_id, page, limit, db, )


@router_trade.put("/update")
def trade_update(form: TradeUpdate, db: Session = Depends(get_db),current_user: TradeBase = Depends(get_current_active_user) ):
	if update_trade(form,current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_trade.get('/order', status_code=200)
def get_order_id(order_id: int, user_id: int, db: Session = Depends(get_db),current_user: TradeBase = Depends(get_current_active_user)):
	return get_order_id_from_trades(id=order_id, user_id=user_id, db=db)
