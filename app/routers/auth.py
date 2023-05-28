from .. import models, schemas, utils, database, utils, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import sqlalchemy
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends()
          , db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user not exist")
    
    if not utils.verify(user_credential.password, str(user.password)): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credential")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
