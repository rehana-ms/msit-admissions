from fastapi import APIRouter,Depends,status
from .. import schemas,database,models,token
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi import FastAPI,Depends,status,Response,HTTPException
from datetime import datetime, timedelta
from fastapi.security import  OAuth2PasswordRequestForm


router=APIRouter(
      tags=['login'])

@router.post('/login')
def login(request:OAuth2PasswordRequestForm= Depends(),db:Session=Depends(database.get_db)):
      user=db.query(models.Admin).filter(models.Admin.email_id==request.username).first()
      if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")
      if not Hash.verify(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect Password")
      access_token = token.create_access_token(
        data={"sub": user.email_id}
      )
      return {"access_token": access_token, "token_type": "bearer"}
