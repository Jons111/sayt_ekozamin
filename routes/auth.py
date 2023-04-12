from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session


from schemas.login import TokenData
from db import get_db
from schemas.users import UserBase
from models.users import Users


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1111


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


login_router = APIRouter()


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = 400, detail = "Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(Users).where(Users.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    if current_user.status :
        return current_user
    raise HTTPException(status_code = 400, detail="Inactive user")


@login_router.post("/token")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Users).where(Users.username == form_data.username, Users.status == True).first()
    if user:
        is_validate_password = pwd_context.verify(form_data.password, user.password)
    else:
        is_validate_password = False
    if not is_validate_password:
        raise HTTPException(status_code = 400, detail="Login yoki parolda xatolik")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    db.query(Users).filter(Users.username == user.username).update({
        Users.token: access_token
    })
    db.commit()
    return {'id': user.id, "access_token": access_token, "roll": user.roll}

# import time
# from passlib.context import CryptContext
# from jose import jwt,JWTError
# from fastapi import Depends, APIRouter, HTTPException
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#
# from sqlalchemy.orm import Session
# from starlette import status
#
# from db import get_db
# from models.users import Users
# from schemas.users import TokenData, Token
#
# router=APIRouter()
#
# # setups for JWT
# SECRET_KEY = 'SOME-SECRET-KEY'
# ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
#
#
# def create_access_token(data:dict):
#     print(data)
#     payload= data.copy()
#     payload.update( {'exp':time.time()+ACCESS_TOKEN_EXPIRE_MINUTES}
#     )
#     token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
#     return token
#
#
# def verify_access_token(token:str,credentials_exceration):
#     try:
#         decode_token = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
#         id:str = decode_token.get('user_id')
#         if id is None:
#             raise credentials_exceration
#         token_data = TokenData(id=id)
#     except JWTError :
#         raise credentials_exceration
#     return token_data
#
#
# def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
#     credentional_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                            detail="User not validated")
#     token = verify_access_token(token,credentional_exception)
#     user= db.query(Users).filter(Users.id == token.id).first()
#
#     return user
#
# def hash(password:str):
#     return pwd_context.hash(password)
#
#
# def verify(plain_password,hashed_password):
#     return pwd_context.verify(plain_password,hashed_password)
#
# @router.post('/login', response_model=Token )
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
#
#     user = db.query(Users).filter(Users.username == user_credentials.username).first()
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid username!!!")
#
#     if not verify(user_credentials.password,user.password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,detail="Invalid password"
#         )
#
#
#     access_token = create_access_token(data={'user_id':user.id})
#     return {"access_token":access_token,"type":'Bearer'}


























