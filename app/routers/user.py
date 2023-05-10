import models, schemas, utils, database
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    #hash the password
    user.password = utils.hash(user.password)
    
    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=f"User with id:{id} does not exist")
    
    return user