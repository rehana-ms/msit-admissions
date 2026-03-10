from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schemas,models
#from . database import engine, SessionLocal,get_db
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import admin_users,Gat_Halltickets,Gat_Call_Letters,send_emails,login
from .database import engine, SessionLocal






      
################# initializing FastAPI  to app#############################
app=FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(login.router)
app.include_router(admin_users.router)
app.include_router(Gat_Halltickets.router)
app.include_router(Gat_Call_Letters.router)
app.include_router(send_emails.router)






