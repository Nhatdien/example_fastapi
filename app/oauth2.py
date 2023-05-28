from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import database, models
from . import schemas
from .config import settings

oauth2_schemes = OAuth2PasswordBearer(tokenUrl="login")


#SECRET KEY
SECRET_KEY = settings.secret_key
#alogrithm
ALGORITHM = settings.algorithm
#Expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() # type: ignore

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)

        id :str = payload.get("user_id") #type: ignore

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user(token: schemas.TokenData = Depends(oauth2_schemes),
                     db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Couldn't validate credential",
                                         headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credential_exception)  #type: ignore

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user


