
from fastapi import FastAPI


from routes import auth,users,phones,customers,products,orders,trades,kpi,kpi_history,incomes,expenses,extra,nasiya
from db import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Eko zamin",

)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {"message":"Welcome"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'],
	responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    users.router_user,
    prefix='/user',
    tags=['User section'],
	responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    phones.router_phone,
    prefix='/phone',
    tags=['Phone section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)


app.include_router(
    customers.router_customer,
    prefix='/customer',
    tags=['Customer section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    products.router_product,
    prefix='/product',
    tags=['Product section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    orders.router_order,
    prefix='/order',
    tags=['Order section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    trades.router_trade,
    prefix='/trade',
    tags=['Trade section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    kpi.router_kpi,
    prefix='/kpi',
    tags=['Kpi section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    kpi_history.router_kpi_history,
    prefix='/kpi_history',
    tags=['Kpi history section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    incomes.router_income,
    prefix='/income',
    tags=['Income section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    expenses.router_expense,
    prefix='/expense',
    tags=['Expense section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    extra.router_extra,
    prefix='/extra',
    tags=['Extra section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    nasiya.router_nasiya,
    prefix='/nasiya',
    tags=['Nasiya section'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

# app.include_router(
#     uploaded_files.router_uploaded_file,
#     prefix='/upload_file',
#     tags=['Upload file section'],
#     responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
# )