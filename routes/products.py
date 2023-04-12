
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.products import one_product, all_products, create_product, update_product, product_delete
from schemas.products import ProductCreate,ProductBase,ProductUpdate

router_product = APIRouter()



@router_product.post('/add', )
def add_product(form: ProductCreate, db: Session = Depends(get_db),current_user: ProductBase = Depends(get_current_active_user) ) : #current_user: CustomerBase = Depends(get_current_active_user
    if create_product(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_product.get('/',  status_code = 200)
def get_products(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: ProductBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_product(id, db)
    else :
        return all_products(search,status, page, limit, db,)


@router_product.put("/update")
def product_update(form: ProductUpdate, db: Session = Depends(get_db),current_user: ProductBase = Depends(get_current_active_user)) :
    if update_product(form,current_user,  db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_product.delete('/{id}',  status_code = 200)
def delete_product(id: int = 0,db: Session = Depends(get_db),current_user: ProductBase = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return product_delete(id,current_user, db)
    










