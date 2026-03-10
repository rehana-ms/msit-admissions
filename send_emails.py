from fastapi import  APIRouter
from .. import schemas,database,models,oauth2
from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from ..database import engine, SessionLocal,get_db
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel, EmailStr
from fastapi import BackgroundTasks, UploadFile, File, Form
from starlette.responses import FileResponse, JSONResponse
from starlette.requests import Request
import os

router=APIRouter(
      tags=['Email_Sending_Call_Letter']
      )

conf = ConnectionConfig(
    MAIL_USERNAME = "sanvi89sharma@gmail.com",
    MAIL_PASSWORD = "sani@496",
    MAIL_FROM = "sanvi89sharma@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="MSIT Admissions 2021",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)

html = """
<html>
<head>
    <meta charset="UTF-8">
    <title>Hall Ticket</title>
</head>
<body>

<h1 style="border:rgb(0, 132, 255); border-width:5px; border-style:solid; border-bottom: hidden; text-align:center; background-color: skyblue; color:white;  padding: 0px; margin: 0px">MSIT Admissions</h1>
<p style="border: rgb(0, 132, 255); border-width:5px; border-style: ridge; text-align:lift; background-color: white; color: black; padding: 50px; margin: 0px;">Student Name: <br> <br> Exam date & time are given below <br> please go through the attachments</p>

</body>

</html>
"""

@router.get('/CallLetter_email', status_code=status.HTTP_201_CREATED,response_model=List[schemas.show_Gat_call_Letter])
async def simple_send(
      db: Session=Depends(get_db),get_current_user:schemas.Admin=Depends(oauth2.get_current_user)
      ) -> JSONResponse:
      
      users=db.query(models.Gat_call_letter).all()
      path="./gatcallletters/"
      
      
      for i in range(len(users)):
            v=users[i].appno
            file=os.path.abspath(path+v+".pdf")
            message = MessageSchema(
                  subject="MSIT CallLetter 2021",
                  recipients=[users[i].email_id],
                  body=html,
                  attachments=[file],
                  subtype="html"
                  )

            fm = FastMail(conf)
            await fm.send_message(message)

      return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.get('/Hall_ticket_email', status_code=status.HTTP_201_CREATED,response_model=List[schemas.GatHallticket])
async def simple_send(
      db: Session=Depends(get_db),get_current_user:schemas.Admin=Depends(oauth2.get_current_user)
      ) -> JSONResponse:
      
      users=db.query(models.GatHallticket).all()
      path="./gatcallletters/"
      
      
      for i in range(len(users)):
            v=users[i].gatAppNo
            file=os.path.abspath(path+v+".pdf")
            message = MessageSchema(
                  subject="MSIT CallLetter 2021",
                  recipients=[users[i].email_id],
                  body=html,
                  attachments=[file],
                  subtype="html"
                  )

            fm = FastMail(conf)
            await fm.send_message(message)

      return JSONResponse(status_code=200, content={"message": "email has been sent"})


